# -*- coding: utf8 -*-
"""
test verdi plugin info
"""
from click.testing import CliRunner


def test_info_help():
    """
    action: verdi plugins info --help
    behaviour: exit with help msg
    """
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['info', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'NAME' in result.output


def test_info_noarg():
    """
    action: verdi plugins info
    behaviour: exit with missing arg msg
    """
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['info'])
    assert result.exception
    assert 'Missing argument' in result.output


def test_info_mul():
    """
    action: verdi plugins info mul
    behaviour: (if connection) print details of plugin mul
    """
    from aiida_verdi.commands.plugin import plugin
    import requests as rq
    runner = CliRunner()
    result = runner.invoke(plugin, ['info', 'mul'])
    if not isinstance(result.exception, rq.ConnectionError):
        assert not result.exception
        assert 'aiida-mul' in result.output
