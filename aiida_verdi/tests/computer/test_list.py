# -*- coding: utf8 -*-
"""
tests for verdi computer list
"""
import click
from click.testing import CliRunner


def test_list_help():
    """
    action: verdi computer list --help
    behaviour: print help message
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['list', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert '--color' in result.output
    assert '--only-usable' in result.output
    assert '--parsable' in result.output
    assert '--all' in result.output
