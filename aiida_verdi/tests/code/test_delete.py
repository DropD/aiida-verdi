# -*- coding: utf8 -*-
"""
tests for verdi code delete
"""
import click
from click.testing import CliRunner


def test_delete_help():
    """
    action: verdi code delete --help
    behaviour: print help message
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['delete', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CODE' in result.output


def test_delete_noargs():
    """
    action: verdi code delete
    behaviour: fail with error msg
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['delete'])
    assert result.exception
    assert 'Usage' in result.output
    assert 'Missing argument' in result.output
