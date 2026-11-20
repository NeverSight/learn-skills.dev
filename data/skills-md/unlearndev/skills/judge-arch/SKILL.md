---
name: judge-arch
description: Judge the current branch's changes against the repo's DECISIONS.md design decisions. Use when asked to judge, check, or review a change or branch against the decisions.
---

Judge the current branch's changes against the design decisions in DECISIONS.md.

## Look

1. Read `DECISIONS.md` in the repo root. If it doesn't exist, stop and
   report that instead of judging.
2. Find the base: the repo's default branch, unless the user names one.
3. Read the full diff (`git diff <base>...HEAD`) and open every changed
   file, so each change is judged in the context of the file it lands in.

## Judge

Check the change against each decision in DECISIONS.md, in order. A
decision is identified by its heading text — use that exact name
everywhere in the report; never number the decisions.

- Only the decisions in the file. No other findings, no style feedback, no
  improvement suggestions.
- A violation needs evidence you can point at in this change: a file and
  line, a whole file, or the set of files involved. If it doesn't clearly
  break a written decision, it isn't a violation.
- The same wrong pattern in two places is two violations.

## Report

Output exactly this structure, and nothing else. Use real markdown
headings so the report renders grouped by decision:

```
# JUDGMENT · <branch> vs <base> · <n> violations

## ❌ <DECISION NAME, UPPERCASE>

**<where>**
<what the code does, one sentence>
- **What breaks:** <the concrete consequence of shipping this as is, one sentence>
- **Potential fix:** <the smallest concrete change that satisfies the decision, one sentence>
```

Rules for the report:

- One `##` section per violated decision, in DECISIONS.md order. Prefix
  the heading with ❌ and set the decision name in uppercase. A decision
  with no violations gets no section.
- One `**<where>**` block per violation, ordered by file within its
  section. `<where>` is `file:line` for a single spot, the file for a
  file-wide problem, or the files involved when the violation spans
  several.
- The **What breaks** line names a real failure with a trigger, even one
  that arrives later (e.g. "rename a column in loyalty and refunds
  break"), never a vague quality complaint ("this hurts maintainability").
- The **Potential fix** line must be actionable without reading anything else: name
  the concrete mechanism to use, not just the one to avoid (e.g. "Move
  the merge steps into an `app/Actions/MergeIdeas` action and have the
  controller call it", not "don't do this in the controller").

If there are no violations:

```
# JUDGMENT · <branch> vs <base> · clean

Every decision in DECISIONS.md holds for this change.
```
