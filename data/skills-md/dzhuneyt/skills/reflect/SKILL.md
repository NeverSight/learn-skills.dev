---
name: reflect
description: Use when the user invokes /reflect or asks to reflect on, wrap up, or take stock of the current session. Re-reads the in-context conversation for anything that would die when the session closes — dropped action items, durable lessons with no home, stale docs, skillify opportunities, global/project CLAUDE.md and AGENTS.md and README gaps, and follow-ups worth an issue or a PR — surfaces them as one ranked shortlist, then acts on the ones the user selects. Not a git-history retro and not a full doc audit.
---

# Reflect

End-of-session reflection. Re-read the current conversation, surface what slipped through and what would be lost, and act on what the user chooses — all before the session wraps.

## Scope and stance

- **Conversation-scoped.** Reflect over the conversation that is in context. Do NOT parse transcript files or git history. This is not `gstack-retro` (commit-history retro) and not `gstack-learn` (learnings store) — stay in the forward-action lane.
- **Assume the session dies after this.** Every fact established here that isn't written to a file, an issue, or a PR is gone. That makes *homeless knowledge* the headline job of this skill, not a footnote: a hard-won gotcha that never reaches `CLAUDE.md` costs the next session the same debug loop.
- **Compaction honesty.** If the session was compacted, reflect on what survived and say so plainly. Do not fabricate recall of summarized turns.
- **No artifact by default.** Findings live in the conversation. The surfaced list is throwaway — the user reacts or ignores it. Write a file ONLY if the user picks an action that writes one, or explicitly asks.
- **Under-report, never spam.** A wrong "loose end" or a skill suggestion for one-off work is worse than silence. Apply the confidence bars below. When in doubt, drop it.
- **Verify before you propose.** Never claim something is undocumented or untracked without checking. Read the destination file (`CLAUDE.md`, `AGENTS.md`, `README.md`) and search open issues first, so what you surface is a real edit against real current content — not a duplicate of a line that's already there.

## Step 1 — Reflect

Re-read the conversation end to end. Hold the whole arc in mind before flagging anything.

## Step 2 — Run the detectors

Each detector has a hard confidence bar. An item that does not clear its bar is silently dropped.

**A. Loose ends** — action items or decisions the user skipped.
- Primary heuristic: find assistant messages that bundled **two or more** decisions/questions into one block, then check whether the user's next reply addressed *all* of them. Example: you asked three things, the user answered one. The unaddressed ones are the highest-value finds — the user reacted to the top of a wall of text and the rest fell through unread.
- Also catch: explicit "let's do X later", TODOs raised but never returned to, errors acknowledged but not fixed.
- Bar: concrete evidence in the conversation that the item was raised and never closed.

**B. Doc gaps** — docs made stale by *this session's* changes.
- Targeted only: "README section X is now wrong because we changed Y." Name the file and the specific staleness.
- Bar: a change made this session directly contradicts existing documented behavior. Never propose a from-scratch documentation audit.

**C. Skillify / harness gaps** — repetitive work a new Skill or Agent could absorb, or a multi-step recipe worth capturing as a reusable skill.
- Bar: the pattern recurred **at least twice** this session, or is obviously recurring work. A single occurrence does not qualify.

**D. CLAUDE.md / AGENTS.md gaps** — memory-file improvements. Tag each finding on two axes:
- **Scope:** `project` (repo-local `CLAUDE.md`/`AGENTS.md`) vs `global` (user's `~/.claude/CLAUDE.md`). Pick by whether the preference is repo-specific or holds everywhere.
- **Kind:**
  - **append** → a new principle, preference, or convention the user clearly holds but hasn't written down.
  - **rewrite** → an *existing* sentence this session proved wrong, stale, or misleading. Quote the current line and propose the replacement wording — don't just add on top of it.
  - **hook** → a `settings.json` hook, NOT prose. Anything of the form "from now on, whenever X, do Y" is an automated behavior the harness must execute — it cannot live as memory-file text. Route these through the `update-config` skill when acting.
- Bar: clear evidence the user holds the preference — they stated it, corrected you on it, or it recurred. A one-off stylistic choice does not qualify.

**E. Homeless knowledge** — a durable fact this session established that currently lives *only* in this conversation.
- What counts: a gotcha found the hard way (the build breaks unless X runs first), an environment or tooling constraint, the real shape of an external API that the docs got wrong, an approach tried and rejected **plus why**, a decision and its rationale, a non-obvious reason a piece of code is the way it is.
- Rejected approaches are worth as much as chosen ones. "We tried X, it fails because Y" is exactly what the next session repeats if nobody writes it down.
- Bar, all three: **(1)** it cost real effort to learn — a failed attempt, a debug loop, a doc dig — or the user asserted it as fact; **(2)** someone would plausibly hit it again; **(3)** you checked, and it isn't already written down. Anything recoverable in thirty seconds fails the bar.
- Then route it to a destination using the table below. A finding with no plausible destination is not a finding.

**F. Unshipped work** — work that exists only in this session and needs somewhere durable to land.
- **Needs a PR:** real code changes sitting in the working tree or on an unpushed branch, complete enough to review. Bar: the change exists and is coherent — not a half-edit you'd be embarrassed to open.
- **Needs an issue:** a concrete follow-up the session identified and won't do. Bar: specific enough that someone else could pick it up cold (what, why, and roughly where), and not already tracked — search open issues before proposing one. "We should improve error handling sometime" fails; "`parseConfig` swallows the YAML error and returns `{}` — should surface it, see `config.ts:41`" passes.
- Never open an issue or PR on your own. It goes through Step 4 like everything else.

### Where knowledge goes

Route every D/E finding to exactly one destination. Getting this wrong is the common failure — a repo-specific build quirk in the global memory file pollutes every other project.

| The knowledge is… | Destination |
| --- | --- |
| A preference or habit that holds in **every** repo (tone, tooling, workflow) | global `~/.claude/CLAUDE.md` |
| A convention or constraint **an agent** needs in this repo | project `CLAUDE.md` / `AGENTS.md` |
| Something **a human** contributor or user needs — install steps, what a thing is, a contributor gotcha | `README.md` or the relevant doc |
| Why the code is shaped this way, tied to one specific place | a code comment where it applies |
| Work worth doing that isn't happening now | a GitHub issue |
| Changes that exist but nobody else can see | a commit + PR |
| A recurring multi-step procedure | a new skill (detector C) |
| "From now on, whenever X, do Y" | a `settings.json` hook, via `update-config` |

If a fact seems to want two destinations, pick the one whose *audience* actually needs it and move on. Don't duplicate the same sentence into three files.

## Step 3 — Collect into one flat, ranked list

Gather every finding that cleared its bar — across **all** detectors — into a single flat list held in memory. Keep each finding's category tag (A–F), but do NOT group the list by category.

- **Rank** by value = confidence × impact × **durability loss**. That third factor is the tiebreaker: between two equally good findings, the one that is *irrecoverable once this session closes* wins. A gotcha that exists nowhere but this transcript outranks a doc tweak anyone can spot later from the code.
- **Merge before ranking.** Two findings headed for the same destination file become one finding, one question, one edit.
- **Take the top 5.** Discard the rest. If more than 5 cleared their bars, say so in one line (e.g. "3 lower-confidence items dropped") so the user knows there's a tail, but do not surface them.
- If nothing cleared any bar, say "Nothing worth flagging" and stop.

## Step 4 — Ask one finding at a time

Surface the shortlist as **separate, single-select `AskUserQuestion` questions — one question per finding**, in ranked order so your strongest recommendation comes first. Do NOT bundle findings into a single `multiSelect` question; that grouping gets in the way. Each finding is its own decision.

For each finding's question:
- `header`: the category label — "Loose end", "Doc gap", "Skillify", "CLAUDE.md", "Knowledge", or "Ship it".
- `question`: state the finding concretely (what was dropped / what's stale / what would be lost / what to open), name the destination, then ask what to do.
- `options` (single-select, `multiSelect: false`): put **your recommended action first**, labeled `(Recommended)`. Follow with the realistic alternatives, ending with a clean decline. Typical recommended actions by category:
  - **A (loose end):** "Finish it now" — or, if large, "Do the smallest next step".
  - **B (doc gap):** "Show the diff and apply".
  - **C (skillify):** "Draft the SKILL.md skeleton".
  - **D (CLAUDE.md/AGENTS.md):** append/rewrite → "Show the edit and apply"; hook → "Wire the hook via update-config".
  - **E (knowledge):** "Write it to <destination> now". Where the destination is genuinely arguable, make the alternatives the *other destinations* rather than a vaguer version of the same action.
  - **F (ship it):** "Open the PR" / "File the issue" — and show the draft title and body before creating anything.
  - Always include a "Skip" / "Leave it" option last.

Ask them one at a time (or a few per call, but never more than one **finding** per question). This lets you act on each answer before moving on.

## Step 5 — Act on each selection

For each finding the user chose to act on, do it in this session immediately:

- **A (loose ends):** complete the dropped item, or confirm the smallest next step if it's large.
- **B (doc gaps):** produce the exact diff and apply on approval.
- **C (skillify):** draft a `SKILL.md` skeleton or propose `/gstack-skillify`. Don't force a full skill build inside `/reflect` — the stub or a deferral is fine.
- **D (CLAUDE.md/AGENTS.md):** append/rewrite → show the exact memory-file diff (quoting the old line for a rewrite) and apply on approval; hook → invoke `update-config` to wire it.
- **E (knowledge):** write it into the routed destination as a real diff against the current file — matching that file's existing voice, section structure, and level of detail. Keep it to the fact and its consequence; a durable line beats a paragraph of session narrative. Never paste conversation transcript into a memory file.
- **F (ship it):** PR → hand off to `/gh-pr` if available, otherwise commit, push, and open it with the drafted title and body. Issue → create it with the drafted title and body, and link it from anywhere in the repo that a reader would look for it. Show the draft first; create only after the user approves.

Persist nothing to disk unless the user picked an action that writes, or explicitly asks for a written record.
