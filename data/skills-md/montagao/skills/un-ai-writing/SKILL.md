---
name: un-ai-writing
description: Rewrite and edit existing text to sound natural and human, removing common AI writing tells while preserving meaning and facts. Use when asked to humanize, de-AI-ify, un-AI, make it sound less robotic, polish an AI draft, or remove AI-writing signs in any prose (emails, docs, posts, essays, scripts).
---

# Un-AI Writing

Make provided text read like a real person wrote it by removing common AI-writing tells and strengthening specificity, voice, and coherence.

## Workflow

1. **Interview the user**
   Ask for:
   - Audience and purpose
   - Desired tone (casual, formal, candid, authoritative, etc.)
   - Format constraints (length, headings, bullets, style guide)
   - Must-keep facts, phrases, or terminology
   - Rewrite intensity (light polish vs. heavy rewrite)
   - Any sensitive claims to preserve exactly

2. **Diagnose AI tells**
   Read the draft and identify likely AI-writing signs using `references/signs_of_ai_writing.md`.
   Do this internally to guide edits. Avoid calling them “AI” in the final output unless the user asks.

3. **Rewrite with intent**
   - Replace generic claims with concrete, specific details where possible
   - Cut fluff, empty transitions, and formulaic sectioning
   - Vary sentence length and structure
   - Prefer simple verbs and direct statements over inflated phrasing
   - Reduce excessive hedging and generic caveats
   - Keep voice consistent across paragraphs

4. **Verify integrity**
   - Preserve meaning and all factual claims
   - Do not add new facts or sources
   - Ensure tone matches the requested audience
   - Remove remaining AI tells from the reference checklist

5. **Deliver**
   Provide the revised text. Optionally include a short bullet list of the most important edits and any open questions.

## Editing Moves

Apply as needed:
- Replace vague modifiers ("significant", "various", "notable") with specifics
- Swap template transitions ("Moreover", "In today's world") for direct links or cut them
- Break up uniform paragraph sizes
- Remove repetitive "rule of three" patterns unless they serve a rhetorical purpose
- Avoid "not X but Y" structures when repeated multiple times
- Use contractions where natural
- Limit em dashes and over-bolded phrases
- Remove filler conclusions ("challenges and future prospects") unless requested

## Special Contexts

- **Wikipedia-like writing**: Keep neutral tone, avoid promotional language, avoid conversational asides, and follow the markup/citation notes in the reference file.
- **Marketing copy**: Keep energy but remove canned phrases; add concrete benefits and proof points supplied by the user.
- **Technical docs**: Preserve exactness and avoid inventing features, metrics, or behavior.

## Reference

Read `references/signs_of_ai_writing.md` when diagnosing or removing AI-writing tells.
