#-*- coding: utf8 -*-
"""
unittests for :py:class:`aiida_verdi.param_types.plugin.PluginParam`
"""
import click
from click.testing import CliRunner

from aiida_verdi.param_types.plugin import PluginParam


def setup_plugin_opt(**kwargs):
    """
    setup scenario plugin-opt:
        cmd with just an option of type plugin
    """
    category = kwargs.pop('category')
    @click.command()
    @click.option('--plugin', type=PluginParam(category), **kwargs)
    def cmd(plugin):
        click.echo(plugin)
    runner = CliRunner()
    return cmd, runner


def test_valid_calculation_plugin():
    """
    scenario: plugin-opt
    action: call with valid plugin name
    behaviour: command runs fine
    """
    cmd, runner = setup_plugin_opt(category='calculations')
    result = runner.invoke(cmd, ['--plugin=simpleplugins.templatereplacer'])
    assert not result.exception
    assert result.output == 'simpleplugins.templatereplacer\n'


def test_invalid_calculation_plugin():
    """
    scenario: plugin-opt
    action: call with invalid plugin name
    behaviour: command fails with invalid value message
    """
    cmd, runner = setup_plugin_opt(category='calculations')
    result = runner.invoke(cmd, ['--plugin=invalid.plugin.name'])
    assert result.exception
    assert 'Error: Invalid value for "--plugin"' in result.output


def test_empty_calculation_plugin():
    """
    scenario: plugin-opt
    action: call with valid plugin name
    behaviour: command runs fine
    """
    cmd, runner = setup_plugin_opt(category='calculations', required=True)
    result = runner.invoke(cmd, [])
    assert result.exception
    assert 'Error: Missing option "--plugin"' in result.output
    assert 'Possible arguments are' in result.output
