"""Typed models for player metadata and category lines."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

CATEGORY_ORDER = [
    "PTS",
    "REB",
    "AST",
    "3PM",
    "STL",
    "BLK",
    "FG%",
    "FT%",
    "TO",
]

VOLUME_FIELDS = {"FGM", "FGA", "FTM", "FTA"}


class PlayerCategoryLine(BaseModel):
    """Per-game statistics in the nine standard categories."""

    PTS: float = 0.0
    REB: float = 0.0
    AST: float = 0.0
    _3PM: float = Field(default=0.0, alias="3PM")
    STL: float = 0.0
    BLK: float = 0.0
    FGM: float = 0.0
    FGA: float = 0.0
    FTM: float = 0.0
    FTA: float = 0.0
    TO: float = 0.0

    class Config:
        allow_population_by_field_name = True

    def to_category_map(self) -> Dict[str, float]:
        fg_pct = (self.FGM / self.FGA) if self.FGA else 0.0
        ft_pct = (self.FTM / self.FTA) if self.FTA else 0.0
        return {
            "PTS": self.PTS,
            "REB": self.REB,
            "AST": self.AST,
            "3PM": self._3PM,
            "STL": self.STL,
            "BLK": self.BLK,
            "FG%": fg_pct,
            "FT%": ft_pct,
            "TO": self.TO,
        }


class PlayerInfo(BaseModel):
    """Basic metadata about a player across providers."""

    player_id: int
    name: str
    positions: List[str]
    team: Optional[str] = None
    espn_id: Optional[int] = None
    nba_id: Optional[int] = None
    per_game: Optional[PlayerCategoryLine] = None

    def per_game_categories(self) -> Dict[str, float]:
        if not self.per_game:
            return {cat: 0.0 for cat in CATEGORY_ORDER}
        return self.per_game.to_category_map()


__all__ = ["CATEGORY_ORDER", "VOLUME_FIELDS", "PlayerCategoryLine", "PlayerInfo"]
