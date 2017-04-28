# -*- coding: utf-8 -*-
"""
verdi calculation outputcat
"""
import click
from aiida_verdi import arguments, options


@click.command()
@arguments.calculation()
@options.path(help="The relative path of the file you want to show. Take the default output file if it is not specified")
def outputcat(calc, path):
    """
    Show an output file of a CALCULATION node.

    It shows the files in the 'path' subdirectory of the output node
    of files retrieved by the parser. Therefore, this will not work
    before files are retrieved by the daemon.
    Use the -h option for more help on the command line options.
    """
    import os

    from aiida.cmdline.commands.node import cat_repo_files
    from aiida.common.old_pluginloader import get_class_typestring

    if path is None:
        path = calc._DEFAULT_OUTPUT_FILE
        if path is None:
            base_class, plugin_string, class_name = get_class_typestring(
                calc._plugin_type_string)
            raise click.ClickException("Calculation '{}' does not define a default output file. Please specify a path explicitly".format(plugin_string))

    try:
        parsed_node = calc.out.retrieved
    except AttributeError:
        raise click.ClickException("No 'retrieved' node found. Have the calculation files already been retrieved?")

    try:
        cat_repo_files(parsed_node, os.path.join('path', path))
        click.echo()
    except ValueError as e:
        raise click.ClickException(e.message)
    except IOError as e:
        import errno
        # Ignore Broken pipe errors, re-raise everything else
        if e.errno == errno.EPIPE:
            pass
        else:
            raise
