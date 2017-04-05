# -*- coding: utf-8 -*-
"""
tests for verdi computer disable
"""
import click
from click.testing import CliRunner


def test_disable_help():
    """
    action: verdi computer disable --help
    behaviour: print help msg and exit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['disable', '--help'])
    assert not result.exception
    assert 'Usage' in result.output


def test_disable_noargs():
    """
    action: verdi computer disable
    behaviour: fail, print missing argument msg, exit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['disable'])
    assert result.exception
    assert 'Missing argument' in result.output
