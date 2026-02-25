---
name: anthropic-1p-prompt-optimizer
description: Optimize, rewrite, and evaluate prompts using the Anthropic 1P interactive prompt-engineering tutorial patterns (clear/direct instructions, role prompting, XML-tag separation, output formatting + prefilling, step-by-step “precognition”, few-shot examples, hallucination reduction, complex prompt templates, prompt chaining, and tool-use XML formats). Use for 提示词优化/Prompt优化/Prompt engineering, rewriting system+user prompts, enforcing structured outputs (XML/JSON), reducing hallucinations, building multi-step prompt templates, adding few-shot examples, or designing prompt-chaining/tool-calling scaffolds.
---

# Anthropic 1p Prompt Optimizer

## Overview

Turn vague “帮我改一下提示词/Make this prompt better” into a repeatable workflow:
1) clarify goals + constraints, 2) restructure the prompt using proven building blocks, 3) add formatting/examples/guardrails, 4) propose a small test plan for iteration.

## Workflow (1P-style)

### Step 0: Intake (ask only what’s missing)

Request:
- Current prompt (system + user), and where it runs (UI / API / multi-turn).
- Target behavior: success criteria + non-goals.
- Inputs the prompt will receive (and typical edge cases).
- Required output format (plain text / XML / JSON) + strictness.
- Common failures (hallucination, wrong tone, ignored constraints, formatting drift).

### Step 1: Diagnose quickly

Check for:
- Ambiguous verbs (e.g., “analyze”, “optimize”) without definitions.
- Missing role/audience/tone context.
- Data mixed with instructions (needs XML delimiting).
- Output format underspecified (needs tags / JSON schema / prefilling).
- No examples for tricky formatting or edge cases.

### Step 2: Apply building blocks (pick only what helps)

Preferred building blocks from the tutorial (details in references):
- Clear + direct instructions; explicitly ask for what you want.
- Role prompting (optionally include intended audience).
- Separate variable input from instructions using XML tags.
- Enforce output format via XML/JSON + optional prefilling (“speaking for Claude”).
- Add “precognition” for multi-step reasoning (thinking step-by-step).
- Use few-shot examples to lock tone and formatting.
- Reduce hallucinations with “give an out” + evidence-first extraction.
- For complex prompts, use the 1P complex-prompt element ordering.

### Step 3: Ship revisions as artifacts

Always output:
- Revised `system` prompt (if needed) and revised `user` prompt.
- Any few-shot examples and XML tag wrappers.
- A short change log (what changed and why; 5–10 bullets max).
- 3–5 test cases with pass/fail criteria.

## Reference Files (load as needed)

- `references/anthropic-1p-cheatsheet.md`: chapter-by-chapter patterns and “why it works”.
- `references/complex-prompt-template.md`: the 1P complex prompt element list + skeleton.
- `references/guardrails-hallucinations.md`: “out”, evidence-first, placement, temperature tips.
- `references/tool-use-xml.md`: function-calling XML formats (`<function_calls>`, `<function_results>`).
- `references/iteration-checklist.md`: prompt chaining + evaluation loop.
