"""Add/drop recommendation helpers."""

from __future__ import annotations

from typing import Mapping, Sequence

import pandas as pd

from .features import CATEGORY_ORDER, weighted_scores, zscores


def replacement_value(
    roster: pd.DataFrame,
    free_agents: pd.DataFrame,
    punt: Sequence[str] | None = None,
    weights: Mapping[str, float] | None = None,
    limit: int = 5,
) -> pd.DataFrame:
    """Return add/drop suggestions ranked by delta in weighted score."""

    if roster.empty or free_agents.empty:
        return pd.DataFrame(columns=["add", "drop", "delta"])

    roster_scores = weighted_scores(zscores(roster, punt=punt, weights=weights))
    fa_scores = weighted_scores(zscores(free_agents, punt=punt, weights=weights))

    results = []
    for fa_idx, fa_row in free_agents.iterrows():
        fa_score = float(fa_scores.get(fa_idx, 0.0))
        add_name = fa_row.get("Player") or fa_row.get("name") or fa_idx
        for roster_idx, roster_row in roster.iterrows():
            drop_score = float(roster_scores.get(roster_idx, 0.0))
            drop_name = roster_row.get("Player") or roster_row.get("name") or roster_idx
            delta = fa_score - drop_score
            results.append({"add": add_name, "drop": drop_name, "delta": delta})

    if not results:
        return pd.DataFrame(columns=["add", "drop", "delta"])

    suggestions = pd.DataFrame(results).sort_values("delta", ascending=False)
    return suggestions.head(limit).reset_index(drop=True)


__all__ = ["replacement_value"]
