#-*- coding: utf8 -*-
"""
verdi code show
"""
import click

from aiida_verdi import options
from aiida_verdi.arguments import code


@click.command()
@code()
def show(_code):
    """
    Show information on a given code
    """
    click.echo(_code.full_text_info)
