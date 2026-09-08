---
name: giljabi
description: Run a feature from an idea to merged PRs while keeping the repo's knowledge layer true at every phase — grill (pages tended first), spec, tickets sliced into independently-mergeable PRs, a plan commit, sequential implementation with page updates in the same diff, three-axis review that tends every page it touches, a closing index check across stacked slices. Owns the phase order and the context resets; each phase's method lives in its own skill. Use when starting or resuming feature work.
---

# giljabi (길잡이)

Six phases from an idea to merged PRs. This skill does none of the work — each phase belongs to a
skill that exists on its own. What it owns is **the order, the slices, and where the context resets.**

A feature does not fit in one context window. The fix is not a bigger window: **every phase leaves an
artifact**, so the next phase reads a file instead of remembering a conversation. Once that holds, a
reset costs nothing.

| Phase | Skill | Leaves behind |
| --- | --- | --- |
| 1. Interrogate | `/grill` (tends touched pages first via `/knowledge-tend`) | knowledge pages (`(intended)`-marked), `findings.md` |
| 2. Specify | `/to-spec` — drafted by a `deep` agent from `findings.md`, edited here | `spec.md` |
| 3. Slice | `/to-tickets` — drafted by a `deep` agent from `spec.md`, approved here | `issues/NN-*.md`, `slices.md` |
| 4. Commit the plan | — | the `(intended)` pages as the first commit on the feature branch |
| 5. Build, per slice | `/implement` × N, `/review` (the layer's primary tend — `/knowledge-tend` on every page the slice touches), `/pr` | code, page updates, one PR per slice |
| 6. Close | `/knowledge-tend` check 2 on the feature's pages, when slices stacked | cleanup, index and relations re-checked across the series, friction routed to retro |

Phases 1–3 need only the knowledge pages (`docs/domain/`, `docs/platform/`) and tolerate their absence. If `docs/agents/` is missing, say
so once and continue; the gate is at phase 4.

## Not every change is a feature

A change that fits one context window and ships as one PR runs the standalone path:
`/implement` → `/review` → `/commit` → `/pr`. No `.scratch/`, no plan commit, no phases. The knowledge
discipline is not what is skipped — `/implement` still updates pages in the same diff and `/review`'s
Knowledge axis still fails drift; only the ceremony that exists to survive context resets is.

The test is artifacts, not size: **if you would need `STATE.md` to resume it, it is a feature** and
runs the six phases. A one-line fix never needs one; a change whose interview surfaces a fork you
cannot settle in one sitting always does — at that point stop, name the slug, and start phase 1 with
what you have learned as the first entry in `findings.md`.

## Phases 2 and 3 — draft delegated, decision here

`/grill` checkpoints `findings.md` after every round so that the transcript is disposable at the end
of phase 1. Phase 2 tests that: spawn a `deep` agent to run `/to-spec` **from `findings.md` and the
repo**, not from this conversation. It returns the draft; you review and edit it here with the user,
then write `spec.md` and publish. If the draft is thinner than the discussion felt, the checkpoint
was thin — fix `findings.md`, re-run the drafter, and log the gap as `[friction]`. Phase 3 is the same
shape: a `deep` agent drafts the ticket breakdown from `spec.md`; the `/to-tickets` quiz runs here as
a **gate** — the breakdown is published only after the user has answered it, and the approval that
closed the spec does not carry over to the breakdown. Both phases' decisions — the spec's defaults,
the quiz's seams, granularity and slice boundaries — go through the structured-question capability
(harness map below), one question per decision, recommendation first, with the argument in prose
beside it as `/grill` does. A default confirmed in prose alone is a default nodded through.

## Phase 4 — commit the plan

**Gate:** `docs/agents/` must exist from here on — branch names, commit language and the PR host all
come from it. Missing → stop and run `/setup`; a workflow that guesses the integration branch
produces PRs nobody wants.

Phase 1 wrote knowledge pages carrying `(intended)` claims. Open the feature branch — one branch for
the whole feature, `feat/<feature-slug>` in `vcs.md`'s convention — and commit them as its first
commit. They ship in slice 1's PR, reviewed beside the code that proves them; every later slice is a
commit on the same branch, so nothing branches blind to the plan. Open the plan as its own PR first
only when the user asks for the design reviewed at design size — it buys that at the price of a
serial merge before any code.

## Phase 5 — build, slice by slice

A **slice** is a group of tickets that ships as one independently-mergeable PR (`/to-tickets`
declares them, in `slices.md`). Tickets bound a context window; slices bound a review. A slice is
not where the context resets — tickets are — and a ticket is not a PR. Slices run **sequentially,
always** — never in parallel, whatever the ticket graph looks like. Per slice:

1. **Branch** — the feature branch from phase 4, stacked: every slice is commits on
   `feat/<feature-slug>`, and each slice's PR is opened from that branch at the slice boundary. After
   a slice's PR merges, sync the branch with the integration branch (`vcs.md`'s merge strategy
   decides merge or rebase) before the next slice's commits — `/pr` scopes from the merge base, and
   under squash-merge an unsynced branch describes the previous slice again.
2. **Implement** — one `/implement` run per ticket, a context reset between tickets. Work the
   frontier: any ticket whose blockers are done, lowest number first. Name tickets by **filename**
   (`/implement 03-invitations-follow-organization-timezone`), never by position.
3. **Review** — `/review` at slice scope: fixed point is the previous slice's merged tip (the
   feature branch's start for slice 1), spec source is
   `spec.md` restricted to this slice's tickets; its three axes run as `deep` agents. `/review`
   disposes its findings and re-checks the fixes at its own scope (its step 4); `/commit` when it is
   green or when a failure is accepted out loud — by the user, not by you.
4. **PR** — `/pr`, run by a `standard` agent. Then write `STATE.md` and reset the context.

The ticket close-out — tests green, page updates in the diff, `/commit`, `STATE.md` — fires at the
reset between tickets. Tickets run back to back in one window blur the boundary, and the close-out
is what goes missing.

## Phase 6 — close

After the last slice's PR merges:

```bash
git fetch origin
# 1. The feature's commits are on the integration branch:
git log origin/<integration-branch> --oneline | head -20
# 2. The knowledge pages landed — derive from the merged ranges, not memory:
git diff --name-only <merge-base> <last-merge-commit> -- docs/
# 3. Only when both hold:
rm -rf .scratch/<feature-slug>
```

`.scratch/` is gitignored; a deleted directory is unrecoverable. That is the point — and why the
checks run first, every time.

**Re-check what only the merged range can show.** A feature of more than one slice runs
`/knowledge-tend` scoped to its pages, check 2 only — the index and relations as they stand after
every slice landed, the one shape no per-slice review saw whole. A single-slice feature skips it and
says so: its merged range is the diff its review already checked. Shape (check 3) was `/review`'s job
on each slice, where a split rides the slice that caused it; a shape proposal surfacing here means a
review missed it, which is a `[friction]` line, and the fix is its own docs commit on approval.

**Route the friction.** `findings.md` lines tagged `[friction]` — moments a skill fought you, an
instruction that misfired, a gate that checked the wrong thing — append to `retro/inbox.md` in the
giljabi repo checkout. `/retro`, run there, reads the inbox, proposes one skill diff per item,
applies each only on approval, and deletes the routed lines. Evolution is regular, never
automatic — a skill that edits itself unsupervised is a feedback loop with no test.

## Delegation and tiers

Work leaves this context when its primary source is an artifact, not the conversation. Three
**tiers** name how much model a delegated job deserves; each fixes model *and* reasoning effort
together, because both answer one question and two knobs is a choice with no rule:

| Tier | Runs | Claude Code | Codex |
| --- | --- | --- | --- |
| `deep` | `/to-spec` and `/to-tickets` drafts; every `/review` axis | agent type `deep` (`fable`, effort high) | `spawn_agent(model: gpt-5.6-sol, reasoning_effort: high)` |
| `standard` | `/pr`; also the inline session default | agent type `standard` (`opus`, medium) | `spawn_agent(model: gpt-5.6-terra, reasoning_effort: medium)` |
| `fast` | `/commit`; test runs; read-only search sweeps | agent type `fast` (`sonnet`, low) | `spawn_agent(model: gpt-5.6-luna, reasoning_effort: low)` |

The Claude Code agent types ship in this repo's `agents/`. `/grill`, `/setup` and `/implement` never
delegate their own work — their primary source is the user. Never verify a tier by asking the model
what it is: self-report is wrong on both harnesses; the harness's session log is the evidence.

## Harness map

Skills name capabilities, not one harness's spelling of them. Where a skill says one of these, do
what this session's harness offers:

| Capability | Claude Code | Codex |
| --- | --- | --- |
| reset the context | `/clear` | `/new` |
| summarise and continue | `/compact` | `/compact` |
| hand off to another session | `/handoff` | write the handoff document by hand |
| ask the user a structured question | `AskUserQuestion` | ask in prose; Codex has no equivalent outside plan mode |
| read-only search subagent | `Explore` | `spawn_agent` with a read-only instruction — Codex has no read-only type, so state the constraint in the prompt |
| tiered subagent | agent types `deep`/`standard`/`fast` | `spawn_agent(model, reasoning_effort)` per the tier table |

Codex subagents can invoke skills and can be pinned to a model (both verified). On an unmapped
harness, translate these six yourself before the first phase and write the translation to
`directives.md`.

## STATE.md — where you are

Artifacts carry content; none carries **position**. `.scratch/<feature-slug>/STATE.md` does,
**overwritten as the closing act of each phase and each ticket**:

```
# State — email-language

Workflow: /giljabi — read that skill before acting
Phase:    5 of 6 — build (slice 2 of 3)
Next:     /implement 04-timezone-backfill
Slices:   1 merged (PR 5699) · 2 in progress: 03 done, 04–05 open · 3 not started
Branch:   feat/email-language-timezone
Directives: 2 active — directives.md
Also:     one-line pointers only — side quests, experiments, warnings
```

Hard cap ~12 lines. **A line may point, never narrate** — slice detail lives in `slices.md`,
outcomes in `findings.md`, operating hazards on knowledge pages. The previous design allowed
narration nowhere and gave overflow no destination, so overflow went here; the destinations now
exist, so use them. Write it when work completes, not when context resets — a reset leaves no turn
to act. Read it first when a session starts mid-feature, then `directives.md`, then the phase's
artifact.

## directives.md — what the user told you to do differently

An instruction from the user that is not spec, not a repo fact, and not a hazard — "skip the e2e
suite this week", "log every skill hiccup to workflow-notes.md", "don't touch the billing module
until Kim's PR lands" — has no page and no ticket. It goes to `.scratch/<feature-slug>/directives.md`
the moment it is said: one line each, current state only, rewritten in place, deleted when it
lapses. Every session start reads it after `STATE.md`; every delegated agent is told to read it. It
is not `findings.md` — that file grows and its register is unjudged discovery; a directive on line
40 is a directive missed.

## Boundaries

At the end of each phase or ticket, take the first yes:

1. **Does the next step need this conversation as a primary source?** Continue. True inside a phase;
   false the moment the artifacts capture it — which phases 2 and 3 exist to do.
2. **Is everything here disposable now?** Reset the context. The usual answer after phase 3,
   between tickets, and after each slice's PR. If the spec reads thinner than the discussion felt,
   fix the spec — don't keep the transcript.
3. **Is the work travelling** — new harness, new repo, a colleague? Hand off.
4. **Can it run unattended, tightly scoped?** A subagent. Discovery sweeps, yes; a ticket, never —
   `/implement` keeps you in the loop by design.
5. Otherwise summarise and continue, with an instruction naming what the next phase needs. Last
   resort, not first reach — a summary is confidently wrong about exactly one decision, and you don't know which.

## Capturing as you go

Every phase appends to `.scratch/<feature-slug>/findings.md` the moment something surfaces — a
defect passed by, a constraint measured, an hour-eating gotcha, a `[friction]` moment with a skill.
Immediate and unjudged: a finding not written within a minute is gone. Routing is judged later —
`/implement` routes discoveries as it works; phase 6 routes friction.

## Before the first run

`/setup` writes `docs/agents/` (vcs, testing, tracker) and the `docs/domain/` scaffold. Phases 1–3
run without it; phase 4 does not (see its gate). Facts may live in other repos — read them wherever
they are. Artifacts are single-homed: `.scratch/`, `docs/`, and every branch belong to the repo
being changed.

## Anti-goals

- **Do not re-explain a phase's skill here.** This file owns sequence and boundaries; each skill owns
  its method. Two copies drift, and this is the copy with no tests.
- **Do not batch tickets into one `/implement` run.** A run spanning four tickets is the context
  problem this skill exists to avoid, wearing a different hat.
- **Do not parallelize slices**, however clean the graph looks. Independently *mergeable* is weaker
  than concurrently *editable*, and nothing computes the stronger property.
