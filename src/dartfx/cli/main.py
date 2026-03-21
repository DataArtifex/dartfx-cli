import shlex
from pathlib import Path

import click
import typer
from rich.console import Console

from dartfx.cli.__about__ import __version__

app = typer.Typer(
    name="dartfx",
    help="Rich CLI for the dartfx ecosystem",
    rich_markup_mode="rich",
)
console = Console()

_SHELL_EXIT_COMMANDS = {"exit", "quit", "q"}
_SHELL_HISTORY_PATH = Path.home() / ".dartfx_history"


def _get_top_level_commands() -> list[str]:
    """Return top-level command names for the CLI."""
    click_app = typer.main.get_command(app)
    if isinstance(click_app, click.Group):
        return sorted(click_app.commands.keys())
    return []


def _get_command_options(cmd_name: str) -> list[str]:
    """Return sorted option names (e.g. --flag) for a named CLI command.

    Includes both explicitly declared options and the built-in ``--help``
    option, which Click 8.x adds dynamically via ``get_help_option()``.
    """
    click_app = typer.main.get_command(app)
    if not isinstance(click_app, click.Group):
        return []
    cmd = click_app.commands.get(cmd_name)
    if cmd is None:
        return []
    options: list[str] = []
    ctx = click.Context(cmd)
    help_option = cmd.get_help_option(ctx)
    if help_option is not None:
        options.extend(help_option.opts)
    for param in cmd.params:
        if isinstance(param, click.Option):
            options.extend(param.opts)
    return sorted(options)


def _get_shell_completion_matches(text: str, line_buffer: str, commands: list[str]) -> list[str]:
    """Return completion matches for a shell line buffer.

    - First token: completes top-level command names.
    - Subsequent tokens: completes options (``--flag``) for that command.
    """
    if line_buffer.lstrip() != line_buffer:
        return []

    tokens = line_buffer.split()
    has_trailing_space = line_buffer.endswith(" ")

    # First token (command name) completion
    if not tokens or (len(tokens) == 1 and not has_trailing_space):
        return [cmd for cmd in commands if cmd.startswith(text)]

    # Option completion for the command in the first token
    cmd_name = tokens[0]
    return [opt for opt in _get_command_options(cmd_name) if opt.startswith(text)]


def _configure_shell_readline(commands: list[str]) -> tuple[object | None, list[str]]:
    """Configure readline history and tab completion for shell mode."""
    try:
        import readline
    except ImportError:
        return None, commands

    def completer(text: str, state: int) -> str | None:
        line_buffer = readline.get_line_buffer()
        matches = _get_shell_completion_matches(text, line_buffer, commands)
        if state < len(matches):
            return matches[state]
        return None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    try:
        readline.read_history_file(_SHELL_HISTORY_PATH)
    except FileNotFoundError:
        pass

    return readline, commands


def _persist_shell_history(readline_module: object | None) -> None:
    """Persist shell history when readline is available."""
    if readline_module is None:
        return

    readline_module.set_history_length(1000)
    readline_module.write_history_file(_SHELL_HISTORY_PATH)


def _run_shell_command(command_line: str) -> None:
    """Run a single dartfx command line from the interactive shell."""
    try:
        args = shlex.split(command_line)
    except ValueError as error:
        console.print(f"[bold red]Parse error:[/bold red] {error}")
        return

    if not args:
        return

    try:
        app(args=args, prog_name="dartfx", standalone_mode=False)
    except typer.Exit:
        return
    except click.ClickException as error:
        error.show()
    except Exception as error:  # pragma: no cover
        console.print(f"[bold red]Error:[/bold red] {error}")


@app.command()
def version():
    """Display the version of dartfx-cli."""
    console.print(f"dartfx-cli version: [bold green]{__version__}[/bold green]")


@app.command()
def shell() -> None:
    """Start an interactive dartfx subshell."""
    commands = _get_top_level_commands()
    readline_module, _ = _configure_shell_readline(commands)
    console.print("Entering dartfx shell. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            command_line = input("dartfx> ").strip()
        except EOFError:
            console.print("\nLeaving dartfx shell.")
            _persist_shell_history(readline_module)
            break
        except KeyboardInterrupt:
            console.print()
            continue

        if not command_line:
            continue

        if command_line in _SHELL_EXIT_COMMANDS:
            console.print("Leaving dartfx shell.")
            _persist_shell_history(readline_module)
            break

        _run_shell_command(command_line)


@app.callback()
def main():
    """
    DartFX CLI - Interactive access to the dartfx ecosystem.
    """
    pass


if __name__ == "__main__":
    app()
