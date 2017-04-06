# -*- coding: utf-8 -*-
"""
tests for verdi calculation cleanworkdir
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    input_ = kwargs.pop('input', None)
    runner = CliRunner()
    cliargs = ['cleanworkdir'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs, input=input_)


def test_cleanworkdir_help():
    """
    action: verdi calculation cleanworkdir --help
    behaviour: print help msg and exit
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_cleanworkdir_noarg():
    """
    action: verdi calculation cleanworkdir
    behaviour: exit with error msg
    """
    result = action()
    assert isinstance(result.exception, SystemExit)
    assert 'Error: You should specify' in  result.output


def test_cleanworkdir_invalidarg_dry():
    """
    action: verdi calculation cleanworkdir --calc <invalid calculation>
    behaviour: exit with invalid args error
    """
    result = action('--dry-run', calc=str(get_invalid_pk()))
    assert result.exception
    assert 'Invalid value for "-c" / "--calc"' in  result.output


def test_cleanworkdir_validarg_dry():
    """
    action: verdi calculation cleanworkdir <valid calculation> --dry-run, input 'y' at prompt
    behaviour: ask for confirmation, output info, don't clean workdir
    """
    item = get_valid_compl_item()
    if item:
        result = action('--dry-run', calc=item[0], input='y\n')
        assert not result.exception
        assert '--dry-run recieved' in result.output


def test_cleanworkdir_validarg_dry_ni():
    """
    action: verdi calculation cleanworkdir <valid calculation> --dry-run --non-interactive
    behaviour: don't ask for confirmation, don't clean workdir, print force missing msg, exit successfully
    """
    item = get_valid_compl_item()
    if item:
        result = action('--dry-run', '--non-interactive', calc=item[0])
        assert not result.exception
        assert '--force not given' in result.output


def test_cleanworkdir_validarg_dry_force():
    """
    action: verdi calculation cleanworkdir <valid calc> --dry-run --force
    behaviour: don't ask, don't try to clean workdir
    """
    item = get_valid_compl_item()
    if item:
        result = action('--dry-run', '--force', calc=item[0])
        assert not result.exception
        assert '--dry-run recieved' in result.output


def test_cleanworkdir_validarg_dry_force_ni():
    """
    action: verdi calculation cleanworkdir <valid calc> --dry-run --force --non-interactive
    behaviour: don't ask, don't clean workdir
    """
    item = get_valid_compl_item()
    if item:
        result = action('--dry-run', '--force', '--non-interactive', calc=item[0])
        assert not result.exception
        assert '--dry-run recieved' in result.output


def test_cleanworkdir_c_and_p():
    """
    action: verdi calculation cleanworkdir --calc <valid calc> --past-days 5
    behaviour: fail with error msg
    """
    item = get_valid_compl_item()
    if item:
        result = action('--dry-run', '--non-interactive', calc=item[0], past_days=5)
        assert isinstance(result.exception, SystemExit)
        assert 'You cannot specify' in result.output


def test_cleanworkdir_c_and_o():
    """
    action: verdi calculation cleanworkdir --calc <valid calc> --older-than 5
    behaviour: fail with error msg
    """
    item = get_valid_compl_item()
    if item:
        result = action('--dry-run', '--non-interactive', calc=item[0], older_than=5)
        assert isinstance(result.exception, SystemExit)
        assert 'You cannot specify' in result.output


def test_cleanworkdir_p_and_o():
    """
    action: verdi calculation cleanworkdir --calc <valid calc> --older-than 5
    behaviour: fail with error msg
    """
    result = action('--dry-run', '--non-interactive', past_days=5, older_than=5)
    assert isinstance(result.exception, SystemExit)
    assert 'Not both' in result.output
