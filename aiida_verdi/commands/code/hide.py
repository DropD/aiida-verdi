# -*- coding: utf-8 -*-
"""
verdi code hide
"""
import click

from aiida_verdi.arguments import code
from aiida_verdi.options import dry_run


@click.command()
@code(nargs=-1)
@dry_run()
def hide(_code, dry_run):
    """
    Hide one or more codes form the verdi list command
    """
    if not dry_run:
        for c in _code:
            c._hide()
            click.echo('{} hidden'.format(c.label))
    else:
        click.echo('not hiding (--dry-run recieved): {}'.format([c.label for c in _code]))

@click.command()
@code(nargs=-1)
@dry_run()
def reveal(_code, dry_run):
    """
    Unhide one or more codes from the verdi list command
    """
    if not dry_run:
        for c in _code:
            click.echo('{} revealed'.format(c.label))
            c._reveal()
    else:
        click.echo('not revealing (--dry-run recieved): {}'.format([c.label for c in _code]))
