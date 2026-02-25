---
name: english-prompt-optimizer
description: "Optimize and restructure user prompts for better AI responses. Use when user writes in non-English (Chinese, Japanese, Korean, etc.), request is vague/unclear, or user asks to improve their prompt. Triggers on: '帮我', '请帮忙', 'お願い', any non-English complex request. Translates, restructures, and shows optimized prompt before proceeding."
---

# English Prompt Optimizer

Transform vague or non-English prompts into clear, structured requests.

## Workflow

```
1. DETECT → Is this non-English or vague?
2. ANALYZE → What does user actually want?
3. OPTIMIZE → Create structured English prompt
4. SHOW → Display optimized version
5. EXECUTE → Proceed with optimized request
```

## Optimization Template

```
[TASK]: Clear statement of what to do
[CONTEXT]: Background information
[REQUIREMENTS]: Specific criteria
[OUTPUT FORMAT]: Expected deliverable
[CONSTRAINTS]: Limitations or preferences
```

## Optimization Rules

| Problem              | Solution                              |
| -------------------- | ------------------------------------- |
| Vague task           | Add specific action verb + object     |
| Missing context      | Ask or infer from conversation        |
| No format specified  | Suggest appropriate format            |
| Implicit constraints | Make them explicit                    |

## Response Format

```
🔄 Optimizing your request:

**Original:** [Original request in user's language]

**Optimized:**
───────────────────
[Structured English version]
───────────────────

Proceeding with optimized request...
```

## Example

**Original:**
```
帮我分析一下这个改动，由程序员改，和由 ai 改；分析一下人效
```

**Optimized:**
```
TASK: Compare human vs AI code changes and analyze efficiency

REQUIREMENTS:
- Compare: code quality, time, correctness
- Analyze: efficiency metrics

OUTPUT FORMAT:
- Comparison table
- Efficiency analysis
- Conclusions with evidence
```

## Behavior

1. Brief acknowledgment in user's language
2. Show optimized prompt
3. Ask for missing info if needed
4. Proceed with optimized version
