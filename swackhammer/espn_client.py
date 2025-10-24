"""Helpers for interacting with the ESPN fantasy basketball API."""

from __future__ import annotations

from typing import Any, Iterable, List, Optional

from espn_api.basketball import League

from .config import Settings, get_settings


def create_league(settings: Optional[Settings] = None) -> League:
    """Instantiate an ``espn_api`` League using configuration values."""

    cfg = settings or get_settings()
    cfg.validate_required()
    return League(
        league_id=cfg.league_id,
        year=cfg.season_id,
        espn_s2=cfg.espn_s2,
        swid=cfg.swid,
    )


def fetch_teams(league: Optional[League] = None) -> List[Any]:
    league = league or create_league()
    return list(league.teams)


def fetch_my_team(team_id: Optional[int] = None, league: Optional[League] = None) -> Any:
    league = league or create_league()
    if team_id is None:
        return league.teams[0]
    for team in league.teams:
        if team.team_id == team_id:
            return team
    raise ValueError(f"Team id {team_id} not found")


def fetch_free_agents(limit: int = 100, league: Optional[League] = None) -> List[Any]:
    league = league or create_league()
    return list(league.free_agents(size=limit))


def list_player_names(players: Iterable[Any]) -> List[str]:
    return [getattr(player, "name", "") for player in players]


__all__ = [
    "create_league",
    "fetch_teams",
    "fetch_my_team",
    "fetch_free_agents",
    "list_player_names",
]
