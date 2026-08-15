"""Command line interface for Swackhammer."""

from __future__ import annotations

from typing import Optional

import pandas as pd
import typer
from rich import print as rprint
from rich.table import Table

from .espn_client import create_league, fetch_free_agents, fetch_my_team, list_player_names
from .features import ensure_percentages
from .nba_client import fetch_per_game_by_season, lookup_player_id
from .recommend import replacement_value

app = typer.Typer(help="Swackhammer fantasy basketball assistant")


def _build_player_frame(names: list[str]) -> pd.DataFrame:
    records = []
    for name in names:
        nba_id = lookup_player_id(name)
        if not nba_id:
            continue
        line = fetch_per_game_by_season(nba_id).to_category_map()
        line["Player"] = name
        records.append(line)
    return ensure_percentages(pd.DataFrame(records))


@app.command()
def free_agents(limit: int = typer.Option(50, help="Number of free agents to fetch")) -> None:
    agents = fetch_free_agents(limit=limit)
    names = list_player_names(agents)
    table = Table(title="Free Agents")
    table.add_column("#")
    table.add_column("Name")
    for idx, name in enumerate(names, start=1):
        table.add_row(str(idx), name)
    rprint(table)


@app.command()
def recommend(
    limit: int = typer.Option(10, help="Number of add/drop suggestions to display"),
    punt_ft: bool = typer.Option(False, help="Punt FT%"),
    punt_to: bool = typer.Option(False, help="Punt turnovers"),
    team_id: Optional[int] = typer.Option(None, help="Your ESPN team id"),
    free_agent_limit: int = typer.Option(100, help="How many free agents to evaluate"),
) -> None:
    team = fetch_my_team(team_id=team_id)
    roster_names = [player.name for player in team.roster]
    fa_names = list_player_names(fetch_free_agents(limit=free_agent_limit))

    roster_df = _build_player_frame(roster_names)
    fa_df = _build_player_frame(fa_names)

    punt = []
    if punt_ft:
        punt.append("FT%")
    if punt_to:
        punt.append("TO")

    suggestions = replacement_value(roster_df, fa_df, punt=punt, limit=limit)
    table = Table(title="Add/Drop Suggestions")
    table.add_column("Add")
    table.add_column("Drop")
    table.add_column("Delta", justify="right")
    for _, row in suggestions.iterrows():
        table.add_row(str(row["add"]), str(row["drop"]), f"{row['delta']:.2f}")
    rprint(table)


@app.command()
def league_info() -> None:
    league = create_league()
    table = Table(title="League Overview")
    table.add_column("Team")
    table.add_column("Owner")
    for team in league.teams:
        table.add_row(team.team_name, team.owner)
    rprint(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
