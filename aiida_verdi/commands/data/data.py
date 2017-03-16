#-*- coding: utf8 -*-
"""
verdi data command group
"""
import click

from aiida_verdi.utils.plugins import PluginGroup


@click.group(group='aiida.cmdline.data', cls=PluginGroup)
def data():
    """
    verdi commandline interface for working with Data nodes
    """
