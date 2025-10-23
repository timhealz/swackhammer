from unittest import mock

import pandas as pd

from swackhammer.config import PipelineConfig
from swackhammer.constants import PLAYER_GAMELOG_SCHEMA
from swackhammer.pipeline import PlayerGameLogPipeline


@mock.patch("swackhammer.pipeline.upload_buffer_to_s3")
@mock.patch("swackhammer.pipeline.write_parquet_to_buffer")
@mock.patch("swackhammer.pipeline.dataframe_to_table")
@mock.patch("swackhammer.pipeline.reorder_columns")
@mock.patch("swackhammer.pipeline.fetch_player_gamelog")
def test_pipeline_happy_path(fetch_mock, reorder_mock, table_mock, buffer_mock, upload_mock):
    frame = pd.DataFrame({col: [1] for col in PLAYER_GAMELOG_SCHEMA})
    fetch_mock.return_value = frame
    reorder_mock.return_value = frame
    table_mock.return_value = mock.Mock(num_rows=1)
    buffer_mock.return_value = mock.Mock()

    config = PipelineConfig(
        player_id=201939,
        season="2023-24",
        season_type="Regular Season",
        s3_bucket="bucket",
        s3_prefix="prefix",
    )
    pipeline = PlayerGameLogPipeline(config)
    result = pipeline.run()

    fetch_mock.assert_called_once()
    reorder_mock.assert_called_once()
    table_mock.assert_called_once()
    buffer_mock.assert_called_once()
    upload_mock.assert_called_once()
    assert result.row_count == 1
    assert result.location.bucket == "bucket"
    assert result.location.key.endswith("playergamelog.parquet")
