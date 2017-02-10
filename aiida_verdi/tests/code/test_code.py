#-*- coding: utf8 -*-
"""
tests for verdi code command group
"""
import click
from click.testing import CliRunner
import pytest
from pkg_resources import iter_entry_points


@pytest.mark.parametrize('subcmd', (i.name for i in iter_entry_points('aiida.cmdline.code')))
def test_subcommand_help(subcmd):
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, [subcmd, '--help'])
    assert not result.exception
    assert 'Usage:' in result.output
