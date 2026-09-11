---
name: simplify
description: Clean up and simplify recently changed code for quality — not bug-hunting. Use whenever the user asks to "simplify", "clean up this code", "tidy up my changes", "refactor for clarity", "polish my diff", "make this cleaner", or wants their recent edits reviewed for reuse, simplification, efficiency, and altitude (right-depth) issues before committing or opening a PR. Reviews the git diff through four cleanup lenses — Reuse, Simplification, Efficiency, Altitude — presents the findings, and applies the fixes on approval. Does NOT hunt for correctness bugs; that is a separate code-review task. Trigger even if the user only says "can you simplify what I just wrote."
---

# Simplify

> ⚠️ **DO NOT install this in Claude Code.** Claude Code ships its own native `/simplify`
> command, purpose-built for that harness — it fans the four lenses out to four real
> parallel review subagents and is tuned to Claude Code's tools. This skill is a **portable
> clone for agents that lack it** (Codex, Cursor, and other [skills.sh](https://skills.sh)
> targets). Installing it inside Claude Code would only shadow the better built-in. Use the
> native `/simplify` there instead.

Improve the quality of recently changed code — do **not** hunt for bugs. Review the
diff through four cleanup lenses (Reuse, Simplification, Efficiency, Altitude), then
fix what you find. Correctness bugs are out of scope here; a dedicated code-review pass
handles those. Keeping the two separate is deliberate: bug-hunting and quality-cleanup
pull attention in different directions, and mixing them makes both worse.

The guiding principle throughout: **preserve behavior exactly.** Every change must leave
what the code does untouched — only *how* it does it improves. Prefer readable, explicit
code over clever compression; "fewer lines" is not the goal, clarity is.

## Phase 0 — Establish the scope

Get the exact set of changes under review. Run the first of these that yields a diff:

```bash
git diff @{upstream}...HEAD      # changes on this branch vs. its upstream
git diff main...HEAD             # fallback if there is no upstream
git diff HEAD~1                  # fallback for a single recent commit
```

Also run `git diff HEAD` to capture **uncommitted** working-tree changes — this skill
usually runs *before* a commit, so those edits are the whole point. If the range diff
above is empty, the working-tree diff is your scope.

If the user named a specific target — a file path, a branch, or a PR number — review that
instead (`git diff main...<branch>`, or check out / fetch the PR). When nothing is
committed or diffable yet, fall back to the code the user just wrote or pointed at in the
conversation.

Treat this diff as the review scope. Do not wander outside it: findings should be about
the changed lines and the code they directly touch, not a general audit of the repo.

## Phase 1 — Review through the four lenses

Read the diff carefully and pass it through each lens below, in order. For every issue,
record: the **file and line**, a **one-line summary**, and the **concrete cost** — what is
duplicated, wasted, or harder to maintain because of it. A finding without a concrete cost
is usually a matter of taste; drop it.

> **If your agent can spawn parallel subagents** (e.g. Claude Code's Task tool, Amp),
> you may fan these four lenses out to four concurrent reviewers for speed. Most agents
> (Codex, Cursor, etc.) are single-agent — just walk the four lenses yourself in one pass.
> The lenses matter; the parallelism is only an optimization.

### Reuse

Flag new code that re-implements something the codebase already has. Grep the shared /
utility modules and the files adjacent to the change, and **name the existing helper to
call instead**. The cost of a near-duplicate is silent drift — two copies of the same idea
that will disagree the first time only one gets fixed.

### Simplification

Flag unnecessary complexity the diff adds: redundant or derivable state, copy-paste with
slight variation, deep nesting, dead code left behind. **Name the simpler form that does
the same job.** Avoid nested ternaries and dense one-liners — prefer an `if`/`else` chain
or an early return that a reader can follow without unpacking.

### Efficiency

Flag wasted work the diff introduces: redundant computation or repeated I/O, independent
operations run sequentially that could run together, blocking work added to startup or a
hot path. Also flag long-lived objects built from closures or captured environments — they
keep the entire enclosing scope alive for the object's lifetime, which leaks memory when
that scope holds large values; prefer a class/struct that copies only the fields it needs.
**Name the cheaper alternative.** Don't micro-optimize cold paths — weigh the cost against
how often the code runs.

### Altitude

Check that each change sits at the right depth, not as a fragile bandaid. Special cases
layered on top of shared infrastructure are a sign the fix isn't deep enough — **prefer
generalizing the underlying mechanism over piling on special cases.** This is the subtle
one: a change can be clean line-by-line yet still be at the wrong altitude because it
patches a symptom where the real fix belongs one layer down.

## Phase 2 — Present the findings

Dedup findings that point at the same line or mechanism. Drop anything that would change
behavior, reach well outside the reviewed diff, or that you judge to be a false positive —
note the skip briefly rather than arguing with it.

Present what remains as a short list grouped by lens, each with its file:line, the concrete
cost, and the concrete fix you propose. Then **stop and ask for the go-ahead before
editing.** If nothing survived review, say so plainly — "the changes already look clean" is
a valid and useful result; don't invent work to look busy.

## Phase 3 — Apply on confirmation

Once the user approves (all findings, or the subset they pick), make the edits directly.
Apply only fixes that preserve behavior exactly. After editing:

- Re-read each changed region to confirm the simplification is correct and complete.
- If tests or a type-checker are readily available, run them to confirm behavior held.
- Finish with a brief summary: what was fixed, and what you skipped and why.

## What this skill does not do

- **Bug-hunting / correctness review** — use a dedicated code-review pass for that.
- **Broad refactors outside the diff** — stay within the reviewed changes.
- **Behavior changes, feature work, or "while I'm here" rewrites** — out of scope by design.
