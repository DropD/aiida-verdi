import click
from click.testing import CliRunner

from aiida_verdi.utils.interactive import InteractiveOption
from aiida_verdi.options import non_interactive


def test_str():
    @click.command()
    @click.option('--opt', prompt='Opt', type=str, cls=InteractiveOption)
    @non_interactive()
    def cmd(opt, non_interactive):
        return opt

    runner = CliRunner()
    result = runner.invoke(cmd, [], input='TEST')
    assert result.output == ('Opt: TEST\n')
