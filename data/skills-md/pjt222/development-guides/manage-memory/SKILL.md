---
name: manage-memory
description: >
  Organize, extract, prune, and verify Claude Code persistent memory files.
  Covers MEMORY.md as a concise index, topic extraction to dedicated files,
  staleness detection, accuracy verification against project state, and
  the 200-line truncation constraint. Use when MEMORY.md is approaching the
  200-line limit, after a session produces durable insights worth preserving,
  when a topic section has grown beyond 10-15 lines and should be extracted,
  or when project state has changed and memory entries may be stale.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: general
  complexity: intermediate
  language: multi
  tags: memory, claude-code, organization, maintenance, auto-memory
---

# Manage Memory

Maintain Claude Code's persistent memory directory so it stays accurate, concise, and useful across sessions. MEMORY.md is loaded into the system prompt on every conversation — lines after 200 are truncated, so this file must be a lean index pointing to topic files for detail.

## When to Use

- MEMORY.md is approaching the 200-line truncation threshold
- A session produced durable insights worth preserving (new patterns, architecture decisions, debugging solutions)
- A topic section in MEMORY.md has grown beyond 10-15 lines and should be extracted
- Project state has changed (renamed files, new domains, updated counts) and memory entries may be stale
- Starting a new area of work and checking whether relevant memory already exists
- Periodic maintenance between sessions to keep the memory directory healthy

## Inputs

- **Required**: Access to the memory directory (typically `~/.claude/projects/<project-path>/memory/`)
- **Optional**: Specific trigger (e.g., "MEMORY.md is too long," "just finished a major refactor")
- **Optional**: Topic to add, update, or extract

## Procedure

### Step 1: Assess Current State

Read MEMORY.md and list all files in the memory directory:

```bash
wc -l <memory-dir>/MEMORY.md
ls -la <memory-dir>/
```

Check the line count against the 200-line limit. Inventory existing topic files.

**Expected:** Clear picture of total lines, number of topic files, and which sections exist in MEMORY.md.

**On failure:** If the memory directory doesn't exist, create it. If MEMORY.md doesn't exist, create a minimal one with a `# Project Memory` header and a `## Topic Files` section.

### Step 2: Identify Stale Entries

Compare memory claims against current project state. Common staleness patterns:

1. **Count drift**: File counts, skill counts, domain counts that changed after additions/removals
2. **Renamed paths**: Files or directories that were moved or renamed
3. **Superseded patterns**: Workarounds that are no longer needed after fixes
4. **Contradictions**: Two entries that say different things about the same topic

Use Grep to spot-check key claims:

```bash
# Example: verify a skill count claim
grep -c "^      - id:" skills/_registry.yml
# Example: verify a file still exists
ls path/claimed/in/memory.md
```

**Expected:** A list of entries that are stale, with the correct current values.

**On failure:** If you can't verify a claim (e.g., it references external state you can't check), leave it but add a `(unverified)` note rather than silently preserving potentially wrong information.

### Step 3: Decide What to Add

For new entries, apply these filters before writing:

1. **Durability**: Will this be true next session? Avoid session-specific context (current task, in-progress work, temporary state).
2. **Non-duplication**: Does CLAUDE.md or project documentation already cover this? Don't duplicate — memory is for things NOT captured elsewhere.
3. **Verified**: Has this been confirmed across multiple interactions, or is it a single observation? For single observations, verify against project docs before writing.
4. **Actionable**: Does knowing this change behavior? "The sky is blue" isn't useful. "Exit code 5 means quoting error — use temp files" changes how you work.

Exception: If the user explicitly asks to remember something, save it immediately — no need to wait for multiple confirmations.

**Expected:** A filtered list of entries worth adding, each meeting durability + non-duplication + verification + actionability criteria.

**On failure:** If unsure whether an entry is worth keeping, err toward keeping it briefly in MEMORY.md — it's easier to prune later than to rediscover.

### Step 4: Extract Oversize Topics

When a section in MEMORY.md exceeds ~10-15 lines, extract it to a dedicated topic file:

1. Create `<memory-dir>/<topic-name>.md` with a descriptive header
2. Move the detailed content from MEMORY.md to the topic file
3. Replace the section in MEMORY.md with a 1-2 line summary and a link:

```markdown
## Topic Files
- [topic-name.md](topic-name.md) — Brief description of contents
```

Naming conventions for topic files:
- Use lowercase kebab-case: `viz-architecture.md`, not `VizArchitecture.md`
- Name by topic, not chronology: `patterns.md`, not `session-2024-12.md`
- Group related items: combine "R debugging" and "WSL quirks" into `patterns.md` rather than creating one file per fact

**Expected:** MEMORY.md stays under 200 lines. Each topic file is self-contained and readable without MEMORY.md context.

**On failure:** If a topic file would be fewer than 5 lines, it's probably not worth extracting — leave it inline in MEMORY.md.

### Step 5: Update MEMORY.md

Apply all changes: remove stale entries, add new entries, update counts, and ensure the Topic Files section lists all dedicated files.

MEMORY.md structure should follow this pattern:

```markdown
# Project Memory

## Section 1 — High-level context
- Bullet points, concise

## Section 2 — Another topic
- Key facts only

## Topic Files
- [file.md](file.md) — What it covers
```

Guidelines:
- Keep each bullet to 1-2 lines maximum
- Use inline formatting (`code`, **bold**) for scanability
- Put the most frequently needed context first
- The Topic Files section should always be last

**Expected:** MEMORY.md is under 200 lines, accurate, and has working links to all topic files.

**On failure:** If you can't get under 200 lines after extraction, identify the least-frequently-used section and extract it. Every section is a candidate — even the project structure overview can go to a topic file if needed, leaving just a 1-line summary.

### Step 6: Verify Integrity

Run a final check:

1. **Line count**: Confirm MEMORY.md is under 200 lines
2. **Links**: Verify every topic file referenced in MEMORY.md exists
3. **Orphans**: Check for topic files not referenced in MEMORY.md
4. **Accuracy**: Spot-check 2-3 factual claims against project state

```bash
wc -l <memory-dir>/MEMORY.md
# Check for broken links
for f in $(grep -oP '\[.*?\]\(\K[^)]+' <memory-dir>/MEMORY.md); do
  ls <memory-dir>/$f 2>/dev/null || echo "BROKEN: $f"
done
# Check for orphan files
ls <memory-dir>/*.md | grep -v MEMORY.md
```

**Expected:** Line count under 200, no broken links, no orphan files, spot-checked claims are accurate.

**On failure:** Fix broken links (update or remove). For orphan files, either add a reference in MEMORY.md or delete them if they're no longer relevant.

## Validation

- [ ] MEMORY.md is under 200 lines
- [ ] All topic files referenced in MEMORY.md exist on disk
- [ ] No orphan `.md` files in memory directory (every file is linked from MEMORY.md)
- [ ] No stale counts or renamed paths in any memory file
- [ ] New entries meet the durability/non-duplication/verified/actionable criteria
- [ ] Topic files have descriptive headers and are self-contained
- [ ] MEMORY.md reads as a useful quick-reference, not a changelog

## Common Pitfalls

- **Memory file pollution**: Writing every session observation to memory. Most findings are session-specific and don't need persisting. Apply the four filters (Step 3) before writing.
- **Stale counts**: Updating code but not memory. Counts (skills, agents, domains, files) drift silently. Always verify counts against the source of truth before trusting memory.
- **Chronological organization**: Organizing by "when I learned it" instead of "what it's about." Topic-based organization (`patterns.md`, `viz-architecture.md`) is far more useful for retrieval than date-based files.
- **Duplicating CLAUDE.md**: CLAUDE.md is the authoritative project instruction file. Memory should capture things NOT in CLAUDE.md — debugging insights, architecture decisions, workflow preferences, cross-project patterns.
- **Over-extraction**: Creating a topic file for every 3-line section. Only extract when a section exceeds ~10-15 lines. Small sections work fine inline.
- **Forgetting the 200-line limit**: MEMORY.md is loaded into every system prompt. Lines after 200 are silently truncated. If the file grows past this, the bottom content is effectively invisible.

## Related Skills

- `write-claude-md` — CLAUDE.md captures project instructions; memory captures cross-session learning
- `create-skill` — new skills may produce memory-worthy patterns
- `heal` — self-healing may update memory as part of integration step
- `meditate` — meditation sessions may surface insights worth persisting
