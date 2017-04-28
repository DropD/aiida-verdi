# -*- coding: utf-8 -*-
"""
verdi quicksetup tests
"""
import click
from click.testing import CliRunner


def test_qs_help():
    """
    action: verdi quicksetup --help
    behaviour: exit with help msg
    """
    from aiida_verdi.commands.quicksetup import quicksetup
    runner = CliRunner()
    result = runner.invoke(quicksetup, ['--help'])
    assert not result.exception
    assert 'Usage:' in result.output


def test_qs_dry_run():
    """
    action: verdi quicksetup --dry-run --non-interactive ...
    behaviour: print info but do not create profile
    """
    from aiida_verdi.commands.quicksetup import quicksetup
    runner = CliRunner()
    args = [
        '--dry-run',
        '--non-interactive',
        '--profile=qs_dry_run',
        '--first-name=Test',
        '--last-name=Testerson',
        '--email=test@test.test',
        '--institution=TUT',
        '--db-host=localhost',
        '--db-port=5432',
        '--db-name=test_qs_dry_run',
        '--db-user=test_qs',
        '--repo=~/test-repo',
        '--backend=sqlalchemy',
        '--make-default=True',
        '--make-daemon=False'
    ]
    result = runner.invoke(quicksetup, args)
    assert not result.exception
    assert result.output.count('(--dry-run recieved)') > 1
