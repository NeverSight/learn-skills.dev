---
name: golang-review
description: "Review Go against evidence-backed rules for bounds, APIs, concurrency, errors, security, tests, and rollout. Use for Go diffs, PRs, branches, modules, or backend protos."
---

Review one axis: whether a Go diff follows [RULES.md](RULES.md) and applicable language contracts. Catalog rules carry aggregate support; version findings cite `/golang` official contracts, not taste.

Run standalone or inline as the **golang hat** in `/review`. Reviewer lanes still require explicit delegation or `/swarm`.

## Exclude

- Anything target `golangci-lint` config already enforces.
- Generic style without catalog/version-contract backing.
- Frontend, vendored, and generated `*.pb.go`, `*_pb.go`, `*.connect.go`, `@generated`/`DO NOT EDIT`.
- Catalog debate; submit feedback rather than invert a rule.

## Procedure

1. **Scope:** diff fixed point to HEAD. Inspect Go/proto plus `go.mod`/`go.work` when toolchain may change. Read `.golangci.yml`; exclude enabled lint rules.
2. **Classify:** proto/API, public SDK/library, handlers, Temporal, controllers, tests, config/rollout, tenant security, concurrency/lifecycle.
3. **Load:** matching [RULES.md](RULES.md) and `/golang` domain files: PROTO-API, CONCURRENCY, ERRORS, TESTING, TEMPORAL, SECURITY, ROLLOUT, STRUCTURE, CONTROLLERS. For Go 1.27 generic methods, compatibility, or leak profiling, load [GO-1.27.md](../golang/GO-1.27.md). Apply in-scope S/A rules, clear B violations, and only plain C/D violations; gate release contracts by module version/surface.
4. **Check tensions:** positive bool versus fail-closed, enum subset, keepalive, filters. Context decides.
5. **Report:** rule/contract id, `file:line`, behavior, required change, priority. Hat limit 400 words; standalone stays concise and sourced.

## Severity

- **P0:** fail-open security, unsafe tenant egress, plaintext secret, progress before durable processing, unversioned live-Temporal break.
- **P1:** other S/A violation: unbounded tenant growth, raw public errors, missing staged removal, mocked integration claim, or Go 1.27 syntax above supported floor.
- **P2:** B violation; judgment-call S/A; generic-method interface/reflection conflict; clean leak profile claimed as proof.
- **P3:** C/D wording/polish.

Confirmed bugs remain P0/P1 regardless of effort.

## Output

Only diff-introduced, user-impacting, actionable, PR-ready findings: What, catalog/contract-backed Why, Suggested fix, One-shot prompt. If clean:
`APPROVED -- <domains checked>, no catalog or version-contract violations.`
