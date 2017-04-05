#-*- coding: utf8 -*-
"""
unit tests for :py:class:`aiida_verdi.param_types.jobcalc.JobCalcParam`
"""
import click
from click.testing import CliRunner

from aiida_verdi.param_types.jobcalc import JobCalcParam


def scenario_jobcalc(convert=True, **kwargs):
    """
    scenario jobcalc: takes JobCalc option, displays uuid
    """
    @click.command()
    @click.option('--calc', type=JobCalcParam(convert=convert), **kwargs)
    def cmd(calc):
        """dummy test command for JobCalcParam"""
        if hasattr(calc, 'uuid'):
            click.echo(calc.uuid)
            click.echo('converted')
        else:
            click.echo(calc)
            click.echo('not converted')
        click.echo('Done')
    runner = CliRunner()
    return cmd, runner


def action(scenario, *args, **kwargs):
    cmd, runner = scenario
    cliargs = list(args) + ['--{}={}'.format(k, v) for k, v in kwargs.iteritems()]
    return runner.invoke(cmd, cliargs)


def test_missing_convert():
    """
    scenario: calc required
    action: call without calc
    behaviour: fail with missing option msg
    """
    scenario = scenario_jobcalc(required=True)
    result = action(scenario)
    assert result.exception
    assert 'Missing option "--calc"' in result.output


def test_missing_nonconvert():
    """
    scenario: calc required, non converting
    action: call without calc
    behaviour fail with missing option msg
    """
    scenario = scenario_jobcalc(required=True, convert=False)
    result = action(scenario)
    assert result.exception
    assert 'Missing option "--calc"' in result.output


def get_valid_compl_item():
    from aiida.orm import load_node
    from aiida.orm import JobCalculation
    calclist = [i for i in JobCalcParam().complete() if isinstance(load_node(int(i[0])), JobCalculation)]
    if calclist:
        return calclist[0]
    else:
        return None


def get_invalid_pk():
    from aiida.orm import load_node
    from aiida.orm import JobCalculation
    pklist = [i[0] for i in JobCalcParam().complete() if isinstance(load_node(int(i[0])), JobCalculation)]
    invalid = 1
    while invalid in pklist:
        invalid += 1
    return invalid


def test_valid_convert():
    """
    action: call with valid calc pk
    behaviour: succeeds printing uuid and 'converted'
    """
    scenario = scenario_jobcalc()
    item = get_valid_compl_item()
    if item:
        pk = item[0]
        result = action(scenario, calc=pk)
        assert not result.exception
        assert result.output.split('\n')[0] in item[1]
        assert 'converted' in result.output

def test_valid_nonconvert():
    """
    action: call with valid calc pk
    behaviour: succeeds printing uuid and 'not converted'
    """
    scenario = scenario_jobcalc(convert=False)
    item = get_valid_compl_item()
    if item:
        result = action(scenario, calc=item[0])
        assert not result.exception
        assert result.output.split('\n')[0] in item[1]
        assert 'not converted' in result.output


def test_invalid_convert():
    """
    action: call with invalid calc pk
    behaviour: exits with invalid param msg
    """
    scenario = scenario_jobcalc()
    invalid = get_invalid_pk()
    result = action(scenario, calc=invalid)
    assert result.exception
    assert 'Invalid value for "--calc"' in  result.output


def test_non_pk_arg():
    """
    action: call with pk < 1
    behaviour: exits with invalid param msg
    """
    scenario = scenario_jobcalc()
    result = action(scenario, calc=0)
    assert result.exception
    assert 'Invalid value for "--calc"' in  result.output
