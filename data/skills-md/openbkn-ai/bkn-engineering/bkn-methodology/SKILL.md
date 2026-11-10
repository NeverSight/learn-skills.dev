---
name: bkn-methodology
description: Shared OpenBKN modeling methodology. Use when reviewing BKN object boundaries, relation semantics, facts, metrics, actions, governance points, evidence, traceability, or Skill / Agent responsibility boundaries.
---

# BKN Methodology

Use this skill as the common modeling rule base for OpenBKN projects.

Read `references/bkn-methodology.md` before making or reviewing BKN modeling decisions.

## Use When

- Deciding whether a concept should be an object, property, fact, state, metric, action, or governance point.
- Reviewing whether a relation expresses a business path rather than a field join.
- Separating stable facts from runtime state and audit records.
- Clarifying the boundary between query, calculation, explanation logic, Skill / Agent work, and side-effecting actions.
- Checking whether evidence, traceability, permissions, approvals, and human confirmation points are represented correctly.

## Output

Return concise modeling guidance with:

1. Recommended classification.
2. Reasoning.
3. Boundary risks.
4. Questions that must be answered before BKN creation.
