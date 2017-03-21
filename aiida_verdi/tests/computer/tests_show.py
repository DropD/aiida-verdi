# -*- coding: utf8 -*-
import click
from click.testing import CliRunner


def test_show_help():
    """
    action: verdi computer show --help
    behaviour: print help message
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['show', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert 'COMPUTER' in result.output
