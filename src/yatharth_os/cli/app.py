import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from yatharth_os.core.loader import load_profile, load_projects, load_skills

app = typer.Typer(help="Yatharth OS: CLI-first engineering portfolio.")
console = Console()


@app.command()
def whoami() -> None:
    """Show a quick identity card."""
    profile = load_profile()
    body = (
        f"[bold]{profile['name']}[/bold]\n{profile['headline']}\n{profile['location']}"
    )
    console.print(Panel(body, title="whoami", expand=False))


@app.command()
def projects(
    tag: str | None = typer.Option(None, help="Filter projects by tag.")
) -> None:
    """List selected projects."""
    items = load_projects()
    if tag:
        items = [project for project in items if tag in project.get("tags", [])]

    table = Table(title="Projects")
    table.add_column("Name", style="bold")
    table.add_column("Tags")
    table.add_column("Description")

    for project in items:
        table.add_row(
            project["name"],
            ", ".join(project.get("tags", [])),
            project["description"],
        )
    console.print(table)


@app.command()
def skills() -> None:
    """List skill groups."""
    data = load_skills()
    table = Table(title="Skills")
    table.add_column("Group", style="bold")
    table.add_column("Skills")
    for group, values in data.items():
        table.add_row(group.replace("_", " ").title(), ", ".join(values))
    console.print(table)
