# Sources

`config/sources.yaml` documents the public sources used by the project. The runtime collector still uses `src/config/sources.py` so the two-hour update path remains unchanged.

For each source, track:

- `id`
- `url`
- `format`
- `parser`
- `enabled`
- `timeout_seconds`
- `max_bytes`
- `license`
- `contact`
- `last_reviewed`

## Operational rules

- A failing source should be logged and skipped, not allowed to stop the whole pipeline.
- If all sources fail, the pipeline should report a serious failure.
- Source licenses and redistribution permissions should be reviewed before presenting sources as official or trusted.
