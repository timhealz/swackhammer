"""Configuration helpers for the Swackhammer pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Fetch an environment variable, returning ``default`` when unset."""

    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


@dataclass(frozen=True)
class PipelineConfig:
    """Configuration for the player game log extraction pipeline.

    Parameters are resolved from environment variables when not provided
    explicitly. All values map to options exposed by ``nba_api`` or the
    pipeline's storage layer.
    """

    player_id: int = field(default_factory=lambda: int(_env("PLAYER_ID", "0")))
    season: str = field(default_factory=lambda: _env("SEASON", _default_season()))
    season_type: str = field(
        default_factory=lambda: _env("SEASON_TYPE", "Regular Season")
    )
    s3_bucket: str = field(default_factory=lambda: _env("S3_BUCKET", ""))
    s3_prefix: str = field(default_factory=lambda: _env("S3_PREFIX", "nba/player_gamelog"))
    parquet_filename: str = field(
        default_factory=lambda: _env("PARQUET_FILENAME", "playergamelog.parquet")
    )
    aws_region: Optional[str] = field(default_factory=lambda: _env("AWS_REGION"))
    profile_name: Optional[str] = field(default_factory=lambda: _env("AWS_PROFILE"))

    def validate(self) -> None:
        """Validate the configuration, raising ``ValueError`` if invalid."""

        if not self.player_id:
            raise ValueError("player_id must be provided")
        if not self.season:
            raise ValueError("season must be provided (e.g., '2023-24')")
        if not self.s3_bucket:
            raise ValueError("s3_bucket must be provided")


def _default_season() -> str:
    """Return the most recent NBA season string (e.g., ``'2023-24'``)."""

    now = datetime.utcnow()
    year = now.year if now.month >= 8 else now.year - 1
    return f"{year}-{str(year + 1)[-2:]}"


__all__ = ["PipelineConfig"]
