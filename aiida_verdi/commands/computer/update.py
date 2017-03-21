# -*- coding: utf8 -*-
"""
verdi computer update
"""
import click

from aiida_verdi import arguments, options
from aiida_verdi.utils.interactive import InteractiveOption, opt_prompter
from aiida_verdi.utils.aiidadb import comp_not_exists
from aiida_verdi.param_types.plugin import PluginParam


def has_no_calcs(ctx, param, comp):
    if comp.get_calculations_on_computer():
        raise click.BadParameter((
            'Cannot modify a computer that has been used to run calculations. '
            'Disable this computer and set up a new one instead!'), param=param)
    else:
        return comp

def confirmation_warning(computer, maxlen=75):
    from textwrap import wrap
    ruler = '*' * maxlen
    warning = "WARNING! Modifying existing computer with name '{}'. ".format(computer.name)
    warning += "Are you sure you want to continue? The UUID will remain the same! "
    warning += "Continue only if you know what you are doing. "
    warning += "If you just want to rename a computer, use the 'verdi computer rename' "
    warning += "command. In most cases, it is better to create a new computer. "
    warning += "Moreover, if you change the transport, you must also reconfigure "
    warning += "each computer for each user! "
    warning = wrap(warning, maxlen)
    warning.insert(0, ruler)
    warning.append(ruler)
    warning = '\n'.join(warning) + '\n'
    return warning


@click.command()
@arguments.computer(callback=has_no_calcs)
@options.label(cls=InteractiveOption, callback=comp_not_exists, help='The name for this Computer')
@options.description(cls=InteractiveOption)
@click.option('--hostname', cls=InteractiveOption, help='The fully qualified host name of this computer')
@click.option('--enabled/--disabled', default=True, help=('if disabled, calculations associated with this computer' 'will not be submitted'))
@click.option('--transport', cls=InteractiveOption, type=PluginParam(category='transports'), help='Transport to be used')
@click.option('--scheduler', cls=InteractiveOption, type=PluginParam(category='schedulers'), help='Scheduler to be used')
@click.option('--workdir', cls=InteractiveOption, type=click.Path(), help='Absolute path on the computer. AiiDA will run all calculations under that directory (typically on the scratch file system). {username} will be replaced by your username on the remote computer')
@click.option('--mpirun', cls=InteractiveOption, help='The mpirun command to be used on the computer to run MPI programs. {tot_num_mpiprocs} will be replaced by the total number of cpus. See the scheduler docs for more replacement fields.')
@click.option('--ppm', '--default-mpiprocs-per-machine', 'ppm', cls=InteractiveOption, type=int, empty_ok=True, help='Default number of CPUs per machine (node) to be used if nothing else specified. Leave empty if you do not want to provide a default value')
@options.prepend_text()
@options.append_text()
@options.non_interactive()
@options.dry_run()
@click.pass_ctx
def update(ctx, computer, dry_run, non_interactive, **kwargs):
    """
    Update (change) an AiiDA computer that has not yet been used
    """
    if not non_interactive:
        if not click.confirm(confirmation_warning(computer)):
            return 0

        '''interactively prompt for missing options'''
        opt_prompt = opt_prompter(ctx, update, kwargs)
        kwargs['label'] = opt_prompt('label', 'Label', computer.label)
        kwargs['description'] = opt_prompt('description', 'Description', computer.description)
        kwargs['hostname'] = opt_prompt('hostname', 'Fully qualified hostname', computer.hostname)
        kwargs['enabled'] = opt_prompt('enabled', 'Enabled', computer.is_enabled())
        kwargs['transport'] = opt_prompt('transport', 'Transport type', computer.get_transport_type())
        kwargs['scheduler'] = opt_prompt('scheduler', 'Scheduler type', computer.get_scheduler_type())
        kwargs['workdir'] = opt_prompt('workdir', 'AiiDA work directory', computer.get_workdir())
        kwargs['mpirun'] = opt_prompt('mpirun', 'mpirun command', computer.get_mpirun_command())
        kwargs['ppm'] = opt_prompt('ppm', 'Default number of CPUs per machine', computer.get_default_mpiprocs_per_machine())
        pre = kwargs['prepend_text'] or ''
        post = kwargs['append_text'] or ''
        if (not pre) or (not post):
            '''let the user edit the pre and post execution scripts'''
            from aiida_verdi.utils.mlinput import edit_pre_post
            pre = pre or computer.get_prepend_text()
            post = post or computer.get_append_text()
            pre, post = edit_pre_post(pre, post, kwargs)
            kwargs['prepend_text'] = pre
            kwargs['append_text'] = post

    '''summarize the changes'''


    if not dry_run:
        computer.set_name(kwargs['label'])
        computer.set_description(kwargs['description'])
        computer.set_hostname(kwargs['hostname'])

