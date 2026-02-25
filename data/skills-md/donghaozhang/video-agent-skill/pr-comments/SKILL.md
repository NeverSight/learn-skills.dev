---
name: pr-comments
description: Export, preprocess, and fix GitHub PR review comments. Use when user wants to export PR comments, evaluate code reviews, or fix review feedback from CodeRabbit/Gemini bots.
argument-hint: <action> [args...]
disable-model-invocation: true
allowed-tools: Bash(gh *), Bash(jq *), Bash(mkdir *), Bash(sed *), Read, Edit, Glob, Grep
---

# PR Comments Skill

Export GitHub PR review comments, preprocess for evaluation, and fix or reject each review.

## Actions

### 1. Export: `/pr-comments export <owner/repo> <pr-number>`

Export all review comments from a PR to individual markdown files.

```bash
bash .claude/skills/pr-comments/scripts/export.sh $1 $2 $3
```

**Output:** `.github/pr-history/pr-{number}/` with one file per comment.

### 2. Preprocess: `/pr-comments preprocess <input-dir>`

Clean exported comments for agentic evaluation (removes `<details>` blocks, adds evaluation prompt).

```bash
bash .claude/skills/pr-comments/scripts/batch-preprocess.sh $1
```

**Output:** `{input-dir}-tasks/` with cleaned task files.

### 3. Analyze: `/pr-comments analyze <tasks-dir>`

Show comments grouped by source file with recommended processing order.

```bash
bash .claude/skills/pr-comments/scripts/analyze.sh $1
```

**Output:** Table showing which files have multiple comments and line numbers (sorted for bottom-up fixing).

### 4. Fix: `/pr-comments fix <task-file.md>`

Evaluate a single PR review comment. Read the source file, determine if valid, then fix or explain.

Follow instructions in [review-fix.md](review-fix.md).

### 5. Batch: `/pr-comments batch <tasks-dir>`

Process all task files in a directory. **Groups comments by source file** and fixes bottom-up to avoid line number shifts.

**Critical:** Multiple comments often target the same file. Batch mode:
1. Groups tasks by source file
2. Sorts by line number descending (bottom-up)
3. Fixes all comments for one file before moving to next

Follow instructions in [review-batch.md](review-batch.md).

### 6. Resolve: `/pr-comments resolve <owner/repo> <pr-number> <comment-id> [task-file]`

Resolve a PR review thread on GitHub and move task to completed folder.

```bash
bash .claude/skills/pr-comments/scripts/resolve-thread.sh $1 $2 $3 $4
```

**Example:**
```bash
/pr-comments resolve donghaozhang/qcut 102 2742327370 .github/pr-history/pr-102-tasks/comment.md
```

**What it does:**
1. Resolves the PR conversation thread on GitHub
2. Moves the task file to `{tasks-dir}_completed/`

**When to use:**
- After FIXED → Resolve and move to completed
- After ALREADY_FIXED → Resolve and move to completed
- NOT_APPLICABLE → Don't resolve (leave comment explaining why)

## Complete Workflow

```bash
# Step 1: Export comments from PR
/pr-comments export donghaozhang/qcut 102

# Step 2: Preprocess into task files
/pr-comments preprocess .github/pr-history/pr-102

# Step 3: Analyze (see file groupings)
/pr-comments analyze .github/pr-history/pr-102-tasks

# Step 4a: Fix single comment
/pr-comments fix .github/pr-history/pr-102-tasks/comment.md

# Step 4b: Or batch fix all
/pr-comments batch .github/pr-history/pr-102-tasks

# Step 5: Resolve thread and move task to completed
/pr-comments resolve donghaozhang/qcut 102 2742327370 .github/pr-history/pr-102-tasks/comment.md
```

## Output Structure

```
.github/pr-history/
├── README.md
├── pr-102/                    # Raw exported comments
│   ├── coderabbitai[bot]_file_L42_123.md
│   └── gemini-code-assist[bot]_file_L50_456.md
├── pr-102-tasks/              # Preprocessed for evaluation (pending)
│   └── coderabbitai[bot]_file_L50_456.md
└── pr-102-tasks_completed/    # Resolved tasks
    └── coderabbitai[bot]_file_L42_123.md
```

## Supporting Files

- [review-fix.md](review-fix.md) - Single comment evaluation instructions
- [review-batch.md](review-batch.md) - Batch processing instructions

## Requirements

- GitHub CLI (`gh`) - installed and authenticated
- `jq` - JSON processing
