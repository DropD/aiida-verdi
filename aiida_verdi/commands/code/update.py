# -*- coding: utf-8 -*-
"""
verdi code update
"""
import click

from aiida_verdi.arguments import code
from aiida_verdi import options
from aiida_verdi.param_types.code import CodeNameParam
from aiida_verdi.param_types.plugin import PluginParam
from aiida_verdi.utils.interactive import InteractiveOption


def modification_comment(code_):
    from datetime import datetime
    cmt = [
        'Code modified on {}'.format(datetime.now()),
        'Old configuration was:',
        'label: {}'.format(code_.label),
        'description: {}'.format(code_.description),
        'input_plugin_name: {}'.format(code_.get_input_plugin_name()),
        'is_local: {}'.format(code_.is_local())
    ]
    if code_.is_local():
        cmt.append('local_executable: {}'.format(code.get_local_executable()))
    else:
        cmt.extend([
            'computer: {}'.format(code_.get_computer()),
            'remote_exec_path: {}'.format(code_.get_remote_exec_path())
        ])
    cmt.extend([
        'prepend_text: {}'.format(code_.get_prepend_text()),
        'append_text: {}'.format(code_.get_append_text())
    ])
    return '\n'.join(cmt)


def opt_prompt(ctx, params, opt, prompt, default):
    optobj = params[opt]
    optobj._prompt = prompt
    optobj.default = default
    return optobj.prompt_loop(ctx, optobj, None)


@click.command()
@click.pass_context
@code()
@options.label(type=CodeNameParam(), help='The new name for CODE', cls=InteractiveOption)
@options.description(help='The new description for CODE', cls=InteractiveOption)
@options.input_plugin(help='The new input plugin for CODE', cls=InteractiveOption)
@options.remote_abs_path(help='Change the remote executable path (CAUTION)', cls=InteractiveOption)
@options.prepend_text()
@options.append_text()
@options.dry_run()
@options.non_interactive()
def update(ctx, _code, dry_run, non_interactive, **kwargs):
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
    mod_cmt = modification_comment(_code)

    '''if interactive, prompt for missing values'''
    if not non_interactive:
        if dry_run:
            click.echo('This is a dry run, no changes will be committed')

        if _code.has_children:
            click.echo("***********************************")
            click.echo("|                                 |")
            click.echo("|            WARNING!             |")
            click.echo("| Consider to create another code |")
            click.echo("| You risk of losing the history  |")
            click.echo("|                                 |")
            click.echo("***********************************")

        '''interactively prompt for the missing options'''
        cliparms = {i.name: i for i in update.params}
        if not kwargs['label']:
           kwargs['label'] = opt_prompt(ctx, cliparms, 'label', 'Label', _code.label)
        if not kwargs['description']:
           kwargs['description'] = opt_prompt(ctx, cliparms, 'description', 'Description', _code.description)
        if not kwargs['input_plugin']:
            kwargs['input_plugin'] = opt_prompt(ctx, cliparms, 'input_plugin', 'Input plugin', _code.get_input_plugin_name())
        if not _code.is_local():
            '''computer cannot be changed but remote executable path can'''
            if not kwargs['remote_abs_path']:
                old = _code.get_remote_exec_path()
                kwargs['remote_abs_path'] = opt_prompt(ctx, cliparms, 'remote_abs_path', 'Remote path', old)
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
        click.echo('Label: {} -> {}'.format(_code.label, kwargs['label']))
    if kwargs['description']:
        click.echo('Description: {} -> {}'.format(_code.description, kwargs['description']))
    if kwargs['input_plugin']:
        click.echo('Input plugin: {} -> {}'.format(_code.get_input_plugin_name(), kwargs['input_plugin']))
    if kwargs['prepend_text']:
        click.echo('Prepend text:\n{}\n->\n{}'.format(_code.get_prepend_text(), kwargs['prepend_text']))
    if kwargs['append_text']:
        click.echo('Append text:\n{}\n->\n{}'.format(_code.get_append_text(), kwargs['append_text']))

    '''update the code attributes'''
    if not dry_run:
        _code.label = kwargs['label'] or _code.label
        _code.description = kwargs['description'] or _code.description
        _code.set_input_plugin_name(kwargs['input_plugin']) or _code.get_input_plugin_name()
        _code.set_prepend_text(kwargs['prepend_text']) or _code.get_prepend_text()
        _code.set_append_text(kwargs['append_text']) or _code.get_append_text()

        if kwargs['remote_abs_path']:
            from aiida.backends.djsite.db.models import DbAttribute
            DbAttribute.set_value_for_node(code.dbnode, 'remote_exec_path', kwargs['remote_abs_path'])

        '''add modification comment'''
        _code.add_comment(mod_cmt, user=get_automatic_user())
    else:
        click.echo('Code not modified (--dry-run recieved)')
