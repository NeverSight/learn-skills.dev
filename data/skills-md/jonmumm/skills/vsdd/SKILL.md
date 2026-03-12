---
name: vsdd
description: >
  Verified Spec-Driven Development (VSDD) — a rigorous AI-native engineering methodology
  that fuses Spec-Driven Development, Test-Driven Development, and adversarial verification
  into a single pipeline. Use when the user says "vsdd", "spec-driven", "verified spec",
  "adversarial review", "zero-slop", "full verification", "spec-first development",
  "build this properly with specs", or wants a rigorous spec → test → implement → verify
  workflow. Also use when asked for formal verification, mutation testing workflows, or
  adversarial code review as part of a development process.
---

# Verified Spec-Driven Development (VSDD)

Specs define *what*. Tests enforce *how*. Adversarial verification ensures *nothing was missed*.

## Pipeline Overview

```
Phase 1: Spec Crystallization ─── define the contract, verification strategy, adversarial spec review
    │
Phase 2: TDD Implementation ──── red → green → refactor, strict test-first discipline
    │
Phase 3: Adversarial Roast ────── Claude sub-agent tears apart spec fidelity, test quality, code quality
    │
Phase 4: Feedback Loop ────────── route flaws back to the right phase, iterate
    │
Phase 5: Formal Hardening ─────── mutation testing, fuzzing, static analysis, optional formal proofs
    │
Phase 6: Convergence ──────────── exit when adversary hallucinates flaws, mutation score ≥ 95%
```

Each phase is a gate. Do not advance until the current phase's exit criteria are met.

## Roles

| Role | Entity | Function |
|------|--------|----------|
| **Architect** | Human | Strategic vision, domain expertise, acceptance authority |
| **Builder** | Claude (primary) | Spec authorship, test generation, implementation, refactoring |
| **Adversary** | Claude (sub-agent, fresh context) | Hyper-critical reviewer. Zero tolerance. Fresh context every pass |

## Tracking

Track all VSDD artifacts in a local `vsdd/` directory at the project root:

```
vsdd/
├── spec.md          # Behavioral spec + verification strategy
├── review-log.md    # Adversarial review findings and resolutions
└── status.md        # Phase status and convergence tracking
```

Create `vsdd/` at the start of Phase 1. Update `status.md` at each phase transition.

## Phase Details

Each phase has detailed instructions in a reference file. Load the relevant reference when entering that phase.

| Phase | Reference | Load when |
|-------|-----------|-----------|
| **Phase 1: Spec Crystallization** | [references/phase1-spec.md](references/phase1-spec.md) | Starting a new VSDD cycle |
| **Phase 2: TDD Implementation** | [references/phase2-tdd.md](references/phase2-tdd.md) | Spec is approved, ready to write tests |
| **Phase 3-4: Adversarial Review & Feedback** | [references/phase3-4-adversarial.md](references/phase3-4-adversarial.md) | All tests green, ready for roast |
| **Phase 5-6: Hardening & Convergence** | [references/phase5-6-hardening.md](references/phase5-6-hardening.md) | Adversarial review converged, ready to harden |

## Quick Start

1. Ask the user what they want to build and at what VSDD intensity level
2. Create `vsdd/` tracking directory
3. Enter Phase 1 — load [references/phase1-spec.md](references/phase1-spec.md)
4. Progress through phases sequentially, loading references as needed

## Intensity Levels

Not every feature needs full ceremony. Ask the user or infer from context:

| Level | Phases | When |
|-------|--------|------|
| **Full** | 1 → 2 → 3 → 4 → 5 → 6 | Correctness-critical: finance, security, infrastructure |
| **Standard** | 1 → 2 → 3 → 4 (mutation testing only from Phase 5) | Most production features |
| **Light** | 1 (spec only) → 2 → quick adversarial pass | Rapid development with guardrails |

Default to **Standard** unless the user specifies otherwise or the domain demands Full.

## Core Principles

1. **Spec Supremacy** — the spec is the highest authority below the human. Nothing exists without tracing to the spec
2. **Red Before Green** — no implementation until a failing test demands it. Do NOT write implementation and tests simultaneously
3. **Anti-Slop Bias** — the first "correct" version is assumed to contain hidden debt. Trust is earned through adversarial survival
4. **Fresh-Context Adversary** — adversarial reviews use sub-agents with no prior conversation context to prevent politeness drift
5. **Four-Dimensional Convergence** — not done until specs, tests, implementation, and verification have all independently survived review
6. **No Redundant Tests** — do not test what the type system already ensures. Tests should cover runtime behavior, invariants, and edge cases that types cannot express; avoid asserting facts that are already in the type signature
7. **Testing Trophy** — most tests should be integration tests (most bang for buck). Fewer unit tests; fewer e2e tests reserved for critical user journeys. Use mutation testing (e.g. Stryker for TypeScript/JavaScript) in Phase 5 to verify tests actually catch bugs

## Contract Chain

Every artifact must be traceable:

```
Spec Requirement → Test Case → Implementation → Adversarial Review → Verification Result
```

At any point, answer: *"Why does this line of code exist?"* by tracing back to a spec requirement.
