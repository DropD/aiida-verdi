# -*- coding: utf8 -*-
"""
test verdi plugin search
"""
import click
from click.testing import CliRunner


def test_search_help():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['search', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'PATTERN' in result.output
    assert '--relevance' in result.output


def test_search():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['search'])
    assert not result.exception
    assert 'mul' in result.output


def test_search():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['search', 'demonstration'])
    assert not result.exception
    assert 'mul' in result.output
