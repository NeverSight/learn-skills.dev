---
name: interrogate-claim
description: "Use when reading, reviewing, replying to, or pressure-testing a strategy note, argument, memo, or critique. Forces claim-location before opinion: reconstruct the central claim, level, burden, objections, and next action before responding."
created: 2026-04-28
modified: 2026-04-28
published: 2026-04-28
---

# Interrogate Claim

Use this before responding to a strategy note, especially when the first reaction is an objection, analogy, or "isn't this just X?"

The goal is not to summarize for skimmers. The goal is to make the reader reconstruct the argument before they comment on it.

The useful output is not agree/disagree. It is: here is the claim, here is the level, here is the real burden.

## Rule

Do not critique the note until you can answer the questions below from the note itself.

## Questions

### 1. Locate the claim

1. What is the note's central claim in one sentence?
2. What problem is the note saying exists?
3. What distinction does the note rely on?
4. What is the note explicitly not claiming?

### 2. Locate the level

5. Is the claim about product, protocol, business model, UX, sequencing, or wording?
6. Am I responding at the same level, or switching levels?
7. If I am using an analogy, which part of the analogy is load-bearing?

### 3. Find the burden

8. What would have to be true for the note to be right?
9. What evidence does the note already give?
10. What evidence would falsify it?
11. Is the note asking "can this exist?" or "does this sequence create demand?"

### 4. Check the objection

12. Does my objection answer the central claim, or only a nearby weaker claim?
13. Has the note already handled my objection?
14. If yes, what is my remaining disagreement?
15. If no, where exactly is the missing premise?

### 5. Apply it

16. If the note is right, what would we stop doing?
17. What would we build or test next?
18. What question should the team answer before deciding?
19. Who is the user in the note, specifically?
20. What behaviour exists today that this product or protocol would standardise?

## Output

Return:

- Central claim:
- Level of claim:
- Strongest supporting argument:
- Strongest objection:
- Does the note already answer that objection?
- Concrete next question:

## Guardrail

If the reader cannot answer the central claim, level, and burden, the correct response is not a counterargument. It is: reread the note.
