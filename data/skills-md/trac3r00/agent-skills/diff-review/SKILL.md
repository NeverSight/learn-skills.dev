---
name: diff-review
description: Fast mechanical review pass over a unified diff before a human or agent reads it. Flags debug output left in production paths, TODO/FIXME/HACK markers added by the change, trivial test assertions that prove nothing, and deleted tests. Chains sibling gates (secret-gate, comment-checker) so one command runs the entire mechanical layer. Deterministic, stdlib-only, reads a unified diff from stdin.
when_to_use: As the first pass on any diff — agent-generated or human — before code review, before merge, or as a CI gate. It catches the low-level debris that wastes reviewer attention. NOT a semantic review; it does not judge logic, only mechanical red flags.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [code-review, diff, ci-gate, quality, automation]
---

# Diff Review

The mechanical layer of code review, automated: run it on every diff and the
human (or agent) reviewer only sees what actually needs judgment.

## Commands

```bash
git diff | python3 scripts/diff_review.py
git diff main...HEAD | python3 scripts/diff_review.py --json
git diff | python3 scripts/diff_review.py --tools-dir skills/
git diff --cached | python3 scripts/diff_review.py --fail-over 3
```

## Detects

| Kind | What it catches |
|---|---|
| `debug-output` | `print(`, `console.log(`, `puts`, `pprint`, `dbg!` added to non-test code |
| `unresolved-marker` | `TODO`, `FIXME`, `HACK`, `XXX`, `WIP`, `REMOVE ME` added by the change |
| `trivial-assertion` | `assert True`, `assert 1 == 1` — tests that can never fail |
| `test-deleted` | `def test_` / `it(` lines removed without replacement |
| `secret-gate-findings` | credential leaks (when chained via `--tools-dir`) |
| `comment-checker-findings` | unjustified comments (when chained via `--tools-dir`) |

## Chaining ecosystem gates

`--tools-dir <skills-root>` looks for `secret-gate/scripts/secret_gate.py` and
`comment-checker/scripts/comment_checker.py` in that directory and feeds them
the added lines. Their findings appear as `*-findings` entries with the first
evidence line. Both are optional — chain whatever is installed.

## Pairs with

`merge-quiz` (the human comprehension gate after the mechanical pass),
`remove-ai-slops` (structural cleanup beyond what a diff pass can see),
`verification-before-completion` (the evidence-before-claims wrapper around
the whole workflow).
