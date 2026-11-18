---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Start by establishing the intended outcome of this discussion: what we need to decide or clarify, its scope and boundaries, and the expected behavior where relevant. Reuse what the user has already made clear; ask only about missing or ambiguous points. Briefly state the working destination. Challenge the framing and surface overlooked risks, dependencies and alternatives; revisit the goal or scope with the user when needed.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Use the harness's native interactive question UI when the whole frontier fits in one call, with your recommended answer as the first option and marked as recommended. When the frontier exceeds the tool's limits, use the text format below, so the round stays whole. Examples:

- OMP (the oh-my-pi coding agent): `ask`
- Claude Code: `AskUserQuestion`, up to 4 questions with 2 to 4 options each
- Codex: `request_user_input`

Otherwise, format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), follow the project's read-only exploration policy: use a fresh-context sub-agent where permitted and useful, or look it up yourself when delegation is unavailable, forbidden or unnecessary. Don't ask the user for anything you could look up yourself. A running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the findings; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
