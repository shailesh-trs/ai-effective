"""Command-line interface for ai-effective.

Usage
-----
  ai-effective serve                   # start API + open browser
  ai-effective profile build -t TITLE  # create a profile interactively
  ai-effective profile list            # show saved profiles
  ai-effective profile delete ID       # remove a profile
  ai-effective score -p ID -q QUERY    # score a single query
"""

from __future__ import annotations

import sys
import threading
import time
import webbrowser

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
def main() -> None:
    """AI Effective — role-aware AI usage efficiency scoring."""


# ── serve ──────────────────────────────────────────────────────────────────────

@main.command()
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=8000, show_default=True)
@click.option("--no-browser", is_flag=True, help="Skip opening browser automatically")
def serve(host: str, port: int, no_browser: bool) -> None:
    """Start the REST API server and open the web UI."""
    import uvicorn

    url = f"http://{host}:{port}"
    console.print(f"\n[bold green]AI Effective[/bold green] — server starting at {url}")
    console.print("  API docs:  [dim]" + url + "/api/docs[/dim]")
    console.print("  Press [bold]Ctrl+C[/bold] to stop.\n")

    if not no_browser:
        def _open() -> None:
            time.sleep(1.8)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()

    uvicorn.run(
        "ai_effective.api.server:app",
        host=host,
        port=port,
        reload=False,
        log_level="warning",
    )


# ── profile ────────────────────────────────────────────────────────────────────

@main.group()
def profile() -> None:
    """Manage role profiles."""


@profile.command("build")
@click.option("--title", "-t", required=True, help="Job title (e.g. 'Senior Data Scientist')")
@click.option("--description", "-d", default=None, help="Job description text (inline)")
@click.option(
    "--file", "-f", "desc_file",
    default=None,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a file containing the job description",
)
def profile_build(title: str, description: str | None, desc_file: str | None) -> None:
    """Build a role profile from a job description."""
    if desc_file:
        with open(desc_file, encoding="utf-8") as fh:
            description = fh.read()
    if not description:
        description = click.edit("# Paste the job description below this line\n\n")
    if not description or not description.strip():
        console.print("[red]No description provided — aborting.[/red]")
        sys.exit(1)

    from ai_effective.role_profile.builder import RoleProfileBuilder
    from ai_effective.store import ProfileStore

    with console.status("[bold green]Building profile…[/bold green]"):
        p = RoleProfileBuilder().build(description, title)
        ProfileStore().save(p)

    console.print(Panel(
        f"[bold]Title:[/bold]   {p.title}\n"
        f"[bold]Domain:[/bold]  {p.domain}\n"
        f"[bold]Keywords:[/bold] {', '.join(p.keywords[:12])}\n"
        f"[bold]ID:[/bold]      {p.id}",
        title="[green]Profile created[/green]",
        expand=False,
    ))


@profile.command("list")
def profile_list() -> None:
    """List all saved role profiles."""
    from ai_effective.store import ProfileStore

    profiles = ProfileStore().list_all()
    if not profiles:
        console.print(
            "[yellow]No profiles found.[/yellow]  "
            "Run [bold]ai-effective profile build[/bold] to create one."
        )
        return

    tbl = Table(title="Saved Role Profiles", show_lines=True)
    tbl.add_column("ID", style="dim", width=10)
    tbl.add_column("Title")
    tbl.add_column("Domain")
    tbl.add_column("Created", style="dim")
    for p in profiles:
        tbl.add_row(p.id[:8] + "…", p.title, p.domain, p.created_at[:10])

    console.print(tbl)


@profile.command("delete")
@click.argument("profile_id")
def profile_delete(profile_id: str) -> None:
    """Delete a role profile by ID (or ID prefix)."""
    from ai_effective.store import ProfileStore

    store = ProfileStore()
    # Support prefix matching
    if len(profile_id) < 36:
        matches = [p for p in store.list_all() if p.id.startswith(profile_id)]
        if len(matches) == 0:
            console.print(f"[red]No profile matching '{profile_id}'[/red]")
            sys.exit(1)
        if len(matches) > 1:
            console.print(f"[red]Ambiguous prefix — {len(matches)} matches. Provide more characters.[/red]")
            sys.exit(1)
        profile_id = matches[0].id

    if store.delete(profile_id):
        console.print(f"[green]Deleted profile {profile_id}[/green]")
    else:
        console.print(f"[red]Profile {profile_id} not found[/red]")
        sys.exit(1)


# ── score ──────────────────────────────────────────────────────────────────────

@main.command()
@click.option("--profile-id", "-p", required=True, help="Profile ID or prefix")
@click.option("--query", "-q", required=True, help="The AI prompt/query to score")
def score(profile_id: str, query: str) -> None:
    """Score a single AI query against a role profile."""
    from ai_effective.scoring.tas import TASScorer
    from ai_effective.store import ProfileStore

    store = ProfileStore()
    # Support prefix
    if len(profile_id) < 36:
        matches = [p for p in store.list_all() if p.id.startswith(profile_id)]
        if not matches:
            console.print(f"[red]No profile matching '{profile_id}'[/red]")
            sys.exit(1)
        prof = matches[0]
    else:
        prof = store.load(profile_id)
        if not prof:
            console.print(f"[red]Profile not found: {profile_id}[/red]")
            sys.exit(1)

    with console.status("[bold green]Scoring…[/bold green]"):
        result = TASScorer().score(prof, query)

    _COLOR = {"high": "green", "medium": "yellow", "low": "red", "very_low": "bright_red"}
    c = _COLOR.get(result.label, "white")

    console.print(Panel(
        f"[bold]TAS Score:[/bold]  [{c}]{result.score} / 100[/{c}]  "
        f"([{c}]{result.label.replace('_', ' ')}[/{c}])\n\n"
        f"  Semantic alignment  (50 %)   {result.semantic_score:>5.1f}\n"
        f"  Keyword overlap     (30 %)   {result.keyword_score:>5.1f}\n"
        f"  Task-type match     (20 %)   {result.task_score:>5.1f}\n\n"
        f"[bold]Matched task type:[/bold]  {result.matched_task_type or '—'}\n"
        f"[bold]Role domain:[/bold]        {result.domain}",
        title=f"[{c}]TAS — {prof.title}[/{c}]",
        expand=False,
    ))


if __name__ == "__main__":
    main()
