---
name: pm-decision-quality-audit
description: Run a structured quality audit on a product decision or its rationale — a build/buy/sunset/re-platform/pricing call, a decision log, a retrospective, or any "we decided X because…". Produces a severity-rated issue list with concrete fixes — catches outcome-based reasoning (resulting), deliberation mismatched to reversibility, uncalibrated confidence, confirmation/anchoring/framing/sunk-cost bias, missing pre-mortems, and undocumented reasoning. Use when reviewing a major decision or its write-up, or as a validation step after a decision is made.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Decision Quality Audit Skill

## What this skill changes vs. default behavior

By default, Claude evaluates a decision by its result — if the launch worked, the call was good — and accepts a confident rationale at face value. It rarely separates the quality of the *reasoning* from the luck of the *outcome*, checks whether the deliberation matched how reversible the decision was, names the bias quietly driving the choice, or asks whether failure modes were surfaced before commitment. This audit forces four things: every finding names the violated principle; decisions are judged on the reasoning available *at the time*, not hindsight; the bias or process gap is named explicitly with a structural countermeasure; and findings come severity-rated by decision damage and reversibility with a concrete fix.

This is an **evaluative** skill: it auto-runs whenever a significant product decision, decision log, or retrospective is being reviewed — and as a validation step after a consequential call is made.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when the `pm-product-review` orchestrator or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **an artifact-specific lens — offered (for high-stakes, hard-to-reverse decisions)**. Explicit scope always wins.

---

## The framework — what to check and what a violation looks like

### 1. Process judged on its merits, not the outcome (resulting)
"Resulting" is grading a decision by what happened next. But outcomes are shaped by forces the team didn't control (a competitor launch, a platform change, timing). The right question is: **given what was known at the time, was this the best reasoning available?** Use the process × outcome matrix — *good process + bad outcome* is bad luck (don't punish it); *bad process + good outcome* is dumb luck (the most dangerous quadrant — the team learns the shortcut works).

**Flag when:** a retro praises or blames purely on results; a lucky win is treated as proof the shortcut works; a careful decision with a bad outcome is condemned; "it worked, so it was right" with no look at the reasoning.

- ❌ "Revenue went up after the redesign, so the redesign decision was correct."
- ✅ "Revenue rose, but the redesign shipped the week a competitor went down — separate the call's reasoning from the result before banking the lesson."

### 2. Deliberation matched to reversibility (one-way vs. two-way doors)
Not every decision deserves the same weight. Ask: **if this is wrong, what does it cost to undo?** Irreversible, expensive calls (sunset a line, re-platform, public pricing commitment) warrant careful, consulted deliberation; reversible ones (a feature flag, copy change, new onboarding flow) should be made fast and rolled back if wrong. Treating reversible choices as one-way doors makes teams slow; treating one-way doors as reversible is reckless.

**Flag when:** a low-stakes, reversible choice is stuck in committee (ceremony as fake rigor); a hard-to-reverse bet is made quickly and casually, with no consultation or rollback plan; the team never asked what undoing it would cost.

- ❌ A three-week debate over a button label that ships behind a flag.
- ✅ "Re-platforming is a one-way door — broaden input and pressure-test it; the onboarding copy is reversible, so ship and measure."

### 3. Calibrated confidence and cost of delay
Every decision is a forecast, so treat it as a **probability, not a verdict** — "65% chance this lifts conversion >5%," not "this will work." Decide once you're around **70% confident**; past that, added certainty rarely justifies the delay, and every week a validated decision sits unacted has a real cost.

**Flag when:** the team waits for near-certainty on a time-sensitive, reversible call (analysis paralysis); binary "it'll work / it won't" framing with no confidence level; a high-stakes irreversible bet made at low confidence without that uncertainty being stated; confidence claims never checked against later results (no calibration).

- ❌ "We need three more weeks of research before we can decide." (on a reversible test)
- ✅ "~70% confident it helps; reversible, so we ship now and measure — the delay costs more than the residual uncertainty."

### 4. Bias surfaced and countered
Bias is the default mode of cognition under uncertainty, not a lapse — so rigor means **structural guardrails**, not "trying to be objective." Watch for **confirmation** (weighting only data that supports the chosen path), **anchoring** (over-weighting the first number/option seen), **framing** (90%-success vs. 10%-failure changing the call), **false consensus** ("I'd use it, so users will"), and **hindsight** (in retros, "we knew all along"). Countermeasures: seek disconfirming evidence, an outside reviewer, neutral framing, and real user data over self-projection.

**Flag when:** the rationale cites only supporting evidence; the decision rests on the team's own preferences as a proxy for users; the framing of the data is doing the persuading; no disconfirming view was sought; a retrospective reconstructs the past as obvious.

- ❌ "Everyone on the team would use this, and the 90% task-success test confirms it — ship."
- ✅ "We ran it past someone outside the project, looked at the 10% who failed the task, and checked real usage — not just our own preference."

### 5. Sunk cost ignored — decide on future value
Money, time, and effort already spent can't be recovered and shouldn't drive the next call. The reframe that breaks the trap: **"starting from zero today, with no prior investment, would we still choose this?"**

**Flag when:** "we've already built so much of this" keeps a weak bet alive; a roadmap item survives because stopping feels like admitting failure rather than because it's the best use of capacity; past investment appears as a reason in the rationale.

- ❌ "We've spent two quarters on it, so we should finish it."
- ✅ "Ignore the two quarters — if we were deciding today with what we now know, would we start it? If no, stop."

### 6. Pre-mortem and explicit trade-offs before commitment
High-stakes decisions need failure modes surfaced *before* acting — a **pre-mortem** ("it's a year out and this failed badly; what happened?") gives the team permission to voice risks that hierarchy and optimism otherwise suppress. And every yes is a no to something: the **rejected alternatives, the cost of the chosen path, and the reasoning** should be visible and survive "why this, why now?"

**Flag when:** a high-profile bet has only a sanitized risk register (no one named real failure modes); no alternatives were considered or recorded; the decision jumps from problem to choice with the trade-off smoothed over; "what would change our mind?" has no answer.

- ❌ "We're confident in the launch plan." (no risks named, no alternatives shown)
- ✅ "Pre-mortem surfaced three failure modes; we chose A over B because…, accepting that B's users wait a quarter; we'd revisit if X."

### 7. Reasoning documented for honest later review
A decision journal — context, options considered, criteria, **confidence level, and reasoning, recorded before the outcome is known** — is what lets the team evaluate the *process* later instead of a hindsight-reconstructed story. Pair it with a scheduled review (compare what happened to what was expected).

**Flag when:** there's no record of why a major decision was made; rationale lives only in someone's head; confidence and assumptions weren't written down, so the retro can't avoid hindsight; no plan to revisit the decision against actual results.

- ❌ A major bet with no written rationale; six months later nobody can say what was actually expected.
- ✅ "Logged: the call, alternatives, criteria, 65% confidence, and the assumptions — with a 3-month review booked."

> **Tension note:** rigor scales to stakes and reversibility — a fast, low-deliberation call on a reversible, low-cost choice is *good* decision-making, not a deficiency; don't prescribe pre-mortems and decision journals for everyday reversible calls. Flag missing rigor where the decision is expensive or hard to undo. And a strategic bet can legitimately override the cautious analysis — the requirement is that the override is explicit and reasoned, not that caution always wins.

---

## Severity rating

Rate each finding by **decision damage** — weighted by how reversible and costly the decision is:

| Severity | Meaning |
|---|---|
| **Critical** | An expensive, hard-to-reverse decision rests on broken reasoning — outcome-based logic, a bias driving the call unchecked, miscalibrated confidence, or no pre-mortem on a high-stakes bet. The team is poised to make a costly wrong turn it can't easily undo. |
| **Major** | A significant decision's reasoning can't be defended — sunk cost keeping a bet alive, no trade-offs or alternatives recorded, confidence uncalibrated, deliberation mismatched to reversibility. |
| **Minor** | Process hygiene — no decision journal entry, no scheduled review, mild framing effects on a reversible call. |
| **Cosmetic** | Wording polish on an otherwise sound rationale; don't pad the report with these. |

Overlaps — defer, don't duplicate: the **ranking discipline** of a scored backlog or roadmap order belongs to `pm-prioritization-rigor-audit` — this audit checks the *decision process and biases*, that one checks the *ranking*. Whether a **metric** used in the decision is valid belongs to `pm-okr-metric-validity-audit`; whether an **assumption** was actually tested belongs to `pm-assumption-rigor-audit`; **ethical/deceptive consequences** belong to `ux-dark-patterns-audit`.

---

## Output format

```
## Decision Quality Audit — [Decision / Log / Retro]
Context: [decision · reversibility & cost · stage (pre-decision / retro), if known]

### Critical
- [Issue] — what's wrong → fix. (Principle)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest decision-damage fixes, each with the specific question the team must answer.
```

Always end with the prioritized top issues — a flat list helps no one act.

---

## How to run a good audit

1. **Establish context first** — what's the decision, how reversible is it, how costly to undo, and are you reviewing it *before* commitment or in a retrospective? Reversibility and stakes set the rigor bar.
2. **Separate process from outcome** — especially in retros; judge the reasoning available at the time, not what you now know.
3. **Only flag real costs** — a quick call on a reversible, low-stakes choice is healthy; don't prescribe ceremony for two-way doors.
4. **Name the bias and the countermeasure** — "confirmation bias — seek disconfirming data / an outside reviewer," not "be more objective."
5. **Be specific in fixes** — propose the pre-mortem, the missing alternative, the confidence level to state, the decision-journal entry. Never just "improve the decision."
6. **Prioritize, don't enumerate** — the three findings that would change a costly call beat ten hygiene notes.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Judge the decision by how it turned out | Judge the reasoning given what was known; separate process from outcome luck |
| Treat a lucky win as proof the approach works | Flag bad-process/good-outcome as the most dangerous quadrant |
| Apply the same deliberation to every call | Match rigor to reversibility — fast on two-way doors, careful on one-way |
| Accept "this will work" | Require a calibrated confidence level; decide ~70%, weigh cost of delay |
| Accept a rationale built only on supporting data | Name the bias (confirmation, anchoring, framing, false consensus); require disconfirming input |
| Let "we've invested so much" justify continuing | Reframe: starting from zero today, would we choose this? |
| Approve a high-stakes bet with a tidy risk register | Run a pre-mortem; surface real failure modes and rejected alternatives |
| Leave the reasoning undocumented | Decision journal — options, criteria, confidence, rationale, recorded before the outcome |
| Re-audit the backlog ranking or metric validity | Defer to `pm-prioritization-rigor-audit` / `okr-metric-validity` |
| Deliver an unranked issue dump | Severity by decision damage + top-3 with the questions to answer |

---

## Source lessons (Uxcel)

- [Decision Quality & Cognitive Bias](https://uxcel.com/lessons/decision-quality-cognitive-bias-476)
- [Decision-Making and Trade-Offs](https://uxcel.com/lessons/decision-making-and-trade-offs-408)
- [Mental Models for Decision Making](https://uxcel.com/lessons/mental-models-for-decision-making-582)
- [Cognitive Biases](https://uxcel.com/lessons/cognitive-biases-988)
