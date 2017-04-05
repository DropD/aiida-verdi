# -*- coding: utf-8 -*-
"""
verdi computer enable
"""
import click
from aiida_verdi import arguments, options


@click.command()
@arguments.computer()
@options.user(help='Disable only for USER, if not given, disable globally')
@options.dry_run()
def disable(computer, user, dry_run):
    """
    Disable COMPUTER (disallow calculations to be run on it)
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.common.exceptions import NotExistent

    if not user:
        if not computer.is_enabled():
            click.echo("Computer '{}' already disabled.".format(computer.name))
        else:
            if not dry_run:
                computer.set_enabled_state(False)
                click.echo("Computer '{}' disabled.".format(computer.name))
            else:
                click.echo("Computer '{}' not disabled (--dry-run recieved).".format(computer.name))

    else:
        try:
            dbauthinfo = computer.get_dbauthinfo(user._dbuser)
            if dbauthinfo.enabled:
                if not_dry_run:
                    dbauthinfo.enabled = False
                    dbauthinfo.save()
                    click.echo("Computer '{}' disabled for user {}.".format(
                        computer.name, user.get_full_name()))
                else:
                    click.echo("Computer '{}' not disabled for user {} (--dry-run recieved).".format(
                        computer.name, user.get_full_name()))
            else:
                click.echo("Computer '{}' was already disabled for user {} {}.".format(
                    computer.name, user.first_name, user.last_name))
        except NotExistent:
            raise click.ClickException("User with email '{}' is not configured for computer '{}' yet.".format(
                user.email, computer.name))
