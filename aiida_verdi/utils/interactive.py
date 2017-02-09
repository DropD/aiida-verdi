#-*- coding: utf8 -*-
"""
.. module::interactive
    :synopsis: Tools and an option class for interactive parameter entry with
    additional features such as help lookup.
"""

import click

from aiida_verdi.utils.conditional import ConditionalOption


def noninteractive(ctx):
    """check context for non_interactive flag"""
    return ctx.params.get('non_interactive')


class InteractiveOption(ConditionalOption):
    """
    Intercepts certain keyword arguments to circumvent :mod:`click`'s prompting
    behaviour and define a more feature-rich one

    Usage::

        import click

        @click.command()
        @click.option('label', prompt='Label', cls=InteractiveOption)
        def foo(label):
            click.echo('Labeling with label: {}'.format(label))
    """

    def __init__(self, param_decls=None, switch=None, empty_ok=False, **kwargs):
        """
        :param param_decls: relayed to :class:`click.Option`
        :param switch: sequence of parameter names
        """
        '''intercept prompt kwarg'''
        self._prompt = kwargs.pop('prompt', None)

        '''super'''
        super(InteractiveOption, self).__init__(param_decls=param_decls, **kwargs)

        '''other kwargs'''
        self.switch = switch
        self.empty_ok = empty_ok

        '''set callback'''
        if self._prompt:
            self._after_callback = self.callback
            self.callback = self.prompt_callback

        '''set controll strings that trigger special features from the input prompt'''
        self._ctrl = {'?': self.ctrl_help}

    def get_default(self, ctx):
        """disable :mod:`click` from circumventing prompting when a default value exists"""
        return None

    def _get_default(self, ctx):
        """provides the functionality of :func:`click.Option.get_default`"""
        return super(InteractiveOption, self).get_default(ctx)

    def prompt_func(self, ctx):
        """prompt function with args set"""
        return click.prompt(self._prompt, default=self._get_default(ctx), hide_input=self.hide_input, confirmation_prompt=self.confirmation_prompt)

    def ctrl_help(self):
        """control behaviour when help is requested from the prompt"""
        click.echo(self.format_help_message())

    def format_help_message(self):
        """
        format the message to be displayed for in-prompt help.

        gives a list of possibilities for parameter types that support completion
        """
        msg = self.help or 'Expecting {}'.format(self.type.name)
        choices = getattr(self.type, 'complete', lambda x, y: [])(None, '')
        if choices:
            msg += '\n\tone of:\n'
            choice_table = ['\t\t{:<12} {}'.format(*choice) for choice in choices]
            msg += '\n'.join(choice_table)
        msg = click.style('\t' + msg, fg='green')
        return msg

    def unacceptably_empty(self, value):
        """check if the value is empty and should not be passed on to conversion"""
        result = not value and not isinstance(value, bool)
        if self.empty_ok:
            return False
        else:
            return result

    def full_process_value(self, ctx, value):
        """
        catch errors raised by ConditionalOption in order to adress them in
        the callback
        """
        try:
            value = super(InteractiveOption, self).full_process_value(ctx, value)
        except click.MissingParameter:
            pass
        return value

    def safely_convert(self, value, param, ctx):
        """
        convert without raising, instead print a message if fails

        :return: Tuple of ( success (bool), converted value )
        """
        successful = False
        try:
            value = self.type.convert(value, param, ctx)
            successful = True
        except click.BadParameter as e:
            click.echo(e.message)
        return successful, value

    def prompt_loop(self, ctx, param, value):
        """prompt until successful conversion. dispatch control sequences"""
        while 1:
            '''prompt'''
            value = self.prompt_func(ctx)
            if value in self._ctrl:
                '''dispatch'''
                self._ctrl[value]()
            elif self.unacceptably_empty(value):
                '''repeat prompting without trying to convert'''
                continue
            else:
                '''try to convert, if unsuccessful continue prompting'''
                successful, value = self.safely_convert(value, param, ctx)
                if successful:
                    return value

    def after_callback(self, ctx, param, value):
        """if a callback was registered on init, call it and return it's value"""
        if self._after_callback:
            return self._after_callback(ctx, param, value)
        else:
            return value

    def prompt_callback(self, ctx, param, value):
        """decide wether to iniciate the prompt_loop or not"""

        '''a value was given'''
        if value is not None:
            return self.after_callback(ctx, param, value)

        '''parameter is not reqired anyway'''
        if not self.is_required(ctx):
            return self.after_callback(ctx, param, value)

        '''help parameter was given'''
        if ctx.params.get('help'):
            return self.after_callback(ctx, param, value)

        '''no value was given'''
        try:
            '''try to convert None'''
            value = self.type.convert(value, param, ctx)
            '''if conversion comes up empty, make sure empty is acceptable'''
            if self.unacceptably_empty(value):
                raise click.MissingParameter(param=param)

        except Exception as e:
            '''
            no value was given but a value is required

            this needs to be Exception because generally convert does not
            check for None and is allowed to raise any exception when
            encountering it
            '''

            '''no prompting allowed'''
            if noninteractive(ctx):
                '''either get a default value and return '''
                default = self._get_default(ctx) or self.default
                if default is not None:
                    return self.type.convert(default, param, ctx)
                else:
                    '''or reraise'''
                    raise e
            '''prompting allowed'''
            value = self.prompt_loop(ctx, param, value)
        return value
