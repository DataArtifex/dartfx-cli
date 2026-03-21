from typer.testing import CliRunner

from dartfx.cli.main import app
from dartfx.cli.main import _get_command_options
from dartfx.cli.main import _get_shell_completion_matches


runner = CliRunner()


def test_shell_exit_command() -> None:
    result = runner.invoke(app, ["shell"], input="exit\n")

    assert result.exit_code == 0
    assert "Entering dartfx shell." in result.stdout
    assert "Leaving dartfx shell." in result.stdout


def test_shell_runs_version_command() -> None:
    result = runner.invoke(app, ["shell"], input="version\nexit\n")

    assert result.exit_code == 0
    assert "dartfx-cli version:" in result.stdout


def test_shell_completion_matches_first_token() -> None:
    matches = _get_shell_completion_matches("v", "v", ["version", "shell"])

    assert matches == ["version"]


def test_shell_completion_ignores_non_first_token() -> None:
    # "v" doesn't match any option of the version command (which has --help)
    matches = _get_shell_completion_matches("v", "version v", ["version", "shell"])

    assert matches == []


def test_shell_completion_matches_options() -> None:
    matches = _get_shell_completion_matches("--h", "version --h", ["version", "shell"])

    assert "--help" in matches


def test_shell_completion_no_options_for_unknown_command() -> None:
    matches = _get_shell_completion_matches("--h", "unknown --h", ["version", "shell"])

    assert matches == []


def test_get_command_options_returns_help() -> None:
    options = _get_command_options("version")

    assert "--help" in options


def test_get_command_options_unknown_returns_empty() -> None:
    options = _get_command_options("nonexistent")

    assert options == []