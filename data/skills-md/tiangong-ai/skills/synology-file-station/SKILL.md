---
name: synology-file-station
description: "Operate Synology DSM File Station via WebAPI for major file workflows including listing, search, folder creation, rename, copy/move, delete, upload/download, and archive extract. Use when tasks need scripted NAS file operations with service address, username, and password loaded from environment variables. Note: compress is temporarily unavailable in this skill."
---

# Synology File Station

## Core Goal
- Run major Synology File Station file operations with one CLI script.
- Read connection credentials from env instead of hardcoding secrets.
- Return JSON output suitable for automation pipelines.

## Workflow
1. Prepare env variables (see `references/env.md` and `assets/config.example.env`).
2. Validate config:

```bash
python3 scripts/synology_file_station.py check-config
```

3. Optional connection probe:

```bash
python3 scripts/synology_file_station.py check-config --probe
```

4. Run the required file operation command (see `references/commands.md`).

## Major Operations
- Read/browse: `info`, `list-shares`, `list`, `get-info`
- Search: `search-start`, `search-list`, `search-stop`, `search-clean`
- Directory/file mutation: `mkdir`, `rename`, `copy`, `move`, `delete`
- Transfer: `upload`, `download`
- Archive workflows: `extract` (`compress` is temporarily unavailable)
- Background task control: `background-list`, `task-status`, `task-stop`

## Environment Contract
Required env:
- `SYNOLOGY_BASE_URL`
- `SYNOLOGY_USERNAME`
- `SYNOLOGY_PASSWORD`

Optional env:
- `SYNOLOGY_VERIFY_SSL`
- `SYNOLOGY_TIMEOUT`
- `SYNOLOGY_SESSION`
- `SYNOLOGY_READONLY` (default `false`; set `true` to block mutation commands)
- `SYNOLOGY_MUTATION_ALLOW_PATHS` (optional mutation path allowlist)

## Output Contract
- Success: JSON object with `type=status` and operation-specific fields.
- Failure: JSON object with `type=error` and structured error metadata.
- Exit code:
  - `0`: success
  - `1`: runtime/API error
  - `2`: invalid env configuration

## References
- `references/env.md`
- `references/commands.md`

## Assets
- `assets/config.example.env`

## Scripts
- `scripts/synology_file_station.py`
