---
name: orizu-cli
description: Operate and troubleshoot the Orizu CLI for authentication and workspace operations. Use when Codex must run or explain `orizu` commands for login/logout/whoami, team and member management, project/app lifecycle, dataset upload (`csv`/`json`/`jsonl`), and task lifecycle (create/assign/status/export), including interactive selection fallbacks and non-interactive flag requirements.
---

# Orizu CLI

## Overview

Execute end-to-end Orizu workflows from the terminal using the `orizu` CLI.
Prefer explicit flags in automation and CI; use interactive prompts only in TTY sessions.

## Prerequisites

- Ensure Node.js 20+ is installed.
- Ensure Orizu API is running (`http://localhost:3000` by default) or set `ORIZU_BASE_URL`.
- Build CLI from source when needed:
  ```bash
  bun install
  bun x tsc -p packages/cli/tsconfig.json
  node packages/cli/dist/index.js --help
  ```
- Use `orizu` directly when globally installed; otherwise run `node packages/cli/dist/index.js ...`.

## Core Workflow

1. Authenticate:
   ```bash
   orizu login
   orizu whoami
   ```
2. Set up workspace:
   ```bash
   orizu teams create --name "Ops Eval"
   orizu projects create --name "Support QA" --team ops-eval
   ```
3. Upload dataset:
   ```bash
   orizu datasets upload --project ops-eval/support-qa --file ./datasets/support.jsonl --name "Support Batch 1"
   ```
4. Create or update app from file (dataset is required):
   ```bash
   orizu apps create \
     --project ops-eval/support-qa \
     --name "Support Labeler" \
     --dataset <datasetId> \
     --file ./apps/SupportLabeler.tsx \
     --input-schema ./schemas/support-input.json \
     --output-schema ./schemas/support-output.json
   ```
5. Optionally link a different dataset to an existing app version:
   ```bash
   orizu apps link-dataset --app <appId> --dataset <datasetId>
   ```
6. Run task lifecycle (task create requires assignees and creates assignments immediately):
   ```bash
   orizu tasks create --project ops-eval/support-qa --dataset <datasetId> --app <appId> --title "Support QA Round 1" --assignees <userId1,userId2>
   orizu tasks status --task <taskId>
   orizu tasks export --task <taskId> --format csv --out ./support-round1.csv
   ```

## Interactive vs Non-Interactive

- Use interactive fallback only when running in a TTY and flags are omitted.
- Provide explicit identifiers in scripts/CI:
  - `--team`, `--project`, `--app`, `--task`, `--dataset`, `--assignees`.
- For `tasks assign`, pass user IDs (comma-separated), not emails.
- Export defaults:
  - `--format` defaults to `jsonl`.
  - output defaults to `<taskId>.<format>`.

## Auth and Error Handling

- On auth failure, run `orizu login` and confirm with `orizu whoami`.
- Login requires localhost callback availability on `127.0.0.1:43123`.
- Credentials are stored in `~/.config/orizu/credentials.json`.
- In non-interactive contexts, avoid prompt-dependent commands; pass required flags explicitly.

## Command Coverage

- Auth: `login`, `logout`, `whoami`
- Teams: list/create, members list/add/remove/role
- Projects: list/create
- Apps: list/create/update/link-dataset
- Datasets: upload (`.csv`, `.json`, `.jsonl`)
- Tasks: list/create/assign/status/export

## References

- Read `references/cli-reference.md` for complete command examples and end-to-end flows.
- Read `docs/cli.md` for the authoritative project-local CLI guide when working in this repository.
