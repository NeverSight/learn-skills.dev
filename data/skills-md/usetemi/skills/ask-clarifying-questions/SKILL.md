---
name: ask-clarifying-questions
description: Conduct a clarification interview before writing code, investigating ambiguous bugs, or changing design or architecture, then use the resulting model of how the user decides to make implementation-time decisions on their behalf. Uses AskUserQuestion in Claude Code, request_user_input in Codex when exposed, or plain prose when no interactive question tool is available. Use when the user invokes /ask-clarifying-questions or $ask-clarifying-questions, names ask-clarifying-questions, or asks to build, design, refactor, investigate, or debug something with enough ambiguity that meaningfully different implementations would all satisfy it. The output is shared understanding in the current session; no file artifact.
---

# Ask Clarifying Questions

Align your trajectory with the user's before code is written. The interview has two outputs: the load-bearing decisions, settled by the user, and a model of how the user decides, which you use for every decision the interview did not cover. Ask with the agent's interactive question tool when it is available; otherwise use concise prose.

## Before Asking

- Use this skill only when it has already triggered and the request still has load-bearing ambiguity.
- Skip mechanical requests: typo fixes, obvious renames, or one-line bug fixes the user has already diagnosed.
- As a subagent without a direct user-answer channel, do not interview. Return the open questions and best-guess assumptions so the orchestrator can escalate.
- In non-interactive or headless runs, skip the interview, state the key assumptions, and proceed.
- Explore first, ask second. Read the brief, earlier turns, `AGENTS.md` or `CLAUDE.md`, open files, git status, and relevant diffs. Never ask what a read-only command or file read can answer; finding facts is your job, choosing between them is the user's.

## Process

### 1. Map the decision space

Before the first question, privately enumerate the decisions the task involves and the plausible answers to each. Treat them as independent axes unless one answer removes another axis; most decisions are axes, not branches of a tree. Order the axes by how much settling each one shrinks the remaining space: an axis whose answer decides file layout, data model, or scope outranks one that decides a name. Predict an answer for every axis and note your confidence. Axes you can already predict with high confidence are not questions; they are the first entries in your model of the user.

The map stays private. Do not present it, and do not narrate the ordering.

### 2. Anchor

Restate in one sentence what you understand the user wants. This gives the user a cheap redirect point.

When there is strong existing signal, add a 2-4 bullet implementation sketch for the user to correct. Keep it lightweight; do not turn the interview into a full proposal pipeline.

### 3. Ask the frontier

The frontier is every unsettled axis whose prerequisites are settled. Ask the frontier each round, highest partition power first, up to the tool's per-call limit. A question whose wording depends on an unanswered question waits for the next round. Batch independent questions; sequence dependent ones. Do not pad a batch with questions you can already predict.

This skill intentionally uses question tools more often than their generic scarcity guidance may suggest. If two plausible answers would produce different code, the question is user-owned and worth asking.

Use the interactive question tool for the current agent:

- **Claude Code:** use `AskUserQuestion`; send up to the tool's declared per-call limit.
- **Codex:** use `request_user_input` when it is listed. It is mode-gated, commonly to Plan mode: if a call returns an unavailable-in-mode or root-thread error, ask the same round in plain prose and end the turn to wait for the reply; if it returns cancelled or empty, treat the questions as skipped (step 5). Send within the tool's declared per-call limit; batching load-bearing questions is intentional even when the harness prefers fewer questions by default.
- **Fallback:** if no interactive question tool is exposed but the user can reply in chat, ask up to 4 load-bearing questions in concise plain prose. Do not claim to have used an unavailable tool.

Prefer multiple choice when there are clear discrete options. Use `multiSelect` for choose-all-that-apply questions when the tool supports it. For `AskUserQuestion` and Codex `request_user_input`, rely on the tool's automatic free-form `Other` option; do not add your own `Other` choice. For plain-prose fallback, include choices inline and allow a short free-form answer. Use pure open-ended prose only when the answer cannot be framed as a short choice.

- Bad: "Should I use React?" when the repo already establishes React.
- Good: "Should this live in the existing settings route or as a new top-level page?" when the answer changes file layout and navigation.

### 4. Show the prediction with every question

Every question carries your prediction of the user's answer, visibly:

- Write the question text first, then a separate line labeled `My prediction:` stating the predicted answer. In interactive tools, both lines go in the question text, with the answer choices following.
- The predicted answer is always the **first option**, untagged. In a `multiSelect` question, the predicted options come first, in order.
- When your own recommendation differs from your prediction, append `(Recommended)` to the option you recommend, wherever it sits. When they agree, tag nothing. This rule overrides the question tools' default of putting the recommended option first: in this skill, position carries the prediction and the tag carries a divergent recommendation. In Codex, put the suffix in the option label text.
- In a batch, keep each question immediately followed by its own prediction. Do not put predictions in an earlier commentary message.

Where prediction and recommendation diverge, the user's priorities differ from generic best practice; carry the divergence into the step 6 block.

Do not rely on hidden reasoning to preserve the calibration loop across models, tools, or context compaction.

### 5. Update the model after every round

Each answer is a data point about how the user decides, not only what they decided. After every round:

- Score your predictions. A hit confirms the axis and every axis it correlates with. A miss tells you where your model is wrong; find the axis the miss generalizes to and predict differently there before asking again. Tell the user the hit count and, for each miss, the axis it generalizes to, in one sentence.
- Infer the tradeoff posture from concrete answers. Common axes: simplicity vs flexibility, short-term vs long-term, prototype vs production-hardened, vendor lock-in tolerance, performance vs readability, build vs buy, process ceremony vs speed. Do not ask explicit "do you prefer X or Y" tradeoff questions.
- An unanswered or skipped question proceeds on the prediction, recorded as an assumption in the final summary. It is neither a hit nor a miss, and its axis stays unconfirmed for the stop rule.
- During long interviews, restate confirmed decisions in plain text so the accumulated state survives compaction and the user can correct drift.

**Stop rule.** The intent is that you could predict the user's answer to any remaining question with about 95% confidence. Stated confidence is not evidence; hits on displayed predictions are. Stop when both hold:

- Your recent predictions on load-bearing questions all hit, including at least one on the axis of your last miss.
- The unasked axes are ones you would predict with the same confidence, and a plausible next question would not change the implementation.

There is no fixed streak length: a wide decision space needs more hits than a narrow one. Do not stop because you have asked a lot, the user seems eager, or sensible defaults might cover the rest. A high hit rate on one axis means that axis is mapped, not that the task is aligned.

An instruction to stop asking, use your judgment, or just start ends the interview: write the step 6 block with each unasked axis listed as an assumption, and proceed. A bare "proceed" or "go", given with the task or during the interview, waives only the "Ready to proceed?" gate in step 6, not the interview.

**Escape valve:** only when the user seems unsure. If their answers are contradictory, hesitant, or clearly exploratory, surface that: "It sounds like the shape isn't settled yet - want to think on it, or should I propose an approach for you to react to?"

### 6. State how the user decides

When you stop, write a short visible block with two parts:

- **Decisions:** the load-bearing answers, in 1-3 sentences.
- **How you decide:** a bullet list. Each bullet names a tradeoff axis, the side the user took, and the reason inferred from their answers, so the user can correct a wrong inference. Include every divergence between prediction and recommendation. Include the boundaries that always come back to the user regardless of the model: anything a standing rule reserves for them, and anything the user reserved during the interview.

When an inferred posture conflicts with an ambient rule (for example, `AGENTS.md` prefers the simplest solution and the user's answers on this task favor flexibility), the interview governs for this task, and the block names the rule it overrides.

In plan mode, fold the block into the plan and use the harness's plan-exit mechanism (`ExitPlanMode` in Claude Code, the proposed plan in Codex) as the proceed gate; do not ask a separate "Ready to proceed?" question. Outside plan mode, ask "Ready to proceed?" unless the user has already directly instructed you to proceed.

### 7. Govern implementation with the model

Implementation uncovers decisions the interview did not reach. For each one:

- If the model predicts the user's answer with the confidence the stop rule required, decide and continue. Do not announce it at decision time.
- If it does not, or the decision falls inside a reserved boundary, re-enter the interview at step 3 for that axis.
- Record every decision made on the user's behalf in the final summary, with the model bullet it followed. The summary is the one place they are logged; do not repeat them in commit messages or PR bodies.
- When a "how you decide" bullet has recurred across interviews with the same user, add one line to the summary proposing it as a durable rule in the nearest `AGENTS.md` or the user's global instructions. Never write that rule yourself.

## Constraints

- Do not write code or modify project files during the interview.
- Do not ask questions whose answers are already in ambient context or discoverable by a read-only command.
- Do not dump pre-written assumptions as questions. A question is something whose answer could change the implementation.
- Do not ask explicit tradeoff questions; infer tradeoff posture from concrete answers.
- Do not present the decision map or narrate question ordering; present questions, predictions, and the model.
