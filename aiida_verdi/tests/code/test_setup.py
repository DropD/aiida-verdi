#-*- coding: utf8 -*-
"""
tests for verdi code setup
"""
import click
from click.testing import CliRunner


def test_code_setup_help():
    """
    action: verdi code setup --help
    behaviour: print help message
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['setup', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert '--label' in result.output
    assert '--description' in result.output
    assert '--installed / --upload' in result.output
    assert '--input-plugin' in result.output
    assert '--code' in result.output
    assert '--remote-abs-path' in result.output
    assert '--code-folder' in result.output
    assert '--code-rel-path' in result.output
    assert '--append-text' in result.output
    assert '--prepend-text' in result.output
# ~
# ~
# ~ def test_installed_non_interactive_dry():
    # ~ from aiida_verdi.commands.code import code
    # ~ runner = CliRunner()
    # ~ result = runner.invoke(
        # ~ code,
        # ~ ['setup', '--dry-run', '--non-interactive',
         # ~ '-L Label', '-D Description', '--installed',
         # ~ '--input-plugin=plugin', '--computer=Computer',
         # ~ '--remote-abs-path=/bin', '--prepend-text=',
         # ~ '--append-text='],
        # ~ resilient_parsing=True
    # ~ )
    # ~ assert not result.exception
    # ~ assert result.output == ''


def test_code_setup_ni():
    """
    action: verdi code setup --non-interactive
    behaviour: fail without prompting
    """
    from aiida_verdi.commands.code import code
    runner = CliRunner()
    result = runner.invoke(code, ['setup', '--non-interactive'])
    assert result.exception
    assert 'Missing option' in result.output
