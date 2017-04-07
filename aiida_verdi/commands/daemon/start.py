# -*- coding: utf-8 -*-
"""
verdi daemon start
"""
import click


@click.command()
def start()
    """
    Start the daemon
    """
    if not is_dbenv_loaded():
        from aiida.backends.utils import load_dbenv
        load_dbenv(process='daemon')

    from aiida.daemon.timestamps import get_last_daemon_timestamp,set_daemon_timestamp

    if args:
        print >> sys.stderr, (
            "No arguments allowed for the '{}' command.".format(
                self.get_full_command_name()))
        sys.exit(1)

    from aiida.backends.utils import get_daemon_user
    from aiida.common.utils import get_configured_user_email

    daemon_user = get_daemon_user()
    this_user = get_configured_user_email()


    if daemon_user != this_user:
        print "You are not the daemon user! I will not start the daemon."
        print "(The daemon user is '{}', you are '{}')".format(
            daemon_user, this_user)
        print ""
        print "** FOR ADVANCED USERS ONLY: **"
        print "To change the current default user, use 'verdi install --only-config'"
        print "To change the daemon user, use 'verdi daemon configureuser'"

        sys.exit(1)

    pid = self.get_daemon_pid()

    if pid is not None:
        print "Daemon already running, try asking for its status"
        return

    print "Clearing all locks ..."
    from aiida.orm.lock import LockManager

    LockManager().clear_all()

    print "Starting AiiDA Daemon ..."
    currenv = _get_env_with_venv_bin()
    process = subprocess.Popen(
        "supervisord -c {}".format(self.conffile_full_path),
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
            print "Re-initializing workflow stepper stop timestamp"
            set_daemon_timestamp(task_name='workflow', when='stop')
    except TypeError:
        # when some timestamps are None (i.e. not present), we make
        # sure that at least the stop timestamp is defined
        print "Re-initializing workflow stepper stop timestamp"
        set_daemon_timestamp(task_name='workflow', when='stop')

    if (process.returncode == 0):
        print "Daemon started"


def kill_daemon(self):
    """
    This is the actual call that kills the daemon.

    There are some print statements inside, but no sys.exit, so it is
    safe to be called from other parts of the code.
    """
    from signal import SIGTERM
    import errno

    pid = self.get_daemon_pid()
    if pid is None:
        print "Daemon not running (cannot find the PID for it)"
        return

    print "Shutting down AiiDA Daemon ({})...".format(pid)
    try:
        os.kill(pid, SIGTERM)
    except OSError as e:
        if e.errno == errno.ESRCH:  # No such process
            print ("The process {} was not found! "
                    "Assuming it was already stopped.".format(pid))
            print "Cleaning the .pid and .sock files..."
            self._clean_sock_files()
        else:
            raise
