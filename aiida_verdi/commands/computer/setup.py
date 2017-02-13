#-*- coding: utf8 -*-
"""
verdi computer setup command
"""
import click

from aiida_verdi.verdic_utils import load_dbenv_if_not_loaded
from aiida_verdi import options
from aiida_verdi.utils.interactive import InteractiveOption
from aiida_verdi.utils.aiida import get_computer


def comp_not_exists(value, param, ctx):
    from aiida.common.exceptions import NotExistent
    try:
        get_computer(name=value)
        msg = '{} exists.'
        msg += 'Use verdi computer update to modify existing computers'
        sys.exit(msg)
    except NotExistent:
        return value


@click.command()
@options.label(prompt='Label', cls=InteractiveOption, callback=comp_not_exists, help='The name for this Computer')
@options.description(prompt='Description', cls=InteractiveOption)
@click.option('--hostname', prompt='Fully-qualified hostname', cls=InteractiveOption, help='The fully qualified host name of this computer')
@click.option('--enabled/--disabled', default=True, prompt='Enabled', help=('if disabled, calculations associated with this computer' 'will not be submitted'))
@click.option('--transport', prompt='Transport type', cls=InteractiveOption, type=PluginParam(category='transport'), help='Transport to be used')
@click.option('--scheduler', prompt='Scheduler type', cls=InteractiveOption, type=PluginParam(category='scheduler'), help='Scheduler to be used')
@click.option('--workdir', prompt='AiiDA work directory', cls=InteractiveOption, type=click.Path(), help='Absolute path on the computer. AiiDA will run all calculations under that directory (typically on the scratch file system). {username} will be replaced by your username on the remote computer')
@click.option('--mpirun', prompt='mpirun command', cls=InteractiveOption, help='The mpirun command to be used on the computer to run MPI programs. {tot_num_mpiprocs} will be replaced by the total number of cpus. See the scheduler docs for more replacement fields.')
@click.option('--ppm', '--default-mpiprocs-per-machine', prompt='Default number of CPUs per machine', cls=InteractiveOption, type=int, empty_ok=True, help='Default number of CPUs per machine (node) to be used if nothing else specified. Leave empty if you do not want to provide a default value')
@options.prepend_text()
@options.append_text()
@options.non_interactive()
@options.dry_run()
def setup(label, description, enabled, transport, scheduler, workdir, mpirun, ppm, prepend_text, append_text, non_interactive, dry_run):
    """
    verdi compute
    """
    load_dbenv_if_not_loaded()
    from aiida.orm.computer import Computer

    computer = Computer(name=label)
    click.echo('Creating new computer with name "{}"'.format(label))

    if not dry_run:
        try:
            computer.store()
            click.echo('Computer "{}" successfully stored.'.format(label))
            click.ehco('pk: {}, uuid: {}'.format(computer.pk, computer.uuid))
            click.echo('Note: before using it with AiiDA, configure it using the command')
            click.echo('  verdi computer configure {}'.format(computer_name))
            click.echo('(Note: machine_dependent transport parameters cannot be set via ')
            click.echo('the command-line interface at the moment)')
        except ValidateionError as e:
            msg = 'Unable to store computer: {}. Exiting...'.format(e.message)
            sys.exit(msg)
