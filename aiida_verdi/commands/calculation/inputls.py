# -*- coding: utf-8 -*-
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.calculation()
@options.path(default='', help="The relative path of the file you want to show. If not specified, show content of all the 'raw_input' directory")
@options.color(help="Color folders with a different color")
def inputls(calc, path, color):
    """
    Show the list of input files of CALCULATION (a calculation node).

    It shows the files in the raw_input subdirectory.
    """
    import os

    from aiida.common.exceptions import NotExistent
    from aiida.cmdline.commands.node import list_repo_files

    try:
        list_repo_files(calc, os.path.join('raw_input', path), color)
    except ValueError as e:
        raise click.ClickException(e.message)
