# -*- coding: utf-8 -*-
"""
tests for verdi calculation outputls
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['outputls'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_outputls_help():
    """
    action: verdi calculation outputls --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_outputls_noargs():
    """
    action: verdi calculation outputls
    behaviour: exit with missing args msg
    """
    result = action()
    assert result.exception
    assert  'Missing argument "calc"' in result.output


def test_outputls_validarg():
    """
    action: verdi calculation outputls <valid calc>
    behaviour: print list of outputfiles or 'No retrived node' msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0])
        raises_sysexit = isinstance(result.exception, SystemExit)
        assert not result.exception or raises_sysexit
        if raises_sysexit:
            assert "No 'retrieved' node found" in result.output
        assert result.output


def test_outputls_validarg_invalidpath():
    """
    action: verdi calculation outputls <valid calc> -p <nonexistent path>
    behaviour: exit with 'No such file' msg or 'No retrieved' msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], path='/not/existent')
        assert isinstance(result.exception, SystemExit)
        no_retrieved = "No 'retrieved' node found" in result.output
        no_such_file = 'No such file or directory' in result.output
        assert no_retrieved or no_such_file


def test_outputls_invalidarg():
    """
    action: verdi calculation outputls <invalid calc>
    behaviour: exit with error msg
    """
    result = action(str(get_invalid_pk()))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output
