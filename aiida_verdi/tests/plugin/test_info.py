# -*- coding: utf8 -*-
"""
test verdi plugin info
"""
import click
from click.testing import CliRunner


def test_info_help():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['info', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'NAME' in result.output


def test_info_noarg():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['info'])
    assert result.exception
    assert 'Missing argument' in result.output


def test_info_mul():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['info', 'mul'])
    assert not result.exception
    assert 'aiida-mul' in result.output
