---
name: remove-ai-style
description: Review and adjust writing style to reduce AI-generated patterns, making text read more naturally and human-like. Supports Chinese and English.
---

# Remove AI Style

Review and adjust the writing style of an article to reduce obvious AI-generated patterns, making the text read more naturally and human-like.

## When to Use

Use this skill when the user asks to:
- Remove AI style from an article
- Make AI-generated text sound more natural
- Polish writing to reduce robotic or formulaic patterns

## Intensity Levels

The user can specify how aggressively to remove AI patterns. If they don't specify, **default to "heavy"**.

| Level | Description |
|-------|-------------|
| **Moderate** (中等) | Only fix the most obvious AI patterns. Preserve most of the original structure and phrasing. Light touch. |
| **Heavy** (尽力去除) | Actively rewrite AI-ish sentences, restructure overly formulaic paragraphs, and replace robotic transitions. This is the **default**. |
| **Full** (完全彻底) | Treat the entire text as a draft and rewrite it from scratch in a natural human voice, while preserving the original meaning and key information. The output should read as if a human wrote it from the start. |

## Instructions

1. **Determine the language** of the article (Chinese or English).
2. **Determine the intensity level** — check if the user specified moderate / heavy / full. Default to heavy.
3. **Load the corresponding reference document**:
   - Chinese articles: `references/chinese.md`
   - English articles: `references/english.md`
4. **Run the quick-scan scripts** provided in the reference document (if any) to locate symbol-level issues first. This gives you a fast overview of problem spots without reading line by line.
5. **Review the article** against the style guidelines in the reference document. The script results are just a starting point — you still need to read through the full text for patterns that scripts can't detect (e.g., overuse of metaphors, formulaic structure, robotic transitions).
6. **Apply fixes according to the intensity level**:
   - Moderate: only fix what the scripts flagged + the most glaring patterns.
   - Heavy: fix everything the guidelines call out, rewrite awkward sentences.
   - Full: rewrite the text from scratch preserving meaning.
7. **Preserve the original meaning and tone** — even at "full" intensity, the core message should remain intact.
