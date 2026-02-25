---
name: help-me-review
disable-model-invocation: true
description: Organize large code diffs into small, prioritized, human-reviewable sections with an interactive HTML viewer. 
---

# Help Me Review

Organize large diffs into small, logically grouped sections ordered by importance, generate an interactive HTML review page, and process user feedback.

## Workflow

### 1. Get the raw diff

Create a working directory inside the project for this review session, then capture the diff:

```bash
REVIEW_DIR=".review"
mkdir -p "$REVIEW_DIR"

# PR (preferred if user provides PR number)
gh pr diff <PR_NUMBER> > "$REVIEW_DIR/raw.diff"

# Current branch vs main
git diff main...HEAD > "$REVIEW_DIR/raw.diff"

# Between two refs
git diff <base>..<head> > "$REVIEW_DIR/raw.diff"
```

If `.review` already exists from a previous session, remove it first (`rm -rf .review`).

### 2. Split into blocks

Split the raw diff into individual block files (one per hunk). This also generates an index with a summary of all blocks.

```bash
node <skill_path>/scripts/split_blocks.mjs "$REVIEW_DIR/raw.diff" "$REVIEW_DIR/blocks"
```

### 3. Read and analyze

Read `$REVIEW_DIR/blocks/index.md` — it contains every block with annotated line numbers (Old and New columns). Use this as your primary reference for understanding changes and for writing comment line numbers later.

For large diffs, also read individual block files (`block-001.diff`, `block-002.diff`, etc.) in batches if you need the full context around hunks.

**Read every block.** Do not skip any. You must understand all changes before grouping them.

**Read the source files too.** Diffs only show changed lines with limited context. For every file touched by the diff, read the full file (or the relevant surrounding code) to understand what the change actually does. This is essential for writing accurate section descriptions and useful comments — you cannot judge the impact of a change without knowing the code around it.

Plan how to group blocks into sections. **Sections are reviewer thought units, not file boundaries.** A section should contain every piece of the diff that a reviewer needs to understand one logical change — even when those pieces are scattered across multiple files.

A section titled "Authentication flow" should contain the middleware hunk from `auth.ts`, the route changes from `user.ts`, and the config addition from `settings.ts` — all the pieces a reviewer needs to understand the auth change. A section titled "Add pagination to list endpoints" should pull together the utility function, the route handlers that call it, and the tests that exercise it.

**If a section contains only one file, ask yourself: are there related changes in other files that belong here?** Single-file sections are a smell — they usually mean the grouping is too shallow. Multi-file sections that track a single concern are the goal.

**Order sections for progressive understanding.** Put foundational changes first: types, interfaces, data models, shared utilities. Then show the code that uses them. The reviewer should see the "what" before the "how." Within that structure, prioritize by importance:

1. Security-sensitive code, API contract changes, data model changes, breaking changes
2. Feature implementation, business logic, error handling, significant refactors
3. Config changes, imports, formatting, type annotations, dependency updates, test-only changes

**Section descriptions should answer:** what is the reviewer looking at, and what should they pay attention to? Not just a label — a sentence that orients the reviewer.

**Size guideline:** aim for 5-50 changed lines per section. Split large concerns into sub-sections if needed.

**Every block number from index.md must appear in exactly one section.** No block may be omitted or duplicated.

### 4. Write manifest

Write `$REVIEW_DIR/manifest.json`. Array order = display order (first = most important). Each section includes a `comments` array of inline annotations that will appear directly on diff lines in the review viewer.

```json
{
  "title": "PR title or short description",
  "base": "main",
  "head": "feature/branch",
  "sections": [
    {
      "title": "Auth middleware refactor",
      "description": "Token validation extracted into standalone middleware",
      "blocks": [1, 2],
      "comments": [
        {
          "file": "src/middleware/auth.ts",
          "line": 42,
          "side": "new",
          "body": "Replaces the inline token check from the route handler. Expiry validation is new."
        }
      ]
    },
    {
      "title": "API routes",
      "description": "Profile endpoint updated to use new auth middleware instead of inline checks",
      "blocks": [3, 4],
      "comments": []
    }
  ]
}
```

Comment fields: `file` (path as it appears in the diff header), `line` (absolute line number from `index.md` — use the **Old** column for `"old"` side, the **New** column for `"new"` side), `side` (`"old"` for removed lines, `"new"` for added/context lines), `body` (1-2 sentences).

**Do not manually count lines from the diff.** The annotated `index.md` already shows the correct absolute line number for every line. Copy the number directly from the Old or New column.

**Writing good comments:**

Focus on *why*, not *what*. The diff already shows what changed — comments explain the reasoning or draw attention to what matters.

Good candidates for comments:
- Non-obvious relationships between files within the section ("This handler now delegates to the middleware added in auth.ts above")
- Breaking or behavioral changes that are not obvious from the code alone
- New code that replaces deleted code elsewhere in the diff
- Subtle logic a reviewer might miss on a first read

Keep to 1-2 sentences per comment. Not every line needs a comment — only annotate where genuine insight helps the reviewer. An empty `comments` array is fine for straightforward sections.

Every block number must appear exactly once across all sections. The assembler will error if any blocks are missing or duplicated.

### 5. Assemble, validate, and generate

```bash
# Build sections JSON from manifest + blocks
node <skill_path>/scripts/assemble_sections.mjs "$REVIEW_DIR/manifest.json" "$REVIEW_DIR/blocks" "$REVIEW_DIR/sections.json"

# Validate all changed lines are covered
node <skill_path>/scripts/validate_coverage.mjs "$REVIEW_DIR/raw.diff" "$REVIEW_DIR/sections.json"

# Generate HTML review page
node <skill_path>/scripts/generate_review.mjs "$REVIEW_DIR/sections.json" "$REVIEW_DIR/review.html"
```

If the assembler errors on missing blocks, fix `$REVIEW_DIR/manifest.json` and re-run. Do not proceed until all blocks are covered.

Open in the user's browser:
```bash
open "$REVIEW_DIR/review.html"        # macOS
xdg-open "$REVIEW_DIR/review.html"    # Linux
```

Tell the user: the review page is open. They can click any line to add comments, then export comments (JSON or text) via the buttons at the top.

### 6. Process review comments

When the user pastes exported comments back, parse them and apply fixes. Comments come in this format:

**JSON format:**
```json
[
  { "file": "src/auth.ts", "line": "15", "type": "add", "comment": "This should validate token expiry" }
]
```

**Text format:**
```
## src/auth.ts
- [line 15] (add): This should validate token expiry
```

For each comment: read the referenced file, understand the context, and apply the requested change. After all fixes, offer to re-run the review on the updated diff (reuse the same `$REVIEW_DIR`).
