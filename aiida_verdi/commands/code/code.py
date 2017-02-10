#-*- coding: utf8 -*-
"""
verdi code commands
"""
import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

from aiida_verdi import options
from aiida_verdi.verdic_utils import (load_dbenv_if_not_loaded,
                                      create_code, InteractiveOption)
from aiida_verdi.utils.interactive import InteractiveOption
from aiida_verdi.param_types.code import CodeParam
from aiida_verdi.param_types.plugin import PluginParam
from aiida_verdi.param_types.computer import ComputerParam


@with_plugins(iter_entry_points('aiida.cmdline.code'))
@click.group()
def code():
    """
    manage codes in your AiiDA database.
    """
