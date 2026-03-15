---
name: refine-prompt
description: >-
  Transforms vague prompts into precise, structured AI instructions. Use when
  asked to refine, improve, or sharpen a prompt, do prompt engineering,
  write a system prompt, or make AI instructions more effective.
---

# Refining Prompts

## Process

1. **Assess** — Identify what the prompt is missing:

| Element | Check |
|---------|-------|
| Task | Is the core action explicit and unambiguous? |
| Constraints | Are length, format, tone, and scope defined? |
| Output format | Does it specify the expected structure? |
| Context | Does the model have enough background to act? Check: audience, input format, success criteria, scope boundaries, technical constraints |
| Examples | Would a demonstration clarify the expected output? |
| Edge cases | Are failure modes and boundary conditions addressed? |

2. **Rewrite** — Transform into specification language: precise, imperative, no filler. Treat the prompt as a spec, not conversation.

3. **Validate** — Check the rewrite against the assessment table. Every gap identified in step 1 must be addressed.

## Rules

- **Length**: 0.75x–1.5x the original. Conciseness is a feature — add only what's missing, cut what's vague.
- **Never invent** — only use information present in the original prompt or conversation context. If critical info is missing, ask instead of assuming.
- **Instruction hierarchy** — order sections by priority: task → constraints → examples → input data → output format. Place the most important instruction first.
- **Progressive complexity** — start with the simplest prompt that could work. Add few-shot examples, chain-of-thought, or role framing only when the task demands it, not by default.
- **Specific verbs** — replace vague actions ("analyze", "process", "handle") with measurable ones ("list the top 3", "classify as A/B/C", "return JSON with keys X, Y").
- **One output format** — specify exactly one format (JSON schema, markdown template, numbered list). Ambiguous format expectations cause inconsistent results.
- **No meta-commentary** — output only the refined prompt as markdown. No preamble ("Here's an improved version..."), no explanation of changes unless explicitly requested.

## Persistence

After refining, save the result to `.ai/PROMPT.md` (create `.ai/` directory if needed). This builds a reusable prompt library over time. Append with a heading and date:

```markdown
## [Prompt Name] — YYYY-MM-DD

[refined prompt content]
```

## Anti-Patterns

| Problem | Fix |
|---------|-----|
| Vague verbs ("look into", "deal with") | Replace with concrete actions ("list", "compare", "extract") |
| Missing output spec | Add explicit format section with example structure |
| Examples contradict instructions | Align examples to match every stated rule |
| Over-engineered from the start | Strip to simplest working version, then add complexity only where output quality requires it |
| Prompt exceeds context with examples | Limit to 2–3 diverse examples; use one simple, one edge case |
