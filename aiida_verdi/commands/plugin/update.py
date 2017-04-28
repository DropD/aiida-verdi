# -*- coding: utf-8 -*-
"""
cli: update the plugin cache by reloading from the online registry
"""
import click
from click_spinner import spinner as cli_spinner

def catch_url_errors(err):
    from aiida.plugins.utils import value_error_msg
    try:
        raise err
    except ValueError as e:
        raise click.ClickException(value_error_msg(e))


@click.command()
def update():
    """
    force a reload of the local registry cache
    """
    from requests import ConnectionError
    from aiida.plugins.registry import update
    from aiida.plugins.utils import connection_error_msg
    with cli_spinner():
        try:
            update(with_info=True, registry_err_handler=catch_url_errors)
        except ConnectionError as e:
            click.ClickException(connection_error_msg(e))
    click.echo('Successfully updated the local plugin registry')
