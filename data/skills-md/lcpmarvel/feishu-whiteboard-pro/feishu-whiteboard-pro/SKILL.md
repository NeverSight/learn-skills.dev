---
name: feishu-whiteboard-pro
version: 1.1.0
description: >
  Builds, revises, restyles, and critiques deliberate, editable Feishu / Lark whiteboards from
  content, references, existing SVGs, or live boards. Use for whiteboards, infographics, diagrams,
  system maps, timelines, decision boards, posters, and visual explainers that need factual fidelity,
  strong hierarchy, intentional composition, and evidence-based review rather than a generic grid of
  equal cards. Routes creation, revision, and critique through separate playbooks; commits to a
  content-and-design contract before drawing; validates deterministic SVG defects; renders and
  inspects the actual artifact; and uses an independent final reviewer for material deliveries.
license: MIT. Palette templates and the medium rules are adapted from beautiful-feishu-whiteboard (MIT, © Zara Zhang @zarazhangrui); the composition, critique, fit-check, and gated-pipeline layers are original additions. Design-judgment approach inspired by the impeccable / frontend-design skills (no code copied).
---

# Feishu Whiteboard Pro

Create real, editable Feishu SVG whiteboards with deliberate composition and verifiable content.
The medium is intentionally narrow: one font, native rectangles/circles/connectors, no gradients,
filters, opacity, or motion. Quality comes from truth, hierarchy, topology, rhythm, contrast, and air.

## Core contract

- **The brief wins.** Honor supplied brand, palette, reference, density, and style commitments. A
  default or anti-pattern warning cannot silently redirect a clear request.
- **Revision preserves; redesign replaces.** A repair keeps content, relationships, geometry, and
  visual identity unless the user names an axis to change. A restyle changes the visual system, not
  the information architecture.
- **Visual authority is evidence.** An existing board, SVG, screenshot, or explicit brief remains
  authoritative even without a separate design document.
- **Relationships are claims.** Never invent an arrow, number, quotation, category, owner, status, or
  causal link to make the layout feel complete. Clearly label authored demonstration content.
- **Mechanical checks and design judgment stay separate.** Scripts own measurable defects; the
  reviewer owns truth, reading path, hierarchy, balance, density, contrast in context, and alignment.
- **Verification is bounded.** Inspect once, batch fixes, confirm once. Clear remaining deterministic
  failures, but do not reopen an unlimited taste loop.

## Setup

Resolve `<skill-dir>` to the directory containing this `SKILL.md`; keep the working directory at the
user's project. All bundled references and scripts resolve from `<skill-dir>`.

Run `bash <skill-dir>/scripts/preflight.sh` once before local rendering. Node 20+ is required. The
whiteboard CLI runs through `npx` and may need network access on first use.

Feishu authentication is required only for publishing. Before writing a live board, run
`bash <skill-dir>/scripts/preflight.sh --publish`. If publishing is unavailable, continue with the
local SVG and tight PNG; do not discard a valid local deliverable.

## Route the request

Read [`RULES.md`](RULES.md) for every build or edit, then load exactly one workflow:

| Request | Workflow | Default authority |
|---|---|---|
| New board or replacement composition | [`references/create.md`](references/create.md) | User content, references, and the new board contract |
| Repair, restructure, restyle, or simplify an existing board | [`references/revise.md`](references/revise.md) | Existing artifact plus the explicitly changed axes |
| Review, diagnose, or approve a board | [`references/critique.md`](references/critique.md) | Current evidence; read-only unless fixes were requested |

Load supporting references only when the selected workflow needs them:

- [`COMPOSITION.md`](COMPOSITION.md) for new structure or restructuring;
- [`CATALOG.md`](CATALOG.md) and one `templates/<slug>/design.md` for palette selection or restyling;
- [`CRITIQUE.md`](CRITIQUE.md) for design review and final delivery;
- [`templates/GENERATE.md`](templates/GENERATE.md) only when no curated palette serves the brief.

If a request is ambiguous between creating and revising, inspect the supplied artifact first. Ask a
question only when choosing the wrong authority would materially change the result.

## Build and verify

For SVG work:

1. Start from the matching `examples/*.svg` when its topology fits. Replace content and recheck old
   arrowheads and meta text rather than trusting the example blindly.
2. Run the deterministic check:

   ```bash
   node <skill-dir>/scripts/fit-check.mjs <dir>/diagram.svg
   ```

3. Render and inspect the tight local image:

   ```bash
   npx -y @larksuite/whiteboard-cli@^0.2.11 \
     -i <dir>/diagram.svg -o <dir>/diagram.png -f svg
   ```

4. Batch visible fixes, rerun fit-check, and make one confirmation render. Use
   `node <skill-dir>/scripts/fit-check.mjs --json <dir>/diagram.svg` when passing evidence to another
   process.
5. For a material delivery, use the fresh read-only reviewer in
   [`agents/whiteboard-finish-reviewer.md`](agents/whiteboard-finish-reviewer.md). Pass the original
   request, fact/design contract, SVG, local PNG, checker output, and any real Feishu evidence.

## Publish and deliver

Follow [`RULES.md`](RULES.md) for exact Feishu creation, update, and query commands. Publishing changes
external state, so do it only when the user requested a live board or supplied a target to update.

Deliver the Feishu document link when publishing succeeded, plus the local `diagram.svg` and tight
`diagram.png`. The square Feishu export is verification evidence, not the share image. If publishing
is unavailable, deliver the local artifacts and the precise authentication step still required.

## Repository files

- [`RULES.md`](RULES.md) — verified medium constraints and publish commands.
- [`references/`](references/) — create, revise, and critique playbooks; load one per request.
- [`COMPOSITION.md`](COMPOSITION.md) — spacing, type scale, archetypes, and anti-reflex guidance.
- [`CRITIQUE.md`](CRITIQUE.md) — truth gate, five visual axes, and bounded review flow.
- [`CATALOG.md`](CATALOG.md) — generated palette index.
- [`templates/`](templates/) — curated palettes and the optional generation recipe.
- [`examples/`](examples/) — editable gold-standard SVG starting points and renders.
- [`scripts/fit-check.mjs`](scripts/fit-check.mjs) — deterministic medium and untransformed-geometry checker with text and JSON output.
- [`scripts/check-repo.mjs`](scripts/check-repo.mjs) — offline repository regression check.
- [`scripts/preflight.sh`](scripts/preflight.sh) — local and publish readiness check.
