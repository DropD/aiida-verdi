from code import code_ as code
from list import list_
from setup import setup
from show import show
from hide import hide, reveal
from rename import rename
from update import update
from delete import delete


code.add_command(list_, name='list')
code.add_command(setup, name='setup')
code.add_command(show, name='show')
code.add_command(hide, name='hide')
code.add_command(reveal, name='reveal')
code.add_command(rename, name='rename')
code.add_command(update, name='update')
code.add_command(delete, name='delete')

__all__=[code]
