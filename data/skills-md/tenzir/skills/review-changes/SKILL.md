---
name: review-changes
description: >-
  Review code changes in Tenzir projects. Use when auditing diffs or pull
  requests for bugs, security issues, missing tests, documentation drift,
  readability problems, performance regressions, user experience issues, or
  when deciding how to respond to GitHub review comments. Also use this skill
  whenever the user says "review", "look at this PR", "check my changes",
  "audit this diff", "what do you think of this code", or asks for feedback on
  any code they've written or changed — even if they don't explicitly say
  "code review."
---

# Review Changes

Review changed code with explicit severity and confidence.

## Process

Follow this sequence to produce a thorough, efficient review:

1. **Understand intent.** Read the PR description, commit messages, and any
   linked issues. Know what the change is _trying_ to do before judging how
   well it does it.
2. **Scan for scope.** Skim the full diff to understand what areas it touches —
   files, modules, layers. This determines which lenses to load.
3. **Select lenses.** Use the table below to pick the relevant reviewer lenses.
   Load only what applies; skip the rest.
4. **Review each file.** Walk the diff file by file. Pull in adjacent unchanged
   code only when it is necessary to explain impact or verify whether an issue
   is real.
5. **Synthesize.** After the file-by-file pass, look for groupable root causes.
   Multiple symptoms in different files may share one underlying problem —
   present those as a grouped finding instead of separate entries.
6. **Write up findings** using the format and presentation rules below.
7. **Produce a verdict** in the summary section.

## Lens Selection

Use this table to decide which lenses to load based on what the diff touches.
Readability is always worth loading as a baseline.

| If the diff touches…                     | Load these lenses       |
| ---------------------------------------- | ----------------------- |
| User input, auth, networking, secrets    | Security                |
| Public APIs, module boundaries           | Architecture            |
| CLI output, error messages, defaults     | UX                      |
| Hot paths, loops, queries, large data    | Performance             |
| New features, bug fixes, branching logic | Tests                   |
| Docs, README, docstrings, examples       | Documentation           |
| Existing GitHub review comments          | GitHub review threads   |
| Anything else                            | Readability (always on) |

## Scope

Focus on the changed code and behavior introduced by the diff. Pull in adjacent
unchanged code only when it is necessary to explain impact or verify whether an
issue is real.

## Rating

Rate impact separately from certainty.

| Severity | Emoji | Meaning                                                                    |
| -------- | ----- | -------------------------------------------------------------------------- |
| P1       | 🔴    | Critical: security flaws, data loss, crashes, or release blockers          |
| P2       | 🟠    | Important: broken features, serious regressions, or major correctness gaps |
| P3       | 🟡    | Should fix: smaller bugs, coverage gaps, or usability problems             |
| P4       | ⚪    | Nice to have: low-impact polish or consistency issues                      |

Report findings with confidence ≥ 80. For findings between 60–79, mention them
briefly in a "Lower-confidence observations" section at the end, clearly marked
as uncertain. Below 60, drop them entirely.

## Finding Format

Each finding must include:

- `File`: location with line numbers
- `Issue`: one-sentence problem statement
- `Reasoning`: why the behavior is wrong or risky
- `Evidence`: concrete code, types, behavior, or reviewer comment
- `Suggestion`: a specific fix or next action

Use this header format:

```markdown
### 🟠 P2 · 🛡️ SEC-1 · Missing authorization check · 92%
```

Use these prefixes:

- `SEC`: security
- `ARC`: architecture
- `TST`: tests
- `UXD`: user experience
- `RDY`: readability
- `DOC`: documentation
- `PRF`: performance
- `GIT`: GitHub review feedback

Use these category icons when presenting a review summary:

| Prefix | Emoji | Category         |
| ------ | ----- | ---------------- |
| `SEC`  | 🛡️    | security         |
| `ARC`  | 🏗️    | architecture     |
| `TST`  | 🧪    | tests            |
| `UXD`  | 🎨    | user experience  |
| `RDY`  | 👁️    | readability      |
| `DOC`  | 📖    | documentation    |
| `PRF`  | 🚀    | performance      |
| `GIT`  | 💬    | GitHub feedback  |
| `GRP`  | 📦    | grouped findings |

## Review Presentation

When summarizing findings for a human, present them in an emoji-led format:

```text
{severity_emoji} {severity} · {category_emoji} {id} · {title} ({confidence}%) · {file}:{line}
```

Examples:

```text
🔴 P1 · 🛡️ SEC-1 · SQL injection vulnerability (95%) · src/db.ts:45
🟠 P2 · 🏗️ ARC-1 · Circular dependency (88%) · src/modules/a.ts:12
🟡 P3 · 🧪 TST-2 · Missing edge case test (82%) · tests/api.test.ts:78
```

For GitHub findings, append the author when available:

```text
🟠 P2 · 💬 GIT-1 · Consider using constants (90%) · src/config.ts:23 (@reviewer)
```

If multiple findings collapse into one root cause, you may present a grouped
summary:

```text
╭──────────────────────────────────────────────────────────────────────────╮
│ 🟠 P2 · 📦 GRP-1 · Inconsistent error handling (3 findings)              │
╰┬─────────────────────────────────────────────────────────────────────────╯
 ├─ 🟠 P2 · 👁️ RDY-1 · Missing error check (85%) · src/api.ts:23
 ├─ 🟡 P3 · 👁️ RDY-2 · Silent failure (82%) · src/api.ts:45
 └─ 🟡 P3 · 👁️ RDY-3 · No error logging (80%) · src/api.ts:67
```

Sort summaries by severity first, then by confidence. Include a legend when the
review is long enough that readers would benefit from one.

## Actionability

Prefer findings that are specific, reproducible, and cheap enough to act on in
the current change. Cap output at roughly 8 findings for a normal-sized diff —
prioritize ruthlessly rather than dumping everything.

Avoid:

- Speculative concerns without concrete evidence in the diff.
- Style preferences that linters or formatters already enforce.
- Suggesting rewrites of working code unless there's a clear maintainability or
  correctness risk.
- Flagging pre-existing TODO/FIXME comments that aren't part of this change.
- Issues outside the review scope (e.g., unrelated files, hypothetical future
  requirements).

## Summary

End every review with a short verdict:

```text
**Verdict:** <one-line recommendation>
<count> P1 · <count> P2 · <count> P3 · <count> P4
```

The one-line recommendation should be one of:

- **Ship it** — no findings, or only P4 nits.
- **Ship with fixes** — P3 or below; nothing blocking.
- **Needs changes** — at least one P2 that should be resolved before merge.
- **Blocked** — at least one P1; do not merge.

If cross-cutting themes emerged (e.g., "error handling is inconsistent across
three files"), call them out in the verdict as a single sentence.

## Reviewer Lenses

Load only the lenses that matter for the current diff:

- [architecture](references/architecture.md)
- [documentation](references/docs.md)
- [GitHub review threads](references/github-review-threads.md)
- [performance](references/performance.md)
- [readability](references/readability.md)
- [security](references/security.md)
- [tests](references/tests.md)
- [user experience](references/ux.md)
