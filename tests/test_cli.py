import pytest
from click.testing import CliRunner
from telem_cli.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Telem CLI" in result.output
