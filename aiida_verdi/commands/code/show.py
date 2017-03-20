#-*- coding: utf8 -*-
"""
verdi code show
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.code()
def show(code):
    """
    Show information on a given code
    """
    click.echo(code.full_text_info)
