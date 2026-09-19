---
name: stelow-product-health
description: Product health monitoring through signals in tension. Monitor both effectiveness and user well-being by observing tension between success signals and counterbalance signals, focusing on removing unwanted side effects.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Product Health: Signals in Tension

## The Problem of Single Signal Optimization

In a world that pushes for incessant number optimization, it's easy to fall into the trap of pursuing signals in isolation — focusing on what grows fastest or looks most impressive (like number of new users or frequency of use).

This practice carries silent risks: the **"cobra effect"** — when trying to solve a problem with one signal, we end up generating unexpected negative consequences in other areas. Optimizing a single signal can lead to a product that "works", but generates unwanted human costs: addiction, anxiety, loss of time, or superficial use that doesn't deliver real value.

## The Proposal: Sets of Signals in Tension

Instead of seeking the absolute signal, monitor the **"pulse of the system"** through **sets of signals in tension**. The intention is to monitor both the effectiveness of the solution and the user's well-being, focusing on removing unwanted side effects instead of just adding more growth numbers.

For each set, there is a **success signal** and one or more **counterbalance signals**. By observing the tension between them, you get a more comprehensive and balanced view.

---

## The 3 Essential Sets of Signals

### 1. Tension: Speed vs. Quality of Activation

#### Success Signal — *Did the User Experience Initial Value?*
**What to observe**: identify the most important action a new user needs to take to experience core value for the first time. Think of the **"aha! moment"** — the instant when the person perceives the purpose of the solution.

**Intuitive Examples**:
- Task organization app: "a new user who creates and completes their first task in the first 3 days"
- Meal delivery service: "a new customer who places and receives their first order in the first week"

**Justification**: this action represents the first delivery of real value — the point at which the user experiences the central purpose of the solution.

#### Counterbalance Signal — *Was Activation Superficial?*
**What to observe**: look for a signal that reveals whether activation was an isolated event, without continuity. Helps avoid the team forcing the user to an action that doesn't translate into real engagement.

**Intuitive Examples**:
- Task app: "the percentage of users who created and completed the first task, but did not return to the app in the next 7 days"
- Delivery service: "the percentage of customers who placed the first order, but did not place a second order in the following month"

**Justification**: protects against "gamifying" activation — where the user is led to a one-time action without genuine engagement.

---

### 2. Triple Tension: Habit vs. Progress vs. Well-Being

This set is the **heart of monitoring a healthy system**, seeking balance between continuous use, real user progress, and ensuring that the product doesn't generate hidden costs.

#### Success Signal — *Is the Product Becoming a Habit?*
**What to observe**: identify a key action that, when repeated, shows that the solution has integrated into the user's routine. A frequency that indicates consistent and intentional use.

**Intuitive Examples**:
- Language learning platform: "the percentage of users who complete one lesson per day for 3 consecutive weeks"
- Financial management tool: "the percentage of users who record their expenses weekly for one month"

#### Efficacy Counterbalance — *Is the Habit Not Generating Progress?*
**What to observe**: look for a signal that shows whether continuous use is, in fact, leading the user to progress in their main purpose. We want to avoid **"treadmill habit"** — there's activity, but no progress.

**Intuitive Examples**:
- Language learning platform: "the percentage of users who complete lessons regularly, but don't advance levels or don't improve on proficiency tests"
- Financial tool: "the percentage of users who record expenses, but don't decrease their spending or don't reach their savings goals"

#### Well-Being Counterbalance — *Is the Habit, Even if Effective, Harmful?*
**What to observe**: identify a signal that monitors the **"human cost" of use**. Ensures that the product doesn't become extractive or addictive, generating anxiety, loss of time, or other negative impacts.

**Intuitive Examples**:
- Language learning platform: "responses to a survey about the level of stress or frustration with learning" or "the percentage of use sessions that exceed X hours per day, indicating potentially compulsive use"
- Financial tool: "responses to a survey about perception of financial control versus anxiety" or "the number of times the user accesses the application outside business hours, indicating excessive worry"

**Justification**: ensures that the habit is healthy. Protects against creating an "extractive" or addictive product that solves a problem but generates anxiety, loss of time, or other hidden costs.

---

### 3. Tension: Depth for the Faithful vs. Accessibility for Newcomers

As a product evolves, optimization for more experienced users can, unintentionally, make life difficult for those who are arriving. This set seeks the **balance between these two needs**.

#### Satisfaction Signal — *Are We Essential to Our Base?*
**What to observe**: for users who have been engaged for longer, what signal shows how indispensable the product has become to them?

**Intuitive Examples**:
- Video editing software: "the percentage of users with more than 6 months of use who would answer 'very disappointed' if the software ceased to exist"
- Online community: "the frequency of contributions from veteran users in complex discussions"

#### Counterbalance Signal — *By Pleasing the Base, Are We Worsening the Experience for Those Arriving?*
**What to observe**: monitor the experience of new users, ensuring that the evolution of the product for the "faithful" doesn't create barriers for "newcomers".

**Intuitive Examples**:
- Video editing software: "the completion rate of the initial tutorial by new users" or "the satisfaction level (CSAT) of users with less than 30 days of use"
- Online community: "the rate of new members who make their first post or comment in their first week"

## Completeness contract

The host validates these minima — never submit fewer:

- Tension board with verdict plus the metric to watch next.
- At least 500 words and 3 headings.

## Examples

### Example: engagement is up, support tickets doubled

**Input:** "DAU grew 40% but churn didn't move. Healthy?"

**Steps:**
1. Name the success signal (DAU) and hunt its tension pair (support load, session quality).
2. Build the 3-set board: growth, quality, sustainability.
3. Call it: growth without quality is not health.

**Output:** Tension board with verdict + the metric to watch next.

## Edge Cases

### Only one signal exists
- Say the product is unmeasurable on health; propose the missing pair before judging.
### Signals agree (all green)
- Distrust briefly: check for vanity definitions and lagging indicators.
### Tension is irreconcilable
- Escalate to strategy (positioning), not to more metrics.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : audit
description    : Final audit. Verify all requirements met.
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : (terminal)
gate           : none
rework-on      : execution
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **audit** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Final audit. Verify all requirements met.

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.

