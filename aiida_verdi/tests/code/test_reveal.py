# -*- coding: utf8 -*-
"""
tests for verdi code reveal
"""
import click
from click.testing import CliRunner


def test_code_reveal_help():
    """
    action verdi code reveal --help
    behaviour: print help messge
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['reveal', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CODE' in result.output
    assert '--dry-run' in result.output


def test_code_reveal_none():
    """
    action verdi code reveal
    behaviour: noop
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['reveal'])
    assert not result.exception
    assert '' == result.output


def test_code_reveal_none_dr():
    """
    action verdi code reveal --dry-run
    behaviour: noop
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['reveal', '--dry-run'])
    assert not result.exception
    assert '--dry-run recieved' in result.output
