---
name: hygiene
description: >
  Monthly environment hygiene sweep for this Mac: disk, vault, Claude config,
  package managers. Identifies stale projects, orphaned files, vault drift, skill rot,
  and package cruft. ALWAYS presents findings for review BEFORE deleting anything —
  never auto-deletes. Use when: "run hygiene", "monthly cleanup", "environment audit",
  "disk cleanup", "clean up my machine", "vault hygiene", "first Monday".
  PROACTIVE TRIGGER (CONDITIONAL): On the first Monday of each month (scheduled via
  MCP scheduled-tasks). Also when the owner mentions running low on disk space, noticing
  vault drift, or after a major project completes.
version: 1.1.0
gotchas_count: 3
---

# Hygiene, Monthly Environment Sweep

Comprehensive this Mac hygiene. Four scopes: **Disk**, **Vault**, **Claude**, **Packages**.

**Default mode: REVIEW-ONLY.** Present findings in tiered format (Safe / Verify / Keep) with counts, sizes, and a clear summary. Wait for explicit the owner approval before any destructive action. When deleting, use `mv ~/.Trash/<dated-folder>/` (reversible 30 days), never `rm -rf`.

## Output Targets

1. **Chat**: concise tiered report (Safe to delete / Needs verification / Keep)
2. **Vault log**: `areas/maintenance/YYYY-MM.md` (created each run with full findings, decisions, actions taken)

## Hard Rules (Never Skip)

1. **No `rm -rf`.** Every candidate deletion moves to `~/.Trash/hygiene-YYYY-MM-DD-HHMMSS/` for 30-day reversibility.
2. **Always ask before deleting.** Even "obvious" junk. the owner has been burned by aggressive cleanup before.
3. **Check external dependencies before classifying any folder as deletable:**
   - `which <command>`, is it on PATH?
   - `readlink <path>`, is it the target of a symlink elsewhere?
   - `grep -r "<path>" ~/.zshrc ~/.zshenv ~/.bashrc ~/.config/`, referenced in shell config?
   - `launchctl list | grep <name>`, loaded as launchd agent?
   - Known near-miss: `<HOME>/flutter dev/` looks like a stale project dir but is the **active Flutter SDK** (`which flutter` resolves there). Always check PATH first.
4. **Git remote verification.** Before proposing to delete any repo, check `git remote -v` in the repo. If no remote or remote doesn't exist on GitHub, explicitly warn that deletion = permanent data loss.
5. **No blanket gitignore rules for Obsidian Sync conflicts.** See "Obsidian Sync conflict triage" below.
6. **Tiered output** (never mix tiers):
   - **Safe to delete**: byte-identical duplicates, confirmed-retired projects with remote backup, build artifacts (node_modules/dist/target), Obsidian Sync byte-identical dup siblings.
   - **Needs verification**: divergent dups, unfamiliar folders, large folders with unclear purpose, projects without git remote.
   - **Keep**: active projects, SDK installs, folders referenced from PATH/shell/launchd/vault registry.

## Procedure

### Step 0: Create the month's vault log

```bash
MONTH=$(date +%Y-%m)
LOG="<HOME>/Documents/jj-knowledge-vault/areas/maintenance/${MONTH}.md"
```

If `$LOG` already exists (re-running same month), append a new dated section; don't overwrite.

### Step 1: Disk scope

Find large folders and candidate-retirements.

```bash
du -sh ~/Documents/GitHub/*/ ~/projects/*/ ~/dev/*/ ~/*/ 2>/dev/null | sort -rh | head -30
```

For each candidate folder:
- Check against vault Project Registry (`~/Documents/jj-knowledge-vault/CLAUDE.md`).
- Check `git remote -v` if it's a repo.
- Check PATH/shell/launchd (per Hard Rules #3).

Cross-reference against memory [project_retired_projects.md](../../..<HOME>/.claude/projects/-Users-joyd-Documents-jj-knowledge-vault/memory/project_retired_projects.md), those folders are already on the never-suggest-reviving list.

Flag for Trash: `~/.Trash/` items older than 30 days (macOS auto-empties but sometimes stalls).

Also check:
- `~/Downloads/` files older than 30 days
- `~/Desktop/` clutter (>10 loose files at root)
- Xcode derived data: `du -sh ~/Library/Developer/Xcode/DerivedData/ 2>/dev/null`
- Homebrew cache: `du -sh $(brew --cache) 2>/dev/null`
- **Docker disk image** (frequently the single biggest hog, and easy to miss): `du -sh ~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw 2>/dev/null`. It is a sparse file: logical size is huge, real on-disk size = `du`. `docker system prune` does NOT shrink it on disk. Reclaim by quitting Docker Desktop then deleting the raw (rebuilds empty on next launch) OR Docker Desktop -> Troubleshoot -> Clean/Purge. Check `docker ps -a` / `docker volume ls` for real data first (if the engine is down you get socket-missing errors, which means nothing is running and it is safe to reset). Seen 2026-06-04: 45G reclaimed, and the 06-01/06-02 scheduled runs had missed it entirely.
- **App container / data hogs**: `du -sh ~/Library/Containers/* ~/Library/Application\ Support/* 2>/dev/null | sort -rh | head`, Docker, Chrome profiles, Claude `vm_bundles`, Signal `attachments.noindex` are commonly multi-GB.
- **Photos myth-check** (before EVER suggesting photo deletion): `du -sh ~/Pictures`. If ~0B, the Photos library is iCloud-offloaded (Optimize Mac Storage) and deleting frees NOTHING while risking the cloud copies. Always `du`-verify a category is actually local before recommending it.

### Step 2: Vault scope

Run `/vault-health` (already-installed skill) first to catch drift. Then specifically:

**a) Project Registry freshness**, read [CLAUDE.md](../../..<HOME>/Documents/jj-knowledge-vault/CLAUDE.md) Project Registry. For each row:
- If Local Path is `—`, skip (already legacy).
- Otherwise, `test -d "$path"`. If path doesn't exist → registry drift, propose row update.

**b) Agent Registry freshness**, same, for the agent table. Archived agents should have `(archived → path)` annotation.

**c) Vault folder consistency**, any `projects/<name>/` without a registry row? Any registry row without a folder?

**d) Inbox backlog**, `ls ~/Documents/jj-knowledge-vault/inbox/ | wc -l`. If >10, suggest running `/triage`.

**e) Obsidian Sync conflict triage**, find ` 2.md` / ` 3.md` files:

```bash
fd -t f ' [0-9]\.md$' ~/Documents/jj-knowledge-vault/ 2>/dev/null
```

For each match, compare against the base file:
- **Byte-identical (sha256 match)**: Safe to delete (classic Sync round-trip artifact).
- **Dup is proper subset of base** (`diff` shows only `<` lines, no `>` lines): Safe to delete.
- **Divergent**: Needs verification. Before recommending delete, check if the dup's unique content might already live in a canonical artifact elsewhere (e.g. for a given project, a dated research log or a decisions log may already be the canonical copy). Dump unique-to-dup lines into a review section of the vault log.

**Do NOT** add a blanket `* 2.md` gitignore rule, it hides real conflicts. Use triage instead.

**f) Legacy folder check**, `legacy/projects/` should have `context.md` stubs for each retired project. Flag gaps.

### Step 3: Claude config scope

**a) Skills health**, run the Step 5 block from `/vault-health` (skills trigger audit, usage report).

**b) Stale agent memory**, any `~/.claude/projects/*/memory/*.md` with `description` pointing to retired/moved paths?

**c) Plans cleanup**, `ls ~/.claude/plans/`, any plan files with status `shipped` or `abandoned` older than 60 days can be archived into `~/.claude/plans/archive/`.

**d) Worktrees**, `ls -la ~/Documents/jj-knowledge-vault/.claude/worktrees/ 2>/dev/null`. Merged worktrees (branch already on main) are deletable via `git worktree remove`.

**e) MCP registry**, `cat ~/.claude/settings.json` (or wherever MCPs live). Flag any MCP entries that the owner has noted as retired or unauthenticated.

**f) Constitution audit (added 2026-08-09, per user.md §8 "Rule sunset review")**, two checks on `system/user.md`:

1. **Budget**: CJK-aware token estimate must stay under ~20K:
   ```bash
   python3 -c "
   import re
   t=open('<HOME>/Documents/jj-knowledge-vault/system/user.md',encoding='utf-8').read()
   cjk=len(re.findall(r'[一-鿿]',t)); print('user.md tokens ~', int(cjk/1.5+(len(t)-cjk)/4))"
   ```
   Over budget = a bug: propose which rule to compress or archive (never silently trim).
2. **Rule sunset review**: for each MANDATORY rule (`grep -n 'MANDATORY' system/user.md`), look for a firing within the last 6 months: a dated incident cited in the rule itself, a matching entry in `agents/shared/corrections.md` or `session-index.md`, or a the owner restatement. List rules with NO observed firing in the report under a CONSTITUTION section, with a proposal to move each to a reference tier (`system/archive/` or the wiki, one-line pointer left behind). **Review-only like everything else in this skill: the owner decides, nothing moves automatically.**

### Step 4: Package managers scope

Do **not** auto-update (can break things). Just report what's outdated so the owner can choose.

```bash
brew outdated
brew cleanup --dry-run   # list what `brew cleanup` would remove
npm outdated -g 2>&1 | head -20   # global npm packages
du -sh $(npm root -g) 2>/dev/null   # size of global node_modules
```

Also:
- Orphaned homebrew deps: `brew autoremove --dry-run`
- Uninstalled apps leaving caches: `ls ~/Library/Application\ Support/ ~/Library/Caches/ | head -40`, only flag clearly-uninstalled apps, never active ones.

### Step 5: Compose report

Report template (chat + vault log both use this structure):

```
Hygiene Sweep — YYYY-MM-DD
===========================

SAFE TO DELETE (N items, ~X GB)
  - <item> — <size> — <reason>
  ...

NEEDS VERIFICATION (N items, ~X GB)
  - <item> — <size> — <why unsure + what to check>
  ...

KEEP (flagged but verified active)
  - <item> — <why keep>
  ...

VAULT DRIFT
  - Registry row <X> points to deleted path <Y>
  - Folder <Z> exists but no registry row
  ...

SKILLS & CONFIG
  - <findings>

PACKAGES
  - brew: N outdated, ~X MB cleanup possible
  - npm global: N outdated
  ...

Summary: approve Safe tier? Discuss Verification tier before any action?
```

### Step 6: On approval, execute

For each approved delete:

```bash
TRASH="$HOME/.Trash/hygiene-$(date +%Y-%m-%d-%H%M%S)"
mkdir -p "$TRASH"
mv <item> "$TRASH/"
```

Record each action in the vault log under "Actions Taken" with timestamp + size freed.

After execution, re-verify:
- `which flutter` still works? (canary check, proves PATH not broken)
- Vault symlinks still resolve?
- Git status of any touched repo still clean?

### Step 7: Finalize vault log

Append to `areas/maintenance/YYYY-MM.md`:
- Total space freed
- Items kept for next month's review
- Any process improvements for the skill itself (feed back to SKILL.md)

## Rules

- Read the vault registry BEFORE classifying any project folder.
- Check PATH/symlinks/launchd BEFORE classifying any root-level folder.
- Trash, never `rm -rf`.
- No blanket gitignores for Obsidian Sync conflicts.
- Default to "Needs verification" when uncertain. "Safe" tier requires **all four** checks passed: not on PATH, not symlinked, not in shell config, not in launchd.
- If a repo has no git remote AND contains uncommitted work, move to "Keep" tier regardless of apparent staleness.
- Append to the monthly log, never overwrite.

- **(2026-07-15) Docker daemon probe:** `docker info --format ok` prints the format string even with NO daemon running (client-side info). Probe with `docker version --format '{{.Server.Version}}'` instead. Also: `open -g -a Docker` may never bring the VM up headlessly; if the socket stays dead ~3 min, hand it to the owner rather than looping.
- **(2026-07-15) zsh bulk-move loops:** zsh does NOT word-split unquoted `$VAR` in `for` loops; a sweep loop can silently process 0 items while echo-counts look right. Use `for n in $(echo "$LIST")` and verify with a post-move count, never the plan count.
