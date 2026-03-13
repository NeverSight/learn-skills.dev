---
name: review-pr
description: End-to-end PR review orchestrator. Fetches GitHub PR diffs via .diff URLs to summarize code changes, triggers CI review using the review-ci skill, and, when CI exposes a preview URL, runs review-ui against that URL and relevant scenarios. Use when the user wants a holistic review of a GitHub Pull Request including code, CI pipelines, and (if possible) the deployed UI.
disable-model-invocation: true
metadata:
  author: Saurabh Daware (https://srbh.dev)
  version: 0.0.1
---

# Review PR

Your role is to review the code, ci checks, and ui related to the code changes. For CI and UI reiew, you are an orchestrator that calls the existing relevant skills

## Arguments

- **PR_URL**: Full GitHub Pull Request URL, e.g. `https://github.com/abelljs/abell/pull/190`
- **SHOULD_REVIEW_UI (only works if preview URL is available on PR)**: Should the UI be reviewed if preview URL is available on PR

If the user does not provide `PR_URL` or `SHOULD_REVIEW_UI`, use **AskQuestion** (or ask conversationally) to obtain it.

## Instructions

Perform a **holistic review of a GitHub Pull Request** by:

1. Fetching the PR `.diff` and doing a sanity **Code Review** (Use `{{PR_URL}}.diff` to fetch the diff. E.g. https://github.com/abelljs/abell/pull/190.diff). Use it smartly with grep if needed since diffs can sometimes be large.
2. Calling the **`/review-ci`** skill to review CI pipelines. Pass the PR_URL to it.
3. If CI reveals a **preview URL** and SHOULD_REVIEW_UI is true, calling **`/review-ui`** with that preview URL and scenario-based on code changes in diff
4. Producing a single consolidated report with **Code Review**, **CI Review**, and **UI Review** sections. Follow the Output Format below.

This skill is an **orchestrator**: it coordinates other skills and tools rather than re-implementing them.

## Output Format

<OutputFormat>
# PR Review

## Code Review

[list of concerns in diff]

## CI Review

[Output as mentioned in `review-ci` skill]

## UI Review

[Output as mentioned in `review-ui` skill. Or whether it was skipped due to unavailability of preview URL]
</OutputFormat>
