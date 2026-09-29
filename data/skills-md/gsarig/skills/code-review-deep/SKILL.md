---
name: code-review-deep
description: "Full code review for large or security-sensitive changes. Gathers requirements first, loads all relevant language references, runs the linter where applicable, applies the full review checklist with security as the top priority."
when_to_use: "Use for code reviews on large diffs (500+ lines) or any change touching security-sensitive paths (auth, crypto, sql, migration, secret, token, .env). Invoked directly with a PR URL or diff file path, or dispatched by `/code-review`. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[PR URL | path to diff file] [--source=...] [--pr=<URL>] [--file=<path>] [--requirements=<text>] [--lint]"
effort: xhigh
allowed-tools: Bash(git *) Bash(gh *) Bash(composer *) Bash(npm *) Bash(make *) Read Grep
---

## Steps

### 1. Source and diff

Read `~/.claude/skills/code-review/references/review-shared.md` and follow its source detection and diff fetching sections. If `--source` and the corresponding identifier args were passed, use those and skip any prompting.

### 2. Gather requirements

If `--requirements=...` was passed, use that text as the requirements. Otherwise ask:

> "Do you have specific requirements I should keep in mind? (e.g. a ticket description, acceptance criteria, or expected behaviour)"

Wait for the response. If declined, proceed without requirements but note in the final output that correctness was assessed against inferred intent only.

### 3. Lint (conditional)

Skip the linter when source mode is `pr` and `--lint` was not passed (CI runs the linter on the PR).

Otherwise run the linter per the linter detection section of the shared doc.

### 4. Load language references (conditional)

If any changed path matches `\.(js|jsx|ts|tsx|mjs|cjs)$`, read `~/.claude/skills/code-review/references/js-security.md`.

### 5. GitHub Actions hash verification (conditional)

If the diff contains any line matching `^\+\s*uses:\s+\S+@[0-9a-f]{40}`, run the verification per the shared doc.

### 6. Review

Read `~/.claude/skills/code-review/references/review-checklist.md` and apply every principle.

Priorities in order:

1. **Security**: always flag, even if unrelated to the change. Include unrelated findings in the dedicated section of the output.
2. **Correctness**: does it fulfil the supplied requirements? If no requirements were supplied, assess against inferred intent and say so.
3. **Best practices**.
4. **Reusability and extensibility**.
5. **Simplicity**: flag overengineering as well as under-engineering.

Apply the common review rules from the shared doc (review only changed lines, surface project-wide patterns separately, never run tests, never run auto-fixers).

### 7. Output

Format per the output section of `~/.claude/skills/code-review/references/review-shared.md`.
