#-*- coding: utf8 -*-
"""
.. module::test_conditional
    :synopsis: Unit tests for :mod:`aiida_verdi.utils.conditional`
"""
import click
from click.testing import CliRunner

from aiida_verdi.utils.conditional import ConditionalOption


def simple_cmd(pname, required_fn=lambda ctx: ctx.params.get('on'), **kwargs):
    """
    returns a command with two options:

        * an option created from the args and kwargs
        * --opt, ConditionalOption with required_fn from kwargs
    """
    @click.command()
    @click.option(pname, **kwargs)
    @click.option('--opt', required_fn=required_fn, cls=ConditionalOption)
    def cmd(on, opt):
        """dummy command for testing"""
        click.echo(opt)
    return cmd


def test_switch_off():
    """
    scenario: flag on/off and option opt required if flag is on
    action: invoke with no options
    behaviour: flag is off by default -> command runs without complaining
    """

    cmd = simple_cmd('--on/--off')
    runner = CliRunner()
    result = runner.invoke(cmd, [])
    assert not result.exception


def test_switch_on():
    """
    scenario: flag on/off and option opt required if flag is on
    action: invoke with --on
    behaviour: fails with Missin option message
    """
    cmd = simple_cmd('--on/--off')
    runner = CliRunner()
    result = runner.invoke(cmd, ['--on'])
    assert result.exception
    assert 'Error: Missing option "--opt".' in result.output


def test_flag_off():
    """
    scenario: flag on and option opt required if on==True
    action: invoke without options
    behaviour: command runs without complaining
    """
    cmd = simple_cmd('--on', is_flag=True)
    runner = CliRunner()
    result = runner.invoke(cmd, [])
    assert not result.exception


def test_flag_on():
    """
    scenario: flag on and option opt required if on==True
    action: invoke with --on
    behaviour: fails with Missing option message
    """
    cmd = simple_cmd('--on', is_flag=True)
    runner = CliRunner()
    result = runner.invoke(cmd, ['--on'])
    assert result.exception
    assert 'Error: Missing option "--opt".' in result.output


def setup_multi_non_eager():
    """
    scenario a-or-b:

        * flag a_or_b
        * opt-a required if a_or_b == True
        * opt-b required if a_or_b == False
    """
    @click.command()
    @click.option('--a/--b', 'a_or_b')
    @click.option('--opt-a', required_fn=lambda c: c.params.get('a_or_b'),
                  cls=ConditionalOption)
    @click.option('--opt-b', required_fn=lambda c: not c.params.get('a_or_b'),
                  cls=ConditionalOption)
    def cmd(a_or_b, opt_a, opt_b):
        """test command for scenario a-or-b"""
        click.echo('{} / {}'.format(opt_a, opt_b))

    runner = CliRunner()
    return runner, cmd


def test_aa():
    """
    scenario = a-or-b
    action: require a, give a (+ reversed order)
    behaviour: command runs
    """
    runner, cmd = setup_multi_non_eager()
    result = runner.invoke(cmd, ['--a', '--opt-a=Bla'])
    assert not result.exception
    assert result.output == 'Bla / None\n'

    result_rev = runner.invoke(cmd, ['--opt-a=Bla', '--a'])
    assert not result_rev.exception
    assert result_rev.output == 'Bla / None\n'


def test_ab():
    """
    scenario = a-or-b
    action: require a, give b (+ reversed order)
    behaviour: fail, Missing option
    """
    runner, cmd = setup_multi_non_eager()
    result = runner.invoke(cmd, ['--a', '--opt-b=Bla'])
    assert result.exception
    assert 'Error: Missing option "--opt-a".' in result.output

    result_rev = runner.invoke(cmd, ['--opt-b=Bla', '--a'])
    assert result_rev.exception
    assert 'Error: Missing option "--opt-a".' in result_rev.output


def test_bb():
    """
    scenario = a-or-b
    action: require b, give a (+ reversed order)
    behaviour: fail, Missing option
    """
    runner, cmd = setup_multi_non_eager()
    result = runner.invoke(cmd, ['--b', '--opt-a=Bla'])
    assert result.exception
    assert 'Error: Missing option "--opt-b".' in result.output

    result_rev = runner.invoke(cmd, ['--opt-a=Bla', '--b'])
    assert result_rev.exception
    assert 'Error: Missing option "--opt-b".' in result_rev.output


def test_ba():
    """
    scenario = a-or-b
    action: require b, give b (+ reversed order)
    behaviour: command works
    """
    runner, cmd = setup_multi_non_eager()
    result = runner.invoke(cmd, ['--b', '--opt-b=Bla'])
    assert not result.exception
    assert result.output == 'None / Bla\n'

    result_rev = runner.invoke(cmd, ['--opt-b=Bla', '--b'])
    assert not result_rev.exception
    assert result_rev.output == 'None / Bla\n'
