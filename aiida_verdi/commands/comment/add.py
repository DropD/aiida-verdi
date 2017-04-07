#-*- coding: utf-8 -*-
"""
verdi command add
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.node()
@click.option('-c', '--comment')
@options.dry_run()
@options.non_interactive()
def add(node, comment, dry_run, non_interactive):
    """
    Add a comment to a NODE in the database.

    if no comment is given via the -c / --comment option, an editor
    will be opened to edit the comment in
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.backends.utils import get_automatic_user

    user = get_automatic_user()

    if not comment:
        if non_interactive:
            return 0
        from aiida_verdi.utils.mlinput import edit_new_comment
        comment = edit_new_comment()

    if not dry_run:
        node.add_comment(comment, user)
    else:
        click.echo('Comment not added (--dry-run recieved).\n')
