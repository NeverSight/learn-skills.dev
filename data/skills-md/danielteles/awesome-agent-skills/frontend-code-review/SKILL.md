---
name: frontend-code-review
description: >-
  A meta skill that orchestrates a frontend code review: given a diff, it picks
  which of the other skills apply, runs them in a sensible order, merges their
  findings into one ordered list, and de-duplicates an issue that two skills
  report. It holds no engineering rules of its own — it routes to
  `core-typescript`, `architecture-and-design`, the framework skills, and the
  lenses. Use it when the user asks for a full code review of a pull request or a
  diff, says "review this change", "run all the skills", "which skills apply
  here", or wants findings from several skills combined without duplication.
license: CC-BY-4.0
metadata:
  author: danielteles
  version: "1.0"
---

# Frontend Code Review — Review Skill

The conductor for a multi-skill review. It decides which skills a diff needs, the order to apply
them, and how to turn several per-skill finding lists into one review a human can act on. It adds no
engineering rules — every finding still comes from another skill's Ruleset.

> **Builds on.** Every other skill in this repository: `core-typescript` and
> `architecture-and-design` (the base), `react` / `angular` / `vue` (framework), and
> `accessibility` / `styling-and-design-tokens` / `web-performance` / `i18n-and-localization` /
> `test-quality` / `e2e-testing` (the lenses), and `component-api-design` for a shared component's
> public contract. This skill only routes; each finding's authority is the skill it came from. If a
> named skill is not loaded, apply its layer from general knowledge and do not block. On a conflict
> between two skills' findings, this skill's de-duplication rules decide which one is reported.

This SKILL.md is self-sufficient: the **Ruleset** below is the complete, enforceable list. Each
`references/<topic>.md` holds that group's reasoning and `❌ / ✅` code, and
`references/worked-example.md` a full review pass; open them for depth when your runtime allows.

---

## How to Use This Skill

Pick the mode that matches the task. Do the steps in order.

| Mode | Steps |
|---|---|
| **Review** — run a full review of a diff | 1. Classify each changed file and pick the skills that apply (`routing`). 2. Apply them in order: `core-typescript` → `architecture-and-design` → the framework skill → the lenses → this skill's checks. 3. Collect every skill's findings in its own Output Format. 4. De-duplicate across skills (`dedup`). 5. Merge into one list — grouped by file, `must-fix` before `consider` within each file, ascending line order within each severity (`merging`). 6. Write the summary line and hand off. Do not invent findings. |
| **Scope** — decide which skills a change needs | 1. Classify the changed files (`routing`). 2. List the skills that apply and why, and the ones that do not. 3. Flag any gap — a changed concern with no skill loaded to cover it. Do not do the full review. |

### Output Format

The merged review. Each finding keeps the Output Format of the skill that produced it:

```
<severity> · <topic> · <file>:<line> — <what is wrong>. <the fix as an action>.
```

- `<topic>` is a Ruleset topic slug (`routing`, `dedup`, `merging`) for a finding this skill raises itself, or the originating skill's own topic (`effects`,
  `tokens`, `lcp`, …) for a routed one.
- Prefix the review with one summary line: the file count, the `must-fix` count, and whether it blocks merge.

### Rules for Every Mode

- This skill never invents an engineering finding. If no other skill's rule is broken, there is no finding.
- Name the skill and topic each finding came from, so the author can read the rule.
- Do not rewrite the author's code. Name the rule and the change.
- Missing coverage is itself a finding: "the diff adds a `.module.css` file and no styling review ran".

---

## Ruleset

### routing → `references/routing.md`

- [ ] Every changed file is classified and mapped to the skills that apply — `.ts`/`.tsx` to `core-typescript`; a component or hook to the matching framework
      skill; any UI to `accessibility` and, if it touches CSS or tokens, `styling-and-design-tokens`; user-facing text or a formatted value to
      `i18n-and-localization`; a change to loading, bundling, or rendering to `web-performance`; a shared or library component's props to
      `component-api-design`; a test file to `test-quality`, an e2e spec to `e2e-testing`; a cross-cutting or structural change to
      `architecture-and-design`.
- [ ] Skills are applied base-first: `core-typescript`, then `architecture-and-design`, then the one framework skill (with `component-api-design` for a
      shared component), then the lenses, then this skill's own checks.
- [ ] Only the framework skill for the codebase runs — not `react` and `angular` and `vue` on the same file.
- [ ] A concern the diff clearly touches with no skill available to cover it is reported as a `routing` gap, not silently skipped.

### dedup → `references/dedup.md`

- [ ] When two skills flag the same line for the same underlying issue, one finding is reported, not two.
- [ ] The finding is kept from the skill that owns that decision: `accessibility` for an a11y requirement, the framework skill for its API,
      `styling-and-design-tokens` for a CSS value, `web-performance` for a budget, `i18n-and-localization` for a translatable string or a locale format,
      `component-api-design` for a props contract, `architecture-and-design` for a design call, `core-typescript` for a type or syntax point, `test-quality`
      for what a test asserts, `e2e-testing` for a locator, wait, or suite-isolation issue in an e2e spec; a physical CSS property in a directional layout
      is `i18n-and-localization`'s requirement and `styling-and-design-tokens`'s fix.
- [ ] The kept finding names the other skill that also flagged it.
- [ ] Two findings on the same line for *different* issues are both kept.
- [ ] A genuine conflict — two skills prescribing incompatible fixes — is surfaced explicitly with the recommended resolution, not silently resolved.

### merging → `references/merging.md`

- [ ] The merged list is grouped by file; within a file `must-fix` comes before `consider`, and within each severity the findings are in ascending line
      order.
- [ ] Each finding is one line in the Output Format, carrying its originating skill and topic.
- [ ] The review opens with a summary line: files reviewed, `must-fix` count, `consider` count, and whether it blocks merge (any `must-fix` blocks).
- [ ] If no skill produced a finding, the review says so in one line and does not manufacture nits.
- [ ] The author's code is not rewritten; each finding names the rule and the change.

---

## Limits

This skill is review orchestration. It does not cover:

- Any engineering rule itself — those live in the skills it routes to. This skill is empty of domain rules by design.
- Reviewing code no skill in this repository covers (backend, infra, SQL, shell) — it routes only among the frontend skills present.
- Deciding whether to merge — it reports what breaks a rule and whether that blocks; the call is the team's.
- Non-diff review: a full-codebase audit, an architecture review from scratch, or a design doc. Point the relevant skill at that directly.
- Running tools (linters, `axe`, Lighthouse, the type checker) — it assumes their output is available and folds it into the same list.

This skill states how to run and combine the other reviews. It is not a substitute for the skills it calls.

---

## References

This skill composes with every other skill in the repository and defers all engineering judgement
to them:

- **`core-typescript`**, **`architecture-and-design`** — the base layers, applied first.
- **`react`** / **`angular`** / **`vue`** — the one framework skill for the codebase.
- **`accessibility`**, **`styling-and-design-tokens`**, **`web-performance`**, **`i18n-and-localization`**, **`test-quality`**, **`e2e-testing`** — the
  lenses, applied after the framework skill.
- **`component-api-design`** — the public contract of a shared component, applied with the framework skill when the diff touches a library component.

On a conflict between two skills' findings, the `dedup` group decides which is reported; on a
conflict about a rule's substance, the owning skill named there wins.
