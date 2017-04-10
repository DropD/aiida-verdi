# -*- coding: utf-8 -*-
"""
verdi daemon restart
"""
import click


@click.command()
def restart():
    """
    Restart the daemon. Before restarting, wait for the daemon to really
    shut down.
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv(process='daemon')
    from aiida_verdi.utils.daemon import get_daemon_pid

    from aiida.backends.utils import get_daemon_user
    from aiida.common.utils import get_configured_user_email

    daemon_user = get_daemon_user()
    this_user = get_configured_user_email()

    if daemon_user != this_user:
        print "You are not the daemon user! I will not restart the daemon."
        print "(The daemon user is '{}', you are '{}')".format(
            daemon_user, this_user)
        return 1

    pid = get_daemon_pid()

    dead = True

    if pid is not None:
        from aiida_verdi.commands.daemon.stop import stop
        dead = stop.main(args=[], standalone_mode=False)

    if dead is None:
        click.echo("Check the status and, when the daemon will be down, ")
        click.echo("you can restart it using:")
        click.echo("    verdi daemon start")
    else:
        from aiida_verdi.commands.daemon.start import start
        start.main(args=[], standalone_mode=False)
