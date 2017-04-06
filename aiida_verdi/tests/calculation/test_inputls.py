# -*- coding: utf-8 -*-
"""
tests for verdi calculation inputls
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['inputls'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_inputls_help():
    """
    action: verdi calculation inputls --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_inputls_noargs():
    """
    action: verdi calculation inputls
    behaviour: exit with missing args msg
    """
    result = action()
    assert result.exception
    assert  'Missing argument "calc"' in result.output


def test_inputls_valid_default():
    """
    action: verdi calculation inputls <valid calc>
    behaviour: print input file or error msg (if raw_input/ not in repo)
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0])
        raises_sysexit = isinstance(result.exception, SystemExit)
        assert not result.exception or raises_sysexit
        if raises_sysexit:
            assert 'No such file' in result.output
        assert result.output


def test_inputls_valid_path():
    """
    action: verdi calculation inputls <valid calc> -p .aiida
    behaviour: print contents of .aiida or no such folder msg and exit
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], path='.aiida')
        raises_sysexit = isinstance(result.exception, SystemExit)
        assert not result.exception or raises_sysexit
        if raises_sysexit:
            assert 'No such file or directory' in result.output
        else:
            assert 'calcinfo.json' in result.output


def test_inputls_invalidarg():
    """
    action: verdi calculation inputls <invalid calc>
    behaviour: exit with error msg
    """
    result = action(str(get_invalid_pk()))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output
