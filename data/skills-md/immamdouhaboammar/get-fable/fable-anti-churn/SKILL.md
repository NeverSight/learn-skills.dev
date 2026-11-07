---
name: fable-anti-churn
description: Prevent duplicate agent actions, infinite retry loops, and unverified churn across all lifecycles. Reuses matching accepted evidence, enforces typed invalidations for changed work, gates deterministic local failures for local repair, and manages candidate promotion readiness with zero token overhead.
version: 1.12.0
pack: proof
inputs:
  - action_event
  - prior_receipts
requires:
  - action_identity
produces:
  - decision_receipt
  - evidence_acceptance
gates:
  - zero_duplicate_churn
  - typed_invalidation_satisfied
fallback: fable-recover
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - get-fable
    - fable-execute
    - fable-tdd
  continuations:
    - fable-verify
    - fable-review
    - fable-heal
  lateral_peers:
    - fable-anti-slop-engineering
    - fable-prove-it
    - fable-judge
  recovery: fable-recover
---

# Fable Anti-Churn

## Purpose

`fable-anti-churn` is the authoritative duplicate-work and evidence-reuse prevention engine in get-fable. Powered by both a native Rust engine (`crates/fable-anti-churn`) and local CLI scripts, it cryptographically fingerprints work requests (RFC 8785 JCS + SHA-256), tracks reservation receipts, reuses identical prior passing evidence, blocks duplicate actions, halts repeated deterministic failures, and validates promotion proof with sub-millisecond execution. Keep material progress separate from churn. Material output can prove progress; it is not a churn dimension.

## When to Use

- Before dispatching repetitive test commands, build scripts, or static analysis tools.
- Before spawning subagents, background workflows, or external tool calls.
- When an action or command fails deterministically, requiring local repair rather than blind retries.
- When evaluating candidate promotion gates (package integrity, test passing, authority verification).
- Across all lifecycle hooks (`SessionStart`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`).

## When NOT to Use

- NOT to cancel or terminate the entire user task — gates only the specific duplicate local action.
- NOT as a substitute for valid code changes; once code changes, compute a typed invalidation (`candidate_changed`, etc.) to run anew.
- NOT to bypass real human authorization or security boundaries.

## Inputs

- `action_event`: Canonical JSON payload containing `action_kind`, `action_scope_digest`, `requirements_digest`, `candidate_digest`, and environmental hashes.
- `prior_receipts`: Historical receipts ledger in NDJSON format (`.fable/anti-churn/receipts.ndjson`).
- `core_policy`: Policy configuration containing intervention level thresholds and retry budget parameters.

## Expected Outputs

- `decision_receipt`: Cryptographically signed receipt with 35 canonical fields, `decision`, `reason_code`, and `evidence_digest`.
- `evidence_acceptance`: Stamped evidence acceptance record updating a pending reservation with verified outcome.
- `churn_status`: Real-time ledger status reporting total receipts, pending reservations, passing evidence, and blocked churn cycles.

## Procedure

1. **Fingerprint Work Identity:** Hash scope, requirements, candidate patch, dependencies, policy, and evaluator using RFC 8785 canonical JSON and SHA-256.
2. **Consult Prior Ledger:** Scan `.fable/anti-churn/receipts.ndjson` for existing matching reservations or passing evidence.
3. **Evaluate Idempotency:**
   - If exact passing evidence exists without invalidation: emit `reuse_prior_evidence`.
   - If pending in-flight reservation exists: emit `block_this_local_action` (prevent race condition).
   - If deterministic local failure exists without workspace mutation: emit `local_fix_required`.
   - If work changed with valid typed invalidation: emit `allow_reexecution`.
   - If first equivalent action: emit `allow` and record reservation receipt.
4. **Execute & Record Outcome:**
   - On success: run `accept` to transition reservation to `pass`.
   - On local failure: record `local_failure` receipt to fence immediate duplicate execution.
5. **Enforce Hook Invariants:** Intercept lifecycle events to ensure zero unaccepted reservations or churn loops remain at turn completion.

## Decision Rules

- **ALLOW:** First equivalent action without prior reservation; reserves slot with pending receipt.
- **ALLOW_REEXECUTION:** Allowed re-run after consuming a valid, unconsumed typed invalidation.
- **ALLOW_WITH_ADVISORY:** Allowed when work identity is incomplete (rate advisory emitted).
- **REUSE_PRIOR_EVIDENCE:** Exact matching work has prior passing evidence; returns stored `evidence_digest` with zero token overhead.
- **LOCAL_FIX_REQUIRED:** Deterministic local failure detected; blocks execution until code is edited.
- **BLOCK_THIS_LOCAL_ACTION:** Duplicate pending action, invalid fanout, or changed work without typed invalidation.

## Tool Policy

- Read-only queries preferred for check and verification steps.
- Native Rust engine binary (`fable-anti-churn` or `get-fable-native anti-churn`) used for sub-millisecond execution.
- Direct NDJSON state file updates guarded by atomic filesystem locking (`fs2`).
- Never delete or corrupt historical receipts; maintain immutable append-only ledger.

## Evidence Requirements

- Validated receipts containing all 35 canonical fields and 0 prohibited keys.
- SHA-256 digests adhering to `sha256:[0-9a-f]{64}` format.
- Passing self-test corpus report confirming 23/23 scenario verifications.
- Verified absence of pending reservations before marking lifecycle phases complete.

## Failure Handling

- If `local_fix_required` or `deterministic_local_failure` is encountered: edit target source code to resolve the defect. Workspace mutation clears the failure lock.
- If invalidation is rejected: inspect invalidation target receipt and ensure reason code matches the changed field.
- If failure streak reaches 2: route to `fable-recover` to diagnose root cause before attempting code edits.

## Completion Criteria

- All open reservations transitioned to `pass` or explicit terminal outcome.
- Zero unresolved pending reservations in `.fable/anti-churn/receipts.ndjson`.
- State ledger passes `anti-churn verify` with 0 validation errors.
- Passing tests verified with fresh evidence matching current mutation generation.

## CLI Commands

```bash
# Evaluate an action event against receipts ledger
bun ./bin/get-fable.js anti-churn decide event.json

# Accept passing evidence for an open reservation
bun ./bin/get-fable.js anti-churn accept <receipt-id> <evidence-digest> [pass|local_failure]

# Quick zero-latency check if an action/command is duplicate
bun ./bin/get-fable.js anti-churn check --action-kind targeted_test --target src/core.ts --command "bun test"

# Verify receipts ledger integrity
bun ./bin/get-fable.js anti-churn verify

# Run native 23-fixture self-test corpus
bun ./bin/get-fable.js anti-churn self-test

# Check anti-churn status & metrics
bun ./bin/get-fable.js anti-churn status
```

## Lifecycle Hook Enforcement

1. **SessionStart**: Scan `.fable/anti-churn/receipts.ndjson` for open reservations or persistent local failure loops.
2. **PreToolUse (Bash / Agent)**: Compute action key. If duplicate without invalidation, intercept and block.
3. **PostToolUse (Write / Edit)**: Compute new candidate hash and clear local failure locks.
4. **PostToolUse (Bash Success)**: Invalidate failure tracking.
5. **PostToolUseFailure (Bash Failure)**: Detect deterministic local failure loops and block blind retries.
6. **Stop**: Verify no unsettled reservations or corrupted receipts before closing turn.

## Progressive Resources

- [Decisions & Receipts Architecture](references/DECISIONS-AND-RECEIPTS.md) — Comprehensive receipt schema and 35 canonical fields specification.
- [Threat Model](references/THREAT-MODEL.md) — Security boundaries, trust domains, and tampering prevention.
- [Privacy Policy](references/PRIVACY.md) — Prohibited fields and secret redaction enforcement.
- [Evaluation Protocol](references/EVALUATION.md) — 23-scenario verification matrix and baseline assertions.
- [Doctrine Review](references/doctrine_review.md) — Mathematical and architectural foundations of duplicate work prevention.
- [Claude Integration](references/CLAUDE-INSTALL.md) — Host lifecycle hook setup for Claude Code.
- [Codex Integration](references/CODEX-INSTALL.md) — Host lifecycle hook setup for OpenAI Codex.
- [Event Template](templates/EVENT_TEMPLATE.json) — Standard action event JSON template.
- [Receipt Template](templates/RECEIPT_TEMPLATE.json) — Canonical decision receipt JSON template.
