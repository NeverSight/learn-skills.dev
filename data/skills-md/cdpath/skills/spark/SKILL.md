---
name: spark
description: Collaborative brainstorming that walks a raw idea to a committed spec, then stops. Guides context-gathering (one question per turn), multiple approaches with trade-offs, section-by-section approval, and a hard gate that blocks all coding until the user greenlights the design. Use when the user wants to think through a design before implementation or produce a spec document.
---

# Spark

Spark is an isolated ideation module: it takes a fuzzy idea and walks it to a written, approved spec, then stops. It does **not** auto-chain into implementation or any other skill. Forked from Jesse Vincent's open-source "brainstorming" (superpowers) skill; this fork halts after the spec lands.

## Hard gate

A `<HARD-GATE>` sits between design and code. Until the user explicitly approves the design, do not write code, scaffold files, or invoke another skill. "Simple project" is not a reason to skip design — that is the anti-pattern this skill rejects.

## Setup

- Set `skill_dir` to the "Base directory for this skill" path shown when the skill loads.
- Completion criterion: you know `skill_dir` and the topic.

## Workflow

1. **Explore context.** Ask about the problem, constraints, audience, and what success looks like. Ask **one question per turn**; let the user answer before asking the next. Do not stack questions.
2. **Propose approaches.** Put forward two or more candidate approaches, each with explicit trade-offs (cost, complexity, risk, fit). Reach for the Visual Companion (see [`references/visual-companion.md`](references/visual-companion.md)) when a layout, diagram, or side-by-side comparison would make the trade-offs clearer; otherwise stay in text.
3. **Present the design section by section.** Walk through scope, architecture, data model, API, UX, edge cases, and open questions one piece at a time. Get a yes/no on each before moving on.
4. **Review the spec.** Once a draft exists, run the spec review in [`references/spec-review.md`](references/spec-review.md). Fix anything material before declaring done.
5. **Save and stop.** Write the approved spec to `docs/spark/YYYY-MM-DD-<topic>-design.md`, report the file path to the user, and **STOP**. Do not continue to implementation planning or invoke further skills.

## Principles

- **YAGNI, ruthlessly.** Cut anything the spec does not need yet. Scope creep is the most common failure mode.
- **Incremental validation.** Confirm each decision before building the next one on top of it.
- **One question per turn.** Stacked questions get shallow answers.
- **Calibrate polish to the decision.** A mockup only needs to be as real as the choice it is informing.

## Files

- [`references/spec-review.md`](references/spec-review.md) — the five-dimension spec review run before sign-off.
- [`references/visual-companion.md`](references/visual-companion.md) — the local web tool for mockups, diagrams, and side-by-side options.
- `scripts/` — the Visual Companion server (`start-server.sh`, `stop-server.sh`, `server.cjs`, `frame-template.html`, `helper.js`).
