---
name: review-council
description: Run all code review tools in parallel and aggregate results into a comprehensive review report.
disable-model-invocation: true
---

## Context

- Current branch: !`git branch --show-current`
- Base branch: !`git rev-parse --verify main >/dev/null 2>&1 && echo main || echo master`
- Arguments: $ARGUMENTS

## Your task

Act as a **Code Review Orchestrator**: discover all available review-capable skills, run them in parallel via read-only sub-agents, and produce a single aggregated report.

### Pre-flight checks

1. Determine the review target:
   - If `$ARGUMENTS` is a PR number, pass it to each reviewer.
   - If `$ARGUMENTS` is a file path or set of changes, pass those directly.
   - If `$ARGUMENTS` is empty, each reviewer should review the current branch compared to the base branch.

### Step 1: Discover available review skills

Look at all skills currently available and identify every skill whose name or description indicates it can perform a code review, PR review, or security review. Exclude this skill itself (`review-council`) to avoid recursion.

### Step 2: Launch all reviewers in parallel

For each review-capable skill discovered in Step 1, launch a **read-only sub-agent** that invokes that skill via the Skill tool with `$ARGUMENTS` and returns the full review output.

All sub-agents MUST be launched **in a single message** to maximize parallelism. Sub-agents must not modify files, create commits, or push changes.

### Step 3: Collect results and aggregate

Wait for all sub-agents to complete. Produce a single report:

```
# Full Code Review Report

## Summary
[1-3 sentence overall assessment. Mention the number of reviewers run and issues found.]

## Critical Issues
[Issues flagged as critical/blocking by ANY reviewer. Deduplicate across reviewers, noting which flagged each.]

## Important Issues
[Non-blocking but significant issues. Deduplicate across reviewers.]

## Minor Issues & Suggestions
[Style, naming, minor improvements. Deduplicate across reviewers.]

## Reviewer Verdicts

| Reviewer | Verdict | Key Concerns |
|----------|---------|--------------|
| [skill name] | ... | ... |

## Detailed Reviews

### [Skill Name]
[Full verbatim output from that reviewer's sub-agent]
```

### Rules

- All sub-agents MUST be launched in parallel in a single message.
- Sub-agents are read-only — they must not modify files, create commits, or push changes.
- Do NOT skip any discovered reviewer. If one fails, report the failure in the output.
- If multiple reviewers flag the same issue (same file, same line, same concern), merge them into one entry and note all reviewers that caught it.
- If reviewers disagree on severity, use the highest. Severity ranking: Critical > Important > Minor.
- If 3+ reviewers flag the same issue, mark it with `[CONSENSUS]`.
- Include the full review output in the Detailed Reviews section, but redact any credentials, secrets, API keys, tokens, or passwords that may appear in the output.
- Keep Critical Issues short and focused on what MUST be addressed before merging.
