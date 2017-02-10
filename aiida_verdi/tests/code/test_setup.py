#-*- coding: utf8 -*-
"""
tests for verdi code setup
"""
import click
from click.testing import CliRunner

import mock


def fake_get_comp(self, comphandle):
    from aiida.orm.computer import Computer
    return Computer()


def fake_comp_complete(ctx, incomplete):
    return [('Computer', None)]


@mock.patch('aiida.orm.computer.Computer.get', new_callable=fake_get_comp)
@mock.patch('aiida_verdi.param_types.computer.ComputerParam.complete', new_callable=fake_comp_complete, ctx=None, incomplete=None)
@mock.patch('aiida_verdi.verdic_utils.create_code')
def test_installed_interactive_dry(comp, crco):
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(
        code,
        ['setup', '--dry-run'],
        input='Label\nDescription\ntrue\nsimpleplugins.templatereplacer\nComputer\n/Path\n\quit\n\quit\n')
    assert not result.exception
    assert result.output == ''
