# -*- coding: utf-8 -*-
"""
verdi comment update
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.node()
@arguments.comment_id()
@click.option('-c', '--comment')
@options.dry_run()
@options.non_interactive()
def update(node, comment_id, comment, dry_run, non_interactive):
    """
    Change a comment of a NODE in the database
    """
    if not comment:
        if non_interactive:
            return 0
        from aiida_verdi.utils.mlinput import edit_comment
        old_cmt = node.get_comments(pk=comment_id)
        if not old_cmt:
            raise click.BadArgument('Node {} has no comment {}!'.format(node.pk, comment_id))
        else:
            old_cmt = old_cmt[0]
        comment = edit_comment(old_cmt['content'])

    if not dry_run:
        node._update_comment(the_comment, comment_id, user)
    else:
        "Comment not changed (--dry-run recieved)"
