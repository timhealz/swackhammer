"""Swackhammer fantasy basketball assistant."""

from .config import Settings, get_settings, settings
from .features import CATEGORY_ORDER, weighted_scores, zscores
from .optimizer import optimize_pool
from .recommend import replacement_value

__all__ = [
    "Settings",
    "settings",
    "get_settings",
    "CATEGORY_ORDER",
    "zscores",
    "weighted_scores",
    "replacement_value",
    "optimize_pool",
]

__version__ = "0.2.0"
