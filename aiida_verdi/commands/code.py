#-*- coding: utf8 -*-
"""
verdi code commands
"""
import sys
import click

from aiida_verdi import options
from aiida_verdi.verdic_utils import (
    load_dbenv_if_not_loaded,
    prompt_with_help,
    computer_validator, multi_line_prompt, create_code,
    InteractiveOption)
from aiida_verdi.utils.interactive import InteractiveOption
from aiida_verdi.param_types.code import CodeParam
from aiida_verdi.param_types.plugin import PluginParam


@click.group()
def code():
    """
    manage codes in your AiiDA database.
    """


@code.command('list')
@click.option('-c', '--computer', help='filter codes for a computer')
#@click.option('-p', '--plugin', type=PluginParam('calculations'), help='filter codes for a plugin')
@options.input_plugin(type=PluginParam(category='calculations', available=False))
@click.option('-A', '--all-users', is_flag=True, help='show codes of all users')
@click.option('-o', '--show-owner', is_flag=True, help='show owner information')
@click.option('-a', '--all-codes', is_flag=True, help='show hidden codes')
def _list(computer, input_plugin, all_users, show_owner, all_codes):
    """
    List available codes
    """
    from aiida_verdi.verdic_utils import print_list_res
    load_dbenv_if_not_loaded()

    computer_filter = computer
    plugin_filter = input_plugin
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

    click.echo("# List of configured codes:")
    click.echo("# (use 'verdi code show CODEID | CODENAME' to see the details)")
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
@click.argument('_code', 'code', metavar='CODE', type=CodeParam())
def show(_code):
    """
    Show information on a given code
    """
    click.echo(_code.full_text_info)


def validate_computer(value, param, ctx):
    """validation callback for computers, wraps around utils.computer_validator.throw"""
    return computer_validator().throw(value, param, ctx)[1]

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
@options.label(prompt='Label', cls=InteractiveOption, help='A label to refer to this code')
@options.description(prompt='Description', cls=InteractiveOption, help='A human-readable description of this code')
@click.option('--installed/--upload', is_eager=False, default=True, prompt='Preinstalled?', cls=InteractiveOption, help=('installed: the executable is installed on the remote computer. ' 'upload: the executable has to be copied onto the computer before execution.'))
@options.input_plugin(prompt='Default input plugin', cls=InteractiveOption)
@click.option('--code-folder', prompt='Folder containing the code', type=click.Path(file_okay=False, exists=True, readable=True), required_fn=lambda c: not c.params.get('installed'), cls=InteractiveOption, help=('[if --upload]: folder containing the executable and ' 'all other files necessary for execution of the code'))
@click.option('--code-rel-path', prompt='Relative path of the executable', type=click.Path(dir_okay=False), required_fn=lambda c: not c.params.get('installed'), cls=InteractiveOption, help=('[if --upload]: The relative path of the executable file inside ' 'the folder entered in the previous step or in --code-folder'))
@click.option('--computer', prompt='Remote computer', cls=InteractiveOption, required_fn=lambda c: c.params.get('installed'), callback=validate_computer, help=('[if --installed]: The name of the computer on which the ' 'code resides as stored in the AiiDA database'))
@click.option('--remote-abs-path', prompt='Remote path', type=click.Path(file_okay=False), required_fn=lambda c: c.params.get('installed'), cls=InteractiveOption, help=('[if --installed]: The (full) absolute path on the remote ' 'machine'))
@click.option('--prepend-text', callback=prepend_callback, help='Text to prepend to each command execution. FOR INSTANCE, MODULES TO BE LOADED FOR THIS CODE. This is a multiline string, whose content will be prepended inside the submission script after the real execution of the job. It is your responsibility to write proper bash code!')
@click.option('--append-text', callback=append_callback, help='Text to append to each command execution. This is a multiline string, whose content will be appended inside the submission script after the real execution of the job. It is your responsibility to write proper bash code!')
@options.non_interactive()
@options.dry_run()
@options.debug()
def setup(**kwargs):
    """create and store a code on the commandline"""
    from aiida.common.exceptions import ValidationError

    click.echo(kwargs['computer'])
    load_dbenv_if_not_loaded()

    the_code = create_code(**kwargs)

    '''Enforcing the code to be not hidden.'''
    the_code._reveal()

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
