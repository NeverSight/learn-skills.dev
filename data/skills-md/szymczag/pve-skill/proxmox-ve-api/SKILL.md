---
name: proxmox-ve-api
description: Use when you need to fetch the current Proxmox VE API docs from the public `apidoc.js`, extract `docs.json`, query endpoints efficiently with `jq`, find methods by path or internal name, or inspect only selected parameters or return schemas without loading the whole API tree into context.
metadata:
  author: "Maciej Szymczak <maciej@szymczak.at>"
---

# Proxmox VE API

Use this skill when the user needs current Proxmox VE API documentation in a form that is efficient for agents and cheap to query.

## Version Provenance

The bundled snapshot is generated from the unversioned Proxmox VE docs stream at `https://pve.proxmox.com/pve-docs/api-viewer/apidoc.js`.
The current local payload matches upstream as of 2026-05-01 and corresponds to Proxmox VE documentation version 9.1.2, last updated Fri Dec 12 13:18:26 UTC 2025.

This skill is centered around:

- `scripts/refresh_proxmox_ve_api.py`: fetch latest `apidoc.js` from Proxmox and generate fresh artifacts
- `scripts/extract_api_schema.py`: extractor from `apidoc.js`
- `references/proxmox-ve-apidocs.md`: query patterns and `jq` cookbook
- `data/source-metadata.json`: freshness metadata for the current local snapshot, if already fetched
- `data/docs.json`: extracted Proxmox API tree, if already fetched

## Workflow

Do not read the whole `docs.json` into context by default.

Preferred workflow:

1. Check whether `data/source-metadata.json` exists and whether the snapshot is fresh enough for the user's request.
2. If latest docs matter or no snapshot exists, refresh first:

```bash
python3 scripts/refresh_proxmox_ve_api.py
```

3. Read [references/proxmox-ve-apidocs.md](references/proxmox-ve-apidocs.md) for the ready-made query patterns.
4. Prefer `python3 scripts/query_proxmox_ve_api.py ...` for deterministic lookups.
5. Use `jq` only as a fallback when you need a custom one-off slice.
6. Narrow to one exact `path` plus HTTP method.
7. Fetch only the needed subfield:
   - `.info[$method]`
   - `.info[$method].parameters.properties`
   - `.info[$method].parameters.properties[$param]`
   - `.info[$method].returns`
   - `.info[$method].permissions`

## Regeneration

To fetch the latest public snapshot from Proxmox and extract fresh local artifacts:

```bash
python3 scripts/refresh_proxmox_ve_api.py
```

For offline work from an already downloaded local `apidoc.js` file:

```bash
python3 scripts/refresh_proxmox_ve_api.py --source-file data/apidoc.js
```

If the user only needs raw extraction from a local file:

```bash
python3 scripts/extract_api_schema.py data/apidoc.js --json-out data/docs.json --stats
```

If the user wants Markdown endpoint dumps:

```bash
python3 scripts/extract_api_schema.py data/apidoc.js --markdown-dir markdown
```

## Notes

- Proxmox method `name` values are not globally unique, so do not rely on `name` alone.
- `data/operations.jsonl` is the cheapest search index; `data/docs.json` is the source of truth for exact details.
- Use `path` plus HTTP method for final disambiguation.
- If refresh is impossible, state explicitly that the answer is based on the snapshot date in `data/source-metadata.json`.
- Treat [references/proxmox-ve-apidocs.md](references/proxmox-ve-apidocs.md) as the main reference file; it contains tested `jq` examples against this repo's schema shape.
