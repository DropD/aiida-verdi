# -*- coding: utf8 -*-
"""
verdi computer show
"""
import click

from aiida_verdi import arguments


@click.command()
@arguments.computer()
def show(computer):
    """
    Show information on an AiiDA computer
    """
    click.echo(computer.full_text_info)
