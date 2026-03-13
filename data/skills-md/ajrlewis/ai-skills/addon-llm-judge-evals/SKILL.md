---
name: addon-llm-judge-evals
description: Use when you want rubric based LLM quality scoring on generated outputs; pair with addon-deterministic-eval-suite.
---

# Add-on: LLM Judge Evals

Use this skill when you need qualitative evaluation (clarity, domain fit, UX coherence, docs quality) in addition to deterministic checks.

## Compatibility

- Works with all stacks.
- Best paired with `addon-deterministic-eval-suite`.

## Inputs

Collect:
- `JUDGE_BACKEND`: `auto` | `langchain` | `google-adk` (default `auto`).
- `JUDGE_MODEL`: model id to run scoring.
- `JUDGE_TIMEOUT_SECONDS`: default `60`.
- `JUDGE_MAX_RETRIES`: default `2`.
- `JUDGE_TEMPERATURE`: default `0`.
- `JUDGE_FAIL_ON_BACKEND_MISMATCH`: `yes` | `no` (default `yes`).
- `JUDGE_RUBRIC_MODE`: `product` | `security` | `developer-experience` | `custom`.
- `PASS_THRESHOLD`: default `0.75`.
- `BLOCK_ON_JUDGE_FAIL`: `yes` | `no` (default `no`).

## Integration Workflow

1. Add judge artifacts:
```text
config/skill_manifest.json
evals/judge/rubric.md
evals/judge/cases/
scripts/evals/run_llm_judge.py
.github/workflows/evals-judge.yml
REVIEW_BUNDLE/JUDGE_REPORT.md
```
- Copy and adapt this skill's bundled starter script:
- `scripts/run_llm_judge.py`
- Place the adapted result in the target project at `scripts/evals/run_llm_judge.py`.

2. Define rubric:
- scoring categories and weights
- failure reasons template
- required evidence links (files/lines/commands)

3. Execute judge run:
- evaluate generated files against rubric per scenario
- resolve backend from `config/skill_manifest.json` plus judge inputs
- use a single adapter boundary for backend-specific scoring
- store structured JSON + markdown summary
- replace the bundled starter template's placeholder reporting with a real project-local backend adapter before treating judge scores as authoritative

4. Merge policy:
- default advisory (`BLOCK_ON_JUDGE_FAIL=no`)
- blocking only when explicitly configured

## Backend Resolution Contract

- `scripts/evals/run_llm_judge.py` must read `config/skill_manifest.json` as the source of truth for selected skills and declared judge capabilities.
- The manifest should include:

```json
{
  "base_skill": "architect-python-uv-fastapi-sqlalchemy",
  "addons": [
    "addon-deterministic-eval-suite",
    "addon-llm-judge-evals",
    "addon-langchain-llm"
  ],
  "capabilities": {
    "judge_backends": ["langchain"]
  }
}
```

- Resolution order:
  - If `JUDGE_BACKEND != auto`, use the requested backend only if the matching addon is present in the manifest.
  - If `JUDGE_BACKEND=auto` and only `addon-langchain-llm` is present, use `langchain`.
  - If `JUDGE_BACKEND=auto` and only `addon-google-agent-dev-kit` is present, use `google-adk`.
  - If both addons are present, fail and require explicit `JUDGE_BACKEND`.
  - If neither addon is present, fail with an explicit unsupported configuration error.
- Model resolution:
  - `JUDGE_MODEL` wins when set.
  - For `langchain`, fall back to `DEFAULT_MODEL`.
  - For `google-adk`, fall back to `ADK_DEFAULT_MODEL`.
- The judge runner should expose a stable adapter interface (for example `JudgeBackend.score(prompt)`) so rubric logic, thresholding, and report generation stay backend-agnostic.

## Required Template

### `evals/judge/rubric.md`
```markdown
# Judge Rubric

- Technical coherence (0-1)
- Requirement coverage (0-1)
- Domain language alignment (0-1)
- UX quality and states (0-1)
- Documentation clarity (0-1)

Pass threshold: 0.75
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Never replace deterministic gates with judge scores.
- Keep prompts/rubrics versioned in repo for auditability.
- Record model/version and timestamp for each run.
- Surface uncertainty as explicit notes, not silent pass.
- Do not infer judge backend from incidental files or imports; use the manifest and explicit inputs.
- If multiple LLM-capable addons are installed, do not guess. Require an explicit `JUDGE_BACKEND`.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f evals/judge/rubric.md
test -f scripts/evals/run_llm_judge.py
test -f .github/workflows/evals-judge.yml
test -f REVIEW_BUNDLE/JUDGE_REPORT.md || true
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
