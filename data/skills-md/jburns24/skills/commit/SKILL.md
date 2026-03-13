---
name: commit
description: Creates a conventional-commit message with embedded generation metadata (model, plan file, unplanned changes) in an HTML comment after implementing a plan. Use this skill whenever the user says "commit this", "git commit", "make a commit", or asks to commit changes after working through a plan in plan mode.
---

# Commit

Creates a structured git commit message that includes embedded generation metadata — the model used, the full contents of the driving plan file, and any changes that deviated from the plan. This provides traceability between what was planned and what was actually shipped.

## When to Use

Trigger this skill when the user asks to commit staged or unstaged changes, especially after plan-mode implementation. Key phrases: "commit this", "git commit", "make a commit", "commit the changes".

## Instructions

### Step 1 — Inspect staged changes

Run `git diff --cached --stat` and `git diff --cached`. If nothing is staged, stop and tell the user — do not proceed with an empty commit.

### Step 2 — Locate the plan file

Check in priority order:

1. Any plan file path mentioned in the current conversation context (pattern `~/.claude/plans/<name>.md`)
2. Most recently modified `.md` in `~/.claude/plans/` via:
   ```
   ls -lt ~/.claude/plans/ | grep '\.md$' | head -1 | awk '{print $NF}'
   ```
3. If not found, set `plan_file = null`

### Step 3 — Read the plan file

Read the full file contents as `plan_contents`. On any read failure, set `plan_file = null` and `plan_contents = null`.

### Step 4 — Determine model name

Read from the system context in the current conversation:

- Sonnet 4.x → `"claude-sonnet-4-6"`
- Opus 4.x → `"claude-opus-4-6"`
- Haiku 4.x → `"claude-haiku-4-5-20251001"`

Default to `"claude-sonnet-4-6"` if uncertain.

### Step 5 — Draft the commit message

Use conventional commit format: `<type>: <short description under 72 chars>` followed by 2–6 bullet points describing logical changes.

Valid types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `style`, `perf`

### Step 6 — Identify unplanned changes

Compare staged files against files named in the plan. An unplanned change is any staged file not described in the plan, or any change that goes beyond what the plan described.

Format each as: `"<filepath>: <brief description>"`

Use an empty array if all changes match the plan or if the plan is unavailable.

### Step 7 — Build the HTML comment block

Construct the metadata block only if `plan_file` is not null. The block consists of two parts placed together with no blank line between them:

1. A human-readable notice line so readers see that metadata is present even in UIs that hide HTML comments:
   ```
   Generated with Claude Code. This commit contains embedded generation metadata (model, plan, unplanned changes). To read it: git log --format="%B" <hash> | less  or use the find-commit skill: https://github.com/jburns24/skills/find-commit
   ```

2. Immediately followed (no blank line) by the HTML comment:
   ```
   <!-- generation-metadata
   {
     "model": "<model>",
     "plan_file": "<absolute tilde-expanded path>",
     "plan_contents": "<full plan text escaped as JSON string>",
     "unplanned_changes": ["<desc>", ...]
   }
   -->
   ```

JSON-escape `plan_contents`: replace `"` → `\"`, newlines → `\n`. Use the full absolute path (no `~` shorthand) for `plan_file`.

### Step 8 — Confirm if ambiguous

Show the drafted message and ask the user for confirmation before committing if any of these are true:

- Unplanned changes exist
- No plan file was found
- More than 20 files are staged

### Step 9 — Execute the commit via heredoc

The full commit message structure is:

```
<type>: <description>

- <bullet 1>
- <bullet 2>

Generated with Claude Code. This commit contains embedded generation metadata (model, plan, unplanned changes). To read it: git log --format="%B" <hash> | less  or use the find-commit skill: https://github.com/jburns24/skills/find-commit
<!-- generation-metadata
{ ... }
-->

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Use the `'EOF'` (quoted) heredoc delimiter to prevent shell interpolation of special characters inside the message body:

```bash
git commit -m "$(cat <<'EOF'
feat: your message here

- bullet one
- bullet two

Generated with Claude Code. This commit contains embedded generation metadata (model, plan, unplanned changes). To read it: git log --format="%B" <hash> | less  or use the find-commit skill: https://github.com/jburns24/skills/find-commit
<!-- generation-metadata
{
  "model": "claude-sonnet-4-6",
  "plan_file": "/Users/jburns/.claude/plans/example.md",
  "plan_contents": "...",
  "unplanned_changes": []
}
-->

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

Omit both the notice line and the HTML comment block entirely when `plan_file` is `null`.

### Step 10 — Verify and report

Run `git log --oneline -1` and `git status`. Report the commit hash to the user. On failure, report the error clearly — do not retry automatically.

## Examples

**Example 1 — Plan-driven commit with no unplanned changes:**

```
feat: migrate to custom domain temporal-bootcamp.liatr.io

- Update docusaurus.config.ts url/baseUrl for custom domain
- Add static/CNAME for GitHub Pages custom domain routing
- Update CLAUDE.md architecture section with new domain

Generated with Claude Code. This commit contains embedded generation metadata (model, plan, unplanned changes). To read it: git log --format="%B" <hash> | less  or use the find-commit skill: https://github.com/jburns24/skills/find-commit
<!-- generation-metadata
{
  "model": "claude-sonnet-4-6",
  "plan_file": "/Users/jburns/.claude/plans/mighty-coalescing-island.md",
  "plan_contents": "# Plan: Custom Domain...\n\n...",
  "unplanned_changes": []
}
-->

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Example 2 — Unplanned change detected (agent confirms with user first):**

```json
"unplanned_changes": [
  "src/pages/404.tsx: fixed hardcoded /liatrio-temporal-bootcamp/ paths to / (build failure discovered during verification)"
]
```

**Example 3 — No plan file found (omit HTML comment block entirely):**

```
chore: update dependency versions

- Bump lodash from 4.17.19 to 4.17.21

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```
