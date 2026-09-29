---
name: decision-ui
description: Design, audit, or reframe data-heavy dashboards, admin tools, operations consoles, analytics products, and enterprise interfaces as decision interfaces rather than metric collections. Use when a user asks to build or improve a dashboard, KPI page, BI view, analytics UI, operational console, monitoring interface, data visualization, or other screen where a person must prioritize, diagnose, compare, decide, or act.
license: MIT
metadata:
  author: chirpyworks
  version: "0.1.0-rc.3"
---

# Decision UI

Build interfaces that reduce decision effort.

Do not begin from components. Do not begin from charts. Do not begin from a dashboard template.

Begin from the decision.

## 1. Establish the decision contract

Before proposing UI, identify:

- **Actor** — who is using the view?
- **Decision** — what choice, prioritization, diagnosis or intervention must they make?
- **Time horizon** — minutes, hours, days, weeks, quarters?
- **Consequence** — what is at risk if they act late or incorrectly?
- **Evidence** — which observations can change the decision?
- **Action** — what can the actor actually do from or after this view?

Write one sentence:

> The user opens this view because they need to decide **[decision]** before **[time/consequence]**.

If this cannot be stated, ask for missing business context or explicitly mark assumptions.

## 2. Build the information hierarchy

Prefer this sequence:

1. **Attention** — what requires attention now?
2. **Comparison** — compared with what?
3. **Cause** — why is it happening?
4. **Impact** — what is exposed or at risk?
5. **Action** — what can be done?
6. **Verification** — what happened after action?

Do not force all six into a single page. Use them as a reasoning sequence.

For multi-step operational or diagnostic products, load `references/decision-flow.md` before finalizing the information architecture.

"Cause" is a diagnostic question, not permission to state causality. Distinguish observed association, diagnostic evidence, working hypothesis and validated cause.

The primary visual mass belongs to the question with the highest decision value, not automatically to the largest number.

## 3. Treat metrics as evidence

A KPI is not important because it is a KPI.

For every metric ask:
- Which decision can this change?
- What is the comparison basis?
- What threshold or range changes interpretation?
- Is freshness known?
- Is uncertainty material?
- Does the number require explanation, action, or neither?

Remove metrics that do not affect the current decision.

## 4. Choose visualization from the question

Load `references/chart-selection.md`.

Never choose a chart because the dashboard “needs variety.”

Charts must make the intended comparison perceptually easy. Prefer position and length over angle and area. Use tables for exact lookup. Use color to carry meaning, not decoration.

If the intended analytical question is unclear, do not invent chart diversity.

## 5. Compose before decorating

Establish hierarchy using:
- position,
- scale,
- whitespace,
- alignment,
- density,
- contrast,
- grouping,
- typography.

Use borders, cards, shadows, gradients and containers only when they clarify structure or state.

Avoid equal-weight tiles unless the underlying decisions are actually equal-weight.

A page with twelve equally loud modules has no hierarchy.

## 6. Connect insight to action

If the UI identifies a problem, show the path to the next action.

Good:
- investigate cause,
- compare affected cohorts,
- open impacted order/account/asset,
- change threshold,
- assign owner,
- approve/reject,
- acknowledge,
- simulate trade-off,
- verify recovery.

Bad:
- display anomaly,
- color it red,
- leave the user to hunt through navigation.

## 7. Design state, not only the happy screenshot

Cover relevant:
- loading,
- empty,
- stale,
- partial,
- delayed,
- disconnected,
- error,
- permission-limited,
- no-action-required,
- acknowledged,
- resolved,
- overridden states.

For operational data, freshness and trust are part of the interface.

## 8. Preserve accessibility

Load `references/accessibility.md` when implementing or auditing an interface.

Critical priority, status, comparison and action must not depend on color alone, hover alone, or a pointing device. Preserve semantic tables where tabular relationships matter. Keep a text-accessible summary of decision-critical chart meaning. Respect focus order, zoom/reflow and reduced-motion needs.

Accessibility does not require making expert interfaces artificially sparse. It requires that hierarchy and action remain perceivable and operable.

## 9. Responsive reconstruction

Do not shrink the desktop grid.

On smaller screens:
1. preserve the primary decision,
2. preserve the most important comparison,
3. collapse secondary evidence,
4. move dense tables to focused views,
5. keep critical actions reachable,
6. recompose rather than merely resize.

## 10. Run the anti-pattern pass

Load `references/anti-patterns.md`.

At minimum reject:
- KPI card walls,
- decorative chart variety,
- redundant summary layers,
- gauges without meaningful threshold logic,
- unexplained red/green semantics,
- dashboards with no visible action path,
- filters that exist because “dashboards have filters,”
- equal emphasis for unequal business consequences.

## 11. Produce a decision-first handoff

For BUILD or REFRAME, return:

1. **Decision contract**
2. **Primary hierarchy**
3. **Screen composition**
4. **Visualization choices and why**
5. **Interaction / diagnostic navigation**
6. **States and exceptions**
7. **Responsive behavior**
8. **What was deliberately removed**

For AUDIT, rank findings by structural impact:
- P0: wrong decision model / missing critical action or evidence
- P1: hierarchy, comparison or visualization obscures interpretation
- P2: interaction, state or responsive weakness
- P3: craft and visual refinement

Do not spend the review on corner radius while P0/P1 problems remain.

## House rules

If `house-style.md` exists, load it after this file.

House rules may change visual language, density, component system and implementation preferences. They may not override decision clarity, truthful visualization, accessibility, or state integrity.
