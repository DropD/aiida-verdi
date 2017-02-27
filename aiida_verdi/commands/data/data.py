#-*- coding: utf8 -*-
"""
verdi data command group
"""
import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points


@with_plugins(iter_entry_points('aiida.cmdline.data'))
@click.group()
def data():
    """
    verdi commandline interface for working with Data nodes
    """
