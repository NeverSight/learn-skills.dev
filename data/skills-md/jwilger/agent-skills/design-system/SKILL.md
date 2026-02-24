---
name: design-system
description: >-
  Collaborative design system creation using Atomic Design methodology.
  Produces a specification artifact with philosophy, tokens, and component
  hierarchy. Activate when creating a design system, defining visual
  language, specifying UI tokens, or planning component architecture
  before implementation begins.
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [event-model]
  phase: decide
  standalone: true
---

# Design System

**Value:** Communication -- a documented design system creates shared
vocabulary for every visual decision. When philosophy is explicit and
tokens are named, contributors extend the system consistently without
guessing at intent.

## Purpose

Facilitates collaborative creation of a design system specification.
Produces an artifact at `docs/design-system.pen` (if Pencil MCP is
available) or `docs/design-system.html` (single-file fallback) that
documents philosophy, tokens, and the full component hierarchy from
atoms through templates.

## Practices

### Detect Artifact Format

Check whether the `mcp__pencil__get_editor_state` tool is available.

- **Present:** Use `.pen` format. Follow `references/pencil-workflow.md`.
- **Absent:** Use HTML format. Follow `references/html-artifact.md`.

Decide the format before starting any design work. Do not switch formats
mid-process.

### Follow the Seven-Phase Collaborative Process

You MUST follow `references/design-phases.md` for the full methodology.
Each phase completes before the next begins.

**Phases at a glance:**

1. **Philosophy & Constraints** -- Brand, principles, accessibility,
   responsive strategy, constraints. Every subsequent decision traces here.
2. **Design Tokens** -- Color, typography, spacing, radii, elevation,
   motion, breakpoints, opacity. Each token cites a philosophy principle.
3. **Atoms** -- Indivisible elements (buttons, inputs, labels, icons).
   Each documents states and references only tokens.
4. **Molecules** -- Functional units composed of atoms (form fields,
   search bars). Documents composition and interaction.
5. **Organisms** -- Distinct UI sections composed of molecules and atoms
   (headers, forms, data tables). Documents layout behavior.
6. **Templates** -- Page layouts arranging organisms. Defines structure,
   content slots, and breakpoint behavior.
7. **Artifact Assembly** -- Compile into the chosen format with
   philosophy as the first section.

### Facilitate, Do Not Assume

You are a facilitator, not a stenographer. Ask probing questions at each
phase. Challenge choices that conflict with stated philosophy. Use
`references/facilitation-questions.md` for question banks.

1. Do not assume visual preferences -- ask
2. Do not skip ahead when the user gives a partial answer -- probe deeper
3. If event model wireframes exist in `docs/event_model/`, use them to
   identify required components, but still confirm with the user
4. Present token proposals informed by the philosophy and ask for
   adjustments

### Enforce Philosophy Traceability

Every design decision traces back to the philosophy.

- Tokens cite which philosophy principle they serve (e.g., `P1`)
- Atoms reference which tokens they use
- Molecules document which atoms they compose
- Organisms document which molecules and atoms they compose
- Templates document which organisms they arrange

If a token cannot cite a principle, either the token is unnecessary or
the philosophy is incomplete. Resolve before proceeding.

**Do:**
- Define philosophy before any visual decisions
- Use only token references in components -- never raw values
- Complete each phase before starting the next
- Verify traceability at every level
- Refer to `references/token-categories.md` for comprehensive token guidance

**Do not:**
- Make technology decisions (CSS framework, component library) -- those
  belong in architecture-decisions
- Skip the philosophy phase or treat it as optional
- Use raw color codes, pixel values, or font names in components
- Design multiple phases simultaneously
- Proceed with gaps -- if something is undefined, ask

## Enforcement Note

This skill provides advisory guidance. The agent tracks phase state and
halts if the philosophy phase is skipped or if raw values are used
instead of token references in components. It cannot mechanically prevent
all violations but will flag traceability gaps when detected. If you
observe the agent skipping a phase or using hard-coded values, point it
out.

## Verification

After completing work guided by this skill, verify:

- [ ] Philosophy documented with named principles before any components
- [ ] Tokens defined for all visual categories (color, typography,
      spacing, radii, elevation, motion, breakpoints, opacity)
- [ ] Every token cites a philosophy principle
- [ ] Atoms reference only tokens (no raw values)
- [ ] Molecules compose only atoms from the catalog
- [ ] Organisms compose only molecules and atoms from the catalog
- [ ] Templates arrange only organisms from the catalog
- [ ] All component states documented (default, hover, focus, disabled,
      error as applicable)
- [ ] Wireframe fields mapped to components if event model exists
- [ ] Artifact exists at `docs/design-system.pen` or
      `docs/design-system.html`
- [ ] Philosophy is the first section in the artifact

If any criterion is not met, revisit the relevant phase before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **event-modeling:** Wireframes from event modeling sessions identify
  which components the design system must include. Run event-modeling
  first for best results.
- **architecture-decisions:** The design system specification informs
  technology decisions for UI implementation (CSS framework, component
  library, build tooling). Run design-system before architecture-decisions.
- **atomic-design:** The design system specification provides the token
  definitions, component catalog, and hierarchy that atomic-design
  implements in code.
- **tdd:** Token values and component specifications become testable
  contracts -- visual regression tests verify token compliance.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill event-modeling
```
