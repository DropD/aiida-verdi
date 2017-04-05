# -*- coding: utf8 -*-
"""
Computer :py:mod:`click` group
"""
import click
from click_plugins import with_plugins


@click.group()
def computer():
    """
    commandline interface for managing AiiDA codes
    """
