# -*- coding: utf-8 -*-
"""
utilities for getting multi line input from the commandline
"""
import click


def edit_pre_post(pre='', post='', summary={}):
    from aiida_verdi.utils.tpl import env
    t = env.get_template('prepost.bash.tpl')
    summary = {k: v for k, v in summary.iteritems() if v}
    content = t.render(default_pre=pre, default_post=post, summary=summary)
    mlinput = click.edit(content, extension='.bash')
    if mlinput:
        from re import findall
        regex = r'(#==*#\n#=\s*P.*execution script\s*=#\n#==*#\n)([^#]*)'
        pre, post = [i[1].strip() for i in findall(regex, mlinput)]
    else:
        pre, post = ('', '')
    return pre, post


def edit_new_comment():
    from aiida_verdi.utils.tpl import env
    t = env.get_template('new_cmt.txt.tpl')
    content = t.render()
    mlinput = click.edit(content, extension='.txt')
    if mlinput:
        import re
        regex = r'^(?!#=)(.*)$'
        cmt = '\n'.join(re.findall(regex, mlinput, flags=re.M))
        cmt = cmt.strip('\n')
    else:
        cmt = ''
    return cmt
