# -*- coding: utf-8 -*-
"""
verdi code rename
"""

import click

from aiida_verdi.arguments import code, codelabel
from aiida_verdi.options import dry_run


@click.command()
@code()
@codelabel()
@dry_run()
def rename(_code, name, dry_run):
    """
    rename CODE (change it's label) to NAME
    """

    compname = _code.get_computer().name
    old_name = '{}@{}'.format(_code.label, compname)
    if not dry_run:
        _code.label = name
        new_name = '{}@{}'.format(_code.label, compname)
        click.echo("renamed '{}' to '{}' (ID={})".format(old_name, new_name, _code.pk))
    else:
        new_name = '{}@{}'.format(name, compname)
        click.echo("not renaming '{}' to '{}' (ID={}), --dry-run recieved)".format(
            old_name, new_name, _code.pk))

