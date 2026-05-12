"""
Rich-powered command-line interface for Yatharth OS.

This module exposes the `yatharth` CLI command configured in `pyproject.toml`.

The CLI intentionally reads from the same JSON-backed data layer as the FastAPI
backend. This keeps the project clean and avoids duplicating portfolio logic
between the API and terminal interface.

Example usage:
    poetry run yatharth whoami
    poetry run yatharth skills
    poetry run yatharth projects
    poetry run yatharth projects --tag rag
    poetry run yatharth experience
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from yatharth_os.core.loader import (
    load_experience,
    load_profile,
    load_projects,
    load_skills,
)
from yatharth_os.exporters.pdf import build_profile_pdf_bytes

app = typer.Typer(
    name="yatharth",
    help="CLI-first engineering portfolio for Yatharth Mahesh Sant.",
    no_args_is_help=True,
)
auth_app = typer.Typer(
    name="auth",
    help="Authenticate with a running Yatharth OS API service.",
    no_args_is_help=True,
)

app.add_typer(auth_app, name="auth")
console = Console()

DEFAULT_API_URL = "http://127.0.0.1:8000"
TOKEN_FILE = Path.home() / ".yatharth_os" / "token.json"


def _api_url() -> str:
    """Return configured API URL for CLI HTTP calls."""

    return os.getenv("YATHARTH_OS_API_URL", DEFAULT_API_URL).rstrip("/")


def _save_token(token: str) -> None:
    """Persist JWT token locally for CLI usage."""

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(
        json.dumps({"access_token": token}, indent=2), encoding="utf-8"
    )


def _load_token() -> str | None:
    """Load stored CLI JWT token if it exists."""

    if not TOKEN_FILE.exists():
        return None

    data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    token = data.get("access_token")
    return str(token) if token else None


def _normalize_tag(value: str | None) -> str | None:
    """Normalize a user-provided tag for case-insensitive filtering.

    Args:
        value: Optional tag value passed from the CLI.

    Returns:
        Lowercase stripped tag if provided, otherwise None.
    """

    if value is None:
        return None

    normalized = value.strip().lower()
    return normalized or None


def _project_matches_tag(project: dict[str, Any], tag: str | None) -> bool:
    """Check whether a project contains the requested tag.

    Args:
        project: Project dictionary loaded from `data/projects.json`.
        tag: Optional normalized tag.

    Returns:
        True if no tag filter is provided or the project contains the tag.
    """

    if tag is None:
        return True

    project_tags = [str(item).lower() for item in project.get("tags", [])]
    return tag in project_tags


@app.command()
def whoami() -> None:
    """Show a concise profile card."""

    profile = load_profile()

    name = profile.get("name", "Yatharth Mahesh Sant")
    title = profile.get("title", "Applied AI Engineer")
    location = profile.get("location", "Singapore")
    summary = profile.get("summary", "")

    content = Text()
    content.append(f"{name}\n", style="bold cyan")
    content.append(f"{title}\n", style="bold")
    content.append(f"Location: {location}\n", style="green")
    content.append("Contact: authenticated contact request flow\n", style="green")

    if summary:
        content.append("\n")
        content.append(summary, style="white")

    console.print(
        Panel(
            content,
            title="Yatharth OS :: whoami",
            subtitle="CLI-first portfolio",
            expand=False,
            border_style="cyan",
        )
    )


@app.command()
def skills() -> None:
    """Show skills grouped by category."""

    skills_data = load_skills()

    table = Table(
        title="Yatharth OS :: Skills",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
    )
    table.add_column("Category", style="bold green", no_wrap=True)
    table.add_column("Skills", style="white")

    for category, items in skills_data.items():
        skill_text = ", ".join(str(item) for item in items)
        table.add_row(str(category), skill_text)

    console.print(table)


@app.command()
def projects(
    tag: str | None = typer.Option(
        None,
        "--tag",
        "-t",
        help="Filter projects by tag, for example: rag, fastapi, computer-vision.",
    ),
) -> None:
    """Show portfolio projects, optionally filtered by tag."""

    normalized_tag = _normalize_tag(tag)
    projects_data = load_projects()

    filtered_projects = [
        project
        for project in projects_data
        if _project_matches_tag(project, normalized_tag)
    ]

    table_title = "Yatharth OS :: Projects"
    if normalized_tag:
        table_title += f" [tag={normalized_tag}]"

    table = Table(
        title=table_title,
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
    )
    table.add_column("Project", style="bold green", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Tags", style="magenta")

    for project in filtered_projects:
        table.add_row(
            str(project.get("name", "Unnamed project")),
            str(project.get("description", "")),
            ", ".join(str(item) for item in project.get("tags", [])),
        )

    if not filtered_projects:
        console.print(
            Panel(
                f"No projects found for tag: [bold]{normalized_tag}[/bold]",
                title="No results",
                border_style="yellow",
            )
        )
        raise typer.Exit(code=0)

    console.print(table)


DEFAULT_EXPORT_OUTPUT = typer.Option(
    Path("yatharth-profile.pdf"),
    "--output",
    "-o",
    help="Output PDF path.",
)


@app.command("export-pdf")
def export_pdf(output: Path = DEFAULT_EXPORT_OUTPUT) -> None:
    """Export the profile and resume-style portfolio data as a PDF."""

    pdf_bytes = build_profile_pdf_bytes()

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(pdf_bytes)

    console.print(
        Panel(
            f"PDF exported successfully:\n[bold green]{output.resolve()}[/bold green]",
            title="Export complete",
            border_style="green",
            expand=False,
        )
    )


@app.command()
def experience() -> None:
    """Show professional experience as terminal panels.

    The experience JSON uses a resume-friendly structure:
    role, organization, location, start, end, and highlights.

    This command intentionally avoids assuming fields like company,
    duration, or description so the CLI stays aligned with the source data.
    """

    experience_data = load_experience()

    for item in experience_data:
        role = item.get("role", "Role")
        organization = item.get("organization", item.get("company", "Organization"))
        location = item.get("location", "")
        start = item.get("start", "")
        end = item.get("end", "")
        highlights = item.get("highlights", [])

        duration = f"{start} - {end}".strip(" -")

        body = Text()
        body.append(f"{role}\n", style="bold green")

        if duration:
            body.append(f"{duration}\n", style="cyan")

        if location:
            body.append(f"{location}\n", style="magenta")

        if highlights:
            body.append("\n")
            for highlight in highlights:
                body.append(f"• {highlight}\n", style="white")

        console.print(
            Panel(
                body,
                title=str(organization),
                border_style="cyan",
                expand=False,
            )
        )


@auth_app.command("register")
def auth_register() -> None:
    """Register with the running Yatharth OS API and store the access token."""

    full_name = typer.prompt("Full name")
    email = typer.prompt("Email")
    password = typer.prompt("Password", hide_input=True, confirmation_prompt=True)

    response = httpx.post(
        f"{_api_url()}/auth/register",
        json={
            "email": email,
            "full_name": full_name,
            "password": password,
        },
        timeout=10.0,
    )

    if response.status_code != 201:
        console.print(
            Panel(response.text, title="Registration failed", border_style="red")
        )
        raise typer.Exit(code=1)

    token = response.json()["access_token"]
    _save_token(token)

    console.print(
        Panel(
            "Registration successful. Access token saved for CLI use.",
            title="Auth complete",
            border_style="green",
        )
    )


@auth_app.command("login")
def auth_login() -> None:
    """Login with the running Yatharth OS API and store the access token."""

    email = typer.prompt("Email")
    password = typer.prompt("Password", hide_input=True)

    response = httpx.post(
        f"{_api_url()}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=10.0,
    )

    if response.status_code != 200:
        console.print(Panel(response.text, title="Login failed", border_style="red"))
        raise typer.Exit(code=1)

    token = response.json()["access_token"]
    _save_token(token)

    console.print(
        Panel(
            "Login successful. Access token saved for CLI use.",
            title="Auth complete",
            border_style="green",
        )
    )


@auth_app.command("me")
def auth_me() -> None:
    """Show the authenticated user from the API."""

    token = _load_token()

    if token is None:
        console.print(
            Panel(
                "No stored token found. Run `yatharth auth login` first.",
                title="Not authenticated",
                border_style="yellow",
            )
        )
        raise typer.Exit(code=1)

    response = httpx.get(
        f"{_api_url()}/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )

    if response.status_code != 200:
        console.print(
            Panel(response.text, title="Authentication failed", border_style="red")
        )
        raise typer.Exit(code=1)

    user = response.json()

    console.print(
        Panel(
            f"[bold cyan]{user['full_name']}[/bold cyan]\n{user['email']}\n"
            f"Active: {user['is_active']}",
            title="Authenticated user",
            border_style="cyan",
        )
    )


@app.command()
def version() -> None:
    """Show CLI version information."""

    console.print("[bold cyan]Yatharth OS[/bold cyan] version 0.1.0")


def main() -> None:
    """CLI entrypoint used by Poetry."""

    app()


if __name__ == "__main__":
    main()
