---
name: ux-loaders-and-progress
description: Design or critique loading states and progress indicators — match the feedback type (spinner, text, determinate bar, skeleton, progress tracker) to the wait duration and task structure, and manage perceived performance. Trigger when the user asks to design or review loaders, spinners, loading states, skeleton screens, progress bars, progress trackers, steppers, or multi-step flow progress.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Loaders & Progress Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure modes: **one spinner for everything** (a full-page spinner whether the wait is 1 second or 60), **no endpoint when one exists** (indeterminate loops for measurable tasks), and **progress theater** (trackers on 2-step forms, percentages that lie). The feedback type is determined by *wait duration* and *task structure* — and a loader's real job is shaping perceived time, not decorating it. This skill gates:

1. **Establish the wait type** — how long, is it measurable, what initiated it, is it a multi-step journey?
2. **Apply the always-true core** — the duration ladder, placement, state visibility.
3. **Surface the context-dependent decisions** (skeletons, custom animation, tracker labeling, save/autosave) with trade-offs.

Then it **hands off to `ux-heuristics-audit`, `ux-accessibility-audit`, `ux-aesthetics-audit`, and `ux-microcopy-audit`** for validation.

---

## Step 0 — Establish the wait type

Four questions pick the indicator:

- **How long is the wait?** <1s → often no indicator needed; 1–5s → indeterminate (spinner/text); ~10s+ → determinate with a visible endpoint; long/variable content loads → skeleton.
- **Is progress measurable?** If the system can know completion % (upload, export), users get a determinate indicator — an endless spinner on a measurable task reads as "maybe broken."
- **What triggered it?** A user click (button) → inline feedback at the action; content loading → skeleton in the content's place; a background process → unobtrusive.
- **Is it a multi-step user journey** (form, checkout, onboarding) rather than a system wait? → progress *tracker*, not loader — different component, different rules (below).

---

## The always-apply core (correct for almost every case)

### The duration ladder (loaders)

- **1–5s: indeterminate** — spinner, or a text loader ("Saving…") with a subtle animation (pulsing dots). Never let a looped animation run past ~5s — looping with no endpoint is where frustration starts.
- **10s+: determinate** — progress bar or filling circle with a clear endpoint; add a percentage label for precision on long tasks.
- **Content loads: skeleton screens** — placeholders mimicking the coming layout (text blocks, image areas), filled sequentially top-to-bottom. They beat spinners on perceived speed because they promise structure.
- **No full-page spinners.** They give zero sense of progress and suggest malfunction. Spinners live small and inline: in a button after click, in a table row, beside the thing that's loading.

### Placement = meaning

- **Near the action** that started it (inline with the submit button), **on the content** that's loading (overlay/skeleton), or **centered** only when the entire page is genuinely loading.
- **In-button progress:** the button shows a spinner and becomes unclickable — feedback and double-submit prevention in one move.

### Progress trackers (multi-step journeys)

- **Three states, always visible:** completed (checkmark/green), current (visually distinct — the "you are here" pin), remaining (muted, activating on arrival).
- **Label the steps** — titles restore context for users who got distracted and make the journey scannable.
- **5–7 steps maximum.** A tracker doesn't shorten a form; if steps multiply, the flow needs restructuring, not a longer tracker.
- **A tracker is feedback, not decoration:** it serves visibility of system status — users should always know what they did, where they are, and what's left.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Skeleton vs. spinner for content** | Layout-known content (feeds, cards, tables) — skeletons cut perceived wait | Tiny, instant loads (skeleton flash looks broken) | Skeleton for content areas; inline spinner for actions |
| **Progress tracker at all** | ≥3 logical stages (checkout, surveys, registration) | Short forms — a tracker on 2 steps adds ceremony | Numbered/labeled steps from 3 stages up |
| **Tracker labeling: titles vs. numbers vs. %** | Titles for scannability; numbers/% for motivation on long journeys | Percentages that jump erratically (trust killer) | Titles + step count; % only when it maps honestly to effort |
| **Bar vs. numbered steps** | Bar for short journeys (overall progress feel); steps for ≥3 distinct milestones | Bars pretending precision they don't have | Steps for forms; bar for processing |
| **Carousel trackers (dots)** | Onboarding/walkthroughs with few skippable screens | Directional, non-skippable flows | Dots for walkthroughs only |
| **Vertical trackers** | Status timelines (delivery tracking, application stages) | Standard form navigation | Vertical for event/status histories |
| **Save / autosave progress** | Any journey over a couple of minutes | Relying on the tracker alone to retain users | Autosave + return-to-last-step for long flows |
| **Custom branded loaders** | Brand moments where the wait is unavoidable; determinate/indeterminate decided first | Novelty that obscures progress | Function first, personality second |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics` and `microcopy` are Tier A (auto-run); `accessibility`, `aesthetics`, and `mobile-responsiveness` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage; `mobile-responsiveness` applies only on mobile. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-heuristics-audit`** *(Tier A)* — visibility of system status is this component's entire reason to exist; also error prevention (disabled buttons during processing).
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — loading states announced to screen readers, animation respecting reduced-motion preferences, contrast of muted tracker steps.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — skeleton fidelity to real layout, animation restraint, tracker visual hierarchy.
- **`ux-microcopy-audit`** *(Tier A)* — text-loader wording, step labels, percentage/status phrasing.
- **`ux-mobile-responsiveness-audit`** *(Tier B — offer; applies only on mobile)* — when the context is mobile: tracker compression, skeleton reflow.

If the audits surface a conflict (e.g., brand animation vs. perceived speed), resolve back toward the primary task: the user is waiting — every design choice either shortens that wait perceptually or lengthens it.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Full-page spinner for everything | Inline spinners, skeletons for content, centered only for true page loads |
| Looping spinner on a 60-second upload | Determinate bar with endpoint + percentage |
| Spinner where the layout is known | Skeleton screens, filled sequentially |
| Clickable button while its action processes | In-button spinner, button disabled |
| Loader floating far from its cause | Feedback at the action or on the content |
| Progress tracker on a 2-step form | Trackers from 3 stages; short forms stay plain |
| Unlabeled tracker dots | Step titles + clear completed/current/remaining states |
| 11-step tracker as a fix for a bloated form | 5–7 steps max; restructure the flow |
| % that jumps 10→80→82→…  | Honest progress mapping, or use steps |
| Long form with no save | Autosave + return to the last step |
| Ship without checking | Hand off to heuristics + accessibility + aesthetics + microcopy |

---

## Source lessons (Uxcel)

- [How to Design Loaders to Keep Users Engaged](https://uxcel.com/lessons/basics-i-971)
- [How & When to Use Progress Trackers in UIs](https://uxcel.com/lessons/basics-559)
- [Showing Progress](https://uxcel.com/lessons/showing-progress-644)
