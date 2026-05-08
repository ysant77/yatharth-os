"""
Tests for CLI PDF export command.
"""

from typer.testing import CliRunner

from yatharth_os.cli.app import app

runner = CliRunner()


def test_export_pdf_command_creates_pdf_file() -> None:
    """The export-pdf command should create a PDF file at the requested path."""

    with runner.isolated_filesystem():
        result = runner.invoke(app, ["export-pdf", "--output", "profile.pdf"])

        assert result.exit_code == 0
        assert "PDF exported successfully" in result.output

        with open("profile.pdf", "rb") as file:
            pdf_bytes = file.read()

        assert pdf_bytes.startswith(b"%PDF")
        assert len(pdf_bytes) > 1000
