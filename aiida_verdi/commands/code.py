#-*- coding: utf8 -*-
"""
verdi code commands
"""
import sys
import click

from aiida_verdi import options
from aiida_verdi.verdic_utils import (
    load_dbenv_if_not_loaded, aiida_dbenv, prompt_help_loop,
    prompt_with_help, path_validator, computer_name_list,
    computer_validator, multi_line_prompt, create_code,
    InteractiveOption, single_value_prompt)
from aiida_verdi.param_types.code import CodeArgument
from aiida_verdi.param_types.plugin import PluginArgument


@click.group()
def code():
    """
    manage codes in your AiiDA database.
    """


@code.command('list')
@click.option('-c', '--computer', help='filter codes for a computer')
@click.option('-p', '--plugin', help='filter codes for a plugin')
@click.option('-A', '--all-users', help='show codes of all users')
@click.option('-o', '--show-owner', is_flag=True, help='show owner information')
@click.option('-a', '--all-codes', is_flag=True, help='show hidden codes')
def _list(computer, plugin, all_users, show_owner, all_codes):
    """
    List available codes
    """
    from aiida_verdi.verdic_utils import print_list_res
    load_dbenv_if_not_loaded()

    computer_filter = computer
    plugin_filter = plugin
    reveal_filter = all_codes

    from aiida.orm.querybuilder import QueryBuilder
    from aiida.orm.code import Code
    from aiida.orm.computer import Computer
    from aiida.orm.user import User
    from aiida.backends.utils import get_automatic_user

    qb_user_filters = dict()
    if not all_users:
        user = User(dbuser=get_automatic_user())
        qb_user_filters['email'] = user.email

    qb_computer_filters = dict()
    if computer_filter is not None:
        qb_computer_filters['name'] = computer_filter

    qb_code_filters = dict()
    if plugin_filter is not None:
        qb_code_filters['attributes.input_plugin'] = plugin_filter

    if not reveal_filter:
        qb_code_filters['attributes.hidden'] = {"~==": True}

    print "# List of configured codes:"
    print "# (use 'verdi code show CODEID | CODENAME' to see the details)"
    if computer_filter is not None:
        qb = QueryBuilder()
        qb.append(Code, tag="code",
                  filters=qb_code_filters,
                  project=["id", "label"])
        # We have a user assigned to the code so we can ask for the
        # presence of a user even if there is no user filter
        qb.append(User, creator_of="code",
                  project=["email"],
                  filters=qb_user_filters)
        # We also add the filter on computer. This will automatically
        # return codes that have a computer (and of course satisfy the
        # other filters). The codes that have a computer attached are the
        # remote codes.
        qb.append(Computer, computer_of="code",
                  project=["name"],
                  filters=qb_computer_filters)
        print_list_res(qb, show_owner)

    # If there is no filter on computers
    else:
        # Print all codes that have a computer assigned to them
        # (these are the remote codes)
        qb = QueryBuilder()
        qb.append(Code, tag="code",
                  filters=qb_code_filters,
                  project=["id", "label"])
        # We have a user assigned to the code so we can ask for the
        # presence of a user even if there is no user filter
        qb.append(User, creator_of="code",
                  project=["email"],
                  filters=qb_user_filters)
        qb.append(Computer, computer_of="code",
                  project=["name"])
        print_list_res(qb, show_owner)

        # Now print all the local codes. To get the local codes we ask
        # the dbcomputer_id variable to be None.
        qb = QueryBuilder()
        comp_non_existence = {"dbcomputer_id": {"==": None}}
        if not qb_code_filters:
            qb_code_filters = comp_non_existence
        else:
            new_qb_code_filters = {"and": [qb_code_filters,
                                           comp_non_existence]}
            qb_code_filters = new_qb_code_filters
        qb.append(Code, tag="code",
                  filters=qb_code_filters,
                  project=["id", "label"])
        # We have a user assigned to the code so we can ask for the
        # presence of a user even if there is no user filter
        qb.append(User, creator_of="code",
                  project=["email"],
                  filters=qb_user_filters)
        print_list_res(qb, show_owner)


@code.command()
@click.argument('code', metavar='CODE', type=CodeArgument())
def show(code):
    """
    Show information on a given code
    """
    from aiida_verdi.verdic_utils import get_code

    code = get_code(code)
    click.echo(code.full_text_info)


def validate_local(ctx, param, value):
    """validate and convert string to boolean"""
    if value in [True, 'True', 'true', 'T']:
        return True, True
    elif value in [False, 'False', 'false', 'F']:
        return True, False
    else:
        return False, None


def validate_path(prefix_opt=None, is_abs=False, **kwargs):
    """validate string input as a path"""
    def decorated_validator(ctx, param, value):
        """validate string input as path"""
        from os import path
        from os.path import expanduser, isabs
        path_t = click.Path(**kwargs)
        if isinstance(ctx.obj, dict):
            if ctx.obj.get('nocheck'):
                return value or 'UNUSED'
        if value:
            try:
                value = expanduser(value)
                if prefix_opt:
                    value = path.join(ctx.params.get(prefix_opt), value)
                if is_abs and not isabs(value):
                    return None
                value = path_t.convert(value, param, ctx)
            except click.BadParameter as e:
                if ctx.params.get('non_interactive'):
                    raise e
                click.echo(e.format_message(), err=True)
                value = None
        return validator_func(ctx, param, value)
    return decorated_validator


def required_if_local(ctx, param):
    """return the boolean value of the is_local parameter"""
    return ctx.params.get('is_local')


def required_if_remote(ctx, param):
    """return the inverse boolean value of the is_local parameter"""
    return not ctx.params.get('is_local')

validate_code_folder = path_validator(
    expand_user=True, exists=True, file_okay=False, readable=True,
    required_if=required_if_local
)

validate_code_rel_path = path_validator(
    exists=True, dir_okay=False, required_if=required_if_local,
    prefix_opt='code_folder'
)

validate_computer = computer_validator(required_if=required_if_remote)

computer_callback = prompt_with_help(
    prompt='Remote computer name', suggestions=computer_name_list,
    callback=validate_computer, ni_callback=validate_computer.throw
)

validate_code_remote_path = path_validator(
    is_abs=True, dir_okay=False, required_if=required_if_remote
)
code_remote_path_callback = prompt_with_help(
    prompt='Remote absolute path', callback=validate_code_remote_path,
    ni_callback=validate_code_remote_path.throw
)

prepend_callback = prompt_with_help(
    prompt=('Text to prepend to each command execution\n'
            'FOR INSTANCE MODULES TO BE LOADED FOR THIS CODE'),
    prompt_loop=multi_line_prompt
)

append_callback = prompt_with_help(
    prompt='Text to append to each command execution',
    prompt_loop=multi_line_prompt
)


@code.command()
@click.option('--label', is_eager=True, callback=prompt_with_help(prompt='Label'), help='A label to refer to this code')
@click.option('--description', is_eager=True, prompt='Description', cls=InteractiveOption, help='A human-readable description of this code')
@click.option('--is-local', is_eager=True, callback=prompt_with_help(prompt='Local', callback=validate_local), help='True or False; if True, then you have to provide a folder with files that will be stored in AiiDA and copied to the remote computers for every calculation submission. if True the code is just a link to a remote computer and an absolute path there')
@click.option('--input-plugin', prompt='Default input plugin', type=PluginArgument(category='calculations'), cls=InteractiveOption, help='A string of the default input plugin to be used with this code that is recognized by the CalculationFactory. Use he verdi calculation plugins command to get the list of existing plugins')
@click.option('--code-folder', callback=prompt_with_help(prompt='Folder containing the code', callback=validate_code_folder, ni_callback=validate_code_folder.throw), help='For local codes: The folder on your local computer in which there are files to be stored in the AiiDA repository and then copied over for every submitted calculation')
@click.option('--code-rel-path', callback=prompt_with_help(prompt='Relative path of the executable', callback=validate_code_rel_path, ni_callback=validate_code_rel_path.throw), help='The relative path of the executable file inside the folder entered in the previous step or in --code-folder')
@click.option('--computer', callback=computer_callback, help='The name of the computer on which the code resides as stored in the AiiDA database')
@click.option('--remote-abs-path', callback=code_remote_path_callback, help='The (full) absolute path on the remote machine')
@click.option('--prepend-text', callback=prepend_callback, help='Text to prepend to each command execution. FOR INSTANCE, MODULES TO BE LOADED FOR THIS CODE. This is a multiline string, whose content will be prepended inside the submission script after the real execution of the job. It is your responsibility to write proper bash code!')
@click.option('--append-text', callback=append_callback, help='Text to append to each command execution. This is a multiline string, whose content will be appended inside the submission script after the real execution of the job. It is your responsibility to write proper bash code!')
@options.non_interactive()
@options.dry_run()
@options.debug()
def setup(**kwargs):
    """create and store a code on the commandline"""
    from aiida.common.exceptions import ValidationError

    code = create_code(**kwargs)

    # Enforcing the code to be not hidden.
    code._reveal()

    '''store or display'''
    if not kwargs.get('dry_run'):
        '''store'''
        try:
            code.store()
        except ValidationError as e:
            print "Unable to store the code: {}. Exiting...".format(e.message)
            sys.exit(1)

        print "Code '{}' successfully stored in DB.".format(code.label)
        print "pk: {}, uuid: {}".format(code.pk, code.uuid)
    else:
        '''dry-run, so only display'''
        click.echo('The following code was created:')
        click.echo(code.full_text_info)
        click.echo('Recieved --dry-run, therefore not storing the code')
