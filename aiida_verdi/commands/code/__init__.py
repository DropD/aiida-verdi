from code import code
from list import _list
from setup import setup
from show import show


code.add_command(_list, name='list')
code.add_command(setup, name='setup')
code.add_command(show, name='show')

__all__=[code]
