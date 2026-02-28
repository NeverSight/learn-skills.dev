---
name: nobs-review
description: Multi-model code review for pull requests and git diffs. Use when asked to "review my code", "review this PR", "review my changes", "find reviewers", or "run a code review". Suggests appropriate reviewers based on which files changed, runs iterative review rounds across multiple AI models, and tracks findings across sessions.
---

# Review

Multi-model review without runtime interception.

- One shared contract per review: `.reviews/<review_id>/contract.json`
- Rounds accumulate: `.reviews/<review_id>/rounds/rNNN/`

## Interaction Order

1. Run init. Report detected dev tool and confidence.
2. Report risk analysis.
3. Report recommended reviewers.
4. Ask user to confirm or override.
5. Run review.

Low-confidence detection: say so and continue.

## Workflow

### 1) Init

```bash
python3 skills/nobs-review/scripts/init_review.py --task "<what to review>"
```

Override tool detection:

```bash
python3 skills/nobs-review/scripts/init_review.py --task "<what to review>" --dev-tool claude
```

Refresh existing review (keep history):

```bash
python3 skills/nobs-review/scripts/init_review.py --id <review_id> --task "<updated scope>" --refresh
```

Init detects the current dev tool, analyzes diff risk, pre-enables recommended reviewers in contract, and sets `.reviews/.active_review_id`.

### 2) Confirm reviewers

Check `.reviews/<id>/contract.json`:
- `reviewers[].enabled`
- `reviewers[].command_template`

Accept recommendation or pick your own.

### 3) Run round

```bash
python3 skills/nobs-review/scripts/run_review.py --id <review_id> --round auto
```

Or use active id:

```bash
python3 skills/nobs-review/scripts/run_review.py --round auto
```

Limit reviewers:

```bash
python3 skills/nobs-review/scripts/run_review.py --id <review_id> --round auto --reviewers codex_high,claude_opus
```

### 4) Merge findings

```bash
python3 skills/nobs-review/scripts/merge_review.py --id <review_id> --round latest
```

`--round auto` treated as `latest` in merge.

Outputs per round: `merged.md`, `resolution.md` in `.reviews/<id>/rounds/rNNN/`.
Latest pointers at review root (`merged-latest.md`, `resolution-latest.md`) are ephemeral — overwritten on next merge.

For persistent checklist edits, use round-scoped `resolution.md`.

### 5) Review auto-fix candidates

After merge, check `auto-fix-candidates.md` in the round directory (or `auto-fix-candidates-latest.md` at review root).

Findings listed there satisfy **both**:
- `fix_determinism = high` — exactly one right fix, no judgment needed
- `fix_scope = local` — change confined to 1–3 lines in one function

Apply each fix, mark `Applied: [x]`, commit, then run a new round to verify:

```bash
python3 skills/nobs-review/scripts/run_review.py --round auto
python3 skills/nobs-review/scripts/merge_review.py --round latest
```

Findings that do **not** appear in `auto-fix-candidates.md` require human judgment and are tracked in `resolution.md`.

The `auto_fix_threshold` in `contract.json → policy` controls the boundary:

```json
"auto_fix_threshold": { "determinism": "high", "scope": "local" }
```

Raise `determinism` to `medium` or `scope` to `cross-file` to widen the auto-fix set.

### 6) Fix and re-review

```bash
python3 skills/nobs-review/scripts/run_review.py --id <review_id> --round auto
python3 skills/nobs-review/scripts/merge_review.py --id <review_id> --round latest
```

Creates `r001 -> r002 -> ...` preserving history.

## Rules

- Missing reviewer CLI: fail, don't fake.
- Invalid JSON output: keep raw, mark parse failure.
- No single round is final truth; compare across rounds.

## Output Contract

- [references/schema.md](references/schema.md)
- [references/providers.md](references/providers.md)

## Notes

- Deterministic logic lives in scripts; this skill is thin by design.
- High-risk diffs: use at least two strong reviewers.
- User decides final reviewer set; recommendation is advisory.
