# Swackhammer

Swackhammer is a Python toolkit for fantasy basketball managers who punt select
categories. It combines ESPN league data with NBA per-game statistics to help
you evaluate free agents, identify profitable add/drop swaps, and assemble
optimized rosters that align with your build.

## Features

- Typed configuration loaded from environment variables or a `.env` file.
- Lightweight ESPN client helpers for fetching rosters, teams, and free agents.
- Cached NBA stats lookups using the `nba_api` package.
- Category-aware scoring utilities for nine-category leagues with punt
  adjustments.
- Replacement-value based add/drop recommendations.
- Linear-programming roster optimizer with optional punt weights.
- Typer-based CLI for quick access to roster insights.

## Getting started

1. Install the package and its dependencies:

   ```bash
   pip install -e .[dev]
   ```

2. Create a `.env` file in the project root that contains your ESPN cookies and
   league identifiers:

   ```text
   LEAGUE_ID=123456
   SEASON_ID=2025
   ESPN_S2=your_espn_s2_cookie
   SWID={XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
   ```

3. Run the CLI to inspect free agents or generate recommendations:

   ```bash
   swackhammer free-agents --limit 25
   swackhammer recommend --punt-ft --punt-to --limit 100
   ```

   The CLI prints a ranked table of suggested add/drop pairs that maximize your
   weighted category score.

## Development

Run the unit tests to validate local changes:

```bash
pytest
```
