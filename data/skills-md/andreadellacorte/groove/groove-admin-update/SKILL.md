---
name: groove-admin-update
description: "Pull latest groove skills and apply pending migrations to local groove state."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-update

## Outcome

All pending migrations are applied to the user's local groove state in version order. `.groove/index.md` reflects the current installed groove version.

## Acceptance Criteria

- `groove-version:` in `.groove/index.md` matches `version:` in `skills/groove/SKILL.md` after update
- Each pending migration was applied in order
- `groove-version:` updated after each successful migration (partial progress is recoverable)
- If already up to date, reports clearly and exits
- **Source-of-truth check**: "up to date" is only reported when the installed skill version equals the latest GitHub release; if the add step left an older version on disk (e.g. cached or default branch), the user is warned and told how to fix it

## Steps

1. Run `npx skills add andreadellacorte/groove --yes` — pulls latest groove skill files and refreshes the lock entry (more reliable than `npx skills update` which requires a pre-populated folder hash). Note: the CLI may install a cached or default-branch copy rather than the latest release tag; step 4 verifies against GitHub.
   - After this step, **re-read this SKILL.md (`skills/groove-admin-update/SKILL.md`) from disk** before continuing — the skill refresh may have updated the update command itself, and the remainder of these steps must reflect the latest version
2. Read `groove-version:` from `.groove/index.md` — if key absent, assume `0.1.0` and write it
3. Read installed version from `version:` in `skills/groove/SKILL.md`
4. **Verify against latest release**: Fetch `https://api.github.com/repos/andreadellacorte/groove/releases/latest` (tag_name, strip leading `v`). If the request succeeds, compare installed with latest using semver. If installed is less than latest: do **not** report "up to date" even if local and installed match; instead report: "Installed skill is v<installed> but latest release is v<latest>. The add step may have used a cached or default-branch copy. Run: `npx skills add andreadellacorte/groove@v<latest> --yes` then run `/groove-admin-update` again." and exit. If the API call fails (network, rate limit), continue without this check.
5. If local and installed versions match: report "groove is up to date (v<version>)" and exit
6. Read `skills/groove/migrations/index.md` — parse the migration table
7. Filter rows where `To` > local version AND `To` <= installed version, in table order — the `From` field is informational only and does not gate execution
8. If no migrations found but versions differ: update `groove-version:` in `.groove/index.md` directly to the installed version and report "no state migrations needed — version bumped to v<version>"
9. For each pending migration:
   a. Report "Applying <from> → <to>: <description>"
   b. Read and execute the migration file
   c. Update `groove-version:` in `.groove/index.md` to the `To` version
   d. Report "✓ <from> → <to> applied"
10. Report summary: N migrations applied, now at v<version>

## Constraints

- **Source of truth for "latest" is GitHub releases** — `npx skills add` can leave an older version on disk (cached clone, default branch). Comparing only `.groove/index.md` with installed `SKILL.md` can falsely report "up to date". Step 4 must verify installed vs `releases/latest` and warn when they differ.
- Never skip a migration — apply every matching migration in table order even if `From` does not match local version exactly
- Update `groove-version:` after each individual migration, not only at the end
- If a migration fails: stop, report the failure and current version, do not continue
- Do not modify skill files — `npx skills update` handles that; this command only migrates local state
- Local state includes: `.groove/index.md` config keys, memory directory structure, AGENTS.md sections
- Each migration file is idempotent — if re-run after partial failure, it should be safe
