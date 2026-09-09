---
name: talkcraft
description: Build, rewrite, critique, or rehearse high-stakes presentations, talks, slide decks, lectures, thesis defenses, demos, and executive briefings using a Winston-inspired framework centered on promise, structure, pacing, examples, transitions, and rehearsal discipline.
metadata:
  tags: presentation, speaking, slides, rhetoric, coaching
---

# TalkCraft

## Overview

Use this skill when the user needs a presentation strategy before slides, a stronger talk structure, a ruthless outline review, speaker notes, rehearsal support, or a deck rewrite grounded in presentation craft rather than generic slide advice.

This skill distills Winston-style presentation principles into an agent workflow that works across Codex, Claude, and other instruction-following agents. It produces strategy first, artifacts second.

## Use When

Trigger this skill for requests such as:

- "Help me prepare a keynote."
- "Rewrite this deck for an executive audience."
- "Audit my thesis defense."
- "Turn rough notes into a talk outline."
- "Prepare speaker notes and Q&A."
- "Make this technical presentation clearer."

Do not use this skill for purely visual slide polishing with no narrative problem. In that case, use a design or slides skill after the storyline is stable.

## Operating Modes

Choose one mode early and say which one you are using:

1. `Design`
   Build a talk from scratch from topic, audience, and time.
2. `Audit`
   Critique an existing outline, deck, or speaker script against the rubric.
3. `Rewrite`
   Keep the core content, replace the structure and delivery plan.
4. `Rehearse`
   Build trim plans, speaker notes, likely questions, and recovery moves.

## Core Outputs

Every serious run should leave behind most of these artifacts:

1. Audience and objective statement.
2. One-sentence promise.
3. One-line slogan or governing idea.
4. Time budget.
5. Section fences with explicit transitions.
6. Evidence plan: example, story, demo, board work, or visual for each fence.
7. Opening move.
8. Closing recap.
9. Q&A prep.
10. Rehearsal risks and next iteration.

## Workflow

### 1. Frame Mission

Extract or infer:

- audience
- audience prior knowledge
- decision or learning goal
- allowed duration
- delivery mode: talk, lecture, pitch, review, defense, briefing
- artifact needed: outline, notes, slide plan, full deck copy, rehearsal memo

If the user skipped one of these, make a reasonable assumption and label it.

### 2. Lock Promise Before Slides

Before editing slides, force the talk into two lines:

- `Promise`: what the audience will know, believe, or do by the end
- `Slogan`: the compact phrase that keeps the talk coherent

If either line feels vague, stop refining slide text and fix the argument first.

### 3. Build Fences

Break the talk into `3-5` sections with explicit names. These are the fences. Each fence must answer one question only.

Default fence count:

- `5-10` minutes: `3` fences
- `10-25` minutes: `3-4` fences
- `25+` minutes: `4-5` fences

For each fence, define:

- rough time allocation
- why it exists
- the one thing the audience must remember
- the evidence artifact
- the board, demo, or visual move
- the transition into the next fence

Avoid decks that wander through a long list of equal-weight bullets.

### 4. Design Opening And Close

Opening must do real work fast:

- establish relevance
- orient the audience
- state the promise
- create curiosity or urgency

Closing must:

- restate the promise
- compress the argument
- end on a decision, implication, or memorable line

Do not end with a weak "questions?" slide after the actual ending. End strongly, then open Q&A.

### 5. Prefer Concrete Evidence

Every important claim should be backed by one of:

- example
- comparison
- short story
- demo
- board sketch
- visual model
- numerical contrast

If a section contains only abstract bullets, rewrite it.

### 6. Use Verbal Punctuation

Make transitions explicit. Good talks tell the audience where they are.

Add phrases such as:

- "First, what problem matters here?"
- "Now that setup done, move to mechanism."
- "Hold that thought; one counterexample first."
- "Three implications follow."

Do not rely on slide titles alone to carry structure.

### 7. Fit The Artifact To The Host

For any host:

- strategy first
- outline second
- slides third

If the host has slide tooling, use it only after the structure passes audit. If not, return:

- a markdown outline
- speaker notes
- slide-by-slide intent
- optional rehearsal memo

See `references/agent-compatibility.md` when choosing the delivery format.
Use `assets/slide-plan-template.md` when the user wants deck-ready structure.

### 8. Audit Before Final Delivery

Use:

`scripts/audit_outline.py`

when the user provides notes, an outline, or draft speaker copy. The script scores the outline against the rubric and identifies missing promise, weak fences, absent timing, weak close, low concreteness, and fence-level structural gaps.

### 9. Rehearse Against Risk

End with a short rehearsal plan:

- what to trim first if time slips
- what line opens strongest
- where energy drops
- which slide needs a better visual
- likely questions

## Resources

- `references/framework.md`
  Read for the distilled framework and talk architecture rules.
- `references/rubric.md`
  Read for the scoring model and review language.
- `references/agent-compatibility.md`
  Read when packaging output for Codex, Claude, or tool-light environments.
- `assets/presentation-brief-template.md`
  Use when the user wants a structured planning artifact.
- `assets/slide-plan-template.md`
  Use when the user needs a slide-by-slide handoff after the storyline is stable.
- `assets/rehearsal-checklist.md`
  Use at the end of drafting or before a dry run.
- `scripts/audit_outline.py`
  Run for deterministic review of markdown outlines.
- `scripts/sync_mirror.py`
  Run to check or repair drift between the Chef bundle and the standalone repo copy.

## Output Shape

When returning a plan or rewrite, default to this order:

1. `Audience`
2. `Promise`
3. `Slogan`
4. `Time Budget`
5. `Fences`
6. `Opening`
7. `Evidence Plan`
8. `Closing`
9. `Q&A Risks`
10. `Next Rehearsal Pass`

Stay concise. High-stakes presentations need hard structure, not ornament.
