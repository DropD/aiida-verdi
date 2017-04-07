# -*- coding: utf-8 -*-
"""
tests for comment add
"""
import click

from aiida_verdi.tests.utils.action import general_action
from aiida_verdi.tests.test_param_node import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.comment import comment
    return general_action(comment, 'add', *args, **kwargs)


def test_add_help():
    """
    action: comment add --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output


def test_add_noargs():
    """
    action: comment add
    behaviour: exit with missing help msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument "node"' in result.output


def test_add_validarg():
    """
    action: comment add <valid node> --dry-run --non-interactive
    behaviour: noop
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', '--non-interactive')
        assert not result.exception
        assert not result.output


def test_add_invalidarg():
    """
    action: comment add <invalid node> --dry-run --non-interactive
    behaviour: exit with invalid arg msg
    """
    result = action(str(get_invalid_pk), '--dry-run', '--non-interactive')
    assert result.exception
    assert 'Invalid value for "node"' in result.output


def test_add_validarg_withcmt():
    """
    action: comment add <valid node> --comment comment --dry-run
    behaviour: exit with dry-run msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', comment='comment')
        assert not result.exception
        assert '--dry-run recieved' in result.output
