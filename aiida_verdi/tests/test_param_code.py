#-*- coding: utf8 -*-
"""
unittests for CodeParameter
"""
import click
from click.testing import CliRunner

from aiida_verdi.param_types.code import CodeParam


def test_complete():
    """
    scenario: given a CodeParam instance
    action: call complete on it with no context
    behaviour: return [(code, help), [...]]
    """
    _code = CodeParam()
    comps = _code.complete(None, '')
    assert isinstance(comps, list)
    if comps:
        assert isinstance(comps[0], tuple)


def setup_code_option_cmd(**kwargs):
    """
    sets up a simple cmd with a code option and runner
    """
    @click.command()
    @click.option('--code', type=CodeParam(), **kwargs)
    def cmd(code):
        """simple test command for CodeParam"""
        click.echo(str(code.__class__.__name__))
    runner = CliRunner()
    return cmd, runner


def test_conversion():
    """
    scenario: code parameter
    action: give valid code
    behaviour: cmd gets a Code object
    """
    cmd, runner = setup_code_option_cmd()
    codes = CodeParam().complete(None, '')
    codename = ''
    if codes:
        codename = codes[0][0]
    result = runner.invoke(cmd, ['--code={}'.format(codename)])

    if codename:
        assert not result.exception
        assert result.output == 'Code\n'
    else:
        assert result.exception


def test_missing():
    """
    scenario: required code parameter
    action: call without value
    behaviour: print missing message with suggestions
    """
    cmd, runner = setup_code_option_cmd(required=True)
    result = runner.invoke(cmd, [])
    assert result.exception
    assert 'Possible arguments are:' in result.output
