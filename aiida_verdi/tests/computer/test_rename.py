# -*- coding: utf-8 -*-
"""
tests for verdi computer rename
"""
from click.testing import CliRunner


def test_rename():
    from aiida_verdi.commands.computer import computer
    """
    action: verdi computer rename --help
    behaviour: print help message
    """
    runner = CliRunner()
    result = runner.invoke(computer, [])
    assert not result.exception
    assert 'Usage' in result.output
