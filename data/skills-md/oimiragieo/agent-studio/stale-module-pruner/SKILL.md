---
name: stale-module-pruner
description: >-
  Ripgrep-powered dead-code crawler that finds stale, broken, or orphaned
  JavaScript/CJS/MJS modules in the Agent Studio framework. Walks a target
  directory, checks each file for external references, and surfaces (or deletes)
  unreferenced files. Prevents registry bloat and silent tool dropouts from
  modules no one calls.
version: 1.0.0
model: sonnet
category: validation
invoked_by: both
user_invocable: true
tools: [Read, Bash, Glob, Grep]
agents:
  - developer
  - code-simplifier
best_practices:
  - Always run in dry-run mode first before enabling --delete
  - Cross-check findings against test files before deletion
  - Save report before any destructive pass
error_handling: strict
streaming: supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Stale Module Pruner

## Overview

Ripgrep-powered dead-code crawler for the Agent Studio framework. Walks a target
directory (default: `.claude/lib`), then for each `.js`/`.cjs`/`.mjs` file checks
whether its module name appears in any other file across the codebase. Files with
no external references are flagged as STALE and optionally deleted.

**Core principle:** Dead modules that stay in `.claude/lib/` create false positive
references in the ecosystem scanner, inflate the registry, and mislead other tools
about what capabilities are actually active. Regular pruning keeps the framework
lean and the scanner signal clean.

## When to Invoke

```javascript
Skill({ skill: 'stale-module-pruner' });
```

Invoke when:

- Post-archival cleanup: after moving modules to `_archive/`, run pruner on `lib/`
- After bulk refactors that relocated or merged modules
- Before running `validate-ecosystem-integrity.cjs` to reduce noise
- As part of a maintenance sprint

## Mandatory Skills

| Skill                             | Purpose                      | When                 |
| --------------------------------- | ---------------------------- | -------------------- |
| `task-management-protocol`        | Track pruning progress       | Always               |
| `ripgrep`                         | Search for module references | During scan          |
| `code-semantic-search`            | Verify intent when uncertain | On ambiguous hits    |
| `token-saver-context-compression` | Compress large result sets   | When output is large |
| `verification-before-completion`  | Gate completion              | Before marking done  |
| `memory-search`                   | Check prior pruning patterns | At start             |

## Iron Laws

1. **Always dry-run first.** Run without `--delete` and save the STALE list before
   any destructive pass. Never delete files on a first invocation without reviewing
   the candidates. One false positive can remove an actively-used module.

2. **Never rely on filename alone.** The pruner matches by module name (filename
   without extension). Files named `utils.cjs` may be legitimately unreferenced by
   that exact name but still used via a barrel import or index re-export. Verify
   ambiguous hits against barrel/index files before treating as truly stale.

3. **Always check test files.** A module may have zero production references but an
   active test. The pruner skips `.json` and `.md` matches but not test `.cjs` files.
   If the only reference is in a test, the module may still be needed.

4. **Never delete archived modules as stale.** Modules in `_archive/` or
   `_archive/dead/` are already archived — the pruner skips `_archive/` dirs by
   default. Do not point `--targetDir` at an archive path.

5. **Always save the prune report before completing.** Write findings to
   `.claude/context/reports/qa/stale-module-prune-{ISO-date}.md` before marking
   the task complete.

## Anti-Patterns

| Anti-Pattern                                 | Risk                                                       | Correct Approach                                        |
| -------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| Running with `--delete` on first invocation  | Destroys modules with barrel/index re-exports              | Always dry-run first, review candidates, then delete    |
| Treating zero-reference as definitive stale  | Barrel imports and test-only references create false stale | Verify each STALE candidate against index files + tests |
| Running from a non-project-root CWD          | All path resolution breaks; misleading output              | Always run from project root (`process.cwd()`)          |
| Pointing `--targetDir` at `.claude/lib` only | Misses stale modules in `scripts/` or `tools/`             | Run separate passes with different `--targetDir` values |
| Deleting without a prune report artifact     | No audit trail; next session can't identify what was lost  | Always save report before deletion                      |

## Step 1: Dry-Run Scan

```bash
# Default: scan .claude/lib for stale CJS/MJS/JS modules (dry-run)
node .claude/skills/stale-module-pruner/scripts/main.cjs

# Scan a different target directory
node .claude/skills/stale-module-pruner/scripts/main.cjs --targetDir .claude/tools/cli

# Scan with custom search scope
node .claude/skills/stale-module-pruner/scripts/main.cjs --targetDir .claude/lib \
  --searchDirs .claude,tests,scripts,package.json
```

The script outputs one line per stale module:

```
STALE: .claude/lib/utils/old-helper.cjs
STALE: .claude/lib/routing/deprecated-matcher.cjs

Total stale items processed: 2
```

## Step 2: Review Candidates

For each `STALE:` line:

1. Open the file — understand its purpose
2. Search for indirect references: barrel imports, `require('./')`, `index.cjs` re-exports
3. Check test files: `grep -r "{filename}" tests/`
4. Confirm it is genuinely unused before approving for deletion

Create a prune report at `.claude/context/reports/qa/stale-module-prune-{ISO-date}.md`:

```markdown
# Stale Module Prune Report

<!-- Agent: developer | Task: #{id} | Session: {date} -->

**Date:** YYYY-MM-DD
**Target:** .claude/lib
**Candidates:** N

## Confirmed Stale (delete)

- .claude/lib/utils/old-helper.cjs — no references, no tests, no barrel export

## Kept (false positive)

- .claude/lib/utils/common.cjs — referenced by index.cjs barrel (not caught by name match)
```

## Step 3: Delete Pass (Conditional)

Only after the prune report is reviewed and candidates confirmed:

```bash
node .claude/skills/stale-module-pruner/scripts/main.cjs \
  --targetDir .claude/lib --delete
```

After deletion, re-run `validate-ecosystem-integrity.cjs` to confirm no new
`[PHANTOM_REQUIRE]` errors were introduced.

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
cat .claude/context/memory/issues.md
```

Review prior pruning patterns and known barrel-import false positives.

**After completing:**

- Pruning pattern → `.claude/context/memory/learnings.md`
- False positive suppression decision → `.claude/context/memory/decisions.md`
- Unresolved stale candidate needing owner review → `.claude/context/memory/issues.md`

> **Assume interruption:** If the prune report isn't saved to disk, it didn't happen.
