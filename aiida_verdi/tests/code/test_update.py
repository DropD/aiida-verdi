#-*- coding: utf8 -*-
"""
tests for verdi code update
"""
import click
from click.testing import CliRunner


def test_code_update_help():
    """
    action: verdi code update --help
    behaviour: print help message
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['update', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert '--label' in result.output
    assert '--description' in result.output
    assert '--input-plugin' in result.output
    assert '--append-text' in result.output
    assert '--prepend-text' in result.output
    assert '--dry-run' in result.output
    assert '--non-interactive' in result.output
