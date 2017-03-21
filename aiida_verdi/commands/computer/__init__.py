from computer import computer
from setup import setup
from list import list_
from show import show
from update import update


computer.add_command(setup, 'setup')
computer.add_command(list_, 'list')
computer.add_command(show, 'show')
computer.add_command(update, 'update')

__all__ = [computer]
