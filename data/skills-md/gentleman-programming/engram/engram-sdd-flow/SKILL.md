---
name: engram-sdd-flow
description: >
  Spec-Driven Development workflow for Engram.
  Trigger: When user requests SDD or multi-phase implementation planning.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Use this skill when:
- Starting non-trivial changes
- Coordinating spec, design, implementation, and validation
- Running command-based SDD flow

---

## Canonical Phase Order

1. `explore` - understand existing behavior and constraints
2. `propose` - define intent and scope
3. `apply` - implement tasks from approved plan
4. `verify` - validate behavior against spec and regressions
5. `archive` - capture completion and close loop

Never skip a phase without explicit rationale.

---

## Artifacts per Phase

- Explore: findings and risks
- Propose: change proposal with scope boundaries
- Apply: code + tests
- Verify: evidence of validation
- Archive: finalized summary and follow-ups

---

## Exit Criteria

- [ ] Scope and risks understood before implementation
- [ ] Tests prove expected behavior
- [ ] Verification covers regressions
- [ ] Session summary captures learnings for next work
