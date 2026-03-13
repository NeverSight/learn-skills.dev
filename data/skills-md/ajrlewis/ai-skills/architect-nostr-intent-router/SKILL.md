---
name: architect-nostr-intent-router
description: Use when project requirements mention Nostr but the right NIP profile is unclear; pair with architect-stack-selector and addon-nostr-nip-profile-selector.
---

# Architect: Nostr Intent Router

Use this skill when a project needs Nostr features and you must detect protocol requirements, select NIPs, and route to the right reusable skills.

This is a protocol control-plane architect skill. It should be combined with exactly one infrastructure base architect (for example `architect-nextjs-bun-app`).

## Compatibility

- Best with `architect-stack-selector`.
- Usually paired with `addon-nostr-client-nextjs` and `addon-nostr-nip-profile-selector`.
- Optional pairings based on intent: `addon-nostr-key-custody`, `addon-nostr-nip23-longform`, `addon-nostr-nip-sync-lock`.

## Inputs

Collect:
- `NOSTR_INTENTS`: capabilities requested by user (for example `login`, `feed`, `publish`, `longform`, `dm`, `relay-policy`, `key-custody`).
- `NIP_CONSTRAINTS`: explicit required/forbidden NIPs if provided.
- `CLIENT_MODE`: `social-client` | `longform-publisher` | `dm-client` | `custom`.
- `LEGACY_COMPAT`: `yes` | `no` (default `no`).
- `NIP_LOCK_POLICY`: `required` | `optional` (default `required` in production-default).

## Intent To NIP Routing

Use this mapping as the starting point and justify deviations:

- identity and baseline events:
  `1`, `19`
- extension signer login:
  `7`
- relay list policy and relay preferences:
  `65`
- short note threading/replies:
  `10`
- reactions:
  `25`
- URI addressing / sharing:
  `21`
- long-form articles:
  `23`
- encrypted DM mode:
  `17`, `44`, `59`

Legacy rule:
- Exclude legacy cryptography NIPs by default unless `LEGACY_COMPAT=yes` with documented reason.

## Skill Routing Rules

1. Always add:
- `addon-nostr-client-nextjs`
- `addon-nostr-nip-profile-selector`

2. Add by detected intent:
- `longform` or `kind 30023` -> `addon-nostr-nip23-longform`
- `key-custody`, `private keys`, `local signing fallback` -> `addon-nostr-key-custody`
- `sync latest nips`, `nip lockfile`, `spec pinning` -> `addon-nostr-nip-sync-lock`

3. Client mode defaults:
- social feed/timeline intent -> `social-client`
- publishing essays/journals intent -> `longform-publisher`
- direct message intent -> `dm-client`
- mixed or unusual protocol requirement -> `custom` with explicit NIP set

4. If NIP requirements are ambiguous:
- choose minimal profile first
- mark ambiguous capabilities in decision log
- require explicit human confirmation before adding risky legacy or weakly specified protocol features

## Required Outputs

Produce:
```text
docs/nostr/NIP_REQUIREMENTS.md
docs/nostr/NIP_DECISIONS.md
```

`NIP_REQUIREMENTS.md` must contain:
- detected intents
- required NIPs
- optional NIPs
- excluded NIPs and why
- selected client mode

`NIP_DECISIONS.md` must contain:
- decision IDs
- alternatives considered
- tradeoffs and residual risks
- resulting skill composition

## Output Template

```text
Detected intents:
- <intent>

Selected client mode:
- <social-client|longform-publisher|dm-client|custom>

Selected NIPs:
- required: <list>
- optional: <list>
- excluded: <list + rationale>

Selected skills (ordered):
1) <base architect>
2) architect-nostr-intent-router
3) addon-nostr-client-nextjs
4) addon-nostr-nip-profile-selector
5) <other nostr add-ons as needed>

Justification summary:
- <why each non-trivial NIP/skill decision was chosen>
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Do not guess broad NIP support without explicit product intent.
- Keep NIP set minimal and capability-driven.
- Treat legacy compatibility as explicit risk acceptance.
- Ensure NIP profile docs, code profile, and lockfile strategy are consistent.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f docs/nostr/NIP_REQUIREMENTS.md
test -f docs/nostr/NIP_DECISIONS.md
rg -n "Selected client mode|required|optional|excluded" docs/nostr/NIP_REQUIREMENTS.md
rg -n "DEC-|tradeoff|risk|composition" docs/nostr/NIP_DECISIONS.md
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
