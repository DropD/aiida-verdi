# -*- coding: utf8 -*-
"""
test verdi plugin search
"""
import click
from click.testing import CliRunner


def test_search_help():
    """
    action: verdi plugins search --help
    behaviour: exit with help msg
    """
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['search', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'PATTERN' in result.output
    assert '--relevance' in result.output


def test_search():
    """
    action: verdi plugins search
    behaviour: (if connection) return list of available plugins
    """
    from aiida_verdi.commands.plugin import plugin
    import requests as rq
    runner = CliRunner()
    result = runner.invoke(plugin, ['search'])
    if not isinstance(result.exception, rq.ConnectionError):
        assert not result.exception
        assert 'mul' in result.output


def test_search_args():
    """
    action: verdi plugins search demonstration
    behaviour: (if connection) return filtered list
    """
    from aiida_verdi.commands.plugin import plugin
    import requests as rq
    runner = CliRunner()
    result = runner.invoke(plugin, ['search', 'demonstration'])
    if not isinstance(result.exception, rq.ConnectionError):
        assert not result.exception
        assert 'mul' in result.output
