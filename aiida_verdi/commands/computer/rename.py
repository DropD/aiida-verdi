# -*- coding: utf-8 -*-
"""
verdi computer rename
"""
import click
from aiida_verdi import options, arguments


@click.command()
@arguments.computer()
@click.argument('name', metavar='NEW_NAME')
@options.dry_run()
def rename(computer, name, dry_run):
    """
    Rename COMPUTER in your database to NEW_NAME
    """
    if not dry_run:
        try:
            computer.set_name(name)
            computer.store()
        except ValidationError as e:
            raise click.BadParameter("Invalid name argument! {}".format(e.message))
        except UniquenessError as e:
            raise click.BadParameter(("Uniqueness error encountered! Probably a "
                                      "computer with name '{}' already exists"
                                      "\n(Message was: {})".format(wname, e.message)))
    else:
        click.echo('not renaming {} to {} (--dry-run recieved)'.format(computer.name, name))
