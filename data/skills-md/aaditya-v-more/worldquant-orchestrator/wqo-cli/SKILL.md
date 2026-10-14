---
name: wqo-cli
description: Set up and use the WQO command-line client for WorldQuant BRAIN research. Use for CLI installation, authentication onboarding, command discovery, or research workflows spanning data discovery, simulations, analysis and explicitly confirmed submission.
---

# WQO CLI

Read [setup and operational boundaries](references/runtime.md) first. This skill
works alone. Companion skills provide deeper workflow guidance when installed.

## Start

Resolve the runner relative to this installed SKILL.md. From the user's project:

```bash
bash /absolute/path/to/wqo-cli/scripts/wqo.sh --version
bash /absolute/path/to/wqo-cli/scripts/wqo.sh --help
bash /absolute/path/to/wqo-cli/scripts/wqo.sh state
```

The runner installs missing WQO into the project's `.wqo/venv`, using PyPI.
Use this runner in place of `wqo` in the commands below, even if a shell cannot
find the command directly. No manual repository clone is required.

## Research workflow

1. `wqo auth status`: establish the account and quotas; hand Persona to the user.
2. `wqo data datasets`, `wqo data fields`, `wqo data operators`: select available
   inputs matching the requested region, universe and delay.
3. `wqo sim run --code 'rank(close)'` tests one generic example;
   `wqo mine --dataset DATASET_ID --budget 10 --dry-run` previews a mining run.
   Live simulations consume quota; respect the user's research scope and budget.
4. `wqo gate ALPHA_ID --json` reports eligibility. Inspect failures and unavailable
   checks; a good grade or attractive Sharpe is not permission to submit.
5. `wqo submit ALPHA_ID` prints the report and exits 4. Only after the user has
   explicitly approved that alpha may you add `--confirm`. Never automatically
   retry an uncertain submission.

Examples are illustrative; choose actual field/alpha IDs from the user's account.
Use `wqo COMMAND --help` for detailed flags and `wqo account status` for standing.
Raw `wqo api GET PATH` is read-only; it cannot bypass dedicated write safeguards.

## Optional companion skills

`wqo-auth`, `wqo-data`, `wqo-simulate`, `wqo-mine`, `wqo-analyze`, `wqo-alphas`,
`wqo-submit` and `wqo-account` each include their own runner and boundaries.
Installing one does not require the others. Skills are installed through
`npx skills add` in the user's project; never add `--global` unless requested.
