# -*- coding: utf-8 -*-
"""
verdi daemon status
"""
import click


@click.command()
def status():
    """
    Print the status of the daemon
    """
    import supervisor
    import supervisor.supervisorctl
    import xmlrpclib
    from pytz import UTC

    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv(process='daemon')

    from aiida.utils import timezone
    from aiida.daemon.timestamps import get_most_recent_daemon_timestamp
    from aiida.common.utils import str_timedelta

    from aiida_verdi.utils.daemon import get_daemon_pid, get_conffile_full_path

    most_recent_timestamp = get_most_recent_daemon_timestamp()

    if most_recent_timestamp is not None:
        timestamp_delta = (timezone.datetime.now(tz=UTC) -
                           most_recent_timestamp)
        click.echo("# Most recent daemon timestamp:{}".format(str_timedelta(timestamp_delta)))
    else:
        click.echo("# Most recent daemon timestamp: [Never]")

    pid = get_daemon_pid()
    if pid is None:
        click.echo("Daemon not running (cannot find the PID for it)")
        return 0

    c = supervisor.supervisorctl.ClientOptions()
    s = c.read_config(get_conffile_full_path())
    proxy = xmlrpclib.ServerProxy('http://127.0.0.1',
                                  transport=supervisor.xmlrpc.SupervisorTransport(
                                      s.username, s.password, s.serverurl))
    try:
        running_processes = proxy.supervisor.getAllProcessInfo()
    except xmlrpclib.Fault as e:
        if e.faultString == "SHUTDOWN_STATE":
            click.echo("The daemon is shutting down...")
            return 0
        else:
            raise
    except Exception as e:
        import socket
        if isinstance(e, socket.error):
            click.echo("Could not reach the daemon, I got a socket.error: ")
            click.echo("  -> [Errno {}] {}".format(e.errno, e.strerror))
        else:
            click.echo("Could not reach the daemon, I got a {}: {}".format(e.__class__.__name__, e.message))
        click.echo("You can try to stop the daemon and start it again.")
        return

    if running_processes:
        click.echo("## Found {} process{} running:".format(len(running_processes), '' if len(running_processes) == 1 else 'es'))
        for process in running_processes:
            click.echo("   * {:<22} {:<10} {}".format(
                "{}[{}]".format(process['group'], process['name']), process['statename'], process['description']))
    else:
        click.echo("I was able to connect to the daemon, but I did not find any process...")
