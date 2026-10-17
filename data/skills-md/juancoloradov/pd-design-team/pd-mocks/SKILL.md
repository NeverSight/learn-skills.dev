---
name: pd-mocks
description: >-
  Use when building mockups or screens in the project's design tool (Figma, Penpot, Pencil, Sketch, Framer, or real code
  components / an HTML prototype) from finished design, content, visual, and component specs, bound to
  the live design system. Also use right after creating a batch of frames or screens. Part of the pd-* design team.
metadata:
  team: product-design
  role: mocks
  version: "2.0.0"
---

# pd-mocks — real screens from real parts

## Overview

Assemble the upstream specs into **real screens** in whatever the project's `design_tool` is, using the
**live design system**: real components and variants, real type styles, bound tokens, and the real copy
from the content artifact. Then verify with a batch audit. Lorem ipsum and invented components make a
mock look finished while hiding the gaps that engineering will hit later.

## Before you start

- Load `pd-foundations`: `design-system.md`, `accessibility.md`, `compliance.md`, and the adapter for
  the project's tool (`tools/README.md`).
- Read `docs/design/PROJECT.md` for `design_tool` and `design_system`. If it is missing, proceed with
  defaults recorded as assumptions in your artifact, or ask `pd-design-lead`.
- Read the upstream artifacts for the fidelity you're building. **Wireframe (lo-fi) mocks** need only
  `*-design-*.md`; use neutral placeholders and label the frames lo-fi. **High-fidelity mocks** need
  `*-design-*.md`, `*-content-*.md`, `*-visual-*.md`, and `*-components-*.md`; if one is missing, route
  back through `pd-design-lead` instead of improvising its content. `*-responsive-*.md` is optional when
  breakpoints are specified.

## When to use

- A visual or clickable artifact is needed in the project's design tool or in code.
- The design spec exists (lo-fi), or design, content, visual, and component specs exist (hi-fi).

**Not for:** missing inputs (route back through `pd-design-lead`; mocks built without specs drift from
the design), or interactive/animated behavior (`pd-prototyping`).

## Process

1. **Gather inputs.** Agree the fidelity with the user, then confirm the artifacts it needs exist. If one
   is missing, stop and route back.
2. **Re-sync the live system.** It evolves, so enumerate the real components, variants, and tokens you
   will use (read recipes in the adapter). Cross-check them against the approved list in
   `*-components-*.md`: using a real-but-unapproved part is still a spec deviation, so flag it.
3. **Plan and confirm.** State which screens you will build, where (file/page, or component/story
   path), and from which parts. Get the user's OK before writing.
4. **Assemble section by section.** Per tool:
   - Design tool (Figma, Penpot, …): real component instances with real variant props, bound type styles, bound
     color/spacing variables.
   - Code: real components from the codebase or Storybook, or an HTML prototype that imports the real
     tokens (CSS variables, theme file); no hard-coded values.
   Use the real copy from `*-content-*.md`. Build incrementally.
5. **Include all states.** Default plus empty, loading, error, and partial, not just the happy path.
6. **Run the batch audit after every batch.** Audit every screen, not a sample. The recipe and
   commands live in the design tool's adapter (`tools/README.md`) or `tools/code.md` (rendered code). The intent:
   - Verify bindings, not looks. A screenshot cannot tell a bound token from a near-miss value that
     merely looks right, so inspect the actual style/variable references (or computed CSS traced back
     to tokens).
   - Instance integrity: every element meant to be a system component is a real instance/import of it,
     not a detached or hand-built lookalike.
   - Type-style binding: every text layer uses the system's type style, not a local override that
     matches size and weight.
   - Visual issues: text clipping, overflow, real icons, consistent column widths.
   Report a findings table and fix before the next batch. If a finding is still unfixable with real
   system parts after 2 attempts (for example no matching icon exists), stop, log it to
   `SYSTEM-BACKLOG.md` as a blocking gap, and note it in the artifact instead of shipping a
   fabricated substitute silently.
7. **Link and flag.** Record screen links or paths and any gaps (route to `pd-design-system-ops`).

## Output

`<artifacts_dir>/<date>-mocks-<topic>.md`: handoff header (`discipline: mocks`), then each screen (link or
path, what it shows, which state), the batch-audit results table, components/variants used, and flagged
gaps. `upstream:` design, content, visual, components (and responsive, if used). `downstream:` `prototype`,
`qa`, `handoff`.

Use realistic, de-identified sample data in shared mocks; real personal data does not belong in
frames, titles, or exports.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for mocks and apply it on top of
this skill.

## Common mistakes

- Lorem ipsum instead of the real `*-content-*.md` copy.
- Inventing components or tokens instead of using, or flagging, the real system.
- Writing to the design tool without loading its adapter (and any write-tool prerequisites) first.
- Skipping the batch audit, or deferring its fixes to a later batch.
- Building only the happy state; raw hex or pixel values instead of tokens.
- A detached or hand-built duplicate standing in for a system component: verify instance integrity,
  not visual similarity.
- Trusting a screenshot to confirm token or style binding.
