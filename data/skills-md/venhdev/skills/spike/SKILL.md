---
name: spike
description: "Prove candidate solutions against original problem criteria through isolated experiments within a supplied direction and constraints."
disable-model-invocation: true
---

# spike — Solution Proof

## Operating Invariants

- **Scratch Boundary**: Author candidate logic, harnesses, fixtures, and proof artifacts only inside `.agents/scratch/`; leave production code and permanent tests untouched.
- **Working Tree Preservation**: Preserve existing changes and unrelated scratch artifacts. Inspect the integration seam read-only and use isolated copies where execution needs modifications.
- **Problem Fidelity**: Ground assertions in the original problem and acceptance criteria. Keep those assertions fixed across baseline and candidate runs; distinguish isolated capability proof from proof of a production fix.
- **Direction Boundary**: Explore finite, evidence-grounded alternatives within the supplied solution direction and constraints. Report a required direction change for a separate decision; never silently expand the search or force a GREEN outcome.
- **Sensitive Evidence & Environment**: Redact secrets before logging; never inspect secret files (`.env*`, `*.key`, `*.pem`). Ground harness runners and scratch datastores in `.agents/environment.md`; confine experiments strictly to `.agents/scratch/`.

## Domain Rubric

### Input and Proof Target

- Accept a problem or RED signal, a candidate solution, and a solution direction with constraints established by the input or confirmed context. The problem may be inferred or vague; derive a testable criterion from available evidence and record assumptions. A candidate can establish its own direction when that boundary is unambiguous; keep unstated architectural choices open.
- Identify the relevant integration seam, expected outcome, original failure mechanism if known, and the principal uncertainty requiring proof. If the input/context cannot establish the test criterion or permitted direction, report `UNRESOLVED` with the needed input before exploring alternatives.
- Use the original symptom to define a fix assertion. For a new capability, use its required behavior as the assertion; choose correctness, compatibility, concurrency, parity, or resource measurements only when relevant to that requirement.

### Baseline and Candidate Experiments

- Establish baseline RED when feasible, then run the same assertion against the candidate to seek GREEN. If original failure cannot be reproduced, preserve that gap in any defect-fix claim.
- Exercise the actual seam or a faithful isolated copy. Declare mock boundaries and omitted integration behavior; mock-only GREEN proves only the modeled scope and cannot confirm an unverified production fix.
- Minimize the harness while retaining load-bearing inputs, environment, state transitions, and boundary cases. Make setup and execution reproducible with commands and sanitized fixtures.
- For intermittent or concurrent behavior, control seeds, clocks, and interleavings where possible; record failures and repetitions rather than accepting a single passing run.
- Use each failure to choose a grounded alternative within direction. Stop at complete proof, exhaustion of relevant permitted alternatives, a runtime/access blocker, or evidence that the direction must change.

### Conclusion States

- `CONFIRMED`: Empirical evidence meets the original criteria in the stated tested scope. Confirming a defect fix also requires a faithful baseline failure and candidate GREEN on the same assertion.
- `INFERRED`: Reasoning or partial execution supports the candidate, but the original criteria lack complete empirical proof; state the exact gap.
- `REJECTED`: Bounded experiments show the candidate or direction fails the criteria after relevant permitted alternatives were exhausted. Limit the conclusion to tested alternatives and conditions; leave global impossibility unclaimed.
- `UNRESOLVED`: Missing direction, criteria, runtime, access, or other prerequisites prevent a defensible proof or rejection.

## Canonical Output Contract

Produce one compact report with enough evidence to replay the proof and assess applicability. Retain sanitized scripts and logs in scratch when useful; summarize decisive observations in the report.

```markdown
# Solution-Proof Report: <problem / candidate>

State: <CONFIRMED | INFERRED | REJECTED | UNRESOLVED>
Conclusion: <what the candidate demonstrably solves, may solve, failed to solve, or leaves unknown>
Original criteria: <problem-grounded assertions>
Direction and constraints: <supplied boundary and assumptions>
Integration seam: <module/interface/runtime boundary>
Evidence: <scratch paths and commands; baseline and candidate results for the same assertion>
Conditions and proof limits: <tested environment, substitutions, missing proof, applicability limits>

## Alternatives *(omit if none were explored)*
<candidate -> decisive observation -> retained or eliminated within direction>
```

### Routing

- The proven solution is accepted and needs file-impact planning → (via /changeset).
- A missing requirement prevents meaningful proof → (via /clarify).
- Success requires changing the supplied direction → (via /architect-decision).
- Missing toolchain or unready test datastores prevent experiment execution → (via /env-doctor).

## Execution Protocol

1. Ground the problem, candidate, direction, constraints, and seam. Define the original assertion and evidence needed to prove it.
2. Build a minimal scratch experiment and run the baseline when possible. Run the candidate against the same criterion and relevant boundaries.
3. Inspect failures and explore grounded alternatives within direction until proof, bounded exhaustion, a blocker, or a required direction change. Record the observations that justify stopping.
4. Present the solution-proof report with its state, conditions, and limits; verify production files remain unchanged and preserve useful sanitized proof artifacts.
