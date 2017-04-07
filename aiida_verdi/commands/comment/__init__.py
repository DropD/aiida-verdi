# -*- coding: utf-8 -*-
"""
gather subcommands for verdi comment
"""
from comment import comment
from add import add
from show import show


comment.add_command(add)
comment.add_command(show)


__all__ = [comment]
