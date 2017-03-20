# -*- coding: utf-8 -*-
"""
verdi code hide
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.code(nargs=-1)
@options.dry_run()
def hide(code, dry_run):
    """
    Hide one or more codes form the verdi list command
    """
    if not dry_run:
        for c in code:
            c._hide()
            click.echo('{} hidden'.format(c.label))
    else:
        click.echo('not hiding (--dry-run recieved): {}'.format([c.label for c in code]))

@click.command()
@arguments.code(nargs=-1)
@options.dry_run()
def reveal(code, dry_run):
    """
    Unhide one or more codes from the verdi list command
    """
    if not dry_run:
        for c in code:
            click.echo('{} revealed'.format(c.label))
            c._reveal()
    else:
        click.echo('not revealing (--dry-run recieved): {}'.format([c.label for c in code]))
