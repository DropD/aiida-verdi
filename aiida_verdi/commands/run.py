import click
from click import FileError


@click.command(short_help='Execute an AiiDA script')
@click.option('-g', '--group', type=bool, default=True,
              help='Enables the autogrouping, default = True')
@click.option('-n', '--groupname', type=str, default=None,
              help='Specify the name of the auto group')
@click.option('-o','--grouponly', type=str, nargs='-1', default=['all'],
              help='Limit the grouping to specific classes (by default, all classes are grouped')
@click.option('-e', '--exclude', type=str, nargs='+', default=[],
              help=('Autogroup only specific calculation classes.'
                    " Select them by their module name.")
              )
@click.option('-E', '--excludesubclasses', type=str, nargs='-1',
              default=[], help=('Autogroup only specific calculation classes.'
                                " Select them by their module name.")
              )
@click.option('-i', '--include', type=str, nargs='-1',
              default=['all'], help=('Autogroup only specific data classes.'
                                     " Select them by their module name.")
              )
@click.option('-I', '--includesubclasses', type=str, nargs='-1',
              default=[], help=('Autogroup only specific code classes.'
                                " Select them by their module name.")
              )
@click.argument('scriptname', metavar='ScriptName', type=click.Path(exists=True))
@click.argument('new_args', metavar='ARGS', nargs=-1, type=str)
@click.pass_context
def run(ctx, group, groupname, grouponly, exclude, excludesubclasses, include, includesubclasses, scriptname, new_args):
    """
    Execute an AiiDA script, given by ScriptName. All additional ARGS are passed to the script
    """
    import aiida
    from aiida.backends.utils import load_dbenv,is_dbenv_loaded
    from aiida.cmdline.commands.shell import default_modules_list
    from aiida.orm.autogroup import Autogroup

    if not is_dbenv_loaded():
        load_dbenv()

    # Prepare the environment for the script to be run
    globals_dict = {
        '__builtins__': globals()['__builtins__'],
        '__name__': '__main__',
        '__file__': scriptname,
        '__doc__': None,
        '__package__': None}

    ## dynamically load modules (the same of verdi shell) - but in
    ## globals_dict, not in the current environment
    for app_mod, model_name, alias in default_modules_list:
        globals_dict["{}".format(alias)] = getattr(
            __import__(app_mod, {}, {}, model_name), model_name)

    if group:
        automatic_group_name = groupname
        if automatic_group_name is None:
            import datetime

        aiida_verdilib_autogroup = Autogroup()
        aiida_verdilib_autogroup.set_exclude(exclude)
        aiida_verdilib_autogroup.set_include(include)
        aiida_verdilib_autogroup.set_exclude_with_subclasses(
            excludesubclasses)
        aiida_verdilib_autogroup.set_include_with_subclasses(
            includesubclasses)
        aiida_verdilib_autogroup.set_group_name(automatic_group_name)
        ## Note: this is also set in the exec environment!
        ## This is the intended behavior
        aiida.orm.autogroup.current_autogroup = aiida_verdilib_autogroup

    try:
        f = open(scriptname)
    except IOError:
        msg = "{}: Unable to load file.".format(ctx.command_path)
        raise FileError(scriptname, msg)
    else:
        try:
            # Must add also argv[0]
            new_argv = [scriptname] + new_args
            with update_environment(new_argv=new_argv):
                # Add local folder to sys.path
                sys.path.insert(0, os.path.abspath(os.curdir))
                # Pass only globals_dict
                exec (f, globals_dict)
                # print sys.argv
        finally:
            f.close()
