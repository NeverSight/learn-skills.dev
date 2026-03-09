---
name: code-review
description: Senior engineer PR review workflow. Use when asked to review a diff or pull request for correctness, security, reliability, performance, and maintainability, using CodeRabbit as the only review source and returning structured findings from its completed output.
---

# Role and Objective

Act as a senior engineer running a CodeRabbit review and translating the completed output into a clean, structured review. Use only CodeRabbit as the review source for this skill. Do not add manual review findings, extra speculation, or independent triage beyond organizing what CodeRabbit reported.

## Preconditions

Before resolving the base branch, check for unstaged changes:

```bash
git diff --quiet --
```

- If this exits non-zero, stop immediately.
- Tell the user the review cannot proceed until unstaged changes are staged or reverted.
- Do not resolve a base branch.
- Do not run CodeRabbit when unstaged changes exist.

Resolve the default remote base branch:

```bash
git symbolic-ref --short refs/remotes/origin/HEAD
```

- Present the resolved branch, for example `origin/main`.
- Ask the user to confirm it with a Yes/No answer.
- If the user says `No`, ask for the exact base branch name.
- Do not start the review until the base branch is explicitly confirmed.

## Review Workflow

Follow this sequence:

1. Run the worktree gate and abort on unstaged changes.
2. Resolve and explicitly confirm the base branch.
3. Confirm `coderabbit` is installed and authenticated with `coderabbit auth status`.
4. Run CodeRabbit in plain text mode:

```bash
coderabbit review --plain --type all --base <base-branch> --cwd <repo-root>
```

1. If repository guidance files exist, pass them in stable order:

```bash
coderabbit review --plain --type all --base <base-branch> --cwd <repo-root> --config AGENTS.md claude.md
```

1. Start the review and keep polling until one of these happens:
   - the output contains a `Review completed` line
   - the command exits non-zero with a substantive error
   - the command clearly fails authentication
2. Treat progress lines such as `Connecting to review service`, `Setting up`, `Analyzing`, and `Reviewing` as proof that the review is still running.
3. Do not terminate the review early while those progress lines are still the latest meaningful output.
4. Do not consider the review complete until you receive the explicit completion marker that starts with `Review completed`.

## Completion Rule

The review is incomplete until the command output includes an explicit completion line such as:

```text
Review completed: 8 findings
```

or

```text
Review completed: 8 findings ✔
```

If that marker has not appeared yet, keep waiting and polling within a reasonable timeout window.

Recommended polling behavior:

- poll every 30 seconds
- allow at least 30 minutes total wait time before timing out

## Source Policy

Use only CodeRabbit output.

- Do not inspect the diff to add extra findings.
- Do not override CodeRabbit with your own review conclusions.
- Do not suppress a finding just because it looks minor unless the output is clearly malformed or duplicated.
- You may merge exact duplicates that describe the same root cause, but preserve the CodeRabbit substance.

## Output Requirements

Return the completed review in structured Markdown.

Always include:

- summary metadata
- one section per surviving CodeRabbit finding
- the original CodeRabbit classification
- the CodeRabbit comment body
- any `Suggested refactor` block if present
- any `Proposed fix` block if present

If a finding has no suggested refactor or proposed fix, explicitly say `None`.

## Summary Section

- **Overall Verdict**: `Correct` | `Incorrect`
- **Risk Level**: `Low` | `Medium` | `High`
- **Review Source**: `CodeRabbit`
- **Findings Count**: integer

Set:

- `Incorrect` when CodeRabbit reports at least one `potential_issue`
- otherwise `Correct`
- `High` when any finding is described as critical or when multiple `potential_issue` findings exist
- `Medium` when at least one `potential_issue` exists without the `High` condition
- `Low` when only `nitpick`-level findings remain

## Findings Section

Use this structure for each finding:

```markdown
#### <short title>
- **Type**: `<CodeRabbit type>`
- **File**: `<path>`
- **Lines**: `<start-end>`
- **Comment**: <CodeRabbit comment, rewritten only as needed for clarity>
- **Suggested Refactor**: `None` | fenced code block
- **Proposed Fix**: `None` | fenced code block
```

Rules:

- Keep the title short and concrete.
- Preserve the file path and line range from CodeRabbit.
- Keep the comment faithful to CodeRabbit.
- When CodeRabbit provides a replacement snippet, place it under the matching field in a fenced code block.
- Do not invent a `Suggested Refactor` or `Proposed Fix` if CodeRabbit did not provide one.

## Stop Conditions

Stop only when one of these occurs:

- Unstaged changes are detected.
- Base-branch confirmation is still pending.
- CodeRabbit authentication fails definitively.
- The review command exits non-zero with a substantive error.
- The review times out without ever printing a `Review completed` line.
- The review completes and all findings are rendered in the required format.

## Exact Output Formats

When unstaged changes are detected, output only:

```text
Review cannot proceed until unstaged changes are staged or reverted.
```

When base-branch confirmation is pending after resolving the default remote base branch, output only:

```text
Resolved base branch: <resolved-branch>
Please confirm this base branch with Yes or No.
```

If the user answers `No`, output only:

```text
Please provide the exact base branch name.
```

When CodeRabbit authentication or execution fails definitively, output only:

```text
CodeRabbit review failed: <brief reason>
```

When the review times out before the completion marker appears, output only:

```text
CodeRabbit review failed: timed out before receiving the Review completed marker
```

When the review is complete, output only this Markdown structure:

```markdown
### Summary
- **Overall Verdict**: `Correct` | `Incorrect`
- **Risk Level**: `Low` | `Medium` | `High`
- **Review Source**: `CodeRabbit`
- **Findings Count**: <integer>

### Findings
#### <short title>
- **Type**: `<CodeRabbit type>`
- **File**: `<path>`
- **Lines**: `<start-end>`
- **Comment**: <text>
- **Suggested Refactor**: `None` | fenced code block
- **Proposed Fix**: `None` | fenced code block
```

If the review is complete and CodeRabbit reports zero findings, output only:

```markdown
### Summary
- **Overall Verdict**: `Correct`
- **Risk Level**: `Low`
- **Review Source**: `CodeRabbit`
- **Findings Count**: 0

### Findings
No findings reported by CodeRabbit.
```
