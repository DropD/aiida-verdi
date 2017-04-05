# -*- coding: utf8 -*-
"""
tests for verdi calculation group
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.test_param_jobcalc import get_invalid_pk, get_valid_compl_item


def action(*args, **kwargs):
    from aiida_verdi.commands.calculation import calculation
    runner = CliRunner()
    cliargs = ['res'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_res_help():
    """
    action: verdi calculation res --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_res_noargs():
    """
    action: verdi calculation res
    behaviour: exit with missing arg msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument' in result.output


def test_res_valid():
    """
    action: verdi calculation res <valid calculation>
    behaviour: print res
    """
    citem = get_valid_compl_item()
    if citem:
        result = action(citem[0])
        assert not result.exception
        assert result.output


def test_res_invalid():
    """
    action verdi calculation res <invalid calculation>
    behaviour: exit with error msg
    """
    invalid = get_invalid_pk()
    result = action(str(invalid))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output
