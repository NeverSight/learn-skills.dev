---
name: swain-doctor
description: "ALWAYS invoke this skill at the START of every session before doing any other work. Validates project health: governance rules, tool availability, memory directory, settings files, script permissions, .agents directory, and .beads/.gitignore hygiene. Remediates issues across all swain skills. Idempotent — safe to run every session."
user-invocable: true
license: MIT
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  short-description: Session-start health checks and repair
  version: 2.2.0
  author: cristos
  source: swain
---

# Doctor

Session-start health checks for swain projects. Validates and repairs health across **all** swain skills — governance, tools, directories, settings, scripts, caches, and runtime state. Idempotent — run it every session; it only writes when repairs are needed.

Run checks in the order listed below. Collect all findings into a summary table at the end.

## Preflight integration

A lightweight shell script (`scripts/swain-preflight.sh`) performs quick checks before invoking the full doctor. If preflight exits 0, swain-doctor is skipped for the session. If it exits 1, swain-doctor runs normally.

The preflight checks are a subset of this skill's checks — governance files, .agents directory, .beads health, script permissions. It runs as pure bash with zero agent tokens. See AGENTS.md § Session startup for the invocation flow.

When invoked directly by the user (not via the auto-invoke flow), swain-doctor always runs regardless of preflight status.

## Session-start governance check

1. Detect the agent platform and locate the context file:

   | Platform | Context file | Detection |
   |----------|-------------|-----------|
   | Claude Code | `CLAUDE.md` (project root) | Default — use if no other platform detected |
   | Cursor | `.cursor/rules/swain-governance.mdc` | `.cursor/` directory exists |

2. Check whether governance rules are already present:

   ```bash
   grep -l "swain governance" CLAUDE.md AGENTS.md .cursor/rules/swain-governance.mdc 2>/dev/null
   ```

   If any file matches, governance is already installed. Proceed to [Legacy skill cleanup](#legacy-skill-cleanup).

3. If no match, run [Legacy skill cleanup](#legacy-skill-cleanup), then proceed to [Governance injection](#governance-injection).

## Legacy skill cleanup

Clean up skill directories that have been superseded by renames or retired entirely. Read the legacy mapping from `references/legacy-skills.json` in this skill's directory.

### Renamed skills

For each entry in the `renamed` map:

1. Check whether `.claude/skills/<old-name>/` exists.
2. If it does NOT exist, skip (nothing to clean).
3. If it exists, check whether `.claude/skills/<new-name>/` also exists. If the replacement is missing, **skip and warn** — the update may not have completed:
   > Skipping cleanup of `<old-name>` — its replacement `<new-name>` is not installed.
4. If both exist, **fingerprint check**: read `.claude/skills/<old-name>/SKILL.md` and check whether its content matches ANY of the fingerprints listed in `legacy-skills.json`. Specifically, grep the file for each fingerprint string — if at least one matches, the skill is confirmed to be a swain skill.
5. If no fingerprint matches, **skip and warn** — this may be a third-party skill with the same name:
   > Skipping cleanup of `.claude/skills/<old-name>/` — it does not appear to be a swain skill (no fingerprint match). If this is a stale swain skill, delete it manually.
6. If fingerprint matches and replacement exists, **delete the old directory**:
   ```bash
   rm -rf .claude/skills/<old-name>
   ```
   Tell the user:
   > Removed legacy skill `.claude/skills/<old-name>/` (replaced by `<new-name>`).

### Retired skills

For each entry in the `retired` map (pre-swain skills absorbed into the ecosystem):

1. Check whether `.claude/skills/<old-name>/` exists.
2. If it does NOT exist, skip (nothing to clean).
3. If it exists, **fingerprint check**: same as for renamed skills — read `.claude/skills/<old-name>/SKILL.md` and check whether its content matches ANY fingerprint in `legacy-skills.json`.
4. If no fingerprint matches, **skip and warn**:
   > Skipping cleanup of `.claude/skills/<old-name>/` — it does not appear to be a known pre-swain skill (no fingerprint match). Delete manually if stale.
5. If fingerprint matches, **delete the old directory**:
   ```bash
   rm -rf .claude/skills/<old-name>
   ```
   Tell the user:
   > Removed retired pre-swain skill `.claude/skills/<old-name>/` (functionality now in `<absorbed-by>`).

After processing all entries, check whether the governance block in the context file references old skill names. If the governance block (between `<!-- swain governance -->` and `<!-- end swain governance -->`) contains any old-name from the `renamed` map, delete the entire block (inclusive of markers) and proceed to [Governance injection](#governance-injection) to re-inject a fresh copy with current names.

## Platform dotfolder cleanup

The `npx skills add --all` command (or older versions of swain-update without autodetect) creates dotfolder stubs (e.g., `.windsurf/`, `.cursor/`) for agent platforms that are not installed. These directories only contain symlinks back to `.agents/skills/` and clutter the working tree. See [GitHub issue #21](https://github.com/cristoslc/swain/issues/21).

Read the platform data from `references/platform-dotfolders.json` in this skill's directory. Each entry in the `platforms` array has a `project_dotfolder` name and one or both detection strategies: `command` (CLI binary name) and `detection` (HOME config directory path). Entries with collision-prone command names (e.g., `cmd`, `cortex`, `mux`, `pi`) omit `command` and rely on HOME detection only.

### Step 1 — Autodetect installed platforms

Iterate over the `platforms` array. For each entry, a platform is considered **installed** if either check succeeds:

1. If the entry has a `command` field → run `command -v <command> &>/dev/null`.
2. If the entry has a `detection` field → expand the path (replace `~` with `$HOME`, evaluate env var defaults like `${CODEX_HOME:-~/.codex}`) and check whether the directory exists.

Always consider `.claude` installed (current platform — never a cleanup candidate).

**Requires:** `jq` (for reading the JSON). If `jq` is not available, skip this section and warn.

```bash
installed_dotfolders=(".claude")
while IFS= read -r entry; do
  dotfolder=$(echo "$entry" | jq -r '.project_dotfolder')
  cmd=$(echo "$entry" | jq -r '.command // empty')
  det=$(echo "$entry" | jq -r '.detection // empty')

  found=false
  if [[ -n "$cmd" ]] && command -v "$cmd" &>/dev/null; then
    found=true
  fi
  if [[ -n "$det" ]] && ! $found; then
    det_expanded=$(echo "$det" | sed "s|~|$HOME|g")
    det_expanded=$(eval echo "$det_expanded" 2>/dev/null)
    [[ -d "$det_expanded" ]] && found=true
  fi

  $found && installed_dotfolders+=("$dotfolder")
done < <(jq -c '.platforms[]' "SKILL_DIR/references/platform-dotfolders.json")
```

*(Replace `SKILL_DIR` with the actual path to this skill's directory.)*

### Step 2 — Build cleanup candidates

Every entry in `platforms` whose `project_dotfolder` is NOT in the `installed_dotfolders` list is a cleanup candidate.

### Step 3 — Remove installer stubs

For each candidate dotfolder:

1. Check whether the directory exists in the project root.
2. If it does NOT exist, skip.
3. If it exists, **verify it is installer-generated** — the directory should contain only a `skills/` subdirectory (possibly with symlinks or further subdirectories). Check:

   ```bash
   # Count top-level entries (excluding . and ..)
   entries=$(ls -A "<dotfolder>" 2>/dev/null | wc -l)
   # Check if the only entry is "skills"
   if [[ "$entries" -le 1 ]] && [[ -d "<dotfolder>/skills" || "$entries" -eq 0 ]]; then
     # Safe to remove — installer-generated stub
   fi
   ```

   - If the directory is empty OR contains only a `skills/` subdirectory → **remove it**:
     ```bash
     rm -rf <dotfolder>
     ```
   - If the directory contains other files or directories besides `skills/` → **skip and warn**:
     > Skipping `<dotfolder>` — contains user content beyond installer symlinks. Remove manually if unused.

4. After processing all entries, report:
   > Removed N platform dotfolder(s) created by `npx skills add` (installer stubs for unused agent platforms).

   If none were found, this step is silent.

## Governance injection

When governance rules are not found (or were deleted during legacy cleanup), inject them into the appropriate context file.

### Claude Code

Determine the target file:

1. If `CLAUDE.md` exists and its content is just `@AGENTS.md` (the include pattern set up by swain-init), inject into `AGENTS.md` instead.
2. Otherwise, inject into `CLAUDE.md` (create it if it doesn't exist).

Read the canonical governance content from `references/AGENTS.content.md` (relative to this skill's directory) and append it to the target file.

### Cursor

Write the governance rules to `.cursor/rules/swain-governance.mdc`. Create the directory if needed.

Prepend Cursor MDC frontmatter to the canonical content from `references/AGENTS.content.md`:

```markdown
---
description: "swain governance — skill routing, pre-implementation protocol, issue tracking"
globs:
alwaysApply: true
---
```

Then append the full contents of `references/AGENTS.content.md` after the frontmatter.

### After injection

Tell the user:

> Governance rules installed in `<file>`. These ensure swain-design, swain-do, and swain-release skills are routable. You can customize the rules — just keep the `<!-- swain governance -->` markers so this skill can detect them on future sessions.

## Beads gitignore hygiene

This section runs every session, after governance checks. It is idempotent. **Skip entirely if `.beads/` does not exist** (the project has not initialized bd yet).

### Step 1 — Validate .beads/.gitignore

The following are the canonical ignore patterns. This list is kept in sync with `references/.beads-gitignore` in this skill's directory.

**Canonical patterns** (non-comment, non-blank lines):

```
dolt/
dolt-access.lock
bd.sock
bd.sock.startlock
sync-state.json
last-touched
.local_version
redirect
.sync.lock
export-state/
ephemeral.sqlite3
ephemeral.sqlite3-journal
ephemeral.sqlite3-wal
ephemeral.sqlite3-shm
dolt-server.pid
dolt-server.log
dolt-server.lock
dolt-server.port
dolt-server.activity
dolt-monitor.pid
backup/
*.db
*.db?*
*.db-journal
*.db-wal
*.db-shm
db.sqlite
bd.db
.beads-credential-key
```

1. If `.beads/.gitignore` does not exist, create it from the reference file (`references/.beads-gitignore`) and skip to Step 2.

2. Read `.beads/.gitignore`. For each canonical pattern above, check whether it appears as a non-comment line in the file.

3. Collect any missing patterns. If none are missing, this step is silent — move to Step 2.

4. If patterns are missing, append them to `.beads/.gitignore`:

   ```

   # --- swain-managed entries (do not remove) ---
   <missing patterns, one per line>
   ```

5. Tell the user:
   > Patched `.beads/.gitignore` with N missing entries. These entries prevent runtime and database files from being tracked by git.

### Step 2 — Clean tracked runtime files

After ensuring the gitignore is correct, check whether git is still tracking files that should now be ignored:

```bash
cd "$(git rev-parse --show-toplevel)" && git ls-files --cached .beads/ | while IFS= read -r f; do
  if git check-ignore -q "$f" 2>/dev/null; then
    echo "$f"
  fi
done
```

This lists files that are both tracked (in the index) and matched by the current gitignore rules.

If no files are found, this step is silent.

If files are found:

1. Remove them from the index (this untracks them without deleting from disk):

   ```bash
   git rm --cached <file1> <file2> ...
   ```

2. Tell the user:
   > Untracked N file(s) from git that are now covered by `.beads/.gitignore`. These files still exist on disk but will no longer be committed. You should commit this change.

## Governance content reference

The canonical governance rules live in `references/AGENTS.content.md` (relative to this skill's directory). Both swain-doctor and swain-init read from this single source of truth. If the upstream rules change in a future swain release, update that file and bump the skill version. Consumers who want the updated rules can delete the `<!-- swain governance -->` block from their context file and re-run this skill.

## Tool availability

Check for required and optional external tools. Report results as a table. **Never install tools automatically** — only inform the user what's missing and how to install it.

### Required tools

These tools are needed by multiple skills. If missing, warn the user.

| Tool | Check | Used by | Install hint (macOS) |
|------|-------|---------|---------------------|
| `git` | `command -v git` | All skills | Xcode Command Line Tools |
| `jq` | `command -v jq` | swain-status, swain-stage, swain-session, swain-do | `brew install jq` |

### Optional tools

These tools enable specific features. If missing, note which features are degraded.

| Tool | Check | Used by | Degradation | Install hint (macOS) |
|------|-------|---------|-------------|---------------------|
| `bd` | `command -v bd` | swain-do, swain-status (tasks) | Task tracking falls back to text ledger; status skips task section | `brew install beads` |
| `uv` | `command -v uv` | swain-stage (MOTD TUI), swain-do (plan ingestion) | MOTD falls back to bash script; plan ingestion unavailable | `brew install uv` |
| `gh` | `command -v gh` | swain-status (GitHub issues), swain-release | Status skips issues section; release can't create GitHub releases | `brew install gh` |
| `tmux` | `command -v tmux` | swain-stage | Workspace layouts unavailable (only relevant if user wants tmux features) | `brew install tmux` |
| `fswatch` | `command -v fswatch` | swain-design (specwatch live mode) | Live artifact watching unavailable; on-demand `specwatch.sh scan` still works | `brew install fswatch` |

### Reporting format

After checking all tools, output a summary:

```
Tool availability:
  git .............. ok
  jq ............... ok
  bd ............... ok
  uv ............... ok
  gh ............... ok
  tmux ............. ok (in tmux session: yes)
  fswatch .......... MISSING — live specwatch unavailable. Install: brew install fswatch
```

Only flag items that need attention. If all required tools are present, the check is silent except for missing optional tools that meaningfully degrade the experience.

## Memory directory

The Claude Code memory directory stores `status-cache.json`, `session.json`, and `stage-status.json`. Skills that write to this directory will fail silently or error if it doesn't exist.

### Step 1 — Compute the correct path

The directory slug is derived from the **full absolute repo path**, not just the project name:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
_PROJECT_SLUG=$(echo "$REPO_ROOT" | tr '/' '-')
MEMORY_DIR="$HOME/.claude/projects/${_PROJECT_SLUG}/memory"
```

### Step 2 — Create if missing

```bash
if [[ ! -d "$MEMORY_DIR" ]]; then
  mkdir -p "$MEMORY_DIR"
fi
```

If created, tell the user:
> Created memory directory at `$MEMORY_DIR`. This is where swain-status, swain-session, and swain-stage store their caches.

If it already exists, this step is silent.

### Step 3 — Validate existing cache files

If the memory directory exists, check that any existing JSON files in it are valid:

```bash
for f in "$MEMORY_DIR"/*.json; do
  [[ -f "$f" ]] || continue
  if ! jq empty "$f" 2>/dev/null; then
    echo "warning: $f is corrupt JSON — removing"
    rm "$f"
  fi
done
```

Report any files that were removed due to corruption. This prevents skills from reading garbage data.

**Requires:** `jq` (skip this step if jq is not available — warn instead).

## Settings validation

Swain uses a two-tier settings model. Malformed JSON in either file causes silent failures across multiple skills (swain-stage, swain-session, swain-status).

### Check project settings

If `swain.settings.json` exists in the repo root:

```bash
jq empty swain.settings.json 2>/dev/null
```

If this fails, warn:
> `swain.settings.json` contains invalid JSON. Skills will fall back to defaults. Fix the file or delete it to use defaults.

### Check user settings

If `${XDG_CONFIG_HOME:-$HOME/.config}/swain/settings.json` exists:

```bash
jq empty "${XDG_CONFIG_HOME:-$HOME/.config}/swain/settings.json" 2>/dev/null
```

If this fails, warn:
> User settings file contains invalid JSON. Skills will fall back to project defaults. Fix the file or delete it.

**Requires:** `jq` (skip these checks if jq is not available).

## Script permissions

All shell and Python scripts in `skills/*/scripts/` must be executable. Skills invoke these via `bash scripts/foo.sh`, which works regardless, but `uv run scripts/foo.py` and direct execution require the executable bit.

### Check and repair

```bash
find skills/*/scripts/ -type f \( -name '*.sh' -o -name '*.py' \) ! -perm -u+x
```

If any files are found without the executable bit:

```bash
chmod +x <files...>
```

Tell the user:
> Fixed executable permissions on N script(s).

If all scripts are already executable, this step is silent.

## .agents directory

The `.agents/` directory stores per-project configuration for swain skills:
- `execution-tracking.vars.json` — swain-do first-run config
- `specwatch.log` — swain-design stale reference log
- `evidencewatch.log` — swain-search pool refresh log

### Check and create

```bash
if [[ ! -d ".agents" ]]; then
  mkdir -p ".agents"
fi
```

If created, tell the user:
> Created `.agents/` directory for skill configuration storage.

If it already exists, this step is silent.

## Status cache bootstrap

If the memory directory exists but `status-cache.json` does not, and the status script is available, seed an initial cache so that swain-stage MOTD and other consumers have data on first use.

```bash
STATUS_SCRIPT="skills/swain-status/scripts/swain-status.sh"
if [[ -f "$STATUS_SCRIPT" && ! -f "$MEMORY_DIR/status-cache.json" ]]; then
  bash "$STATUS_SCRIPT" --json > /dev/null 2>&1 || true
fi
```

If the cache was created, tell the user:
> Seeded initial status cache. The MOTD and status dashboard now have data.

If the script is not available or the cache already exists, this step is silent. If the script fails, ignore — the cache will be created on the next `swain-status` invocation.

## bd health (extended .beads checks)

This extends the existing [Beads gitignore hygiene](#beads-gitignore-hygiene) section. **Skip entirely if `.beads/` does not exist.**

### bd doctor

If `bd` is available and `.beads/` exists, run the bd built-in health check:

```bash
bd doctor --json 2>/dev/null
```

If the exit code is non-zero, attempt automatic repair:

```bash
bd doctor --fix 2>/dev/null
```

Report the result to the user. If `--fix` resolves all issues, note it. If issues persist, list them and suggest the user investigate.

### Stale runtime files

Check for runtime files that may have been left behind by a crashed bd process:

```bash
for f in .beads/bd.sock .beads/bd.sock.startlock .beads/dolt-server.pid .beads/dolt-server.lock .beads/.sync.lock; do
  if [[ -f "$f" ]]; then
    echo "stale: $f"
  fi
done
```

If stale files are found, warn:
> Found stale bd runtime files. If bd is not currently running (`pgrep -f "bd serve"` shows nothing), these can be safely removed. Remove them? (list the files)

**Do not auto-delete** — ask the user first, since a bd process might actually be running.

## Summary report

After all checks complete, output a concise summary table:

```
swain-doctor summary:
  Governance ......... ok
  Legacy cleanup ..... ok (nothing to clean)
  Platform dotfolders  ok (nothing to clean)
  .beads/.gitignore .. ok
  Tools .............. ok (1 optional missing: fswatch)
  Memory directory ... ok
  Settings ........... ok
  Script permissions . ok
  .agents directory .. ok
  Status cache ....... seeded
  bd health .......... ok

3 checks performed repairs. 0 issues remain.
```

Use these status values:
- **ok** — nothing to do
- **repaired** — issue found and fixed automatically
- **warning** — issue found, user action recommended (give specifics)
- **skipped** — check could not run (e.g., jq missing for JSON validation)

If any checks have warnings, list them below the table with remediation steps.
