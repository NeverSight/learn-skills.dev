---
name: decision-interview
description: "Interviews the requester about a plan, design, or idea one question at a time, offering options and a recommendation, until every material decision is resolved, then restates the decisions for explicit confirmation. Use when a plan is vague, has hidden branches, or needs a shared understanding before work starts. Not for refining a work item into a build specification and not for starting the work."
disable-model-invocation: true
---

# Decision Interview

## Purpose
Turn a loosely stated plan into a short list of confirmed decisions by asking focused questions in order, so nothing material is assumed silently.

## When to use
- Use when: a plan, design, or request has open choices, unclear scope, or dependencies between choices, and the requester is available to answer.
- Do not use when: the goal is an approved, implementation-ready specification for a work item to build (use `refine-issue`), when the answers are all in supplied material, or when the requester wants the work done instead.

## Inputs
- Required: the plan, design, or request, and a requester who can answer.
- Optional: supporting documents, prior decisions, and constraints such as deadline or budget.
- Assumptions: nothing is built, saved, or sent during the interview.

## Process
1. Read the supplied material. List the open decisions and order them so that a decision comes before any decision that depends on it.
2. Remove questions the material already answers. Record those as assumptions with where they came from.
3. Restate the objective in one or two sentences so the requester can correct it.
4. Ask exactly one question. Number two to four options, mark a recommended one, and give the reason in a sentence. Allow a free-form answer.
5. Wait. Record the answer as a decision. Re-order or drop later questions that the answer changes.
6. Repeat from step 4 until no material decision is open or the requester stops the interview.
7. Present the [decision record](templates/decision-record.md): decisions, assumptions, and open items. Ask for explicit confirmation.
8. Apply corrections and ask again if anything changed materially.

## Rules and heuristics
- Required: one question per turn. Never send a batch of questions.
- Required: agreement with a single answer is not approval of the whole record; ask for confirmation of the full record.
- Required: do not begin the work during the interview, even if asked to start "once it's clear". Finish, confirm, and stop.
- Required: when the requester says "you decide", state the choice, label it delegated, and continue.
- Recommended: ask the question whose answer removes the most other questions first.
- Recommended: prefer questions that expose a tradeoff over questions about preferences with no consequences.

## Checks
- Each decision traces to an answer or a labeled assumption, not to a guess.
- No question was asked that the supplied material answered.
- Nothing was done beyond the interview, and the record separates decisions from open items.

## Output
Return the decision record with decisions (and who made each), assumptions with their sources, open items with owners, and the confirmation status.

## Completion criteria
- The requester has explicitly confirmed the record, or the interview was stopped and the open items are listed.
- No material decision is silently assumed.
