"""
Tests for CLI auth helper behavior.

These tests avoid calling a live API and focus on local token persistence helpers.
"""

import yatharth_os.cli.app as cli_app


def test_save_and_load_token(tmp_path, monkeypatch) -> None:
    """CLI should persist and load JWT tokens from the configured token file."""

    token_path = tmp_path / "token.json"

    monkeypatch.setattr(cli_app, "TOKEN_FILE", token_path)

    cli_app._save_token("fake-token")

    assert token_path.exists()
    assert cli_app._load_token() == "fake-token"


def test_api_url_uses_environment_variable(monkeypatch) -> None:
    """CLI should support overriding API URL through environment variable."""

    monkeypatch.setenv("YATHARTH_OS_API_URL", "http://localhost:9000/")

    assert cli_app._api_url() == "http://localhost:9000"
