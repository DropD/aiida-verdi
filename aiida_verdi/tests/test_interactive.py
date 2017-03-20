#-*- coding: utf8 -*-
"""
Unit tests for :py:class:`aiida_verdi.utils.interactive.InteractiveOption`
"""
import pytest
import click
from click.testing import CliRunner

from aiida_verdi.utils.interactive import InteractiveOption
from aiida_verdi import options


def simple_command(**kwargs):
    """
    return a simple command with one InteractiveOption,
    kwargs get relayed to the option
    """
    @click.command()
    @click.option('--opt', prompt='Opt', cls=InteractiveOption, **kwargs)
    @options.non_interactive()
    def cmd(opt, non_interactive):
        """test command for InteractiveOption"""
        click.echo(str(opt))
    return cmd


def prompt_output(cli_input, converted=None):
    """return expected output of simple_command, given a commandline cli_input string"""
    return "Opt: {}\n{}\n".format(cli_input, converted or cli_input)


def test_prompt_str():
    """
    scenario: using InteractiveOption with type=str
    behaviour: giving no option prompts, accepts a string
    """
    cmd = simple_command(type=str)
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='TEST\n')
    expected = prompt_output('TEST')
    assert not result.exception
    assert result.output == expected


def test_prompt_empty_input():
    """
    scenario: using InteractiveOption with type=str and invoking without options
    behaviour: pressing enter on empty line at prompt repeats the prompt without
        a message
    """
    cmd = simple_command(type=str)
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='\nTEST\n')
    expected = "Opt: \nOpt: TEST\nTEST\n"
    assert not result.exception
    assert result.output == expected


def test_prompt_help_default():
    """
    scenario: using InteractiveOption with type=str and no help parameter
        and invoking without options
    behaviour: entering '?' leads to a default help message being printed
        and prompt repeated
    """
    cmd = simple_command(type=str)
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='?\nTEST\n')
    expected = "Opt: ?\n\tExpecting text\nOpt: TEST\nTEST\n"
    assert not result.exception
    assert result.output == expected


def test_prompt_help_custom():
    """
    scenario: using InteractiveOption with type=str and help message
        and invoking without options
    behaviour: entering '?' leads to the given help message being printed
        and the prompt repeated
    """
    cmd = simple_command(type=str, help='Please enter some text')
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='?\nTEST\n')
    expected = "Opt: ?\n\tPlease enter some text\nOpt: TEST\nTEST\n"
    assert not result.exception
    assert result.output == expected


@pytest.mark.parametrize(('ptype', 'cli_input', 'output'),
                         [(bool, 'true', 'True'), (int, '98', '98'),
                          (float, '3.14e-7', '3.14e-07')])
def test_prompt_simple(ptype, cli_input, output):
    """
    scenario: using InteractiveOption with type=bool
    behaviour: giving no option prompts, accepts 'true'
    """
    cmd = simple_command(type=ptype, help='help msg')
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='\n?\n{}\n'.format(cli_input))
    expected = 'Opt: \nOpt: ?\n\thelp msg\n'
    expected += prompt_output(cli_input, output)
    assert not result.exception
    assert result.output == expected


def strip_line(text):
    """returns text without the last line"""
    return text.rsplit('\n')[0]


@pytest.mark.parametrize(('ptype', 'cli_input'),
                         [(click.File(), __file__),
                          (click.Path(exists=True), __file__)])
def test_prompt_complex(ptype, cli_input):
    """
    scenario: using InteractiveOption with type=float
    behaviour: giving no option prompts, accepts 3.14e-7
    """
    cmd = simple_command(type=ptype, help='help msg')
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='\n?\n{}\n'.format(cli_input))
    expected_beginning = 'Opt: \nOpt: ?\n\thelp msg\n'
    expected_beginning += strip_line(prompt_output(cli_input))
    assert not result.exception
    assert result.output.startswith(expected_beginning)


def test_default_value_prompt():
    """
    scenario: using InteractiveOption with a default value, invoke without options
    behaviour: prompt, showing the default value, take default on empty cli_input.
    """
    returns = []
    cmd = simple_command(default='default')
    runner = CliRunner()
    result = runner.invoke(cmd, [], input='\n')
    returns.append(result)
    expected = 'Opt [default]: \ndefault\n'
    assert not result.exception
    assert result.output == expected
    result = runner.invoke(cmd, [], input='TEST\n')
    returns.append(result)
    expected = 'Opt [default]: TEST\nTEST\n'
    assert not result.exception
    assert result.output == expected
    return returns


def test_default_value_empty_opt():
    """
    scenario: InteractiveOption with default value, invoke with empty option (--opt=)
    behaviour: accept empty string as input
    """
    cmd = simple_command(default='default')
    runner = CliRunner()
    result = runner.invoke(cmd, ['--opt='])
    expected = '\n'
    assert not result.exception
    assert result.output == expected


def test_opt_given_valid():
    """
    scenario: InteractiveOption, invoked with a valid value on the cmdline
    behaviour: accept valid value
    """
    cmd = simple_command(type=int)
    runner = CliRunner()
    result = runner.invoke(cmd, ['--opt=4'])
    expected = '4\n'
    assert not result.exception
    assert result.output == expected


def test_opt_given_invalid():
    """
    scenario: InteractiveOption, invoked with a valid value on the cmdline
    behaviour: accept valid value
    """
    cmd = simple_command(type=int)
    runner = CliRunner()
    result = runner.invoke(cmd, ['--opt=foo'])
    assert result.exception
    assert 'Invalid value' in result.output


def test_non_interactive():
    """
    scenario: InteractiveOption, invoked with only --non-interactive
    behaviout: fail
    """
    cmd = simple_command()
    runner = CliRunner()
    result = runner.invoke(cmd, ['--non-interactive'])
    assert result.exception
    assert 'Usage: ' in result.output
    assert 'Missing option' in result.output


def test_non_interactive_default():
    """
    scenario: InteractiveOption, invoked with only --non-interactive
    behaviout: fail
    """
    cmd = simple_command(default='default')
    runner = CliRunner()
    result = runner.invoke(cmd, ['--non-interactive'])
    assert not result.exception
    assert result.output == 'default\n'
