---
name: pm-experimentation-ab
description: "Design or critique an A/B test or controlled product experiment with statistical rigor — pre-registered falsifiable hypothesis, sample-size/power up front, a full business cycle, one primary metric plus guardrails, segment + long-term reads, and a pre-set iterate/pivot/persevere decision. Catches the defaults Claude misses: peeking/early stopping, tiny samples, no guardrails, vanity metrics, \"it won\" with no learning loop. Trigger when asked to set up or review an A/B test, design an experiment, pick experiment metrics, decide sample size/significance/duration, or interpret/act on test results."
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# A/B Testing & Experimentation Skill

## How this skill behaves (read first)

This is a **generative** skill (it designs or revises an experiment plan, and can review an existing test setup). Experimentation is where an AI assistant's defaults are quietly wrong in ways that produce confident, false conclusions. Claude will happily "set up an A/B test" that **declares a winner on a handful of users**, **peeks and stops the moment p < 0.05**, **optimizes one metric with no guardrail** for the damage it does elsewhere, runs for three weekdays, and ends at "B won" with no segments, no long-term read, and nothing written down. A bad experiment is worse than none — it launders a guess into "data."

So this skill gates, and the gate is statistical discipline:

1. **Establish context** — is a controlled experiment even the right tool here, what single decision it informs, and the risk level (these set confidence, split, and duration).
2. **Apply the always-true core** — pre-register the hypothesis and success criteria, size the test *before* running it, run a full cycle, use one primary metric + guardrails, interpret past "it won," and close the learning loop.
3. **Surface the context-dependent decisions** (confidence threshold, traffic split, A/B vs. multivariate, metric type, leading/long-term indicators, test prioritization) with trade-offs; let the user choose.

Then it **hands off to `pm-okr-metric-validity-audit`** (are the chosen metrics valid, not vanity?) and **`pm-assumption-rigor-audit`** (is the hypothesis the riskiest, falsifiable, pre-committed?).

Scope & pairing: this skill owns **the controlled-experiment method and its statistics**. It pairs with `pm-assumption-testing`, which owns *choosing what to test and the cheapest way to test it* — when the question is early-stage, low-traffic, or better answered qualitatively, **defer to assumption-testing** rather than forcing an A/B test. It defers broad **what-to-build-next ranking** to `pm-prioritization`, **metric definitions/OKRs** to `pm-okrs-kpis`, and the high-stakes **roll-out go/no-go** to `pm-decision-quality-audit`.

---

## Step 0 — Establish context before designing the test

Ask if not known; state the assumption if proceeding without an answer:

- **Is a controlled experiment the right tool?** A/B testing needs enough traffic to hit a valid sample in reasonable time, a change that shows up in *behavior*, and a question of "which performs better," not "does anyone want this." If traffic is thin, the idea is unvalidated, or the question is "why," **route to `pm-assumption-testing`** (cheaper qualitative or low-fidelity tests first). Don't A/B test your way to product-market fit.
- **What single decision does this inform, and at what risk?** One decision per experiment. The risk/impact of being wrong sets the confidence threshold and traffic split (a checkout or pricing change is not a button-color change).
- **What's the baseline and the minimum effect worth detecting (MDE)?** You need the current metric value and the smallest improvement that would matter — both feed the sample-size calculation. Smaller baselines and smaller MDEs need bigger samples.
- **What's the business cycle / are there confounds?** Weekday-vs-weekend patterns, seasonality, launches, promos, competitor moves. These set minimum duration and rule out skewed windows.

---

## The always-apply core (true for any controlled experiment)

### Pre-register before you run

- **Write a falsifiable hypothesis with reasoning:** "If we [make this change], then [this metric] will [increase/decrease] by [magnitude] because [user insight]." Vague ("let's see if a bigger button works") produces vague results.
- **Design to *disprove*, not confirm.** Set success *and* failure criteria up front; pre-commit to what result would change your mind. If every test "wins," you're measuring the wrong things or retrofitting the story — you need to be wrong sometimes.
- **Set the decision thresholds in advance.** Decide before launch what outcome means iterate vs. pivot vs. persevere (e.g., "<20% lift → pivot, 20–40% → iterate, >40% → persevere"). Pre-commitment is what stops post-hoc rationalization.

### Size and run it correctly

- **Calculate sample size first, then derive duration.** From baseline, MDE, and confidence, compute users-per-variation; daily traffic then tells you how long to run. Skipping this is how tests get stopped too early or dragged on forever.
- **Reach real significance — don't peek.** Use a confidence level (95%/p<0.05 default) and let the test run to its planned sample and a full business cycle (≥1–2 weeks). Stopping at the first green p-value inflates false positives. "Significant after 100 users" is a setup bug, not a win.
- **Assign randomly and persistently; QA both arms.** 50/50 by default, consistent per user across visits, verified on devices/browsers with tracking firing correctly. Never change the split mid-test — it skews results.

### Measure honestly

- **One primary metric + guardrails.** The primary metric is tied to the hypothesis and decides success; add **guardrail/health metrics** (e.g., revenue, churn, order value, support volume, latency) so you catch a "win" that quietly harms something else. Drop vanity metrics that feel good but don't drive a decision.
- **Interpret past "it won."** Read **segments** (mobile/desktop, new/returning, geo, source — an overall +10% can hide mobile −5%), check **secondary impacts**, and weigh **short-term vs. long-term** (a holdout group reveals whether a short-term lift survives).

### Close the loop

- **Document and decide.** Record the pre-written hypothesis, setup, result (including failures), and the iterate/pivot/persevere call against your pre-set thresholds. Feed the outcome into the relevant OKR. Build a searchable learning repository so the org stops re-running the same test — failed experiments often carry the most valuable warnings, and surprising user behavior (Twitter's "@username", Airbnb business travelers) is where the breakthroughs hide.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Applying every method and metric type at once is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Confidence threshold** | 99% for critical/irreversible flows (checkout, pricing); 90% for low-risk, fast-iteration features | Treating 95% as sacred for trivial changes, or using 90% on high-blast-radius changes | Tiered by risk; 95% default, raise for critical, lower only for cheap reversible calls |
| **Traffic split** | 50/50 for fast, low-risk reads | 90/10 (or smaller exposure) when the variant carries real downside (new pricing, major redesign) | 50/50 unless downside risk justifies limiting exposure; never change mid-test |
| **A/B vs. multivariate** | A/B to isolate one change cleanly; multivariate to find interaction effects between elements | Multivariate without the traffic — N elements × variations multiplies the sample needed (4 combos = 4× traffic) | A/B by default; multivariate only on high-traffic surfaces |
| **Standardized vs. custom metrics** | Standardized (signup rate, WAU) for cross-experiment comparability; custom ("time to first task") for the specific hypothesis | Only-standardized (misses the feature's real effect) or only-custom (loses alignment) | Track a small standardized set *plus* a custom metric tied to the hypothesis |
| **Leading vs. lagging / long-term** | Leading indicators (add-to-cart) for fast signal when the goal is rare/slow; holdout groups for sustained impact | Calling a long-term win from short-term metrics alone | Use leading indicators to read early; hold out a slice to confirm durability |
| **Test prioritization** | PIE (Potential × Importance × Ease) or similar to sequence a backlog of test ideas | Running many tests at once with no ranking, or testing low-traffic pages first | Score ideas on PIE; broad roadmap ranking defers to `pm-prioritization` |

A couple of contexts flip several defaults at once: a **low-traffic / pre-PMF** product should usually *not* run A/B tests (route to assumption-testing); a **high-risk irreversible** change warrants 99% confidence, a conservative split, guardrails weighted heavily, and a `decision-quality` check before roll-out.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — is the hypothesis the *riskiest* assumption worth a controlled test, phrased falsifiably, with success criteria set before the run, and read honestly afterward (not confirmation-biased)?
- **`pm-okr-metric-validity-audit`** *(offer — if it names primary/guardrail metrics)* — are the primary and guardrail metrics valid measures of the outcome (not vanity metrics like page views), and do they tie to a real objective? An experiment optimizing a bad metric scales the wrong thing.
- **`pm-decision-quality-audit`** *(offer — if it drives a high-stakes/irreversible roll-out)* — was the iterate/pivot/persevere call a sound *process* (pre-set thresholds, pre-mortem, separating process from outcome) rather than resulting on a lucky number?

**Composition (per `docs/orchestration-policy.md` §9):** this skill pairs with `pm-assumption-testing` — a peer that owns *what to test and the cheapest method* (defer); this one runs the controlled experiment once A/B is the right tool. If the audits surface a conflict, resolve toward the purpose: **an experiment exists to produce a trustworthy decision — if it can't reach a valid sample, lacks guardrails, or won't change what you do, don't run it as an A/B test.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Declare a winner on a tiny sample | Calculate sample size first; run to it |
| Peek and stop at the first p < 0.05 | Pre-set confidence + a full business cycle; don't stop early |
| Run for three weekdays | Cover ≥1–2 weeks / a full business cycle; avoid skewed windows |
| Optimize one metric blind to side effects | One primary metric + guardrail/health metrics |
| Chase vanity metrics (page views) | Tie metrics to the hypothesis and a decision |
| Write a vague "let's test X" | Falsifiable "if/then/because" hypothesis with success *and* failure criteria |
| Read only the overall number | Segment (device/new-returning/geo) + secondary + long-term reads |
| Change the traffic split mid-test | Fix split up front; keep assignment random and persistent |
| Multivariate with no traffic | A/B by default; multivariate only on high-traffic pages |
| A/B test an unvalidated, low-traffic idea | Route early/low-traffic/qualitative questions to assumption-testing |
| Stop at "B won" | Document, decide iterate/pivot/persevere on pre-set thresholds, bank the learning |
| Ship the test plan unchecked | Hand off to okr-metric-validity + assumption-rigor (+ decision-quality for big roll-outs) |

---

## Source lessons (Uxcel)

- [A/B Testing & Experimentation](https://uxcel.com/lessons/ab-testing-experimentation-142)
- [A/B Testing](https://uxcel.com/lessons/ab-testing-838)
- [Experimentation Metrics](https://uxcel.com/lessons/experimentation-metrics-882)
- [Learning from Your Launches](https://uxcel.com/lessons/learning-from-your-launches-634)
