#-*- coding: utf8 -*-
"""
.. module::test_conditional
    :synopsis: Unit tests for :mod:`aiida_verdi.utils.conditional`
"""
import click
from click.testing import CliRunner

from aiida_verdi.utils.conditional import ConditionalOption


def simple_cmd(pname, required_fn=lambda ctx: ctx.params.get('on'), **kwargs):
    @click.command()
    @click.option(pname, is_eager=True, **kwargs)
    @click.option('--opt', required_fn=required_fn, cls=ConditionalOption)
    def cmd(on, opt):
        click.echo(opt)
    return cmd


def test_switch_off():
    cmd = simple_cmd('--on/--off')
    runner = CliRunner()
    result = runner.invoke(cmd, [])
    assert not result.exception


def test_switch_on():
    cmd = simple_cmd('--on/--off')
    runner = CliRunner()
    result = runner.invoke(cmd, ['--on'])
    assert result.exception


def test_flag_off():
    cmd = simple_cmd('--on', is_flag=True)
    runner = CliRunner()
    result = runner.invoke(cmd, [])
    assert not result.exception


def test_flag_on():
    cmd = simple_cmd('--on', is_flag=True)
    runner = CliRunner()
    result = runner.invoke(cmd, ['--on'])
    assert result.exception
