# -*- coding: utf8 -*-
"""
tests for verdi computer update
"""
import click
from click.testing import CliRunner


def test_computer_update_help():
    """
    action: verdi computer update --help
    behaviour: display help message
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['update', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert '--label' in result.output
    assert '--description' in result.output
    assert '--enabled / --disabled' in result.output
    assert '--transport' in result.output
    assert '--scheduler' in result.output
    assert '--workdir' in result.output
    assert '--mpirun' in result.output
    assert '--ppm' in result.output
    assert '--prepend-text' in result.output
    assert '--append-text' in result.output
    assert '--non-interactive' in result.output
    assert '--dry-run' in result.output


def test_computer_update_ni():
    """
    action: verdi computer update --non-interactive --dry-run
    behaviour: fail without prompting
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['update', '--non-interactive', '--dry-run'])
    assert result.exception
    assert 'Missing argument' in result.output
