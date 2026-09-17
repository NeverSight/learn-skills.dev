---
name: shape
description: >
  Design codebase structure before implementation: ground in real system, explore two distinct structures in parallel, synthesize one design doc. Use when ownership/interfaces/seams change. Skip when one owner and interaction are obvious.
---

# Shape: Codebase Structure Design

Design shape, hand over. Output: one design doc in `docs/design/`. No implementation code.

**Method**: Ground → Explore twice → Synthesize → Present

**Skip when**: one owner/dependency/interaction already obvious → write `codebase-design skipped: <reason>`

## Phase A: Ground

**Skip for**: greenfield or trivial grounding (inline in 3 lines).

Spawn one subagent. Pass inline prompt:

```
**First principles thinking**: decompose <change description> to core mechanism.
**Surface uncertainties** explicitly.

Trace the real current system. Output `/tmp/codebase-design-<slug>/grounding.md` (≤2 pages, facts only):

## The change
<Copy from upstream>

## Locked decisions  
<User-confirmed fields/flags/choices - candidates cannot reopen>

## Current shape
Which module owns what decision/state/effect. Cite `path:line`.
Trace: data enters → decides/stores/effects → leaves

## Surviving contracts
Public exports with live callers: `path:symbol - compatibility requirement`
Find real callers, don't infer.

## Dependencies crossed
Classify: in-process / local-substitutable / remote-owned / external + rationale

## Repository idioms
Syntax, error handling, layout, naming. Cite one representative file.

## Unknown
Gaps + what each would change

---
Every claim cites `path:line` or commit/PR, else → Unknown.
Do not propose structure. Facts only.
```

Read output file. Move uncited claims to Unknown.

## Phase B: Design Twice

Spawn 2 parallel subagents with different constraints.

**Pick constraint pair**:
- Default: (1) minimize interface vs (2) optimize for dominant caller
- When grounding shows contested ownership: (1) keep boundary vs (2) merge ownership
- When external dependency dominates: (1) port locally vs (2) adapt at edge
- When seam unclear: (1) separate early vs (2) separate late

Pass each candidate:

```
**Independent thinking**: ignore other candidate.
**Occam's razor**: simplest structure that solves.

Your constraint: <specific constraint>
Grounding: <paste grounding content>

Design discipline to apply:
- **High cohesion, low coupling**: group by owned knowledge
- Interface depth: capability hidden ÷ surface size
- Data structures first, then operations
- Explicit domain intent (no transport on surface)
- Idempotence: what if runs twice/crashes
- Short call chains (flatten if >3 files)

Return structured text:

1. Caller usage (write first): 2-3 real call sites showing constraint applied
2. Module map: ASCII, compact, annotated with state/effects/recovery
3. Load-bearing declarations: signatures only (no bodies)
4. Seam placement: category + adapters (2+ or none) + test strategy, or "no new seam"
5. Rationale: load-bearing decisions, complexity hidden, alternatives rejected

Follow your constraint honestly. Diverge from other candidate (that's the signal).

Terms (use exactly): module, interface, depth, seam, adapter.
```

Wait for both.

## Phase C: Synthesize

Read both candidates.

**Critical comparison** + **ablation thinking**: what breaks if we remove this component?

Screen for flags:
- **Shallow** (reject): surface exposes coordination → concentrate
- **Leakage** (reject): shared representation → translate at boundaries
- **Temporal decomposition** (reject): stages share knowledge → group by owned knowledge
- **Pass-through** (revise): forwards without policy → ablation test, inline if no divergence
- **Policy displacement** (revise): adapter infers effect → pass explicit intent
- **Hypothetical seam** (revise): one adapter → inline until varies (Occam's razor)
- **Contract drift** (revise): map ≠ declarations → reconcile

If reject flag found: revise candidate or re-run Phase B with adjusted constraint.

Compare on depth. Pick base (future can extend without breaking). Graft what other got right. Screen again. Reconcile all interactions.

If converge: note it, ship consensus.

## Phase D: Present

Write to **`docs/design/NN-<slug>.md`** (user's language). `NN` = next unused number.

Structure:
1. **Decision** (2-3 lines): shape + why
2. **Caller usage**: 2-3 sites (cite `path:line` or mark `new`)
3. **Module map**: ASCII, annotated
4. **Contracts**: signatures (mark `inferred` if not traced)
5. **Synthesis**: base why, grafted why, rejected why
6. **Preserved contracts**: `path:symbol - compat` (one line each, or "none")
7. **Seams**: location + category + adapters + tests (or "none added")
8. **Caller knowledge change**: added/removed (or "unchanged")
9. **Tradeoffs**: "accept X for Y" (or "none identified")
10. **Implementation guidance**: load-bearing contracts, where to start, deviation signal
11. **Blockers**: unresolved + impact + owner (or "none")

Cite preserved contracts, don't reprint. No bodies.

**Verify before completion**:
□ Preserved contracts checked (grounding line 37-38: surviving contracts exist?)
□ Seams documented (candidates introduced adapters?)
□ Caller knowledge change stated (grounding line 32-34: current shape changes?)
□ Tradeoffs surfaced (synthesis rejected alternatives?)
□ Blockers surfaced (grounding line 46-47: unknowns remain?)

**Then stop**. No implementation, no tickets.

**Human pushback**:
- On facts/grounding → re-run Phase A
- On constraint choice → re-run Phase B with different pair
- On synthesis logic → revise Phase C with user guidance
- On presentation only → edit doc directly