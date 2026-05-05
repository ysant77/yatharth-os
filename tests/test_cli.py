"""
Tests for the Yatharth OS CLI.

The CLI is tested through Typer's CliRunner, which allows command execution
without spawning a real shell process. These tests validate command behavior,
exit codes, and key output content.
"""

from typer.testing import CliRunner

from yatharth_os.cli.app import app

runner = CliRunner()


def test_whoami_command_displays_profile() -> None:
    """The whoami command should display the profile owner."""

    result = runner.invoke(app, ["whoami"])

    assert result.exit_code == 0
    assert "Yatharth" in result.output
    assert "CLI-first portfolio" in result.output


def test_skills_command_displays_skill_table() -> None:
    """The skills command should render a table of skill categories."""

    result = runner.invoke(app, ["skills"])

    assert result.exit_code == 0
    assert "Skills" in result.output


def test_projects_command_displays_projects() -> None:
    """The projects command should display available portfolio projects."""

    result = runner.invoke(app, ["projects"])

    assert result.exit_code == 0
    assert "Projects" in result.output


def test_projects_command_supports_tag_filter() -> None:
    """The projects command should support tag-based filtering."""

    result = runner.invoke(app, ["projects", "--tag", "rag"])

    assert result.exit_code == 0
    assert "Projects" in result.output


def test_projects_command_handles_unknown_tag() -> None:
    """Unknown tags should produce a clean no-results message."""

    result = runner.invoke(app, ["projects", "--tag", "unknown-tag"])

    assert result.exit_code == 0
    assert "No projects found" in result.output


def test_experience_command_displays_experience() -> None:
    """The experience command should display professional experience."""

    result = runner.invoke(app, ["experience"])

    assert result.exit_code == 0
    assert result.output.strip() != ""


def test_version_command_displays_version() -> None:
    """The version command should display project version information."""

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Yatharth OS" in result.output
    assert "0.1.0" in result.output


def test_cli_without_args_shows_help() -> None:
    """Running the CLI without arguments should show help text."""

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "CLI-first engineering portfolio" in result.output
