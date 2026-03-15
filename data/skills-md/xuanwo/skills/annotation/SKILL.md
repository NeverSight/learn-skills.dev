---
name: annotation
description: Maintain continuous human-Agents collaboration on already-drafted documents by interpreting and applying review annotations. Use when a user reviews a completed draft (for example `PLAN.md`) and leaves added content, deletion intent, or `===`-marked paragraphs for Agents to process in iterative review-response cycles.
---

## Objective

Run a review loop where humans annotate an existing draft and Agents respond block-by-block, then apply the agreed edits directly to the document.

## Scope

1. Start only after a draft already exists.
2. Treat this skill as post-draft review handling, not initial document writing.
3. Repeat the same workflow for each review round.

## Required behavior

1. Locate the reviewed document (for example `PLAN.md`) and read the latest full content before editing.
2. Detect review signals:
   - Added content (new paragraphs or explicit add/insert instructions).
   - Deletion intent (removed text, strike-through text, or explicit delete/remove instructions).
   - Paragraphs containing `===` markers.
   - User questions that request explanation, rationale, or decision guidance.
3. Split detected signals into independent review blocks.
4. For each block in the current round, do all of the following:
   - Infer likely intent from surrounding context.
   - Reply with the intended action briefly.
   - Apply the edit directly to the document.
   - If the block is a question, provide a direct and sufficiently detailed answer before applying related edits (if any).
5. Keep unrelated sections untouched.
6. Remove temporary collaboration markers (including `===`) after applying edits, unless the user explicitly asks to keep them.
7. Finish the round with a concise progress update so humans can continue the next review cycle.

## Intent inference rules

1. Treat user annotations as guidance, not final wording.
2. Prefer the simplest interpretation that keeps structure, tone, and terminology consistent with nearby sections.
3. If one block is ambiguous, choose a conservative edit that is easy to iterate.
4. If an edit could change critical meaning, keep existing facts and adjust phrasing instead of inventing new claims.
5. When two signals conflict, prioritize:
   - Explicit user instruction.
   - Document consistency.
   - Minimal-risk change.

## Question handling

1. Treat explicit user questions as first-class review inputs, even when no `ADD/DELETE/===` marker is present.
2. Answer questions with enough detail to unblock the next step:
   - direct conclusion;
   - key reasoning and assumptions;
   - concrete recommendation or next action.
3. If a question implies document changes, apply those changes in the same round when safe and clear.
4. If critical information is missing and could change correctness, ask only the minimum focused clarification needed.

## Response style

1. Prefer natural, concise summaries aligned with user style and context.
2. Keep output focused on what was changed and what remains unresolved (if any).

## Editing checklist

1. Ensure each detected block has both a response and an applied change.
2. Ensure no accidental edits outside targeted blocks.
3. Ensure no unresolved `===` marker remains unless explicitly requested.
4. Re-read neighboring paragraphs to keep flow and references consistent.

## Fallback

If no review signals or actionable questions are found, reply briefly that this round has no actionable annotation blocks and wait for the next annotated review.
