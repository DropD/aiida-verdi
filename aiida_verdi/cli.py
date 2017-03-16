import click
from commands.code import code
from commands.computer import computer
from commands.data import data
from commands.plugin import plugin


@click.group()
def main():
    """Experimental verdi commandline upgraded to click"""


main.add_command(code, name='code')
main.add_command(computer)
main.add_command(data)
main.add_command(plugin)


if __name__ == '__main__':
    main()
