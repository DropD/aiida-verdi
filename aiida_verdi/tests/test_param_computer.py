#-*- coding: utf8 -*-
"""
unit tests for :py:class:`aiida_verdi.param_types.computer.ComputerParam`
"""
import click
from click.testing import CliRunner

from aiida_verdi.param_types.computer import ComputerParam


def setup_comp_opt_cmd(convert=True, **kwargs):
    """
    scenario comp: simple cmd with only a ComputerParam option
    """
    @click.command()
    @click.option('--comp', type=ComputerParam(convert=convert), **kwargs)
    def cmd(comp):
        """dummy test command for ComputerParam tests"""
        click.echo(comp.__class__.__name__)
    runner = CliRunner()
    return cmd, runner


def test_missing():
    """
    scenario: comp, option required
    action: call without option
    behaviour: fail with missing command
    """
    cmd, runner = setup_comp_opt_cmd(required=True)
    result = runner.invoke(cmd, [])
    assert result.exception
    assert 'Missing option "--comp"' in result.output


def test_valid_convert():
    """
    scenario: comp
    action: call with valid computer name or pk
    behaviour: cmd gets valid Computer
    """
    cmd, runner = setup_comp_opt_cmd()
    comps = [i[0] for i in ComputerParam().complete()]
    assert comps
    result = runner.invoke(cmd, ['--comp={}'.format(comps[0])])
    assert not result.exception
    assert result.output == 'Computer\n'


def test_valid_noconvert():
    """
    scenario: comp but no conversion
    action: call with valid computer name or pk
    behaviour: cmd gets name (str) or pk (int)
    """
    cmd, runner = setup_comp_opt_cmd(convert=False)
    comps = [i[0] for i in ComputerParam().complete()]
    assert comps
    result = runner.invoke(cmd, ['--comp={}'.format(comps[0])])
    assert not result.exception
    assert result.output == 'int\n' or result.output == 'str\n'
