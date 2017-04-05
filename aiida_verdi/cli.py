import click
from click_completion import init as cc_init
from commands.calculation import calculation
from commands.code import code
from commands.computer import computer
from commands.data import data
from commands.plugin import plugin
from commands.run import run
from commands.quicksetup import quicksetup
from commands.setup import setup


cc_init()

@click.group()
def main():
    """Experimental verdi commandline upgraded to click"""


main.add_command(code)
main.add_command(calculation)
main.add_command(computer)
main.add_command(data)
main.add_command(plugin)
main.add_command(run)
main.add_command(quicksetup)
main.add_command(setup)


if __name__ == '__main__':
    main()
