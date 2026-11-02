---
name: architect-decision
description: "Frame design constraints and converge architectural evidence into a supported direction, provisional candidate, bounded rejection, or unresolved decision."
disable-model-invocation: true
---

# architect-decision — Design Direction & Architectural Decision

## Domain Rubric

### Framing Axes

Establish grounded direction before implementation. Resolve irrelevant axes to `N/A` with a reason; resolve material axes before settling the choice:

- **Problem Boundary**: Operational outcome and observable success criteria, separate from the requested mechanism.
- **Hard Constraints**: Non-negotiables eliminating approach families: time, money, compliance, data safety, platform, or team capacity.
- **Frozen Surface**: Contracts, persisted data, APIs, and relied-on behavior that must survive unchanged.
- **Reversibility Class**: One-way doors foreclose undo; two-way doors permit reversal without external cost. Identify concrete rollback exposure.

### Framing Discipline

- **Inference Before Inquiry**: Ask about business consequences, infer technical constraints from evidence, and offer grounded defaults for confirmation.

  ```text
  Bad:  "Expected throughput? What p99 latency budget?"
  Good: "When an order fails, does it lose revenue or delay processing?"
        (Derive the durability requirement and offer it as a default.)
  ```

- **Zero-Ambiguity Fast Path**: Lock axes already fixed by the request and evidence; ask only about unresolved choices.
- **Framing Payload**:

  ```text
  ### Axis<N>: <Framing Axis>
  Bottleneck: <Unresolved tension shaping the design space>
  [A] <Option> — Trade-off: <advantage> vs. <disadvantage>
  [B] <Option> — Trade-off: <advantage> vs. <disadvantage>
  Default: [Option] because <grounded rationale>
  ```

### Convergence Criteria

Score candidates against all five:

- **Problem Closure**: Resolve the framed outcome rather than relocate it downstream.
- **Constraint Fitness**: Disqualify candidates violating a hard constraint regardless of other merits.
- **Precedent Backing**: Assess actual production precedent at disclosed scale and named failure modes; distinguish production evidence from examples or claims.
- **Reversibility**: Quantify rollback exposure and prefer two-way doors when other criteria hold.
- **Evidence Strength**: Support load-bearing claims with code pointers, verified citations, or measured results. Resolve discoverable repository facts directly; reserve open gaps for external unknowns and unmeasured runtime risks.

### Convergence & Evidence States

- **One Direction, When Supported**: Choose one approach when evidence permits; break ties by reversibility, narrower frozen surface, then simpler established precedent. Keep a provisional candidate or unresolved decision when proof is missing.
- **Adversarial Review**: State the strongest sourced counter-case and the observable condition that would change the conclusion. Revise when the counter-case wins a convergence criterion.
- `CONFIRMED`: Enough evidence supports the architectural choice within stated conditions; this state neither declares implementation GREEN nor authorizes mutation.
- `INFERRED`: A provisional candidate is supported by reasoning but depends on named assumptions or proof.
- `REJECTED`: Evidence supports a bounded no-build conclusion because viable candidates fail outcome or constraints; name its conditions and justification.
- `UNRESOLVED`: Material uncertainty prevents selecting a supported direction or candidate.

Use missing proof to identify evidence work; reserve rejection for supported failure, not uncertainty alone.

### Search Budget & Delegation

- Pre-scout source, schemas, and governing decisions; inspect localized scope directly and stop once load-bearing claims are supported or gaps identified.
- Delegate only when multiple layers or packages exceed focused inspection capacity. Seed disjoint slices with exact boundaries, discovered anchors, framing axes, candidates, rubric, and the sub-report contract: evidence pointers, criterion findings, counter-evidence, and gaps. Reconcile the reports against the locked frame.

## Canonical Output Contract

```markdown
# Architectural Decision: <Problem Slug>

## Decision & Boundaries
- **State**: <CONFIRMED | INFERRED | REJECTED | UNRESOLVED>
- **Conclusion**: <Supported direction, provisional candidate, justified bounded no-build, or what prevents selection>
- **Outcome**: <Operational outcome and observable success criteria>
- **Conditions**: <Evidence and scope under which the conclusion holds>
- **Boundaries**: Hard constraints: <constraints> | Frozen surface: <contracts/paths/APIs> | Reversibility: <class and exposure>

## Solution Mechanics
<Use a minimal comparison, interface boundary, state flow, or diagram when it explains a candidate. For rejection, state the disqualifying constraint or demonstrated failure. Omit if no candidate or rejection mechanism can be supported.>

## Cost & Falsification
- **Accepted Cost**: <Concrete trade-off; omit if no direction or candidate exists>
- **Counter-Case**: <Strongest sourced challenge> — changes conclusion when <observable condition>; omit if no defensible sourced counter-case exists, and record any decision-affecting review limitation under Open Gaps instead of inventing evidence
- **Open Gaps**: <External unknowns or runtime risks and what settles them; omit when none>
```

Separate state from its conditions and substantive conclusion; present one deterministic decision dossier, not a fixed routing menu.

### Routing

- A candidate needs viability proof; carry the problem, success criteria, candidate, and direction constraints → (via /spike).
- A supported direction is settled and accepted; carry evidence, boundaries, and acceptance criteria → (via /changeset).

## Execution Protocol

### Phase 1: Grounded Framing & Evidence

1. Pre-scout architectural anchors and evaluate framing axes against the request and source evidence.
2. Present unresolved axes with grounded defaults; batch independent axes and halt for the user's response. Take the fast path when already settled.
3. Ingest answers and inspect newly exposed paths. Invalidate only axes and claims affected by requirement shifts; preserve unchanged context.
4. Gather criterion evidence within the search budget, using grounded delegation only when necessary.

### Phase 2: Convergence & Delivery

1. Score candidates, apply hard constraints and tie-breaks, then run adversarial review.
2. Select the evidence state and substantive conclusion; scope conditions and gaps independently from the state.
3. Deliver the dossier with context-appropriate routing and halt for the user's decision. Keep this workflow read-only; leave code, experiments, and workspace mutation to separately invoked workflows.
   - End without a handoff when the bounded no-build conclusion needs no further action.
