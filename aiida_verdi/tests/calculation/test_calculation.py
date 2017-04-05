# -*- coding: utf8 -*-
"""
tests for verdi calculation group
"""
import click
from click.testing import CliRunner


def test_calculation_help():
    """
    action: verdi calculation --help
    behaviour: display help message
    """
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    result = runner.invoke(calculation, ['--help'])
    assert not result.exception
    assert 'Usage' in result.output

