# Technical Implementation Overview

This document describes the technical architecture and implementation details of the `dartfx-cli` package.

## Architecture

The CLI is built using a modular subcommand-based architecture, designed to scale as more tools are added to the dartfx ecosystem.

### Core Frameworks
- **[Typer](https://typer.tiangolo.com/)**: Used as the primary CLI engine. It leverages Python type hints for argument parsing, validation, and automatic help generation.
- **[Rich](https://rich.readthedocs.io/)**: Integrated for terminal UI enhancements, including colors, tables, markdown rendering, and progress indicators.
- **[Pydantic](https://docs.pydantic.dev/)**: Used for data modeling and configuration validation across the package.

### Entry Point
The main entrance to the CLI is `dartfx.cli.main:app`.
- Defined in `src/dartfx/cli/main.py`.
- Configured in `pyproject.toml` under `[project.scripts]`.

### Subcommand Pattern
Each logical tool or package interface is implemented as a separate Typer application or command.
- Simple commands are defined as functions in separate files (e.g., `src/dartfx/cli/foo.py`).
- Complex subcommands use a subpackage with their own `main.py` entry point.
- Subcommands are registered in the root app using `app.add_typer()`.

## Directory Structure

```text
src/dartfx/cli/
├── __about__.py    # Dynamic versioning source
├── __init__.py     # Package exports
├── main.py        # Root Typer application (entry point)
└── [subcommand].py # Individual subcommand implementations
```

## Features

### Versioning
Dynamic versioning is handled by Hatchling. The version is stored in `src/dartfx/cli/__about__.py` and exposed to the CLI via the `version` command in `main.py`.

### Help & Documentation
- Every command and subcommand includes docstrings which Typer automatically converts into terminal help messages (accessible via `--help`).
- Rich markup is enabled in Typer (`rich_markup_mode="rich"`) allowing for formatted help text.

## Development Standards

### Type Hinting
Strict type hinting is required for all function signatures. Typer uses these hints to determine the expected CLI argument types (e.g., `int`, `Path`, `bool`).

### Formatting & Linting
Enforced via **Ruff**. The configuration is defined in `pyproject.toml`, focusing on standard PEP 8 compliance and modern Python practices.

### Environment Management
The project prefers **uv** for fast dependency resolution and environment sync. 
- Configuration: `pyproject.toml`
- Locks: `uv.lock`
