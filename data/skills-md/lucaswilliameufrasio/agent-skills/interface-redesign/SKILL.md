---
name: interface-redesign
description: >-
  Redesign every screen of an existing web, mobile, desktop, or terminal (TUI)
  application against one researched and documented design system, preserving
  behavior, data, and public contracts, and proving the result with real
  screenshots and journey verification. Use when asked to restyle, repaint,
  modernize, or overhaul an app's interface as a whole, or when a previous
  redesign was judged poor. Inventory all screens and states first, fix the
  first paint, and record what was and was not verified.
---

# Redesign a whole application interface

Make every screen of the application follow one design direction so the product
looks modern, serious, and coherent, communicates its brand and purpose, and is
more pleasant and usable than before, without losing features, data, or
contracts.

A redesign is complete only when every screen and state was changed, checked on
the real application at the sizes that matter, and the evidence is recorded.
A good-looking home page with untouched inner screens is a partial delivery.

## 1. Establish scope and authorization

Read the repository's agent instructions, README, decision log, testing policy,
and any existing design document. Confirm:

- the surfaces in scope (web, mobile, desktop, TUI) and the target sizes;
- whether behavior changes are allowed (default: no; visual and interaction
  quality only, plus fixes for defects found on the way, reported separately);
- the delivery path (branch, commit, PR, deploy) and what still needs approval.

## 2. Secure the design definition first

A redesign implements a design system; it does not invent one screen by screen.

- If an approved design document exists, read it fully and follow it.
- If none exists, or it is outdated, or the owner rejected the current look,
  run the `design-system-definition` workflow first (understand, audit,
  research, decide, record, prove on one screen) and get the concept approved.
  If that skill is not installed, follow the same order and record the result in
  the repository's documentation before touching every screen.

Do not skip the research and audit to save time; their absence is the most
common reason a redesign is rejected.

## 3. Inventory every screen and state

Build a table from the code and the running app, not from memory:

| Screen / route / command / window | Entry point | States to cover | Contracts to keep | Before evidence |

Include internal and rarely seen views: error and not-found pages, empty states,
loading and offline states, dialogs, sheets, toasts, onboarding, settings,
permission prompts, print/export views, help screens, and minimized or
background modes (for example a mini player).

Capture **before** evidence for each row at the documented sizes using the
repository's existing tooling (see [platform implementation](references/platform-implementation.md)).

List every contract the redesign must preserve:

- element IDs, test IDs, roles, and accessible names used by tests or scripts;
- required copy and strings checked by validators or tests;
- URLs, deep links, routes, commands, flags, keyboard bindings, exit codes;
- persisted keys and formats (local storage, preferences, files, databases);
- analytics events and SEO/social metadata;
- third-party embed and licensing rules.

Run the existing test suite and record the baseline, including tests that
already fail and why.

## 4. Plan in slices, foundations first

1. **Tokens and global styles:** colors, typography, spacing, shape, motion,
   focus, and reduced-motion handling, wired through the platform's styling
   mechanism.
2. **Shared components:** buttons, inputs, navigation, cards/rows, dialogs,
   toasts, badges, media controls, empty and error states. Extract duplicated
   markup into components when it reduces drift; keep their public props/IDs.
3. **Screens, highest value first:** the first screen a new user sees, then the
   core job, then secondary and internal screens.
4. **System polish:** first paint, loading and transitions, social image and
   icons, error pages.

Each slice must leave the app working and testable. Do not mix unrelated
refactors or feature work into the redesign.

## 5. Implement against the definition

- Use tokens only; no raw colors, sizes, or durations in components.
- Show real content: real titles, artwork, and data from the product's sources.
  Never fill layouts with invented items, numbers, people, or reviews; design an
  honest empty state instead.
- Design every state listed in the inventory, including disabled, read-only,
  loading, error, and long or missing content (wrapping, truncation, absent
  images).
- Keep the accent for actions and current state; let content carry color.
- Accessibility as you go: semantic roles, accessible names on icon-only
  controls, visible focus, keyboard and screen-reader operation, target sizes,
  contrast measured for every new pair, reduced motion.
- Interaction feedback within about 100 ms; progress for anything slower than
  about 400 ms.
- Engagement features follow the design document's ethical limits.
- Apply the platform-specific rules in
  [platform implementation](references/platform-implementation.md), especially
  styled first paint on the web and color-depth fallbacks in terminals.

When a test breaks, decide whether the contract changed (update the test only if
the change was authorized and is documented) or the redesign broke behavior
(fix the code). Never weaken a test to make the redesign pass.

## 6. Verify on the real application

- Build and run the full quality gate the repository defines.
- Capture **after** evidence for every inventory row at every documented size
  and compare with the before evidence. Look at each image yourself; a capture
  that was never inspected is not evidence.
- Review each screen against the design document's directives and checklist and
  the usability heuristics; fix findings and recapture. Typical findings: text
  over translucent bars, clipped titles, overlays covering controls, duplicated
  glyphs, focus rings hidden, layout shift on load, unstyled first paint.
- Drive the main user journeys end to end. If the repository has no repeatable
  verification path, create or update one with `create-verification-skill` (or
  an equivalent project-local procedure) and run it; record the result.
- Confirm persisted user data from before the redesign still loads.

## 7. Record and hand off

- Update the design document with any decision made during implementation, and
  the decision log for non-trivial changes. Keep the agent instructions pointing
  at the design document.
- Report per screen: changed, verified (with evidence location), and anything
  skipped or unverified (third-party embeds, devices not available, production
  behavior). Name known limitations and follow-ups.
- Deliver through the repository's delivery workflow; committing, pushing,
  merging, and deploying each need the authorization the repository requires.

## Guardrails

- Preserve features, data, and contracts; a visual overhaul is not permission to
  remove capabilities or change persistence formats.
- Never copy another product's identity, artwork, or layout signature.
- Internal showcase or prototype pages must be excluded from production or gated
  by environment, not indexed, clearly labeled, and must not write user data.
- Do not install new dependencies, fonts, or services without approval; prefer
  what the stack already provides.
