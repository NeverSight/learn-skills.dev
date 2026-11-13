---
name: ux-dashboard
description: Design or critique an analytics or data dashboard — which metrics earn a place, how to organize and prioritize them, and which chart fits each one. Trigger when designing a dashboard, building an analytics or reporting screen, choosing chart types, or reviewing a dashboard for clarity and information overload.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Dashboard Skill


## How this skill behaves (read first)

This is a **generative** skill, and dashboards have a signature **over-design** trap: cramming every available metric onto one screen. As the lessons put it — *"when everything is important, nothing is."* The default instinct is to show all the data; a good dashboard shows the *few* things that answer the user's question. So this skill gates:

1. **Establish who's looking and what decision they're making** — that determines what belongs on the screen.
2. **Apply the always-true core** — organization, hierarchy, and chart-fit principles that hold for any dashboard.
3. **Decide density, detail, and chart types deliberately** — surface the context-dependent choices instead of defaulting to "show it all."

Then **hand off to the audits** — especially `aesthetics` (clutter/hierarchy is the make-or-break here).

---

## Step 0 — Establish context before designing

- **Audience & the decision they make** — when and why they look at this, and what action the data should drive. (User research is the real answer; ask if unknown.) This is the filter for what belongs.
- **Dashboard type:**
  - **Operational** — real-time, monitoring, needs an immediate response (patient vitals, flight traffic). Comprehensive at a glance, frequent updates.
  - **Analytical** — for investigation and thoughtful decisions (a sales dashboard); not time-sensitive, supports drill-down.
- **Roles** — one audience or many? Multiple roles → customization matters.
- **Platform** — screen size shapes how many widgets fit and the responsive layout.

State assumptions if proceeding without answers.

---

## The always-apply core (true for any dashboard)

- **Start from the user's question, not the data you have.** For each widget ask: "what decision does this support?" If nothing, cut it. Let goals + user needs + data nature pick the widgets.
- **Don't overwhelm.** Relevant few over comprehensive many. Density without hierarchy is a mess.
- **Prioritize for scanning.** People scan, not read. Put the most important metric where the eye lands first; arrange by importance.
- **Group related content.** Use containers, dividers, and white space so related metrics read as a group (common-region principle); section **labels/titles** act as visual anchors — make them distinct.
- **Use white space to segment and highlight** — it improves legibility in data-dense screens and gives key numbers breathing room.
- **Keep structure consistent** — shared alignment, title sizes, and margins across containers; this also makes responsive layouts scale.
- **Keep comparison data visible together.** Don't bury things users need to compare behind tabs/pop-ups; never hide always-needed info. Use tabs only for content that isn't compared side by side.
- **Match the chart to the data** (see reference below) — the single highest-leverage correctness decision.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Operational vs. analytical framing** | Real-time monitoring needs glanceable, comprehensive layout | Analytical use wants drill-down, less time pressure | Match layout/refresh to the type from Step 0 |
| **Which metrics/widgets to show** | The metric supports a real decision | "Because we have the data" / vanity metrics | Ruthlessly cut to what answers the user's question |
| **Level of detail / drill-down** | Analytical dashboards benefit from overview → detail | Operational dashboards needing everything visible at once | Overview first, progressive drill-down; don't tab-hide comparisons |
| **Chart type per metric** | Pick by data intent (trend/compare/part-of-whole/correlation) | Decorative chart choices; pie charts for many categories | Match to data (reference below) |
| **Customization by role** | Multi-role systems (sales mgr vs. analyst) | Single, well-known audience (adds needless complexity) | Offer when roles genuinely differ |
| **Real-time updates** | Operational monitoring | Analytical review (constant refresh is noise) | Refresh cadence matched to decision speed |

---

## Chart selection & honesty (quick reference)

**Match the chart to the data intent:**

- **Bar** — compare discrete categories. **Line** — trends over time. **Area** — trend + volume over time. **Pie/Donut** — parts of a whole (few slices only). **Scatter** — correlation between two variables. **Bubble** — three dimensions. **Radar** — compare multiple variables (few). **Candlestick** — financial price ranges.

**Chart honesty & clarity (non-negotiable — these mislead or exclude users):**

- **Start axes at zero.** A truncated baseline exaggerates differences and is misleading. (Deliberately misleading viz → flag with the dark-patterns audit.)
- **No 3D chart styling** — it distorts perceived values.
- **Don't encode meaning with color alone** — pair with icons/labels/shapes (→ accessibility).
- **Horizontal labels**, readable annotations, consistent color/markers, appropriate intervals (don't crowd a year into daily ticks), standard sharp-cornered bars, focus/unfocus states for multi-line charts.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole thing through `ux-design-review`. Here, **`heuristics`, `dark-patterns`, and `microcopy` are Tier A (auto-run); `accessibility` and `aesthetics` are Tier B (offered)** — under an existing design system `aesthetics` is suppressed and `accessibility` narrows to usage. If the user invoked this skill for one specific thing, respect that scope.

- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — the dashboard make-or-break: clutter, visual hierarchy, white space, container grouping, "is one thing clearly most important?"
- **`ux-heuristics-audit`** *(Tier A)* — recognition, visibility of status (esp. operational), user control (customization), keeping comparisons visible.
- **`ux-accessibility-audit`** *(Tier B — offer; narrow under a design system)* — chart color not the sole encoding, contrast, labelled sections, keyboard access to interactive widgets.
- **`ux-dark-patterns-audit`** *(Tier A)* — misleading visualization: truncated axes, 3D distortion, cherry-picked intervals.
- **`ux-microcopy-audit`** *(Tier A)* — section titles, labels, and annotations are clear and consistent.

If aesthetics flags overload, return to the gate: cut widgets back to the ones that answer the user's question.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Show every metric you have | Show the few that support a decision |
| Equal visual weight for everything | Prioritize; most important where the eye lands first |
| Loose widgets floating on one plane | Group with containers, dividers, white space, labelled sections |
| Hide comparison data behind tabs | Keep side-by-side comparisons visible together |
| Decorative chart choice / pie with 12 slices | Match chart to data intent |
| Truncated y-axis / 3D bars | Zero baseline, flat charts — don't mislead |
| Color-only series legend | Color + icon/label/shape |
| Vertical/diagonal axis labels | Horizontal, readable labels |
| Ship without checking | Hand off to aesthetics + heuristics + accessibility |

---

## Source lessons (Uxcel)

- [How to Design Dashboards for Better Analytics](https://uxcel.com/lessons/dashboard-best-practices-876)
- [Types of Charts & When to Use Them](https://uxcel.com/lessons/charts-790)
- [Best Practices for Designing Charts](https://uxcel.com/lessons/charts-best-practices-201)
