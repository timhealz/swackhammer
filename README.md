# Swackhammer

Swackhammer is a lightweight Python package for fetching NBA player game logs via the
[`nba_api`](https://github.com/swar/nba_api) client and exporting the results to
Parquet files in Amazon S3. The package is designed to be run as a scheduled batch
job (for example, in AWS Batch or AWS Lambda) that keeps a historical log of player
performance up to date.

## Features

- Thin wrapper around the `playergamelog` endpoint with sensible defaults.
- Schema-aware transformations that align the output Parquet files with the API
  response fields.
- Convenience functions for uploading the result to S3 with `boto3`.
- Configurable orchestration pipeline that can be invoked from the command line or
  programmatically.

## Quick start

```bash
pip install -e .[dev]
export PLAYER_ID=201939  # Stephen Curry
export SEASON=2023-24
export S3_BUCKET=my-data-bucket
export S3_PREFIX=nba/player_game_logs
export AWS_REGION=us-east-1
swackhammer-run
```

This command downloads the specified player's game logs, orders the columns to match
the API schema, and writes a partitioned Parquet file to
`s3://$S3_BUCKET/$S3_PREFIX/player_id=201939/season=2023-24/playergamelog.parquet`.

## Configuration

Configuration values can be supplied either through environment variables or by
instantiating `swackhammer.config.PipelineConfig` directly. Refer to the module
docstrings for the full list of options.

## Development

```bash
pip install -e .[dev]
pytest
```

