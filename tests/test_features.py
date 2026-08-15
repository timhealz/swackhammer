import pandas as pd

from swackhammer.features import ensure_percentages, weighted_scores, zscores
from swackhammer.models import CATEGORY_ORDER


def test_ensure_percentages_builds_fields():
    df = pd.DataFrame(
        [
            {"Player": "A", "FGM": 5, "FGA": 10, "FTM": 4, "FTA": 5},
            {"Player": "B", "FGM": 3, "FGA": 6, "FTM": 1, "FTA": 2},
        ]
    )
    result = ensure_percentages(df)
    assert "FG%" in result.columns
    assert "FT%" in result.columns


def test_zscores_handles_punt_categories():
    df = pd.DataFrame(
        [
            {"PTS": 10, "TO": 3},
            {"PTS": 20, "TO": 4},
            {"PTS": 15, "TO": 1},
        ]
    )
    z = zscores(df, punt=["TO"])
    assert (z["TO"] == 0).all()
    assert "PTS" in z.columns


def test_weighted_scores_sums_rows():
    df = pd.DataFrame(
        [
            {cat: 1.0 for cat in CATEGORY_ORDER},
            {cat: 0.5 for cat in CATEGORY_ORDER},
        ]
    )
    scores = weighted_scores(df)
    assert scores.iloc[0] > scores.iloc[1]
