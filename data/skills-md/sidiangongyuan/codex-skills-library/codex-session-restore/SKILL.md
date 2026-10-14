---
name: codex-session-restore
description: Use when Codex Desktop sidebar sessions disappear, fail with systemError, or cannot continue after a model_provider switch. Diagnoses and repairs active, non-archived sessions without changing authentication or provider configuration.
license: MIT
compatibility: Requires Windows and local access to Codex Desktop data.
---

# Codex Session Restore

Use the bundled script first. It is dry-run by default and writes nothing unless
`--apply` is present.

## Provider Direction Rule

Set `--provider` to the provider that Codex Desktop should recognize now, not
automatically to the provider that originally created the sessions.

- If the user switched from krill/custom to official OAuth and wants old active
  sessions to appear under the current official login, use `--provider openai`.
- If the user explicitly wants to switch the environment back to krill and make
  sessions belong to krill, use `--provider krill`.
- Do not edit `config.toml`, `auth.json`, or cc-switch's current provider just
  to restore sidebar visibility. Changing current auth/provider is a separate
  user request.

## Quick Start

Resolve `<skill-dir>` to the directory containing this `SKILL.md`; do not
assume a particular global skills installation root.

Restore old krill sessions into the current official/OAuth sidebar:

```powershell
python "<skill-dir>/scripts/restore_codex_sessions.py" scan --provider openai
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-active --provider openai
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-active --provider openai --apply --yes
python "<skill-dir>/scripts/restore_codex_sessions.py" verify --provider openai
```

Repair one thread:

```bash
python "<skill-dir>/scripts/restore_codex_sessions.py" scan-thread --thread-id THREAD_ID --provider openai
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-thread --thread-id THREAD_ID --provider openai
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-thread --thread-id THREAD_ID --provider openai --apply
python "<skill-dir>/scripts/restore_codex_sessions.py" verify --thread-id THREAD_ID --provider openai
```

Use `repair-active --provider PROVIDER --apply --yes` only after a dry run
confirms the active non-archived session set is correct. Open turns newer than
30 minutes are treated as possibly active and are not closed unless
`--close-recent-open-turns` is explicitly present. Archived sessions stay
untouched unless `--include-archived` is explicitly present.

## Workflow

1. Identify the target thread id or run `scan` to find active non-archived
   threads with provider mismatch, parse errors, open turns, open child spawn
   edges, or stale goals.
2. Decide the target provider from the user's current login/config goal:
   current official OAuth means `openai`; current krill means `krill`.
3. Run `scan-thread --thread-id ID` before single-thread repair. Read
   `references/recovery-checklist.md` when the report shows multiple issue
   types or Codex Desktop still shows `systemError`.
4. Run `repair-thread --thread-id ID --provider PROVIDER` or
   `repair-active --provider PROVIDER` without `--apply` to preview actions.
5. Run the same command with `--apply` only after the preview is acceptable.
6. Run `verify --provider PROVIDER` or `verify --thread-id ID --provider PROVIDER`.
7. If available, search the live Codex thread list for a known old title to
   confirm local sessions reappeared. Otherwise fully restart Codex Desktop so
   the app server reloads thread state from disk.

## Common Provider Switch Recipes

When the user says, "I am logged in with official Codex now, but my krill
sessions disappeared," keep official OAuth as-is and migrate active session
metadata to `openai`:

```bash
python "<skill-dir>/scripts/restore_codex_sessions.py" scan --provider openai
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-active --provider openai
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-active --provider openai --apply --yes
python "<skill-dir>/scripts/restore_codex_sessions.py" verify --provider openai
```

When the user explicitly wants to use krill as the current provider, repair
active session metadata to `krill`:

```bash
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-active --provider krill
python "<skill-dir>/scripts/restore_codex_sessions.py" repair-active --provider krill --apply --yes
python "<skill-dir>/scripts/restore_codex_sessions.py" verify --provider krill
```

## Safety Rules

- Do not touch `archived_sessions` or archived rows unless the user explicitly
  asks and the command includes `--include-archived`.
- Do not switch provider configuration or copy third-party auth settings unless
  the user explicitly asks to change providers. Session restore normally repairs
  metadata to match the provider already in use.
- Do not edit live files manually when the script can perform the same repair.
- Do not use `task_complete` to close an interrupted or damaged turn. Use
  `turn_aborted`.
- Do not delete non-empty historical turns. The script isolates open turns by
  inserting or appending `turn_aborted`.
- Do not close recent open turns unless the user explicitly confirms they are
  stale. Use `--close-recent-open-turns` only for known failed continuations.
- Back up before every write. The script creates
  `session-restore-backup-YYYYMMDD-HHMMSS` under `CODEX_HOME`.
- Prefer single-thread repair before bulk repair unless the user explicitly asks
  to restore all active sessions.

## Script Capabilities

- Update `threads.model_provider` and rollout `session_meta` provider metadata.
- Detect rollout parse errors, missing rollout files, open task turns, and
  provider metadata drift.
- Coalesce duplicate `turn_context` entries by unique `turn_id`; ignore legacy
  no-`turn_id` contexts for mutation.
- Insert one `turn_aborted` event per stale open turn.
- Close stale `thread_spawn_edges` after making child rollouts internally closed.
- Report non-complete `thread_goals`; optionally complete them only when an
  explicit repair flag is used.
- Print provider distributions, backup paths, modified files, and restart
  guidance.

## Reference

Read `references/recovery-checklist.md` when deciding whether to repair provider
metadata only, repair rollout structure, close child edges, complete stale goals,
or ask the user to restart Codex Desktop.
