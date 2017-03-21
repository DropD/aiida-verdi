#-*- coding: utf8 -*-
"""
tests for verdi code list
"""
import click
from click.testing import CliRunner


def test_code_list_help():
    """
    action verdi code list --help
    behaviour: print help messge
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['list', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert '--computer' in result.output
    assert '--input-plugin' in result.output
    assert '--all-users' in result.output
    assert '--show-owner' in result.output
    assert '--all' in result.output
