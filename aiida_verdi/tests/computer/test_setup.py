# -*- coding: utf8 -*-
"""
tests for verdi computer setup
"""
import click
from click.testing import CliRunner


def test_computer_setup_help():
    """
    action: verdi computer setup --help
    behaviour: display help message
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['setup', '--help'])
    assert not result.exception
    assert 'Usage' in result.output
    assert '--label' in result.output
    assert '--description' in result.output
    assert '--enabled / --disabled' in result.output
    assert '--transport' in result.output
    assert '--scheduler' in result.output
    assert '--workdir' in result.output
    assert '--mpirun' in result.output
    assert '--ppm' in result.output
    assert '--prepend-text' in result.output
    assert '--append-text' in result.output
    assert '--non-interactive' in result.output
    assert '--dry-run' in result.output


def test_computer_setup_ni():
    """
    action: verdi computer setup --non-interactive --dry-run
    behaviour: fail without prompting
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, ['setup', '--non-interactive', '--dry-run'])
    assert result.exception
    assert 'Missing option' in result.output


def test_full_dry_run():
    """
    action: verdi computer setup --non-interactive --dry-run <all possible options>
    behaviour: complete dry run
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, [
        'setup', '--non-interactive', '--dry-run', '-L aiida_verdi/tests/computer/test_ful_dry_run',
        '-D "A nonexistent test computer"', '--hostname=testssh',
        '--transport=ssh', '--scheduler=torque', '--workdir=/scratch/work',
        '--mpirun=mpirun', '--ppm=12', '--enabled'
    ])
    assert not result.exception
    assert '--dry-run recieved' in result.output or 'recieved --dry-run' in result.output


def test_ni_missing_enable():
    """
    action: verdi computer setup --non-interactive --dry-run <all possible opts except --enabled>
    behaviour: works, uses default value
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, [
        'setup', '--non-interactive', '--dry-run', '-L aiida_verdi/tests/computer/test_ful_dry_run',
        '-D "A nonexistent test computer"', '--hostname=testssh',
        '--transport=ssh', '--scheduler=torque', '--workdir=/scratch/work',
        '--mpirun=mpirun', '--ppm=12'
    ])
    assert not result.exception


def test_ni_missing_ppm():
    """
    action: verdi computer setup --non-interactive --dry-run <all opts but leave off --ppm>
    behaviour: fail if scheduler accepts ppm value, succeed otherwise
    """
    from aiida_verdi.commands.computer import computer
    runner = CliRunner()
    result = runner.invoke(computer, [
        'setup', '--non-interactive', '--dry-run', '-L aiida_verdi/tests/computer/test_ful_dry_run',
        '-D "A nonexistent test computer"', '--hostname=testssh',
        '--transport=ssh', '--scheduler=lsf', '--workdir=/scratch/work',
        '--mpirun=mpirun'
    ])
    assert not result.exception

    result = runner.invoke(computer, [
        'setup', '--non-interactive', '--dry-run', '-L aiida_verdi/tests/computer/test_ful_dry_run',
        '-D "A nonexistent test computer"', '--hostname=testssh',
        '--transport=ssh', '--scheduler=torque', '--workdir=/scratch/work',
        '--mpirun=mpirun'
    ])
    assert result.exception
