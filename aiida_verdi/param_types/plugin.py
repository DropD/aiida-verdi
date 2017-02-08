#-*- coding: utf8 -*-
"""
click parameter type for Plugins
"""
import click
from click_completion import startswith

from aiida_verdi.verdic_utils import aiida_dbenv


class PluginArgument(click.ParamType):
    """
    handle verification, completion for plugin arguments
    """
    name = 'aiida plugin'

    def __init__(self, category=None, *args, **kwargs):
        self.category = category
        super(PluginArgument, self).__init__(*args, **kwargs)
        if self.category == 'calculations':
            self.get_all_plugins = self.old_get_calculations
        elif self.category == 'parsers':
            self.get_all_plugins = self.old_get_parsers
        else:
            raise ValueError('unsupported plugin category for cmdline args')

    def get_possibilities(self, incomplete=''):
        """return a list of plugins starting with incomplete"""
        return [p for p in self.get_all_plugins() if startswith(p, incomplete)]

    @aiida_dbenv
    def old_get_calculations(self):
        """return all available input plugins"""
        from aiida.common.pluginloader import existing_plugins
        from aiida.orm.calculation.job import JobCalculation
        return existing_plugins(
            JobCalculation, 'aiida.orm.calculation.job', suffix='Calculation')

    @aiida_dbenv
    def old_get_parsers(self):
        """return all available parser plugins"""
        from aiida.common.pluginloader import existing_plugins
        from aiida.parsers import Parser
        return existing_plugins(Parser, 'aiida.parsers.plugins')

    def complete(self, ctx, incomplete):
        """return possible completions"""
        return self.get_possibilities(incomplete=incomplete)

    def get_missing_message(self, param):
        return 'Possible arguments are:\n\n' + '\n'.join(self.get_all_plugins())

    def convert(self, value, param, ctx):
        """check value vs. possible plugins, raising BadParameter on fail """
        pluginlist = self.get_possibilities()
        if value not in pluginlist:
            raise click.BadParameter('{} is not a plugin for category {}'.format(value, self.category))
        return value
