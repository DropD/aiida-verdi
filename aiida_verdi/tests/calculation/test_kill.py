# -*- coding: utf-8 -*-
"""
tests for verdi calculation kill
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    input_ = kwargs.pop('input', None)
    runner = CliRunner()
    cliargs = ['kill'] + list(args) + ['--{}={}'.format(k, v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs, input=input_)


def test_kill_help():
    """
    action: verdi calculation kill --help
    behaviour: print help msg and exit
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_kill_noarg():
    """
    action: verdi calculation kill
    behaviour: do nothing
    """
    result = action()
    assert not result.exception
    assert not result.output


def test_kill_invalidarg_dry():
    """
    action: verdi calculation kill <invalid calculation>
    behaviour: exit with invalid args error
    """
    result = action(str(get_invalid_pk()), '--dry-run')
    assert result.exception
    assert 'Invalid value for "calc"' in  result.output


def test_kill_validarg_dry():
    """
    action: verdi calculation kill <valid calculation> --dry-run, input 'y' at prompt
    behaviour: ask for confirmation, don't try to kill
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', input='y\n')
        assert not result.exception
        assert '--dry-run recieved' in result.output


def test_kill_validarg_dry_ni():
    """
    action: verdi calculation kill <valid calculation> --dry-run --non-interactive
    behaviour: ask for confirmation, don't try to kill
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', '--non-interactive')
        assert not result.exception
        assert not result.output


def test_kill_validarg_dry_force():
    """
    action: verdi calculation kill <valid calc> --dry-run --force
    behaviour: don't ask, don't try to kill
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', '--force')
        assert not result.exception
        assert '--dry-run recieved' in result.output


def test_kill_validarg_dry_force_ni():
    """
    action: verdi calculation kill <valid calc> --dry-run --force --non-interactive
    behaviour: don't ask, don't try to kill
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', '--force', '--non-interactive')
        assert not result.exception
        assert '--dry-run recieved' in result.output
