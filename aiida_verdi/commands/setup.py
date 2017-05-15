# -*- coding: utf-8 -*-
"""verdi setup command"""
import click
from aiida_verdi import options


def _migrate_sqla(gprofile):
    """execute a database migration for SQLAlchemy backend"""
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv

    click.echo("...for SQLAlchemy backend")
    ensure_aiida_dbenv()

    from aiida.backends.sqlalchemy.models.base import Base
    from aiida.backends.sqlalchemy import utils
    from aiida.common.setup import get_profile_config

    # Those import are necessary for SQLAlchemy to correctly create
    # the needed database tables.
    from aiida.backends.sqlalchemy.models import (
        authinfo, comment, computer, group, lock, log,
        node, user, workflow, settings)

    utils.reset_session(get_profile_config(gprofile))
    from aiida.backends.sqlalchemy import get_scoped_session
    connection = get_scoped_session().connection()
    Base.metadata.create_all(connection)
    utils.install_tc(connection)


def _migrate_django(gprofile):
    """execute a database migration for django backend"""
    import os
    from aiida.cmdline import pass_to_django_manage, execname
    from aiida.common.setup import DEFAULT_UMASK

    click.echo("...for Django backend")
    # The correct profile is selected within load_dbenv.
    # Setting os.umask here since sqlite database gets created in
    # this step.
    old_umask = os.umask(DEFAULT_UMASK)

    try:
        pass_to_django_manage([execname, 'migrate'], profile=gprofile)
    finally:
        os.umask(old_umask)


def _migrate(gprofile, created_conf):
    """execute a database migration for a profile"""
    from aiida.backends.profile import BACKEND_SQLA, BACKEND_DJANGO
    from aiida.backends.utils import set_backend_type
    from aiida.common.exceptions import InvalidOperation

    click.echo("Executing now a migrate command...")

    backend_choice = created_conf['AIIDADB_BACKEND']
    if backend_choice == BACKEND_DJANGO:
        _migrate_django(gprofile)
        set_backend_type(BACKEND_DJANGO)
    elif backend_choice == BACKEND_SQLA:
        _migrate_sqla(gprofile)
        set_backend_type(BACKEND_SQLA)
    else:
        raise InvalidOperation("Not supported backend selected.")


def _set_profile(profile):
    """prevent profile arg vs profile option"""
    from aiida.backends import settings as settings_profile

    if settings_profile.AIIDADB_PROFILE and profile:
        click.Error('the profile argument cannot be used if verdi is called with -p option: {} and {}'.format(settings_profile.AIIDADB_PROFILE, profile))
    gprofile = settings_profile.AIIDADB_PROFILE or profile
    if gprofile == profile:
        settings_profile.AIIDADB_PROFILE = profile
    if not settings_profile.AIIDADB_PROFILE:
        settings_profile.AIIDADB_PROFILE = 'default'

    return settings_profile.AIIDADB_PROFILE


def _try_create_conf_ni(gprofile, **kwargs):
    """try to noninteractively create a new profile"""
    from aiida.common.setup import create_config_noninteractive

    try:
        created_conf = create_config_noninteractive(
            profile=gprofile,
            backend=kwargs['backend'],
            email=kwargs['email'],
            db_host=kwargs['db_host'],
            db_port=kwargs['db_port'],
            db_name=kwargs['db_name'],
            db_user=kwargs['db_user'],
            db_pass=kwargs['db_pass'],
            repo=kwargs['repo'],
            force_overwrite=kwargs.get('force_overwrite', False)
        )
        return created_conf
    except ValueError as e:
        raise click.Error("Error during configuation: {}".format(e.message))
    except KeyError as e:
        raise click.Error("--non-interactive requires all values to be given on the commandline! {}".format(e.message))


def _try_create_conf_interactive(gprofile):
    """try to interactively create a new profile"""
    from aiida.common.setup import create_configuration

    try:
        created_conf = create_configuration(profile=gprofile)
        return created_conf
    except ValueError as e:
        raise click.Error("Error during configuration: {}".format(e.message))


def _check_ni_required_params(non_interactive, setup_, kwargs):
    """if non_interactive, check for missing required parameters"""
    if non_interactive:
        params = {i.name: i for i in setup.params}
        required = ['backend', 'email', 'db_host', 'db_port',
                    'db_name', 'db_user', 'first_name',
                    'last_name', 'institution', 'no_password', 'repo']
        for i in required:
            if not kwargs[i]:
                raise click.MissingParameter(param=params[i])


def _create_profile(gprofile, dry_run, non_interactive, **kwargs):
    """do all the profile creation depending on cli params"""
    if non_interactive and not dry_run:
        return _try_create_conf_ni(gprofile, **kwargs)
    elif not dry_run:
        return _try_create_conf_interactive(gprofile)
    else:
        click.echo('Not creating profile (--dry-run recieved)')


def _print_profile_info(gprofile, **kwargs):
    """print profile info for dry run"""
    from aiida_verdi.commands.quicksetup import profile_info
    click.echo(profile_info(gprofile, kwargs))


def _configure_user(non_interactive, **kwargs):
    """configure the user for the profile"""

    # I create here the default user
    click.echo("Loading new environment...")
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()

    from aiida.common.setup import DEFAULT_AIIDA_USER
    from aiida.orm.user import User as AiiDAUser

    if not AiiDAUser.search_for_users(email=DEFAULT_AIIDA_USER):
        click.echo("Installing default AiiDA user...")
        nuser = AiiDAUser(email=DEFAULT_AIIDA_USER)
        nuser.first_name = "AiiDA"
        nuser.last_name = "Daemon"
        nuser.is_staff = True
        nuser.is_active = True
        nuser.is_superuser = True
        nuser.force_save()

    from aiida.common.utils import get_configured_user_email
    email = get_configured_user_email()
    click.echo("Starting user configuration for {}...".format(email))
    if email == DEFAULT_AIIDA_USER:
        click.echo("You set up AiiDA using the default Daemon email ({}),".format(
            email))
        click.echo("therefore no further user configuration will be asked.")
    else:
        # Ask to configure the new user
        from aiida.cmdline.commands.user import User
        if not non_interactive:
            User().user_configure(email)
        else:
            # or don't ask
            User().user_configure(
                kwargs['email'],
                '--first-name=' + kwargs.get('first_name'),
                '--last-name=' + kwargs.get('last_name'),
                '--institution=' + kwargs.get('institution'),
                '--no_password'
            )


@click.command('setup', short_help='Setup an AiiDA profile')
@click.argument('profile', default='', metavar='PROFILE', type=str)  # help='Profile Name to create/edit')
@click.option('--only-config', is_flag=True, help='Do not create a new user')
@options.non_interactive(help='run without user interactions, requires all non-flag options to be set. These options will be ignored without --non-interactive.')
@options.dry_run(help='make no actual changes')
@options.backend(help='[if --non-interactive]: backend choice')
@options.email(help='[if --non-interactive]: user email address')
@options.db_host(help='[if --non-interactive]: database hostname')
@options.db_port(help='[if --non-interactive]: database port')
@options.db_name(help='[if --non-interactive]: database name')
@options.db_user(help='[if --non-interactive]: database user')
@options.db_pass(default='', help='[if --non-interactive]: database user password')
@options.first_name(help='[if --non-interactive]: user first name')
@options.last_name(help='[if --non-interactive]: user last name')
@options.institution(help='[if --non-interactive]: user institution')
@click.option('--no-password', is_flag=True, help='do not set a password (--non-interactive fails otherwise)')
@options.repo(help='[if --non-interactive]: data file repository')
def setup(only_config, non_interactive, dry_run, **kwargs):
    """
    Setup PROFILE for aiida for the current user

    This command creates the ~/.aiida folder in the home directory
    of the user, interactively asks for the database settings and
    the repository location, does a setup of the daemon and runs
    a migrate command to create/setup the database.

    In --non-interactive mode, the command will never prompt but
    instead expect all parameters to be given as commandline options.
    If values are missing or invalid, the command will fail.
    """

    from aiida.common.setup import (create_base_dirs, set_default_profile)

    _check_ni_required_params(non_interactive, setup, kwargs)

    # create the directories to store the configuration files
    create_base_dirs()

    # set the global profile setting from option or argument
    gprofile = _set_profile(kwargs['profile'])

    created_conf = None
    # ask and store the configuration of the DB
    created_conf = _create_profile(gprofile, dry_run, non_interactive, **kwargs)

    # set default DB profiles
    set_default_profile('verdi', gprofile, force_rewrite=False)
    set_default_profile('daemon', gprofile, force_rewrite=False)

    if dry_run:
        click.echo('Not executing database migration (--dry-run recieved)')
        _print_profile_info(gprofile, **kwargs)
    else:
        if only_config:
            click.echo("Only user configuration requested, "
                       "skipping the migrate command")
        else:
            _migrate(gprofile, created_conf)
            click.echo("Database was created successfully")

        _configure_user(non_interactive, **kwargs)

    click.echo("Setup finished.")
