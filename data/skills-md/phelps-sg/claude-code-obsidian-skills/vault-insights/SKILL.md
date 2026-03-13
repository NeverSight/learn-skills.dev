---
name: vault-insights
model-invocable: true
description: Audit the Obsidian vault for inconsistencies and latent insights
allowed-tools: Read, Glob, Grep, Edit, Task, Bash
---

# Vault Insights

Audit the shared Obsidian vault at `~/Documents/obsidian-vault/` for internal consistency and latent cross-cutting insights.

## What This Skill Does

Reads all notes in the vault and produces two analyses:

1. **Inconsistency scan** — finds contradictions, broken links, stale sections, and notes that have drifted out of sync
2. **Latent insight scan** — traverses the wiki-link graph and tag dimensions to surface knowledge that is implicit in the connections between notes but not stated in any individual note

All output is written to the **daily note only** (`YYYY-MM-DD.md`), clearly tagged so findings are traceable. The skill **must not edit any other note** unless the user explicitly instructs it to.

## Procedure

### Step 1: Read the vault

1. Glob `*.md` in the vault root to list all notes
2. Read every note (use parallel reads for efficiency)
3. Build a mental model of: tags, wiki-links between notes, key claims/facts, status markers (resolved, superseded, complete, etc.), open questions

### Step 2: Inconsistency scan

Check for:

- **Contradictions**: Note A says X, Note B says Y, where X and Y conflict
- **Stale sections**: A note's later section resolves/supersedes an earlier section in the same note, but the earlier section wasn't updated
- **Broken link targets**: A `[[wiki-link]]` points to a note that is empty or doesn't exist
- **Stale PR notes**: For any note with the `#pr` tag or `pr-` filename prefix, check the PR's current status using `gh pr view <number> --json state,mergedAt,closedAt`. Flag if the note says "in progress" but the PR is already merged/closed.
- **Unresolved propagation**: A finding in one note invalidates or changes claims cited in other notes, but those other notes haven't been updated
- **Duplicate/overlapping notes**: Two notes cover substantially the same content with risk of drift

For each inconsistency found, classify its severity:

| Severity | Meaning |
|----------|---------|
| **error** | Directly contradictory information across notes — reader would be misled |
| **warning** | Stale or unpropagated information — reader might be confused |
| **info** | Minor issues (empty link targets, cosmetic) |

### Step 3: Latent insight scan

This is where the graph structure earns its keep. Because notes are explicitly linked by wiki-links and tagged along multiple dimensions, you can traverse the graph to surface knowledge that is implicit in the connections but not stated anywhere.

Look for:

- **Cross-note implications**: Does a finding in note A have consequences for the design/approach described in note B that aren't mentioned in either? Follow the wiki-link chains — a domain note linked to an architecture note linked to a service note may reveal implications that no single note articulates.
- **Unconnected solutions**: Does a problem described in one note have a solution (or partial solution) already described in another note, without either linking to the other?
- **Pattern repetition**: Is the same pattern/problem appearing across multiple notes without being recognised as a general principle?
- **Gaps**: Is there something that logically should exist given the surrounding notes, but doesn't?

For each insight, assign a confidence and immediacy rating:

| Rating | Confidence | Meaning |
|--------|-----------|---------|
| **high** | Strong evidence from multiple notes; concrete and specific | |
| **medium** | Reasonable inference; depends on one or two assumptions | |
| **low** | Speculative; interesting but unverified | |

| Rating | Immediacy | Meaning |
|--------|----------|---------|
| **now** | Actionable against current codebase/branch without dependency on future work |
| **soon** | Relevant when planned work (next phase/PR) begins |
| **future** | Relevant only if/when speculative future work materialises |

### Step 4: Review recent vault insights for dedup

Before writing, search for recent `#vault-insights` sections:

```
Grep: pattern="#vault-insights" path="~/Documents/obsidian-vault" output_mode="files_with_matches"
```

Read the `## Vault Insights` section from the **3 most recent** daily notes that contain one. Compare your current findings against previously reported items:

- **Resolved**: If a previously reported inconsistency has been fixed, note its resolution briefly.
- **Unchanged**: If previously reported items have not changed, **do not repeat them individually**. Add a single-line "Unchanged" section with a count and a link to the most recent daily note where they were reported.
- **Updated**: If a previously reported item has new information, report it in full with a note describing what changed.
- **New**: Report in full as normal.

### Step 5: Write findings to daily note

Append a `## Vault Insights` section to today's daily note (`YYYY-MM-DD.md`). Create the daily note if it doesn't exist (with H1 title and no tags — daily notes are journals, not tagged knowledge).

Use this exact format:

```markdown
## Vault Insights

#vault-insights

### Inconsistencies

#### [severity: error] Short title
**Notes**: [[note-a]], [[note-b]]
Description of the contradiction and what needs reconciling.

#### [severity: warning] Short title
**Notes**: [[note-a]]
Description of the staleness or drift.

### Latent Insights

#### [confidence: high | immediacy: now] Short title
**Notes**: [[note-a]], [[note-b]]
Description of the insight. Why it matters. What could be done.

### Summary
- X inconsistencies found (N error, N warning, N info)
- Y latent insights found (N high/now, N medium/soon, N low/future)
```

## Constraints

- **Read-only except for the daily note.** Do not edit, create, or delete any other note in the vault. Report what needs fixing; let the user decide what to act on.
- **No codebase reads.** This skill audits the vault's internal consistency, not whether notes match the code. (The user can verify against code separately.)
- **No hallucinated links.** Only reference notes that actually exist in the vault. If a note should exist but doesn't, flag that as a gap, don't create it.
- **Be calibrated.** Don't inflate severity or confidence. An insight that depends on future work that may never happen is `low/future`, not `high/now`.
- **Deprioritize sketches.** Notes tagged `#sketch` are speculative designs — they may never be built. Give low priority to findings that only involve sketch notes.
- **Use the Explore agent** (via Task tool with subagent_type=Explore) to parallelise reading large numbers of notes if the vault has grown significantly.

## Usage

```
/vault-insights        # Run full audit (inconsistencies + insights)
```

The skill always runs both scans. There is no partial mode — the vault is small enough that a full read is fast, and inconsistencies often inform insights.
