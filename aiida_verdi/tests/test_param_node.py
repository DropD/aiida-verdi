#-*- coding: utf8 -*-
"""
unit tests for :py:class:`aiida_verdi.param_types.node.NodeParam`
"""
import click
from click.testing import CliRunner

from aiida_verdi.param_types.node import NodeParam


def scenario_node(convert=True, **kwargs):
    """
    scenario node: takes Node option, displays uuid
    """
    @click.command()
    @click.option('--node', type=NodeParam(convert=convert), **kwargs)
    def cmd(node):
        """dummy test command for NodeParam"""
        if hasattr(node, 'uuid'):
            click.echo(node.uuid)
            click.echo('converted')
        else:
            click.echo(node)
            click.echo('not converted')
        click.echo('Done')
    runner = CliRunner()
    return cmd, runner


def action(scenario, *args, **kwargs):
    cmd, runner = scenario
    cliargs = list(args) + ['--{}={}'.format(k, v) for k, v in kwargs.iteritems()]
    return runner.invoke(cmd, cliargs)


def test_missing_convert():
    """
    scenario: node required
    action: call without node
    behaviour: fail with missing option msg
    """
    scenario = scenario_node(required=True)
    result = action(scenario)
    assert result.exception
    assert 'Missing option "--node"' in result.output


def test_missing_nonconvert():
    """
    scenario: node required, non converting
    action: call without node
    behaviour fail with missing option msg
    """
    scenario = scenario_node(required=True, convert=False)
    result = action(scenario)
    assert result.exception
    assert 'Missing option "--node"' in result.output


def get_valid_compl_item():
    from aiida.orm import load_node
    from aiida.orm import Node
    nodelist = [i for i in NodeParam().complete() if isinstance(load_node(int(i[0])), Node)]
    if nodelist:
        return nodelist[0]
    else:
        return None


def get_invalid_pk():
    from aiida.orm import load_node
    from aiida.orm import Node
    pklist = [int(i[0]) for i in NodeParam().complete() if isinstance(load_node(int(i[0])), Node)]
    if pklist:
        invalid = int(pklist[-1]) + 1
    else:
        '''guess 100 to guard against computers'''
        invalid = 100
    while invalid in pklist:
        invalid += 1
    return invalid


def test_valid_convert():
    """
    action: call with valid node pk
    behaviour: succeeds printing uuid and 'converted'
    """
    scenario = scenario_node()
    item = get_valid_compl_item()
    if item:
        pk = item[0]
        result = action(scenario, node=pk)
        assert not result.exception
        assert result.output.split('\n')[0] in item[1]
        assert 'converted' in result.output

def test_valid_nonconvert():
    """
    action: call with valid node pk
    behaviour: succeeds printing uuid and 'not converted'
    """
    scenario = scenario_node(convert=False)
    item = get_valid_compl_item()
    if item:
        result = action(scenario, node=item[0])
        assert not result.exception
        assert result.output.split('\n')[0] in item[1]
        assert 'not converted' in result.output


def test_invalid_convert():
    """
    action: call with invalid node pk
    behaviour: exits with invalid param msg
    """
    scenario = scenario_node()
    invalid = get_invalid_pk()
    result = action(scenario, node=invalid)
    assert result.exception
    assert 'Invalid value for "--node"' in  result.output


def test_non_pk_arg():
    """
    action: call with pk < 1
    behaviour: exits with invalid param msg
    """
    scenario = scenario_node()
    result = action(scenario, node=0)
    assert result.exception
    assert 'Invalid value for "--node"' in  result.output
