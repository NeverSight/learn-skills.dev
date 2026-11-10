---
name: distill
description: "Ground and confirm independent user intents, then assess outcome needs and mechanism fit before architectural design."
disable-model-invocation: true
---

# distill — Grounded Intent Inquiry

## Domain Rubric

### Intent Boundaries

- Separate desired outcome **X** from requested mechanism **Y**. Extract independently assessable intents with stable IDs (`I1`, `I2`, ...); shared goals or mechanisms are valid.
- Preserve explicit requests and label inferred intent as inferred. An outcome without a mechanism is valid; keep its solution open rather than inventing technologies.
- Ground proposals with targeted authoritative docs and relevant code. Inspect enough to identify context and boundaries; reserve suitability evaluation for confirmed intent.
- User confirmation establishes intended meaning, not runtime proof or implementation authorization. Preserve confirmed context across turns; revisions invalidate only affected intents and their dependent claims.
- Keep inquiry read-only: inspect and report; leave design, workspace mutation, and experiments to separately invoked workflows.

### Post-Confirmation Evaluation

Assess each confirmed intent against:

- **Need & Success**: Actual problem, desired outcome, and observable success criteria.
- **Existing Capability**: What the system already supports and the remaining delta.
- **Constraints & Cost**: Scale, consistency, latency, operational capacity, maintenance, and user/environmental limits that affect the outcome.
- **Relation Fit**: Whether Y, when present, addresses X proportionally within the stated scope.
- **Evidence & Gaps**: Load-bearing code, contract, verified source, or measured evidence; distinguish supported claims from assumptions and runtime unknowns.
- **Cross-Intent Dependencies**: Shared constraints, ordering, conflicts, and evidence whose failure changes another intent.

Use this taxonomy internally; translate findings into rationale rather than exposing rubric labels:

- `Aligned`: Y resolves X proportionally within known constraints.
- `Overkill`: Y resolves X with avoidable cost or complexity disproportionate to the need.
- `Misaligned`: Y addresses a symptom or different outcome while leaving X unmet.
- `Premature`: The case for Y depends on unverified future requirements.

### Evidence States

- `CONFIRMED`: Available evidence supports the need and, when present, the mechanism within stated scope. Without Y, confirm the outcome while leaving the solution open.
- `INFERRED`: A plausible conclusion relies on an identified assumption or proof still needed.
- `REJECTED`: Evidence establishes a bounded reason the need or proposed mechanism fails; state the scope and conditions of rejection.
- `UNRESOLVED`: A material ambiguity or evidence gap prevents a supported conclusion.

Assign evidence states only after meaning is confirmed; awaiting user confirmation remains a pending proposal, not an `UNRESOLVED` assessment. State evidence boundaries explicitly: absence of proof identifies a gap, never a fabricated proof or an automatic rejection of a feature.

### Search Budget & Delegation

- Start with narrow docs/code searches and stop when enough evidence supports framing or identifies a load-bearing gap. Route broad mapping or production research (via /recon or /scout) rather than expanding inquiry indefinitely.
- Inspect localized scope directly. When broad inquiry is required within scope, pre-scout anchors and delegate disjoint slices with exact boundaries, discovered anchors, relevant rubric, and the sub-report contract: intent IDs, evidence pointers, supported claims, gaps, and dependencies. Reconcile reports before concluding.

## Canonical Output Contract

Use one Framing Dossier across the confirmation exchange and final evaluation.

### Intent Proposal & Confirmation

```markdown
# Framing Dossier: <Topic>

**I1 — <X via Y, or X if Y is absent>**
Source: <Explicit request or inferred interpretation, with its source>
Meaning: <Desired outcome, requested mechanism if present, and relevant scope>

<Initially repeat for each independent intent using stable IDs; on revision, include only affected intents awaiting confirmation.>

Is this what you mean?
```

Localize the short confirmation question to the caller. Present proposal and confirmation together, then halt immediately; evaluate suitability only after intent confirmation.

### Final Evaluation

```markdown
# Framing Dossier: <Topic>

**I1 — <X via Y, or X if Y is absent> · CONFIRMED/INFERRED/REJECTED/UNRESOLVED**
<Short-to-medium rationale: evidence, scope/conditions, practical trade-off, and load-bearing gap where relevant.>

<Repeat for each intent whose meaning is confirmed; choose one evidence state per intent.>

Dependencies: <Cross-intent effects and affected IDs. Omit when none.>
```

### Routing

- An intent depends on unknown repository capabilities → (via /recon).
- An intent needs production precedent or failure-mode evidence → (via /scout).
- A symptom or latency problem needs causal investigation → (via /diagnose).
- A confirmed intent has unresolved requirements or trade-offs → (via /clarify).
- An outcome needs a solution or a direction decision → (via /architect-decision).
- A supplied candidate needs empirical proof → (via /spike).
- A supported direction is settled and accepted for file-impact planning → (via /changeset).

## Execution Protocol

1. Ingest the request and confirmed session context; inspect targeted docs/code to propose independent intents and their sources.
2. Present the proposal and short confirmation question in one turn; halt before suitability evaluation.
3. Incorporate confirmation or corrections. Re-propose only affected intents; retain unchanged confirmations and halt for any revised meaning.
4. Evaluate confirmed intents using the rubric and grounded evidence. Keep unconfirmed meanings pending without suitability claims.
5. Present the final dossier with per-intent evidence states and any necessary routes, then halt. Further user clarification may reopen only affected conclusions.
