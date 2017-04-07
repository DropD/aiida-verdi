# -*- coding: utf-8 -*-
"""
tests for comment update
"""
from aiida_verdi.tests.utils.action import general_action
from aiida_verdi.tests.test_param_node import get_valid_compl_item, get_invalid_pk


def action(*args, **kwargs):
    """call comment update with args & opts"""
    from aiida_verdi.commands.comment import comment
    return general_action(comment, 'update', *args, **kwargs)


def test_update_help():
    """
    action: comment update --help
    behaviour: exit with help msg
    """
    result = action('--help')
    assert not result.exception
    assert 'Usage' in result.output


def test_update_noargs():
    """
    action: comment update
    behaviour: exit with missing help msg
    """
    result = action()
    assert result.exception
    assert 'Missing argument "node"' in result.output


def test_update_validnode():
    """
    action: comment update <valid node> --dry-run --non-interactive
    behaviour: exit with missing arg msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], '--dry-run', '--non-interactive')
        assert result.exception
        assert 'Missing argument "comment_id"' in result.output


def test_update_invalidarg():
    """
    action: comment update <invalid node> --dry-run --non-interactive
    behaviour: exit with invalid arg msg
    """
    result = action(str(get_invalid_pk()), '--dry-run', '--non-interactive')
    assert result.exception
    assert 'Invalid value for "node"' in result.output


def test_update_validarg_withcmt():
    """
    action: comment update <valid node> 1 --dry-run --non-interactive
    behaviour: noop
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], 1, '--dry-run', '--non-interactive')
        if result.exception:
            assert 'has no comment 1' in result.output
        else:
            assert not result.output


def test_update_validarg_withcmt_content():
    """
    action: comment update <valid node> --comment comment --dry-run --non-interactive
    behaviour: exit with dry-run msg
    """
    item = get_valid_compl_item()
    if item:
        result = action(item[0], 1, '--dry-run', '--non-interactive', comment='comment')
        assert not result.exception
        assert '--dry-run recieved' in result.output
