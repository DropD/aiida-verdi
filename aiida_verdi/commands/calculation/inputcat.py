# -*- coding: utf-8 -*-
"""
verdi calculation inputcat
"""
import click
from aiida_verdi import arguments, options


@click.command()
@arguments.calculation()
@options.path(help="The relative path of the file you want to show. Take the default input file if it is not specified")
def inputcat(calc, path):
    """
    Write the contents of an input file for CALCULATION from the repository to stdout
    """
    import os

    from aiida.cmdline.commands.node import cat_repo_files
    from aiida.common.pluginloader import get_class_typestring

    if path is None:
        path = calc._DEFAULT_INPUT_FILE
        if path is None:
            base_class, plugin_string, class_name = get_class_typestring(
                calc._plugin_type_string)
            raise click.ClickException("Calculation '{}' does not define a default input file. Please specify a path explicitly".format(plugin_string))

    try:
        cat_repo_files(calc, os.path.join('raw_input', path))
    except ValueError as e:
        raise click.ClickException(e.message)
    except IOError as e:
        import errno
        # Ignore Broken pipe errors, re-raise everything else
        if e.errno == errno.EPIPE:
            pass
        else:
            raise
