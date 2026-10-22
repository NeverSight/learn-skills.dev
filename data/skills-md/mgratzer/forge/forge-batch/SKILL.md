---
name: forge-batch
description: Group a scope of Issues into Waves that can be implemented concurrently without stepping on each other — estimate what each Issue touches, exclude the ones that need a human, and print launch lines. Use when the user has several prepared Issues and wants to know which can run in parallel unattended.
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Glob, AskUserQuestion
---

# Batch Issues into Waves

Decide which Issues can ship side by side, and in what order.

## Input

A scope (`$ARGUMENTS`): `milestone:<name>`, `label:<name>`, `epic:<number>`, or Issue numbers. Optional: `-- <additional context>` such as a wave size cap or Issues to pin together. `--unattended` skips the approval step.

## Process

### Step 1: Collect Candidates

List the scope's Issues with *List Issues by Scope* in [issue-operations](_shared/issue-operations.md), keeping only number, title, labels, execution mode, and dependency references — bodies are read later, per Issue. Then fetch open PRs once and match `#<number>` or `<type>/<number>-` locally:

```bash
gh pr list --state open --limit 100 --json number,title,headRefName,body
```

Exclude, with a stated reason each: HITL Issues, Issues labeled `blocked`, Issues with an open PR, and Issues that depend on an open Issue outside the scope. Everything left is AFK and free to start.

### Step 2: Estimate Touch Sets (delegate)

For each candidate, produce its **touch set** — the files and directories the implementation will most likely change. When the scope has more than five Issues, delegate to [forge-scout](_shared/roles/forge-scout.md) sub-agents in parallel on a cheap fast model, about five Issues per scout so shared greps run once; otherwise estimate inline. Unlike implement's blind research, the scout receives the Issues here — the touch set is about them.

> For each Issue: list every path it names explicitly, then grep for the concepts it names (routes, tables, components, message keys) and add the files that define them. Return paths only.

**Inputs provided to sub-agent:** Role: forge-scout, the Issue bodies, codebase access.
**Expected output:** `#<number>: <paths...>` per Issue.

### Step 3: Build Waves

Two Issues **conflict** when their touch sets share a file or both match the same serialized-resource glob from [unattended-config](_shared/unattended-config.md). Issue A **depends on** B when A's body says so (`depends on #B`, `blocked by #B`, `after #B`).

Place Issues greedily: order by priority label, then by number; put each into the earliest Wave where it conflicts with nothing already there and every dependency sits in an earlier Wave. Cap a Wave at 10 Issues unless the trailing context says otherwise. Issues sharing a directory but no file are allowed together and marked *adjacent* so the human can veto.

### Step 4: Confirm

Present the batch via AskUserQuestion: approve, move an Issue, or exclude one. **In unattended mode:** skip and print.

### Step 5: Print the Batch

Use the output format below. The launch line names `$FORGE_LAUNCHER` when that variable is set, otherwise just the numbers for whatever the user starts by hand.

## Output Format

```text
## Batch: <scope>

### Wave 1 (<n> Issues)
| # | Title | Touch set | Notes |
|---|-------|-----------|-------|
| 123 | feat(api): ... | src/api/x.ts, src/api/x.test.ts | |
| 124 | fix(ui): ... | src/ui/y.tsx | adjacent to #125 |

launch: <launcher> 123 124 ...

### Wave 2 (<n> Issues, after Wave 1 merges)
...

### Excluded
- #130: HITL
- #131: open PR #400 already
```

## Guidelines

- **Touch sets are estimates** — say so; a Wave is a bet the human approves, not a proof
- **Serialized resources trump everything** — two migrations in one Wave is a merge conflict by construction
- **Later Waves are provisional** — re-run after a Wave merges; touch sets shift as code lands

## Related Skills

**Before:** `forge-create-issue` classifies Issues as AFK or HITL — only AFK Issues enter a Wave.
**After:** start each Issue in a Wave with `forge-ship --guard`, through `$FORGE_LAUNCHER` or by hand.

## Example Usage

```
/forge-batch milestone:v1.1.0
/forge-batch label:ready
/forge-batch epic:601
/forge-batch 610 611 612 613 -- cap waves at 4
/forge-batch --unattended label:ready
```
