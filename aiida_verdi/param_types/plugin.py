#-*- coding: utf8 -*-
"""
click parameter type for Plugins
"""
import click
from click_completion import startswith

from aiida_verdi.verdic_utils import aiida_dbenv, input_plugin_validator


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
        self.validator = input_plugin_validator()

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

    def unsafe_convert(self, value, param, ctx):
        """check value vs. possible plugins, raising BadParameter on fail """
        # ~ if not value in self.get_all_plugins():
            # ~ raise click.BadParameter('Must be an installed plugin')
        # ~ return value
        return self.validator.throw(ctx, param, value)

    def safe_convert(self, value, param, ctx):
        """check value vs. possible plugins without raising"""
        # ~ try:
            # ~ value = self.unsafe_convert(value, param, ctx)
        # ~ except click.BadParameter as e:
            # ~ click.echo(e.format_message())
        # ~ return value
        return self.validator(ctx, param, value)
