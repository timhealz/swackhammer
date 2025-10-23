"""Thin client helpers around :mod:`nba_api` for fetching player game logs."""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonTypeAllStar

from .constants import DEFAULT_SEASON_TYPE

LOGGER = logging.getLogger(__name__)


def fetch_player_gamelog(
    player_id: int,
    season: str,
    season_type: str = DEFAULT_SEASON_TYPE,
    **request_kwargs: Any,
) -> pd.DataFrame:
    """Fetch player game logs as a :class:`~pandas.DataFrame`.

    Parameters
    ----------
    player_id:
        Numeric NBA player identifier.
    season:
        NBA season string (e.g., ``"2023-24"``).
    season_type:
        Season type accepted by :class:`~nba_api.stats.library.parameters.SeasonTypeAllStar`.
    **request_kwargs:
        Additional keyword arguments passed to :class:`~nba_api.stats.endpoints.playergamelog.PlayerGameLog`.
    """

    _validate_season_type(season_type)
    LOGGER.info(
        "Fetching player game log", extra={"player_id": player_id, "season": season, "season_type": season_type}
    )

    endpoint = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star=season_type,
        **request_kwargs,
    )
    data_frames = endpoint.get_data_frames()
    if not data_frames:
        raise RuntimeError("playergamelog endpoint returned no data frames")
    return data_frames[0]


def _validate_season_type(season_type: str) -> None:
    """Validate that ``season_type`` is supported by the API."""

    valid = {choice.value for choice in SeasonTypeAllStar}
    if season_type not in valid:
        raise ValueError(f"Invalid season_type '{season_type}'. Expected one of: {sorted(valid)}")


__all__ = ["fetch_player_gamelog"]
