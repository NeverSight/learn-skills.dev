---
name: outbound-ab-test
description: "Use this skill when you want to test what works in outbound instead of guessing: \"A/B test my cold emails\", \"design an outbound experiment\", \"which variant won\", \"testing plan for our sequences\". Picks the variable worth testing (list, angle, offer, first line, CTA, channel, timing), writes the hypothesis, splits the audience fairly, sets the sample size and decision rule, and reads the result honestly, including when it is a tie. Produces a test plan, a log entry and the decision."
license: MIT
metadata:
  title: Outbound A/B test
  category: revops
  tags: "RevOps, SDR, Founders, Agencies, Marketing"
  author: prosyo
  version: "1.0.0"
  keywords: "cold email a/b testing, outbound experiment design, sequence split test, claude ab test skill, email testing sample size"
  inputs: "Current campaign and results, What you want to improve, Available volume"
  outputs: "Test plan with hypothesis, Sample size and split, Decision rule, Result readout"
---

Use this to run outbound tests that produce decisions. Most outbound "tests" compare 40 sends to 40 sends and crown a winner by noise.

## Inputs

- The current campaign and its baseline numbers.
- The metric to improve (usually positive reply rate or meetings per 100 contacts).
- How many contacts per week the team can send to the test.

## The play

### 1. Test the biggest lever first
Impact order, roughly: **list and segment** > **angle and offer** > **first line and personalization** > **CTA** > **subject line** > **send time**. Testing send time while the list is wrong wastes a month.

### 2. Write a hypothesis
"Leading with the hiring trigger instead of the pain will raise positive replies for SDR leaders, because the trigger shows why now." One variable changes; everything else stays the same.

### 3. Size it
Required contacts per variant depend on baseline and the lift you want to detect:

| Baseline positive reply rate | Detect 2x lift | Detect 1.5x lift |
| --- | --- | --- |
| 1% | ~2,300 per variant | ~7,700 per variant |
| 2% | ~1,150 | ~3,800 |
| 4% | ~550 | ~1,900 |

(Approximate, 80% power, 5% significance.) Rare outcomes need big samples. If volume cannot reach the size, test bigger changes (detect 2x), use total reply rate as a leading metric (it has a higher baseline), or run the test across several weeks of sends.

### 4. Split fairly
Random assignment within the same segment, same senders spread across both variants, same days and times. Never run variant A this week and B next week.

### 5. Decide in advance
Write the stop rule: the sample size, the metric, and what counts as a win. Check for guardrails too: bounce and unsubscribe rates must not rise.

### 6. Read and log
Report both variants with counts, the difference and whether it clears the rule. "No difference" is a result: keep the cheaper or simpler variant. Log every test so the team does not re-run old ones.

## Output format

```
Test: <name>   Hypothesis: <...>
Variable: <one>   Held constant: <list, senders, timing, steps>
Metric: <primary> | Guardrails: bounces, opt-outs
Size: N per variant | Expected duration: N weeks
Decision rule: <...>
Readout: A x/N (x%) vs B x/N (x%) → winner / no difference → action
```

## What good looks like

- One variable per test.
- Sample size decided before launch.
- The log shows what was learned, including tests that changed nothing.
- The common mistake is judging on open rates, which are inflated by privacy features and say nothing about replies.

## Rules

- MUST change only one variable per test.
- MUST set sample size and decision rule before launch.
- NEVER declare a winner below the planned sample, and never on fewer than 200 contacts per variant.
- NEVER use open rate as the deciding metric.

## Example prompts

- "Design a test: trigger-led vs pain-led first email for VP Sales. We send 400 a week."
- "Here are results for two variants. Is B really better?"
- "Plan the next 3 outbound experiments for our team, in order of impact."
