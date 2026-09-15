---
name: arize-phoenix-migration
description: Migrate existing Phoenix (PX) project traces into Arize AX, preserving historical IDs and timestamps and verifying the imported spans. Use when users ask to move or copy Phoenix traces to AX; not for adding live instrumentation or exporting AX traces alone.
metadata:
  author: arize
  version: "1.0"
---

# Phoenix to AX migration

Help the user migrate a Phoenix project to AX using the bundled helper. Handle setup and commands yourself; the user should only need to supply their source and destination details.

Requires Python 3.10 or later, shell access, and network access to Phoenix and AX. No particular coding agent, ax CLI, or AX Phoenix connector is required.

## Gather missing details

Reuse details from the request and configured environment. Ask only for missing information:

- Phoenix host URL and source project name.
- Phoenix API key if that instance requires authentication.
- AX API key, destination space ID, and destination project name.

Explain how to configure missing credentials locally in environment variables or a Git-ignored `.env`. Never echo credentials, place them in command arguments, or copy them to reports. Prefer a user-created existing `.env` and request its path. Never embed literal keys in displayed tool requests or generated shell/Python commands, including heredocs; writing to a file without stdout still exposes command contents. Avoid patch/edit tools that echo secret values. If your available tools cannot write secrets without displaying them, ask the user to configure the local file themselves. Keep the file owner-only (for example, `chmod 600` on Unix). Load an explicitly chosen environment file through the helper; do not print or source its contents. See [configuration and migration details](references/migration.md) for variable names and examples.

If the user only supplies a space name, optionally use an already configured ax CLI for discovery: `ax spaces list -o json` or `ax spaces get "<space-name>" -o json`. Run `ax spaces --help` if command syntax differs. Reuse the user's configured CLI authentication; never put keys in CLI arguments. Without the CLI, resolve the name through AX APIs. Ask the user to choose if multiple spaces match. Use a fresh destination project; suggest a source-derived name when none is specified and establish that destination with the user. Do not ask about the separate AX button, feature flags, or browser tokens.

## Set expectations and wait for continue

Before starting setup or migration commands, explain that setup, export, upload, and AX indexing/readback can take several minutes. Verification may wait up to 15 minutes for indexing, and readback or larger projects can take longer; do not promise a fixed completion time.

For example: "This migration may take a few minutes. After upload, AX indexing and verification can take 15 minutes or longer. I'll verify the traces before reporting success. Continue?"

Wait for the user's continue before starting. A request to migrate alone does not acknowledge the expected wait. If the user has already acknowledged it and said to continue, or explicitly requested execution without pausing, proceed. Ask once for the migration, not again for each stage. A read-only planning request needs no migration confirmation.

## Run the migration

Locate this installed skill's root and run its bundled commands by absolute path, so they work from any workspace. Check the chosen interpreter is Python 3.10 or later before creating an isolated environment or installing the [helper dependencies](scripts/requirements.txt). Use an available compatible interpreter if the default is older.

1. Run `scripts/migrate.py preflight` with the user's local configuration and chosen destination. Present a short source/destination summary. Missing configuration returns `needs_input`; ask for those fields. A dry-run or planning request stops here without uploading.
2. Run `scripts/migrate.py export --manifest <local-path>` to export every page under a fixed snapshot boundary. For selected complete traces, repeat `--trace-id` for each trace ID. Export does not change Phoenix or AX.
3. Run `scripts/migrate.py import --manifest <local-path>` when the user's request authorizes migration to the resolved destination. It refuses an existing destination on the first import. Keep the original manifest for resuming the same migration.
4. Run `scripts/migrate.py verify --manifest <local-path>`. For an empty snapshot, report `empty`: no spans were uploaded and no destination was created. For nonempty snapshots, only `verified` establishes success. Otherwise report uploaded-but-unverified with counts, differing field names, and the command for rerunning verification.

Use `--env-file <path>` on each command when the user has configured a local file. Use `--project <name>` to set the destination without modifying their environment. See the [migration reference](references/migration.md) for resume and troubleshooting.

While running, keep the user informed at stage changes and during long waits. Distinguish installing dependencies, exporting, uploading, waiting for AX indexing, and verifying readback. The verify command emits redacted progress JSON on stderr and final results on stdout. Report available elapsed time and found/expected counts; partial counts describe completed readback windows, not total indexed spans. If there is no new progress, do not invent counts or imply verified success. Do not retry uploads just because verification is slow.

## Preserve and report

Preserve original span/trace IDs, parents, historical timestamps, span kinds, input/output, sessions, token counts, and attributes. The helper also stores original attributes, events, and timestamp strings in AX metadata for preservation checks. It reports AX REST timestamp readback differences up to 128 ns separately and requires exact original timestamp preservation in metadata. It does not migrate Phoenix datasets, prompts, experiments, evaluations, or annotations.

Do not change historical timestamps to make traces appear in a recent-time UI filter. Do not label a successful upload as a verified migration. The helper does not guarantee server-side ingestion idempotency: reconcile uncertain submissions through readback rather than blindly retrying them.

Summarize source and destination, exported/imported/verified counts, and any differences or unverified outcomes. Keep raw exports, manifests, and credentials local and ignored by version control. Report core fields stored in AX separately from values preserved only in metadata.
