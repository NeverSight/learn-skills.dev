---
name: ds-explain
description: "Explain how a piece of code works, why it is built that way, and what that means, in plain language a person can follow. Use for 'how does X work', 'why is it like this', 'teach me this', onboarding to a subsystem, or /ds-explain."
---

# ds-explain

Give one plain account of what a thing is, how it runs, and why it has its current shape, so the reader can change it with confidence.

## Steps

1. Work out what the reader needs. Read the conversation: are they about to change it, review it, debug it, or are they new? Pick the three or four things they should walk away knowing. Skip what they already know.
2. Size the job. A single function needs one pass. A subsystem across many files can use two to four parallel read-only subagents, each on one angle, then one pass to combine them.
3. How it works. Read the actual code. Trace the main runtime path from entry point to effect. Note who owns each piece of state and where the boundaries are. Cite files and lines.
4. Why it is that way. Check commit history, blame, PR descriptions, linked issues and comments near the code. Separate what the record says from what you infer, and label inferences clearly. If no record exists, say so.
5. Write the explanation. Start with a plain definition in general terms, then tie it to this codebase. Walk through what happens when someone actually uses it. Then the reasons, then the edge cases. Use a small diagram or table when it helps.
6. Offer to go deeper on one named part.

## Stop when

- The reader's question is answered with cited code and sourced reasons.
- Or you have spent three rounds of searching for the reason with no record. Say the reason is unknown.

## Rules

- Do not edit code.
- Every claim about behavior points at a file and line.
- Never present a guess about intent as fact.
- Explain ideas, do not list functions.
