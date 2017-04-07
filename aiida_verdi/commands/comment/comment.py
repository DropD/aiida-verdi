# -*- coding: utf-8 -*-
"""
verdi comment command group
"""
import click


@click.group()
def comment():
    """
    Manage general properties of nodes in the database
    """
