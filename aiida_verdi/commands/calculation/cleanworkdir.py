# -*- coding: utf-8 -*-
"""
verdi calculation cleanworkdir
"""
import click

from aiida_verdi import options
from aiida_verdi.param_types.jobcalc import JobCalcParam
from aiida_verdi.param_types.computer import ComputerParam


@click.command()
@options.calculation(multiple=True, type=JobCalcParam(convert=False, pass_pk=True), help='[can be given multiple times] PK or UUID of calculation(s) to clean the workdir of')
@options.force(help='Force the cleaning (no prompt)')
@options.past_days(help="Add a filter to clean workdir of calculations modified during the past N days")
@click.option("-o", "--older-than", type=int, metavar="N", help="Add a filter to clean workdir of calculations that have been modified on a date before N days ago")
@options.computer(multiple=True, type=ComputerParam(convert=False, pass_pk=True), help='[can be given multiple times] name(s) of computer(s) to filter for')
@options.dry_run(help='Leave all files and directories untouched')
@options.non_interactive()
def cleanworkdir(dry_run, non_interactive, **kwargs):
    """
    Clean work directory (i.e. remote folder) of AiiDA calculations.


    At least one --calc or either of --past-days, --older-than must be specified (but never both).
    Pass multiple --calc options for a list of calculations to clean
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()

    from aiida.backends.utils import get_automatic_user
    from aiida.backends.utils import get_authinfo
    from aiida.common.utils import query_yes_no
    from aiida.orm.computer import Computer as OrmComputer
    from aiida.orm.user import User as OrmUser
    from aiida.orm.calculation import Calculation as OrmCalculation
    from aiida.orm.querybuilder import QueryBuilder
    from aiida.utils import timezone
    import datetime

    if kwargs['calc']:
        if kwargs['past_days'] or kwargs['older_than']:
            raise click.BadOptionUsage("You cannot specify both a list of --c options pks and the -p or -o options")
    else:
        if not kwargs['past_days'] and not kwargs['older_than']:
            raise click.BadOptionUsage("You should specify at least a list of --calc options or the -p, -o options")

    if kwargs['past_days'] and kwargs['older_than']:
        raise click.BadOptionUsage("Not both of the -p, -o options can be specified in the same time")

    qb_user_filters = dict()
    user = OrmUser(dbuser=get_automatic_user())
    qb_user_filters["email"] = user.email

    qb_computer_filters = dict()
    if kwargs['computer']:
        kwargs['computer'] = [str(i) for i in kwargs['computer']]
        qb_computer_filters["name"] = {"in": kwargs['computer']}

    qb_calc_filters = dict()
    if kwargs['past_days']:
        pd_ts = timezone.now() - datetime.timedelta(
            days=kwargs['past_days'])
        qb_calc_filters["mtime"] = {">": pd_ts}
    if kwargs['older_than']:
        ot_ts = timezone.now() - datetime.timedelta(
            days=kwargs['older_than'])
        qb_calc_filters["mtime"] = {"<": ot_ts}
    if kwargs['calc']:
        click.echo("--calc: {}".format(kwargs['calc']))
        qb_calc_filters["id"] = {"in": [str(i) for i in kwargs['calc']]}

    qb = QueryBuilder()
    qb.append(OrmCalculation, tag="calc",
                filters=qb_calc_filters,
                project=["id", "uuid", "attributes.remote_workdir"])
    qb.append(OrmComputer, computer_of="calc",
                project=["*"],
                filters=qb_computer_filters)
    qb.append(OrmUser, creator_of="calc",
                project=["*"],
                filters=qb_user_filters)

    no_of_calcs = qb.count()
    if no_of_calcs == 0:
        click.echo("No calculations found with the given criteria.")
        return 0

    click.echo("Found {} calculations with the given criteria.".format(no_of_calcs))

    if not kwargs['force']:
        if non_interactive:
            click.echo('Aborting (--force not given)...')
            return 0
        click.confirm("Are you sure you want to clean the work directory?", abort=True)

    # get the uuids of all calculations matching the filters
    calc_list_data = qb.dict()

    # get all computers associated to the calc uuids above, and load them
    # we group them by uuid to avoid computer duplicates
    comp_uuid_to_computers = {_["computer_1"]["*"].uuid: _["computer_1"]["*"] for _ in calc_list_data}

    # now build a dictionary with the info of folders to delete
    remotes = {}
    for computer in comp_uuid_to_computers.values():
        # initialize a key of info for a given computer
        remotes[computer.name] = {'transport': get_authinfo(
            computer=computer, aiidauser=user._dbuser).get_transport(),
                                    'computer': computer,
        }

        # select the calc pks done on this computer
        this_calc_pks = [_["calc"]["id"] for _ in calc_list_data
                            if _["computer_1"]["*"].id == computer.id]

        this_calc_uuids = [unicode(_["calc"]["uuid"])
                            for _ in calc_list_data
                            if _["computer_1"]["*"].id == computer.id]

        remote_workdirs = [_["calc"]["attributes.remote_workdir"]
                            for _ in calc_list_data
                            if _["calc"]["id"] in this_calc_pks
                            if _["calc"]["attributes.remote_workdir"]
                            is not None]

        remotes[computer.name]['remotes'] = remote_workdirs
        remotes[computer.name]['uuids'] = this_calc_uuids

    # now proceed to cleaning
    for computer, dic in remotes.iteritems():
        click.echo("Cleaning the work directory on computer {}.".format(computer))
        counter = 0
        t = dic['transport']
        with t:
            remote_user = remote_user = t.whoami()
            aiida_workdir = dic['computer'].get_workdir().format(
                username=remote_user)

            t.chdir(aiida_workdir)
            # Hardcoding the sharding equal to 3 parts!
            existing_folders = t.glob('*/*/*')

            folders_to_delete = [i for i in existing_folders if
                                    i.replace("/", "") in dic['uuids']]

            for folder in folders_to_delete:
                if not dry_run:
                    t.rmtree(folder)
                counter += 1
                if counter % 20 == 0 and counter > 0:
                    if not dry_run:
                        click.echo("Deleted work directories: {}".format(counter))
                    else:
                        click.echo('Work directories not deleted: {}'.format(counter))

        if not dry_run:
            click.echo("{} remote folder(s) cleaned.".format(counter))
        else:
            click.echo("{} remote folder(s) not cleaned (--dry-run recieved).".format(counter))
