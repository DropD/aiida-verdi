#-*- coding: utf-8 -*-
"""
assembling the verdi plugin cli
"""
from plugin import plugin
from info import info
from search import search
from update import update


plugin.add_command(info)
plugin.add_command(search)
plugin.add_command(update)

__all__ = [plugin]
