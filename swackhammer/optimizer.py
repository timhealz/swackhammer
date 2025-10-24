"""Roster optimization utilities."""

from __future__ import annotations

from typing import Mapping, Sequence

import pandas as pd
import pulp

from .features import CATEGORY_ORDER


def _score_row(row: pd.Series, weights: Mapping[str, float]) -> float:
    total = 0.0
    for cat in CATEGORY_ORDER:
        weight = weights.get(cat, 0.0)
        if weight == 0.0:
            continue
        if cat not in row:
            continue
        value = row[cat]
        if cat == "TO":
            value = -value
        total += weight * float(value)
    return total


def optimize_pool(
    pool: pd.DataFrame,
    roster_size: int,
    punt: Sequence[str] | None = None,
    weights: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """Select the best ``roster_size`` players maximizing weighted score."""

    if pool.empty or roster_size <= 0:
        return pd.DataFrame(columns=list(pool.columns) + ["score"])

    punt_set = set(punt or [])
    weight_map = {cat: (0.0 if cat in punt_set else 1.0) for cat in CATEGORY_ORDER}
    if weights:
        weight_map.update(weights)

    scores = pool.apply(lambda row: _score_row(row, weight_map), axis=1)
    pool_with_scores = pool.copy()
    pool_with_scores["score"] = scores

    prob = pulp.LpProblem("swackhammer_roster", pulp.LpMaximize)
    decision_vars = {
        idx: pulp.LpVariable(f"player_{i}", cat="Binary")
        for i, idx in enumerate(pool_with_scores.index)
    }

    prob += pulp.lpSum(decision_vars[idx] * pool_with_scores.loc[idx, "score"] for idx in pool_with_scores.index)
    prob += pulp.lpSum(decision_vars.values()) == roster_size

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    chosen_indices = [idx for idx, var in decision_vars.items() if var.value() == 1.0]

    return pool_with_scores.loc[chosen_indices].sort_values("score", ascending=False)


__all__ = ["optimize_pool"]
