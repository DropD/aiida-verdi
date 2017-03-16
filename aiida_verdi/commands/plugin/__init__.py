from plugin import plugin
from info import info
from search import search


plugin.add_command(info)
plugin.add_command(search)

__all__ = [plugin]
