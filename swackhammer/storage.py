"""Storage helpers for exporting NBA game logs to Amazon S3."""

from __future__ import annotations

import io
import logging
from dataclasses import dataclass
from typing import Optional

import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .constants import PLAYER_GAMELOG_SCHEMA

LOGGER = logging.getLogger(__name__)


@dataclass
class S3Location:
    """Represents an S3 object location."""

    bucket: str
    key: str

    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"


def reorder_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``frame`` ordered according to ``PLAYER_GAMELOG_SCHEMA``."""

    missing = [col for col in PLAYER_GAMELOG_SCHEMA if col not in frame.columns]
    if missing:
        raise KeyError(f"Missing expected columns: {missing}")
    reordered = frame[PLAYER_GAMELOG_SCHEMA].copy()
    LOGGER.debug("Reordered columns", extra={"columns": PLAYER_GAMELOG_SCHEMA})
    return reordered


def dataframe_to_table(frame: pd.DataFrame) -> pa.Table:
    """Convert a DataFrame to a :class:`~pyarrow.Table` with API-aligned schema."""

    return pa.Table.from_pandas(frame, preserve_index=False)


def write_parquet_to_buffer(table: pa.Table, compression: str = "snappy") -> io.BytesIO:
    """Serialize ``table`` into an in-memory Parquet buffer."""

    sink = io.BytesIO()
    pq.write_table(table, sink, compression=compression)
    sink.seek(0)
    LOGGER.debug(
        "Serialized Parquet table",
        extra={"rows": table.num_rows, "columns": table.num_columns, "compression": compression},
    )
    return sink


def upload_buffer_to_s3(
    buffer: io.BytesIO,
    location: S3Location,
    *,
    aws_region: Optional[str] = None,
    profile_name: Optional[str] = None,
) -> None:
    """Upload ``buffer`` to S3 using :mod:`boto3`."""

    session_kwargs = {}
    if profile_name:
        session_kwargs["profile_name"] = profile_name
    if aws_region:
        session_kwargs["region_name"] = aws_region

    session = boto3.Session(**session_kwargs)
    client = session.client("s3")
    client.upload_fileobj(buffer, location.bucket, location.key)
    LOGGER.info("Uploaded Parquet file", extra={"uri": location.uri()})


__all__ = [
    "S3Location",
    "reorder_columns",
    "dataframe_to_table",
    "write_parquet_to_buffer",
    "upload_buffer_to_s3",
]
