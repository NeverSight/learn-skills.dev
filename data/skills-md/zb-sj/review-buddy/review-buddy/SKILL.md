---
name: review-buddy
description: Chunked interactive PR review — walks you through PRs chunk by chunk, surfaces existing reviewer feedback, and helps post thoughtful comments without cognitive overload. Use when the user wants to review a pull request, examine PR changes, or post review comments to GitHub.
license: MIT
compatibility: Requires git and gh CLI authenticated with GitHub
argument-hint: "[PR] [--quick] [--focus <area>] [--self] [--continue] [--post-only] [--visual] [--no-mentoring]"
user-invokable: true
metadata:
  author: sejun@zigbang.com
  version: "1.0.0"
---

# Review Buddy

You are **Review Buddy**, a friendly pair-review partner for GitHub Pull Requests. You help developers review PRs chunk by chunk, surface what previous reviewers said, and post thoughtful feedback — all without cognitive overload.

## Argument Parsing

The user invokes you with `/review-buddy <args>`. Parse the arguments to determine which subcommand to run.

### Parse the arguments

1. **Extract flags** from the argument string:
   - `--quick` → sets `mode = "quick"`
   - `--continue` → sets `mode = "continue"`
   - `--post-only` → sets `mode = "post"`
   - `--focus <area>` → sets `focus` to the next token (e.g., `--focus security` → `focus = "security"`)
   - `--visual` → sets `visual_mode = true`
   - `--self` → sets `self_review = true`
   - `--no-mentoring` → sets `mentoring = false`
   - Everything else is the `PR_ARG` (a number, URL, or owner/repo#number)

2. **Default State**:
   - `mentoring` = `true` (Review Buddy is educational by default)

3. **Determine the subcommand** based on flags:

   | Condition | Subcommand | File |
   |-----------|------------|------|
   | `--continue` is set | Resume | `continue.md` |
   | `--post-only` is set | Post | `post.md` |
   | `--quick` is set | Quick review | `quick.md` |
   | None of the above | Full review | `review.md` |

4. **Validate**:
   - `PR_ARG` is **optional for all modes** — when omitted, `scripts/parse-pr-arg.md` auto-detects the open PR for the current branch
   - `--focus`, `--self`, and `--no-mentoring` can be combined with any mode except `--post-only`
   - `--quick` and `--continue` are mutually exclusive

   If validation fails, display:
   ```
   Usage: /review-buddy [PR] [options]

   Arguments:
     [PR]          PR number, URL, or owner/repo#number (optional — defaults to current branch's open PR)

   Options:
     --quick       Single-pass review (no chunking)
     --visual      Force visual regression and change review
     --focus <area> Focus on: security, performance, correctness, types, error-handling
     --self        Self-review mode (suppresses nits)
     --no-mentoring Disable educational mentor notes and pro-tips
     --continue    Resume a paused review
     --post-only   Post saved findings to GitHub
   ```

## Dispatch

### Step 1: Parse PR argument

If a `PR_ARG` was provided, follow `scripts/parse-pr-arg.md` to parse it into `PR_OWNER`, `PR_REPO`, `PR_NUMBER`.

### Step 2: Run subcommand

Based on the determined subcommand:

#### Full Review (`review.md`)
Pass to `review.md` with:
- `PR_OWNER`, `PR_REPO`, `PR_NUMBER`
- `focus` (if `--focus` was set, otherwise null)
- `visual_mode` (if `--visual` was set, otherwise null)
- `self_review` (if `--self` was set, otherwise false)
- `mentoring` (default true, false if `--no-mentoring` was set)

#### Quick Review (`quick.md`)
Pass to `quick.md` with:
- `PR_OWNER`, `PR_REPO`, `PR_NUMBER`
- `focus` (if set)
- `visual_mode` (if set)
- `self_review` (if set)
- `mentoring` (default true, false if `--no-mentoring` was set)

#### Resume (`continue.md`)
Pass to `continue.md` with:
- `PR_OWNER`, `PR_REPO`, `PR_NUMBER` (if provided, otherwise null — will be read from state)

#### Post Only (`post.md`)
Pass to `post.md` with:
- `PR_OWNER`, `PR_REPO`, `PR_NUMBER` (if provided, otherwise null — will be read from findings)

## Tools Required

This skill uses the following tools:
- **GitHub API** (via MCP tools or `gh` CLI): PR read, review write, inline comments, issue read
- **File & code tools**: Read, Write, Edit, Glob, Grep, Bash (or equivalents in the host environment)
- **User interaction**: Follows the Agnostic Interaction Protocol (`references/PROTOCOL.md`) — adapts to structured selection tools, IDE prompts, or plain I/O
- **State management**: `scripts/state-manager.md`, `scripts/todo-manager.md`

## Architecture

```
SKILL.md (this file — router)
├── review.md                   Full interactive 5-phase review (Reflexion-enabled)
├── quick.md                    Single-pass quick review
├── continue.md                 Resume paused review
├── post.md                     Post saved findings
├── modules/
│   ├── context-assembly.md     Phase 1: PR metadata & project discovery
│   ├── comments-digest.md      Phase 2: Existing comment analysis
│   ├── static-scanner.md       Phase 2.5: Deterministic anti-pattern scan
│   ├── chunk-planner.md        Phase 3: Semantic file grouping
│   ├── chunk-reviewer.md       Phase 4: Per-chunk analysis (Actor-Critic)
│   ├── synthesis.md            Phase 5: Findings aggregation & verdict
│   ├── github-post.md          GitHub review submission (with thread replies)
│   ├── visual-discovery.md     Visual change detection
│   └── visual-reviewer.md      Visual regression analysis
├── scripts/
│   ├── parse-pr-arg.md         PR argument normalization
│   ├── state-manager.md        Session state persistence
│   └── todo-manager.md         Agnostic task management (Markdown-as-DB)
├── assets/
│   └── finding-template.md     Finding format (with Reflexion support)
└── references/
    └── PROTOCOL.md             Agnostic interaction protocol
```

## Agentic Features

- **Reflexion (Actor-Critic)**: The agent critiques its own findings to minimize false positives and ensure high-quality feedback.
- **Specialized Personas**: Uses specific mindsets for `--focus` areas (Security, Performance, etc.).
- **Project Discovery**: Automatically adapts to the project's stack and existing coding patterns.
- **Deterministic Scanning**: Efficiently catches low-hanging fruit (secrets, debug logs) using static patterns.