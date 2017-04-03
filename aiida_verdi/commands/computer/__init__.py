# -*- coding: utf-8 -*-
"""
collecting computer subcommands
"""
from aiida_verdi.commands.computer.computer import computer
from aiida_verdi.commands.computer.setup import setup
from aiida_verdi.commands.computer.list import list_
from aiida_verdi.commands.computer.show import show
from aiida_verdi.commands.computer.update import update
from aiida_verdi.commands.computer.rename import rename
from aiida_verdi.commands.computer.configure import configure


computer.add_command(setup, 'setup')
computer.add_command(list_, 'list')
computer.add_command(show, 'show')
computer.add_command(update, 'update')
computer.add_command(rename, 'rename')
computer.add_command(configure, 'configure')

__all__ = [computer]
