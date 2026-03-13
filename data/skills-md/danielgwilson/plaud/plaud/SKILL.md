---
name: plaud
description: Use this skill whenever you need to list/search/download/export Plaud files (audio, transcripts, AI summaries), manage tags/speakers, or trash/restore items from app.plaud.ai using the plaud CLI (agent-first, JSON-friendly).
---

# Plaud (agent-first CLI)

Use this skill to pull content out of Plaud in a way that’s reliable for agents: small defaults, stable `--json` envelopes, and explicit paging/filters.

## Default workflow (read-only)

- Sanity check: `plaud doctor --json`
- Browse recent files: `plaud files list --limit 25` (table) or `plaud files list --json --limit 25`
- Drill in: `plaud files get <id> --json`
- Pull content: `plaud files download <id> --out ./plaud-out --what transcript,summary,json`

## Common tasks

- Download audio: `plaud files download <id> --out ./plaud-out --what audio --audio-format opus`
- Export everything: `plaud files export --zip`
- Trash / restore: `plaud files trash <id>` and `plaud files restore <id>`
- Tags: `plaud files tags list --json`, `plaud files tags add <tagId> <id>`, `plaud files tags clear <id>`
- Speaker labels (per recording): `plaud files speakers list <id> --json` and `plaud files speakers rename <id> --from "Speaker 2" --to "Person A"`
- Re-run transcript/summary: `plaud files rerun <id> --wait`

## Paging and filtering (agent ergonomics)

- Prefer filters over “dump everything”:
  - Last N: `plaud files list --json --last 30d --limit 50`
  - Date range: `plaud files list --json --from 2026-02-01 --to 2026-03-01 --limit 50`
- Page forward: `plaud files list --json --skip 50 --limit 50`
- If results change during paging, anchor with `--to` (or use a narrower range) and retry.

## Auth (only when needed)

If `plaud doctor --json` indicates missing auth:

- Best UX (interactive): `plaud auth login` (opens a browser, captures token, closes when done)
- Headless/remote:
  - Copy `~/.config/plaud/config.json` from a trusted machine, or
  - `plaud auth set --stdin` (paste token via stdin), or
  - `PLAUD_AUTH_TOKEN=... plaud doctor --json` (ephemeral; avoid saving)
- HAR import exists (`plaud auth import-har ...`) but is a last resort (HARs often contain sensitive data).

## Hard constraints (security)

- Never print/paste full tokens or HAR contents into chat/logs.
- Never pass tokens via CLI flags (use login/stdin/config/env).
- Prefer `--json` outputs; treat non-JSON text as human-only.

## JSON contract (for tool use)

- Stable machine-readable behavior is documented in `docs/CONTRACT_V1.md`.
