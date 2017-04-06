# -*- coding: utf-8 -*-
"""
verdi calculation kill
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.calculation(nargs=-1)
@options.force(help='Force the kill of calculations')
@options.non_interactive()
@options.dry_run()
def kill(calc, force, non_interactive, dry_run):
    """
    Kill AiiDA CALCULATIONs.
    """
    from aiida.common.exceptions import InvalidOperation, RemoteOperationError
    calcs = calc
    '''noop if no calcs given'''
    if not calcs:
        return 0

    if not force:
        if non_interactive:
            return 0
        question = "Are you sure to kill {} calculation{}?".format(len(calcs), "" if len(calcs) == 1 else "s")
        click.confirm(question, abort=True)

    counter = 0
    for c in calcs:
        try:
            if not dry_run:
                c.kill()  # Calc.kill(calc_pk)
            counter += 1
        except (InvalidOperation, RemoteOperationError) as e:
            raise click.ClickException(e.message)

    msg_vars = {
        'num': counter,
        's': "" if counter == 1 else "s",
        'not': 'not ' if dry_run else '',
        'dry_run': ' (--dry-run recieved)' if dry_run else ''
    }
    click.echo("{num} calculation{s} {not}killed{dry_run}.".format(**msg_vars))
