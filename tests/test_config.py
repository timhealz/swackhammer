import pytest

from swackhammer.config import PipelineConfig


def test_default_season(monkeypatch):
    monkeypatch.delenv("SEASON", raising=False)
    monkeypatch.setenv("PLAYER_ID", "201939")
    monkeypatch.setenv("S3_BUCKET", "bucket")
    config = PipelineConfig()
    config.validate()
    assert config.season.count("-") == 1


def test_validation_missing_bucket(monkeypatch):
    monkeypatch.setenv("PLAYER_ID", "201939")
    monkeypatch.setenv("SEASON", "2023-24")
    monkeypatch.delenv("S3_BUCKET", raising=False)
    config = PipelineConfig()
    with pytest.raises(ValueError):
        config.validate()


def test_validation_missing_player(monkeypatch):
    monkeypatch.delenv("PLAYER_ID", raising=False)
    monkeypatch.setenv("SEASON", "2023-24")
    monkeypatch.setenv("S3_BUCKET", "bucket")
    config = PipelineConfig()
    with pytest.raises(ValueError):
        config.validate()
