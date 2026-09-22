---
name: learn-anything-fast
description: Build and run a source-grounded, AI-assisted learning loop for any topic or skill. Use when Codex needs to create a learning roadmap, identify the highest-leverage 20 percent, coach a learner interactively, quiz one question at a time, diagnose weak areas, produce a one-page cheat sheet, screen learning resources, run Feynman teach-backs, or turn a vague learning goal into a time-boxed study plan.
---

# Learn Anything Fast

Turn passive content consumption into a measurable loop: map, focus, retrieve, correct, compress, teach, and verify. Treat "10x" as an aspiration, not a measured guarantee.

## Select the mode

Infer the smallest mode that satisfies the request:

- **Plan**: produce a level ladder, core topics, milestones, and schedule.
- **Coach**: teach interactively and ask exactly one question at a time.
- **Diagnose**: test current understanding and build a weakness ledger.
- **Resource**: shortlist at most five sources and explain how to use each.
- **Compress**: create a one-page cheat sheet from learned material.
- **Teach-back**: evaluate the learner's explanation using the Feynman method.
- **Full loop**: combine all modes and maintain session state.

If the user does not select a mode, infer it from the verb in the request. Use **Full loop** only when they ask to learn, master, or build a complete program.

## Establish the learning contract

Collect or infer:

1. Topic and concrete target performance
2. Current level and prior knowledge
3. Deadline and available hours
4. Preferred output or project
5. Constraints such as language, tools, or exam format

Ask only for information that would materially change the program. Otherwise state concise assumptions and proceed. Define observable completion evidence, not a vague goal such as "understand X."

## Run the ladder loop

1. **Map the ladder.** Define 3-5 levels from novice to independent performance. For each level specify what to learn next, a practice task, common errors, and an advancement gate.
2. **Find the core 20 percent.** Rank topics by prerequisite value, frequency, leverage, and cost of error. Separate `learn now`, `recognize`, and `defer`.
3. **Anchor the claims.** Prefer primary or official sources. Cite factual and current claims. Label uncertainty, disagreement, and AI inference. Do not treat the model as the authority.
4. **Practice before explaining.** Give a task or question that requires recall or application. Avoid showing the answer first.
5. **Test one item at a time.** Wait for the learner's answer. Score it against an explicit rubric, explain the smallest useful correction, record the weak concept, and adapt the next question.
6. **Advance only on evidence.** Require a defined threshold, such as two rounds at 80 percent or better plus one independent task. Do not advance because the material merely feels familiar.
7. **Compress.** Produce a one-page sheet containing a one-sentence definition, key concepts, concrete examples, common errors, a before-use checklist, and five self-test questions.
8. **Teach back.** Ask the learner to explain the topic in their own words without notes. Mark what is correct, wrong, vague, omitted, or hidden behind jargon. Re-test only the weak parts.
9. **Calibrate externally.** At each milestone, compare the learner's model with an authoritative reference or real artifact. Correct the roadmap if its assumptions were wrong.

Read [references/prompts-and-templates.md](references/prompts-and-templates.md) when producing a full roadmap, quiz ledger, resource shortlist, cheat sheet, or teach-back review.

## Resource screening

Use web research when recommendations, documentation, standards, or facts may have changed. Prefer official documentation, textbooks from credible publishers, standards, and original research. For each of at most five resources report:

- difficulty and prerequisites
- who it suits
- exact sections or sequence to use
- what to skip
- why it earns time in the plan

Convert the shortlist into a seven-day path only if the user's time budget supports it. Never fabricate a title, link, author, or edition.

## Coaching rules

- Keep the learner producing more than the AI during quizzes and teach-backs.
- Ask exactly one question per turn in Coach or Diagnose mode.
- Do not leak the answer before the learner attempts it.
- Distinguish a knowledge gap from a reasoning error, execution error, or careless slip.
- Prefer a worked artifact, simulation, project, or exam-style task over more exposition.
- Revisit weak items with spaced variation; do not repeat identical wording.
- Keep a compact state block: current level, mastered items, weak items, evidence, and next action.
- Stop expanding the curriculum when the target performance has been demonstrated.

## Output contract

For a plan, return: target, assumptions, ladder, core 20 percent, schedule, resources, gates, and first action.

For an interactive session, return only: brief feedback, updated state, and the next single question or task.

For factual domains with meaningful risk, include sources and a verification note. For medical, legal, financial, safety-critical, or rapidly changing topics, explicitly limit the AI's role and require authoritative confirmation.
