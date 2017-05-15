# -*- coding: utf-8 -*-
"""
verdi quicksetup command
"""
import click

from aiida.backends.profile import BACKEND_SQLA
from aiida_verdi import options as cliopt
from aiida_verdi.utils.interactive import InteractiveOption

_create_user_command = 'CREATE USER "{}" WITH PASSWORD \'{}\''
_create_db_command = 'CREATE DATABASE "{}" OWNER "{}"'
_grant_priv_command = 'GRANT ALL PRIVILEGES ON DATABASE "{}" TO "{}"'
_get_users_command = "SELECT usename FROM pg_user WHERE usename='{}'"


def _get_pg_access(non_interactive=False):
    '''
    find out how postgres can be accessed.

    Depending on how postgres is set up, psycopg2 can be used to create dbs and db users, otherwise a subprocess has to be used that executes psql as an os user with the right permissions.
    :return: (method, info) where method is a method that executes psql commandlines and info is a dict with keyword arguments to be used with method.
    '''
    # find out if we run as a postgres superuser or can connect as postgres
    # This will work on OSX in some setups but not in the default Debian one
    can_connect = False
    can_subcmd = None
    dbinfo = {'user': None, 'database': 'template1'}
    for pg_user in [None, 'postgres']:
        if _try_connect(**dbinfo):
            can_connect = True
            dbinfo['user'] = pg_user
            break

    # This will work for the default Debian postgres setup
    if not can_connect:
        if non_interactive:
            can_subcmd = True
            dbinfo['user'] = 'postgres'
        elif _try_subcmd(user='postgres'):
            can_subcmd = True
            dbinfo['user'] = 'postgres'
        else:
            can_subcmd = False

    # This is to allow for any other setup
    if not can_connect and not can_subcmd:
        click.echo('Detected no known postgres setup, some information is needed to create the aiida database and grant aiida access to it.')
        click.echo('If you feel unsure about the following parameters, first check if postgresql is installed.')
        click.echo('If postgresql is not installed please exit and install it, then run verdi quicksetup again.')
        click.echo('If postgresql is installed, please ask your system manager to provide you with the following parameters:')
        dbinfo = _prompt_db_info()
    elif non_interactive:
        click.echo('Database setup not confirmed, (--non-interactive). This may cause problems if the current user is not allowed to create databases.')

    pg_method = None
    if can_connect:
        pg_method = _pg_execute_psyco
    elif can_subcmd:
        pg_method = _pg_execute_sh

    result = {
        'method': pg_method,
        'dbinfo': dbinfo,
    }
    return result


def _prompt_db_info():
    '''prompt interactively for postgres database connecting details.'''
    access = False
    while not access:
        dbinfo = {}
        dbinfo['host'] = click.prompt('postgres host', default='localhost', type=str)
        dbinfo['port'] = click.prompt('postgres port', default=5432, type=int)
        dbinfo['database'] = click.prompt('template', default='template1', type=str)
        dbinfo['user'] = click.prompt('postgres super user', default='postgres', type=str)
        click.echo('')
        click.echo('trying to access postgres..')
        if _try_connect(**dbinfo):
            access = True
        else:
            dbinfo['password'] = click.prompt('postgres password of {}'.format(dbinfo['user']), hide_input=True, type=str)
            if _try_connect(**dbinfo):
                access = True
            else:
                click.echo('you may get prompted for a super user password and again for your postgres super user password')
                if _try_subcmd(**dbinfo):
                    access = True
                else:
                    click.echo('Unable to connect to postgres, please try again')
    return dbinfo


def _try_connect(**kwargs):
    '''
    try to start a psycopg2 connection.

    :return: True if successful, False otherwise
    '''
    from psycopg2 import connect
    success = False
    try:
        connect(**kwargs)
        success = True
    except Exception:
        pass
    return success


def _try_subcmd(**kwargs):
    '''
    try to run psql in a subprocess.

    :return: True if successful, False otherwise
    '''
    success = False
    try:
        _pg_execute_sh(r'\q', **kwargs)
        success = True
    except Exception:
        pass
    return success


def _create_dbuser(dbuser, dbpass, method=None, **kwargs):
    '''
    create a database user in postgres

    :param dbuser: Name of the user to be created.
    :param dbpass: Password the user should be given.
    :param method: callable with signature method(psql_command, **connection_info)
        where connection_info contains keys for psycopg2.connect.
    :param kwargs: connection info as for psycopg2.connect.
    '''
    method(_create_user_command.format(dbuser, dbpass), **kwargs)


def _create_db(dbuser, dbname, method=None, **kwargs):
    '''create a database in postgres

    :param dbuser: Name of the user which should own the db.
    :param dbname: Name of the database.
    :param method: callable with signature method(psql_command, **connection_info)
        where connection_info contains keys for psycopg2.connect.
    :param kwargs: connection info as for psycopg2.connect.
    '''
    method(_create_db_command.format(dbname, dbuser), **kwargs)
    method(_grant_priv_command.format(dbname, dbuser), **kwargs)


def _pg_execute_psyco(command, **kwargs):
    '''
    executes a postgres commandline through psycopg2

    :param command: A psql command line as a str
    :param kwargs: will be forwarded to psycopg2.connect
    '''
    from psycopg2 import connect, ProgrammingError
    conn = connect(**kwargs)
    conn.autocommit = True
    output = None
    with conn:
        with conn.cursor() as cur:
            cur.execute(command)
            try:
                output = cur.fetchall()
            except ProgrammingError:
                pass
    return output


def _pg_execute_sh(command, user='postgres', **kwargs):
    '''
    executes a postgres command line as another system user in a subprocess.

    :param command: A psql command line as a str
    :param user: Name of a system user with postgres permissions
    :param kwargs: connection details to forward to psql, signature as in psycopg2.connect
    '''
    options = ''
    database = kwargs.pop('database', None)
    if database:
        options += '-d {}'.format(database)
    kwargs.pop('password', None)
    host = kwargs.pop('host', None)
    if host:
        options += '-h {}'.format(host)
    port = kwargs.pop('port', None)
    if port:
        options += '-p {}'.format(port)
    try:
        import subprocess32 as sp
    except ImportError:
        import subprocess as sp
    from aiida.common.utils import escape_for_bash
    result = sp.check_output(['sudo', 'su', user, '-c', 'psql {options} -tc {}'.format(escape_for_bash(command), options=options)], **kwargs)
    if isinstance(result, str):
        result = result.strip().split('\n')
        result = [i for i in result if i]
    return result


def _dbuser_exists(dbuser, method, **kwargs):
    '''return True if postgres user with name dbuser exists, False otherwise.'''
    return bool(method(_get_users_command.format(dbuser), **kwargs))


def _check_db_name(dbname, method=None, **kwargs):
    '''looks up if a database with the name exists, prompts for using or creating a differently named one'''
    create = True
    while create and method("SELECT datname FROM pg_database WHERE datname='{}'".format(dbname), **kwargs):
        click.echo('database {} already exists!'.format(dbname))
        if not click.confirm('Use it (make sure it is not used by another profile)?'):
            dbname = click.prompt('new name', type=str, default=dbname)
        else:
            create = False
    return dbname, create


def profile_info(name, dct):
    import tabulate
    table = []
    table.append(['Name', name])
    table.extend([
        ['Backend', dct['backend']],
        ['User Name', '{} {}'.format(dct['first_name'], dct['last_name'])],
        ['User email', dct['email']],
        ['User institution', dct['institution']],
        ['DB name', dct['db_name']],
        ['DB user', dct['db_user']],
        ['DB host', '{}:{}'.format(dct['db_host'], dct['db_port'])],
        ['File Repo', dct['repo']]
    ])
    return tabulate.tabulate(table)


@click.command(short_help='Quick setup for new users')
@cliopt.email(prompt='Email Address (for publishing experiments)', cls=InteractiveOption, help='This email address will be associated with your data and will be exported along with it, should you choose to share any of your work')
@cliopt.first_name(prompt='First Name', cls=InteractiveOption)
@cliopt.last_name(prompt='Last Name', cls=InteractiveOption)
@cliopt.institution(prompt='Institution', cls=InteractiveOption)
@cliopt.backend(default=BACKEND_SQLA)
@cliopt.db_user()
@cliopt.db_pass()
@cliopt.db_name()
@cliopt.db_host()
@cliopt.db_port()
@click.option('--profile', type=str, metavar='PROFILE_NAME', help='defaults to quicksetup')
@cliopt.repo()
@click.option('--make-default', help='make this the default profile')
@click.option('--make-daemon', help='make this the profile that can run the daemon')
@cliopt.dry_run(help='do not create a database or profile')
@cliopt.non_interactive()
@click.pass_obj
def quicksetup(obj, non_interactive, dry_run, **kwargs):
    '''
    Quick setup for the most common usecase (1 user, 1 machine).

    Uses click for options. Creates a database user 'aiida_qs_<username>' with random password if it doesn't exist.
    Creates a 'aiidadb_qs_<username>' database (prompts to use or change the name if already exists).
    Makes sure not to overwrite existing databases or profiles without prompting for confirmation.),
    '''
    import os
    from aiida_verdi.commands.setup import setup
    from aiida.common.setup import create_base_dirs, AIIDA_CONFIG_FOLDER
    create_base_dirs()

    aiida_dir = os.path.expanduser(AIIDA_CONFIG_FOLDER)

    # access postgres
    pg_info = _get_pg_access(non_interactive=non_interactive)
    pg_execute = pg_info['method']
    dbinfo = pg_info['dbinfo']

    # check if a database setup already exists
    # otherwise setup the database user aiida
    # setup the database aiida_qs_<username>
    from getpass import getuser
    from aiida.common.setup import generate_random_secret_key
    osuser = getuser()
    dbuser = kwargs['db_user'] or 'aiida_qs_' + osuser
    dbpass = kwargs['db_pass'] or generate_random_secret_key()
    dbname = kwargs['db_name'] or 'aiidadb_qs_' + osuser

    # check if there is a profile that contains the db user already
    # and if yes, take the db user password from there
    # This is ok because a user can only see his own config files
    from aiida.common.setup import (set_default_profile, get_or_create_config)
    confs = get_or_create_config()
    profs = confs.get('profiles', {})
    for v in profs.itervalues():
        if v.get('AIIDADB_USER', '') == dbuser and not kwargs['db_pass']:
            dbpass = v.get('AIIDADB_PASS')
            print 'using found password for {}'.format(dbuser)
            break

    if not dry_run:
        try:
            create = True
            if not _dbuser_exists(dbuser, pg_execute, **dbinfo):
                _create_dbuser(dbuser, dbpass, pg_execute, **dbinfo)
            else:
                dbname, create = _check_db_name(dbname, pg_execute, **dbinfo)
            if create:
                _create_db(dbuser, dbname, pg_execute, **dbinfo)
        except Exception as e:
            click.echo('\n'.join([
                'Oops! Something went wrong while creating the database for you.',
                'You may continue with the quicksetup, however:',
                'For aiida to work correctly you will have to do that yourself as follows.',
                'Please run the following commands as the user for PostgreSQL (Ubuntu: $sudo su postgres):',
                '',
                '\t$ psql template1',
                '\t==> ' + _create_user_command.format(dbuser, dbpass),
                '\t==> ' + _create_db_command.format(dbname, dbuser),
                '\t==> ' + _grant_priv_command.format(dbname, dbuser),
                '',
                'Or setup your (OS-level) user to have permissions to create databases and rerun quicksetup.',
                '']))
            raise e
    else:
        click.echo('Not creating database (--dry-run recieved)')
        click.echo('The following or equivalent would otherwise be run:')
        click.echo(' $ psql template1')
        click.echo(' > {}'.format(_create_user_command.format(dbuser, '<password>')))
        click.echo(' > {}'.format(_create_db_command.format(dbname, dbuser)))
        click.echo(' > {}'.format(_grant_priv_command.format(dbname, dbuser)))

    # create a profile, by default 'quicksetup' and prompt the user if
    # already exists
    profile_name = kwargs['profile'] or 'quicksetup'
    write_profile = False
    confs = get_or_create_config()
    while not write_profile:
        if profile_name in confs.get('profiles', {}):
            if non_interactive:
                if kwargs['overwrite']:
                    write_profile = True
                    break
                else:
                    click.clickException('profile already exists, use --overwrite to overwrite')

            if click.confirm('overwrite existing profile {}?'.format(profile_name)):
                write_profile = True
            else:
                profile_name = click.prompt('new profile name', type=str)
        else:
            write_profile = True

    dbhost = dbinfo.get('host', 'localhost')
    dbport = dbinfo.get('port', '5432')

    from os.path import isabs
    repo = kwargs['repo'] or 'repository-{}/'.format(profile_name)
    if not isabs(repo):
        repo = os.path.join(aiida_dir, repo)

    setup_args = {
        'backend': kwargs['backend'],
        'email': kwargs['email'],
        'db_host': dbhost,
        'db_port': dbport,
        'db_name': dbname,
        'db_user': dbuser,
        'db_pass': dbpass,
        'repo': repo,
        'first_name': kwargs['first_name'],
        'last_name': kwargs['last_name'],
        'institution': kwargs['institution'],
        'force_overwrite': write_profile,
        'only-config': False,
        'non_interactive': True
    }
    if not dry_run:
        ctx = click.get_current_context()
        #setup.invoke(profile_name, **setup_args)
        ctx.forward(setup)
    else:
        click.echo('profile not written (--dry-run recieved)')
        click.echo(profile_info(profile_name, setup_args))

    # set as new default profile
    # prompt if there is another non-quicksetup profile
    defprof = confs.get('default_profiles', {})
    if defprof.get('daemon', '').startswith('quicksetup'):
        use_new = False
        if non_interactive:
            if kwargs['make_daemon'] and not dry_run:
                use_new = True
        else:
            use_new = click.confirm('The daemon default profile is set to {}, do you want to set the newly created one ({}) as default? (can be changed back later)'.format(defprof['daemon'], profile_name))
        if use_new:
            set_default_profile('daemon', profile_name, force_rewrite=True)
    if defprof.get('verdi'):
        use_new = False
        if non_interactive:
            if kwargs['make_default'] and not dry_run:
                use_new = True
        else:
            use_new = click.confirm('The verdi default profile is set to {}, do you want to set the newly created one ({}) as new default? (can be changed back later)'.format(defprof['verdi'], profile_name))
        if use_new:
            set_default_profile('verdi', profile_name, force_rewrite=True)
