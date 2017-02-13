#-*- coding: utf8 -*-
"""
Computer :py:mod:`click` group
"""
import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points


@with_plugins(iter_entry_points('aiida.cmdline.code'))
@click.group()
def computer():
    """
    commandline interface for managing AiiDA codes
    """
