# -*- coding: utf-8 -*-
"""
test verdi computer delete
"""
import click
from click.testing import CliRunner


def test_delete_help():
    """
    action: verdi computer delete --help
    behaviour: print help msg and quit
    """
    from aiida_verdi.commands.computer.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['delete', '--help'])
    assert not result.exception
    assert 'Usage' in result.output


def test_delete_noarg():
    """
    action: verdi computer delete
    behaviour: fail, print missing args error msg and quit
    """
    from aiida_verdi.commands.computer.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['delete'])
    assert result.exception
    assert 'Missing argument' in result.output
