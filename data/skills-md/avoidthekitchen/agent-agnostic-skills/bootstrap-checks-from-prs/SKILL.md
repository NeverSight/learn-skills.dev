---
name: bootstrap-checks-from-prs
description: Bootstrap high-signal Amp checks from merged pull request history. Use this whenever the user asks to generate `.agents/checks`, infer team review conventions from PRs, or suggest checks from review history.
---

# Bootstrap Checks From PRs

Use this skill to mine recent merged PRs, infer recurring review expectations, and auto-write draft checks into `.agents/checks/` (and subtree check folders when applicable).

## What This Skill Produces

- Draft check files in `.agents/checks/*.md` (global) and `<area>/.agents/checks/*.md` (scoped)
- Root `AGENTS.md` updated to reference `.agents/checks/` for code reviews (created if missing)
- Evidence artifacts:
  - `artifacts/pr-scan.json`
  - `artifacts/rule-candidates.json`
  - `artifacts/check-drafts.json`
  - `artifacts/check-bootstrap-report.md`

## Inputs

- `repo` (optional): `owner/name`; if omitted, infer from local repo via `gh`
- `x` (optional): merged PRs to analyze (default `30`)
- `base_branch` (optional): default branch if not provided
- `time_window_days` (optional): constrain recency
- `min_frequency` (optional): default `2` (recommend `2-3`)
- `include_labels` (optional): list of labels
- `include_paths` (optional): only focus on these prefixes
- `exclude_paths` (optional): ignore these prefixes
- `max_checks` (optional): cap initial output (default `10`)
- `default_severity` (optional): default `medium`

## Execution Workflow

Run these scripts in sequence from the skill directory:

1. Collect PR evidence

```bash
python scripts/collect_prs.py --x 30
```

2. Extract and score candidate rules

```bash
python scripts/extract_rule_candidates.py --min-frequency 2
```

3. Render candidate check drafts

```bash
python scripts/generate_check_drafts.py --max-checks 10 --default-severity medium
```

4. Write checks with collision safety

```bash
python scripts/write_checks.py
```

5. Ensure root `AGENTS.md` references checks

- If root `AGENTS.md` is missing, create it.
- Add code-review guidance that tells agents to load `.agents/checks/` and relevant subtree-scoped `<subtree>/.agents/checks/`.
- Preserve existing instructions; append a focused section if needed.

6. Generate review report

```bash
python scripts/generate_report.py
```

If user provides custom inputs, pass them through all relevant scripts.

## Safety and Quality Requirements

- Never overwrite existing check files silently.
- On filename collisions, use `-draft` suffix (or `-draft-N`).
- Ensure root `AGENTS.md` references `.agents/checks/` for review checks.
- If root `AGENTS.md` is missing, create it.
- Do not rely on `write_checks.py` to mutate `AGENTS.md`; enforce this in agent workflow.
- Keep one check per file.
- Keep checks focused and actionable.
- Favor a small high-signal initial set (`5-10` checks).
- Escalate to `high`/`critical` only with strong security/compliance evidence.

## Recommended Agent Response After Running

Return a concise report with:

- Files created
- Confidence score per check
- Estimated false-positive risk
- Suggested decision for each check (`keep`, `refine`, `drop`)

Then recommend calibration on a holdout PR/diff before broad adoption.
