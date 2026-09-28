---
name: review-harness-spec
description: Audit an existing hedera-harness recipe for wiring and evaluate-checklist problems before a run. Use when the user wants a harness recipe reviewed before running it.
---

# Review Harness Spec

Audit a hedera-harness **recipe** on disk along two axes. Catch mistakes the
harness only surfaces after a generator attempt is already burning.

Load the shared vocabulary first: read
[`../harness-spec-anatomy/SKILL.md`](../harness-spec-anatomy/SKILL.md) and its
[GLOSSARY.md](../harness-spec-anatomy/GLOSSARY.md).

Targets **hedera-harness schemaVersion 3**.

Authoring-only skill. Recipes do not list skills.

## Step 1: Locate the recipe

The recipe is `.harness/spec.yaml` under the project root. Read every file it
resolves to, remembering that v3 **defaults** most paths — an absent key is not
a missing file:

| Key | Default when absent |
|-----|---------------------|
| `prd` | `.harness/prd.md` (a list means **increments**) |
| `eval` | absent (EVALUATE off). A list must be 1:1 with `prd:` |
| `validators.static` | `.harness/validators/static.json` |
| `validators.commands` | `.harness/validators/yarn.json` |

If the recipe file is missing, stop and ask. If `schemaVersion` is absent, `1`,
or `2`, stop and recommend rewriting to v3 (`contract:` → `eval:`, drop
`skills:`, set `schemaVersion: 3`) — or regenerate with `hedera-harness init`.
`migrate` is gone. Review the rewritten recipe, not the stale original.

## Step 2: Wiring axis

```bash
bash <path-to>/harness-spec-anatomy/scripts/check-spec.sh <project-root>
```

`<project-root>` is the directory containing `.harness/`. The script runs
`hedera-harness doctor --recipe-only` for schema validity, then adds cross-file
coherence checks.

Report its findings **verbatim** under `## Wiring`.

If it reports the schema was **not** validated (harness CLI missing or too
old), say so explicitly in the report — the wiring axis is then partial,
not passed.

## Step 3: Eval axis

Judgment only — what a script cannot see. Work through
[references/review-checklist.md](references/review-checklist.md). Cover at least:

- Every PRD journey maps to ≥ 1 assertion in the matching **evaluate checklist**
- Every assertion traces back to a PRD journey (no orphans / scope creep)
- Severity budget sane (prefer ≤ 2 `critical`)
- **Needles** pin real scripts, not brittle implementation strings
- Playwright stage stays thin; deep UX lives in the checklist
- No `skills:` key (product plugins are discovered; the generator picks)
- The recipe is not padded with values that merely restate a default
- For **increments**: each one leaves the app green, they are ordered by
  dependency, and `eval:` is 1:1 with `prd:`

Report under `## Eval`. Do **not** merge or rerank with Wiring — a **recipe**
can be perfectly wired and still grade the wrong thing.

## Step 4: Emit the report

```markdown
# Harness Recipe Review — <slug>

## Summary
- **Schema**: v3 | stale (rewrite first)
- **Stage ambition**: ASSERT | +SMOKE | +EVALUATE | +CHAIN
- **Increments**: single PRD | N ordered (eval paired: yes / no / scalar)
- **Ready to run ASSERT?**: yes / no
- **Wiring findings**: N  (schema validated: yes / no)
- **Eval findings**: N

## Wiring
- [script output or hand-checked findings]

## Eval
### Blocker
- [id] <what> — <where> — <fix>
### Warning
- [id] <what> — <where> — <fix>
### OK
- [id] <what>
```

## Step 5: Handoff

If ready for ASSERT:

```bash
hedera-harness run .harness/spec.yaml --max-attempts 3
# or: yarn harness:run
```

## Additional resources

- [references/review-checklist.md](references/review-checklist.md)
- Companion: `/create-harness-spec`
- Vocabulary: `/harness-spec-anatomy`
