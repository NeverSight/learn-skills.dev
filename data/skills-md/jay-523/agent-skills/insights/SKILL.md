---
name: insights
description: Extract coding patterns and preferences from session transcripts for CLAUDE.md
disable-model-invocation: true
context: fork
agent: Explore
allowed-tools: Read, Glob, Bash(ls *)
argument-hint: "[current|latest|all]"
---

# /insights -- Extract Session Insights for CLAUDE.md

Analyze Claude Code session transcripts to extract patterns that should be
codified in CLAUDE.md files. Produces two-level output: Global entries
(apply to all projects) and Project entries (apply to this project only).

## Arguments

- `current` (default): Analyze the most recent session transcript
- `latest`: Analyze the 3 most recent session transcripts
- `all`: Analyze the 10 most recent session transcripts

## Procedure

### Step 1 -- Locate Transcripts

Find session JSONL files for this project:

```bash
ls -lt ~/.claude/projects/*/
```

Identify the encoded project path that matches the current working directory.
Sort by modification time (newest first).

Based on the argument:
- `current` / no argument: read the 1 most recent .jsonl file
- `latest`: read the 3 most recent .jsonl files
- `all`: read the 10 most recent .jsonl files

### Step 2 -- Extract Insights

Scan user messages in each transcript for five categories:

**A. Corrections and Redirections**
Look for signals: "no", "wrong", "actually", "instead", "should be",
"not that", "stop", user restating the same instruction differently,
or messages where the user interrupted and changed direction.

For each correction:
- What was Claude's wrong assumption?
- What is the correct behavior the user wanted?

**B. Coding Style Preferences**
Look for: naming conventions, formatting preferences, comment style,
import ordering, file organization, language/framework choices.

**C. Tool and Workflow Preferences**
Look for: preferred package managers, test runners, build tools, shell
commands, editor workflows, git conventions, CI/CD preferences.

**D. Communication Style**
Look for: preferred response length, level of explanation desired,
when to ask vs. proceed, tone preferences, what annoys the user.

**E. Architecture and Project Patterns**
Look for: module structure, dependency patterns, API design, error handling
conventions, naming patterns specific to this project.

### Step 3 -- Categorize by Scope

Assign each insight to a scope:

| Category | Scope |
|----------|-------|
| Coding style preferences | Global (~/.claude/CLAUDE.md) |
| Tool/workflow preferences | Global (~/.claude/CLAUDE.md) |
| Communication style | Global (~/.claude/CLAUDE.md) |
| Architecture/project patterns | Project (./CLAUDE.md) |
| Corrections -- depends on context | Either (judge by specificity) |

### Step 4 -- Check for Duplicates

Read the existing CLAUDE.md files:
- `~/.claude/CLAUDE.md` (global)
- `./CLAUDE.md` (project, if it exists)

Compare each extracted insight against existing entries. Mark duplicates
so they are not proposed again.

### Step 5 -- Present Findings

Output a findings table:

```
| # | Insight | Category | Scope | Duplicate? |
|---|---------|----------|-------|------------|
| 1 | ... | Correction | Project | No |
| 2 | ... | Coding style | Global | Yes (line 42) |
```

Then output draft CLAUDE.md entries organized by scope:

```
## Global Entries (for ~/.claude/CLAUDE.md)

- Entry 1
- Entry 2

## Project Entries (for ./CLAUDE.md)

- Entry 1
- Entry 2
```

## Important

- Do NOT modify any files. Present findings for the user to review.
- The user decides what to add and where.
- If no meaningful insights are found, say so plainly rather than
  fabricating entries.
- Skip transcripts that are too short to contain useful patterns
  (fewer than 10 user messages).
