from computer import computer
from setup import setup
from list import list_
from show import show


computer.add_command(setup, 'setup')
computer.add_command(list_, 'list')
computer.add_command(show, 'show')

__all__ = [computer]
