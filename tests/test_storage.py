import io

import pandas as pd
import pyarrow as pa
import pytest

from swackhammer.constants import PLAYER_GAMELOG_SCHEMA
from swackhammer.storage import (
    S3Location,
    dataframe_to_table,
    reorder_columns,
    write_parquet_to_buffer,
)


def _sample_frame():
    data = {col: [1] for col in PLAYER_GAMELOG_SCHEMA}
    data["MATCHUP"] = ["GSW @ LAL"]
    data["GAME_DATE"] = ["2024-01-01"]
    return pd.DataFrame(data)


def test_reorder_columns_success():
    frame = _sample_frame()
    reordered = reorder_columns(frame)
    assert list(reordered.columns) == PLAYER_GAMELOG_SCHEMA


def test_reorder_columns_missing():
    frame = _sample_frame().drop(columns=["FGM"])
    with pytest.raises(KeyError):
        reorder_columns(frame)


def test_write_parquet_roundtrip():
    frame = _sample_frame()
    table = dataframe_to_table(frame)
    buffer = write_parquet_to_buffer(table)
    reader = pa.ipc.open_file(buffer)
    assert reader.schema == table.schema
    assert reader.num_rows == table.num_rows


def test_s3_location_uri():
    loc = S3Location(bucket="bucket", key="path/file.parquet")
    assert loc.uri() == "s3://bucket/path/file.parquet"
