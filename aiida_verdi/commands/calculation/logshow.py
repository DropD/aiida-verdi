# -*- coding: utf-8 -*-
"""
verdi calculation logshow
"""
import click

from aiida_verdi import arguments


@click.command()
@arguments.calculation()
def logshow(calc):
    """
    Show the log for CALCULATION
    """
    from aiida.backends.utils import get_log_messages
    from aiida.common.datastructures import calc_states
    log_messages = get_log_messages(calc)
    label_string = " [{}]".format(calc.label) if calc.label else ""
    state = calc.get_state()
    if state == calc_states.WITHSCHEDULER:
        sched_state = calc.get_scheduler_state()
        if sched_state is None:
            sched_state = "(unknown)"
        state += ", scheduler state: {}".format(sched_state)
    click.echo("*** {}{}: {}".format(calc.pk, label_string, state))

    sched_out = calc.get_scheduler_output()
    sched_err = calc.get_scheduler_error()
    if sched_out is None:
        click.echo("*** Scheduler output: N/A")
    elif sched_out:
        click.echo("*** Scheduler output:")
        click.echo(sched_out)
    else:
        click.echo("*** (empty scheduler output file)")

    if sched_err is None:
        click.echo("*** Scheduler errors: N/A")
    elif sched_err:
        click.echo("*** Scheduler errors:")
        click.echo(sched_err)
    else:
        click.echo("*** (empty scheduler errors file)")

    if log_messages:
        click.echo("*** {} LOG MESSAGES:".format(len(log_messages)))
    else:
        click.echo("*** 0 LOG MESSAGES")

    for log in log_messages:
        click.echo("+-> {} at {}".format(log['levelname'], log['time']))
        # Print the message, with a few spaces in front of each line
        click.echo("\n".join(["|   {}".format(_) for _ in log['message'].splitlines()]))
