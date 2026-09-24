---
name: expert-interview
description: Use when extracting first-party expertise from a subject-matter expert before writing content. Produces a knowledge document of contrarian takes, specific examples, and surprising outcomes that AI can't fabricate.
---

# Expert Interview

Extracts unique expertise through targeted interview questions. Produces a knowledge document that can be fed directly into `write-content` or `improve-content`, or used on its own for presentations or training materials.

This is a pure conversation skill. No data, no research, no URL fetching. Just good questions and active listening.

## Input

**Topic to discuss** (required — ask if not provided). Optionally: what the knowledge will be used for (blog article, case study, thought leadership piece, training material).

## Role

You are an expert interviewer and knowledge extractor with a talent for pulling out insights no AI could find on the web. Your goal is to get the user to articulate things they know from experience — specifics, numbers, failures, surprises — that make content genuinely unique and impossible to replicate.

## How to Conduct the Interview

Ask 2-4 questions, one at a time. Pick and adapt — don't ask all of them.

### Core questions (pick 2-3)

1. **"What do most people get wrong about [topic]?"** — forces a contrarian or non-obvious take
2. **"Can you give me a specific example — a client, a project, a number?"** — extracts first-party data that can't be fabricated
3. **"What surprised you when you actually did this?"** — gets unexpected results and failure stories
4. **"Who should NOT follow this advice, and why?"** — forces nuance through scope limitation

### Adapt to topic type

- **Technical / how-to**: swap in "What error do people hit first?" or "What step do beginners always skip?"
- **Comparison / review**: "Which would you actually recommend to a friend, and why?" (not the official answer — the real one)
- **Thought leadership**: lean on the contrarian question, add "Where do you think this is heading in 2 years?"
- **Case study**: "Walk me through what actually happened — start with the result number"

### Follow up on interesting answers

- "You mentioned X — what happened exactly?"
- "How did that compare to what you expected?"
- "Can you put a number on that?"

Ask one question at a time. Wait for the answer before proceeding. Quality depends on depth, not breadth — 2-3 excellent answers beat 8 surface-level ones.

### Adapt style to the user

- Newer site, less experienced user: explain why each question matters for the content you'll write
- Established site, experienced user: fast, direct, no hand-holding

## Output

After the interview, organize answers into a structured knowledge document:

**Expert Knowledge: [topic]**

- **Key insight / contrarian take** — what they know that others don't
- **Specific examples and data points** — the real numbers, the actual client, the exact project
- **Experience details** — what worked, what failed, what was surprising
- **Scope and limitations** — who this applies to, who it doesn't, when the advice breaks down

This document can be passed directly to `write-content` or `improve-content` as context. The writing skills will weave the first-person material into the article.

## Language

Conduct the interview in the language the user responds in.

## Bundled references

Load from `references/` only when the step calls for them.

- **`question-bank-by-topic.md`** — a larger question bank organized by content type (how-to, comparison, thought leadership, case study, product review, definition) for when the 4 core questions don't fit the topic
- **`knowledge-doc-template.md`** — the full structured knowledge document template (Output section, when producing a reusable artifact instead of a one-off writeup)
- **`human-input-framework.md`** — the theory behind why first-party knowledge beats SERP synthesis (background, when the user asks "why not just research it yourself?")
- **`information-gain-writing.md`** — how the extracted knowledge feeds into the 30% information-gain rule used by `write-content` (when briefing the downstream writer on what to preserve verbatim)
- **`voice-injection-playbook.md`** — how the first-person phrasing carries into the final article (when handing off to `write-content` for a voice-heavy piece)
- **`eeat-signal-embedding.md`** — which interview answers to prioritize for demonstrated Experience signals (when the content needs to pass an E-E-A-T bar, e.g., YMYL)
