---
name: vibe-verify
description: Collect proportionate evidence for an executable change and limit completion claims to what it proves. Use for implementation completion or explicit verification, not planning or explanation.
---

# Vibe Verify

Load named skills through the host mechanism; call the Skill tool when exposed.
Do not reload an active skill.

## Authority

- **Verification only:** run/inspect evidence without changing code, tests,
  configuration, fixtures, or external systems to make checks pass. Use this mode
  when asked only whether existing work is correct.
- **Implementation finishing:** repair an authorized in-scope cause exposed by
  verification, then rerun the affected check.

## Assertions

Recover the smallest observable assertions from the request and established
in-scope contracts, using repository evidence, tests, types, and the owning
boundary. Newly added tests cannot independently authorize new behavior. Include
negative assertions when accepted behavior or policy requires them; do not invent
UX, authorization, idempotency, data, or deployment policy. Report missing policy
as an unverified boundary. Match evidence to risk and coupling.

## Evidence

| Type | Proves |
| --- | --- |
| structural | types, lint, build, packaging, diff scope |
| focused executable | changed assertion and regression behavior |
| runtime interaction | rendering, input, timing, wiring, side effects |
| trusted boundary | allow/deny/deduplicate/persist/reject policy |
| external/deployed | real provider, credentials, migration, infrastructure, production |

Use the cheapest evidence that directly proves each assertion; combine types
only as needed and run focused checks first. Exercise representative API/CLI
inputs and selected UI states when static evidence is insufficient. For bug
fixes, rerun the original red-capable loop; without one, state the confidence
limit and invoke `vibe-debug` when causal investigation is authorized. Inspect
the final diff for scope drift, generated artifacts, debug code, and bypasses.

## Failure and cost

Apply the authority mode above. Stop at missing product decisions, unavailable
external state, new authorization, or scope expansion.

When verification requires new test infrastructure or unrelated environment
repairs, or harness adjustments repeat without new behavior evidence, reassess
the next step against the original assertions. Prefer cheaper direct evidence;
continue proportionate, authorized harness repairs that unlock necessary checks.
Prior effort does not justify more work. If no adequate in-scope method remains,
report the limit and seek agreement for concrete scope expansion. Never weaken
necessary acceptance or mark unverified behavior as passed to contain cost.

## Claim

- **Implemented:** code/config changed.
- **Locally verified:** relevant local evidence passed.
- **Externally provisioned:** required external configuration exists.
- **Production verified:** deployed behavior was exercised in production.

Keep claims within the observed state. Mark checks passed, failed, not run,
unavailable, or blocked; report decisive evidence and material unverified
boundaries. On actual agent transfer invoke `vibe-handoff`.
