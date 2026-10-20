---
name: design-memory
description: Use at project start and completion to OBSERVE and record how the user designs — the decisions they make, the styles they reach for, their habits and inclinations across projects. This is a descriptive record (a mirror), NOT a controller — it is never fed back to steer the work. Per-project direction comes from design-taste and a DESIGN.md; design-memory only watches and reflects, surfaced to the user as a report out of curiosity
---

# Design Memory

Design memory is an **observational record of how you design** — the decisions you make, the styles you reach for, the habits and inclinations that show up across projects. It is a mirror, not a controller. It notices what you do and reflects it back to you out of curiosity. It does **not** steer future work.

## The one rule that defines this skill

**Design memory is descriptive, never prescriptive.** It records what you did; it is *not* applied to drive new projects. The current project's direction comes from what you tell the team now (`design-taste`) and from any brand spec you provide (`design-md` / `DESIGN.md`) — never from this record. Observation that never feeds back into the work cannot mis-steer it, which is exactly why a record built across many different clients stays safe and honest: it's a journal, not a set of orders.

If you ever want to *act* on an observation, that's your call to make explicitly in the moment — the system will not quietly apply your past decisions to a new client's project.

## Welcome Gate

**BEFORE reading or updating design memory, check whether the Designpowers welcome sequence has been shown this session.** If the user has not yet seen the welcome (the bird, the greeting, and the walkthrough offer), you MUST invoke the `using-designpowers` skill FIRST and complete the welcome sequence before returning here. The bird must appear before any work begins. No exceptions.

## When to Use

- **At project completion** — observe the project's decisions and add them to the record
- **When the user asks** "how do I design?", "what are my habits?", "what's my style?" — produce the report
- **When the user makes a notably characteristic choice** — note it as an observation
- It is **not** loaded to constrain a new project. (Loading at project start is only to *show the user their report if they want it*, not to feed preferences into the pipeline.)

## The Record (`taste-profile.md`)

Lives at `~/.designpowers/taste-profile.md` (cross-project). It is a journal of observations about how the user works — not a rulebook. Every entry is phrased as *something observed*, with evidence, never as an instruction for future work.

### Structure

```markdown
# Design Record — How [user] Designs
_An observational journal. Descriptive, not prescriptive — this is never applied to steer projects._

_Last updated: [date] after project [project name]_
_Projects observed: [count]_

## Recurring Decisions
Choices that have shown up more than once — noticed, not mandated.

| Observation | Times seen | Evidence |
|-------------|-----------|----------|
| [e.g., "Reaches for generous whitespace"] | 3 projects | A, C, D — chose it unprompted |
| [e.g., "Decides colour last, after structure"] | 2 projects | Sequence in B, D |

## Style & Habits
How the user tends to work and decide (not what to impose).

- **Visual leanings:** [e.g., "warm neutrals show up often; rarely picks saturated primaries"]
- **Process habits:** [e.g., "subtracts before adding — overrides usually remove an element"]
- **Decision style:** [e.g., "settles type and spacing before touching colour"]
- **Content voice tendencies:** [e.g., "consistently plain language, contractions, grade ~7"]

## Inclinations & Curiosities
Softer, single-occurrence or emerging things worth noticing — explicitly uncertain.

| Noticed | Where | Note |
|---------|-------|------|
| [e.g., "tried a serif display once and kept it"] | Project D | one occurrence, may not be a pattern |

## Things the user has moved away from
Choices they've reversed or corrected — observed, not a ban.

| Observation | Evidence |
|-------------|----------|
| [e.g., "removed gradient backgrounds twice"] | A, B |

## Project History
| Project | Date | What was decided | What it suggested about how they work |
|---------|------|------------------|----------------------------------------|
| [name] | [date] | [key decisions] | [the habit/inclination it revealed] |
```

## Process

### Observing (during and at end of a project)

Watch for **signals about how the user decides** — and record them as observations, with evidence:

| Signal | What it tells you |
|--------|-------------------|
| **User override** | A strong signal of an inclination — note *what* they changed and *to what* |
| **Explicit statement** ("I always…", "that's not me") | The user naming their own habit — record their words |
| **Emphatic approval** | A choice that resonated — worth noting |
| **Correction** ("no, more like…") | A direction they lean away from |
| **Silent approval** | Weak — don't record until it recurs |

When you notice a signal:
1. Phrase it as an **observation** ("reaches for X", "tends to decide Y last"), never a rule ("always use X").
2. Check whether it reinforces an existing observation (increase the count / add evidence) or is new (add it under the right section).
3. If it *contradicts* an earlier observation, don't agonise — just note both; people change, and the record is a journal, not a contract.

### Consolidating (end of project)

When a project completes:
1. Review the decisions in `design-state.md` and the user's overrides.
2. Add observations to the record, with evidence and project attribution.
3. **Keep it to how the user works, not what this client needed.** A client's required brand colour is *that client's* taste (it lives in their `DESIGN.md`) — it is **not** an observation about the user. Only record things that reflect *the user's own way of deciding*, the kind that would still be true with a different client.
4. Offer the report: "Want to see what this project added to your design record?"

## The Report

The primary way the user experiences design memory is as a **report they read out of curiosity** — "here's how you design." Generate it from the record by synthesising *across* observations, not just listing them:

```markdown
# How You Design
_Observed across [N] projects · descriptive, not applied_

## In one line
[The sharpest honest characterisation — e.g. "You're a subtractor who trusts whitespace and decides colour last."]

## How you tend to decide
[3-5 observations about process and decision-making, each with evidence.]

## What you reach for
[Recurring stylistic choices, framed as tendencies, with counts.]

## What you've moved away from
[Reversals/corrections, as observations.]

## Curiosities & emerging things
[Single-occurrence or uncertain signals — explicitly low-confidence.]

## Where the record is thin
[Honest note on what there isn't enough evidence to say yet.]
```

Rules for the report:
1. **Synthesise, don't transcribe** — the value is patterns across entries, not a table dump.
2. **Every claim cites evidence** — no evidence, no claim.
3. **Describe, never prescribe** — "you tend to…" never "you should…" and never "so I'll apply this."
4. **Be honest about confidence** — separate well-evidenced habits from one-off curiosities.
5. **It's a mirror, offered with curiosity** — the goal is self-awareness, not a grade and not a directive.

## What design memory does NOT do

- It does **not** pass preferences to design-lead, design-strategist, or any agent as constraints.
- It does **not** gate or steer the build. The pipeline runs from the brief, the personas, `design-taste` (your live direction for *this* project), and any `DESIGN.md`.
- It does **not** override or even nudge project decisions. If a past habit is relevant, the *user* raises it; the system won't apply it silently.

This is the deliberate design: by never feeding back, the record can accumulate across wildly different clients without ever contaminating a new project. Observation is safe precisely because it's inert.

## Integration

- **Called by:** `using-designpowers` (may offer the report), `design-state`/`design-retrospective` (at project end, to add observations)
- **Reads from:** `design-state.md`, handoff chain, user overrides — to *observe*, not to extract constraints
- **Writes to:** `~/.designpowers/taste-profile.md` (the observational record)
- **Does NOT inform:** the agents or the build — by design
- **Distinct from:** `design-taste` (your live aesthetic *direction* for the current project, which IS applied) and `design-md` (the client's brand spec, which IS applied). Design memory only watches.

## Anti-Patterns

| Pattern | Why It Fails |
|---------|-------------|
| Feeding the record back into the build as constraints | This is the old prescriptive model. The record is descriptive — applying it silently is exactly the contamination we're avoiding |
| Recording a client's brand requirement as the user's taste | A client's `DESIGN.md` is that client's, not the user's way of working. Only record portable observations about *how the user decides* |
| Phrasing observations as rules ("always use X") | It's a journal, not a rulebook. "Reaches for X (3 projects)" is honest; "always use X" is a directive the system shouldn't issue |
| Recording every decision | Most choices are contextual. Note the ones that reveal something about how the user works |
| Treating the record as a grade | It's a mirror offered out of curiosity, not a scorecard |
