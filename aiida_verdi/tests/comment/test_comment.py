# -*- coding: utf-8 -*-
"""
tests for verdi comment
"""
import click
from click.testing import CliRunner

from aiida_verdi.tests.utils.action import general_action


def action(*args, **kwargs):
    """
    call comment without subcommand
    """
    from aiida_verdi.commands.comment import comment
    return general_action(comment, *args, **kwargs)



def test_comment_help():
    """
    action: verdi comment --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output
