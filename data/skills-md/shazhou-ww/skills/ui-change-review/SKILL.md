---
name: ui-change-review
description: "Create concise before/after HTML review artifacts for proposed changes to an existing user interface. Use when a human needs to compare affected screens, workflows, states, layout, or interaction changes before implementation without requiring a complete prototype."
argument-hint: "[affected UI or review goal]"
user-invocable: true
---

# UI Change Review

Create a decision-ready visual comparison, not a replacement application. The
reviewer should understand the proposed UI change in about five minutes.

## Establish The Decision

1. Inspect the current UI in source, screenshots, or a running build. Do not
   invent or deliberately weaken the Before state.
2. Identify the smallest set of screens and states that exposes the material
   change. Omit unchanged navigation and workflows unless they provide needed
   orientation.
3. State the requested decision in one sentence. List no more than the few
   deltas that could change that decision.
4. Keep normative behavior in the owning interface specification, task, or
   contract. Label the visual comparison as illustrative and link to the
   normative source when one exists.

If the current behavior cannot be established, label the uncertainty instead
of presenting an assumption as Before.

## Build The Comparison

Create one standalone HTML file that opens without a build step. Use the
existing product's visual language when available; the artifact should explain
the change, not introduce a new design system.

- Put Before and After beside each other at wide widths and stack them in the
  same order on narrow screens.
- Use the same scenario, representative data, viewport, shell, and scale on
  both sides so the comparison is fair.
- Show only affected regions at enough fidelity to judge hierarchy, labels,
  controls, density, and state changes.
- Put the requested decision and material deltas before the comparison. Let the
  UI carry the explanation; avoid paragraphs that narrate visible details.
- Include error, empty, destructive, loading, or permission states only when
  they materially affect the decision.
- Use concise callouts tied to visible changes. Move implementation detail,
  exhaustive rationale, and validation evidence to secondary references.
- Make the first viewport useful. A reviewer should not need to read task
  history before seeing what changed and why.

Use static states by default. Add only the interaction needed to expose a
decision-relevant state, such as switching scenarios, opening a dialog, or
showing validation feedback. Do not recreate routing, persistence, backend IO,
or every production interaction.

## Preserve The Boundary

The artifact must say that it is an illustrative review aid, not production UI
or a normative behavior contract. It must not:

- silently add features outside the proposed change;
- use polished After styling to make an inaccurate Before look inferior;
- hide unresolved behavior behind a visually complete mock;
- copy secrets, private customer data, or production credentials;
- become the only record of error, privacy, authorization, or compatibility
  behavior.

## Validate What Humans Will See

Open the HTML in a browser and inspect the actual rendered result. When browser
automation is available:

1. Capture or inspect one representative desktop width and one narrow mobile
   width.
2. Confirm there is no document-level horizontal overflow, clipped text,
   incoherent overlap, or layout shift between comparable states.
3. Exercise every included interaction and verify its visible result.
4. Check keyboard order, visible focus, accessible names, dialog semantics, and
   focus restoration when the artifact includes interactive controls.
5. Confirm Before and After still use equivalent scenarios and data after
   responsive changes.

Report any check that could not be performed. Do not expand the prototype merely
to make the validation list longer.

## Present For Review

Give the reviewer only:

- the decision requested;
- the standalone HTML artifact;
- the material changes and governing reason;
- unresolved risks or choices that affect approval;
- the normative source link, when applicable.

End with an explicit approval question that names the decision, rather than a
generic request for feedback.

Keep test logs, implementation inventories, and exhaustive alternatives out of
the primary review narrative.