# -*- coding: utf-8 -*-
"""
tests for verdi calculation inputcat
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['inputcat'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_inputcat_help():
    """
    action: verdi calculation inputcat --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_inputcat_noargs():
    """
    action: verdi calculation inputcat
    behaviour: exit with missing args msg
    """
    result = action()
    assert result.exception
    assert  'Missing argument "calc"' in result.output


def test_inputcat_valid_default():
    """
    action: verdi calculation inputcat <valid calc>
    behaviour: print input file or error msg (if no default input defined / present), exit
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0])
        raises_sysexit = isinstance(result.exception, SystemExit)
        assert not result.exception or raises_sysexit
        if raises_sysexit:
            no_default = 'does not define a default' in result.output
            no_such_file = 'No such file' in result.output
            assert no_default or no_such_file
        assert result.output


def test_inputcat_valid_path():
    """
    action: verdi calculation inputcat <valid calc> -p _aiidasubmit.sh
    behaviour: print submit file or no such file msg and exit
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], path='_aiidasubmit.sh')
        raises_sysexit = isinstance(result.exception, SystemExit)
        assert not result.exception or raises_sysexit
        if raises_sysexit:
            assert 'No such file' in result.output
        else:
            assert '#!' in result.output


def test_inputcat_invalidarg():
    """
    action: verdi calculation inputcat <invalid calc>
    behaviour: exit with error msg
    """
    result = action(str(get_invalid_pk()))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output
