---
name: comment-checker
description: Flags newly written comments and docstrings in files or diffs so an agent must justify or remove them — BDD markers, lint/type directives, license headers, shebangs, and TODO/FIXME markers auto-pass. A standalone CLI port of oh-my-opencode's comment-checker hook, usable by any agent or CI without the OMO harness.
when_to_use: Enforce a no-unjustified-comments discipline on agent-written code — as a pre-commit gate over a diff, a CI check, or a self-check after editing. NOT a style linter; it only finds comments that need a justification decision.
version: 1.0.0
license: MIT (detection rules adapted from oh-my-opencode / oh-my-claudecode)
metadata:
  agentskills:
    tags: [comments, code-quality, ci-gate, diff, discipline]
---

# Comment Checker

Agent-written code accumulates narration comments a human never would. This
skill flags every new comment or docstring that is not self-justifying, so the
author must either justify it (complex algorithm, security, regex, public API)
or delete it and make the code clearer instead.

## Commands

```bash
python3 scripts/comment_checker.py src/foo.py src/bar.ts   # scan whole files
git diff | python3 scripts/comment_checker.py --diff        # only added lines
git diff main... | python3 scripts/comment_checker.py --diff --fail-over 0  # CI gate
python3 scripts/comment_checker.py --json --diff < changes.patch
```

## What auto-passes (never flagged)

- Shebang lines (`#!` on line 1)
- BDD structure comments: given / when / then / arrange / act / assert
- Type-checker and linter directives: `noqa`, `type:`, `eslint-disable`,
  `@ts-expect-error`, `clippy::`, `nolint`, `biome-ignore`, coverage markers, ...
- Copyright / license headers
- TODO / FIXME / HACK / XXX / NOTE / REVIEW markers

Everything else is reported with file:line and the comment text.

## Handling a flag

Priority order, same as the original hook:

1. Comment existed before your change - keep, note it is pre-existing.
2. Necessary comment - justify it: complex algorithm, security, performance,
   regex, math, or public-API docstring.
3. Unnecessary - remove it and make the code self-explanatory instead.
   Comment-based section dividers (`# ----`) mean the file is too long: split it.

## Languages

C-family (js/ts/jsx/tsx/java/c/cpp/cs/rust/swift/kotlin/go), hash-family
(python + docstrings, ruby, shell, yaml, toml), html/xml, sql, lua.
