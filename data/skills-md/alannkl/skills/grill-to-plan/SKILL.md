---
name: grill-to-plan
description: Turn casual ideas, vague goals, plans, or designs into clearer decisions through scoped questioning, decision-tree review, and optional records.
disable-model-invocation: true
---

# Grill to Plan

Turn a vague goal, rough idea, plan, or design into shared understanding, clear decisions, and a final actionable plan.

## Modes

- Lightweight mode: ask only the highest-value questions, keep the tone conversational, and skip repo docs unless the user asks or a durable project decision emerges.
- Documented mode: apply the full workflow — code/doc checks, glossary updates, ADRs when warranted, session records, and final synthesis.

## Workflow

1. Restate the goal.
   - Rephrase the user's current intent in specific, concrete terms.
   - Treat the input as a goal description until the user has provided enough decisions for it to count as a plan.
   - Say what you believe the desired end state is, what is in scope, and what may be out of scope.
   - If the initial context is too thin to make a reasonable guess, ask for the missing context first.
   - Choose the mode by stakes: default to lightweight, switch to documented when project knowledge, architecture, or durable decisions are involved. If the initial input leaves the mode unclear, ask whether the user wants lightweight clarification or documented decision capture before continuing.

2. Scope before drilling down.
   - Judge from the initial input whether the scope is settled: can you already list the decisions that need making?
   - If not — the boundaries are fuzzy or several directions are still open — ask scoping questions first to narrow the target.
   - Ask scoping questions in convergence order: highest-leverage boundary questions first, then progressively narrower ones.
   - Once scope is clear, switch to decision-tree order and resolve dependent decisions branch by branch.

3. Use available context before asking.
   - Answer discoverable questions yourself: inspect the codebase, docs, issue tracker, or session log first and report what you found; ask only what exploration cannot settle.
   - If a needed fact requires lengthy exploration, do not stall the session: start the exploration in the background when the harness allows, move on to questions that do not depend on it, and fold the finding in when it arrives.
   - Look for `CONTEXT-MAP.md`, `CONTEXT.md`, and `docs/adr/` when the discussion touches domain language or architecture.

4. Ask one question at a time by default.
   - Open each question by restating the goal and the relevant settled decisions.
   - Ask only non-obvious questions: architecture-changing ones first, detail-tuning last.
   - Probe domain relationships with concrete edge-case scenarios that force precise boundaries.
   - When genuine alternatives exist, present 2-4 candidates — answers or options you propose — each with a trade-off phrase, and mark your recommendation with its reasoning. If more than 4 are viable, split the decision or name the pruned rest.
   - Alongside the candidates, always offer a way into discussion — a final "discuss / re-explain this" option in a structured choice, or a standing invitation in plain text. When the user takes it, re-pitch before discussing: restate the question plainly, supply the premise behind it, and use the session's canonical terms.
   - Pick the channel by the answer's shape. A short pick goes through the ask-question tool (structured tool for putting a question with options to the user) when one is available and permitted; a question that needs an explanation, a scenario, or free text goes in a normal chat message with the same candidates numbered. The option set must never depend on the tool.
   - Keep the recommendation inside the options. A tool call is the last thing in its turn: end there and wait for the answer; no closing message or restated recommendation after it.
   - Only an explicit pick counts as acceptance. A timeout, a skipped or expired prompt, or a preselected option leaves the decision open: repeat the question in chat.
   - Prefer batching related light questions — grouped by topic in a single ask-question call — when they are truly independent: no answer could change another, and all are detail-tuning rather than architecture-changing. Coupled or architecture-changing questions stay one at a time. If a batched answer sparks discussion, return to that question on its own.
   - After resolving each branch, briefly note which branches remain. Offer to close out the rest in bulk — present your recommendations for the remaining decisions and let the user accept, tweak, or defer them — when answers turn terse, when the user repeatedly says to just decide, or as a checkpoint after every 10 resolved questions regardless of signals. A "just decide" settles only the question it answers, not the rest.

5. Resolve each question before moving on.
   - If the user wants discussion, stay on that question until there is a conclusion, explicit deferral, or a documented disagreement.
   - If the user's reply is a question, objection, or request for clarification rather than a decision, switch to discussion: answer in detail in a normal message and end the turn there. Do not invoke the ask-question tool in that reply; let the user respond freely in conversation.
   - Return to the ask-question tool only after the discussion has converged or the user signals readiness to decide; the tool is for collecting decisions, not delivering explanations.
   - Before asking the next question, review the current conversation and the latest session record, then align the next question with what has already been decided.

6. Push back on weak or harmful choices.
   - If the user's proposed decision appears wrong, risky, inconsistent, or inferior to an available alternative, do not silently comply.
   - Explain why the current approach or an alternative is better, state the concrete downside of the proposed choice, and ask whether the user wants to discuss or proceed anyway.
   - Continue only after the user confirms or gives a convincing counterargument.
   - Record the final decision; create an ADR when it meets the ADR rule.

7. Maintain project knowledge in documented mode.
   - Challenge terms that conflict with `CONTEXT.md`.
   - Sharpen vague or overloaded terms into precise canonical language.
   - Cross-check user claims against code when possible and surface contradictions.
   - Update `CONTEXT.md` inline when a domain term is resolved. Keep it as a glossary only, without implementation details.
   - Create `CONTEXT.md` or `docs/adr/` lazily, only when there is something concrete to write.
   - Use `references/CONTEXT-FORMAT.md` when creating or updating `CONTEXT.md`.
   - In lightweight mode, do this only when the user asks or a durable project decision emerges.

8. Maintain a session record when useful.
   - Create or update a session document as decisions crystallize. Store it at `plans/{yyyy-mm-dd}-{slug}/session.md` unless the repo has an established planning or decision-log location.
   - For each question, record: context, question, your recommendation, discussion or debate summary, final conclusion, and any follow-up.
   - Also capture the load-bearing facts behind decisions: verified research findings, external-API constraints, contract details, and rejected alternatives. Do not record only the decisions; the implementer will not have this conversation.
   - Treat the live conversation as the immediate source of truth and the session record as the durable checkpoint for settled state.
   - Keep it concise enough to guide the next question without becoming a transcript.
   - Use `references/SESSION-RECORD-FORMAT.md` when creating or updating this document.
   - Skip the session record for lightweight mode unless requested or the discussion produces decisions worth preserving.

9. Finish with a synthesis sized to the mode.
   - Before synthesizing, sweep for silent assumptions: anything you relied on but never asked becomes an explicit decision, an open question, or a stated assumption in the record — present the plan as settled only when nothing remains silently assumed.
   - Settle the definition of done with the user like any other decision: propose acceptance criteria as falsifiable checks, let the user confirm or correct them, and state the confirmed criteria in the synthesis, recorded in `plan.md` whenever one is written; the implementer inherits no checkable "done" from this conversation otherwise.
   - Always assume implementation happens in a different session, possibly by a different agent. The persistent documents (`plan.md`, `session.md`, ADRs) must be self-contained hand-offs. Every decision, constraint, research finding, naming choice, and integration contract needed for implementation must appear in them or a linked doc; the conversation is discarded context.
   - In lightweight mode, give the resolved decision, any explicit deferral, and the next step.
   - In documented mode, provide the full synthesis: resolved plan, decisions made, open questions, docs updated, risks, and next steps.
   - Order the plan by likelihood of revision: lead with the decisions the user is most likely to tweak (data models, type interfaces, user-facing behavior) and put mechanical or well-understood work last.
   - Use a diagram (flow, sequence, state, dependency) in the synthesis and in `plan.md` or `session.md` when structure — component interactions, data flow, decision branches, build order — is easier to grasp visually than in prose. Write diagrams in mermaid, in chat and in the records alike, unless the repo's existing docs use another diagram convention. Never diagram what a sentence covers.
   - Offer an alignment quiz alongside the synthesis: a short multiple-choice round checking the user and the plan agree on how the planned system should behave — probing behaviors the user never reasoned through and the plan's critical paths. On acceptance, read `references/ALIGNMENT-QUIZ.md` and follow it; fold any changed decision back into the synthesis and records.
   - Whenever a session record exists, also persist the final plan as `plan.md` next to `session.md`, following `references/SESSION-RECORD-FORMAT.md`. Overwrite it if the session resumes and the plan changes.
   - Keep `plan.md` forward-looking: what to build and in what order. Link to `session.md` for decision history instead of duplicating it.

## ADR rule

Offer or create an ADR only when all three are true:

- Hard to reverse: changing the decision later would be meaningfully costly.
- Surprising without context: a future reader would reasonably ask why this choice was made.
- Real trade-off: there were genuine alternatives and the decision chose one for specific reasons.

Use `references/ADR-FORMAT.md` when creating ADRs.
