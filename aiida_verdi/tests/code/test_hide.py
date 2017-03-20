# -*- coding: utf8 -*-
"""
tests for verdi code hide
"""
import click
from click.testing import CliRunner


def test_code_hide_help():
    """
    action verdi code hide --help
    behaviour: print help messge
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['hide', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CODE' in result.output
    assert '--dry-run' in result.output


def test_code_hide_none():
    """
    action verdi code hide
    behaviour: noop
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['hide'])
    assert not result.exception
    assert '' == result.output


def test_code_hide_none_dr():
    """
    action verdi code hide --dry-run
    behaviour: noop
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['hide', '--dry-run'])
    assert not result.exception
    assert '--dry-run recieved' in result.output
