# -*- coding: utf8 -*-
"""
verdi code delete
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.code()
@options.dry_run()
def delete(code, dry_run):
    """
    Delete CODE from your AiiDA Database
    """
    from aiida.common.exceptions import InvalidOperation
    from aiida.orm.code import delete_code

    label = code.label
    pk = code.pk

    if not dry_run:
        try:
            delete_code(code)
            click.echo('code {} (pk={}) deleted.'.format(label, pk))
        except InvalidOperation as e:
            click.echo(e.message, err=True)
    else:
        click.echo('code {} (pk={}) not deleted (--dry-run recieved)'.format(label, pk))
