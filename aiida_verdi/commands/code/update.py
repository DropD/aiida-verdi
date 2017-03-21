# -*- coding: utf-8 -*-
"""
verdi code update
"""
import click

from aiida_verdi import arguments, options
from aiida_verdi.param_types.code import CodeNameParam
from aiida_verdi.param_types.plugin import PluginParam
from aiida_verdi.utils.interactive import InteractiveOption, opt_prompter


def modification_comment(code):
    from datetime import datetime
    cmt = [
        'Code modified on {}'.format(datetime.now()),
        'Old configuration was:',
        'label: {}'.format(code.label),
        'description: {}'.format(code.description),
        'input_plugin_name: {}'.format(code.get_input_plugin_name()),
        'is_local: {}'.format(code.is_local())
    ]
    if code.is_local():
        cmt.append('local_executable: {}'.format(code.get_local_executable()))
    else:
        cmt.extend([
            'computer: {}'.format(code.get_computer()),
            'remote_exec_path: {}'.format(code.get_remote_exec_path())
        ])
    cmt.extend([
        'prepend_text: {}'.format(code.get_prepend_text()),
        'append_text: {}'.format(code.get_append_text())
    ])
    return '\n'.join(cmt)

# ~
# ~ def opt_prompt(ctx, params, opt, prompt, default):
    # ~ optobj = params[opt]
    # ~ optobj._prompt = prompt
    # ~ optobj.default = default
    # ~ return optobj.prompt_loop(ctx, optobj, None)
# ~

@click.command()
@click.pass_context
@arguments.code()
@options.label(type=CodeNameParam(), help='The new name for CODE', cls=InteractiveOption)
@options.description(help='The new description for CODE', cls=InteractiveOption)
@options.input_plugin(help='The new input plugin for CODE', cls=InteractiveOption)
@options.remote_abs_path(help='Change the remote executable path (CAUTION)', cls=InteractiveOption)
@options.prepend_text()
@options.append_text()
@options.dry_run()
@options.non_interactive()
def update(ctx, code, dry_run, non_interactive, **kwargs):
    """
    Update CODE, change the information stored for it.

    Use cautiously, if CODE has been used for calculations
    """
    # ~ label = kwargs['label']
    # ~ desc = kwargs['description']
    # ~ calc = kwargs['input_plugin']
    # ~ prescr = kwargs['append_text']
    # ~ postscr = kwargs['prepend_text']
    # ~ remabs = kwargs['remote_abs_path']
    mod_cmt = modification_comment(code)

    '''if interactive, prompt for missing values'''
    if not non_interactive:
        if dry_run:
            click.echo('This is a dry run, no changes will be committed')

        if code.has_children:
            click.echo("***********************************")
            click.echo("|                                 |")
            click.echo("|            WARNING!             |")
            click.echo("| Consider to create another code |")
            click.echo("| You risk of losing the history  |")
            click.echo("|                                 |")
            click.echo("***********************************")

        '''interactively prompt for the missing options'''
        opt_prompt = opt_prompter(ctx, update, kwargs)
        kwargs['label'] = opt_prompt('label', 'Label', code.label)
        kwargs['description'] = opt_prompt('description', 'Description', code.description)
        kwargs['input_plugin'] = opt_prompt('input_plugin', 'Input plugin', code.get_input_plugin_name())
        if not code.is_local():
            '''computer cannot be changed but remote executable path can'''
            old = code.get_remote_exec_path()
            kwargs['remote_abs_path'] = opt_prompt('remote_abs_path', 'Remote path', old)
            if not kwargs['remote_abs_path'] == old:
                '''make sure the user understands this should not be
                used to change the executable, only it's location'''
                if not click.confirm('Is it the same executable, just in a different path?'):
                    kwargs['remote_abs_path'] = None
                    click.echo('***********')
                    click.echo('| WARNING |')
                    click.echo('***********')
                    click.echo('Changing the executable itself would break provenance!')
                    click.echo('Not changing remote path')
                    click.echo('Create a new code instead!')
        '''local code's folder and relative path cannot be changed'''
        if (not kwargs['prepend_text']) or (not kwargs['append_text']):
            '''use editor to change pre and post execution scripts'''
            from aiida_verdi.utils.mlinput import edit_pre_post
            pre = kwargs['prepend_text'] or ''
            post = kwargs['append_text'] or ''
            kwargs['prepend_text'], kwargs['append_text'] = edit_pre_post(pre, post, kwargs)

    '''summarize the changes'''
    if kwargs['label']:
        click.echo('Label: {} -> {}'.format(code.label, kwargs['label']))
    if kwargs['description']:
        click.echo('Description: {} -> {}'.format(code.description, kwargs['description']))
    if kwargs['input_plugin']:
        click.echo('Input plugin: {} -> {}'.format(code.get_input_plugin_name(), kwargs['input_plugin']))
    if kwargs['prepend_text']:
        click.echo('Prepend text:\n{}\n->\n{}'.format(code.get_prepend_text(), kwargs['prepend_text']))
    if kwargs['append_text']:
        click.echo('Append text:\n{}\n->\n{}'.format(code.get_append_text(), kwargs['append_text']))

    '''update the code attributes'''
    if not dry_run:
        code.label = kwargs['label'] or code.label
        code.description = kwargs['description'] or code.description
        code.set_input_plugin_name(kwargs['input_plugin']) or code.get_input_plugin_name()
        code.set_prepend_text(kwargs['prepend_text']) or code.get_prepend_text()
        code.set_append_text(kwargs['append_text']) or code.get_append_text()

        if kwargs['remote_abs_path']:
            from aiida.backends.djsite.db.models import DbAttribute
            DbAttribute.set_value_for_node(code.dbnode, 'remote_exec_path', kwargs['remote_abs_path'])

        '''add modification comment'''
        code.add_comment(mod_cmt, user=get_automatic_user())
    else:
        click.echo('Code not modified (--dry-run recieved)')
