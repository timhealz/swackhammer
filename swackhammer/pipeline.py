"""Orchestration helpers for the Swackhammer batch workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import PurePosixPath

from .config import PipelineConfig
from .nba_client import fetch_player_gamelog
from .storage import (
    S3Location,
    dataframe_to_table,
    reorder_columns,
    upload_buffer_to_s3,
    write_parquet_to_buffer,
)

LOGGER = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Result metadata produced by :class:`PlayerGameLogPipeline`."""

    location: S3Location
    row_count: int


class PlayerGameLogPipeline:
    """End-to-end orchestration for downloading and storing player game logs."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.config.validate()

    def run(self) -> PipelineResult:
        """Execute the pipeline and return metadata about the stored object."""

        LOGGER.info("Starting pipeline", extra={"config": self.config})
        frame = fetch_player_gamelog(
            player_id=self.config.player_id,
            season=self.config.season,
            season_type=self.config.season_type,
        )
        LOGGER.info("Fetched frame", extra={"rows": len(frame)})

        ordered = reorder_columns(frame)
        table = dataframe_to_table(ordered)
        buffer = write_parquet_to_buffer(table)

        location = self._build_s3_location()
        upload_buffer_to_s3(
            buffer,
            location,
            aws_region=self.config.aws_region,
            profile_name=self.config.profile_name,
        )

        return PipelineResult(location=location, row_count=table.num_rows)

    def _build_s3_location(self) -> S3Location:
        now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        prefix = PurePosixPath(self.config.s3_prefix)
        key = prefix.joinpath(
            f"player_id={self.config.player_id}",
            f"season={self.config.season}",
            f"season_type={self.config.season_type.replace(' ', '_')}",
            f"extracted_at={now}",
            self.config.parquet_filename,
        ).as_posix()
        return S3Location(bucket=self.config.s3_bucket, key=key)


def main() -> None:
    """Entry point for the ``swackhammer-run`` console script."""

    logging.basicConfig(level=logging.INFO)
    config = PipelineConfig()
    pipeline = PlayerGameLogPipeline(config)
    result = pipeline.run()
    LOGGER.info("Pipeline completed", extra={"row_count": result.row_count, "uri": result.location.uri()})


__all__ = ["PlayerGameLogPipeline", "PipelineResult", "main"]
