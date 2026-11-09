---
name: marketing-council
description: Use when the user needs to diagnose ambiguous or cross-functional marketing problems and coordinate the minimum set of specialist skills; route here only when this decision boundary is the clear owner.
---

# Marketing Council

## Job

Diagnose ambiguous or cross-functional marketing problems and coordinate the minimum set of specialist skills

Own the request when the marketing problem is ambiguous or genuinely cross-functional. If a single dominant function clearly owns the next decision, delegate to that focused Skill instead of retaining Council ownership. Otherwise Council is the safe fallback. If the request explicitly establishes dependent work across functions, use the dynamic router in `../../scripts/dynamic_router.py` to build a bounded DAG.

## Operating contract

1. Read `references/skill-spec.json` first for activation, invariants, workflow freedom, evidence rules, handoffs, and completion conditions.
2. Use `references/decision-model.md` when framing or challenging the decision.
3. Check `references/failure-modes.md` before finalizing a recommendation.
4. Render the response against `references/output-contract.md`.
5. Use packaged shared references or current external research only when they are load-bearing. Never present inference as evidence.

## Evidence discipline

Classify material claims as fact, inference, assumption, or unknown. Prefer supplied primary evidence. Verify current platform, policy, product, pricing, or market claims when freshness affects the recommendation. Do not fabricate research, tool calls, metrics, customer language, or causal proof.

## Routing

- Canonical Skill Router registry: `../../routing/skill-routes.json`.
- Single dominant function: delegate to the selected focused Skill.
- Ambiguous or cross-functional ownership: Council remains the fallback diagnostic owner.
- Explicit dependency chain: use the dynamic router at `../../scripts/dynamic_router.py` and keep the graph bounded to the minimum required Skills.
- After Skill ownership is known, theory/agent selection may use `../../scripts/neural_router.py`; neural nodes never replace Skill routing.

## Execution connections

- Primary specialist: `../../agents/council-director.md`
- Skeptical counterweight: `../../agents/marketing-skeptic.md`
- Domain challenge gate: `../../hooks/post-strategy-red-team.md`
- Evidence gate: `../../hooks/evidence-gate.md`
- Keep these as decision inputs, not automatic authority. The Skill owns the final evidence-bound synthesis.


## Council execution resources

- Synthesis and conflict resolution: `../../agents/council-director.md`
- Adversarial falsification: `../../agents/marketing-skeptic.md`
- Measurement and causality: `../../agents/measurement-strategist.md`
- Host capability contract: `../../tools/capabilities.yml`
- Focused Skill modules are under `skills/` in the standalone Council bundle; delegate only after ownership is established.

### Principle canon

- Market structure and segmentation: `../../references/canon/kotler.md`
- Relevance and smallest viable audience: `../../references/canon/godin.md`
- Product focus and demonstration: `../../references/canon/jobs-product-principles.md`
- Proposition and proof: `../../references/canon/ogilvy.md`
- Awareness and sophistication: `../../references/canon/schwartz.md`
- Reach, availability, and distinctive assets: `../../references/canon/sharp.md`
- Short and long effectiveness horizons: `../../references/canon/binet-field.md`

## Neural connections

- Owning Skill: `marketing-council`
- Decision boundary: `cross-functional decision`
- Neural graph: `../../neural/graph.json`
- Neural router: `../../scripts/neural_router.py`
- Theory and specialist selection happens only after Skill ownership; neural nodes never replace Skill routing.
- Use the local `references/skill-spec.json` evidence policy and invariants to reject neural recommendations that are unsupported by the request evidence.

## Completion gate

Complete only when the decision is explicit, evidence and inference are separated, a credible alternative was considered, outputs are rendered, material uncertainty is stated, and measurement plus reversal evidence are defined.

Local behavioral evaluations live in `evals/activation.yml`, `evals/behavior.yml`, `evals/pressure.yml`, and `evals/regression.yml`.
