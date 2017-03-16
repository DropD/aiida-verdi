#-*- coding: utf8 -*-
"""
verdi plugin command group
"""
import click
from click_plugins import with_plugins
# ~ from pkg_resources import iter_entry_points


# ~ @with_plugins(iter_entry_points('aiida.cmdline.plugin'))
@click.group()
def plugin():
    """
    commandline interface for plugin management
    """
