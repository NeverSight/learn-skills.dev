---
name: creating-taps
description: Creates, runs, and validates Hotglue Singer taps. Use when scaffolding a tap, implementing connector extraction, or debugging tap discovery and sync output.
---

# Creating Singer Taps

## Scaffold a tap

```bash
cookiecutter https://github.com/hotgluexyz/hotglue-tap-cookiecutter.git
cd tap-<service>
uv venv --python 3.10 --seed .venv
uv pip install --python .venv/bin/python -e .
```

Read the generated `README.md` and `AGENTS.md`. If the user may already have a connector for this source, confirm with them before scaffolding a new tap.

Use a dedicated tap venv (not a target or ETL venv). Match deployed Python and package pins when reproducing a job.

## Run locally

Keep credentials, catalogs, Singer output, and state in git-ignored `.secrets/`:

```bash
mkdir -p .secrets && cd .secrets
../.venv/bin/tap-<service> --config config.json --discover > catalog.json
../.venv/bin/singer-discover --input catalog.json --output catalog-selected.json
../.venv/bin/tap-<service> --config config.json --catalog catalog-selected.json > data.singer
```

Install catalog selection when needed:

```bash
../.venv/bin/python -m pip install https://github.com/hotgluexyz/singer-discover/archive/master.zip
```

Validate outputs, not just exit codes: parse `catalog.json` and `catalog-selected.json`; inspect `data.singer` as JSONL (`SCHEMA`, `RECORD`, `STATE`). Confirm stream names, keys, replication settings, and that schema includes fields you need downstream.

Use the Hotglue Docs MCP for connector and platform behavior.
