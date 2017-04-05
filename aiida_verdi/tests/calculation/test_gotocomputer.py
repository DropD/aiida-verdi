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
    cliargs = ['gotocomputer'] + list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(calculation, cliargs)


def test_gotocomputer_help():
    """
    action: verdi calculation gotocomputer --help
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
    assert 'CALCULATION' in result.output


def test_gotocomp_noargs():
    """
    action: verdi calculation gotocomputer
    behaviour: exit with missing arg msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument' in result.output


def get_valid_compl_item():
    from aiida.orm import load_node
    from aiida.orm import JobCalculation

    from aiida_verdi.param_types.jobcalc import JobCalcParam
    calclist = [i for i in JobCalcParam().complete()
                if isinstance(load_node(int(i[0])), JobCalculation)
                and bool(load_node(int(i[0]))._get_remote_workdir())]
    if calclist:
        return calclist[0]
    else:
        return None


def test_gotocomp_valid_dry():
    """
    action: verdi calculation gotocomputer <valid computer> --dry-run
    behaviour: print command and dry-run message
    """
    citem = get_valid_compl_item()
    if citem:
        result = action(citem[0], '--dry-run')
        assert not result.exception
        assert '--dry-run recieved' in result.output


def test_gotocomp_invalid_dry():
    """
    action: verdi calculation gotocomputer <invalid computer> --dry-run
    behaviour: print invalid arg msg and exit
    """
    invalid = get_invalid_pk()
    result = action(str(invalid))
    assert result.exception
    assert 'Invalid value for "calc"' in result.output
