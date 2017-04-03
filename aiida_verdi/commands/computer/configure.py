# -*- coding: utf-8 -*-
"""
verdi computer configure
"""
import click
from functools import update_wrapper

from aiida_verdi import options, arguments


def _dj_auth_info(computer, user):
    """get authinfo - django"""
    from django.core.exceptions import ObjectDoesNotExist

    from aiida.backends.djsite.db.models import DbAuthInfo

    try:
        authinfo = DbAuthInfo.objects.get(
            dbcomputer=computer.dbcomputer,
            aiidauser=user)

        old_authparams = authinfo.get_auth_params()
    except ObjectDoesNotExist:
        authinfo = DbAuthInfo(dbcomputer=computer.dbcomputer, aiidauser=user)
        old_authparams = {}
    return authinfo, old_authparams


def _sqla_auth_info(computer, user):
    '''get authinfo - sqla'''
    from aiida.backends.sqlalchemy.models.authinfo import DbAuthInfo
    from aiida.backends.sqlalchemy import get_scoped_session
    session = get_scoped_session()

    authinfo = session.query(DbAuthInfo).filter(
        DbAuthInfo.dbcomputer == computer.dbcomputer
    ).filter(
        DbAuthInfo.aiidauser == user
    ).first()
    if authinfo is None:
        authinfo = DbAuthInfo(
            dbcomputer=computer.dbcomputer,
            aiidauser=user
        )
        old_authparams = {}
    else:
        old_authparams = authinfo.get_auth_params()
    return authinfo, old_authparams


def _get_authinfo(computer, user):
    """get the authentication info for a given user with a given computer"""
    from aiida.backends.settings import BACKEND
    from aiida.backends.profile import BACKEND_SQLA, BACKEND_DJANGO
    if BACKEND == BACKEND_DJANGO:
        return _dj_auth_info(computer, user)
    elif BACKEND == BACKEND_SQLA:
        return _sqla_auth_info(computer, user)
    else:
        raise Exception(
            "Unknown backend {}".format(BACKEND)
        )


def required_if_ssh(ctx):
    comp = ctx.params.get('computer')
    req = False
    if comp:
        if comp.get_transport_type() == 'ssh':
            req = True
    return req


def ssh_options(f):
    """
    ssh transport option pack
    """
    from aiida_verdi.utils.interactive import InteractiveOption

    @click.option('--username', prompt='Username', required_fn=required_if_ssh, cls=InteractiveOption, help='[if transport is ssh]: username to connect to COMPUTER via ssh')
    @click.option('--port', required_fn=required_if_ssh, cls=InteractiveOption)
    @click.option('--look_for_keys', prompt='look for keys', required_fn=required_if_ssh, cls=InteractiveOption)
    def new_f(*args, **kwargs):
        return f(*args, **kwargs)
    return update_wrapper(new_f, f)


@click.command()
@options.user()
@arguments.computer()
@ssh_options
def configure(user, computer, **kwargs):
    """
    Configure a computer for a given AiiDA user
    """
    from aiida.backends.utils import get_automatic_user
    #~ if not ctx.obj:
    #~     ctx.obj = {}

    '''should possibly be in user parameter type'''
    if not user:
        user = get_automatic_user()
    #~ ctx.obj['user'] = user
    #~ ctx.obj['computer'] = computer

    authinfo, old_authparams = _get_authinfo(computer, user)
    #~ ctx.obj['authinfo'] = authinfo
    #~ ctx.obj['old_authparams'] = old_authparams

    click.echo(("Configuring computer '{}' for the AiiDA user '{}'".format(computer.name, user.email)))
    click.echo("Computer {} has transport of type {}".format(computer.name, computer.get_transport_type()))


@click.command()
@click.pass_context
def configure_default(ctx):
    """
    configure for the specific context
    """
    import inspect
    import readline

    from aiida.common.utils import get_configured_user_email
    from aiida.common.exceptions import ValidationError
    user = ctx.obj['user']
    computer = ctx.obj['computer']
    authinfo = ctx.obj['authinfo']
    old_authparams = ctx.obj['old_authparams']

    '''configuring the computer'''
    Transport = computer.get_transport_class()

    if user.email != get_configured_user_email():
        click.echo("*" * 72)
        click.echo("** {:66s} **".format("WARNING!"))
        click.echo("** {:66s} **".format("  You are configuring a different user."))
        click.echo("** {:66s} **".format("  Note that the default suggestions are taken from your"))
        click.echo("** {:66s} **".format("  local configuration files, so they may be incorrect."))
        click.echo("*" * 72)

    valid_keys = Transport.get_valid_auth_params()

    default_authparams = {}
    for k in valid_keys:
        if k in old_authparams:
            default_authparams[k] = old_authparams.pop(k)
    if old_authparams:
        click.echo("WARNING: the following keys were previously in the authorization parameters,")
        click.echo("but have not been recognized and have been deleted:")
        click.echo(", ".join(old_authparams.keys()))

    if not valid_keys:
        click.echo("There are no special keys to be configured. Configuration completed.")
        authinfo.set_auth_params({})
        authinfo.save()
        return

    click.echo("")
    click.echo("Note: to leave a field unconfigured, leave it empty and press [Enter]")

    # I strip out the old auth_params that are not among the valid keys

    new_authparams = {}

    for k in valid_keys:
        key_set = False
        while not key_set:
            try:
                converter_name = '_convert_{}_fromstring'.format(k)
                try:
                    converter = dict(inspect.getmembers(
                        Transport))[converter_name]
                except KeyError:
                    click.echo("Internal error! No {} defined in Transport {}".format(converter_name, computer.get_transport_type()), err=True)
                    click.exit(1)

                if k in default_authparams:
                    readline.set_startup_hook(lambda:
                                              readline.insert_text(str(default_authparams[k])))
                else:
                    # Use suggestion only if parameters were not already set
                    suggester_name = '_get_{}_suggestion_string'.format(k)
                    try:
                        suggester = dict(inspect.getmembers(
                            Transport))[suggester_name]
                        suggestion = suggester(computer)
                        readline.set_startup_hook(lambda:
                                                  readline.insert_text(suggestion))
                    except KeyError:
                        readline.set_startup_hook()

                txtval = raw_input("=> {} = ".format(k))
                if txtval:
                    new_authparams[k] = converter(txtval)
                key_set = True
            except ValidationError as e:
                click.echo("Error in the inserted value: {}".format(e.message))
                click.exit("1")

    authinfo.set_auth_params(new_authparams)
    authinfo.save()
    click.echo("Configuration stored for your user on computer '{}'.".format(computer.name))
