---
name: fable-simulator
description: "Verify complex code changes against independent mathematical oracles, derived specifications, headless browser environments, and isolated sandbox states. Use when deriving independent verification oracles, testing algorithms against reference models, verifying UI with headless browsers, or testing state transitions in sandboxes — even if the user does not explicitly say \"fable-simulator\" (e.g. \"simulate this workflow\", \"verify with an independent oracle\", \"headless browser check\", \"derive a test oracle\"). Do NOT use for simple unit test runs (use fable-verify)."
version: 1.3.0
pack: system
inputs:
  - verification_target
requires:
  - independent_oracle
produces:
  - oracle_evidence
  - causal_verification_matrix
gates:
  - oracle_independent
  - untracked_files_preserved
fallback: fable-verify
mutatesWorkspace: false
parallelSafe: false
neural_links:
  precursors:
    - fable-verify
  continuations:
    - fable-verify
    - fable-review
  lateral_peers:
    - fable-verify
  recovery: fable-recover
---

# Fable Simulator

Create an independent model of expected behavior and compare it with the candidate without pretending the simulation itself is production evidence.

## Mission
Simulation is useful when ordinary tests risk sharing the same assumptions as the implementation, when a UI/agent flow needs controlled playthrough, or when failure injection can expose paths that are hard to reproduce safely.

The Skill must preserve a hard boundary between **simulated/oracle evidence** and **real runtime verification**.

## Activate When
- an algorithm/rewrite needs an independently derived oracle;
- a contract is implicit across callers and needs reconstruction;
- UI/agent state transitions benefit from scripted playthrough/failure injection;
- testing destructive/rare conditions safely requires a model/sandbox;
- differential testing between two independent implementations is valuable.

## Do Not Activate When
- normal tests/runtime evidence already proves the claim cheaply;
- the proposed oracle is derived from the same code/assumptions under test;
- simulation would be reported as proof that an external production system actually behaved that way.

## Simulation Classification
| Mode | Independence requirement |
| --- | --- |
| Golden fixtures | fixture expected outputs come from trusted contract/observations |
| Reference implementation | independently written/maintained logic |
| Differential provider/model | separate implementation/model with blinded oracle |
| State-machine simulation | transitions/invariants defined from product contract |
| Failure injection | controlled faults with explicit modeled assumptions |
| UI playthrough | browser actions + observable DOM/network/runtime evidence |

## Protocol
### Stage 1 — Define the claim and oracle independence
State what candidate behavior is being checked and why the oracle does not simply repeat candidate logic.

List shared assumptions. If a shared assumption could cause both candidate and oracle to be wrong identically, record that coverage gap.

### Stage 2 — Derive contract from independent sources
Use public interfaces, callers, specs, historical golden outputs, primary docs, or separately maintained reference behavior. Avoid reading implementation details solely to recreate the same algorithm.

### Stage 3 — Build representative and edge corpus
Include normal, boundary, invalid, stateful, adversarial, and failure cases relevant to the claim. Preserve user/untracked workspace files and run in isolated temp/sandbox locations where possible.

### Stage 4 — Execute candidate and oracle separately
Capture inputs, outputs, errors, side effects/state transitions, timing only when required, and tool/environment identity.

### Stage 5 — Compare semantically
Normalize only differences that the contract declares irrelevant. Do not normalize away a real behavioral difference just to reach zero diff.

For UI, compare causal rows:
`action → expected observable → actual observable → evidence`
not pixels alone unless pixel fidelity is itself the contract.

### Stage 6 — Triage divergence
A mismatch means one of:
- candidate wrong;
- oracle wrong/stale;
- contract ambiguous;
- normalization invalid;
- environment differs.

Do not automatically "fix candidate to oracle" until the source of truth is established.

### Stage 7 — Mark evidence scope
Report simulation/oracle evidence distinctly. Hand off to `fable-verify` for real runtime/package/environment proof where the claim requires it.

## Decision Rules
- An oracle copied from candidate implementation is self-confirming and invalid.
- A second LLM is not automatically an independent oracle if it receives the candidate answer or hidden expected output.
- Golden fixtures need provenance; unexplained fixtures can encode old bugs.
- UI screenshots without interaction/state evidence are weak for functional causality.
- Failure injection proves behavior under the modeled fault, not that real infrastructure fails exactly that way.
- Zero diff across a narrow corpus is not universal correctness; state coverage explicitly.
- Never modify/delete untracked user files to make simulation deterministic.

## Invariants
- Oracle independence and shared assumptions are explicit.
- Simulation evidence is labeled as simulation.
- Input corpus and normalization are reproducible.
- User/untracked workspace state is preserved.
- Divergence is diagnosed before deciding which side is wrong.
- Real-world claims receive real verification when required.

## Failure Taxonomy
### Tautological oracle
Oracle reuses candidate implementation/answer. Redesign independently.

### Stale oracle
Reference behavior no longer matches accepted contract. Re-ground oracle before judging candidate.

### Ambiguous contract
Candidate and oracle differ but both are plausible. Route to plan/research rather than choose arbitrarily.

### Over-normalization
Comparison strips a meaningful difference. Narrow normalization to contract-declared irrelevant fields.

### Simulation/reality confusion
Simulated pass is used as production/runtime proof. Downgrade claim and hand to verify/run.

### Workspace contamination
Simulation writes into real user state. Move to isolated sandbox and restore owned mutations only.

## Anti-Patterns
- implementing the oracle by copying candidate code;
- giving an LLM oracle the expected answer;
- demanding 100% zero diff without representative corpus reasoning;
- treating screenshots as complete UI verification;
- normalizing every mismatch until green;
- claiming external service behavior from a fake;
- deleting untracked files to reset simulation;
- changing candidate immediately on any oracle mismatch.

## Simulation Packet
```text
Claim:
Oracle type/source:
Independence + shared assumptions:
Corpus/failure injections:
Candidate environment:
Comparison/normalization:
Divergences:
Oracle validity decision:
Simulation verdict:
Real evidence still required:
```

## Completion Criteria
Simulation completes when:
- oracle independence is credible and documented;
- corpus covers the important contract dimensions;
- candidate/oracle comparisons are reproducible;
- divergence is classified instead of blindly resolved;
- workspace remains safe;
- evidence is labeled narrowly and handed to real verification where needed.

## Progressive Resources
- Deep guide: `references/oracle-independence-and-simulation-boundaries.md`
- Existing guide: `references/oracle-derivation-guide.md`
- Example: `examples/independent-oracle-verification.md`
