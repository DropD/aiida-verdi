#-*- coding: utf8 -*-
"""
tests for verdi code show
"""
import click
from click.testing import CliRunner


def test_code_show_help():
    """
    action: verdi code show --help
    behaviour: print help message
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['show', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
