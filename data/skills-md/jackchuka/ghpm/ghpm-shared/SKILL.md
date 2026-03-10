---
name: ghpm-shared
description: "Shared reference for all ghpm skills — prerequisites, config format, startup sequence, and error handling."
---

# ghpm — Shared Reference

## Prerequisites

- `gh` CLI installed and authenticated
- Token scopes: `read:project`, `project`
- GitHub Projects v2 (not classic projects)

## Config Files

All ghpm files live under `.ghpm/`:

| File                          | Purpose                               |
| ----------------------------- | ------------------------------------- |
| `.ghpm/config.json`           | Project config (fields, views, repos) |
| `.ghpm/cache.json`            | Cached project items                  |
| `.ghpm/sessions/<number>.json`| Active work session per issue         |

The entire `.ghpm/` directory is gitignored (project-specific).

If `.ghpm/config.json` is missing, tell the user to run `/ghpm-init` first and stop.

## Startup Sequence

Every skill that reads project data should follow this sequence:

1. Read `.ghpm/config.json` from the current directory. If missing, stop with init guidance (above).
2. Load cache following `references/cache.md`. If the cache is stale or missing, **automatically re-fetch** — no user prompt needed. If the re-fetch fails (network error, rate limit), fall back to the stale cache if available and note the age inline (e.g., "Using cached data from 2 hours ago").
3. Check for stale sessions: list `.ghpm/sessions/*.json`. For each session file, read `started_at` and compare to now. If a session is older than 24 hours, prompt the user:
   ```
   Found stale session for #<num> "<title>" (started <N> days ago).
   Wrap up and post journal, or discard?
   ```
   - **Wrap up**: follow the wrap-up sequence from `ghpm-work` (gather git context, post journal, clear session).
   - **Discard**: delete the session file silently.
   - If the user declines both, leave it and continue — don't block the current skill.

## Error Handling

- **Auth expired** (`gh auth status` fails): tell the user to run `gh auth login` and stop.
- **Rate limited** (HTTP 403 with rate limit message): tell the user to wait and retry later.
- **Network error**: if cache exists (even stale), offer to use stale cache as fallback.
- **Permission denied** (HTTP 403/404 on project): tell the user to check token scopes (`read:project`, `project`).

## Write Operations & Prompts

Skills that modify project items are **write** operations. Whether to confirm with the user is controlled by `prompts` config — see `references/prompts.md` for resolution logic.

Default behavior (no config): always prompt.

## Agent Integrations

Optional hooks/rules enhance `ghpm-work` sessions (auto session context, stale session detection). See `references/integrations.md` for details. Installed by `/ghpm-init` when an agent is detected. Without hooks, all skills work via explicit commands.

## Skills

| Skill                                      | Purpose                                   |
| ------------------------------------------ | ----------------------------------------- |
| [`ghpm-init`](../ghpm-init/SKILL.md)       | Initialize config from GitHub Projects v2 |
| [`ghpm-status`](../ghpm-status/SKILL.md)   | Project health dashboard                  |
| [`ghpm-view`](../ghpm-view/SKILL.md)       | Query items by view or ad-hoc filter      |
| [`ghpm-suggest`](../ghpm-suggest/SKILL.md) | Context-aware work recommendations        |
| [`ghpm-work`](../ghpm-work/SKILL.md)       | Start a work session on an issue      |
