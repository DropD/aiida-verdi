# -*- coding: utf-8 -*-
"""
verdi code rename
"""

import click

from aiida_verdi import arguments, options


@click.command()
@arguments.code()
@arguments.codelabel()
@options.dry_run()
def rename(code, name, dry_run):
    """
    rename CODE (change it's label) to NAME
    """

    compname = code.get_computer().name
    old_name = '{}@{}'.format(code.label, compname)
    if not dry_run:
        code.label = name
        new_name = '{}@{}'.format(code.label, compname)
        click.echo("renamed '{}' to '{}' (ID={})".format(old_name, new_name, code.pk))
    else:
        new_name = '{}@{}'.format(name, compname)
        click.echo("not renaming '{}' to '{}' (ID={}), --dry-run recieved)".format(
            old_name, new_name, code.pk))

