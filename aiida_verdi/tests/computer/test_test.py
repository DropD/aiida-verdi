# -*- coding: utf-8 -*-
"""
tests for verdi computer test
"""
import click
from click.testing import CliRunner


def test_test_help():
    """
    action: verdi computer test --help
    behaviour: print help msg, quit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['test', '--help'])
    assert not result.exception
    assert 'Usage' in result.output


def test_test_noargs():
    """
    action: verdi computer test
    behaviour: fail, print missing argument msg, quit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['test'])
    assert result.exception
    assert 'Missing argument' in result.output
