#-*- coding: utf8 -*-
"""
tests for verdi code setup
"""
import click
from click.testing import CliRunner

import mock


def fake_get_comp():
    from aiida.orm.computer import Computer
    def get(comphandle=4):
        return Computer()
    return get


def fake_complete(self, ctx=None, incomplete=None):
    return [('Computer', None)]


@mock.patch('aiida.orm.implementation.sqlalchemy.computer.Computer', autospec=True)
@mock.patch('aiida_verdi.param_types.computer.ComputerParam')
@mock.patch('aiida_verdi.verdic_utils.create_code')
def test_installed_interactive_dry(m1, ComputerParam, m3):
    ComputerParam.complete = fake_complete.__get__(ComputerParam)
    m1.get = fake_get_comp()
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(
        code,
        ['setup', '--dry-run'],
        input='Label\nDescription\ntrue\nsimpleplugins.templatereplacer\n?\nComputer\n/Path\n\quit\n\quit\n')
    assert not result.exception
    assert result.output == ''
