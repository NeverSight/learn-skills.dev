---
name: pm-roadmap
description: Create or critique a product roadmap — outcome-oriented, theme-based, confidence-aware (Now-Next-Later) roadmaps tied to strategy, instead of dated feature lists. Gates format and detail by audience and planning horizon. Trigger when the user asks to build, write, review, or restructure a product roadmap, quarterly/annual plan, Now-Next-Later view, or roadmap presentation.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Product Roadmap Skill

## How this skill behaves (read first)

This is a **generative** skill. The default failure mode is the **dated feature list**: features pinned to months, presented as commitments, mistaken for a backlog, stale within a quarter — manufacturing an illusion of certainty that converts every market shift into a broken promise. A roadmap is a *strategic communication tool*: it answers why and what-outcome, in sequence, at the right confidence level. This skill gates:

1. **Establish strategy, audience, and horizon** — these decide format, detail, and date precision.
2. **Apply the always-true core** — outcomes over outputs, themes over features, strategy linkage, honest uncertainty.
3. **Surface the format and process decisions** (Now-Next-Later vs. timeline, quarterly vs. annual, audience views) with trade-offs.

Then it **hands off to `pm-prioritization-rigor-audit` and `pm-okr-metric-validity-audit`** for validation.

---

## Step 0 — Establish context before drafting

Ask if not known; state the assumption if proceeding without an answer:

- **Is there a strategy and are there OKRs?** A roadmap *translates* strategy into sequenced initiatives. No strategy → stop; help articulate goals first (a roadmap built without one is a wishlist). Existing key results become the spine: work backward from each KR to the initiatives believed to move it.
- **Audience** — internal teams (detail, dependencies, risks), executives (themes, milestones, strategic linkage), or customers (value and direction, no dates, no internals)? Each gets a *different view of the same truth* — never one document for all.
- **Horizon and cadence** — annual (budgeting, directional bets) vs. quarterly (execution detail)? What triggers replanning besides the calendar?
- **Delivery context** — fixed-date commitments (compliance, contracts) legitimately need timeline treatment; discovery-driven products need confidence-based structure.

---

## The always-apply core (correct for almost every case)

### Outcomes, not outputs

- **Each roadmap item names the problem/outcome, not just the deliverable.** Outputs (features shipped) measure activity; outcomes (behavior or business change) measure value.
  - ❌ "Q2: AI assistant, dark mode, new dashboard" ✅ "Now: cut onboarding drop-off at step 3 (drives activation KR) — candidate bets listed under it"
- **Translate business outcomes into product outcomes:** "reduce churn" is too broad to act on; "increase week-1 feature adoption among new accounts" is a product outcome a team can own.

### Themes and initiatives, not feature catalogues

- **Theme** = problem space tied to strategy ("onboarding," "localization"); **initiative** = significant effort within a theme; features live *underneath* as current bets. This keeps direction stable while solutions stay swappable.
- **Every theme visibly traces to a strategic goal** — an initiative that can't name its strategy link is a pet project in costume (the audit will flag it).

### Honest uncertainty

- **Confidence is part of the content.** Near-term work is committed; far-out items are bets. Mark the difference explicitly — stakeholders treat everything undifferentiated as a promise.
- **No false-precision dates.** Internally, sequencing and dependency timing; externally, direction without delivery dates.

### A living document with a communication job

- **The roadmap is a shared tool, not a file** — and it decays: schedule reviews (quarterly planning + event triggers: major discovery findings, competitor moves, strategy shifts) and feed **continuous discovery** into priorities (weekly user insights; dual-track discovery/delivery).
- **Roadmap ≠ backlog.** Strategic direction lives in the roadmap; tasks, bugs, and tickets live in the backlog. If items have story points, they're in the wrong document.
- **Presentation is part of the deliverable:** short, focused, visual (themes/colors/milestones), with a narrative thread — present challenges → outcomes → future vision. Answer "why is X delayed/excluded" with strategy, not apology.

---

## The context-dependent decisions (surface, don't auto-apply)

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Now-Next-Later** | Uncertain timing, sequence matters; discovery-driven teams | Contractual/compliance dates exist | The default modern format — confidence-organized |
| **Theme-based view** | Communicating direction to executives/customers | Teams needing execution sequencing beneath it | Themes on top, initiatives within, features as bets |
| **Timeline/Gantt view** | Hard dependencies, cross-team handoffs, fixed dates | As the public face (reads as a promise) | Internal execution layer only |
| **Annual vs. quarterly** | Annual: budget, hiring, directional bets. Quarterly: execution detail | One artifact for both jobs | Both, linked: annual themes → quarterly initiatives |
| **Audience views** | Internal-detailed / executive-thematic / customer-value | Showing customers internals, or execs ticket-level detail | Three views of one source of truth |
| **Data-driven sizing** | Opportunity sizing, impact estimates, historical timelines, success thresholds where analytics exist | Inventing numbers where data doesn't exist (→ rigor audit) | Size with real data; mark estimates as estimates |
| **Dependency mapping** | Multi-team initiatives, shared systems, external partners | Solo-team simple scopes | Map for anything crossing team boundaries |
| **Technical-debt allocation** | A standing capacity share for debt/platform work | Letting debt compete feature-by-feature (it always loses) | Explicit recurring allocation, themed like any other work |
| **Stakeholder input process** | Structured intake from sales/support/customers with bias awareness | Loudest-voice routing into the roadmap | Input channels in, strategy filter out; involve stakeholders at goal-setting to build buy-in |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`prioritization-rigor` is the always-relevant lens for this artifact (auto-runs)** — a roadmap's integrity is its strategy-linked sequencing; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-prioritization-rigor-audit`** *(auto-runs)* — is the sequencing evidence-based, strategy-linked, and trade-off-explicit? Are scores real? Is anything on top because someone shouted?
- **`pm-okr-metric-validity-audit`** *(offer — if it targets outcomes/KRs)* — are the outcomes/KRs the roadmap targets themselves valid (falsifiable, non-vanity, guardrailed)? A roadmap aimed at bad metrics is well-organized waste.

If the audits surface a conflict (e.g., a stakeholder commitment vs. strategy fit), resolve back toward the primary task: the roadmap exists to align everyone on *why* and *what outcome* — protect its credibility over any single line item.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Features pinned to months, presented as promises | Now-Next-Later with explicit confidence levels |
| "Q3: Dashboard v2" | Theme → initiative → outcome, with the KR it serves |
| One roadmap document for everyone | Internal / executive / customer views of one truth |
| Roadmap items with story points and bug fixes | Roadmap = direction; backlog = tasks |
| Set-and-forget annual plan | Scheduled reviews + discovery-triggered replanning |
| Invent reach/impact numbers to look rigorous | Size from analytics; label estimates (→ prioritization-rigor) |
| Bury "why X isn't on it" | Explicit Won't-do/Later reasoning tied to strategy |
| Dense Gantt in the board deck | Short, visual, narrative presentation; details on request |
| Let sales-deal requests jump the queue silently | Structured intake, strategy filter, conscious exceptions |
| Ship without checking | Hand off to prioritization-rigor + okr-metric-validity |

---

## Source lessons (Uxcel)

- [Why You Need a Roadmap](https://uxcel.com/lessons/why-you-need-a-roadmap-946)
- [From Static to Dynamic](https://uxcel.com/lessons/from-static-to-dynamic-630)
- [Data-Driven Roadmapping](https://uxcel.com/lessons/data-driven-roadmapping-391)
- [Using the Product Strategy to Build Your Roadmap](https://uxcel.com/lessons/using-the-product-strategy-to-build-your-roadmap-387)
- [From Strategy to Story](https://uxcel.com/lessons/from-strategy-to-story-145)
- [Communicating and Socializing Your Roadmap](https://uxcel.com/lessons/communicating-and-socializing-your-roadmap-197)
- [Roadmap Planning & Prioritization](https://uxcel.com/lessons/roadmap-planning-prioritization-154)
