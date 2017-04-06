# -*- coding: utf-8 -*-
"""
tests for verdi calculation plugins
"""
import click
from click.testing import CliRunner


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['plugins'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_plugins_help():
    """
    action: verdi calculation plugins --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'PLUGIN NAME' in result.output


def test_plugins_noargs():
    """
    action: verdi calculation plugins
    behaviour: print list, exit
    """
    result = action()
    assert not result.exception
    assert result.output


def test_plugins_validarg():
    """
    action: verdi calculation plugins simpleplugins.templatereplacer
    behaviour: print details, exit
    """
    result = action('simpleplugins.templatereplacer')
    assert not result.exception
    assert 'simpleplugins.templatereplacer' in result.output
    assert 'Inputs' in result.output
    assert 'Module location' in result.output


def test_plugins_invalidarg():
    """
    action: verdi calculation plugins <invalid plugin name>
    behaviour: exit with error msg
    """
    result = action('aiida_verdi/test/calculation/plugins/invalid_plugin')
    assert result.exception
    assert 'Invalid value for "input_plugin"' in result.output
