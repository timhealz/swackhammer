"""Configuration helpers for Swackhammer."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Iterable, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, Field, ValidationError

# Load environment variables from a .env file if present.
load_dotenv()


class Settings(BaseSettings):
    """Application settings populated from the environment."""

    league_id: Optional[int] = Field(default=None, env="LEAGUE_ID")
    season_id: int = Field(default=2025, env="SEASON_ID")
    espn_s2: Optional[str] = Field(default=None, env="ESPN_S2")
    swid: Optional[str] = Field(default=None, env="SWID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def required_fields(self) -> List[str]:
        """Return the names of required fields that are missing values."""
        required = {"league_id", "espn_s2", "swid"}
        return [field for field in required if getattr(self, field) in (None, "")]

    def validate_required(self) -> None:
        """Raise a ``ValidationError`` if required settings are missing."""
        missing = self.required_fields()
        if missing:
            raise ValidationError(
                [
                    {
                        "loc": (name,),
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                    for name in missing
                ],
                Settings,
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance."""

    return Settings()  # type: ignore[arg-type]


settings = get_settings()


class CategoryWeights(BaseModel):
    """User supplied weights for nine-category scoring."""

    weights: Dict[str, float] = Field(default_factory=dict)

    def as_dict(self, categories: Iterable[str]) -> Dict[str, float]:
        return {cat: self.weights.get(cat, 1.0) for cat in categories}


__all__ = ["Settings", "settings", "get_settings", "CategoryWeights"]
