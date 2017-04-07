#-*- coding: utf-8 -*-
"""
verdi command show
"""
import click

from aiida_verdi import arguments, options


@click.command()
@arguments.node()
@arguments.comment_id(required=False)
@options.user()
@options.dry_run()
@options.non_interactive()
def show(node, comment_id, user, dry_run, non_interactive):
    """
    Show the comments (with COMMENT_ID) of a NODE in the database.
    """
    from aiida_verdi.utils.aiidadb import ensure_aiida_dbenv
    ensure_aiida_dbenv()
    from aiida.backends.utils import get_automatic_user

    user = get_automatic_user()

    all_comments = node.get_comments(pk=comment_id)

    if user:
        to_print = [i for i in all_comments if i['user__email'] == user.email]
        if not to_print:
            click.echo("Nothing found for user '{}'.".format(user))
            click.echo(
                "Valid users found for Node {} are: {}.".format(node.pk,
                                                                ", ".join(set(
                                                                    ["'" + i['user__email'] + "'" for i in
                                                                     all_comments]))))
    else:
        to_print = all_comments

    if comment_id > 0:
        to_print = [i for i in to_print if i['pk'] == comment_id]

    for i in to_print:
        click.echo("*"*58)
        click.echo("Comment of '{}' on {}".format(i['user__email'],
                                                  i['ctime'].strftime("%Y-%m-%d %H:%M")))
        click.echo("ID: {}. Last modified on {}".format(i['pk'],
                                                        i['mtime'].strftime("%Y-%m-%d %H:%M")))
        click.echo("")
        click.echo("{}".format(i['content']))
        click.echo("")

    # If there is nothing to print, print a message
    if not to_print:
        click.echo("No comment found.")
