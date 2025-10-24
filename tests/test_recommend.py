import pandas as pd

from swackhammer.recommend import replacement_value


def test_replacement_value_returns_sorted_moves():
    roster = pd.DataFrame(
        [
            {"Player": "A", "PTS": 10, "REB": 5, "TO": 3},
            {"Player": "B", "PTS": 12, "REB": 4, "TO": 2},
        ]
    )
    free_agents = pd.DataFrame(
        [
            {"Player": "C", "PTS": 20, "REB": 7, "TO": 3},
            {"Player": "D", "PTS": 8, "REB": 3, "TO": 1},
        ]
    )
    suggestions = replacement_value(roster, free_agents, punt=["TO"], limit=2)
    assert list(suggestions.columns) == ["add", "drop", "delta"]
    assert suggestions.iloc[0]["add"] == "C"
