import typer
from rich.console import Console
from dartfx.cli.__about__ import __version__

app = typer.Typer(
    name="dartfx",
    help="Rich CLI for the dartfx ecosystem",
    rich_markup_mode="rich"
)
console = Console()

@app.command()
def version():
    """Display the version of dartfx-cli."""
    console.print(f"dartfx-cli version: [bold green]{__version__}[/bold green]")

@app.callback()
def main():
    """
    DartFX CLI - Interactive access to the dartfx ecosystem.
    """
    pass

if __name__ == "__main__":
    app()
