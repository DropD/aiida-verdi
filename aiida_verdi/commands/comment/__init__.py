# -*- coding: utf-8 -*-
"""
gather subcommands for verdi comment
"""
from aiida_verdi.commands.comment.comment import comment
from aiida_verdi.commands.comment.add import add
from aiida_verdi.commands.comment.show import show
from aiida_verdi.commands.comment.remove import remove


comment.add_command(add)
comment.add_command(show)
comment.add_command(remove)


__all__ = ['comment']
