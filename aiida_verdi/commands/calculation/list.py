# -*- coding: utf-8 -*-
"""
verdi calculation list
"""
import click

from aiida.common.datastructures import calc_states
from aiida_verdi import options


_default_calcstates = (calc_states.WITHSCHEDULER,
               calc_states.NEW,
               calc_states.TOSUBMIT,
               calc_states.SUBMITTING,
               calc_states.COMPUTED,
               calc_states.RETRIEVING,
               calc_states.PARSING)

_projectors = ['pk', 'state', 'ctime', 'sched', 'computer',
               'type', 'description', 'label', 'uuid',
               'mtime', 'user']

_default_projectors = ('pk', 'state', 'ctime', 'sched', 'computer', 'type')


@click.command('list')
@click.option('-s', '--states', multiple=True, type=click.Choice(calc_states), default=_default_calcstates, help="[can be given multiple times] Show only the AiiDA calculations with given state(s)")
@options.past_days(help="add a filter to show only calculations created in the past N days")
@click.option('-g', '--group', '--group-name', 'group', metavar='GROUPNAME', help="add a filter to show only calculations within a given group")
@click.option('-G', '--group-pk', metavar='GROUPPK', type=int, help="add a filter to show only calculations within a given group")
@click.option('-a', '--all-states', is_flag=True, help="Overwrite manual set of states if present, and look for calculations in every possible state")
@click.option('-A', '--all-users', is_flag=True, help="Show calculations for all users, rather than only for the current user")
@click.option('-t', '--absolute-time', 'relative_ctime', is_flag=True, default=True, help="Print the absolute creation time, rather than the relative creation time")
@click.option('-l', '--limit', type=int, help='set a limit to the number of rows returned')
@click.option('-o', '--order-by', type=click.Choice(['id', 'ctime']), default='ctime', help='order the results')
@click.option('-P', '--project', 'projections', type=click.Choice(_projectors), multiple=True, default=_default_projectors, help="[can be given multiple times] Define the list of properties to show")
@click.argument('pks', metavar='PK', type=int, nargs=-1)
def list_(**kwargs):
    """
    List AiiDA calculations.

    if one or multiple PK arguments are given (ignores -p and -r options), list only these calculations.
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.orm import JobCalculation as C
    if kwargs['all_states']:
        kwargs['states'] = None
    else:
        kwargs['states'] = [i.upper for i in kwargs['states']]
    kwargs.pop('all_states')

    C._list_calculations(**kwargs)
