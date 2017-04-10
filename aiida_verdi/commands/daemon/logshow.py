# -*- coding: utf-8 -*-
"""
verdi daemon logshow
"""
import click


@click.command()
def logshow():
    """
    Show the log of the daemon, press CTRL+C to quit.
    """
    try:
        import subprocess32 as subprocess
    except ImportError:
        import subprocess
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv(process='daemon')
    from aiida_verdi.utils.daemon import get_daemon_pid, get_env_with_venv_bin, get_conffile_full_path

    pid = get_daemon_pid()
    if pid is None:
        click.echo("Daemon not running (cannot find the PID for it)")
        return 0

    try:
        currenv = get_env_with_venv_bin()
        process = subprocess.Popen(
            "supervisorctl -c {} tail -f aiida-daemon".format(
                get_conffile_full_path()),
            shell=True, env=currenv)  # , stdout=subprocess.PIPE)
        process.wait()
    except KeyboardInterrupt:
        # exit on CTRL+C
        process.kill()
