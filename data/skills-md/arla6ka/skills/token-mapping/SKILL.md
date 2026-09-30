---
name: token-mapping
description: Reports how hardcoded style values on a page, file or diff map onto a project's existing design tokens, purpose first, then value. Use for "are we using our tokens here", "which hardcoded colors map to which tokens", a token audit or planning a token migration. It never edits and never creates or renames tokens. Fixes and whole-app consistency go to design-system-boss.
---

# Token mapping

1. Load the rules: `references/mapping-rules.md`, AGENTS.md or CLAUDE.md, and `docs/system/decisions.md`. Note overrides and any precedence rule.
2. Load the list and record its name, format, location, read method and time (`references/sources.md`).
3. Resolve every alias to its final value in each mode, and write down every disagreement with a second source.
4. Collect the groundwork: one row per property, with its location, category and job (`mapping-rules.md`, What counts as the team's list).
5. Normalize both sides per the rules file, converting colors with code.
6. Classify: candidate tokens whose stated purpose covers the job, semantic before primitive, one class per row per mode, each with a reason and its difference in numbers.
7. Count and close: the gap threshold, Consistency by role when the rules call for it, then Summary and Source.

Never ship:

- A token name that is not in the list that was read. A gap never gets a new name.
- A match on value before purpose, or outside the rules file's tolerances.
- A primitive where a semantic token covers the job.
- A list or value filled from memory after a failed read.
- A public system's token names, Geist's included, standing in for the team's list.
- Any change to the repo.

The result is a report that lands raw values (hex codes, pixel values, shadows) on a token list someone else owns. With no token set, it hands back groundwork for building one.

## Start from whatever the ask gives

"Check the tokens on the settings page" is enough. Find the values and the list yourself, and ask only for what no tool can reach. Defaults:

- Values: what the person named, else the branch diff, else the product code (`references/sources.md`).
- Mode: the list's default mode, named in Source.
- rem root: 16px, unless the project sets another.

## When a coordinator calls it

Take the values and the list in the brief as given and run to the end without asking. Questions go under For a person to decide, each with a default, which the caller turns into gates. Start with a status line, `Status: complete`, `Status: not actionable (gap threshold)` or `Status: stopped: <condition>`, then `Commit: none`. Return the report, or the stop shape below, as your final message.

## Output

Seven parts, in this order, each specified in `references/mapping-rules.md` (Report shape): Summary, Mapping, Do not use, Ambiguous, Gaps, For a person to decide, Source.

Run directly, the chat reply gives the Summary's answer with its numbers, each command with its exit code, up to three questions for a person with defaults, and `Next:` with one prompt to paste.

The report is ready when:

- Every row has a job, a class and a reason, and every ambiguous row names two or more candidates.
- A semantic token appears wherever one covers the job, never its primitive.
- Anything inferred rather than read, such as a job taken from a class name, is marked inferred.
- Nothing in the repo changed.
- The last line reads `Coverage:` (`mapping-rules.md`, Report shape).

## Stops

Stop and report on these only.

- No list exists, or no tool can read one.
- One name has two values in the same mode, which makes the list broken.
- Two sources disagree and no project rule says which wins. Report both sides.

A stopped run returns the condition, the groundwork from step 4 (grouped per `mapping-rules.md`, When the repo has no token file), and the shortest message that unblocks it, such as "Paste `tokens.json` or give its path." Gaps are never a stop.
