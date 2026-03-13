---
name: comprehensive-review
description: "Comprehensive code review using parallel specialized subagents. Use when you want a thorough code review covering architecture, security, performance, code quality, requirements compliance, and bugs. Works with GitHub PR links OR local branch changes. If a PR URL is provided, fetches PR details and can post comments. If no PR is provided, reviews the diff between the current branch and its base branch plus any uncommitted changes. IMPORTANT: this skill is costly, don't use it unless user explicitly requested to use this skill."
disable-model-invocation: true
metadata:
  version: 1.0.0
---

# Comprehensive Code Review

Run parallel specialized code reviews via subagents, covering architecture, security, performance, code quality, requirements compliance, and bugs. Merge findings and let the user act on them. Works with both GitHub PRs and local branch diffs.

## Workflow

### Step 1: Determine review mode

Check if the user provided a GitHub PR link.

- **PR mode**: A PR URL is provided matching `https://github.com/<OWNER>/<REPO>/pull/<PR_NUMBER>`. Extract owner, repo, and PR number.
- **Local mode**: No PR URL provided. The review will be based on the diff between the current branch and its base branch, plus any uncommitted changes.

### Step 2: Fetch diff and task description via subagent

Call a subagent to gather all change details, save the diff, and checkout the correct branch.

**CRITICAL**: You MUST spawn a subagent for this step. Do NOT perform the diff-gathering, branch detection, or complexity assessment yourself. Do NOT read the file `<SKILL_DIRECTORY>/fetch-diff.md` yourself. The subagent must read it and follow its instructions.

Construct the subagent prompt as follows:

```
Read the file `<SKILL_DIRECTORY>/fetch-diff.md` for detailed instructions, then follow them.

Mode: <PR mode or Local mode>
<If PR mode: Owner: <OWNER>, Repo: <REPO>, PR Number: <PR_NUMBER>>
```

Use a subagent tool to spawn the subagent. Use a cheap/fast model since this is a data-gathering task that doesn't require deep reasoning.

The subagent will return:
- **Diff file path**: absolute path to the saved diff file (must start with `/`, e.g. `/tmp/review-diff-feature.patch`)
- **Title**: the PR title or summary from commits
- **Description**: comprehensive task description with all requirements
- **Complexity**: one of `simple`, `medium`, or `hard`

Remember these values for use in subsequent steps.

### Step 3: Run specialized reviews

The review strategy depends on the **complexity** returned by the fetch-diff subagent.

#### Review Criteria and Instruction Files

Each review criterion has a corresponding instruction file inside this skill's directory:

| Review criterion | Instruction File |
|-------------|-----------------|
| architecture | `criteria/architecture.md` |
| security | `criteria/security.md` |
| performance | `criteria/performance.md` |
| code-quality | `criteria/code-quality.md` |
| requirements-compliance | `criteria/requirements-compliance.md` |
| bugs | `criteria/bugs.md` |

#### Strategy A: Simple complexity

For **simple** PRs, perform the review yourself (the root agent) without calling subagents.

1. Read **all 6** criteria instruction files from `<SKILL_DIRECTORY>/criteria/`.
2. Read the diff file.
3. Apply all criteria to review the change yourself, producing findings in the same format as subagents would.

#### Strategy B: Medium complexity

For **medium** PRs, launch **6 parallel subagent calls** — one per review criterion.

**CRITICAL**: You MUST spawn subagents for this step. Do NOT read the criteria instruction files yourself. Do NOT perform the reviews yourself. Each subagent must read its own instruction file.

Use a subagent tool to spawn each subagent. Use the most powerful models available. Use different models from different providers for different criteria to get diverse perspectives.

Construct prompts for subagents as follows:

```
Read the file `<INSTRUCTION_FILE>` for detailed review instructions, then follow them to review the following change.

## <title>

### Task Description
<task description>

### Diff
Read the diff from file: <absolute path to diff file>
```

Where `<INSTRUCTION_FILE>` is the absolute path to the instruction file (e.g. `<SKILL_DIRECTORY>/criteria/architecture.md`).

#### Strategy C: Hard complexity

For **hard** PRs, launch **2 parallel subagent calls per criterion** (12 total) — one per criterion per model, using 2 different models from different providers for diverse perspectives.

**CRITICAL**: You MUST spawn subagents for this step. Do NOT read the criteria instruction files yourself. Do NOT perform the reviews yourself. Each subagent must read its own instruction file.

**Model selection**: Choose exactly 2 of the most powerful models available from different providers. If only 1 provider is available, use it for all 6 calls (fall back to Strategy B behavior).

Use a subagent tool to spawn each subagent.

For each of the 6 criteria, launch 2 subagent using powerful models from different providers. 
Use following prompt:

```
Read the file `<INSTRUCTION_FILE>` for detailed review instructions, then follow them to review the following change.

## <title>

### Task Description
<task description>

### Diff
Read the diff from file: <absolute path to diff file>
```

Where `<INSTRUCTION_FILE>` is the absolute path to the instruction file (e.g. `<SKILL_DIRECTORY>/criteria/architecture.md`).

All 12 calls should be launched in parallel.

### Step 4: Merge results

Compile all findings into a single deduplicated list. For **simple** PRs, you already have all findings from your self-review. For **medium** and **hard** PRs, collect findings from all subagent responses.

1. Collect all findings from each review (self-review or subagent responses).
2. Group findings by file and line number.
3. Merge issues that describe the same problem (same file, similar line range, same category). When merging, combine their review types. For **hard** PRs, findings from different models on the same criterion that agree strengthen confidence; findings from only one model should be noted as lower confidence.
4. Keep the best description and suggested fix from among duplicates.
5. Sort by priority (P0 first), then by file path.
6. Filter out any false positives (if a subagent itself said that it's not a real issue or you're 100% sure it's not a real issue).

```
## Comprehensive Review Findings

| # | Priority | Issue | File:Line | Review type |
|---|----------|-------|-----------|------------|
| 1 | P0 | Description | path:line | architecture(opus-4-6-think), security(gpt-5-3-codex) |
| 2 | P1 | Description | path:line | bugs(opus-4-6-think) |
| ... | | | | |

### Details

#### 1. [P0] Issue title
**File:** `path/to/file:line`
**Review type:** architecture(opus-4-6-think), security(gpt-5-3-codex)

Description and why it matters.

**Suggested fix:**
\`\`\`
code
\`\`\`
```

### Step 5: Ask user how to handle each finding

Ask questions to let the user decide what to do with each finding:

- Use one question per finding, presenting each with its number, priority, and short description.
- **PR mode options**: "Fix", "Post comment", "Ignore"
- **Local mode options**: "Fix", "Ignore"
- Use tool to ask questions if available. Ask all questions with on tool call if tool allows asking multiple questions at once. Otherwise, ask sequentially.
- If no tool available, ask all questions at once with regular message to user.

### Step 6: Apply fixes for issues marked "Fix"

For each finding the user chose "Fix":

1. Read the relevant file and understand the surrounding context.
2. Apply the suggested fix (or an appropriate fix if the suggestion is incomplete).
3. After all fixes are applied, present a summary of changes made.

### Step 7: Post selected issues as PR comments (PR mode only)

**Skip this step entirely if no findings were marked "Post comment".**

Only applies in PR mode. Use the GitHub reviews API to post line-specific comments for selected issues:

```bash
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews \
  --method POST \
  -f event='COMMENT' \
  -f body='## Comprehensive Code Review

### Findings Summary

| Priority | Issue | Location | Review type |
|----------|-------|----------|------------|
| P0 | ... | file:line | code-quality(gpt-5-3-codex) |

### Recommendation
[Concise recommendation]' \
  --input - << 'EOF'
{
  "comments": [
    {
      "path": "path/to/file.ts",
      "line": 42,
      "side": "RIGHT",
      "body": "**[P0] Issue Title** (review type: code-quality(gpt-5-3-codex))\n\nDescription.\n\n**Suggested fix:**\n```\ncode\n```"
    }
  ]
}
EOF
```

Requirements for the API call:
- Use `/pulls/{PR}/reviews` endpoint (NOT `/pulls/{PR}/comments`)
- `event` must be `COMMENT`
- `line` = line number in the NEW version of file (from the diff's `+` side)
- `side` = `RIGHT` for new/modified code, `LEFT` for deleted code
- `path` = relative to repo root
- Only include comments for issues the user selected as "Post comment"
- Include the review type with model name (e.g., `code-quality(gpt-5-3-codex)`, `security(opus-4-6-think)`) in each comment
