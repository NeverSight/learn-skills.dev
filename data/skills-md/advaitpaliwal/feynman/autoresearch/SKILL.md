---
name: autoresearch
description: Bounded research experiment loop that tries hypotheses, measures benchmark evidence, keeps what works, and records what fails. Use when the user asks to optimize a research metric, run an experiment loop, improve model/retrieval/evaluation performance iteratively, or benchmark a research hypothesis.
---

# Autoresearch

Run the `/autoresearch` workflow. The slash command expands the full workflow instructions in the active session; do not try to read a relative prompt-template path from the installed skill directory.

Optional tools used when visible: `init_experiment`, `run_experiment`, `log_experiment`. Without those tools, run the benchmark through the available shell/tooling and record benchmark result, evidence, and decision in the session files.

Session files: `autoresearch.md`, `autoresearch.sh`, `autoresearch.jsonl`
