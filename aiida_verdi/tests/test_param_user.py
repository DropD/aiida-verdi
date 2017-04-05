"""
unit tests for :py:class`aiida_verdi.param_types.user.UserParam`
"""
import click
from click.testing import CliRunner

from aiida_verdi.param_types.user import UserParam


def scenario_user(convert=True, **kwargs):
    """
    scenario user: simple cmd, takes a user, displays email
    """
    @click.command()
    @click.option('--user', type=UserParam(convert=convert), **kwargs)
    def cmd(user):
        """dummy test command for UserParam"""
        if not hasattr(user, 'email'):
            click.echo(user)
            click.echo('not converted')
        else:
            click.echo(user.email)
            click.echo('converted')
        click.echo('Done')
    runner = CliRunner()
    return cmd, runner


def action(scenario, *args, **kwargs):
    cmd, runner = scenario
    cliargs = list(args) + ['--{}={}'.format(k, v) for k, v in kwargs.iteritems()]
    return runner.invoke(cmd, cliargs)


def test_missing_convert():
    """
    scenario: user, required option
    action: call without required option
    behaviour: fail with missing option msg
    """
    scenario = scenario_user(required=True)
    result = action(scenario)
    assert result.exception
    assert 'Missing option "--user"' in result.output


def test_missing_noconvert():
    """
    scenario: user, required option, non converting
    action: call without required option
    behaviour: fail with missing option msg
    """
    scenario = scenario_user(required=True, convert=False)
    result = action(scenario)
    assert result.exception
    assert 'Missing option "--user"' in result.output


def test_valid_convert():
    """
    action: call with valid user email
    behaviour: succeeds printing user email and conversion confirmation
    """
    scenario = scenario_user()
    result = action(scenario, user='aiida@localhost')
    assert not result.exception
    assert 'aiida@localhost' in result.output
    assert 'converted' in result.output


def test_valid_noconvert():
    """
    scenario: user, non converting
    action: call with valid user email
    behaviour: succeds printing user email and 'not converted'
    """
    scenario = scenario_user(convert=False)
    result = action(scenario, user='aiida@localhost')
    assert not result.exception
    assert 'aiida@localhost' in result.output
    assert 'not converted' in result.output
