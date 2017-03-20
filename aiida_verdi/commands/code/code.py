#-*- coding: utf8 -*-
"""
verdi code commands
"""
import click
from click_plugins import with_plugins
# ~ from pkg_resources import iter_entry_points


# ~ @with_plugins(iter_entry_points('aiida.cmdline.code'))
@click.group('code')
def code_():
    """
    manage codes in your AiiDA database.
    """
