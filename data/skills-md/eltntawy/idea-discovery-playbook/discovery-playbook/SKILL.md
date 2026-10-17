---
name: discovery-playbook
description: >-
  Orchestrates end-to-end software idea discovery and validation—stage gates,
  skill routing, artifact filenames, and kill checkpoints from assumption map
  through scorecard. Use when validating an idea end-to-end, asking what to do
  next in discovery, or starting a new topic research folder.
disable-model-invocation: true
---

# Discovery Playbook

**Repository:** [idea-discovery-playbook](https://github.com/eltntawy/idea-discovery-playbook) — `npx skills add eltntawy/idea-discovery-playbook -g -y`

**Start here** for full idea validation. Invoke one child skill per stage; do not skip gates without user consent.

## Validation phases

| Phase               | Question                   | Exit gate                                                       |
| ------------------- | -------------------------- | --------------------------------------------------------------- |
| **0 — Frame**       | What are we testing?       | Topic folder + `assumption-map` with top assumptions; `regulatory-risk-scan` if regulated |
| **1 — Idea**        | Is the problem real?       | `problem-discovery` passed (kill criteria not met); or pivot segment |
| **2 — Market**      | Is there a wedge and room? | `market-research` + `competitor-landscape`; economics sketch OK |
| **3 — Economics**   | Can it pay?                | `market-sizing`, `revenue-model`, `positioning-wedge`           |
| **4 — Feasibility** | Can we ship and win?       | `feasibility-gate` — not Reject                                 |
| **5 — Demand test** | Will they act/pay?         | `validation-experiments` — fail threshold not hit               |
| **6 — Decision**    | Build, wait, or kill?      | `idea-scorecard` — Strong or Conditional go only for build      |
| **7 — Synthesis**   | One pack for stakeholders  | `discovery-synthesis`                                           |

**Product validation** (after prototype): `pmf-sean-ellis` — not part of pre-build gates.

## Skill router

| User need                         | Skill                     |
| --------------------------------- | ------------------------- |
| Riskiest assumptions, test queue  | `assumption-map`          |
| Mom Test interviews               | `problem-discovery`       |
| Why buyers switch / JTBD          | `jtbd-interviews`         |
| Live market + gap memo            | `market-research`         |
| Full competitor memo              | `competitor-landscape`    |
| TAM / SAM / SOM                   | `market-sizing`           |
| Category and positioning          | `positioning-wedge`       |
| Pricing and LTV:CAC               | `revenue-model`           |
| Build / wait / reject feasibility | `feasibility-gate`        |
| Smoke test, fake door, concierge  | `validation-experiments`  |
| End-to-end behavior memo          | `behavior-led-validation` |
| Weighted go/no-go                 | `idea-scorecard`          |
| Single researcher report          | `discovery-synthesis`     |
| Regulated domain                  | `regulatory-risk-scan`    |

## First run (workspace bootstrap)

If `discovery/` is missing:

1. Create `discovery/INDEX.md` listing active topic slugs, status, opened date, and last decision (see example below).
2. Create `discovery/<topic-slug>/` with `TOPIC.md` from `problem-discovery` → [TOPIC-TEMPLATE.md](../problem-discovery/TOPIC-TEMPLATE.md).
3. Create subfolders: `briefs/`, `research/`, `experiments/`, `scorecards/`.

**INDEX.md example:**

```markdown
# Discovery index

## Active

| Slug | Status | Opened | Last decision |
| --- | --- | --- | --- |
| <slug> | active | YYYY-MM-DD | In progress |

## Archived

(none)
```

## Artifact filenames (per topic)

| Kind               | Path pattern                                                               |
| ------------------ | -------------------------------------------------------------------------- |
| Topic index        | `discovery/<slug>/TOPIC.md`                                                |
| Brief / interviews | `briefs/YYYY-MM-DD-<slug>-brief.md`                                        |
| Market memo        | `research/YYYY-MM-DD-<slug>-market.md`                                     |
| Market sizing      | `research/YYYY-MM-DD-<slug>-market-sizing.md` (or section in `-market.md`) |
| Competitors        | `research/YYYY-MM-DD-<slug>-competitors.md`                                |
| Revenue            | `research/YYYY-MM-DD-<slug>-revenue.md`                                    |
| Positioning        | `research/YYYY-MM-DD-<slug>-positioning.md`                                |
| Feasibility        | `research/YYYY-MM-DD-<slug>-feasibility.md`                                |
| Assumptions        | `research/YYYY-MM-DD-<slug>-assumptions.md`                                |
| Experiments        | `experiments/YYYY-MM-DD-<slug>-experiment.md`                              |
| JTBD               | `briefs/YYYY-MM-DD-<slug>-jtbd.md`                                         |
| Regulatory         | `research/YYYY-MM-DD-<slug>-regulatory.md`                                 |
| Scorecard          | `scorecards/YYYY-MM-DD-<slug>-scorecard.md`                                |
| Synthesis          | `YYYY-MM-DD-<slug>-synthesis.md` (topic root or `research/`)               |
| PMF (post-build)   | `research/YYYY-MM-DD-<slug>-pmf.md`                                        |

## Default memo sections

Facts, Assumptions, Evidence, Analysis, Decision, Next experiment.

## Build gate

No production implementation until `idea-scorecard` = **Strong go** or **Conditional go** with named gaps.

## Related skills (external)

Optional complements — install separately:

- `npx skills add ferdinandobons/startup-skill` — full strategy, pitch
- `npx skills add brandonsgitstub/jtbd-skill` — JTBD docx workflow
- `npx skills add EmersonBraun/skills --skill brainstorm` — divergent ideation
