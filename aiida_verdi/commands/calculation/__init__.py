# -*- coding: utf-8 -*-
"""
assemble calculation subcommands
"""
from aiida_verdi.commands.calculation.calculation import calculation
from aiida_verdi.commands.calculation.gotocomputer import gotocomputer
from aiida_verdi.commands.calculation.list import list_
from aiida_verdi.commands.calculation.res import res
from aiida_verdi.commands.calculation.show import show
from aiida_verdi.commands.calculation.logshow import logshow
from aiida_verdi.commands.calculation.plugins import plugins


calculation.add_command(gotocomputer)
calculation.add_command(list_, name='list')
calculation.add_command(res)
calculation.add_command(show)
calculation.add_command(logshow)
calculation.add_command(plugins)


__all__ = [calculation]
