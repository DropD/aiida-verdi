# -*- coding: utf-8 -*-
"""
verdi calculation list
"""
import click

from aiida_verdi import arguments


@click.command()
@arguments.calculation()
@click.option('-f', '--format', 'format_', default='json+date', help="Format for the output.")
@click.option('-k', '--keys', multiple=True, help="[can be given multiple times] Show only the selected keys.")
def res(calc, format_, keys):
    """
    Show calculation results (from calc.res) for CALCULATION
    """
    from aiida.cmdline import print_dictionary
    full_dict = calc.res._get_dict()
    if keys:
        try:
            the_dict = {k: full_dict[k] for k in keys}
        except KeyError as e:
            raise click.ClickException("The key '{}' was not found in the .res dictionary".format(e.message))
    else:
        # Return all elements
        the_dict = full_dict

        print_dictionary(the_dict, format=format_)
