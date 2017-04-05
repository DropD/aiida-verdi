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
    cliargs = ['logshow'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_logshow_help():
    """
    action: verdi calculation logshow --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_logshow_noargs():
    """
    action: verdi calculation show
    behaviour: exit with missing arg msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument "calc"' in result.output


def test_logshow_valid():
    """
    action: verdi calculation show <valid calculation>
    behaviour: print show
    """
    citem = get_valid_compl_item()
    if citem:
        result = action(citem[0])
        assert not result.exception
        assert result.output


def test_logshow_invalid():
    """
    action verdi calculation show <invalid calculation>
    behaviour: exit with error msg
    """
    invalid = get_invalid_pk()
    result = action(str(invalid))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output

