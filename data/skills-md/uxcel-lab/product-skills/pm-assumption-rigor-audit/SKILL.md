---
name: pm-assumption-rigor-audit
description: Run a structured rigor audit on how a team validated (or plans to validate) its assumptions — for a discovery plan, experiment, test, or any "we validated it" claim. Produces a severity-rated issue list with concrete fixes — catches testing the comfortable assumption instead of the riskiest, untestable phrasing, method fidelity mismatched to decision risk, stated intent mistaken for behavior, success criteria set after the fact, goalpost-moving, and underpowered evidence. Use when reviewing a validation/discovery approach or as the validation step after generating an assumption-test plan.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Assumption Rigor Audit Skill

## What this skill changes vs. default behavior

By default, Claude accepts validation at face value — "we ran a survey and users liked it, so it's validated" passes without challenge. It rarely asks whether the *riskiest* assumption was the one tested, whether the method was strong enough for the decision it's meant to support, whether "would you use this?" answers were mistaken for evidence, whether success was defined *before* the test, or whether the sample was big enough to mean anything. This audit forces four things: every finding names the violated principle; the *decision the test is meant to support* is the unit of judgment (rigor scales to what's at stake); evidence claims are tested for signal vs. noise; and findings come severity-rated by decision damage with a concrete fix.

This is an **evaluative** skill: it auto-runs whenever a validation plan, experiment, discovery approach, or a "we validated…" claim is being reviewed — and as the validation step after `pm-assumption-testing` produces a test plan.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when the `pm-product-review` orchestrator or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **the always-relevant PM lens — auto-runs**. Explicit scope always wins.

---

## The framework — what to check and what a violation looks like

### 1. The riskiest assumption was tested — not the comfortable one
Assumptions should be mapped on **importance × certainty**; the **high-importance / low-certainty** ones (the leap-of-faith beliefs) carry the risk and get tested first. Testing everything indiscriminately, or testing what's easy, is wasted motion.

**Flag when:** the load-bearing assumption ("users will pay for this," "this is even a problem") is never named or never tested while easy/safe ones are; "we're testing everything" with no prioritization; the idea was tested but the *beliefs the idea depends on* weren't.

- ❌ Building a food-delivery app and surveying "do you like healthy meals?" (everyone says yes) while never testing "will users pay a premium" or "will they pick curated over à la carte."
- ✅ Assumptions mapped; the highest-importance/lowest-certainty one ("users will pay 20% more for curated healthy meals") is tested first.

### 2. The assumption is phrased as a falsifiable, specific statement
A testable assumption uses the hypothesis format — **"We believe [change] for [user] will result in [outcome]; we'll know we're right when [metric] changes by [amount]"** — phrased positively (what users *will* do) and specifically, so it has a real fail condition.

**Flag when:** vague beliefs ("users will like it," "this will improve engagement") with no metric or threshold; negative phrasing ("users won't churn" — harder to test than what they *will* do); an idea ("shorten checkout") presented as if it were a testable assumption.

- ❌ "Users will find onboarding intuitive."
- ✅ "We believe streamlined onboarding for new users will raise activation; right when ≥80% complete it in under 2 minutes."

### 3. Method fidelity matched to the decision's risk (the truth curve)
Pick the **cheapest, fastest method that answers the question** — and no cheaper. Low-fidelity (surveys, interviews, paper prototypes) tests *the problem*; medium (clickable mockups, landing/painted-door, concierge/Wizard-of-Oz) tests *the solution*; high (live beta, A/B in production, full build) tests *viability and scale*. The judgment call is "enough certainty to make *this* decision," not "most rigorous possible."

**Flag when:** building production code to answer a question a prototype or painted-door test would have settled (over-investment); **or** a big, expensive, hard-to-reverse bet justified by a one-day landing-page test or a hallway survey (under-powered for the stakes); a method that structurally can't answer the question asked (a click-through test used to claim the feature satisfies the need).

- ❌ Six engineer-weeks building a feature to "see if anyone wants it."
- ✅ A painted-door test measures click-through first; code follows only once demand is real.

### 4. Behavior over stated intent
Asking "would you use this?" or "would you pay $20?" produces false positives — people want to be helpful. Trust **past behavior** over hypothetical future intent (the Mom Test: ask about their life and specific past episodes, not your idea).

**Flag when:** desirability or willingness-to-pay is "validated" purely on hypothetical interview/survey answers; the test asked users to predict their own future behavior or to design the solution; stated preference is treated as equivalent to a real action (a purchase, a click, a sign-up).

- ❌ "8 of 10 interviewees said they'd definitely use it → validated."
- ✅ "Tell me about the last time you faced this" + a painted-door click-through measuring real reach-for-it behavior.

### 5. Success criteria were defined before the test
The team must agree **what result would prove the assumption right** *before* running the test — a specific, measurable threshold.

**Flag when:** no pass/fail threshold was set in advance; "success" is described only after results are in; the metric exists but the target doesn't ("we'll see how sign-ups go").

- ❌ Run the landing page, then decide 30 sign-ups "feels like enough."
- ✅ "Success = ≥10% of visitors pre-order," agreed before launch.

### 6. Results read as evidence, not wishful thinking
Stick to the pre-set criteria; don't move the goalposts. Respect the data basics — **sample size** (n=10 finds usability bugs but says nothing about conversion/preference across an audience), **duration** (a one-day test catches atypical traffic), and **statistical significance** for comparisons. Distinguish a **pattern** (repeated across sources) from an **anecdote** (the single loudest voice), and **cross-check qualitative against quantitative** — agreement is a green light, conflict is a signal to run another test, not to pick the convenient one.

**Flag when:** "60% vs. our 70% target — close enough"; conversion/preference claims from a handful of users; a one-day or tiny-window result generalized; a single loud customer/exec request driving the call; quant says one thing, qual another, and the team proceeds anyway; confirmation-biased reading of ambiguous data.

- ❌ "Only 55% completed it but the feedback was positive, so we'll ship."
- ✅ "55% missed the 70% bar → we revise and re-test; we don't reinterpret the bar."

### 7. Disconfirming results actually change the plan
Testing is a learning opportunity, and **invalidation is valuable** — it saves a wrong build. A disproven assumption must change a decision (revise, pivot, or drop), and the result is documented (assumption, method, criteria, finding, next step). A test run only to rubber-stamp a decision already made isn't a test.

**Flag when:** an assumption was disproven but nothing changed; the test was theater for a foregone conclusion; results aren't documented, so the team can't learn or revisit; validation is scheduled *after* the build as a checkbox rather than early, when it could still change direction.

- ❌ Usability test fails, ship the original design unchanged "because we're committed."
- ✅ Failure triggers a documented revision and a re-test before commitment.

> **Tension note:** rigor scales to risk — a small, cheap, reversible decision doesn't need a statistically significant experiment, and demanding one is its own failure. Don't flag a fast low-fi test that's *appropriate* for a low-stakes call. Flag the mismatch in either direction: heavy method on a trivial decision, or flimsy evidence under a costly, irreversible one.

---

## Severity rating

Rate each finding by **decision damage** — what acting on this validation, as-is, would cost:

| Severity | Meaning |
|---|---|
| **Critical** | A load-bearing assumption drives a major or hard-to-reverse investment with no valid test — untested, tested only on stated intent, goalposts moved, or sample far too small to support the claim. The decision is effectively unsupported. |
| **Major** | The right assumption is in view but the evidence is weak for the stakes — wrong-fidelity method, no pre-set success criteria, anecdote- or single-voice-driven, qual/quant conflict ignored. |
| **Minor** | Hygiene that erodes trust in the learning — undocumented results, episodic instead of continuous testing, a secondary assumption left vague. |
| **Cosmetic** | Phrasing polish on an otherwise sound plan; don't pad the report with these. |

Overlaps — defer, don't duplicate: whether a **success metric is itself valid** (vanity, gameable, unfalsifiable) belongs to `pm-okr-metric-validity-audit` — this audit checks the assumption was *tested rigorously*, that one checks the *metric is worth hitting*. Whether the **spec document surfaced its assumptions as risks at all** belongs to `pm-spec-quality-audit` — this audit checks the *testing method and evidence*. Ranking discipline across competing bets belongs to `pm-prioritization-rigor-audit`.

---

## Output format

```
## Assumption Rigor Audit — [Plan / Experiment / Claim]
Context: [decision it informs · reversibility/stakes · discovery stage, if known]

### Critical
- [Issue] — what's wrong → fix. (Principle)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest decision-damage fixes.
```

Always end with the prioritized top issues — a flat list helps no one act.

---

## How to run a good audit

1. **Establish context first** — what decision does this validation support, and how costly/reversible is it? Rigor scales to that. A reversible $0 copy tweak and a six-month platform bet are not held to the same bar.
2. **Find the leap-of-faith assumption** — name the belief the whole thing rests on, and check whether *that* is what got tested.
3. **Only flag real costs** — an appropriately light test for a low-stakes call is correct, not a deficiency.
4. **Interrogate the evidence, not just the activity** — running a test ≠ learning something; check sample, duration, pre-set criteria, and signal vs. anecdote.
5. **Be specific in fixes** — name the assumption to test first, the better-fit method, the missing success threshold — not "be more rigorous."
6. **Prioritize, don't enumerate** — three decision-damaging findings beat fifteen nitpicks.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Accept "we tested it and users liked it" | Ask which assumption, by what method, against what pre-set bar |
| Treat the idea as the thing to test | Test the beliefs the idea depends on (desirability, viability, feasibility, usability, ethics) |
| Let the team test the comfortable assumption | Check the high-importance / low-certainty one was tested first |
| Pass "would you use this?" as validation | Require past behavior or a real action, not hypothetical intent |
| Accept conversion claims from n=10 | Match sample/duration/significance to the claim being made |
| Allow "close enough" after the fact | Hold the pre-agreed success criteria; shortfall → revise and re-test |
| Ignore that a disproven assumption changed nothing | Disconfirmation must move the decision; document the learning |
| Re-audit whether the metric itself is any good | Defer metric validity to `pm-okr-metric-validity-audit` |
| Demand a rigorous experiment for a tiny reversible call | Scale rigor to the decision's stakes |
| Deliver an unranked issue dump | Severity by decision damage + top-3 priorities |

---

## Source lessons (Uxcel)

- [Assumption Testing](https://uxcel.com/lessons/assumption-testing-988)
- [Best Practices for Assumption Testing](https://uxcel.com/lessons/best-practices-for-assumption-testing-486)
- [Evidence-Based Product Discovery](https://uxcel.com/lessons/evidence-based-product-discovery-287)
- [Framing the Problem into Hypotheses](https://uxcel.com/lessons/framing-the-problem-into-hypotheses-415)
