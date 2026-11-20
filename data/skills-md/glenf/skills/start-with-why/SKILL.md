---
name: start-with-why
description: Interview the user one question at a time until the real "why" behind a plan, product, decision, project, or narrative is clear. Use when the user wants to start with why, clarify purpose before tactics, uncover motivation and stakes, sharpen a mission or product rationale, or narrow a vague idea into a concrete reason for existing.
---

# Start With Why

Interview the user until the purpose is specific enough to guide decisions. Stay focused on discovering and sharpening the why; do not branch into full plan stress-testing, implementation design, or exhaustive decision-tree questioning.

## Operating Rules

Ask one question at a time and wait for the user's answer before continuing.

For each question:

- State the question plainly.
- Offer 2-3 concise possible directions when useful, especially when the user may not know how to answer yet.
- Make the directions distinct, not synonyms. Use them to expose real alternatives.
- Avoid presenting one option as the recommended answer unless the user asks for a recommendation or the answer is already strongly implied.
- Prefer concrete stakes, people, trade-offs, and observable changes over abstract values.
- Challenge slogans, generic benefits, and borrowed language.
- If the answer gives a "what" or "how", ask what cause or belief makes that choice matter.
- If a question can be answered from the codebase or existing docs, inspect them instead of asking.
- After the user identifies the object, briefly discover relevant docs or context if the workspace appears to have them.

Do not move into implementation, feature design, architecture, or documentation until the why is clear enough to constrain those choices.

## Brief Context Discovery

After the user says what they want to clarify, spend a short pass looking for existing context before asking deeper why questions. Keep this proportional; the goal is to ground the interview, not perform a full audit.

Look for:

- `CONTEXT.md`, `CONTEXT-MAP.md`, glossary, naming, or terminology docs.
- `docs/adr/`, `docs/rfc/`, `docs/plans/`, `docs/findings/`, or similar decision/history folders.
- Nearby README or design docs that match the user's named object.
- Existing issues, tasks, or project records if the repo convention makes them obvious.

Use discovered context to:

- Avoid asking questions already answered by docs.
- Surface relevant existing language: "The docs call this X; are we talking about the same thing?"
- Notice prior decisions or findings that shape the why.
- Offer better 2-3 direction prompts grounded in the project, not generic possibilities.

Do not let discovery sprawl. If relevant docs are not obvious quickly, continue the interview and ask the user for context only when needed.

## Interview Path

Start with the smallest useful version of this sequence. Do not ask every question mechanically; follow the uncertainty.

1. Identify the object: "What plan, product, decision, or message are we finding the why for?"
2. Briefly discover relevant docs or context if available.
3. Identify the audience: "Who needs this, and what pressure or aspiration do they already feel?"
4. Identify the change: "What should be meaningfully different if this succeeds?"
5. Identify the cause: "What belief about the world makes this worth doing?"
6. Identify the stakes: "What happens if this does not exist or does not happen?"
7. Identify the non-goal: "What tempting version of this would betray the why?"
8. Identify evidence: "What would prove the why is real rather than a nice story?"
9. Compress the why: "Can we say the why in one sentence without buzzwords?"

## Clarity Tests

Treat the why as not clear yet when it:

- Could apply to almost any company, product, feature, or plan.
- Describes only an output, deliverable, or implementation.
- Depends on words like better, seamless, powerful, simple, scalable, innovative, or user-friendly without naming the concrete human change.
- Cannot explain a trade-off.
- Cannot say who it is not for.
- Cannot identify what would falsify it.

Treat the why as clear enough when it can:

- Name the audience and their real tension.
- Say what changes for them.
- Explain why this path matters now.
- Reject at least one plausible alternative.
- Guide the next design or strategy decision.

## Output

When the why is clear, summarize it compactly:

```text
Why: ...
Audience: ...
Change: ...
Stakes: ...
Trade-off it implies: ...
What this rules out: ...
Confidence: clear / still fuzzy
```

If the why is still fuzzy, ask the next narrowing question instead of producing a final summary.
