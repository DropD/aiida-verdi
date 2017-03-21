#-*- coding: utf8 -*-
"""
verdi code list
"""
import click

from aiida_verdi import options
from aiida_verdi.param_types.computer import ComputerParam
from aiida_verdi.param_types.plugin import PluginParam


@click.command('list')
@options.computer(type=ComputerParam(convert=False), help='filter codes for a computer')
@options.input_plugin(type=PluginParam(category='calculations', available=False))
@click.option('-A', '--all-users', is_flag=True, help='show codes of all users')
@click.option('-o', '--show-owner', is_flag=True, help='show owner information')
@click.option('all_codes', '-a', '--all', is_flag=True, help='show also hidden codes')
def list_(computer, input_plugin, all_users, show_owner, all_codes):
    """
    List available codes
    """
    from aiida_verdi.verdic_utils import print_list_res, load_dbenv_if_not_loaded
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
        click.echo('TEST')
