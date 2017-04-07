# -*- coding: utf-8 -*-
"""
tests for comment show
"""
import click

from aiida_verdi.tests.utils.action import general_action
from aiida_verdi.tests.test_param_node import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    from aiida_verdi.commands.comment import comment
    return general_action(comment, 'show', *args, **kwargs)


def test_show_help():
    """
    action: comment show --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output


def test_show_noargs():
    """
    action: comment show
    behaviour: exit with missing help msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument "node"' in result.output


def test_show_validarg():
    """
    action: comment show <valid node>
    behaviour: output comments
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0])
        assert not result.exception
        assert result.output


def test_show_invalidarg():
    """
    action: comment show <invalid node> --dry-run --non-interactive
    behaviour: exit with invalid arg msg
    """
    result = action(str(get_invalid_pk()), '--dry-run', '--non-interactive')
    assert result.exception
    assert 'Invalid value for "node"' in result.output


def test_show_validarg_withcmt():
    """
    action: comment show <valid node> 1
    behaviour: exit with dry-run msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '1')
        assert not result.exception
        found = 'ID: 1' in result.output
        notfound = 'No comment found' in result.output
        assert found or notfound
