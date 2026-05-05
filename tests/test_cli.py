from typer.testing import CliRunner

from yatharth_os.cli.app import app

runner = CliRunner()


def test_whoami_command() -> None:
    result = runner.invoke(app, ["whoami"])
    assert result.exit_code == 0
    assert "Yatharth Mahesh Sant" in result.output
