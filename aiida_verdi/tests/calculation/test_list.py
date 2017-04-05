# -*- coding: utf8 -*-
"""
tests for verdi calculation group
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['list'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_list_help():
    """
    action: verdi calculation list --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'PK' in result.output


def test_list_noargs():
    """
    action: verdi calculation list
    behaviour: print list (may be empty)
    """
    result = action()
    assert not result.exception


def test_all_states():
    """
    action: verdi calculation list --all-states
    behaviour: print list (may be empty)
    """
    result = action('--all-states')
    assert not result.exception
