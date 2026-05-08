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

from pathlib import Path
from typing import Any

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

console = Console()


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
    email = profile.get("email", "ysant77@gmail.com")
    summary = profile.get("summary", "")

    content = Text()
    content.append(f"{name}\n", style="bold cyan")
    content.append(f"{title}\n", style="bold")
    content.append(f"Location: {location}\n", style="green")
    content.append(f"Email: {email}\n", style="green")

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


@app.command()
def version() -> None:
    """Show CLI version information."""

    console.print("[bold cyan]Yatharth OS[/bold cyan] version 0.1.0")


def main() -> None:
    """CLI entrypoint used by Poetry."""

    app()


if __name__ == "__main__":
    main()
