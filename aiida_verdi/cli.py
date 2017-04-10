# -*- coding: utf-8 -*-
"""
The experimental next-gen verdi commandline
"""
import click
from click_completion import init as cc_init
from aiida_verdi.commands.calculation import calculation
from aiida_verdi.commands.code import code
from aiida_verdi.commands.comment import comment
from aiida_verdi.commands.computer import computer
from aiida_verdi.commands.data import data
from aiida_verdi.commands.plugin import plugin
from aiida_verdi.commands.run import run
from aiida_verdi.commands.quicksetup import quicksetup
from aiida_verdi.commands.setup import setup
from aiida_verdi.commands.daemon import daemon


cc_init()


@click.group()
def main():
    """Experimental verdi commandline upgraded to click"""


main.add_command(calculation)
main.add_command(code)
main.add_command(comment)
main.add_command(computer)
main.add_command(data)
main.add_command(plugin)
main.add_command(run)
main.add_command(quicksetup)
main.add_command(setup)
main.add_command(daemon)


if __name__ == '__main__':
    main()
