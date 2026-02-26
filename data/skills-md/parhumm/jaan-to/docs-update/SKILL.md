---
name: docs-update
description: Audit and maintain documentation quality using smart staleness checks. Use when reviewing or fixing documentation.
allowed-tools: Read, Glob, Grep, Write($JAAN_DOCS_DIR/**), Write($JAAN_OUTPUTS_DIR/**), Edit($JAAN_DOCS_DIR/**), Edit(jaan-to/config/settings.yaml), Bash(git add:*), Bash(git commit:*), Bash(git log:*), Bash(git mv:*)
argument-hint: "[path] [--full] [--fix] [--check-only] [--quick]"
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# docs-update

> Smart documentation auditing with git-based staleness detection.

## Context Files

- `${CLAUDE_PLUGIN_ROOT}/docs/STYLE.md` - Documentation standards (read from plugin source)
- `$JAAN_TEMPLATES_DIR/jaan-to-docs.template.md` - Shared docs template (shared with docs-create)
- `$JAAN_LEARN_DIR/jaan-to-docs.learn.md` - Shared docs lessons (shared with docs-create, loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

**Note:** STYLE.md is read from the plugin source. Templates are read from `$JAAN_TEMPLATES_DIR`. Pre-execution protocol Step C offers to seed from the plugin on first use.

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `docs-update`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)
**Shared resource override:** Template and learn files are shared with `docs-create`. For Steps A/B/C, resolve using `docs` as the resource name:
- Learn: `$JAAN_LEARN_DIR/jaan-to-docs.learn.md` (fallback: `${CLAUDE_PLUGIN_ROOT}/skills/docs-create/LEARN.md`)
- Template: `$JAAN_TEMPLATES_DIR/jaan-to-docs.template.md` (fallback: `${CLAUDE_PLUGIN_ROOT}/skills/docs-create/template.md`)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_docs-update`

---

## File Mapping (Code → Docs)

| Code Path | Related Doc |
|-----------|-------------|
| `skills/{name}/SKILL.md` | `$JAAN_DOCS_DIR/skills/{role}/{slug}.md` |
| `$JAAN_LEARN_DIR/{name}.learn.md` | (referenced in skill doc) |
| `$JAAN_CONTEXT_DIR/hooks/{name}.sh` | `$JAAN_DOCS_DIR/hooks/{name}.md` |
| `$JAAN_CONTEXT_DIR/config.md` | `$JAAN_DOCS_DIR/config/README.md` |
| `$JAAN_CONTEXT_DIR/*.md` | `$JAAN_DOCS_DIR/config/context.md` |
| `$JAAN_CONTEXT_DIR/boundaries.md` | `$JAAN_DOCS_DIR/config/boundaries.md` |

**Slug extraction:** `pm-prd-write` → `prd-write` (remove role prefix)

---

# PHASE 0: Smart Default - Staleness Detection

**Goal:** Find docs that are out of sync with their source code.

**Trigger:** Run with NO arguments or just `--fix`

## Step 0.1: Parse Arguments

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| (none) | Smart default: staleness check |
| `[path]` | Check specific path only |
| `--full` | Skip staleness, do full audit |
| `--fix` | Auto-fix issues |
| `--check-only` | Report only, no changes |
| `--quick` | Inventory only |

**If `--full` or `[path]` provided:** Skip to PHASE 1 (Quick Inventory)

## Step 0.2: Get Recent Code Changes

```bash
git log --since="30 days ago" --name-only --pretty=format: -- skills/ $JAAN_CONTEXT_DIR/hooks/ $JAAN_CONTEXT_DIR/config.md $JAAN_CONTEXT_DIR/ | sort -u | grep -v '^$'
```

Extract unique changed files.

## Step 0.3: Map Code Files to Docs

For each changed code file, find related doc:

**Skills:**
```
skills/{name}/SKILL.md → $JAAN_DOCS_DIR/skills/{role}/{slug}.md

# Extract slug: remove brand prefix and role
# pm-prd-write → prd-write
# learn-add → learn-add (core role)
```

**Hooks:**
```
$JAAN_CONTEXT_DIR/hooks/{name}.sh → $JAAN_DOCS_DIR/hooks/{name}.md
```

**Config:**
```
$JAAN_CONTEXT_DIR/config.md → $JAAN_DOCS_DIR/config/README.md
$JAAN_CONTEXT_DIR/*.md → $JAAN_DOCS_DIR/config/context.md
$JAAN_CONTEXT_DIR/boundaries.md → $JAAN_DOCS_DIR/config/boundaries.md
```

## Step 0.4: Compare Timestamps

For each code→doc pair:
```bash
# Get code last modified
git log -1 --format=%ai -- {code_path}

# Get doc last modified
git log -1 --format=%ai -- {doc_path}
```

**Staleness threshold:** 7 days
- If code_date > doc_date + 7 days → Flag as STALE

## Step 0.5: Check for Missing Docs

```bash
# Check if expected doc exists
git ls-files -- {expected_doc_path}
```

If code exists but doc doesn't → Flag as MISSING

## Step 0.6: Generate Staleness Report

```markdown
# Documentation Staleness Report
**Date:** {date} | **Code changes:** {n} files | **Docs checked:** {n}

## Potentially Outdated

| Doc | Related Code | Code Changed | Doc Updated | Delta |
|-----|--------------|--------------|-------------|-------|
| $JAAN_DOCS_DIR/skills/pm/prd-write.md | skills/pm-prd-write/SKILL.md | 2026-01-25 | 2026-01-10 | 15d stale |

## Missing Documentation

| Code File | Expected Doc | Action |
|-----------|--------------|--------|
| skills/new-skill/SKILL.md | $JAAN_DOCS_DIR/skills/?/new-skill.md | Create |

## Up to Date

✅ {n} docs are current (code and doc in sync)

---

What would you like to do?
[1] Review stale docs one by one
[2] Full audit (check everything)
[3] Quick fix (update dates only)
[4] Exit
```

**HARD STOP:** Wait for user choice.

**Option 1:** For each stale doc, show side-by-side what changed in code, ask what to update.
**Option 2:** Continue to PHASE 1 (full audit).
**Option 3:** Just update `updated_date` in stale docs.
**Option 4:** Stop.

---

# PHASE 1: Quick Inventory

**Goal:** Understand documentation state without reading everything.

**Trigger:** `--full`, `[path]` argument, or user chose Option 2 from staleness report

## Step 1.1: Inventory Files

Use Glob to count docs (don't read all):
```
Glob: $JAAN_DOCS_DIR/**/*.md
```

Exclude: `node_modules/`

## Step 1.2: Check Recent Doc Changes

```bash
git log --since="30 days ago" --oneline --name-only -- $JAAN_DOCS_DIR/ | head -30
```

## Step 1.3: Quick Scan for Issues

Use Grep to detect problems without reading files:

**Missing frontmatter:**
```
Grep: "^---$" in $JAAN_DOCS_DIR/**/*.md (check first line)
```

**Missing tagline:**
```
Grep: "^>" in $JAAN_DOCS_DIR/**/*.md
```

## Step 1.4: Generate Audit Proposal

```markdown
## Documentation Audit Proposal

**Files found:** X docs
**Recent changes:** X files in last 30 days

### Quick Scan Results
- Missing frontmatter: X files
- Missing tagline: X files
- Potential issues: X files

Proceed with full audit? [yes/no/quick-fixes-only]
```

**If `--quick`:** Stop here.
**If "no":** Stop here.
**If "quick-fixes-only":** Only fix frontmatter/dates.
**If "yes":** Continue to full audit.

---

# PHASE 2: Full Analysis

## Step 2.1: Progressive File Loading

Load files one at a time to save tokens.
For each file, check:

### Frontmatter Validation

```yaml
---
title: Required
doc_type: Required (skill|hook|config|guide|concept|index)
created_date: Required (YYYY-MM-DD)
updated_date: Required (YYYY-MM-DD)
tags: Required (array)
---
```

### Structure Validation

- [ ] Has H1 title (only one)
- [ ] Has tagline (`> description`)
- [ ] Sections separated with `---`
- [ ] No H4+ headings
- [ ] Under line limit for type

### Link Validation

Check all internal links:
- `[text](path.md)` - file exists?
- `[text](../path.md)` - relative path valid?

### README Index Consistency

For each `$JAAN_DOCS_DIR/skills/{role}/README.md`:

1. **List all `.md` files** in the same directory (excluding README.md itself)
2. **Parse the "## Available Skills" table** rows in the README
3. **Compare and flag:**
   - **MISSING**: `.md` file exists in directory but not listed in Available Skills table
   - **PHANTOM**: Listed in table but `.md` file doesn't exist in directory
   - **STALE DESCRIPTION**: Description in table differs significantly from the skill's SKILL.md `description:` field

4. **Also check `$JAAN_DOCS_DIR/skills/README.md` root Available Roles table:**
   - Compare against actual `$JAAN_DOCS_DIR/skills/*/` subdirectories that contain files
   - Flag roles with directories but missing from table as MISSING ROLE
   - Flag roles listed as "Planned" that have active skill docs as STALE STATUS

5. **Report findings** in the audit report under a "## README Index Consistency" section

**Auto-fix logic** (Phase 3):
- MISSING → add row to table using description from SKILL.md frontmatter
- PHANTOM → remove row or ask user for decision
- STALE DESCRIPTION → update description from SKILL.md
- MISSING ROLE → add row to root Available Roles table with "Active" status
- STALE STATUS → update "Planned" to "Active" in root table

### Duplication Detection

Compare similar docs for overlap:

| Overlap | Action |
|---------|--------|
| >80% | Flag for consolidation |
| 50-80% | Suggest differentiation |
| <50% | Keep separate |

### Location Check

Verify docs are in correct folders:

| Content Type | Correct Location |
|--------------|------------------|
| Skill docs | `$JAAN_DOCS_DIR/skills/{role}/` |
| Hook docs | `$JAAN_DOCS_DIR/hooks/` |
| Config docs | `$JAAN_DOCS_DIR/config/` |
| Guides | `$JAAN_DOCS_DIR/extending/` |

## Step 2.2: Compile Issues

Categorize findings:

| Category | Icon | Description |
|----------|------|-------------|
| Healthy | ✅ | No issues |
| Need Updates | ⚠️ | Minor fixes needed |
| Deprecated | 🔴 | Archive candidate |
| Duplicates | 📦 | Consolidation needed |
| Misplaced | 📁 | Wrong location |

---

# HARD STOP - Audit Report

Show audit report:

```markdown
# Documentation Audit Report
**Date:** {date} | **Files:** {count} | **Issues:** {count}

## Summary
| Category | Count | Action |
|----------|-------|--------|
| ✅ Healthy | X | None |
| ⚠️ Need Updates | X | Update |
| 🔴 Deprecated | X | Archive |
| 📦 Duplicates | X | Consolidate |
| 📁 Misplaced | X | Move |

## Priority Actions

### High Priority
1. **{file}** - {issue} - {action}

### Medium Priority
2. **{file}** - {issue} - {action}

### Low Priority
3. **{file}** - {issue} - {action}

---

Apply fixes? [yes/no/selective]
```

**If `--check-only`:** Stop here.
**Do NOT proceed without explicit approval.**

---

# PHASE 3: Apply Fixes

## Step 3.1: Archive Deprecated Docs

```bash
mkdir -p $JAAN_DOCS_DIR/archive
git mv $JAAN_DOCS_DIR/deprecated-file.md $JAAN_DOCS_DIR/archive/
```

Add note at top: "ARCHIVED: See [new-doc.md] for current information."

## Step 3.2: Consolidate Duplicates

1. Read both documents
2. Merge best content into primary
3. Archive the duplicate
4. Update cross-references

## Step 3.3: Fix Frontmatter

Add missing frontmatter:
```yaml
---
title: [Inferred from H1]
doc_type: [Inferred from path]
created_date: [From git log or today]
updated_date: [Today]
tags: [Inferred from content]
---
```

## Step 3.4: Fix Structure

- Add missing `---` separators
- Convert H4+ to H3 or bullets
- Add missing tagline (ask user)

## Step 3.5: Fix Links

- Report broken links with suggestions
- Update paths for moved files

## Step 3.6: Update Dates

For any modified file:
```yaml
updated_date: {today}
```

## Step 3.7: Move Misplaced Files

```bash
git mv $JAAN_DOCS_DIR/wrong-location/file.md $JAAN_DOCS_DIR/correct-location/
```

Update any references to moved file.

---

# PHASE 4: Commit & Report

## Step 4.1: Commit Changes

Ask: "Commit documentation updates? [y/n]"

If yes:
```bash
git add $JAAN_DOCS_DIR/
git commit -m "docs: Audit and update documentation

- Fixed: X files
- Archived: X files
- Moved: X files

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Step 4.2: Final Report

```markdown
✅ Documentation audit complete!

## Changes Applied
- Fixed frontmatter: X files
- Fixed structure: X files
- Archived: X files
- Moved: X files
- Updated dates: X files

## Documentation Health: [EXCELLENT/GOOD/NEEDS WORK]

Commit: {hash}
```

---

## Error Handling

### No Docs Found
> "No documentation files found in `{path}`."

### Permission Denied
> "Cannot modify `{file}`. Check permissions."

### Git Not Available
> "Git not available. Changes saved but not committed."

---

## Trust Rules

1. **NEVER** delete without approval (archive instead)
2. **ALWAYS** preserve content when consolidating
3. **ASK** before major changes
4. **SKIP** generated files (jaan-to/)
5. **BACKUP** before bulk operations
6. **PREVIEW** all changes before applying

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

- [ ] Staleness check completed across all doc paths
- [ ] Stale or missing docs identified and reported
- [ ] Fixes applied (if --fix mode) or report generated (if --check-only)
- [ ] User approved changes
