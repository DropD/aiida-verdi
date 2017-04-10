# -*- coding: utf-8 -*-
"""
verdi daemon start
"""
import click


@click.command()
def start():
    """
    Start the daemon
    """
    from datetime import timedelta
    try:
        import subprocess32 as subprocess
    except ImportError:
        import subprocess
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv(process='daemon')
    from aiida.common import aiidalogger
    logger = aiidalogger.getChild('workflowmanager')
    from aiida.daemon.timestamps import get_last_daemon_timestamp,set_daemon_timestamp

    from aiida.backends.utils import get_daemon_user
    from aiida.common.utils import get_configured_user_email

    daemon_user = get_daemon_user()
    this_user = get_configured_user_email()


    from aiida_verdi.utils.daemon import is_daemon_user
    if not is_daemon_user():
        click.echo("You are not the daemon user! I will not start the daemon.")
        click.echo("(The daemon user is '{}', you are '{}')".format(daemon_user, this_user))
        click.echo("")
        click.echo("** FOR ADVANCED USERS ONLY: **")
        click.echo("To change the current default user, use 'verdi install --only-config'")
        click.echo("To change the daemon user, use 'verdi daemon configureuser'")
        return 1

    from aiida_verdi.utils.daemon import get_daemon_pid
    pid = get_daemon_pid()

    if pid is not None:
        click.echo("Daemon already running, try asking for its status")
        return 0

    click.echo("Clearing all locks ...")
    from aiida.orm.lock import LockManager

    LockManager().clear_all()

    click.echo("Starting AiiDA Daemon ...")
    from aiida_verdi.utils.daemon import get_env_with_venv_bin, get_conffile_full_path
    currenv = get_env_with_venv_bin()
    process = subprocess.Popen(
        "supervisord -c {}".format(get_conffile_full_path()),
        shell=True, stdout=subprocess.PIPE, env=currenv)
    process.wait()

    # The following lines are needed for the workflow_stepper
    # (re-initialize the timestamps used to lock the task, in case
    # it crashed for some reason).
    # TODO: remove them when the old workflow system will be
    # taken away.
    try:
        if (get_last_daemon_timestamp('workflow',when='stop')
            -get_last_daemon_timestamp('workflow',when='start'))<timedelta(0):
            logger.info("Workflow stop timestamp was {}; re-initializing "
                        "it to current time".format(
                        get_last_daemon_timestamp('workflow',when='stop')))
            click.echo("Re-initializing workflow stepper stop timestamp")
            set_daemon_timestamp(task_name='workflow', when='stop')
    except TypeError:
        # when some timestamps are None (i.e. not present), we make
        # sure that at least the stop timestamp is defined
        click.echo("Re-initializing workflow stepper stop timestamp")
        set_daemon_timestamp(task_name='workflow', when='stop')

    if (process.returncode == 0):
        click.echo("Daemon started")
