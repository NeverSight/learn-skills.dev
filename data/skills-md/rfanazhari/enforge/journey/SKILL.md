---
name: journey
description: "Compose business capabilities into an end-to-end user journey document (UJ-00N) for a single primary actor, before any code exists. Each journey step references an existing or to-be-created capability doc and its BR-XXX rules — the journey never restates rule text. Use this whenever the user says 'user journey', 'journey doc', 'journey document', 'UJ-', 'alur pengguna', 'buat journey', 'end-to-end flow', 'compose capabilities', 'chain these capabilities', or asks how several capabilities fit together into one business flow from trigger to outcome. Also use when the user has a business document and wants to find out which capability docs still need to be written (discovery), or has capability docs and wants them stitched into a flow with conflicts and gaps flagged (compose). Do NOT use for writing the capability docs themselves (capability-doc-generator), for system/technical design (engineering-tripack-generator), or for documenting how existing code behaves (flow-scanner). Trigger prefix: journey:"
---

# Journey

Turn a business document and a set of capabilities into a **user journey document**: one
primary actor pursuing one business goal, step by step, where every step points at the
capability (`CAP`) and business rules (`BR-XXX-0NN`) that govern it.

The journey is a **parent by reference**:

```text
UJ-00N  (journey)      — who wants what, and in which order things happen
  └─ CAP-xxx (capability) — one unit of business behaviour, owned by one service
       └─ BR-xxx (rule)    — one Given/When/Then decision with its business reason
```

A journey points down to capabilities and rules. It never copies them.

## Why this exists

Capability docs are deliberately narrow: one capability, one service, its rules. Nobody
reading them in isolation can tell whether the rules of `onboarding` and `kyc-verification`
actually line up when a real user walks through signup. The journey is where that question
is asked and answered — while it is still cheap, before the tripack and the code exist.

It also closes the loop in the other direction: starting from a business document, the
journey reveals **which capabilities need to exist at all**, so `capability-doc-generator`
can be pointed at the right targets instead of guessing.

## Scope boundaries

This skill writes **one journey document at a time**, at pure business level: actors,
intents, actions, outcomes, rules.

Do NOT do these, even if asked mid-task — offer them as separate follow-up work instead:

- Write or edit a **capability document** or any `BR-XXX` rule. Gaps go into the journey's
  "Gaps and open questions" section and are handed to `capability-doc-generator`.
- **Duplicate rule text.** A step cites `BR-XXX-0NN`; it does not restate the Given/When/Then.
  If the reader needs the rule, they follow the reference.
- Describe **system design**: services, APIs, endpoints, tables, queues, UI widgets, error
  codes. Those belong to `engineering-tripack-generator`. If the source document is full of
  them, translate each into the business action or outcome it serves and drop the rest.
- Write a journey with **more than one primary actor**. See "Actor model". If the request
  genuinely has two goal-owners, it is two journeys — say so and offer to write both.
- Write the implementation code.
- Claim anything is implemented. The journey describes what *should* happen; nothing has
  been verified against code.

## Modes

Mode is the **mandatory first input**. It determines what must be provided, what the output
contains, and which skill runs next.

| Mode | Required input | Optional input | Primary outcome |
|---|---|---|---|
| `compose` | Business doc **and** links/paths to the existing capability docs | — | Journey doc where every step references an existing CAP and its BR ids; conflicts between capabilities and gaps in coverage are flagged |
| `discovery` | Business doc | Existing capability docs, if any | Journey doc **plus** a "capabilities needed" list with suggested CAP titles, ready to hand to `capability-doc-generator` |

**If the mode is not given, ask for it before doing anything else.** Do not infer it from
the number of files provided, do not read the documents first, do not start drafting. A
one-line question is enough:

> Which mode — `compose` (capability docs exist, stitch them into a journey) or
> `discovery` (start from the business doc, find out which capabilities are needed)?

## Pipeline position

The skill sits in a different place depending on the mode:

```text
discovery:  journey ──▶ capability-doc-generator ──▶ journey (compose, re-run) ──▶ engineering-tripack-generator
compose:    capability-doc-generator ──▶ journey ──▶ spec-delta-analyzer / engineering-tripack-generator
```

The last section of every journey document names the recommended next skill (see Step 9).

## Actor model

**One journey = one primary actor with one business goal.** The primary actor is the one
whose intent starts the journey and who receives the outcome at the end.

Everyone else is a **supporting actor**: they appear on individual steps ("approved by
Admin", "verified by Compliance Officer") and are recorded in that step's Actor column.
They never co-own the journey, and their own goals are not described here.

When a step depends on data or state produced by **another actor's flow** — an export
reads records that a different actor created, a payout requires a merchant that another
journey onboarded — that is a **cross-journey dependency**, not a second primary actor:

- Record it under "Depends on" with the other journey's id (`UJ-00M`).
- If that flow has no journey document yet, use a placeholder id (`UJ-TBD-<slug>`), and
  list it under "Gaps and open questions" as a missing journey.
- Do not pull the other flow's steps into this journey. Reference it, and move on.

The reverse relation goes under "Used by": journeys that depend on the state this one
produces, when you know them.

## Input needed

Collect these before writing. Ask for whatever is missing rather than inventing it.

1. **Mode** — `compose` or `discovery`. Mandatory, first, no default.
2. **Business document** — requirement, PRD section, meeting notes, or a verbal explanation.
   Both modes need it; it is where the actor, goal, trigger, and ordering come from.
3. **Capability docs** — paths or links to `docs/business/capabilities/*.md` in the target
   repo. Required in `compose`; optional in `discovery`.
4. **Journey title and primary actor** — if not obvious from the business document, offer
   2–3 options and let the user choose. Never silently invent them.
5. **Related journeys** (optional) — anything the user already knows this flow depends on
   or feeds into.

If the business document is too thin to establish a clear trigger, actor, and outcome, say
so and ask. A journey assembled from guessed steps is worse than no journey.

## Step 1 — Select the mode

Confirm the mode and check its required input is present:

- `compose` without capability docs → ask for them, or ask whether the user meant
  `discovery`.
- `discovery` with capability docs provided → use them for the steps they cover, and treat
  everything else as a gap.

State the chosen mode back to the user in one line before continuing.

## Step 2 — Locate the repo and the journeys folder

Read `AGENTS.md` or `CLAUDE.md` at the repo root to learn the repo name and layout. Derive
the path rather than assuming:

```text
<repo-or-service-root>/docs/business/journeys/UJ-00N-<slug>.md
```

Journeys are cross-service by nature, so in a mono-repo they usually sit at the repo root's
`docs/business/journeys/`, next to (not inside) the per-service `capabilities/` folders.
If the folder does not exist yet, this is the first journey — say so and confirm the path
before writing.

**Numbering.** Scan the folder for existing `UJ-` ids and take the next free number,
zero-padded to three digits (`UJ-001`, `UJ-002`, …). If the folder is empty, propose
`UJ-001` and confirm. The `<slug>` is the kebab-case journey title.

## Step 3 — Establish actor, goal, trigger

From the business document, extract and confirm:

- **Primary actor** — one role, named the way the business names it.
- **Business goal** — one sentence from the actor's point of view ("get my first payout").
- **Trigger** — the event or decision that starts the journey.
- **Preconditions** — what must already be true before the trigger counts.
- **End state** — what is true when the journey has succeeded.

If two candidate primary actors emerge, stop and split: this is two journeys.

## Step 4 — Read the capability docs

Skip this step only in `discovery` with no capability docs provided.

For each capability doc:

1. Note its `id`, owning service, and the rule ids it declares.
2. Pull out the actors and triggers it covers — this is what the journey steps attach to.
3. Note anything that looks like an invariant across capabilities: a status that must be
   reached before another capability may act, a quantity that two rules both constrain, a
   term defined differently in two ubiquitous-language tables.

Do not read the implementation. The journey describes intended behaviour, and code is not
evidence of intent.

## Step 5 — Build the happy path

Write the main success sequence as a table, one row per step:

| Column | Content |
|---|---|
| Step | `S1`, `S2`, … — stable ids, never renumbered on revision |
| Actor | Primary actor by default; a supporting actor where the business says so |
| Action | A business action in plain language — what the actor does or decides |
| Capability | The capability doc that owns this behaviour (see "Referencing capabilities") |
| Rules | The `BR-XXX-0NN` ids that govern the step, as ids only |
| Outcome | The business-visible result of the step |

A step is one business action with one outcome. If the Outcome needs "and then", split
the step. If several consecutive steps are all internal to one capability with nothing
business-visible between them, merge them — the journey is the actor's view, not the
system's.

**Referencing capabilities.** Use the `id` from the capability doc's frontmatter, linked to
the file (`[kyc-verification](../capabilities/kyc-verification.md)`). If the target repo
uses explicit `CAP-xxx` ids, use those. For a capability that does not exist yet
(`discovery`, or a gap found in `compose`), write `CAP-TBD-<suggested-slug>` and leave the
Rules cell as `—`; the same placeholder reappears in "Gaps and open questions".

## Step 6 — Add alternate and exception paths

Same table shape, one table per path. Name each path after the business situation that
causes it ("Document rejected by Compliance", "Actor abandons before confirmation"), state
which happy-path step it branches from, and end each path with where it rejoins or how it
terminates.

Cover the situations the business document names, plus the ones the capability docs' edge
cases make inevitable. Do not invent failure modes the business has not discussed — list
those as open questions instead.

## Step 7 — Check invariants, conflicts, and dependencies

**Cross-capability invariants** — conditions that must hold across more than one step or
capability for the journey to make business sense ("a Member is never billed before KYC
is approved"). Each invariant names the rules that enforce it. An invariant with no rule
behind it is a gap.

**Detected conflicts** — places where two capabilities disagree: contradictory rules,
one capability assuming a state another never produces, a term that means two things.
Record each with both rule ids, what the disagreement is, and who should decide. Never
resolve a conflict by picking a side in the journey document.

**Depends on / Used by** — fill from the actor model: cross-journey dependencies with
`UJ-00M` ids or `UJ-TBD-<slug>` placeholders, and the reverse relation where known.

## Step 8 — Record gaps and write the document

**Gaps and open questions** is where the two modes differ most:

- `compose`: steps with no capability to cite, rules the business document implies that no
  capability declares, missing journeys found under "Depends on", and product questions
  nobody has answered. Name who decides each.
- `discovery`: the same, **plus** a "Capabilities needed" list — one entry per
  `CAP-TBD-*` placeholder, with a suggested title, the owning service if it can be
  inferred, the journey steps it would cover, and the business behaviours it must
  contain. This list is the direct input for `capability-doc-generator`.

Then fill the **traceability matrix** (UJ → CAP → BR): every step, every capability it
cites, every rule id. Every rule referenced anywhere in the document must appear here,
and nothing may appear here that no step cites.

Write the file using the template in
[`references/journey-template.md`](references/journey-template.md). Keep every heading, in
that order, even when a section is short — write "None." rather than deleting it.

## Step 9 — Report back and name the next skill

The last section of the document, **Recommended next skill**, is decided by mode and by
what the journey found:

| Situation | Recommended next skill |
|---|---|
| `discovery` — any `CAP-TBD-*` placeholders | `capability-doc-generator`, once per entry in "Capabilities needed"; then re-run `journey` in `compose` mode against the new docs |
| `discovery` — every step already had a capability | Treat as `compose`: see the rows below |
| `compose` — unresolved conflicts or blocking open questions | None yet — resolve the listed conflicts first; name the decider |
| `compose` — a current-state flow or contract document exists for this journey | `spec-delta-analyzer` with this journey as the existing-flow document |
| `compose` — clean, greenfield | `engineering-tripack-generator` with this journey (and its capability docs) as input |

After writing the file, tell the user:

- Where it was written and which `UJ-` id was assigned
- Which mode was used
- The step count on the happy path and the number of alternate paths
- Every conflict and every `CAP-TBD-*` / `UJ-TBD-*` placeholder, in one line each
- The recommended next skill, and why that one

## Rules

- **All output documents must be written in English**, regardless of conversation language
- Mode first. No reading, no drafting, no path discovery until the mode is confirmed
- One primary actor, one goal. Supporting actors live on steps; other flows live under
  "Depends on"
- Reference, never restate: rule ids in the journey, rule text in the capability doc
- Business level only — if a sentence names a service, endpoint, table, or screen, rewrite
  it as the business action it performs or delete it
- Placeholders (`CAP-TBD-*`, `UJ-TBD-*`) are visible gaps, not quiet guesses: every one
  must appear under "Gaps and open questions"
- Conflicts are reported with both sides and a decider, never silently resolved
- Step ids are stable across revisions — add new ids, never renumber
- The journey is `status: draft` while any placeholder or unresolved conflict remains, and
  `status: planned` once every step cites an existing capability. Neither means
  implemented
