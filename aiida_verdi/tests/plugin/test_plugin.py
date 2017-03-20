# -*- coding: utf8 -*-
"""
test verdi plugin group
"""
import click
from click.testing import CliRunner


def test_plugin_help():
    from aiida_verdi.commands.plugin import plugin
    runner = CliRunner()
    result = runner.invoke(plugin, ['--help'])
    assert not result.exception
    assert 'Usage' in result.output
