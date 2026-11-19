---
name: prove-it
description: Adversarially verify claims that code, fixes, tests, CI, deployments, logs, or systems are correct, complete, healthy, or safe to merge. Use when asked to prove, verify, validate, confirm, double-check, review the agent's own work, check whether a bug is actually fixed, or decide whether green signals justify a conclusion. Define a falsifiable claim, search for disconfirming evidence, verify outcomes rather than proxies, and return PROVEN, FAILED, NOT PROVEN, or BLOCKED. Do not trigger for ordinary implementation unless verification is requested.
---

# Prove It

Apply falsification before confidence. Do not ask only whether the evidence supports a conclusion. Ask what would make the conclusion false, then actively look for it.

## Preserve verification integrity

- Treat every prior conclusion, including your own, as a claim rather than evidence.
- Rebuild the case from artifacts: code, diffs, tests, commands, logs, runtime state, and external effects.
- Prefer raw artifacts and executable checks over narrative summaries. Do not demand infinite provenance: treat an artifact as what its metadata says unless provenance is part of the claim or a concrete inconsistency makes integrity doubtful.
- Keep verification read-only by default. Do not mutate production, destroy data, weaken controls, or broaden authorization to obtain proof.
- State the scope of any verdict. `PROVEN` means proven by the available checks within that scope, never formal correctness or universal safety.
- Freeze the claim and its acceptance criteria before inspecting the evidence. Do not make the claim easier after a check fails.
- Separate facts from interpretations. Use `KNOWN`, `INFERRED`, and `UNKNOWN` when ambiguity matters.

## 1. Define the claim

Turn vague language such as "fixed," "healthy," "done," or "safe" into a falsifiable statement.

Include the relevant behavior, target, environment, version, time window, and acceptance criteria. Split compound claims when their parts require different evidence.

Write:

```text
Claim: <what must be true>
False if: <observable contradiction>
Scope: <target, version, environment, and time window>
```

If the user did not provide enough detail, state the narrowest reasonable claim and expose the missing assumptions. Do not silently choose a convenient definition of success.

## 2. Try to break it

Before collecting more confirming signals, make a short falsification plan. Rank checks by how decisively they could distinguish a true claim from a false one. Execute meaningful safe checks when tools and evidence are available; do not merely recommend them.

Look for claim-specific counterexamples:

- **Code:** bypasses, boundary cases, stale reads, races, partial failure, swallowed exceptions, unsafe fallbacks, and changed requirements.
- **Tests:** whether the original failure is reproduced; assertions weakened; tests skipped; behavior mocked away; results hardcoded; exit codes ignored; timeouts merely increased.
- **CI:** required jobs absent, conditional paths not exercised, cached or stale artifacts, allowed failures, and a mismatch between the tested commit and claimed commit.
- **Logs:** wrong environment, service, instance, or time window; missing intervals; retries, warnings, restarts, rollback, duplicates, and evidence from only part of the system.
- **Deployments:** running artifact on every replica, migration state, background workers, dependencies, rollback status, and before/after runtime metrics.
- **Asynchronous work:** durable final state and real side effect, not only an accepted request, queued job, or HTTP 200.

When possible, run the original reproducer unchanged against both the failing and fixed versions. A new test that was never observed failing is weaker evidence because it may not represent the original defect.

Do not count implementation reasoning as verification. If you wrote the fix, start a fresh evidence pass from the frozen claim.

## 3. Verify the outcome, not the signal

Evaluate each important artifact through four gates:

1. **Target** — Is it from the claimed environment, version, instance set, and time window?
2. **Directness** — Does it observe the claimed outcome or only a proxy?
3. **Coverage** — Does it cover the relevant paths, states, replicas, and failure window?
4. **Discrimination** — Could this signal remain green while the claim is false?

Common non-equivalences:

```text
command succeeded != intended outcome occurred
tests passed != original behavior is correct
deploy job passed != every instance runs the new version
healthcheck returned 200 != the system is healthy
request returned 200 != asynchronous operation succeeded
no ERROR lines != no relevant failure occurred
agent confidence != evidence
```

Several weak proxies do not automatically add up to direct proof. Evidence also expires when the system, deployment, code, or relevant time window changes.

Surface contradictions before support. Never average conflicting evidence into "mostly fine."

## 4. Return a verdict with evidence

Use exactly one verdict:

- **PROVEN** — Direct evidence covers the defined claim, and meaningful falsification attempts found no contradiction.
- **FAILED** — Direct evidence contradicts the claim.
- **NOT PROVEN** — Available checks were performed, but evidence is missing, indirect, stale, or too narrow to establish the claim.
- **BLOCKED** — A required check cannot be performed because access, data, credentials, tools, environment, or testability is unavailable.

Do not use `BLOCKED` merely because the evidence already supplied is weak; perform accessible checks first. Do not use `NOT PROVEN` when direct contradictory evidence requires `FAILED`.

Choose the verdict in this order:

1. Return `FAILED` when direct evidence contradicts the claim.
2. Return `PROVEN` when the Target, Directness, Coverage, and Discrimination gates pass and executed falsification found no contradiction. Do not invent an unbounded hypothetical gap after the defined scope is covered.
3. Return `BLOCKED` when a specific required decisive check cannot be executed now because an attempted check or supplied fact establishes that its data source, access, tool, environment, or test path is unavailable.
4. Otherwise return `NOT PROVEN` for evidence that is merely insufficient, indirect, stale, or narrow.

Missing or omitted evidence alone means `NOT PROVEN`, not `BLOCKED`. If the sole reason proof is missing is that the necessary database, provider, production environment, credential, log source, or other dependency is explicitly unavailable, prefer `BLOCKED` and name the blocked check.

For a meaningful verification, prefer this compact structure:

```text
CLAIM
<falsifiable claim and scope>

VERDICT
<PROVEN | FAILED | NOT PROVEN | BLOCKED>

WHY
<decisive reason>

FALSIFICATION ATTEMPTS
- <check performed -> result>

EVIDENCE
- Supporting: <direct evidence, if any>
- Contradicting: <contradiction, if any>

GAPS
- <missing evidence, if relevant>

NEXT PROOF
1. <smallest decisive next check, if needed>
```

Keep simple cases shorter. Never end with vague success language such as "looks good," "should be fixed," or "probably healthy."

## Reject counterfeit proof

Flag verification bypasses when they hide the behavior under investigation, including `test.skip()`, `xit()`, ignored exit codes, removed or weakened assertions, empty catches, `|| true`, blanket suppressions, hardcoded results, unrelated mocks, and timeout increases without a reproduced timing cause.

These constructs are not universally forbidden. Treat them as evidence against the claim only when they bypass, conceal, or redefine the original acceptance criterion.
