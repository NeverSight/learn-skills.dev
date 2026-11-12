---
name: design-pipeline
description: Design or redesign a UI from a rough idea — named art directions to choose from, locked into a DESIGN.md, then built and reviewed. Use for "je veux designer une app de X", "propose-moi des directions", "design me a dashboard", "refais cette page". Web, desktop, mobile. Reviewing an existing UI without designing is `web-design-guidelines`.
user-invocable: true
argument-hint: "[what you're designing — e.g. 'a dashboard for X', 'landing page', or nothing at all]"
---

# Design Pipeline

The user may arrive without a visual idea. The pipeline produces one, shows it, lets them choose, then holds the choice for the whole build.

Two constraints hold in every phase:

- **No slop**: avoid the banned defaults in `reference/directions.md`. Sameness is the failure mode.
- **No overload**: `reference/density.md`. An interface that says everything says nothing.

## Phase 1 — Brief

Ask at most six questions in one message, each with a default so the user can answer "va comme tu veux":

1. What is it and who uses it? (one sentence)
2. The one thing a user must be able to do on the main screen
3. Surface: web / desktop / mobile / native
4. Stack, if it exists (check `package.json` before asking)
5. A product whose look they'd point at ("like that")
6. Anything forbidden: brand, palette, an aesthetic they hate

On "surprise me", infer from the domain and go to Phase 2.

Done when the answers (or defaults) are in hand. A brief is not a direction: Phase 2 comes before any build.

## Phase 2 — Directions, shown not described

Three named directions, each as comps. A written description is unjudgeable by a non-designer, and the person asking usually is one.

Pick the single most important screen from the brief and render *the same screen with the same real content* three times: only identical content makes the treatments comparable. Build the comps first, then write the captions.

Route by availability:

1. **Paper** (`paper-desktop`) if running: comps on the canvas.
2. **The `design` skill**: multi-artboard canvas Artifact, one artboard per direction. Best when there is no project yet.
3. **One self-contained HTML file**, three sections, opened in the browser. The default when in doubt.

Each direction gets a caption: name and one-line thesis; a reference product **with its URL**; **what it is bad at**.

Load `reference/comps.md` to build them and `reference/directions.md` for the catalogue.

Then ask the user to pick or remix ("the type of A with the depth of C" is common). If none land, offer three more and say what changed about the search.

Done when the user has chosen or remixed a direction.

## Phase 3 — Lock

Write `DESIGN.md` at the project root, derived from the chosen direction, including anything the user said while choosing:

```markdown
# Design
Direction: <name> — <one-line thesis>
Reference: <product> — what we take from it, what we don't

## Tokens
Type: <families, scale, the 3 sizes in use>
Colour: <surface, text, one accent — with contrast ratios>
Depth: <how elevation is expressed>
Radius / spacing: <scale>

## Motion
<easing rules and duration bands — see review.md>

## Density budget
<from density.md, filled in for this surface>

## Banned here
<the specific things this project must never do>
```

Add `Always read DESIGN.md before touching UI.` to `CLAUDE.md` or `AGENTS.md`. Skills have no memory; this file is it, and without it the direction resets every session.

## Phase 4 — Build

- **Code**: build against `DESIGN.md`. Source components through `ui-sources`; `pick-ui-library` gives the canonical React library per task.
- **Canvas exploration**: Paper (`paper-desktop`) if running; iterate shapes there before committing to code.
- **Static artefact or mock**: the `design` skill's canvas.

Finish the main screen **fully** before starting a second; a half-finished set cannot be judged.

## Phase 5 — Review

Load `reference/review.md` and run its passes, then fix in one batch. Done when the passes are run and the batch is fixed.
