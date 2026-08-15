import os

import pytest

from swackhammer.config import Settings, get_settings


def test_settings_load_from_env(monkeypatch):
    monkeypatch.setenv("LEAGUE_ID", "12345")
    monkeypatch.setenv("SEASON_ID", "2026")
    monkeypatch.setenv("ESPN_S2", "cookie")
    monkeypatch.setenv("SWID", "{abcd}")

    settings = Settings()
    assert settings.league_id == 12345
    assert settings.season_id == 2026
    assert settings.espn_s2 == "cookie"
    assert settings.swid == "{abcd}"


def test_validate_required_missing():
    settings = Settings()
    with pytest.raises(Exception):
        settings.validate_required()
