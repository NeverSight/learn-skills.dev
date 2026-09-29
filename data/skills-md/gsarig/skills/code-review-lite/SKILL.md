---
name: code-review-lite
description: "Abbreviated code review for small or low-stakes code changes. Skips requirements gathering. Skips the linter in PR mode (CI runs it). Focuses on correctness against obvious intent, readability, and pattern consistency. For large or security-sensitive diffs, use code-review-deep instead."
when_to_use: "Use for code reviews on small, low-stakes diffs (no security paths, under ~500 lines). Invoked directly with a PR URL or diff file path, or dispatched by `/code-review`. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[PR URL | path to diff file] [--source=...] [--pr=<URL>] [--file=<path>] [--lint]"
effort: high
allowed-tools: Bash(git *) Bash(gh *) Bash(composer *) Bash(npm *) Bash(make *) Read Grep
---

## Steps

### 1. Source and diff

Read `~/.claude/skills/code-review/references/review-shared.md` and follow its source detection and diff fetching sections. If `--source` and the corresponding identifier args were passed, use those and skip any prompting.

### 2. Lint (conditional)

Skip the linter when source mode is `pr` and `--lint` was not passed (CI runs the linter on the PR).

Otherwise run the linter per the linter detection section of the shared doc.

### 3. Load language references (conditional)

If any changed path matches `\.(js|jsx|ts|tsx|mjs|cjs)$`, read `~/.claude/skills/code-review/references/js-security.md`.

### 4. GitHub Actions hash verification (conditional)

If the diff contains any line matching `^\+\s*uses:\s+\S+@[0-9a-f]{40}`, run the verification per the shared doc.

### 5. Review

Read `~/.claude/skills/code-review/references/review-checklist.md` first for general principles.

Focus on:

- Correctness against obvious intent. Lite reviews do not gather requirements; reason about what the diff is trying to do from the code itself.
- Readability and naming.
- Matches existing patterns in the file or nearby files.
- Dead code, debug artefacts, accidental scope creep.
- Security issues that are visible without deep analysis (hardcoded secrets, obvious injection, missing input validation on user-facing entry points).

Do not deep-dive architecture or push for refactors beyond the diff. Honour the common review rules in the shared doc.

### 6. Output

Format per the output section of `~/.claude/skills/code-review/references/review-shared.md`.
