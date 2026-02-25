---
name: researching-codebases
description: Use when answering complex questions about a codebase that require exploring multiple areas or understanding how components connect - coordinates parallel sub-agents to locate, analyze, and synthesize findings
---

# Researching Codebases

Coordinate parallel sub-agents to answer complex codebase questions.

## When to Use

- Questions spanning multiple files or components
- "How does X work?" requiring tracing through code
- Finding patterns or examples across the codebase
- Understanding architectural decisions or data flow

## When NOT to Use

- Simple "where is X?" - use `code-locator` directly
- Single file questions - just read the file
- External/web research only - use `web-searcher` directly

## Workflow

### 0. Check past research (optional)

Before decomposing a new research question, consider checking for related past research:

1. Run `list-research.py` script to see recent research docs
2. Run `search-research.py` script with relevant keywords
3. If related research exists, run `read-research.py` script to load it
4. Build on previous findings instead of starting fresh

See `research-tools.md` for script usage.

### 1. Read mentioned files first

If the user references specific files, read them FULLY before spawning agents. This gives you context for decomposition.

### 2. Decompose the question

Break the query into parallel research tasks. Consider:

- Which areas of the codebase are relevant?
- Do I need locations, analysis, or examples?
- See `agent-selection.md` for agent capabilities

### 3. Spawn parallel agents

Launch multiple agents concurrently for independent tasks. Use the `task` tool with appropriate `subagent_type`.

**Wait for ALL agents to complete before synthesizing.**

### 4. Synthesize and respond

Combine findings into a coherent answer:

- Direct answer to the question
- Key `file:line` references
- Connections between components
- Open questions if any areas need more investigation

### 5. Offer to save (optional)

For substantial research, ask:

> Want me to save this to a research doc? (project: `.research/` or global: `~/.research/`)

Skip this for quick answers.

When saving:

1. Run `gather-metadata.py` script to get date, repo, branch, commit, cwd.
2. Add query (from user's question) and tags (from content)
3. Format YAML frontmatter per `output-format.md`
4. Create directory if it doesn't exist
5. Use filename: `{filename_date}_topic-slug.md`

## Agent Reference

See `agent-selection.md` for when to use each agent.

## Common Mistakes

**Spawning agents before reading context:** Read any files the user mentions first.

**Not waiting for all agents:** Synthesize only after ALL agents complete.

**Over-documenting simple answers:** Not every question needs a saved research doc.

**Sequential when parallel works:** If tasks are independent, spawn them together.
