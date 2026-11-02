---
name: env-doctor
description: "Audit runtime toolchains, verify container service health, seed hermetic test primitives, and execute safe local remediation."
---

# env-doctor — Execution Environment Diagnostics & Remediation

## Operating Invariants

- **Idempotent Local Boundary**: Confine remediation strictly to project-scoped actions (declared dependency sync, local service boot, test datastore migration, synthetic test secrets); forbid system-wide mutations (`sudo`, `brew`), host PATH tampering, or remote secret fetching. Halt with `UNRESOLVED` for port collisions, missing daemons, or destructive actions.
- **Zero-Secret Exposure**: Never inspect or copy production secret files (`.env*` except `.env.example`); inject deterministic mocks into `.env.test` or environment stubs.
- **Manifest SSOT Grounding**: Read `.agents/environment.md` as the authoritative specification. Treat omissible sections (services for pure libraries, external datastores) as `PASS` when absent.
- **Adaptive Invocation Output**: Render the full Canonical Output Contract when invoked by a human; output only a single-line Micro-Summary token (`READY` or `UNRESOLVED: <blocker>`) when called by an autonomous runner.

## Domain Rubric

### 1. Dimension Audit & Probing Discipline
Cross-reference declared manifests against host runtimes and execution wrappers (`pnpm`, `cargo`, `uv`). Execute declared service readiness probes (socket, HTTP `/healthz`, database ping) with exponential backoff (max 15s); forbid treating process state (`Up`) as readiness. Verify test datastore migrations, fixtures, and synthetic `.env.test` stubs.

## Canonical Output Contract

```markdown
# Environment Health Report: <Scope> · <READY | STAGED | UNRESOLVED>

Basis: .agents/environment.md

| Dimension | Declared / Target | Active / Detected | State |
| :--- | :--- | :--- | :--- |
| **Toolchain** | <Target runtime version> | <Active version / wrapper> | <PASS | FAIL> |
| **Services** | <Declared services or N/A> | <Probe outcome or Standalone>| <PASS | FAIL> |
| **Datastore** | <Target test datastore> | <Migration & seed status> | <PASS | FAIL> |
| **Test Stubs** | <Test env / secrets> | <Stubs presence (.env.test)> | <PASS | FAIL> |

*(omit if clean)* ## Applied Remediation
- **[<Auto | Staged>] <Action>**: <Command and outcome or pending approval>

*(omit if READY)* Gap: <Root cause blocker and required human action.>
```

*Autonomous Micro-Token Contract*:
```text
READY | runtime: <version> | services: <healthy|standalone> | fixtures: verified
```
*(On failure, output `UNRESOLVED: <single-sentence blocker>`)*.

### Routing

- Environment is READY, proceed to task decomposition → (via /split-tasks).
- Environment is READY, proceed to code implementation → (via /forge).
- Environment is READY, proceed to root-cause diagnosis → (via /diagnose).
- Missing service architecture requires design decision → (via /architect-decision).

## Execution Protocol

1. Read `.agents/environment.md` and probe declared host tools, runtimes, services, and fixtures. Short-circuit to `READY` if all pass.
2. Execute safe auto-remediations (boot declared services, sync dependencies, run test datastore migrations/fixtures). Re-probe health; report `READY` or halt turn with `UNRESOLVED` on blockers.
