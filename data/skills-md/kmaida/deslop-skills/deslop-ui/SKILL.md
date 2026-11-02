---
name: deslop-ui
description: Context-aware catalog of the visual "tells" that make a UI read as AI-generated,
  with fixes. Use when the user says "deslop" about any interface, or when generating, styling,
  or reviewing any web or app interface (landing pages, dashboards, components, artifacts) to
  avoid generic AI design clichés such as gradient text headlines, announcement badge pills,
  purple gradients, blurred background blobs, accent bars, pulsing status dots, all-caps
  microtext, nested containers, glowing orbs, sparkles icons, unmodified component-library
  defaults, templated landing-page sections, and reflexive scroll animations, and to audit
  existing UI for them. Works standalone; also complements broader design-direction skills
  when installed. Flags reflexive decoration, not meaningful affordances.
---

# UI Slop Review

A focused catalog of the specific visual "tells" that make an interface read instantly as
AI-generated, plus how to fix them. Use it both when **generating** UI and when **reviewing**
UI (code or screenshots).

## Core principle: intentionality, not prohibition

**The slop is never the element. It is the reflexive, meaningless use of the element.**

The single test for anything on screen is: **"Does this convey real information or serve the
context here?"**

- If yes, it is craft. Keep it. A nav icon that encodes a real category, a chevron that
  signals "expandable," a status pill that maps to a distinct state, a relative-time feed in
  an activity log, a dark-mode toggle: all good.
- If it is there because it "looks like a dashboard" or "looks technical," it is slop. Cut it
  or replace it with something that earns its place.

Do not strip meaningful affordances in the name of avoiding tells. Over-correction (a flat
banned-list applied blindly) is its own failure mode. The catalog reflects this: Tier 1 items
are almost always reflex; Tier 2 items are good when meaningful and slop only when decorative.

When generating, your own house style is the highest-risk slop source. Counter your defaults
by making context-driven decisions, not by imitating a different generator's defaults; slop
points both loud (gradient maximalism) and quiet (unmade decisions). The catalog covers both
directions.

## Working with other design skills (all optional)

This skill stands alone; no other skill is required.

If a broader design-direction skill is installed (for example `frontend-design`), it owns
aesthetic direction: font choice, palette strategy, layout philosophy. Where its guidance
overlaps a tell in this catalog (purple gradients, nested cards, centered heroes,
glassmorphism, bento sameness), follow the design-direction skill's fuller treatment and use
this catalog as the review checklist. Invoke both on UI work when both exist.

If targeted refinement skills are installed, route to them by intent after building or
reviewing. Skip this table when none are present. These are not all run together; some are
mutually exclusive (`bolder` vs `quieter`). Suggest the most relevant one and let the user
confirm.

| Intent / cue | Skill(s) |
|---|---|
| About to ship / production-readiness | `audit`, `harden`, `polish` |
| "Make it pop" / more striking | `bolder`, `colorize`, `delight` |
| "Too loud" / too much | `quieter`, `distill` |
| Conform to the design system | `normalize` |
| Consolidate reusable components/tokens | `extract` |
| Copy / microcopy unclear | `clarify` |
| Responsive / cross-device | `adapt` |
| Add motion | `animate` |
| Empty / first-run states | `onboard` |
| Performance | `optimize` |
| Evaluate UX quality | `critique` |

## The catalog and review checklist

The full Tier 1 / Tier 2 catalog, copy tells, and the review checklist live in
[reference/tells.md](reference/tells.md). Consult it whenever generating or reviewing UI.

Note: keep all output em-dash-free. The em dash used as clause punctuation is itself the most
recognizable AI writing tell.
