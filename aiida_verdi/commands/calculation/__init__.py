# -*- coding: utf-8 -*-
"""
assemble calculation subcommands
"""
from aiida_verdi.commands.calculation.calculation import calculation
from aiida_verdi.commands.calculation.gotocomputer import gotocomputer


calculation.add_command(gotocomputer)


__all__ = [calculation]
