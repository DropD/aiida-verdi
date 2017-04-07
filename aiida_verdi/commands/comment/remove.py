# -*- coding: utf-8 -*-
"""
verdi comment remove
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.node()
@click.argument('comment-id', type=int, nargs=-1)
@click.option('-a', '-all', 'all_cmt', is_flag=True, help='If used, deletes all the comments of the active user attached to the node')
@click.option('-f', '--force', is_flag=True, help='Delete without confirmation')
@options.dry_run()
@options.non_interactive()
def remove(node, comment_id, all_cmt, force, dry_run, non_interactive):
    """
    Remove comment(s) (with COMMENT_ID) from a NODE
    """
    # Note: in fact, the user can still manually delete any comment
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.backends.utils import get_automatic_user

    user = get_automatic_user()

    if not comment_id and not all_cmt:
        return 0
    if comment_id and all_cmt:
        raise click.BadOptionUsage("Only one between -a and ID should be provided")

    if all_cmt:
        conf_msg = 'Delete all comments of user {} for node {}?'.format(user, node.pk)
        comments = node.get_comment_obj(user=user)
    else:
        conf_msg = 'Delete {} comments for node {}?'.format(len(comment_id), node.pk)
        from aiida.orm.implementation import Comment as CommentOrm
        comments = [CommentOrm(id=id_, user=user) for id_ in comment_id]

    if not force:
        if non_interactive:
            click.echo('Not deleting (use --force to non-interactively delete)')
            return 0
        else:
            click.confirm(conf_msg, abort=True)

    if not dry_run:
        for comment in comments:
            comment.delete()
            click.echo("Deleted {} comment(s).".format(len(comments)))
    else:
        click.echo('Not deleting {} comment(s) (--dry-run recieved)'.format(len(comments)))
