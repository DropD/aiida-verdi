# -*- coding: utf-8 -*-
"""
verdi computer enable
"""
import click
from aiida_verdi import arguments, options


@click.command()
@arguments.computer()
@options.user(help='Enable only for USER, if not given, enable globally')
@options.dry_run()
def enable(computer, user, dry_run):
    """
    Enable COMPUTER (allow calculations to be run on it)
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.common.exceptions import NotExistent

    if not user:
        if computer.is_enabled():
            click.echo("Computer '{}' already enabled.".format(computer.name))
        else:
            if not dry_run:
                computer.set_enabled_state(True)
                click.echo("Computer '{}' enabled.".format(computer.name))
            else:
                click.echo("Computer '{}' not enabled (--dry-run recieved).".format(computer.name))

    else:
        try:
            dbauthinfo = computer.get_dbauthinfo(user._dbuser)
            if not dbauthinfo.enabled:
                if not dry_run:
                    dbauthinfo.enabled = True
                    dbauthinfo.save()
                    click.echo("Computer '{}' enabled for user {}.".format(
                        computer.name, user.get_full_name()))
                else:
                    click.echo("Computer '{}' not enabled for user {} (--dry-run recieved).".format(
                        computer.name, user.get_full_name()))
            else:
                click.echo("Computer '{}' was already enabled for user {} {}.".format(
                    computer.name, user.first_name, user.last_name))
        except NotExistent:
            raise click.ClickException("User with email '{}' is not configured for computer '{}' yet.".format(
                user.email, computer.name))
