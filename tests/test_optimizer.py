import pandas as pd

from swackhammer.optimizer import optimize_pool


def test_optimize_pool_selects_top_scores():
    pool = pd.DataFrame(
        [
            {"Player": "A", "PTS": 15, "REB": 5, "TO": 2},
            {"Player": "B", "PTS": 12, "REB": 8, "TO": 1},
            {"Player": "C", "PTS": 5, "REB": 2, "TO": 3},
        ]
    )
    result = optimize_pool(pool, roster_size=2, punt=["TO"])
    assert len(result) == 2
    assert set(result["Player"]) == {"A", "B"}
