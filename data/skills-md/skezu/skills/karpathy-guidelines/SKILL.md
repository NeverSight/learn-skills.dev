---
name: karpathy-guidelines
description: Behavioral guidelines for reducing LLM coding mistakes, derived from Andrej Karpathy's observations. Use when writing, reviewing, or refactoring code to ensure simplicity, surgical changes, and verifiable success. Essential for maintaining the high-quality standards of Antigravity Kit.
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls. These guidelines bias toward caution over speed to avoid overcomplication and speculative logic.

## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing any logic:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them—don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop and name what's confusing.

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

- Write the minimum amount of code that fulfills the request.
- Do not add features beyond what was asked.
- Avoid abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- If you write 200 lines and it could be 50, rewrite it.
- **Goal:** Senior engineers should view the code as simple, not clever.

## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Do not "improve" adjacent code, comments, or formatting unless requested.
- Do not refactor things that aren't broken.
- Match existing style perfectly, even if it contradicts your preferences.
- If you notice unrelated dead code, mention it instead of deleting it.
- Remove imports, variables, or functions that YOUR changes made unused.

## 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```markdown
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

## Integration with Antigravity Kit
Align these guidelines with the following Antigravity standards:
- **@[skills/clean-code]**: Concise, direct logic and AAA testing.
- **@[skills/brainstorming]**: Use for complex request analysis (Socratic Gate).
- **@[skills/tdd-workflow]**: For implementing the "Goal-Driven Execution" phase.
