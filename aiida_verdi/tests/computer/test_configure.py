# -*- coding: utf8 -*-
"""
tests for verdi computer configure
"""
import click
from click.testing import CliRunner


def test_configure_help():
    """
    action: verdi computer configure --help
    behaviour: print help msg and quit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['configure', '--help'])
    assert not result.exception
    assert 'Usage' in result.output


def test_configure_ni_empty():
    """
    action: verdi computer configure --dry-run
    behaviour: fail, print missing argument msg and quit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['configure', '--dry-run'])
    assert result.exception
    assert 'Missing argument' in result.output
