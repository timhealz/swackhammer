"""Feature engineering helpers for category scoring."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

from .models import CATEGORY_ORDER


def ensure_percentages(frame: pd.DataFrame) -> pd.DataFrame:
    """Ensure FG% and FT% columns are present if volume stats exist."""

    df = frame.copy()
    if "FG%" not in df.columns and {"FGM", "FGA"}.issubset(df.columns):
        with np.errstate(divide="ignore", invalid="ignore"):
            df["FG%"] = np.where(df["FGA"] == 0, 0.0, df["FGM"] / df["FGA"])
    if "FT%" not in df.columns and {"FTM", "FTA"}.issubset(df.columns):
        with np.errstate(divide="ignore", invalid="ignore"):
            df["FT%"] = np.where(df["FTA"] == 0, 0.0, df["FTM"] / df["FTA"])
    return df


def zscores(
    frame: pd.DataFrame,
    punt: Sequence[str] | None = None,
    weights: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """Compute weighted z-scores for each category."""

    if frame.empty:
        return pd.DataFrame(columns=CATEGORY_ORDER)

    punt_set = set(punt or [])
    weight_map: Dict[str, float] = {
        cat: (0.0 if cat in punt_set else 1.0) for cat in CATEGORY_ORDER
    }
    if weights:
        weight_map.update(weights)

    df = ensure_percentages(frame)
    result = pd.DataFrame(index=df.index, columns=CATEGORY_ORDER, dtype=float)

    for cat in CATEGORY_ORDER:
        if cat not in df.columns:
            result[cat] = 0.0
            continue
        if cat in punt_set:
            result[cat] = 0.0
            continue

        values = df[cat]
        if cat == "TO":
            values = -values

        mean = float(values.mean())
        std = float(values.std(ddof=0))
        if std == 0.0:
            z = pd.Series(0.0, index=df.index)
        else:
            z = (values - mean) / std
        result[cat] = z * weight_map.get(cat, 1.0)

    return result.fillna(0.0)


def weighted_scores(zscore_frame: pd.DataFrame) -> pd.Series:
    if zscore_frame.empty:
        return pd.Series(dtype=float)
    return zscore_frame.sum(axis=1)


__all__ = ["CATEGORY_ORDER", "ensure_percentages", "zscores", "weighted_scores"]
