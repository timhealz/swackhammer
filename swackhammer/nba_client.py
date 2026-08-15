"""Utilities for fetching NBA player data via ``nba_api``."""

from __future__ import annotations

import time
from typing import Dict, Optional

from nba_api.stats.endpoints import playerdashboardbyyearoveryear
from nba_api.stats.static import players

from .cache import cached
from .models import PlayerCategoryLine

DEFAULT_SEASON = "2024-25"


@cached(ttl=24 * 3600)
def lookup_player_id(full_name: str) -> Optional[int]:
    matches = players.find_players_by_full_name(full_name)
    if not matches:
        return None
    return matches[0]["id"]


@cached(ttl=12 * 3600)
def fetch_per_game_by_season(player_id: int, season: str = DEFAULT_SEASON) -> PlayerCategoryLine:
    dash = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(
        player_id=player_id, season=season
    ).get_dict()
    # polite pause to avoid hammering the API if caching disabled
    time.sleep(0.6)
    datasets = dash["resultSets"]
    headers = datasets[1]["headers"]
    rows = datasets[1]["rowSet"]
    latest = rows[-1]
    data = dict(zip(headers, latest))
    return PlayerCategoryLine(
        PTS=data.get("PTS", 0.0),
        REB=data.get("REB", 0.0),
        AST=data.get("AST", 0.0),
        **{"3PM": data.get("FG3M", 0.0)},
        STL=data.get("STL", 0.0),
        BLK=data.get("BLK", 0.0),
        FGM=data.get("FGM", 0.0),
        FGA=data.get("FGA", 0.0),
        FTM=data.get("FTM", 0.0),
        FTA=data.get("FTA", 0.0),
        TO=data.get("TOV", 0.0),
    )


def per_game_category_map(player_id: int, season: str = DEFAULT_SEASON) -> Dict[str, float]:
    return fetch_per_game_by_season(player_id, season).to_category_map()


__all__ = ["DEFAULT_SEASON", "lookup_player_id", "fetch_per_game_by_season", "per_game_category_map"]
