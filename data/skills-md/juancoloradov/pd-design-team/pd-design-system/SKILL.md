---
name: pd-design-system
description: >-
  Use when translating a design into concrete design-system parts: choosing the exact type styles,
  color/spacing tokens, and component variants from the project's live system (Figma, Penpot, Pencil,
  code-based, or other) and verifying every name binds to something real. Consumes the system; to grow or change it,
  use pd-design-system-ops.
metadata:
  team: product-design
  role: design-system-consumer
  version: "2.0.0"
---

# pd-design-system — apply the live system

## Overview

This is the bridge from design intent to real system parts. Every element resolves to a token or component
variant that exists in the live system, by exact name: no approximations, no invented names, because
anything off-system becomes drift once built. This skill consumes the system and never changes it. Missing
parts are flagged for `pd-design-system-ops`.

## Before you start

- Load `pd-foundations`: `design-system.md`, and the adapter for the declared tool (`tools/README.md`).
- Read `docs/design/PROJECT.md`: `design_system` (where the live system is), `conventions` (its naming),
  and `design_tool`. If missing, proceed with defaults recorded as assumptions, or ask `pd-design-lead`.
  Backlog and artifact paths below are relative to `artifacts_dir`.
- Read the upstream `*-design-*.md` and `*-visual-*.md` (both required; if absent, route back through
  `pd-design-lead`).

## When to use

- Turning a design or visual spec into a concrete list of components, variants, and tokens.
- Before `pd-mocks`, so the build uses the right parts.
- Verifying that a design only uses real, current system parts.

## Process

1. **Re-sync the live system.** Enumerate current components, variants, and tokens from the source named in
   `PROJECT.md` (the adapter has the read recipes and fallbacks). Trust the live source over any earlier
   list. If a read fails or times out, use the adapter's fallback and state in the artifact that the roster
   was only partially synced.
2. **If `design_system.source` is `none`,** a provisional system should already exist, established by
   `pd-design-system-ops` before visual work (`design-system.md`). Map against it, and mark every
   status `provisional`. If none exists yet, stop and route to `pd-design-lead` so it is created first;
   don't invent a mapping here, and never present provisional names as real.
3. **Map every element** to a real component plus its variant properties and real type and color/spacing
   tokens. Illustration, using example names (the project's real ones come from its system): "a primary
   medium button" becomes `Button kind=primary, size=md, state=default`, with type style
   `role/label/default`.
4. **Cover all states** each component needs: default, hover, pressed, focused, disabled, loading, error
   as applicable.
5. **Handle gaps honestly.** If a part doesn't exist, append an entry to
   `<artifacts_dir>/design-system/SYSTEM-BACKLOG.md` using the fields in `templates/SYSTEM-BACKLOG.md`
   (what was needed, where, why existing parts don't fit, substitution, severity per `compliance.md`,
   blocking yes/no). Use a substitute only when the gap is not blocking;
   otherwise stop and flag for triage.
6. **Verify.** Confirm every name exists in the live source, and that the exact property combination
   (example: `kind=danger, size=xs`) is a built variant, not just individually valid values. Confirm the
   part isn't marked deprecated: a name that exists may no longer be the one to use.

## Output

`<artifacts_dir>/<date>-components-<topic>.md` with the artifact header (`discipline: components`; see
`handoff-protocol.md`), then a mapping table:

| Design element | Component · variant | Type style | Tokens | States needed | Status |
|---|---|---|---|---|---|
| Primary CTA (example) | `Button kind=primary, size=md` | `role/label/default` | (token names) | default, hover, focused, disabled, loading | OK |

`Status` is one of: OK, substituted, gap → backlog, blocked, provisional. Add flagged gaps and
substitutions. `upstream:` design, visual. `downstream:` `mocks`, `qa`, `handoff`.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for the design system and apply it on top of
this skill.

## Common mistakes

- Approximating ("a blue button") instead of resolving the real variant.
- Trusting an earlier list instead of re-syncing.
- Inventing variant or token names instead of flagging the gap.
- Mapping only the default state.
- Resolving to a deprecated style or variant.
- Logging a gap without severity and a blocking flag, leaving `pd-design-system-ops` unable to triage it.
- Passing provisional names downstream as if they were real.
