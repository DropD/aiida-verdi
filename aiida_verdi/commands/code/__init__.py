from code import code
from list import _list
from setup import setup
from show import show
from hide import hide, reveal
from rename import rename
from update import update


code.add_command(_list, name='list')
code.add_command(setup, name='setup')
code.add_command(show, name='show')
code.add_command(hide, name='hide')
code.add_command(reveal, name='reveal')
code.add_command(rename, name='rename')
code.add_command(update, name='update')

__all__=[code]
