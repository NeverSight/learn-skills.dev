---
name: token-mapping
description: Use to report how hardcoded style values on a page, file or diff map onto a project's existing design tokens, such as "are we using our tokens here", "which hardcoded colors map to which tokens", a token audit or planning a token migration. It never edits. Replacing the values is build-design-system.
---

# Token mapping

A read-only report that lands raw values (hex, px, shadows) on a token list someone else owns. Classes, normalising and tolerances are in `references/mapping-rules.md`. "Check the tokens on the settings page" is enough of an ask. Find the values and the list yourself.

## Steps

1. **Find the list.** Token files, theme entries, custom properties on `:root`, a component library's variable pairs. A framework's default theme is not the team's list, and neither is a public system's (Geist's names never stand in for the team's). Record its name, location and how you read it. If a read fails, say so and stop. Never fill a list from memory.
2. **Find the values.** What the person named, else the branch diff, else the product code. Record each with its file, line, property and job.
3. **Resolve.** Follow every alias to its final value in each mode. Write down every disagreement between two sources.
4. **Normalise** both sides (lengths to px, colours to OKLCH compared by delta E OK) with code, never by eye.
5. **Classify** each row once per mode. Purpose first, then value.
   - Exact: the token's stated job covers the row and the values match.
   - Semantic: the job covers it and the value is inside tolerance. State the difference in numbers.
   - Ambiguous: two or more tokens fit and nothing picks one. Name every candidate.
   - Gap: no token's job covers it, or the only fitting token is out of tolerance. A gap never gets a new name.
6. **Count and close.** When gaps are over 30% of rows and number 12 or more, the list is usually the wrong one. Say so, still deliver the table, and lead with `Status: not actionable (gap threshold)`.

## Report

Summary, Mapping, Do not use (a token whose value matches but whose job differs), Ambiguous, Gaps, For a person to decide, Source. Last line `Coverage:` with what was scanned and what was not. Run on its own, the chat reply gives the answer with its numbers and one prompt the person can paste to take the next step.

## Rules

- A match on value before purpose is wrong. Wrong: `#6b7280` mapped to `color.border.default` because the hex is equal. Right: it is text, so the candidates are text tokens, and the border token goes in Do not use.
- A semantic token wins over the primitive it aliases. Map to a primitive only when no semantic token covers the job, and say so.
- A palette class (`text-gray-500`) names a value and no job. It gets a row, counted apart from raw values.
- Anything inferred rather than read, such as a job taken from a class name, is marked inferred.
- Counts carry their unit: occurrences, lines or mapping rows.

## Stops

Stop and report on these only. No list exists. One name has two values in the same mode. Two sources disagree and no project rule says which wins (report both). Return what stopped it, the groundwork so far, and the shortest message that unblocks it, such as "Paste `tokens.json` or give its path."

## Done

Every row has a job, a class and a reason. Every ambiguous row names two or more candidates. Nothing in the repo changed (`git status` is the same before and after). The last line reads `Coverage:`.
