---
name: incrementality-design
description: Use when the user needs to design counterfactual measurement that estimates causal marketing lift; route here only when this decision boundary is the clear owner.
---

# Incrementality Design

## Job

Design counterfactual measurement that estimates causal marketing lift

Own this request only when **incrementality design** is the clear decision boundary. If ownership is ambiguous or several functions compete, route to `marketing-council`. If the user explicitly asks for dependent work across functions, use `../../scripts/dynamic_router.py` to build a bounded DAG.

## Operating contract

1. Read `references/skill-spec.json` first for activation, invariants, workflow freedom, evidence rules, handoffs, and completion conditions.
2. Use `references/decision-model.md` when framing or challenging the decision.
3. Check `references/failure-modes.md` before finalizing a recommendation.
4. Render the response against `references/output-contract.md`.
5. Use packaged shared references or current external research only when they are load-bearing. Never present inference as evidence.

## Evidence discipline

Classify material claims as fact, inference, assumption, or unknown. Prefer supplied primary evidence. Verify current platform, policy, product, pricing, or market claims when freshness affects the recommendation. Do not fabricate research, tool calls, metrics, customer language, or causal proof.

## Routing

- Focused request: stay inside this Skill.
- Ambiguous or cross-functional ownership: hand to `marketing-council`.
- Explicit dependency chain: use `../../scripts/dynamic_router.py`.
- After Skill ownership is known, theory/agent selection may use `../../scripts/neural_router.py`; neural nodes never replace Skill routing.

## Execution connections

- Primary specialist: `../../agents/measurement-strategist.md`
- Skeptical counterweight: `../../agents/marketing-skeptic.md`
- Domain challenge gate: `../../hooks/incrementality-required.md`
- Evidence gate: `../../hooks/evidence-gate.md`
- Keep these as decision inputs, not automatic authority. The Skill owns the final evidence-bound synthesis.


## Neural connections

- Owning Skill: `incrementality-design`
- Decision boundary: `incrementality design`
- Neural graph: `../../neural/graph.json`
- Neural router: `../../scripts/neural_router.py`
- Theory and specialist selection happens only after Skill ownership; neural nodes never replace Skill routing.
- Use the local `references/skill-spec.json` evidence policy and invariants to reject neural recommendations that are unsupported by the request evidence.

## Completion gate

Complete only when the decision is explicit, evidence and inference are separated, a credible alternative was considered, outputs are rendered, material uncertainty is stated, and measurement plus reversal evidence are defined.

Local behavioral evaluations live in `evals/activation.yml`, `evals/behavior.yml`, `evals/pressure.yml`, and `evals/regression.yml`.
