# -*- coding: utf-8 -*-
"""
tests for verdi calculation outputcat
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['outputcat'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_outputcat_help():
    """
    action: verdi calculation outputcat --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_outputcat_noargs():
    """
    action: verdi calculation outputcat
    behaviour: exit with missing args msg
    """
    result = action()
    assert result.exception
    assert  'Missing argument "calc"' in result.output


def test_outputcat_valid_default():
    """
    action: verdi calculation outputcat <valid calc>
    behaviour: print input file or error msg (if no default output defined / present / not retrieved), exit
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0])
        raises_sysexit = isinstance(result.exception, SystemExit)
        assert not result.exception or raises_sysexit
        if raises_sysexit:
            no_default = 'does not define a default' in result.output
            no_such_file = "No such file" in result.output
            no_retrieved = "No 'retrieved' node found" in result.output
            assert no_default or no_such_file or no_retrieved
        assert result.output


def test_outputcat_invalidarg():
    """
    action: verdi calculation outputcat <invalid calc>
    behaviour: exit with error msg
    """
    result = action(str(get_invalid_pk()))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output
