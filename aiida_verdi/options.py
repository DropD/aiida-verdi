#-*- coding: utf8 -*-
"""
standard options for consistency throughout the verdi commandline
"""
import click

from aiida.backends.profile import (BACKEND_DJANGO, BACKEND_SQLA)


class overridable_option(object):
    """
    wrapper around click option that allows to store the name
    and some defaults but also to override them later, for example
    to change the help message for a certain command.
    """
    def __init__(self, *args, **kwargs):
        """
        store the defaults.
        """
        self.args = args
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        """
        override kwargs (no name changes) and return option
        """
        kwargs.update(self.kwargs)
        return click.option(*self.args, **kwargs)


backend = overridable_option('--backend', type=click.Choice([BACKEND_DJANGO, BACKEND_SQLA],),
                             help='backend choice')
email = overridable_option('--email', metavar='EMAIL', type=str, help='valid email address for the user')
db_host = overridable_option('--db_host', metavar='HOSTNAME', type=str, help='database hostname')
db_port = overridable_option('--db_port', metavar='PORT', type=int, help='database port')
db_name = overridable_option('--db_name', metavar='DBNAME', type=str, help='database name')
db_user = overridable_option('--db_user', metavar='DBUSER', type=str, help='database username')
db_pass = overridable_option('--db_pass', metavar='DBPASS', type=str, help='password for username to access the database')
first_name = overridable_option('--first-name', metavar='FIRST', type=str, help='your first name')
last_name = overridable_option('--last-name', metavar='LAST', type=str, help='your last name')
institution = overridable_option('--institution', metavar='INSTITUTION', type=str, help='your institution')
repo = overridable_option('--repo', metavar='PATH', type=click.Path(), help='data file repository')
non_interactive = overridable_option('--non-interactive', is_flag=True, is_eager=True, help='noninteractive mode: never prompt the user for input')
dry_run = overridable_option('--dry-run', is_flag=True, is_eager=True, help='do not commit to database or modify configuration files')
debug = overridable_option('--debug', is_flag=True, is_eager=True, help='print debug information')
