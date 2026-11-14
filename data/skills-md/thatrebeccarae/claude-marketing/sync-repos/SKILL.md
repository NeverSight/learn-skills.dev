---
name: sync-repos
description: "Manage public/private repository pairs. Verify parity, detect drift, run sync scripts, and validate no sensitive data leaks to the public repo. Use for projects that maintain separate dev and public repositories."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: devops
  domain: git
  updated: 2026-03-19
  tested: 2026-03-19
  tested_with: "Claude Code v2.1"
---

# Sync Repos

Manage public/private repository pairs. Verify parity between a dev (private) repo and its public counterpart, detect drift, run sync scripts, validate results, and ensure no PII or secrets leak to the public side.

## Install

```bash
claude install-skill https://github.com/thatrebeccarae/claude-skills/tree/main/sync-repos
```

## When to Use

- Before pushing a public repo — verify the sync is clean and current
- After major dev work — check whether the public repo has drifted behind
- On a periodic cadence — weekly or before releases, catch unsynced changes early
- When setting up a new public/private repo pair for the first time

## Usage

- `/sync-repos check [dev-path] [public-path]` — Compare repos and report drift
- `/sync-repos sync [dev-path] [public-path]` — Run sync script and validate
- `/sync-repos setup [dev-path] [public-path]` — Create initial sync-public.sh and config

If paths are omitted, prompt the user for them. Look for `.syncignore` or `scripts/sync-public.conf` in the dev repo to auto-detect the pair.

## Procedure

### Check Mode

1. **Validate paths.** Confirm both paths exist and contain `.git/` directories. Abort with a clear message if either is not a git repo.

2. **Detect sync script.** Look for `scripts/sync-public.sh`, `scripts/sync-public.conf`, or `.syncignore` in the dev repo. Report whether a sync mechanism exists.

3. **Compare file lists.** Generate sorted file lists for both repos (excluding `.git/`, `node_modules/`, `dist/`). Categorize differences:
   - **Expected exclusions** — files matching known exclusion patterns (see Common Exclusion Patterns below) or listed in `.syncignore` / `sync-public.conf`
   - **Unexpected drift** — files present in dev but missing from public that are NOT in any exclusion list
   - **Diverged files** — files present in both repos but with different content (compare via `sha256sum` or `git hash-object`)
   - **Public-only files** — files in public but not in dev (legitimate: README, CONTRIBUTING, LICENSE, .github/)

4. **Check last sync timestamp.** If `scripts/sync-public.sh` exists, check its last execution time via the most recent commit in the public repo that matches a sync pattern. Compare against the latest commit in the dev repo.

5. **Report.** Present a summary table:
   - Sync script: found / not found
   - Files only in dev (expected): count
   - Files only in dev (unexpected): count + list
   - Diverged files: count + list
   - Public-only files: count + list
   - Estimated drift: number of dev commits since last sync
   - Recommendation: "in sync", "minor drift", or "sync needed"

### Sync Mode

1. **Run check first.** Execute the full check procedure above. If no drift is detected, report "already in sync" and stop.

2. **Locate sync script.** Look for `scripts/sync-public.sh` in the dev repo. If not found, ask the user whether to run setup mode to create one.

3. **Preview the sync.** Show what the sync script will do — files to copy, exclusions, text replacements. Require user confirmation before proceeding.

4. **Execute the sync script.** Run from the dev repo root:
   ```bash
   bash scripts/sync-public.sh
   ```
   Capture stdout and stderr. If the script exits non-zero, report the error and stop.

5. **Post-sync validation.** After the script completes:
   - Run the check procedure again to confirm parity
   - Scan the public repo diff for PII and secrets (see REFERENCE.md for scan patterns)
   - Flag any findings and block until resolved

6. **Report results.** Summarize:
   - Files synced: count
   - Exclusions applied: count
   - PII/secrets scan: clean or findings
   - Next step: "Review changes in public repo, then `/safe-push` when ready"

### Setup Mode

1. **Scan the dev repo.** Identify files and directories that should NOT sync to public:
   - Environment files: `.env`, `.env.*` (except `.env.example`)
   - Planning/internal: `.planning/`, `.claude/`, `CLAUDE_CONTEXT.md`, `briefs/`
   - Data/build artifacts: `data/`, `dist/`, `node_modules/`, `.git/`
   - Sync infrastructure: `scripts/sync-public.sh`, `scripts/sync-public.conf`
   - Sensitive config: `*.pem`, `*.key`, `*.plist`, `config/soul.md`
   - Project-specific patterns detected via `.gitignore` analysis

2. **Generate sync-public.conf.** Create a config file with:
   - `SOURCE_DIR` and `TARGET_DIR` variables
   - `PACKAGE_NAME` for the public repo
   - `EXCLUDE_PATHS` array with all identified exclusions
   - `PRESERVE_PATHS` array for public-only files (README, LICENSE, .github/)

3. **Generate sync-public.sh.** Create the sync script using the rsync-based template from REFERENCE.md. Include:
   - Config file sourcing
   - Path validation
   - Target cleanup (preserve `.git/` and `PRESERVE_PATHS`)
   - rsync with `--delete-excluded` and exclusion list
   - Personal data leak check
   - File count summary

4. **User review.** Display the generated config and script. Wait for explicit approval before writing.

5. **Write files.** Save `scripts/sync-public.sh` (chmod +x) and `scripts/sync-public.conf` to the dev repo.

## Common Exclusion Patterns

These patterns are excluded from sync by default. Append project-specific patterns as needed.

| Pattern | Reason |
|---------|--------|
| `.git/` | Git history stays separate |
| `.env`, `.env.*` | Secrets and environment config |
| `.planning/` | Internal planning docs |
| `.claude/` | Claude Code project config |
| `CLAUDE_CONTEXT.md` | Internal agent context |
| `data/` | Local data / databases |
| `dist/`, `node_modules/` | Build artifacts |
| `*.pem`, `*.key` | Private key material |
| `*.plist` | macOS service config |
| `scripts/sync-public.*` | Sync infrastructure itself |
| `briefs/` | Internal content briefs |
| `config/soul.md` | Personal agent config |

## Key Principles

- **Never auto-push.** Sync writes files locally. Pushing to remote is always a separate, user-confirmed step via `/safe-push`.
- **Always validate after sync.** Every sync run ends with a PII/secrets scan on the public repo. No exceptions.
- **Exclusion list is append-only.** Never remove exclusion patterns without explicit user approval. It is safer to exclude too much than too little.
- **Preserve public-only files.** The public repo may have its own README, LICENSE, CONTRIBUTING, .github/ workflows. Sync must never overwrite these.
- **Conf is separate from script.** Keep `sync-public.conf` separate so exclusion lists are easy to review and update without touching script logic.
