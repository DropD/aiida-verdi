# -*- coding: utf-8 -*-
"""
verdi daemon command group
"""
import click


@click.group()
def daemon():
    """
    Commandline interface to manage the AiiDA Daemon
    """
