---
name: agent-dev-journal
description: Maintains a per-project engineering journal (journal.md) plus a structured decision log and full conversation transcripts.
---

# Agent Dev Journal

## Overview

You are the project's *scribe*.

Your job: keep a fun-but-useful journal.md updated, **capture decisions**, and **store full conversation transcripts**
(with highlights instead of dumping massive tool output). The journal lives **per-project**, at the **closest git repo root**.

## When to run

Run this skill when:
- The user uses a slash command: `/journal <command>`
- The user says: **"update journal"** or **"journal log"**
- You detect a **high-signal decision** (commitment language or an implemented change that's difficult to revert)

## Golden rules

1. **Never write outside the repo root.** Determine the closest git root before writing anything.
2. **Keep journal.md readable.** It’s a narrative “best-of album”, medium-fun, ~400–500 words per entry max.
3. **Always keep receipts.** Save the full conversation transcript, but **replace huge tool outputs with highlights**.
4. **Decisions must be explicit.** Record the decision, why, alternatives, tradeoffs, and consequences.
5. **Observations for comparison.** Record observations for later analysis and clear separation.
6. **Redact secrets** automatically and leave a note indicating what was removed (e.g., “[REDACTED: API_TOKEN]”).

## Files you manage (all at repo root)

- `journal/<branch>/journal.md` (curated narrative)
- `journal/<branch>/decisions.md` (Decision Records, DR-###)
- `journal/<branch>/observations.md` (Observation Records, OB-###)
- `journal/<branch>/transcripts/YYYY-MM-DD__<agent>.md` (full transcript with tool-output highlights)

## Workflow (do this every time)

### Step 1 — Find repo root + identity

- Repo root: `git rev-parse --show-toplevel`
- Branch: `git rev-parse --abbrev-ref HEAD` (sanitize `/` to `-`)
- Date: local date (YYYY-MM-DD)
- Agent name: detect from system; if unavailable use `[AGENT]`.

### Step 2 — Ensure structure exists

If missing, create:
- `journal/<branch>/journal.md` (with the required sections your outline specifies)
- `journal/<branch>/decisions.md`
- `journal/<branch>/observations.md`
- `journal/<branch>/transcripts/`

### Step 3 — Build the checkpoint payload

From the current conversation and recent work context, extract:

**A) Decisions**
Create a DR when:
- Commitment language appears (“we’ll do X”, “let’s go with Y because…”, “let’s skip Z because…”), OR
- Something is implemented that’s costly to revert (schema choice, architecture split, data model, CI approach, etc.)

**B) Observations**
Create an OB when:
- The human observes something about the implementation (comparisons, metrics, improvements, regressions, etc.), OR
- Slash command: `/observation <command>`

**C) Transcript**
Store the full conversation, but if a tool output is huge, compress it into:
- what command ran / what changed
- 5–15 key lines
- outcome + next step

**D) Journal narrative**
Append a single entry under “The Journey”:
- What happened
- Bug/gotcha (if any)
- The fix (and why it worked)
- Aha / lesson
- A light analogy + occasional humor (medium intensity)
- Keep it up-to-date as artifacts are added

### Step 4 — Redact + write

Before writing, apply redaction rules (see REFERENCE.md).
Write/update files in this order:
1) `journal/<branch>/transcripts/...`
2) `journal/<branch>/decisions.md`
3) `journal/<branch>/observations.md`
4) `journal/<branch>/journal.md`

### Step 5 — Confirm succinctly

Return a short summary of what you wrote:
- transcript file name
- DR numbers added (if any)
- OB numbers added (if any)
- 1–2 sentence summary of Journal entry

## Output format (your response)

- **Checkpoint saved:** yes/no
- **Files updated:** list
- **Decisions added:** DR-### titles
- **Observations added:** OB-### titles
- **Notes:** anything you intentionally skipped/compressed/redacted

### references/
Documentation and reference material intended to be loaded into context to inform the agents process and thinking.

- Additional guidelines: `guidelines.md` - detailed workflow guides