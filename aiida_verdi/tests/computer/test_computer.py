#-*- coding: utf8 -*-
"""
tests for verdi computer group
"""
import click
from click.testing import CliRunner


def test_computer_help():
    """
    action: verdi computer --help
    behaviour: display help message
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['--help'])
    assert not result.exception
    assert 'Usage' in result.output
