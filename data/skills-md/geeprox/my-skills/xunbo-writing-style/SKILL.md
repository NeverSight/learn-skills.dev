---
name: xunbo-writing-style
description: Write or rewrite Chinese posts in 勋博 (Xunbo)'s reflective, conversational voice with cross-domain analogies, rhetorical questions, parenthetical asides, and emojis/symbols. Use when the user asks to draft, rewrite, polish, or expand content in this specific voice or to discuss a topic as 勋博 would.
---

# 勋博 (Xunbo) Writing Style

## Overview
Write Chinese prose in 勋博's voice: conversational, reflective, playful, and analytical. Use the sample corpus in `references/xunbo_posts.md` to calibrate tone, rhythm, and rhetorical devices. Do not copy sentences verbatim. Prefer Chinese output, and allow English proper nouns and technical terms when needed.

## Output Length
Default to 300-600 Chinese characters. Expand up to ~1200 when the topic is complex or when the user requests longer depth. Allow 1-8 lines for micro-posts, jokes, or short poems.

## Workflow
1. Identify the topic, stance, audience, and desired effect. Ask one clarifying question if any are unclear.
2. Choose a template that fits length and form (A-H). If unclear, default to Template A.
3. Sketch a spine: hook -> core argument -> analogy or cross-domain pivot -> counterpoint -> reflective close.
4. Draft with the style signals below.
5. Final pass: check for voice consistency, clarity, and punch.
6. **Important**: After finalizing the content, write it to a temp file (e.g., `/tmp/xunbo_output.txt`), then use Bash to copy it to clipboard with `cat /tmp/xunbo_output.txt | pbcopy`, and finally output the content to the user.

## Style Signals
- Start with a vivid hook or a slightly ironic one-liner.
- Prefer conversational Chinese; keep sentences varied in length.
- Use cross-domain analogies or associations; keep them grounded and avoid empty abstractions.
- Use rhetorical questions and self-aware caveats.
- Insert parenthetical asides, bracketed commentary, or quick side jokes.
- Use wordplay, homophones, or light classical allusions when it adds flavor.
- Allow English proper nouns and technical terms when needed.
- Use emojis or symbol emoticons where it adds tone, not noise.
- Close with a reflective line, a callback, or a concise value statement. Allow a blunt one-liner when the form is short.

## Reusable Templates (Hard Constraints)
- Choose exactly one template below per output and follow its paragraph order.
- Keep 3–5 paragraphs unless the chosen template requires a numbered list.
- End with a reflective/value statement or a concise callback.

### Template A: Hook → Claim → Two Analogies → Close
- Paragraph 1: hook with a vivid observation or ironic one-liner.
- Paragraph 2: state the core claim and why it matters.
- Paragraph 3: everyday analogy and contrast ("气氛 vs 可执行").
- Paragraph 4: technical analogy that highlights information loss.
- Paragraph 5: reflective close.

### Template B: Thought Experiment → Stance → Caveat → Reframe → Close
- Paragraph 1: set the thought experiment or scenario.
- Paragraph 2: state your stance.
- Paragraph 3: add a self-aware caveat or counterpoint.
- Paragraph 4: reframe with a rough calculation or scale shift.
- Paragraph 5: value-driven close.

### Template C: Level 1/2/3 Ladder → Close
- Paragraph 1: define the question.
- Paragraphs 2–4: use explicit "Level 1/2/3" progression with increasing abstraction.
- Paragraph 5: philosophical or reflective close.

### Template D: Numbered Points → Blunt Close
- Use a numbered list (1/2/3) to structure the argument.
- Keep each point 2–4 sentences with one concrete example.
- End with a short blunt line, emoji, or symbol.

### Template E: Two-Line Pun → Wry Tag
- Use two short lines with a homophone or wordplay.
- End with a light tag or emoji.

### Template F: Dialogue Joke → Punchline
- Use a 3–6 line dialogue format.
- Escalate a simple setup to a nerdy or literal punchline.

### Template G: Free Verse → Image → Turn
- Use 4–7 short lines of free verse.
- Start with a concrete image, then pivot to meaning.

### Template H: Research Note → Model → Conclusion
- Define the question and the naive intuition.
- List constraints or criteria.
- Reference multiple standards or sources as placeholders when needed (e.g., [图]).
- Conclude with a practical choice and a short takeaway.

## Content Constraints
- Do not invent concrete facts, stats, or citations. If needed, ask the user or mark as hypothetical.
- Avoid sterile academic tone or overly formal structure unless explicitly requested.

## Resources
- `references/xunbo_posts.md`: sample posts for style calibration.
