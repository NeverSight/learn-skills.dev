---
name: idea-scorecard
description: Scores software ideas across validation stages using an evidence hierarchy, assumption ledger, weighted go, conditional go, pivot, or kill thresholds. Use when the user asks to score an idea, make a go/no-go decision, or validate before build.
disable-model-invocation: true
---

# Idea Scorecard

## Evidence hierarchy (canonical)

Weakest to strongest — map all memos and experiments to these levels:

| Level | Label     | Examples                                            |
| ----- | --------- | --------------------------------------------------- |
| 1     | Awareness | Views, impressions                                  |
| 2     | Interest  | Opinions, compliments, hypothetical praise          |
| 3     | Intent    | Signups, meetings, waitlists with context           |
| 4     | Behavior  | Repeat use, workflow adoption, design-partner time  |
| 5     | Revenue   | Payment, deposits, LOIs, pre-orders at target price |

`behavior-led-validation` uses L0–L5 labels that map to this hierarchy (L0–L1 ≈ 1–2, L2 ≈ 3, L3 ≈ 4, L4–L5 ≈ 5).

## Assumption ledger

Before scoring, list open claims from `assumption-map` or prior memos:

| Assumption | Evidence tier (1–5) | Test | Status                    |
| ---------- | ------------------- | ---- | ------------------------- |
|            |                     |      | open / validated / killed |

Cap **Revenue** and **Channel** stage scores when critical assumptions remain open with tier ≤ 2.

## Weighted scorecard

| Stage              | Score 1-10 | Weight | Weighted | Evidence summary                          |
| ------------------ | ---------- | ------ | -------- | ----------------------------------------- |
| Problem            |            | 1.5    |          |                                           |
| Solution           |            | 1.5    |          |                                           |
| Market             |            | 1.0    |          |                                           |
| Channel            |            | 1.0    |          |                                           |
| Revenue            |            | 1.5    |          |                                           |
| Founder–market fit |            | 0.5    |          | Domain, access, distribution, constraints |
| Scale              |            | 0.5    |          |                                           |
| **Total**          |            |        | **/75**  |                                           |

**Total max:** sum of (score × weight). Weights sum to 7.5; perfect 10s → **75**.

## Decision thresholds

- **60–75:** Strong go
- **45–59:** Conditional go — close named gaps first
- **30–44:** Pivot
- **0–29:** Kill or restart

Recalculate thresholds if you omit Founder–market fit (max **70**, bands: 56 / 42 / 28 / 0).

## Kill cues

- Problem confirmed by fewer than half of relevant interviews
- No paying customers after four weeks of revenue testing
- LTV:CAC **below 2:1** in the base case (see `revenue-model` bands)
- All acquisition channels exceed target CAC
- `feasibility-gate` records **Reject** or **Wait**

LTV:CAC **2:1 to < 3:1** does not auto-kill; use **Conditional go** and document the economics gap.

## Output

Save to `discovery/<topic-slug>/scorecards/YYYY-MM-DD-<topic-slug>-scorecard.md` using [TEMPLATE.md](TEMPLATE.md).

Do not recommend implementation unless the decision is **Strong go** or **Conditional go** with explicit remaining gaps.

After scoring, offer `discovery-synthesis` to compile a researcher pack.
