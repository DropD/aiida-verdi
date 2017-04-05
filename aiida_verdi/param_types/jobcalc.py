# -*- coding: utf-8 -*-
"""
JobCalculation Parameter type for arguments and options
"""
import click
from click_completion import startswith
from click_spinner import spinner as cli_spinner

from aiida_verdi.verdic_utils import aiida_dbenv


class JobCalcParam(click.ParamType):
    """
    :py:mod:`click` parameter type for JobCalculation nodes

    if convert=True, passes a JobCalculation,
    if convert=False, passes the uuid of the calculation
    """
    name = 'aiida calculation item'

    def __init__(self, convert=True, **kwargs):
        self.get_from_db = convert

    @aiida_dbenv
    def convert(self, value, param, ctx):
        """
        tries to load a JobCalculation from the given pk / uuid.

        returns the node or the uuid for convert=True / convert=False

        catches

        * empty arguments
        * no node for given pk / uuid
        * node is not a JobCalculation
        """
        from aiida.cmdline import delayed_load_node as load_node
        from aiida.orm import JobCalculation
        from aiida.common.exceptions import NotExistent

        if not value:
            raise click.BadParameter('computer parameter cannot be empty')

        try:
            '''assume is pk'''
            value = int(value)
            if value < 1:
                raise click.BadParameter("PK values start from 1")
        except ValueError:
            '''assume is uuid'''
            pass

        '''try to load a node'''
        try:
            calc = load_node(value)
        except NotExistent:
            '''no node found'''
            raise click.BadParameter("No node exists with ID={}.".format(calc.id))

        '''ensure node is JobCalculation'''
        if not isinstance(calc, JobCalculation):
            raise click.BadParameter("Node with ID={} is not a calculation; it is a {}".format(
                calc.pk, calc.__class__.__name__))

        if self.get_from_db:
            value = calc
        else:
            value = calc.uuid
        return value

    @aiida_dbenv
    def complete(self, ctx=None, incomplete=''):
        """
        list calculations (pk with uuid and description)
        """
        with cli_spinner():
            from aiida.orm.querybuilder import QueryBuilder
            from aiida.orm import JobCalculation
            qb = QueryBuilder()
            qb.append(cls=JobCalculation, project=['id', 'uuid', 'description', 'type'])
            '''init match list'''
            matching = []
            '''match against pk'''
            if not incomplete or incomplete.isdigit():
                matching = [i for i in qb.iterall() if str(i[0]).startswith(incomplete)]
                descstr = 'uuid = {calc[1]}, type = {calc[3]:<40}, {calc[2]}'
                results = [(str(i[0]), descstr.format(calc=i)) for i in matching]
            '''if no matches from pk, match against uuid'''
            if not matching:
                matching = [i for i in qb.iterall() if  str(i[1]).startswith(incomplete)]
                descstr = 'pk = {calc[0]}, type = {calc[3]:<40}, {calc[2]}'
                results = [(str(i[1]), descstr.format(calc=i)) for i in matching]
            '''take common part out of type string'''
            for m in matching:
                m[3] = m[3].replace('calculation.job.', '')
            return results

    def get_missing_message(self, param):
        """
        returns the message to be printed on :py:class:`click.MissingParameter`
        """
        comps = ['{:<12} {}'.format(*c) for c in self.complete()]
        return 'Possible arguments are:\n\n' + '\n'.join(comps)
