# -*- coding: utf-8 -*-
"""
convenience utility to save a few lines for each test
"""
import click
from click.testing import CliRunner

def general_action(cmd, *args, **kwargs):
    input_ = kwargs.pop('input', None)
    runner = CliRunner()
    cliargs = list(args) + ['--{}={}'.format(k.replace('_', '-'), v) for k, v in kwargs.iteritems()]
    return runner.invoke(cmd, cliargs, input=input_)
