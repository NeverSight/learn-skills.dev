---
name: taiga-ui
description: >
  Any interface work in an Angular project that uses Taiga UI (`@taiga-ui/*`): it is the app's UI layer,
  so every component, template, form, dialog, notification and style goes through it. Use when building
  or changing UI, when picking which `Tui*` component fits a need, and when Taiga code won't compile,
  renders unstyled or renders inert. If the project has no `@taiga-ui/*` packages yet, that is
  `taiga-ui-setup`; schematics migration TODOs after a version bump are `taiga-ui-migration`.
---

# Building with Taiga UI

The method for building with Taiga UI: the library's shape, how to pick components, and the mistakes to
avoid. It holds **no** exhaustive API — that lives in the live source you consult per task; the depth
lives in [`references/`](references).

> The #1 failure is writing Taiga code from memory that reflects an older major or an invented API.
> Everything here exists to prevent that.
>
> **Authority order: the live source > this skill > the surrounding code.** If the live source and this
> skill disagree, the live source wins. And "it matches the rest of the repo" is not a quality bar — a
> project mid-upgrade is full of exactly the patterns this skill exists to remove, so never take a
> neighbouring file as proof that an API is current.

## Step 0 — before writing any markup

1. **Is Taiga installed and wired?** If `package.json` has no `@taiga-ui/*`, or the app has no
   `<tui-root>` / `provideTaiga()`, stop — that is setup, not development. Run the **`taiga-ui-setup`** skill
   first, then come back here.
2. **Open the live source.** Prefer the Taiga UI **MCP** — `get_overview` (import map, checklist, common
   mistakes) once, then `get_component_example` per component you use. Otherwise
   `https://taiga-ui.dev/llms-full.txt`. **Confirm the owning package for every symbol before importing —
   never guess one.** No MCP configured? Setting it up is step 5 of the **`taiga-ui-setup`** skill; until
   then use `llms-full.txt`, and [facts.md](references/facts.md) if nothing is reachable.

## Core rules

- **Pick by behaviour, then confirm the exact symbol live.** Map a need to a primitive in
  [capabilities.md](references/capabilities.md) — it also lists the habit each need tempts you into —
  then get the real selector/import from the live source.
- **Controls are directives on native elements** inside a textfield wrapper — not custom `<tui-*>` tags.
- **Configure through DI**, not ad-hoc markup: providers and injected services (dialogs, notifications).
- **Compiles ≠ works.** Some wrong choices type-check and fail only at runtime — an unprovided service is
  a blank page, an unbound control renders inert. Run the app before you claim it's done.

## Reference files — read when

| Read | When |
|---|---|
| [architecture.md](references/architecture.md) | starting anything — the library's shape and the DI-first mental model |
| [capabilities.md](references/capabilities.md) | choosing what to reach for — need → the wrong reflex → the primitive |
| [forms.md](references/forms.md) | building any form, input, validation, or submit flow |
| [overlays.md](references/overlays.md) | dialogs, confirms, notifications / toasts, dropdowns, hints |
| [styling.md](references/styling.md) | about to write CSS — the escalation ladder that usually removes the need |
| [pitfalls.md](references/pitfalls.md) | before finishing — the anti-hallucination self-review |
| [platform.md](references/platform.md) | event modifiers, custom controls, DI helpers, masking, Polymorpheus, platform tokens |
| [facts.md](references/facts.md) | offline / no MCP — concrete symbols, stale-recall table (safety net) |

## Angular fundamentals (compose, don't re-teach)

Assumes idiomatic modern Angular: standalone components, `ChangeDetectionStrategy.OnPush`, reactive
forms, signals for local state and `computed` for derived, logic in `.ts` / template in `.html` / styles
in the stylesheet, and `[class.x]` / `[style.p]` over `ngClass` / `ngStyle`. This skill does **not**
re-teach these — pair it with a general Angular skill.
