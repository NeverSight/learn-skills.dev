---
name: wikiskill-evolve
description: "Run the WikiSkill self-evolution loop (arXiv 2608.27454) on a Hermes workspace — raw→maintainer→proposer→gate with strict R_val > R_best gating."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wikiskill, evolution, skills, paper-implementation, hermes]
    homepage: https://github.com/ashutoshsinghpr7/wikiskill
---

# WikiSkill Evolve

Run Google's WikiSkill evolution loop (arXiv:2608.27454) — a faithful
implementation with Hermes as the reference backend. The agent evolves its own
skills: raw sessions → a maintainer distills failure patterns into a
persistent wiki → a proposer writes a candidate skill → a validation gate
accepts it **only if** `R_val > R_best` (git rollback otherwise).

## When to use

- You want an agent's own experience (traces) turned into reusable skills
- You want to test whether a candidate skill actually helps, with statistics
  instead of vibes
- You're running the paper's protocol on your own tasks

## Install

```bash
pip install wikiskill          # Python ≥ 3.10; works with Hermes, Claude Code
```

## Run the loop

```bash
wikiskill init myws                        # workspace + auto-graded bench
wikiskill evolve myws --iters 3            # train → maintain → propose → gate
wikiskill status myws                      # baseline, r_best, skill state
wikiskill compare wsA wsB --iters 5        # paired exact-binomial comparison
wikiskill transfer src dst                 # copy accepted skills to another ws
```

## Reading the output

- `runs/state.json` — `baseline` (S₀ on val), `r_best`, `next_iter`
- `wiki/log.md` — every maintenance/proposal/gate decision with evidence
- `wiki/patterns/` — distilled failure patterns (the raw material)
- `wiki/skill-impact.md` — rejected proposals stay visible (paper requirement)
- Gate verdicts: `ACCEPTED` (R_val > R_best, git commit), `REJECTED`
  (rolled back), `no_action` (proposer declined — a valid outcome)

## Backends

```bash
wikiskill init myws --backend claude       # Claude Code as the worker
```

Hermes is the reference backend; Claude Code ships in the box; codex/opencode
are on the roadmap. All speak open SKILL.md, so evolved skills transfer.

## Honest-expectation notes

- Each iteration costs ~$0.09 on free-tier models (gemini-lite class) —
  turn budgets and `--max-turns` bound the spend
- A weak model may produce `no_action` iterations — that's the gate working,
  not a failure; skill accumulation needs a reasonably strong proposer
- The gate has rejected harmful skills in live runs — a rejection is a win
