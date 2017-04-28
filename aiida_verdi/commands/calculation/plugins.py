# -*- coding: utf-8 -*-
"""
verdi calculation plugins
"""
import click

from aiida_verdi import arguments


@click.command()
@arguments.input_plugin(metavar='PLUGIN NAME', nargs=-1)
def plugins(input_plugin):
    """
    Show available calculation plugins.

    Pass one or multiple PLUGIN NAMEs to get more details on them.
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()

    from aiida.orm import CalculationFactory
    from aiida.orm.calculation.job import JobCalculation
    from aiida.common.pluginloader import all_plugins
    from aiida.common.exceptions import MissingPluginError

    names = input_plugin

    if names:
        for name in names:
            try:
                C = CalculationFactory(name)
                click.echo("* {}".format(name))
                docstring = C.__doc__
                if docstring is None:
                    docstring = "(No documentation available)"
                docstring = docstring.strip()
                click.echo("\n".join(["    {}".format(_.strip()) for _ in docstring.splitlines()]))
                click.echo("  Inputs:")
                for key, val in C._use_methods.iteritems():
                    if isinstance(val['valid_types'], (list, tuple)):
                        v_types = val['valid_types']
                    else:
                        v_types = tuple([val['valid_types']])
                    click.echo("    {}: {}".format(key, [i.__name__ for i in v_types]))
                click.echo("  Module location: {}".format(C.__module__))

            except MissingPluginError:
                click.echo("! {}: NOT FOUND OR FAILED TO LOAD!".format(name))
    else:
        plugins = sorted(all_plugins('calculations'))
        if plugins:
            click.echo("## Pass as a further parameter one (or more) plugin names to get more details on a given plugin.")
            for plugin in plugins:
                click.echo("* {}".format(plugin))
        else:
            click.echo("## No calculation plugins found")
