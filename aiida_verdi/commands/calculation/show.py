# -*- coding: utf-8 -*-
"""
verdi calculation show
"""
import click

from aiida_verdi import arguments


@click.command()
@arguments.calculation(nargs=-1)
def show(calc):
    """
    Show information about one or multiple CALCULATIONs
    """
    from aiida.cmdline.common import print_node_info

    table_headers = ['Link label', 'PK', 'Type']
    for c in calc:
        print_node_info(c)
