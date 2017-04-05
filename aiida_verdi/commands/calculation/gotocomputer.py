# -*- coding: utf-8 -*-
"""
verdi calculation gotocomputer
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.calculation()
@options.dry_run()
def gotocomputer(calc, dry_run):
    """
    Open a shell to the work folder for CALCULATION on the cluster

    This command opens a ssh connection to the scratch folder on the remote
    computer on which CALCULATION is being/has been executed.
    """
    import os

    from aiida.common.exceptions import NotExistent

    # get the transport
    try:
        t = calc._get_transport()
    except NotExistent as e:
        raise click.ClickException(e.message)
    # get the remote directory
    remotedir = calc._get_remote_workdir()
    if not remotedir:
        raise click.ClickException("No remote work directory is set for this calculation! (It is possible that the daemon did not submit the calculation yet)")

    # get the command to run (does not require to open the connection!)
    cmd_to_run = t.gotocomputer_command(remotedir)
    # Connect (execute command)
    # print cmd_to_run
    if not dry_run:
        click.echo("Going the the remote folder...")
        os.system(cmd_to_run)
    else:
        click.echo("The command to go to the remote folder:")
        click.echo(cmd_to_run)
        click.echo("\nNot going to the remote folder (--dry-run recieved).\n")
