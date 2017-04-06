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
from aiida_verdi.commands.calculation.inputcat import inputcat
from aiida_verdi.commands.calculation.inputls import inputls


calculation.add_command(gotocomputer)
calculation.add_command(list_, name='list')
calculation.add_command(res)
calculation.add_command(show)
calculation.add_command(logshow)
calculation.add_command(plugins)
calculation.add_command(inputcat)
calculation.add_command(inputls)


__all__ = [calculation]
