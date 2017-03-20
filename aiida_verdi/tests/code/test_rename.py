# -*- coding: utf8 -*-
"""
tests for verdi code rename
"""
import click
from click.testing import CliRunner


def test_rename_help():
    """
    action: verdi code rename --help
    behaviour: print help message
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['rename', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CODE' in result.output
    assert 'NAME' in result.output
    assert '--dry-run' in result.output
