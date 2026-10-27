---
name: reuse-first
description: "Search before you write, sweep before you finish. Use BEFORE creating any utility, type, schema, component, hook, constant, module, or package; BEFORE hardcoding a literal that may be an exported constant; when about to copy-paste similar code; and as a completion gate over every file the task touched, not just the diff."
---

# Reuse first

Every duplicate is a future divergence. A bug fixed in one copy stays broken in the other.

Greenfield with no codebase to search yet. Run project-discovery first, then come back here.

## 3-layer search

Exact name often misses it, so search in three passes:

1.  **Name layer**: `grep -r "functionName"`, exact + camelCase + snake_case variants
2.  **Behavior layer**: grep for what it does, `format.*date`, `validate.*email`, `parse.*currency`
3.  **Reference layer**: find a feature that uses the thing you are looking for. Open it, follow its imports

You are done when you have printed what each layer returned. Write these three lines before you write anything:

```text
Name layer:      <variants grepped> -> <hits, or none>
Behavior layer:  <3+ keywords> -> <hits, or none>
Reference layer: <feature file opened> -> <imports followed>
```

Those three lines are the artifact. Creating the file without them is the failure this skill exists to prevent, and it stays invisible afterward. The new code compiles, passes review, and ships because nothing downstream re-asks the question. If you already wrote the artifact, run the search anyway and delete what it finds a home for. Do not rationalise the copy.

One search per artifact, not per batch. Creating six modules in one sitting is six searches. Batching them into one glance is how a shared constant gets missed. The search that would have found it was never phrased with its keywords.

If you cannot name three behavior keywords for the thing you are about to write, you do not understand it well enough to search for it. That is the finding, not the search.

## What to do with what you find

Load `${CLAUDE_SKILL_DIR}/references/artifact-guide.md` now. Reach its acceptable-duplication section only after all three layers have returned.

## Signs you are about to fork

- Naming with a suffix: `formatDate2`, `userServiceV2`, `validateInputNew`, `parseFooHelper`
- Variant naming for similar behavior: `formatPrice` + `formatCurrency` + `priceFormatter` coexisting, a divergence in progress
- Inline reimplementation of something that "feels like it should exist": that feeling is usually correct
- A new file in `utils/` or `lib/` under 30 lines likely belongs in an existing file
- A new type alias that mirrors a Zod schema's inferred type. Use `z.infer` instead
- Copy-pasted boilerplate across files like auth checks, error mapping, and response shaping. Extract it to a shared helper
- You define a new constant inline when a similarly named one already lives in `constants/`

## Sweep mode: before claiming the task done

The pre-creation search only sees what you were about to write. Load `${CLAUDE_SKILL_DIR}/references/sweep-mode.md` now and run the full sweep it describes before claiming the task done.
