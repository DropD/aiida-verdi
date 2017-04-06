# -*- coding: utf-8 -*-
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.calculation()
@options.path(default='', help="The relative path of the file you want to show. If not specified, show content of all the 'raw_input' directory")
@options.color(help="Color folders with a different color")
def outputls(calc, path, color):
    """
    Show the list of output files of a CALCULATION node.

    It lists the files in the 'path' subdirectory of the output node
    of files retrieved by the parser. Therefore, this will not work
    before files are retrieved by the daemon.
    """
    import os

    from aiida.cmdline.commands.node import list_repo_files

    try:
        parsed_node = calc.out.retrieved
    except AttributeError:
        raise click.ClickException("No 'retrieved' node found. Have the calculation files already been retrieved?")

    try:
        list_repo_files(parsed_node,
                        os.path.join('path', path),
                        color)
    except ValueError as e:
        raise click.ClickException(e.message)

