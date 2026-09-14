---
name: know-my-repo
description: >-
  Onboards an agent onto an unfamiliar repository from zero knowledge: deep
  parallel read of the codebase, extraction of the repo's actual conventions
  (each proven by at least two examples), verified build/test/run commands,
  an end-to-end exemplar trace of how a feature is really added, then
  generates the initial knowledge set — AGENTS.md and docs/ARCHITECTURE.md —
  with every fact cited. Nothing is deleted. Use on repositories with no (or
  trivial) agent knowledge files, when the user asks to onboard, initialize,
  understand, or learn a repo, generate a CLAUDE.md/AGENTS.md from scratch,
  or mentions know-my-repo or /know-my-repo.
license: MIT
argument-hint: "[project-root]"
---

# Know My Repo

Day one on a codebase you have never seen. No docs, no notes, no memory —
just code. This skill turns that into a knowledge set a future agent can
load and be productive immediately, built the only honest way: **by reading
the code, running the commands, and citing everything.**

Sibling skills: this one creates knowledge where there is none. If rotten
knowledge files already exist, recommend **clean-slate** (reset with backup
gate) instead of writing competing docs next to them.

## The Prime Directive (family rule)

> **No claim without evidence.** Every statement in the generated docs
> carries a `file:line` citation, a command you actually ran, or an explicit
> `UNVERIFIED` tag. A convention is only a convention with **two or more
> examples and no counterexample** — otherwise report it as an inconsistency.

## Progress checklist

Copy this into your response and check items off:

```
Know My Repo Progress:
- [ ] Step 1: Recon — stack, size, knowledge files checked, Newcomer Questions written
- [ ] Step 2: Deep read — structure, data flow, wiring, git trajectory, ops (parallel)
- [ ] Step 3: Conventions — extracted with 2+ examples each; inconsistencies listed
- [ ] Step 4: Commands — build/test/lint verified by running them
- [ ] Step 5: Exemplar trace — one real feature followed end to end
- [ ] Step 6: Write — Findings Brief confirmed, then AGENTS.md + docs/ARCHITECTURE.md, fully cited
- [ ] Step 7: Cold-start test — docs answer the Newcomer Questions; mechanical checks pass
- [ ] Step 8: Report
```

## Step 1 — Recon

- Resolve the target: if a `[project-root]` argument was given, treat that
  path as the repo root for every step below; otherwise use the current
  working directory. State which one you used in the final report.
- Detect stack and size: manifests (`package.json`, `composer.json`,
  `go.mod`, …), lockfiles, top-level layout, file count.
- Check for existing knowledge files (`CLAUDE.md`, `AGENTS.md`,
  `.cursorrules`, `docs/ARCHITECTURE.md`, …):
  - **None or trivial** (< ~20 meaningful lines): proceed; merge the trivial
    content in later.
  - **Substantial:** stop and ask ONE question — update what exists, or
    reset via clean-slate? Recommended answer included. Never write
    competing docs beside living ones.
- Write the **Newcomer Questions** — a numbered list (typically 8–15) of
  what a productive newcomer must be able to answer. Always include: where
  does feature work happen, how do I run the tests, how is a feature added
  end to end, how does this deploy and run in production, and what will
  bite me first. Add repo-specific questions as recon reveals them. Steps
  2–5 exist to answer this list: findings cite the question number they
  answer, questions discovered mid-read are appended, and the deep read is
  complete when every question is answered with evidence or tagged
  `UNVERIFIED` — **not** when every file has been read.

**Preflight:** if the repo is empty or contains only scaffolding (no
meaningful code), note it and proceed with minimal docs reflecting that state.

## Step 2 — Deep read

Read the repo like deep-plan Phase 1. If exploration subagents are
available, fan out **in parallel with distinct scopes**; otherwise cover the
same scopes sequentially — see
[references/exploration-guide.md](references/exploration-guide.md):

1. Structure & entry points
2. Data flow (write path AND read path, end to end)
3. Wiring (DI, config, registration, env)
4. Tests & quality gates
5. Git trajectory (~30 commits: what is the team building toward?)
6. Operational reality (deploy pipeline, environments, background jobs,
   data scale — docs that ignore how the thing ships are incomplete)

Classify components **works / half-wired / dead**, each with a proving file
path. Merge subagent reports and spot-check surprising claims yourself
before accepting them.

## Step 3 — Extract conventions

Conventions are what make generated code look native. Extract them with
evidence per [references/conventions-guide.md](references/conventions-guide.md):
naming, module boundaries, error handling, state, styling, test patterns.
**Rule: 2+ examples = convention; 1 example = observation; conflicting
examples = inconsistency (report it, do not pick a winner silently).**

## Step 4 — Verify the commands

Find the build / test / lint / run commands (manifests, CI config, Makefile)
and **run the safe ones** (read-only: build, test, lint — not deploy, not
migrate). Record real results: a test suite that fails on a clean checkout
is a first-class finding, not an embarrassment to hide. Commands you could
not run are listed as `UNVERIFIED` with the reason AND what would unblock a
real run (missing env var, service, credentials) — no unknown sits silently
behind a bare tag.

## Step 5 — Exemplar trace

The single most useful artifact for a newcomer: pick ONE representative,
recently-touched feature and trace it end to end — route/entry → handler →
service → storage → output/render, naming every file on the path. This
becomes the "How to add a feature here" section: the repo's own pattern,
proven by its own code, not a generic tutorial.

## Step 6 — Write the knowledge set

**Findings Brief Gate** — before writing a single file, present a compact
brief in chat: stack and architecture in a sentence or two, the target file
names (AGENTS.md vs CLAUDE.md), the verified command results, and every
inconsistency with a recommended resolution. 10–20 lines total; this is
the brief, not the docs. Ask for confirmation **once**. A correction here
costs one message; after Step 6 it costs a rewrite. If the user cannot
respond (headless/CI run), proceed — creating files is reversible and
nothing is deleted — but leave every inconsistency dual-cited and
unresolved, and tag any user-dependent choice `UNCONFIRMED` in the docs.

Then follow [references/knowledge-templates.md](references/knowledge-templates.md):

- `AGENTS.md` — ground rules from real conventions, verified commands,
  observed gotchas. **Under 150 lines.** (Write to `CLAUDE.md`/`AGENT.md`
  instead if the repo's tooling expects that name.)
- `docs/ARCHITECTURE.md` — overview, component table with status, data flow,
  the exemplar trace, inconsistencies and sharp edges.

Do NOT generate a ROADMAP.md — direction is the user's call, not the
code's. If half-wired components suggest unfinished intent, list them in
the report and offer deep-plan as the follow-up.

## Step 7 — Cold-start test

Re-read only the files you just wrote, as if you were a fresh agent, and
answer the numbered **Newcomer Questions** from Step 1 using the docs
alone. Every question you cannot answer from the docs is a gap — fix it,
or list it under Unverified with what would confirm it, before presenting.

Then run the **mechanical checks** — these are commands, not judgment
calls, and all MUST pass before presenting:

1. `wc -l AGENTS.md` → **150 or less.** Over budget = cut informative
   lines until it passes; do not present and apologize.
2. Repo metadata is evidence, not inference: any remote/hosting/author
   line in the docs must match `git remote -v` / git config output
   exactly. **Never construct a GitHub/GitLab URL from the repo's name —
   that is fabrication.** No remote configured = say so.
3. Every "convention" line cites 2+ locations; anything with one citation
   is relabeled *observation* — grep your own output for the word
   "convention" and check each.
4. Proportionality: docs should not dwarf the code (a 500-line app does
   not need 600 lines of architecture doc) — cut repetition, keep facts.
5. Walk the Newcomer Questions by number: every question is either
   answered in the generated docs or listed in the Unverified section.
   A silently dropped question fails the gate.
6. Every Gotcha line carries a `file:line` citation or an "observed
   running `<command>`" note. A gotcha that could be pasted into any
   repo's docs unchanged is deleted, not kept as filler.

## Step 8 — Report

- **The completed progress checklist** from the top of this skill —
  checked off honestly; an unchecked item with a reason beats a falsely
  checked one.
- **Created:** the files, one line each.
- **Key findings:** stack, architecture in one paragraph, top 3 sharp edges.
- **Inconsistencies:** conventions that conflict (the team may want to pick one).
- **UNVERIFIED:** what you could not confirm and why.
- **Suggested follow-up:** half-wired components worth a deep-plan run.

## When things go wrong

| Situation | Response |
|-----------|----------|
| Repo is empty or only scaffolding | Complete with minimal docs noting current state; AGENTS.md states "scaffolding only, no features yet" |
| Commands fail on clean checkout (Step 4) | Record honest failure with output; this is a first-class finding, not a failure of the skill |
| No git history available | Skip git trajectory (Step 2 Scope 5); note `UNVERIFIED: no git history` in ARCHITECTURE.md; rely on file timestamps |
| User unavailable at Findings Brief Gate (headless) | Proceed with file creation (reversible); leave inconsistencies dual-cited and unresolved; tag choices `UNCONFIRMED` |
| Cold-start test fails (Step 7) — docs don't answer Newcomer Questions | Fix the gaps or list them under Unverified with what would confirm them; do not present until gate passes |
