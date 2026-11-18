---
name: us-ac-formatter
description: Convert user stories and acceptance criteria pasted as a markdown table into the project's Gherkin (Given/When/Then) format, grouped by sprint goal. Use when the user pastes a US/AC table and wants it reformatted into per-sprint Gherkin acceptance-criteria docs, or asks to "format these user stories", "turn this table into Gherkin", or "break these AC down by sprint".
---

<what-to-do>

The user gives you user stories and acceptance criteria as an ASCII or markdown table. Convert them into the project's structured output: `US-XX` story entries, `AC-XX.YY` Gherkin scenarios, and a sprint breakdown, matching the exact shape in [references/layout.md](references/layout.md).

Steps:

1. **Parse the table.** Identify each user story (persona, action/goal, business value) and each acceptance criterion attached to it. One table row is usually one US or one AC; infer the columns from the header. If the table is ambiguous (columns unclear, AC not mapped to a US, no sprint hints), ask before guessing.

2. **Assign IDs.** Number stories `US-01`, `US-02`, and so on, and their criteria `AC-<story>.<seq>` (`AC-01.01`). Preserve any IDs already present in the input rather than renumbering. If the input has gaps in numbering, keep them. The index script adds the gap notes.

3. **Group by sprint goal.** Every US needs a sprint and every sprint a goal title. If the input carries a sprint breakdown (for example from `product-discovery`), confirm it with the user. If it has none, or it is ambiguous, ask. Never invent one.

4. **Write Gherkin.** Convert each AC into a `Given / When / Then` body inside a ```gherkin fence. Use `And` for continuation lines, indented two spaces. Where a Then enumerates fields/buttons/options, list them as `  - item` bullets. Keep the user's domain wording and language verbatim (e.g. Bahasa Indonesia UI copy): translate nothing.

5. **Emit the three artifacts** in the output format of [references/layout.md](references/layout.md), writing them into `docs/business/` (see its file targets). Read each target first if it exists; merge rather than clobber unless the user asks for a clean overwrite. Show a short summary of what was written.

</what-to-do>

<rules>

- Faithful conversion, not authoring. Do not add, remove, or reinterpret criteria: if an AC is vague, render it as-is and flag it in a trailing `> Note:` rather than fixing it (fixing is the `grooming` skill's job).
- One scenario per AC. Don't merge or split rows.
- Preserve source language and exact domain terms/labels.
- Keep Gherkin steps in the canonical order: all `Given`/`And` context, then `When`, then `Then`. Multiple whens/thens use `And`.

</rules>

## Helper script

After writing the per-sprint breakdown files, do **not** hand-write the AC index
(`acceptance-criteria.md`). Regenerate it deterministically so it can never drift
from the bodies:

```bash
python3 <this skill's dir>/scripts/build_ac_index.py --business-dir docs/business --write
```

It scans `acceptance-criteria-breakdown/*.md`, preserves every US and AC heading
verbatim, counts ACs, pulls sprint focus titles from `sprint-breakdown.md`, and
auto-emits `> Note:` lines for numbering gaps. Run it again any time the bodies
change. Run without `--write` to preview.

## Writing conventions (enforced in all output)

- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative tone.
- If a document carries a metadata header (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`), each such line ends with two trailing spaces so Markdown renders them on separate lines.
