# -*- coding: utf-8 -*-
"""
gather subcommands for verdi comment
"""
from comment import comment
from add import add


comment.add_command(add)


__all__ = [comment]
