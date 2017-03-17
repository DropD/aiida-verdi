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


@click.command()
@click.pass_context
@code()
@options.label(type=CodeNameParam(), help='The new name for CODE', cls=InteractiveOption)
@options.description(help='The new description for CODE', cls=InteractiveOption)
@options.input_plugin(help='The new input plugin for CODE', cls=InteractiveOption)
@options.remote_abs_path(help='Change the remote executable path (CAUTION)', cls=InteractiveOption)
@options.prepend_text(callback=None)
@options.append_text(callback=None)
@options.dry_run()
@options.non_interactive()
def update(ctx, _code, **kwargs):
    """
    Update CODE, change the information stored for it.

    Use cautiously, if CODE has been used for calculations
    """
    label = kwargs['label']
    desc  = kwargs['description']
    calc  = kwargs['input_plugin']
    prescr = kwargs['append_text']
    postscr = kwargs['prepend_text']
    remabs = kwargs['remote_abs_path']
    mod_cmt = modification_comment(_code)

    '''if interactive, prompt for missing values'''
    if not kwargs['non_interactive']:
        if kwargs['dry_run']:
            click.echo('This is a dry run, no changes will be committed')

        if _code.has_children:
            click.echo("***********************************")
            click.echo("|                                 |")
            click.echo("|            WARNING!             |")
            click.echo("| Consider to create another code |")
            click.echo("| You risk of losing the history  |")
            click.echo("|                                 |")
            click.echo("***********************************")

        '''get the commands option objects to use their prompting with help'''
        cliparms = {i.name: i for i in update.params}
        if not label:
            labelpar = cliparms['label']
            labelpar._prompt = 'Label'
            labelpar.default = _code.label
            label = labelpar.prompt_loop(ctx, labelpar, None)
        if not desc:
            descpar = cliparms['description']
            descpar._prompt = 'Description'
            descpar.default = _code.description
            desc = descpar.prompt_loop(ctx, descpar, None)
        if not calc:
            calcpar = cliparms['input_plugin']
            calcpar._prompt = 'Input Plugin'
            calcpar.default = _code.get_input_plugin_name()
            calc = calcpar.prompt_loop(ctx, calcpar, None)
        if not _code.is_local():
            if not remabs:
                old = _code.get_remote_exec_path()
                remabspar = cliparms['remote_abs_path']
                remabspar._prompt = 'Remote path'
                remabspar.default = old
                remabs = remabspar.prompt_loop(ctx, remabspar, None)
                if not remabs == old:
                    if not click.confirm('Is it the same executable, just in a different path?'):
                        remabs = None
                        click.echo('***********')
                        click.echo('| WARNING |')
                        click.echo('***********')
                        click.echo('Changing the executable itself would break provenance!')
                        click.echo('Not changing remote path')
                        click.echo('Create a new code instead!')
        if not prescr:
            prepar = cliparms['prepend_text']
            prescr = options.append_callback(ctx, prepar, None)
        if not postscr:
            postpar = cliparms['append_text']
            postscr = options.append_callback(ctx, prepar, None)

    '''update the code attributes'''
    if not kwargs['dry_run']:
        _code.label = label or _code.label
        _code.description = desc or _code.description
        _code.set_input_plugin_name(calc) or _code.get_input_plugin_name()
        _code.set_prepend_text(prescr) or _code.get_prepend_text()
        _code.set_append_text(postscr) or _code.get_append_text()

        if remabs:
            from aiida.backends.djsite.db.models import DbAttribute
            DbAttribute.set_value_for_node(code.dbnode, 'remote_exec_path', remabs)

        '''add modification comment'''
        _code.add_comment(mod_cmt, user=get_automatic_user())
    else:
        click.echo('Code not modified (--dry-run recieved)')
