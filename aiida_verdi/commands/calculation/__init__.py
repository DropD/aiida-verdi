# -*- coding: utf-8 -*-
"""
assemble calculation subcommands
"""
from aiida_verdi.commands.calculation.calculation import calculation
from aiida_verdi.commands.calculation.gotocomputer import gotocomputer
from aiida_verdi.commands.calculation.list import list_


calculation.add_command(gotocomputer)
calculation.add_command(list_, name='list')


__all__ = [calculation]
