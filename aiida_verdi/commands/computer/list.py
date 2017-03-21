# -*- coding: utf8 -*-
"""
verdi computer list
"""
import click

from aiida_verdi import options
from aiida_verdi.utils.aiidadb import get_computer_names


@click.command('list')
@click.option('-C', '--color', is_flag=True, help='Use colors to help visualizing the different categories')
@click.option('-o', '--only-usable', is_flag=True, help='Show only computers that are usable (i.e., configured for the given user and enabled)')
@click.option('-p', '--parsable', is_flag=True, help='Show only the computer names, one per line, without any other information or string.')
@click.option('all_comps', '-a', '--all', is_flag=True, help='Show also disabled or unconfigured computers')
def list_(color, only_usable, parsable, all_comps):
    """
    List compute resources in AiiDA
    """
    from aiida_verdi.verdic_utils import load_dbenv_if_not_loaded
    load_dbenv_if_not_loaded()
    from aiida.orm.computer import Computer
    from aiida.backends.utils import get_automatic_user

    computer_names = get_computer_names()

    if color:
        color_id = 90  # Dark gray
        color_id = None  # Default color
        if color_id is not None:
            start_color = "\x1b[{}m".format(color_id)
            end_color = "\x1b[0m"
        else:
            start_color = ""
            end_color = ""
    else:
        start_color = ""
        end_color = ""

    if not parsable:
        click.echo("{}# List of configured computers:{}".format(
            start_color, end_color))
        click.echo("{}# (use 'verdi computer show COMPUTERNAME' "
                   "to see the details){}".format(start_color, end_color))
    if computer_names:
        for name in sorted(computer_names):
            computer = Computer.get(name)

            # color_id = 90 # Dark gray
            # color_id = 34 # Blue

            is_configured = computer.is_user_configured(get_automatic_user())
            is_user_enabled = computer.is_user_enabled(get_automatic_user())

            is_usable = False  # True if both enabled and configured

            if not all_comps:
                if not is_configured or not is_user_enabled or not computer.is_enabled():
                    continue

            if computer.is_enabled():
                if is_configured:
                    configured_str = ""
                    if is_user_enabled:
                        symbol = "*"
                        color_id = None
                        enabled_str = ""
                        is_usable = True
                    else:
                        symbol = "x"
                        color_id = 31  # Red
                        enabled_str = "[DISABLED for this user]"
                else:
                    symbol = "x"
                    color_id = 90  # Dark gray
                    enabled_str = ""
                    configured_str = " [unconfigured]"
            else:  # GLOBALLY DISABLED
                symbol = "x"
                color_id = 31  # Red
                if is_configured and not is_user_enabled:
                    enabled_str = " [DISABLED globally AND for this user]"
                else:
                    enabled_str = " [DISABLED globally]"
                if is_configured:
                    configured_str = ""
                else:
                    configured_str = " [unconfigured]"

            if color:
                if color_id is not None:
                    start_color = "\x1b[{}m".format(color_id)
                    bold_sequence = "\x1b[1;{}m".format(color_id)
                    nobold_sequence = "\x1b[0;{}m".format(color_id)
                else:
                    start_color = "\x1b[0m"
                    bold_sequence = "\x1b[1m"
                    nobold_sequence = "\x1b[0m"
                end_color = "\x1b[0m"
            else:
                start_color = ""
                end_color = ""
                bold_sequence = ""
                nobold_sequence = ""

            if parsable:
                click.echo("{}{}{}".format(start_color, name, end_color))
            else:
                if (not only_usable) or is_usable:
                    click.echo("{}{} {}{}{} {}{}{}".format(
                        start_color, symbol,
                        bold_sequence, name, nobold_sequence,
                        enabled_str, configured_str, end_color))

    else:
        click.echo("# No computers configured yet. Use 'verdi computer setup'")
