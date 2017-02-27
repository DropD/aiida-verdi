#-*- coding: utf8 -*-
"""
tests for verdi data command group
"""


import click
from click.testing import CliRunner


def test_data_help():
    from aiida_verdi.commands.data import data
    runner = CliRunner()
    result = runner.invoke(data, ['--help'])
    assert not result.exception
    assert 'Usage' in result.output
