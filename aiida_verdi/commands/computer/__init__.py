# -*- coding: utf-8 -*-
"""
assemble computer subcommands
"""
from aiida_verdi.commands.computer.computer import computer
from aiida_verdi.commands.computer.setup import setup
from aiida_verdi.commands.computer.list import list_
from aiida_verdi.commands.computer.show import show
from aiida_verdi.commands.computer.update import update
from aiida_verdi.commands.computer.rename import rename
from aiida_verdi.commands.computer.configure import configure
from aiida_verdi.commands.computer.delete import delete
from aiida_verdi.commands.computer.test import test
from aiida_verdi.commands.computer.enable import enable
from aiida_verdi.commands.computer.disable import disable


computer.add_command(setup, 'setup')
computer.add_command(list_, 'list')
computer.add_command(show, 'show')
computer.add_command(update, 'update')
computer.add_command(rename, 'rename')
computer.add_command(configure, 'configure')
computer.add_command(delete, 'delete')
computer.add_command(test, 'test')
computer.add_command(enable, 'enable')
computer.add_command(disable, 'disable')

__all__ = [computer]
