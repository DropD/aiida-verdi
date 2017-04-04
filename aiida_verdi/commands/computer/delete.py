# -*- coding: utf8 -*-
"""
verdi computer delete
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.computer()
@options.dry_run()
def delete(computer, dry_run):
    """
    Delete COMPUTER from the database

    Does not delete the computer if there are calculations that are using
    it.
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.common.exceptions import InvalidOperation
    from aiida.orm.computer import delete_computer

    if not dry_run:
        try:
            delete_computer(computer)
        except InvalidOperation as e:
            raise click.ClickException(e.message)
        click.echo("Computer '{}' deleted.".format(computer.name))
    else:
        click.echo("Computer '{}' not deleted (--dry-run recieved).".format(computer.name))
