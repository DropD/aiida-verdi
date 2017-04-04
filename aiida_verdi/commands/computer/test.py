# -*- coding: utf-8 -*-
"""
verdi computer test
"""
import click
from aiida_verdi import arguments, options


def _computer_test_get_jobs(transport, scheduler, dbauthinfo):
    """
    Internal test to check if it is possible to check the queue state.

    :note: exceptions could be raised

    :param transport: an open transport
    :param scheduler: the corresponding scheduler class
    :param dbauthinfo: the dbauthinfo object (from which one can get
        computer and aiidauser)
    :return: True if the test succeeds, False if it fails.
    """
    click.echo("> Getting job list...")
    found_jobs = scheduler.getJobs(as_dict=True)
    # For debug
    # for jid, data in found_jobs.iteritems():
    #    print jid, data['submission_time'], data['dispatch_time'], data['job_state']
    click.echo("  `-> OK, {} jobs found in the queue.".format(len(found_jobs)))
    return True


def _computer_create_temp_file(transport, scheduler, dbauthinfo):
    """
    Internal test to check if it is possible to create a temporary file
    and then delete it in the work directory

    :note: exceptions could be raised

    :param transport: an open transport
    :param scheduler: the corresponding scheduler class
    :param dbauthinfo: the dbauthinfo object (from which one can get
        computer and aiidauser)
    :return: True if the test succeeds, False if it fails.
    """
    import tempfile
    import datetime
    import os

    file_content = "Test from 'verdi computer test' on {}".format(
        datetime.datetime.now().isoformat())
    click.echo("> Creating a temporary file in the work directory...")
    click.echo("  `-> Getting the remote user name...")
    remote_user = transport.whoami()
    click.echo("      [remote username: {}]".format(remote_user))
    workdir = dbauthinfo.get_workdir().format(
        username=remote_user)
    click.echo("      [Checking/creating work directory: {}]".format(workdir))

    try:
        transport.chdir(workdir)
    except IOError:
        transport.makedirs(workdir)
        transport.chdir(workdir)

    with tempfile.NamedTemporaryFile() as f:
        fname = os.path.split(f.name)[1]
        click.echo("  `-> Creating the file {}...".format(fname))
        remote_file_path = os.path.join(workdir, fname)
        f.write(file_content)
        f.flush()
        transport.putfile(f.name, remote_file_path)
    click.echo("  `-> Checking if the file has been created...")
    if not transport.path_exists(remote_file_path):
        click.echo("* ERROR! The file was not found!")
        return False
    else:
        click.echo("      [OK]")
    click.echo("  `-> Retrieving the file and checking its content...")

    fd, destfile = tempfile.mkstemp()
    os.close(fd)
    try:
        transport.getfile(remote_file_path, destfile)
        with open(destfile) as f:
            read_string = f.read()
        click.echo("      [Retrieved]")
        if read_string != file_content:
            click.echo("* ERROR! The file content is different from what was expected!")
            click.echo("** Expected:")
            click.echo(file_content)
            click.echo("** Found:")
            click.echo(read_string)
            return False
        else:
            click.echo("      [Content OK]")
    finally:
        os.remove(destfile)

    click.echo("  `-> Removing the file...")
    transport.remove(remote_file_path)
    click.echo("  [Deleted successfully]")
    return True


@click.command()
@arguments.computer()
@options.user()
@click.option('-t', '--traceback', 'print_traceback', is_flag=True, default=False, help="Print the full traceback in case an exception is raised",)
def test(computer, user, print_traceback):
    """
    Test the connection to a remote computer
    """
    import traceback

    from aiida.backends.utils import get_automatic_user
    from aiida.orm.user import User
    from aiida.orm.computer import Computer as OrmComputer
    from aiida.common.exceptions import NotExistent

    '''default user'''
    if not user:
        user = User(dbuser=get_automatic_user())

    click.echo("Testing computer '{}' for user {}...".format(computer.name, user.email))
    try:
        dbauthinfo = computer.get_dbauthinfo(user._dbuser)
    except NotExistent:
        raise click.ClickException("User with email '{}' is not yet configured for computer '{}' yet.".format(user.email, computer.name))

    warning_string = None
    if not dbauthinfo.enabled:
        warning_string = ("** NOTE! Computer is disabled for the "
                            "specified user!\n   Do you really want to test it?")
    if not computer.is_enabled():
        warning_string = ("** NOTE! Computer is disabled!\n"
                            "   Do you really want to test it?")
    if warning_string:
        click.confirm(warning_string, default=False, abort=True)

    s = OrmComputer(dbcomputer=dbauthinfo.dbcomputer).get_scheduler()
    t = dbauthinfo.get_transport()

    ## STARTING TESTS HERE
    num_failures = 0
    num_tests = 0

    try:
        click.echo("> Testing connection...")
        with t:
            s.set_transport(t)
            num_tests += 1
            for test in [_computer_test_get_jobs,
                            _computer_create_temp_file]:
                num_tests += 1
                try:
                    succeeded = test(transport=t, scheduler=s,
                                        dbauthinfo=dbauthinfo)
                except Exception as e:
                    click.echo("* The test raised an exception!")
                    if print_traceback:
                        click.echo("** Full traceback:")
                        # Indent
                        click.echo("\n".join(["   {}".format(l) for l
                                            in traceback.format_exc().splitlines()]))
                    else:
                        click.echo("** {}: {}".format(e.__class__.__name__,
                                                    e.message))
                        click.echo("** (use the --traceback option to see the full traceback)")
                    succeeded = False

                if not succeeded:
                    num_failures += 1

        if num_failures:
            click.echo("Some tests failed! ({} out of {} failed)".format(
                num_failures, num_tests))
        else:
            click.echo("Test completed (all {} tests succeeded)".format(
                num_tests))
    except Exception as e:
        click.echo("** Error while trying to connect to the computer! Cannot ")
        click.echo("   perform following tests, stopping.")
        if print_traceback:
            click.echo("** Full traceback:")
            # Indent
            click.echo("\n".join(["   {}".format(l) for l
                                in traceback.format_exc().splitlines()]))
        else:
            click.echo("{}: {}".format(e.__class__.__name__, e.message))
            click.echo("(use the --traceback option to see the full traceback)")
        succeeded = False
