---
name: agent-memory
description: Agent-first persistent memory for storing, retrieving, and maintaining human-readable notes across conversations. The agent should proactively capture important decisions and work completed; users can also ask to remember, save, note, recall, remind, or review prior work (e.g., “remember this”, “save this”, “note this”, “remind me about…”, “what did we decide about…”, “check your notes”, “clean up memories”).
license: Proprietary
compatibility: Designed for Agent Skills runtimes that can read/write local files and run basic shell commands (ls, mkdir, cat, rg).
---

# Agent Memory

An **agent-first** persistent memory space for storing knowledge that survives across conversations. Memories are **human-readable** markdown files so that both the agent and humans can inspect and edit them.

## Location

Store memories under:

* `memories/`

(If your runtime expects a specific root, keep `memories/` inside the skill folder and reference it relative to the skill directory.)

## When to Use

### Agent-first usage

Use this skill as a default tool for the agent to record and retrieve knowledge:

* Capture important decisions, rationale, and work completed
* Preserve research findings, tricky fixes, and important commands
* Record in-progress work that should be resumable later
* Check existing memories before starting related work

### Explicit user requests

Use this skill when the user asks to:

* Remember or save information
* Recall prior decisions, context, or investigation results
* Resume a workstream after a break
* Review notes, history, or “what we decided”
* Consolidate / clean up / organize memories

### Proactive usage

Save memories at your own initiative when you discover something worth preserving, such as:

* Research findings that took effort to uncover
* Non-obvious patterns, sharp edges, or gotchas
* Solutions to tricky problems (including commands, files, and the “why”)
* Architectural decisions and rationale
* Important decisions and work completed
* In-progress work that may be resumed later

After completing any task or job, you **must** use this skill to record a brief memory of the work completed (even if no issues were found). Keep it concise and focused on resumption value.

Check memories when starting related work:

* Before investigating a known problem area
* When working on a feature you’ve touched before
* When resuming work after a conversation break

## What to Store

Focus on **resumption value**:

* Decision + rationale
* Current state (done / in-progress / blocked)
* Key artifacts (files, links, commands, configs)
* Next steps and open questions

Avoid storing:

* Secrets (API keys, passwords, tokens)
* Personal data not required for the user’s goals
* Large verbatim logs unless essential (prefer summaries + pointer to where to find the log)

## Folder Structure

Organize memories into category folders. There is **no fixed taxonomy**; create categories that match the content.

Guidelines:

* Use `kebab-case` for folder and file names
* Consolidate or reorganize as the knowledge base evolves

Example:

```
memories/
├── project-context/
│   └── january-2026-focus.md
├── dependencies/
│   └── iconv-esm-problem.md
└── performance/
    └── large-file-worker-leak.md
```

## Memory File Format

Every memory **must** start with YAML frontmatter including a concise `summary` field.

### Required frontmatter

```
---
summary: "1–2 lines describing what this memory contains (decisive + searchable)"
created: 2026-01-22
---
```

### Optional frontmatter

```
---
summary: "Worker thread leak during large file processing — cause and fix"
created: 2026-01-15
updated: 2026-01-20
status: in-progress   # in-progress | resolved | blocked | abandoned
tags: [performance, worker, memory-leak]
related: [src/core/file/fileProcessor.ts]
---
```

### Body guidelines

Use markdown headings when helpful. Keep content self-contained.

Recommended sections (use what’s relevant):

* Context
* Decision / Findings
* Evidence (commands, snippets, links)
* Impact
* Next steps

## Search Workflow (Summary-first)

Use a summary-first approach to find relevant memories efficiently.

1. List categories

```sh
ls memories/
```

2. View all summaries

```sh
rg "^summary:" memories/ --no-ignore --hidden
```

3. Search summaries for a keyword

```sh
rg "^summary:.*KEYWORD" memories/ --no-ignore --hidden -i
```

4. Search by tag

```sh
rg "^tags:.*KEYWORD" memories/ --no-ignore --hidden -i
```

5. Full-text search (when summary search isn’t enough)

```sh
rg "KEYWORD" memories/ --no-ignore --hidden -i
```

6. Read the specific memory file(s) that appear relevant.

> Note: if `memories/` is gitignored, use `--no-ignore` and `--hidden`.

## Operations

### Save a memory

1. Determine an appropriate category folder
2. Check if an existing category fits; otherwise create a new one
3. Create a new file (avoid overwriting existing files)
4. Write required frontmatter + a clear title and content

Example:

```sh
mkdir -p memories/category-name/

# Ensure the target file does not already exist
test -e memories/category-name/filename.md && echo "File exists" && exit 1

cat > memories/category-name/filename.md << 'EOF'
---
summary: "Brief description of this memory"
created: 2026-01-22
status: in-progress
tags: [tag1, tag2]
---

# Title

## Context

## Findings / Decision

## Next steps
EOF
```

### Recall / remind

1. Search summaries for relevant terms
2. Read only the most promising files
3. Summarize back to the user (include the decision + the actionable next step)

### Maintain

* Update: when information changes, update the content and add `updated:`
* Consolidate: merge related memories as they grow
* Delete: remove memories that are no longer relevant
* Reorganize: move memories into better categories over time

Example delete:

```sh
rm -f memories/category-name/filename.md
rmdir memories/category-name/ 2>/dev/null || true
```

## Quality Rules

1. Write for resumption: a future reader should be able to continue without prior context
2. Keep summaries decisive: reading the summary should indicate whether the full file is worth opening
3. Prefer clarity over completeness: store what is useful, not everything
4. Keep the memory base current: update or delete stale content

## Examples (User Prompts That Should Trigger This Skill)

* “Remember this: we decided to migrate to X because …”
* “Save these investigation notes for later.”
* “Remind me what we concluded about the caching bug.”
* “What did we decide about the API pagination approach?”
* “Check your notes about the deployment process.”
* “Clean up our notes and consolidate duplicates.”
