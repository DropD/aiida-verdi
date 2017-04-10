# -*- coding: utf-8 -*-
"""
tests for comment remove
"""
from aiida_verdi.tests.utils.action import general_action
from aiida_verdi.tests.test_param_node import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    """call comment remove with args & opts"""
    from aiida_verdi.commands.comment import comment
    return general_action(comment, 'remove', *args, **kwargs)


def test_remove_help():
    """
    action: comment remove --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output


def test_remove_noargs():
    """
    action: comment remove
    behaviour: exit with missing help msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument "node"' in result.output


def test_remove_validarg():
    """
    action: comment remove <valid node> --dry-run --non-interactive
    behaviour: noop
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', '--non-interactive')
        assert not result.exception
        assert not result.output


def test_remove_invalidarg():
    """
    action: comment remove <invalid node> --dry-run --non-interactive
    behaviour: exit with invalid arg msg
    """
    result = action(str(get_invalid_pk()), '--dry-run', '--non-interactive')
    assert result.exception
    assert 'Invalid value for "node"' in result.output


def test_remove_validarg_withcmt_force():
    """
    action: comment remove <valid node> <comment> --dry-run --force
    behaviour: exit with dry-run msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '1', '--dry-run', '--force')
        assert not result.exception
        assert '--dry-run recieved' in result.output
