---
name: ux-empty-states
description: Design or critique empty states — first-use screens, cleared states, no-results pages, and 404s that explain why the screen is empty and guide the next action instead of dead-ending. Trigger when the user asks to design or review an empty state, blank screen, zero-data view, first-run dashboard, no-results page, or 404 page.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Empty States Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure mode is the **dead screen**: "No tasks found." — a blank dead-end at exactly the moment a user is newest, most confused, or most blocked. Every empty state is secretly one of the product's highest-leverage screens: it's onboarding (first use), reassurance (cleared), or recovery (no results / 404). The opposite failure exists too — an "empty" screen so stuffed with text, illustration, and three CTAs that it's no longer calm. This skill gates:

1. **Establish why the screen is empty** — the cause picks the pattern.
2. **Apply the always-true core** — explain + guide, never blame, stay calm.
3. **Surface the embellishment decisions** (illustration, CTAs, humor) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish why the screen is empty

The cause picks the pattern:

- **First use** — the user hasn't created anything yet. This is onboarding's last mile: explain what lives here and make the first action effortless ("Add your first task").
- **Cleared / completed** — the user emptied it themselves (inbox zero, done list). Tone shifts to positive reinforcement: "You're all caught up!" + a low-pressure next step.
- **No results** — a search/filter came up empty. Not really "empty" — it's a recovery moment: spelling check, search tips, popular categories, recent searches (align with `ux-search`'s no-dead-ends rule).
- **Error / 404** — something's missing or broken. Explain plainly, no jargon, no blame, and route back to safety (homepage, popular content).

Also establish **platform and brand voice** — they bound illustration style and whether humor is safe.

---

## The always-apply core (correct for almost every case)

### Explain + guide — the two jobs every empty state has

- **Say *why* it's empty, specifically.** ❌ "No tasks found" ✅ "You're all caught up! Add a new task to stay productive." Clarity plus encouragement, never a bare negation.
- **Always offer a next step.** Even a basic informational empty state hints at what to do ("Your inbox is empty. Start by composing a new message"). An empty state with no path forward is a defect.
- **Action empty states pair message and CTA:** the button continues the sentence — "Your cart is empty. Start shopping now!" → [Shop now]. Secondary paths (docs, examples) can live as links in the copy.
- **Never blame the user** — especially on no-results and 404 pages. The system explains what happened and offers routes, not fault.

### CTAs that actually move users

- **Specific, action-oriented labels:** "Add your first task," "Explore features" — not "OK" or "Get started" floating contextless.
- **One primary action.** If two are warranted (template vs. custom), the recommended path is visually primary and the alternative clearly secondary — never two equal buttons.

### Calm over clutter

- **An empty screen is not a billboard.** Concise microcopy + minimal visuals; every element nudges toward the user's primary goal. First-run dashboards especially: guide, don't carpet-bomb with tips, tours, and banners at once.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Illustration** | It communicates the state (sun-behind-clouds for no weather data) and fits brand personality | Decoration that adds noise or delays comprehension; inconsistent style | Relevant, on-brand, subordinate to the message |
| **Humor / personality** | Brands where playfulness fits; low-frustration moments (cleared states) | Error/404 contexts for serious products; users mid-task and blocked | Warmth always; jokes only where frustration is low |
| **Second CTA** | A genuine alternative path (template vs. custom) | Choice paralysis on a screen meant to unblock | One primary; secondary visually subordinate |
| **Educational content (docs links, demos)** | Complex products where the first action needs context | Simple actions that need no manual | Link in copy, not a competing button |
| **Sample/demo data** | Dashboards where showing the value beats describing it | When fake data could be mistaken for real | Clearly-labeled sample content as a preview |
| **404 navigation aids** | Links to homepage + popular content; search box | A bare "page not found" | Illustration + plain explanation + ≥2 routes onward |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility` and `aesthetics` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status (why is it empty?), error recovery quality, match to user expectations per state type.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — illustration alt text, CTA contrast and target size, message readability.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — calm-vs-clutter balance, illustration consistency with the product's visual language.
- **`ux-microcopy-audit`** *(Tier A)* — this skill lives or dies on copy: explanation specificity, CTA labels, tone (encouraging, never blaming).

If the audits surface a conflict (e.g., brand wants a big illustration vs. fast comprehension), resolve back toward the primary task: the user hit this screen wanting to do something — get them doing it.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| "No data available." and nothing else | Why it's empty + what to do next, every time |
| Generic "No tasks found" | "You're all caught up! Add a new task to stay productive" |
| Empty cart with no path | "Your cart is empty. Start shopping now!" + [Shop now] |
| Blaming phrasing on no-results ("You entered a bad query") | Spelling tips, search suggestions, popular categories |
| Jargon-filled 404 | Plain words + illustration + links onward |
| Three equal CTAs on a first-run screen | One primary action; alternatives subordinate |
| Tutorial walls on an empty dashboard | Minimal copy + one clear first step (+ labeled sample data if helpful) |
| Random cute illustration everywhere | Relevant, on-brand visuals that carry meaning |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [How to Design Helpful Empty States](https://uxcel.com/lessons/empty-states-best-practices-330)
