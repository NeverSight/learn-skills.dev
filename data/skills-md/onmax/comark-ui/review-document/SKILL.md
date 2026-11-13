---
name: review-document
description: Turns a review's findings into one short Markdown document a reader can act on, with the verdict first and each finding ranked, located, backed by evidence, and paired with its fix. Use when writing up a code review, a design or QA review, or an audit, where the reader must decide what to do about what you found.
license: MIT
---

# Review document

A review's reader has one question: what do I do now? Answer it in the first two lines, then give each finding just enough evidence that the reader trusts it without redoing your work. This skill organizes findings you already have; finding them is the review itself.

Length is the usual failure. A reader who has to dig through praise, process, and restated findings misses the one that blocks the merge. Every line below the verdict either supports a finding or says what you didn't check.

## 1. Decide the verdict

Pick one: **approve**, **approve with changes**, **request changes**, or **blocked** on a named thing. Under it, write the reason in one sentence that names the finding behind it.

Done when someone who reads only the verdict knows what to do.

## 2. Keep the findings that change the decision

- Keep a finding when fixing it, or not, changes what the reader should do.
- Merge findings with one root cause into one, and list every place it appears.
- Rank each one: **blocking** (wrong results, lost data, a security hole, broken for users), **should fix** (a real cost that can wait), or **nit**, only when the reader asked for them.

Order them blocking first. Done when every finding has a rank and no two share a cause.

## 3. Back each finding

Each finding is four parts, in this order:

1. **A title that states the consequence**, for whom: "Small avatars load the 512px image", not "Cache key issue".
2. **Where**: the file and line, linked when there's a URL.
3. **Evidence**, the strongest you have: a failing test or command you ran (`::tests`, a fenced block of output), a screenshot of the wrong state (measured as the before-after-evidence skill describes), the lines that cause it (a fence with the line highlighted), then reasoning. Say which it is: a finding you reproduced reads differently from one you read in the code.
4. **The fix**: a `::diff` of the smallest change, or one sentence when the fix is a decision for the reader.

Done when every blocking finding has evidence you ran or captured, or says plainly that it comes from reading the code.

## 4. Say what you checked

End with two short lists: what you checked and how, and what you didn't check. A review that implies more coverage than it had loses the reader's trust in the parts that were real.

## 5. Write it

Follow [references/example.md](references/example.md):

- The verdict in a callout: `> [!CAUTION]` for request changes or blocked, `> [!WARNING]` for approve with changes, `> [!TIP]` for approve.
- One `##` heading per finding, numbered, with its rank in the heading. About a dozen lines each, evidence included.
- No summary that repeats the findings, no section for an empty rank, no list of what's good unless the reader asked.

[references/blocks.md](references/blocks.md) has the syntax for the callout, `::tests`, `::diff`, and highlighted lines.

## 6. Check the render

1. Lint it, and fix until it reports no problems:

   ```sh
   vp dlx --package comark-linter --package comark-ui comark-lint review.md
   ```

   These commands use the [global Vite+ CLI](https://viteplus.dev/guide/global-cli). Without it, `pnpm dlx` takes the same arguments.

2. Open the rendered page where it will be read and read it top to bottom as the reader would. Each finding's evidence should be visible without expanding anything except a long log, and each `::diff` should start at the line its finding names.

Done when the page renders without problems and you've read it once as the reader.
