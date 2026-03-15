---
name: addon-nostr-nip-sync-lock
description: Use when you need a reproducible NIP lockfile synced from official specs; pair with addon-nostr-nip-profile-selector.
---

# Add-on: Nostr NIP Sync Lock

Use this skill when a project needs an auditable, refreshable snapshot of selected NIP specs.

## Compatibility

- Best with `addon-nostr-nip-profile-selector`.
- Works with any Nostr project regardless of runtime stack.

## Inputs

Collect:
- `NIP_LIST`: comma-separated list (default from selected profile).
- `LOCKFILE_PATH`: default `docs/nostr/nips.lock.json`.
- `SOURCE_REF`: default `master`.

## Integration Workflow

1. Add files:
```text
scripts/nostr/sync_nips_lock.py
docs/nostr/nips.lock.json
```
- Copy and adapt this skill's bundled script:
- `scripts/sync_nips_lock.py`
- Place the adapted result in the target project at `scripts/nostr/sync_nips_lock.py`.

2. Generate lock:
```bash
python3 scripts/nostr/sync_nips_lock.py --nips 1,7,19,21,23,65 --out docs/nostr/nips.lock.json --ref master
```

3. Add CI check:
- Regenerate lock in CI and fail when committed lock is stale.

4. Add review rule:
- Changes to `docs/nostr/nips.lock.json` require human review (`CODEOWNERS`).

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Pull NIP sources only from the official `nostr-protocol/nips` repository.
- Keep lock deterministic and machine-readable.
- Never auto-merge lock updates without human review.
- Treat deprecated/legacy NIP detections as explicit review items.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f scripts/nostr/sync_nips_lock.py
python3 scripts/nostr/sync_nips_lock.py --nips 1,7,23 --out /tmp/nips.lock.json --ref master
test -f /tmp/nips.lock.json
```
Manual checks:
- Lockfile includes URLs and hash for each selected NIP.
- Lockfile changes are visible in PR diff and summarized in review bundle.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
