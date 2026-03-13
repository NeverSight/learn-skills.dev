---
name: refresh-docs
description: Incrementally update reverse-engineering docs based on git changes since they were last generated. Reads the commit hash from .stackshift-docs-meta.json, diffs against HEAD, analyzes only the changed files, and surgically updates the affected docs. Saves time and cost compared to full regeneration.
---

# Refresh Docs

**Incrementally update reverse-engineering docs from git changes — no full regeneration needed.**

**Estimated Time:** 2-15 minutes (depends on change volume)
**Prerequisites:** Reverse-engineering docs exist with `.stackshift-docs-meta.json`
**Output:** Updated docs in `docs/reverse-engineering/` with new commit hash

---

## When to Use This Skill

Use this skill when:
- Reverse-engineering docs already exist from a previous run
- Code has changed since docs were generated (new commits)
- You want to keep docs up to date without full regeneration
- Cost/time matters — only analyze what changed

**Trigger Phrases:**
- "Update the reverse-engineering docs"
- "Refresh the docs"
- "Sync docs with latest code"
- "What changed since docs were generated?"
- "Are the docs out of date?"

---

## What This Skill Does

```
Previous Docs (commit abc123)           Latest Code (commit def456)
┌─────────────────────────┐            ┌─────────────────────────┐
│ 11 reverse-eng docs     │            │ New commits since abc123│
│ .stackshift-docs-meta   │──── diff ──│ Changed files list      │
└─────────────────────────┘            └─────────────────────────┘
                                                │
                                       Analyze only changes
                                                │
                                                ▼
                                       Updated docs + new hash
```

1. Reads the pinned commit hash from `.stackshift-docs-meta.json`
2. Runs `git diff` between that hash and HEAD
3. Categorizes changed files by which docs they affect
4. Analyzes only the changed code
5. Surgically updates affected sections in the relevant docs
6. Updates the commit hash in metadata

---

## Process

### Step 1: Read Metadata and Assess Changes

```bash
# Read the pinned commit hash
META_FILE="docs/reverse-engineering/.stackshift-docs-meta.json"

if [ ! -f "$META_FILE" ]; then
  echo "ERROR: No metadata file found. Run /stackshift.reverse-engineer first."
  exit 1
fi

PINNED_HASH=$(cat "$META_FILE" | jq -r '.commit_hash')
CURRENT_HASH=$(git rev-parse HEAD)
PINNED_DATE=$(cat "$META_FILE" | jq -r '.commit_date')

echo "Docs pinned to: $PINNED_HASH ($PINNED_DATE)"
echo "Current HEAD:   $CURRENT_HASH"

if [ "$PINNED_HASH" = "$CURRENT_HASH" ]; then
  echo "Docs are up to date. Nothing to refresh."
  exit 0
fi

# Count commits since docs were generated
COMMIT_COUNT=$(git rev-list --count "$PINNED_HASH".."$CURRENT_HASH" 2>/dev/null || echo "unknown")
echo "Commits since last generation: $COMMIT_COUNT"
```

### Step 2: Get Changed Files and Commit Summary

```bash
# Get list of changed files with change type
git diff --name-status "$PINNED_HASH"..HEAD

# Get commit log summary (for context)
git log --oneline "$PINNED_HASH"..HEAD

# Get a statistical summary
git diff --stat "$PINNED_HASH"..HEAD
```

**Present to user:**
```
Docs were generated at commit abc1234 (2025-12-15)
Current HEAD: def4567 (2026-02-12)

42 commits, 156 files changed:
  src/api/        - 12 files (endpoints, middleware)
  src/models/     - 3 files (User, Product schemas)
  src/services/   - 8 files (business logic)
  package.json    - dependency updates
  .env.example    - new env vars
  docker-compose  - infrastructure changes
  tests/          - 15 new test files

Estimated refresh time: ~5 minutes
```

### Step 3: Map Changes to Affected Docs

Categorize each changed file by which reverse-engineering doc(s) it affects:

| Changed File Pattern | Affected Doc(s) |
|---|---|
| `src/api/**`, `routes/**`, `controllers/**` | functional-specification.md, integration-points.md, data-architecture.md |
| `src/models/**`, `schema/**`, `prisma/**`, `migrations/**` | data-architecture.md |
| `src/services/**`, `src/lib/**`, `src/utils/**` | functional-specification.md |
| `package.json`, `go.mod`, `requirements.txt` | decision-rationale.md, configuration-reference.md |
| `.env*`, `config/**`, `*.config.*` | configuration-reference.md |
| `docker*`, `terraform/**`, `k8s/**`, `.github/**` | operations-guide.md |
| `tests/**`, `__tests__/**`, `*.test.*`, `*.spec.*` | test-documentation.md |
| `src/components/**`, `src/pages/**`, `styles/**` | visual-design-system.md |
| `README*`, `CHANGELOG*`, `docs/**` | business-context.md |
| Infrastructure/monitoring files | observability-requirements.md |
| Any tech stack changes | decision-rationale.md |
| External service integrations | integration-points.md |

**Files that don't map to any doc** (e.g., `.gitignore` changes) can be skipped.

**Output a refresh plan:**
```
Docs to update:
  functional-specification.md  - 8 changed files affect this doc
  data-architecture.md         - 3 changed files (schema changes)
  configuration-reference.md   - 2 changed files (new env vars)
  test-documentation.md        - 15 new test files

Docs unchanged:
  visual-design-system.md      - no UI changes detected
  observability-requirements.md - no monitoring changes
  business-context.md          - no business context changes
  decision-rationale.md        - no tech stack changes
  operations-guide.md          - no infra changes
  integration-points.md        - no integration changes
  technical-debt-analysis.md   - no debt-relevant changes
```

### Step 4: Analyze Changes and Update Docs

For each affected doc, use the Task tool with `subagent_type=Explore` (or `stackshift:code-analyzer`) to:

1. **Read the current doc** to understand its structure and content
2. **Read the changed files** that map to this doc
3. **Read the git diff** for those files to understand what specifically changed
4. **Determine updates needed:**
   - New sections to add (e.g., new API endpoint → new FR)
   - Existing sections to modify (e.g., schema change → update data model)
   - Sections to remove (e.g., deleted feature → remove FR)
   - No change needed (e.g., refactor that doesn't change behavior)

**Update strategy per change type:**

| Change Type | Update Approach |
|---|---|
| **New file** (Added) | Add new section/entry to relevant doc |
| **Modified file** | Read diff, update affected sections, preserve unchanged |
| **Deleted file** | Mark related sections as removed or deprecated |
| **Renamed file** | Update file paths in brownfield docs |
| **New dependency** | Add to decision-rationale.md and/or integration-points.md |
| **Config change** | Update configuration-reference.md |
| **New test** | Update test-documentation.md coverage |

**Important: Surgical updates only.** Do NOT rewrite entire docs. Edit specific sections using the Edit tool to preserve unchanged content.

### Step 5: Update Metadata

After all docs are updated, update the metadata file:

```bash
NEW_HASH=$(git rev-parse HEAD)
NEW_DATE=$(git log -1 --format=%ci)
REFRESHED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
```

Update `docs/reverse-engineering/.stackshift-docs-meta.json`:
- Set `commit_hash` to new HEAD
- Set `commit_date` to new date
- For each updated doc, set its `generated_at` to now and `commit_hash` to new HEAD
- For unchanged docs, keep their original timestamps
- Add a `refresh_history` array tracking each refresh:

```json
{
  "commit_hash": "<NEW_HASH>",
  "commit_date": "<NEW_DATE>",
  "generated_at": "<original generation date>",
  "last_refreshed_at": "<REFRESHED_AT>",
  "doc_count": 11,
  "route": "brownfield",
  "refresh_history": [
    {
      "from_commit": "<OLD_HASH>",
      "to_commit": "<NEW_HASH>",
      "refreshed_at": "<REFRESHED_AT>",
      "commits_analyzed": 42,
      "files_changed": 156,
      "docs_updated": ["functional-specification.md", "data-architecture.md", "configuration-reference.md", "test-documentation.md"],
      "docs_unchanged": ["visual-design-system.md", "observability-requirements.md", "..."]
    }
  ],
  "docs": {
    "functional-specification.md": { "generated_at": "<original>", "last_updated": "<REFRESHED_AT>", "commit_hash": "<NEW_HASH>" },
    "data-architecture.md": { "generated_at": "<original>", "last_updated": "<REFRESHED_AT>", "commit_hash": "<NEW_HASH>" },
    "configuration-reference.md": { "generated_at": "<original>", "last_updated": "<REFRESHED_AT>", "commit_hash": "<NEW_HASH>" },
    "test-documentation.md": { "generated_at": "<original>", "last_updated": "<REFRESHED_AT>", "commit_hash": "<NEW_HASH>" },
    "visual-design-system.md": { "generated_at": "<original>", "last_updated": "<original>", "commit_hash": "<OLD_HASH>" },
    "...": "unchanged docs keep old timestamps"
  }
}
```

### Step 6: Update Doc Headers

For each updated doc, update the metadata header line:

```markdown
> **Generated by StackShift** | Commit: `<new-short-hash>` | Updated: `<REFRESHED_AT>` | Originally generated: `<original-date>`
```

### Step 7: Present Summary

```
Docs Refresh Complete
═════════════════════

Analyzed: 42 commits (abc1234 → def4567)
Changed files: 156
Time: 4 minutes

Updated docs (4):
  functional-specification.md
    + Added FR-008: Bulk export feature
    ~ Updated FR-003: Modified user registration flow
    - Removed FR-005: Legacy import (deleted)

  data-architecture.md
    + Added Product.variants field
    ~ Updated User model (new preferences column)

  configuration-reference.md
    + Added EXPORT_BATCH_SIZE env var
    + Added REDIS_CLUSTER_URL env var

  test-documentation.md
    ~ Coverage updated: 67% → 74%
    + 15 new test files documented

Unchanged docs (7):
  visual-design-system.md, observability-requirements.md,
  business-context.md, decision-rationale.md, operations-guide.md,
  integration-points.md, technical-debt-analysis.md

Next refresh: Run /stackshift.refresh-docs again after more commits.
```

---

## Modes

### Default: Smart Refresh
- Only updates docs affected by changes
- Preserves unchanged sections
- Fast and cost-effective

### Full Refresh (override)
If the user says "do a full refresh" or changes are too extensive (100+ files, major refactor):
- Regenerate all 11 docs from scratch using `/stackshift.reverse-engineer`
- Equivalent to a full Gear 2 run
- Use when: major refactors, framework migrations, or when incremental updates would miss systemic changes

**Auto-detect when full refresh is recommended:**
- More than 60% of source files changed
- Package.json/go.mod major version bumps
- New top-level directories added
- Framework migration detected (e.g., Express → Fastify)

```
Large change detected: 78% of source files modified.
A full refresh is recommended over incremental update.

A) Full refresh (regenerate all docs, ~30 min)
B) Incremental anyway (faster but may miss systemic changes)
```

---

## Edge Cases

### Docs exist but no metadata file
Legacy docs from before commit tracking. Offer two options:
1. Run `/stackshift.reverse-engineer` to regenerate with metadata
2. Create metadata file pinned to current HEAD (treats current docs as up-to-date)

### Pinned commit no longer exists
The commit was rebased or force-pushed away. Fall back to full refresh.

### No git repository
Not a git repo. Cannot do incremental updates. Guide user to full regeneration.

### Merge commits
When the diff spans merge commits, use `git diff` (not `git log -p`) to get the net effect rather than per-commit changes.

---

## Integration

### With Cruise Control
Cruise control can optionally run refresh-docs instead of full reverse-engineer if docs already exist:
```
Existing docs detected (pinned to abc1234, 15 commits behind).
A) Refresh docs incrementally (~5 min)
B) Full regeneration (~30 min)
```

### With Batch Processing
Batch mode can run refresh-docs on repos that already have docs, saving significant time when re-processing a large monorepo.

### With CI/CD
Can be run in CI to keep docs updated on every merge to main:
```yaml
- name: Refresh StackShift docs
  run: |
    # Check if docs need refresh
    if [ -f "docs/reverse-engineering/.stackshift-docs-meta.json" ]; then
      echo "Refreshing docs..."
      # Trigger /stackshift.refresh-docs
    fi
```

---

## Success Criteria

- ✅ Changes since pinned commit identified and categorized
- ✅ Only affected docs updated (unchanged docs preserved)
- ✅ Metadata file updated with new commit hash
- ✅ Refresh history logged
- ✅ Doc headers updated with new timestamps
- ✅ Summary shows what was added/modified/removed per doc

---

## Technical Notes

- Use `git diff --name-status` for file-level change detection (fast)
- Use `git diff <hash>..HEAD -- <file>` for content-level analysis of specific files
- Parallelize: Read changed files for different docs concurrently using Task agents
- For large diffs (500+ files), batch the analysis into groups of 50 files
- Preserve doc structure — use Edit tool for surgical updates, not Write for full rewrites
- The metadata JSON should be committed to git so team members share the same pinned hash
