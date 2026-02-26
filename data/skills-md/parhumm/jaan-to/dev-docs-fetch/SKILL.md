---
name: dev-docs-fetch
description: Fetch and cache library docs via Context7 MCP with auto-detect. Use when fetching technical documentation.
allowed-tools: Read, Glob, Grep, Bash(find:*), Bash(stat:*), Bash(mkdir:*), Bash(date:*), Bash(ls:*), mcp__context7__resolve-library-id, mcp__context7__get-library-docs, Write($JAAN_OUTPUTS_DIR/dev/docs/context7/**), AskUserQuestion
argument-hint: [library-names...]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# dev-docs-fetch

> Fetch and cache library documentation via Context7 MCP.

## Context Files

- `$JAAN_CONTEXT_DIR/tech.md` — Tech stack for library auto-detection
  - Uses sections: `#current-stack`, `#frameworks`
- `$JAAN_LEARN_DIR/jaan-to-dev-docs-fetch.learn.md` — Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` — Language resolution protocol

## Input

**Arguments**: $ARGUMENTS

- `[library-names...]` — Explicit library names (e.g., `fastapi react nextjs`)
- No arguments — Auto-detect from `$JAAN_CONTEXT_DIR/tech.md`

If no input and no tech.md, ask: "Which libraries do you need documentation for?"

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `dev-docs-fetch`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` — Know the tech stack for library detection

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_dev-docs-fetch`

> **Language exception**: Library names, Context7 IDs, package names, and cache file paths are NOT affected by this setting — always English.

---

## Token Budget & Efficiency Rules

**Target:** <10,000 tokens per execution

- Use Bash to check cache freshness before MCP calls (no file reads for fresh cache)
- Fetch only libraries relevant to current task
- Cache aggressively (7-day TTL)
- Max 3-5 libraries per run
- Report concisely (no verbose logging)

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Parse Arguments & Detect Libraries

**If $ARGUMENTS provided:**
Extract library names directly:
- Example: `/jaan-to:dev-docs-fetch fastapi openai` → `["fastapi", "openai"]`
- Example: `/jaan-to:dev-docs-fetch react` → `["react"]`

**If no arguments (auto-detection):**
1. Read `$JAAN_CONTEXT_DIR/tech.md` `#current-stack` section
2. Extract framework and library names from the tech stack
3. Map to Context7-searchable names (use the framework/library name as-is)
4. If tech.md missing → ask user for library names

**No hardcoded library tiers.** This skill is tech-agnostic — it reads whatever stack is declared in tech.md and resolves via Context7's search.

## Step 2: Cache Freshness Check

For each library to check, determine cache status:

**Cache path:** `$JAAN_OUTPUTS_DIR/dev/docs/context7/{library-name}.md`

```bash
CACHE_DIR="$JAAN_OUTPUTS_DIR/dev/docs/context7"
mkdir -p "$CACHE_DIR"
```

For each library (e.g., `fastapi`):

```bash
CACHE_FILE="$CACHE_DIR/fastapi.md"

if [ -f "$CACHE_FILE" ]; then
    FRESH=$(find "$CACHE_FILE" -mtime -7 -print 2>/dev/null)
    if [ -n "$FRESH" ]; then
        echo "FRESH"
    else
        if [ "$(uname)" = "Darwin" ]; then
            MTIME=$(stat -f %m "$CACHE_FILE")
        else
            MTIME=$(stat -c %Y "$CACHE_FILE")
        fi
        NOW=$(date +%s)
        DAYS=$(( ($NOW - $MTIME) / 86400 ))
        echo "STALE ($DAYS days)"
    fi
else
    echo "MISSING"
fi
```

Build lists:
- **FRESH**: Libraries with cache <7 days old — skip fetch
- **STALE**: Libraries with cache ≥7 days old — re-fetch
- **MISSING**: Libraries without cache — fetch

Present summary:
```
Cache Status:
✓ Fresh (N): lib1, lib2 (will skip)
↻ Stale (N): lib3 (X days old)
⬇ Missing (N): lib4, lib5

Will fetch: N libraries (stale + missing)
```

---

# HARD STOP — Confirm Fetch Plan

Use AskUserQuestion:
- Question: "Fetch {N} libraries? ({fetch-list})"
- Header: "Fetch"
- Options:
  - "Proceed" — Fetch listed libraries
  - "Edit list" — Modify which libraries to fetch
  - "Cancel" — Skip fetching

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Fetch & Store

## Step 3: Resolve Library IDs

For each library in the fetch list:

Use `mcp__context7__resolve-library-id`:
```
Input:
  libraryName: "{name}"

Expected Output:
  Context7-compatible library ID (e.g., /tiangolo/fastapi)
```

**Error handling — Library not found:**
```
⚠️ Library "{name}" not found in Context7

Options:
  retry <name> — Try different library name
  skip — Continue without this library
```

Wait for user input before proceeding.

## Step 4: Fetch Documentation

For each resolved library:

Use `mcp__context7__get-library-docs`:
```
Input:
  context7CompatibleLibraryID: "{resolved-id}"
  mode: "code"
  topic: (optional, extracted from task context)
```

**Mode selection:**
- Default: `mode="code"` (API references + code examples)
- Use `mode="info"` if task mentions: architecture, concepts, design patterns, how it works

**Topic extraction (optional):**
Extract specific topic from task description if mentioned:
- "FastAPI middleware" → `topic="middleware"`
- "React hooks" → `topic="hooks"`
If no specific topic, omit the `topic` parameter.

**Error handling — API failure:**
```
❌ Context7 API error for "{name}"

Fallback Strategy:
  Stale cache available: {name}.md ({age} days old)
  Use stale cache? (better than nothing)

Options:
  use-stale — Use stale cache
  skip — Continue without this library
  retry — Try again
```

**Error handling — Network timeout:**
Retry up to 3 times. After 3 failures, offer skip or use-stale.

## Step 5: Store Documentation

For each successfully fetched library:

**File path:** `$JAAN_OUTPUTS_DIR/dev/docs/context7/{library-name}.md`

**Naming convention:** Lowercase, hyphenated, match package name.
Examples: `fastapi.md`, `python-telegram-bot.md`, `nextjs.md`

**Handle created date:**
- If file exists (re-fetch): read existing frontmatter, preserve `created` date, update `updated`
- If new file: set both `created` and `updated` to today

**Write file with YAML frontmatter:**
```yaml
---
title: {Library Name} Documentation
library_id: {context7-compatible-library-id}
type: context7-reference
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
context7_mode: {code|info}
topic: {topic_if_specified|null}
tags: [context7, {library-name}, technical-reference]
source: Context7 MCP
cache_ttl: 7 days
---

{Full Context7 markdown response}
```

**Verify each write:**
```bash
ls -lh "$JAAN_OUTPUTS_DIR/dev/docs/context7/{library-name}.md"
```

## Step 6: Summary Report

```
Documentation Fetch Complete

Fetched (N):
  ✅ lib1.md (code mode, XX KB)
  ✅ lib2.md (info mode, topic: hooks, XX KB)

Cached - Fresh (N):
  ✓ lib3.md (X days old)

Skipped (N):
  ⚠️ lib4 (not found in Context7)

Storage: $JAAN_OUTPUTS_DIR/dev/docs/context7/
Total libraries available: N

Next step: Documentation ready for use in planning and implementation phases.
```

## Step 7: Suggest Next Actions

Context-aware recommendations:
- Docs fetched for backend libraries → suggest `/jaan-to:backend-scaffold` or `/jaan-to:dev-tech-plan`
- Docs fetched for frontend libraries → suggest `/jaan-to:frontend-scaffold`
- Docs fetched for testing libraries → suggest `/jaan-to:qa-test-generate`
- General → "Documentation ready for use in planning and implementation phases."

## Step 8: Capture Feedback

Use AskUserQuestion:
- Question: "How did the documentation fetch turn out?"
- Header: "Feedback"
- Options:
  - "Perfect!" — Done
  - "Missing library" — What library should we try to find?
  - "Learn from this" — Capture a lesson for future runs

If "Learn from this": Run `/jaan-to:learn-add dev-docs-fetch "{feedback}"`

---

## Scope Boundaries

- Does NOT generate code (only fetches and caches reference documentation)
- Does NOT modify project source files
- Does NOT start services or run builds
- Only writes to `$JAAN_OUTPUTS_DIR/dev/docs/context7/`
- Requires Context7 MCP server configured (`.mcp.json` for Claude Code, `~/.codex/config.toml` for Codex)

---

## DAG Position

```
(standalone — callable from any skill's Phase 1)
  |
  v
dev-docs-fetch
  |
  v
dev-tech-plan, backend-scaffold, frontend-scaffold, etc.
```

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Tech-agnostic via tech.md detection (no hardcoded library lists)
- Uses `$JAAN_*` environment variables throughout
- Learning integration via `$JAAN_LEARN_DIR`

## Definition of Done

- [ ] Cache checked before any fetch (7-day TTL enforced)
- [ ] Libraries fetched via Context7 MCP with YAML frontmatter
- [ ] Error handling covers: not found, API failure, timeout
- [ ] Summary report shown to user
- [ ] User feedback captured
