#-*- coding: utf-8 -*-
"""
cli: search online plugin registry
"""
import click
from click_spinner import spinner as cli_spinner


@click.command()
@click.argument('pattern', default='.*')
@click.option('--relevance', is_flag=True, default=False)
def search(pattern, relevance):
    """
    search online registry for plugins
    """
    import re
    from aiida.plugins.info import find_by_pattern
    with cli_spinner():
        pat = re.compile(pattern)
        res = find_by_pattern(pat, ranking=relevance)
    page = 'Found the following plugins:'
    page += '\n\t'
    page += '\n\t'.join([i.entry_point for i in res])
    click.echo(page)

