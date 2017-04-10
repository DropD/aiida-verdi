# -*- coding: utf-8 -*-
"""
verdi daemon stop
"""
import click


@click.command()
@click.option('-n', '--no-wait', 'wait_for_death', default=True, is_flag=True, help='Do not wait for the deamon to shut down before returning')
@click.option('-m', '--max-retries', type=int, default=20, help='max number of shutdown attempts')
def stop(wait_for_death, max_retries):
    """
    Stop the daemon.

    :param wait_for_death: If True, also verifies that the process was already
        killed. It attempts at most ``max_retries`` times, with ``sleep_between_retries``
        seconds between one attempt and the following one (both variables are
        for the time being hardcoded in the function).

    :return: None if ``wait_for_death`` is False. True/False if the process was
        actually dead or after all the retries it was still alive.
    """
    from datetime import timedelta
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv(process='daemon')
    from aiida.common import aiidalogger
    logger = aiidalogger.getChild('workflowmanager')

    from aiida.daemon.timestamps import get_last_daemon_timestamp, set_daemon_timestamp

    import time

    sleep_between_retries = 3

    # Note: NO check here on the daemon user: allow the daemon to be shut
    # down if it was inadvertently left active and the setting was changed.
    from aiida_verdi.utils.daemon import kill_daemon, get_daemon_pid
    kill_daemon()

    dead = None
    if wait_for_death:
        dead = False
        for _ in range(max_retries):
            pid = get_daemon_pid()
            if pid is None:
                dead = True
                click.echo("AiiDA Daemon shut down correctly.")
                # The following lines are needed for the workflow_stepper
                # (re-initialize the timestamps used to lock the task, in case
                # it crashed for some reason).
                # TODO: remove them when the old workflow system will be
                # taken away.
                try:
                    if (get_last_daemon_timestamp('workflow', when='stop') -
                        get_last_daemon_timestamp('workflow', when='start')) < timedelta(0):
                        logger.info("Workflow stop timestamp was {}; re-initializing"
                                    " it to current time".format(
                                        get_last_daemon_timestamp('workflow', when='stop')))
                        click.echo("Re-initializing workflow stepper stop timestamp")
                        set_daemon_timestamp(task_name='workflow', when='stop')
                except TypeError:
                    # when some timestamps are None (i.e. not present), we make
                    # sure that at least the stop timestamp is defined
                    click.echo("Re-initializing workflow stepper stop timestamp")
                    set_daemon_timestamp(task_name='workflow', when='stop')
                break
            else:
                click.echo("Waiting for the AiiDA Daemon to shut down...")
                # Wait two seconds between retries
                time.sleep(sleep_between_retries)
        if not dead:
            click.echo("Unable to stop (the daemon took too much time to shut down).")
            click.echo("Probably, it is in the middle of a long operation.")
            click.echo("The shut down signal was sent, anyway, so it should shut down soon.")

    return dead
