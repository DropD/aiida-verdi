# -*- coding: utf-8 -*-
"""
tests for verdi computer enable
"""
import click
from click.testing import CliRunner


def test_enable_help():
    """
    action: verdi computer enable --help
    behaviour: print help msg and exit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['enable', '--help'])
    assert not result.exception
    assert 'Usage' in result.output


def test_enable_noargs():
    """
    action: verdi computer enable
    behaviour: fail, print missing argument msg, exit
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['enable'])
    assert result.exception
    assert 'Missing argument' in result.output
