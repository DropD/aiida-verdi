#-*- coding: utf8 -*-
"""
show detailed info about a specific plugin
"""
import click


@click.command()
@click.argument('name')
def info(name):
    """
    display detailed info about a plugin
    """
    from aiida_verdi.verdic_utils import load_dbenv_if_not_loaded
    from aiida.plugins.info import find_by_name
    load_dbenv_if_not_loaded()
    entry = find_by_name(name)
    click.echo(entry.format_info(format='tabulate', as_str=True))
