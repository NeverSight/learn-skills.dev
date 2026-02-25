---
name: codex-advisor
description: Get a second opinion from OpenAI Codex CLI for plan reviews, code reviews, architecture decisions, and hard problems. Use when you need external validation, want to compare approaches, or are stuck on a difficult problem.
---

# Codex Advisor

## Overview

Use OpenAI's Codex CLI as a second-opinion advisor when you need external validation on plans, code reviews, or are stuck on hard problems. This skill uses non-interactive mode (`codex exec`) for scripted/automated usage.

## When to Use

- Reviewing implementation plans before starting work
- Code review for complex or security-sensitive changes
- Architecture decisions with significant trade-offs
- Debugging problems where you've been stuck for >30 minutes
- Getting alternative approaches to a solution
- Validating assumptions about unfamiliar codebases

## Prerequisites

- OpenAI API key or ChatGPT Plus/Pro/Business account
- Codex CLI installed

### Installation

```bash
# Via npm
npm install -g @openai/codex

# Or via Homebrew
brew install --cask codex
```

### Authentication

```bash
# Option 1: API key (required for non-interactive mode in CI)
export OPENAI_API_KEY="your-key"

# Option 2: Codex-specific key for CI environments
export CODEX_API_KEY="your-key"

# Option 3: Interactive login (one-time setup)
codex --login
```

## Model Selection

Choose the right model for your task:

| Model | Best For | Use When |
|-------|----------|----------|
| `gpt-5.2` | General-purpose reasoning | Default for plan reviews, architecture questions, non-coding tasks |
| `gpt-5.2-codex` | Real-world software engineering | Code reviews, debugging, coding-specific tasks |
| `gpt-5.1-codex-max` | Extended multi-step workflows | Long-running tasks (>10 min), large migrations, complex refactors |
| `gpt-5.1-codex-mini` | Budget-conscious projects | Simple reviews when cost matters |

**Recommendation:**
- Start with `gpt-5.2` for general questions
- Use `gpt-5.2-codex` when the task is specifically about code
- Use `gpt-5.1-codex-max` for tasks involving many files or complex multi-step work

## Reasoning Effort Levels

Always use `xhigh` reasoning for thorough analysis:

| Level | Use Case |
|-------|----------|
| `xhigh` | **Default** - Deep analysis, security review, architecture decisions |
| `high` | Complex analysis when latency matters |
| `medium` | Quick responses for simple tasks |
| `low`/`none` | Not recommended for advisor use cases |

## Non-Interactive Mode

All commands use `codex exec` for non-interactive execution. This is essential for scripted usage and piping.

### Key Flags

| Flag | Purpose |
|------|---------|
| `--json` | Output JSON Lines for machine parsing |
| `-o <path>` | Save final message to file |
| `-C <path>` | Set working directory (use `-C .` for current codebase) |
| `--full-auto` | Enable file modifications (use with caution) |
| `--sandbox read-only` | Read-only sandbox (default, safest) |
| `--sandbox workspace-write` | Allow writes to workspace only |

### Output Handling

```bash
# JSON output for parsing
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" \
  --json "Your prompt" 2>/dev/null

# Save to file
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" \
  -o output.txt "Your prompt"

# Pipe input and capture output
git diff | codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" \
  "Review this diff" > review.txt 2>/dev/null
```

## Command Reference

### Plan Review

Get feedback on an implementation plan:

```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" \
  "Review this implementation plan. Identify potential issues, missing edge cases, security concerns, or better approaches:

<paste plan here>"
```

For plans involving the current codebase:

```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" -C . \
  "Review this implementation plan in the context of this codebase. Identify potential issues, conflicts with existing patterns, or better approaches:

<paste plan here>"
```

### Code Review

Review code changes for bugs, security issues, and improvements:

```bash
# Review staged changes
git diff --staged | codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" \
  "Review these changes before commit. Check for:
- Bugs or logic errors
- Security vulnerabilities
- Performance issues
- Missing error handling"

# Review a specific diff
git diff | codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" \
  "Review this diff for bugs, security issues, and improvements"

# Review with codebase context
codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" -C . \
  "Review src/auth/login.ts for bugs, security vulnerabilities, and suggest improvements"
```

### Hard Problem Solving

When stuck on a difficult problem:

```bash
codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" -C . \
  "I'm stuck on this problem: <description>

What I've tried:
1. <attempt 1>
2. <attempt 2>

Error/behavior I'm seeing: <details>

Suggest solutions or debugging approaches."
```

### Architecture Decisions

Get input on design trade-offs:

```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" -C . \
  "I need to decide between these approaches for <feature>:

Option A: <description>
Option B: <description>

Given this codebase, which approach is better and why? Consider maintainability, performance, and consistency with existing patterns."
```

### Alternative Approaches

When you want a fresh perspective:

```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" -C . \
  "Here's my current approach to <problem>: <description>

What are alternative ways to solve this? What am I missing?"
```

## Workflow Examples

### Pre-Implementation Review

```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" -C . \
  "Review this implementation plan for a user authentication system:

1. Add JWT middleware to Express routes
2. Create /auth/login and /auth/register endpoints
3. Store refresh tokens in Redis
4. Add rate limiting on auth endpoints

Identify missing pieces, security concerns, or better approaches."
```

### Pre-Commit Review

```bash
git diff --staged | codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" \
  "Review these changes for a PR. Check for:
- Bugs or logic errors
- Security vulnerabilities
- Performance issues
- Missing error handling
- Test coverage gaps

Provide specific line-by-line feedback."
```

### Long-Running Migration

For complex, multi-file refactors, use `gpt-5.1-codex-max`:

```bash
codex exec -m gpt-5.1-codex-max -c model_reasoning_effort="xhigh" -C . \
  "Help me migrate this codebase from Express to Fastify.

Review the current structure and create a detailed migration plan.
Identify all files that need changes and potential breaking changes."
```

## CI/Automation

For CI environments, use `CODEX_API_KEY`:

```bash
# In CI environment
CODEX_API_KEY=${{ secrets.CODEX_API_KEY }} \
  codex exec -m gpt-5.2-codex -c model_reasoning_effort="xhigh" \
  --json "Review this code" > review.json
```

### GitHub Actions Example

```yaml
- name: Code Review with Codex
  env:
    CODEX_API_KEY: ${{ secrets.CODEX_API_KEY }}
  run: |
    git diff origin/main...HEAD | codex exec \
      -m gpt-5.2-codex \
      -c model_reasoning_effort="xhigh" \
      -o review.txt \
      "Review this PR diff for bugs and security issues"
```

## Best Practices

### When to Use Codex Advisor

- Complex changes affecting multiple systems
- Security-sensitive code (auth, crypto, input validation)
- Performance-critical sections
- Unfamiliar codebases or languages
- When you've been stuck for >30 minutes

### When NOT to Use

- Simple, obvious changes (typos, formatting)
- Trivial bug fixes with clear solutions
- When you need to move fast on low-risk changes
- Repetitive tasks where the pattern is established

### Tips for Better Results

1. **Provide context**: Include relevant file paths, error messages, and what you've tried
2. **Be specific**: Ask focused questions rather than "review everything"
3. **Use `-C .`**: Let Codex see your codebase for context-aware advice
4. **Choose the right model**: `gpt-5.2` for general, `gpt-5.2-codex` for code, `gpt-5.1-codex-max` for complex
5. **Verify suggestions**: Always validate Codex's recommendations against your codebase

## Security Considerations

- Codex sends code to OpenAI's servers for analysis
- Review your organization's policies before sharing proprietary code
- Avoid sending sensitive credentials, API keys, or PII in code samples
- Use API keys with appropriate rate limits for usage monitoring

## Troubleshooting

### "stdin is not a terminal"

When piping data, always use `codex exec`:

```bash
# Wrong - interactive mode doesn't support piped input
git diff | codex -m gpt-5.2 "Review this..."

# Correct - use exec for non-interactive execution
git diff | codex exec -m gpt-5.2 "Review this..."
```

### "Command not found"

```bash
# Check installation
which codex

# Reinstall if needed
npm install -g @openai/codex
```

### Authentication errors

```bash
# Re-authenticate interactively
codex --login

# Or set API key
export OPENAI_API_KEY="your-key"
export CODEX_API_KEY="your-key"  # For CI
```

### Rate limiting

For heavy usage, use an API key with appropriate tier limits rather than ChatGPT authentication.

### No output / empty response

Ensure stderr is handled separately from stdout:

```bash
# Capture output properly
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" \
  "Your prompt" 2>/dev/null > output.txt

# Or use -o flag
codex exec -m gpt-5.2 -c model_reasoning_effort="xhigh" \
  -o output.txt "Your prompt"
```
