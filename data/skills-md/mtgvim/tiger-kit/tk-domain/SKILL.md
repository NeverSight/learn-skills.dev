---
name: tk-domain
description: "[user/auto] 저장소 고유 용어를 정립하거나 되돌리기 어렵고 맥락 없이 의외이며 실제 절충이 있는 결정을 sparse ADR로 남깁니다. 일반 구현 설명에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<domain term, durable decision, evidence, or context scope>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Repository Domain Context

Use this skill only to create or refine repository-owned ubiquitous language and sparse durable decision context.
Glossary entries and ADRs remain distinct artifacts. This is not a generic memory store, rules corpus, architecture
document, implementation guide, or troubleshooting archive.

## Evidence

Investigate repository source, product material, and supplied conversation evidence for one concrete project-specific
term. Confirm the canonical spelling, meaning, and useful alternatives. If the meaning claims code behavior, ground it
in current source. Ask the user only when canonical vocabulary is a genuine product/domain decision that evidence cannot
resolve.

Do not create an artifact before the first real term is confirmed. Respect an existing repository glossary convention
instead of duplicating it.

Sharpen fuzzy or overloaded language only when the ambiguity changes an artifact or decision. Use one concrete edge
case only when the relationship cannot otherwise be resolved. Fresher code or runtime evidence beats a stale glossary
claim; surface the conflict instead of silently preserving stale wording. Ordinary wording ambiguity needs no domain
ceremony.

## Artifact

For one context, create or refine root `CONTEXT.md` with the smallest useful form:

```md
# Domain Context

## Language

**<canonical term>**
<short project-specific meaning>
_Avoid_: <misleading synonym>, <unwanted translation>
```

`_Avoid_` is optional. Preserve Korean/English spelling, acronyms, casing, and spacing exactly when they are part of
the canonical term.

Exclude file paths, classes/functions/tables, debugging tips, generic programming vocabulary, transient values,
task acceptance criteria, general engineering rules, and long product specifications. Move behavioral invariants to
their repo-native owner instead of the glossary.

## Optional Multi-Context Escalation

Default to root `CONTEXT.md`. A monorepo or multiple packages alone is not evidence for splitting. Propose
`CONTEXT-MAP.md` only when actual bounded contexts exist, such as one term having different meanings, unrelated
vocabularies repeatedly mixing, or workers rarely needing another context's language. This structural change requires
explicit current-turn approval.

The map contains only relevant context paths and relationships; it never duplicates glossary entries. After approval,
place each glossary at the natural bounded-context path and verify every mapped path.

## Sparse Durable Decisions

Propose an ADR only when all three thresholds hold:

1. **hard to reverse**: changing course has meaningful rollback or migration cost;
2. **surprising without context**: a future maintainer may undo the choice without its rationale;
3. **real trade-off**: at least two valid alternatives existed and the decision chose among them for a reason.

Keep local implementation rationale in a code comment or its repository-native owner. Do not ADR-ize ticket plans,
test methods, coding conventions, simple library selection, or easily reversible choices.

Prefer an established repository ADR convention. When none exists, use the minimal fallback
`docs/adr/0001-<slug>.md`, incrementing the highest filename number without reading unrelated files. Create
`docs/adr/` lazily for the first real ADR. The fallback contains a title and usually one to three sentences stating
the context, decision, and why. Add status, alternatives, consequences, or other fields only when they carry information.

Before proposing a new ADR, read only existing ADR evidence relevant to that decision. Compare it with current code
and decide whether the request is a duplicate, refinement, or supersession. Do not silently overwrite or contradict
owned rationale: reuse an unchanged decision, or surface `revisit ADR` with the changed premise and propose an explicit
`refine or supersede` path. Never scan an unrelated ADR or context tree.

## 🔴 CHECKPOINT · 🛑 STOP

Before any write, present the term or durable decision, evidence, exact target path, proposed wording, exclusions, and
whether this is a root refinement, approved multi-context change, new ADR, refinement, or supersession. Require
current-turn approval for the exact mutation. Evidence or scope drift invalidates approval.

After approval, write the minimum artifact atomically and reread it. Verify that glossary terms and `_Avoid_` values
are exact, or that the ADR preserves its evidence, decision, why, and relationship to existing rationale. Ensure no
excluded implementation/rule content entered either artifact. Do not create central TigerKit state, host-specific
memory, a learning corpus, or automatic repository scanning.

Return the changed path, canonical terms or decision, evidence basis, verification, and one actual status:
`Pass | Blocked | Unverifiable | Fail`.
