---
name: system-one
description: >-
  Design, integrate, evaluate, self-host, and troubleshoot typed System One
  decision models including TypeSafe Jev and Convai Innovations Laya. Use for
  Choice/Score/Noul judgments inside deterministic software, app-control loops,
  routing, ranking, guardrails, calibration, or private Laya inference. Do not
  use for open-ended generation, exact rules or authorization, or generic LLM
  serving without a bounded decision contract.
license: MIT
compatibility: Current provider/model documentation needs network access; local Laya operation needs Python 3.10+, PyTorch, Transformers, and model-weight storage.
metadata:
  author: magnus919
  version: "1.1"
---

# System One decision models

Use a model for a constrained judgment, not for permissions or side effects:

```text
authorized state + trusted typed questions -> validated model answers
-> deterministic policy -> act / wait / review / abstain -> observed outcome
```

Keep hard business rules, authority checks, thresholds, action execution,
confirmation, and rollback in code or human control. A legal response shape
does not imply a correct judgment; a high probability is not permission.

## Start here

1. Inspect the real application's state source, action boundary, tests, and
   deployment before changing it. Preserve existing deterministic/no-key
   behavior unless explicitly changing it is in scope.
2. Fill `templates/decision-contract.md`: trusted state, question IDs/types,
   allowed answers, unknown/review lane, side effects, owner, deadlines, and
   rollback. For tool control, also use `templates/action-control-contract.md`.
   Use `references/concepts-and-patterns.md` for primitive semantics and composition.
3. Open **only the matching reference** below. Keep exact question text and
   criteria in trusted configuration, not user-supplied state.
4. Validate response IDs, types, option sets, distributions, score rubric,
   and finite values before policy code; record returned model/version and
   enforce the pinned deployment identity. Treat malformed,
   unavailable, stale, or low-evidence results as the specified fallback.
5. Verify on representative held-out data and the actual delivery boundary;
   record provider/model, question/policy revision, outcome, and failure lane
   without raw secrets or unnecessary personal data.

## Route by task

| Task | Read next |
|---|---|
| Hosted Jev API or SDK integration | `references/jev.md`; run `scripts/decision_demo.py` offline first |
| Laya checkpoints, routing, language, CPU/GPU/MPS | `references/laya.md` |
| Native C++ Laya inference, CUDA/Vulkan, or Jev-compatible HTTP | `references/laya-cpp.md` |
| Local or private/VPC Laya service | `references/laya-self-hosting.md`, then `references/hosting-and-troubleshooting.md` |
| Browser/desktop/voice control, agent routing, ranking, guardrails, deadlines | `references/use-case-patterns.md` |
| Probability, threshold, calibration, model comparison | `references/evaluation-and-calibration.md` and `templates/benchmark-record.md` |
| Synthetic QA pilot for Jev (failure triage, extra-test choice, semantic grading) | `references/qa-pilot.md`; run `scripts/jev_qa_pilot.py` offline first |
| Paired-eval semantic assertion audit in CI | `references/qa-pilot.md`, then `scripts/jev_eval_audit.py`; treat its verdicts as advisory and preserve exact grader results |
| Calibrate Jev's advisory eval judgments against real outputs | `references/qa-pilot.md` and `references/evaluation-and-calibration.md`; use `scripts/jev_eval_calibration.py` locally with a complete audit artifact and independent reviewer labels |
| New open model or Jev-style replica | `references/ecosystem-radar.md` |
| Failure, latency, device fallback, upgrade, rollback | `references/hosting-and-troubleshooting.md` |

Run `python3 scripts/systemone_probe.py --request examples/request.json` for an offline
contract check. Add `--live` only when the user has authorized transmitting
that state and incurring cost. For local Laya, `scripts/laya_service.py`
requires a pinned local model directory and a runtime secret; it is a private
reference adapter, not a public Internet service.

## Cross-cutting limits

- Jev is managed/API-only; do not invent a self-hosted Jev weight download.
- Laya and Jev can share a typed application interface, but not assumed
  thresholds, calibration, latency, language behavior, or model quality.
- Prefer `other`, `unknown`, or review when labels are not exhaustive.
  Shortlisting changes the population over which Choice probabilities apply.
- Independent questions may share one call. Dependent questions need another
  call only when the first answer changes their state or candidate set.
- A model cannot replace exact arithmetic, provenance, eligibility, safety
  reflexes, or irreversible approval. A text-generating model may be a separate
  bounded stage after a typed route, not an implicit source of authority.

Finish an integration only when its contract, held-out evaluation, failure
path, deployment/readiness check, and rollback record exist. For diagnosis,
stop after the smallest evidence identifies the boundary and one recheck
verifies a fix, or after three non-converging passes with evidence for the
owner. Do not generalize from a single demo or vendor benchmark.

## When not to use

Use `ml-engineering` for general training strategy; `docker-compose` or
`kubernetes` for their serving infrastructure; `ai-governance` for
organization-wide authority design. Use a generative-model skill for prose,
open-ended planning, or long reasoning without a typed-decision contract.
