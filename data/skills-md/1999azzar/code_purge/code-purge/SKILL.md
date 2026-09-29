---
name: code-purge
description: >
  Deep code analysis and automated cleanup skill. Removes dead code, unused imports,
  unreferenced files, and duplicated logic from any codebase. Simplifies overly complex
  or hard-to-maintain code. Always backs up before changes and validates with tests after.

  Use when the user asks to:
  - "clean up", "remove dead code", "purge unused code"
  - "find and delete unused files/folders"
  - "remove duplicate code" or "refactor duplicated logic"
  - "simplify this codebase" or "the code is too complex"
  - "do a cleanup pass" or "code hygiene"
  - "remove everything that's not used"
---

# Code Purge

A five-phase workflow for safe, thorough removal of waste from any codebase.

## Workflow

```
Phase 1 → Analyze     deep scan: detect languages, map dead code, duplicates, unused files
Phase 2 → Report      present findings to user, confirm scope before touching anything
Phase 3 → Backup      snapshot the codebase without changing working-tree or index state
Phase 4 → Clean       execute removals in order: imports → dead code → files → refactors
Phase 5 → Verify      run test suite; report pass/fail; rollback guide if needed
```

---

## Phase 1 — Analyze

Run the bundled analyzer first. Never skip this step.

```bash
python3 scripts/analyze.py <project_root> --summary     # quick overview
python3 scripts/analyze.py <project_root> --json        # full machine-readable report
```

The script auto-detects languages and dispatches to installed tools:
- **Python**: `vulture` (dead code) + `pyflakes` (unused imports)
- **JS/TS**: `knip` (dead exports, unused deps, unused files)
- **All languages**: `jscpd` (duplicate blocks)

Use project-pinned tool executables when available. Do not let `npx` download and execute an unpinned package during analysis.

Read `references/tools.md` for the full tool inventory and manual commands per language.

**Also perform manual analysis:**
- Scan `package.json` / `pyproject.toml` / `Cargo.toml` for unused dependencies
- Check for `TODO`, `FIXME`, `HACK` comments that indicate dead branches
- Check git blame for files/functions untouched for >12 months with no external callers
- Review complexity: run `radon cc . -nb` (Python) or `lizard . --CCN 10` (multi-lang)

Read `references/patterns.md` for the complete list of dead code, duplicate, and complexity patterns.

---

## Phase 2 — Report & Confirm

Present a structured report before touching any file:

```
DEAD CODE        23 findings  (8 high, 11 medium, 4 low)
DUPLICATES        7 blocks    (2 high, 4 medium, 1 low)
UNUSED FILES      5 files     (all medium confidence)
UNUSED IMPORTS   41 imports   (all low severity)
COMPLEXITY        3 functions (CC > 10, flagged for refactor)
```

For each category, list the top findings with file:line.
Ask the user: "Which categories should I clean? Any items to skip?"

**Do NOT proceed to Phase 3 without explicit user confirmation of scope.**

---

## Phase 3 — Backup

Always create a backup before any removal. No exceptions.

```bash
bash scripts/backup.sh <project_root>
```

The script creates:
1. Git status and binary patches for tracked staged/unstaged changes (if inside a git repo)
2. A `.tar.gz` archive under `${XDG_STATE_HOME:-$HOME/.local/state}/code-purge/`, including untracked files

Set `CODE_PURGE_BACKUP_ROOT` to override the backup location. The script never writes inside, stages, stashes, resets, or otherwise mutates the target repository. Note the archive path in the final summary.

**Rollback command to provide to user:**
```bash
tar -xzf <backup-directory>/project.tar.gz -C <project_root>
```

---

## Phase 4 — Clean

Execute removals in this order to minimize cascading errors:

### 4a. Unused imports (lowest risk)
```bash
# Python — auto-remove
autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports <root>

# JS/TS — manual or ESLint fix
eslint --fix --rule 'no-unused-vars: ["error", {"vars": "all"}]' <root>
```

### 4b. Dead code — functions, classes, variables
- Remove high-confidence findings first (vulture ≥90%, knip unused exports)
- For each removal: delete the definition, then grep for any remaining references
- Verify the project still compiles/imports after each batch of 5–10 removals

### 4c. Unused files
- Delete files only after confirming no string-based references exist:
  ```bash
  grep -r "filename_stem" <root> --include="*.{py,js,ts,yaml,json,toml,cfg}"
  ```
- Delete empty directories after removing their files
- Never delete: `__init__.py` that may affect package structure, config files loaded by name

### 4d. Duplicate consolidation
- Extract the shared logic into a well-named shared module/function
- Update all call sites to use the shared version
- Delete the duplicate copies
- Do one duplicate group per commit — do not mix multiple consolidations

### 4e. Complexity refactors
Follow the heuristics in `references/patterns.md#refactoring-heuristics`.
Key rules:
- Apply "guard clause" / early-return to reduce nesting depth
- Extract sub-functions when cyclomatic complexity > 10
- Replace long if/elif chains with dict dispatch or polymorphism
- Add a docstring only if the "why" is non-obvious (not the "what")

---

## Phase 5 — Verify

```bash
bash scripts/run_tests.sh <project_root>
```

The script auto-detects pytest, jest/vitest/mocha, go test, cargo test, rspec, and maven. Exit `0` means at least one detected suite passed, `1` means a suite failed, and `2` means no suite could be executed. Exit `2` is unverified, not success.

**If tests pass**: commit the cleanup with a message like:
```
chore: remove dead code, unused imports, and 5 unreferenced files

- vulture: removed 8 dead functions in auth/, utils/
- knip: removed 3 unused exports, 2 unused npm deps
- jscpd: consolidated 2 duplicate validation blocks into shared/validators
- autoflake: removed 41 unused imports
```

**If tests fail**:
1. Identify which removal caused the failure (bisect with `git diff --stat`)
2. Restore that specific file from the backup archive without overwriting unrelated files
3. Re-run tests to confirm restoration
4. Investigate: was the "dead" code actually called dynamically (reflection, config)?
5. Add to a "skip list" for this project and continue with the rest

---

## Tool Installation (quick reference)

```bash
# Python
pip install vulture pyflakes autoflake radon lizard

# JS/TS (pick one)
npm i -g knip jscpd
npm exec --offline knip
npm exec --offline jscpd -- .
```

Read `references/tools.md` for per-language tool details, Go/Rust/Ruby specifics, and SonarQube setup.

---

## Key Safety Rules

- **Never skip backup** — even for "quick" cleanups
- **Never mix dead-code removal with feature changes** in the same commit
- **Always grep for string references** before deleting a file or function
- **Framework magic is invisible to static analysis** — decorators, signals, dynamic dispatch need manual verification
- **Public API surfaces** (published packages, shared libraries) require extra caution — check external consumers
- Read `references/patterns.md#safe-removal-checklist` before each removal batch
