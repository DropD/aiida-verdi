#-*- coding: utf8 -*-
"""
verdi code show
"""
import click

from aiida_verdi import options
from aiida_verdi.param_types.code import CodeParam


@click.command()
@click.argument('_code', 'code', metavar='CODE', type=CodeParam())
def show(_code):
    """
    Show information on a given code
    """
    click.echo(_code.full_text_info)
