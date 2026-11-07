---
name: simplicity-review
description: Cold review of a diff for complexity it can shed, each finding naming what to cut and what replaces it. Use when asked what can be deleted or simplified in a branch, PR or local changes, whether code is over-engineered, or when another skill dispatches a simplicity review.
metadata:
  credits:
    - skill: ponytail-review
      author: Dietrich Gebert
      url: "https://github.com/dietrichgebert/ponytail/blob/main/skills/ponytail-review/SKILL.md"
---

# Simplicity review

Review the diff you were handed, with its contract or ticket if one came along. When you compute the diff yourself, run `git fetch origin <base>` and diff against `origin/<base>`: a local base branch can lag the remote and pull unrelated commits in.

The contract draws the line between required and speculative. Read its linked issues and parent spec too: a data model, result type or acceptance criterion there makes code required even when the contract file never names it. When prior-round verdicts come along, rejected findings stay closed and applied ones stand.

Simplicity is your only axis; bugs, spec gaps and style belong to the other reviews. Every finding is a cut: less code for the same behavior, or code nobody needs gone.

## Cuts

- `delete:` code nothing needs: dead code, unused fields, props, params and options, unrequested features, re-checks of what an upstream guard already ensures, leftovers of the change. Replacement: nothing.
- `reuse:` something that already exists: a repo helper, component, type or constant (name the path), a stdlib function, a platform feature, an installed dependency. A dependency added for a few lines is a `reuse:` of the code it replaces.
- `yagni:` an abstraction with one implementation, config nobody sets, a layer with one caller, perf machinery (lazy loading, caches, memoization, retries) no requirement or measurement asked for.
- `inline:` a single-use helper or wrapper, or one function split into pieces nothing else calls. Fold the logic into its call site. A separate function stays only when it is reused, composable, hides a genuinely complex boundary, or its name reads clearer at the call site than its body would.
- `derive:` stored or synced state the code can compute from data it already has: a column, a store field, a prop.
- `shrink:` the same logic in fewer lines: copy-paste folded into one helper, a literal or rule repeated three or more times, a switch turned into a table, queries merged. Show the shorter form.
- `ask:` complexity the contract requires that looks out of proportion to its need, such as a rare failure path, an error taxonomy or a cache. Quote the contract line; the user decides. A guard against a speculative or vanishingly unlikely race or security edge case is an `ask:` too, contract or not: name its concrete failure mode, likelihood and complexity cost.

Tests are code: cut a test that repeats another (name the test that already covers the case) and hoist duplicated fixtures.

## What makes a finding

Report a cut only when all of these hold:

- `shrink:` and `reuse:` keep observable behavior identical: errors, stored values, output and edge-case UX. `delete:` and `yagni:` name the behavior that goes.
- The replacement passes the repo's lint rules and type-check. Read the lint config and neighboring code before proposing a form; when the cut touches types, type-check a scratch file under `$TMPDIR`.
- It follows the codebase's existing structure and conventions.
- It saves at least two lines or removes a concept.
- You can state it without a caveat. A cut you could not confirm stays out of the report.
- A cut test suite still goes red against the old code.

Keep validation at trust boundaries, error handling that prevents data loss, security against a concrete threat, accessibility, anything the contract asks for, and one smoke test or assert-based self-check per new piece of logic. Moved or merged code keeps its error handling and validation.

## Report

Open with finding `1.` and number across the whole report, so the user can say "fix 2 and 5":

`<N>. <file>:L<line>: <tag> <what>. <replacement>.`

- `1. src/auth/email.ts:L12-38: reuse: 27-line validator class. The zod schema already checks the address, delete the class.`
- `2. src/date.ts:L4: reuse: moment imported for one format call. Intl.DateTimeFormat, 0 deps.`
- `3. db/schema.ts:L41: derive: stored initials column. Compute from name at render, drop the column and its sync.`
- `4. routes/export.ts:L52-71: yagni: retry wrapper around an idempotent local call. Nothing replaces it.`

After the findings, at most three unnumbered `kept:` lines for code that looks speculative but is required, each quoting its contract line.

With nothing to cut, the whole report is `Lean already. Ship.`

Leave the working tree as you found it: someone else is building in it.

Completion: every changed hunk read, every finding passes every check above, and `git status` matches what it showed when you started.
