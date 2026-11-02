---
name: human-first-linear
description: Explain, draft, or rewrite Linear issues in human-first form. Use for a Linear issue, ticket, task, PRD, umbrella issue, or follow-up when the user wants a read-only explanation, proposed wording, or an authorized live cleanup.
---

# Human-First Linear

Make the issue explain the work to a human before it instructs a machine.

## Select the Mode

- **Explain:** the user asks what an issue means or wants to talk it through. Read the live issue and answer in chat. Make no external write.
- **Draft:** the user asks for proposed wording, or write authorization is ambiguous. Return a complete draft without changing Linear.
- **Live edit:** the user explicitly asks to update, rewrite, clean up, or replace the live issue. Change only the fields they authorized.

Conversation context counts as authorization. When the mode remains unclear, use Draft.

## Workflow

1. Read the live issue when one exists; otherwise read the supplied notes or source material. Completion: the problem, blocker, and accepted decisions are supported by available evidence; missing evidence is named.
2. Snapshot the fields in scope. For an existing description, classify every section as **keep**, **rewrite**, **move**, or **remove**, and map every original claim to its destination. A claim may disappear only with explicit deletion authorization. Completion: every claim remains represented, moves to a verified owner, or is explicitly authorized for removal.
3. State the problem and solution in one plain sentence each. If no solution is accepted, state the unresolved decision instead of inventing one. Completion: the problem and accepted solution or unresolved decision make sense without internal implementation detail.
4. Use only the sections the issue needs:
   - **Very simply** — what is wrong and what changes.
   - **The problem** — the concrete failure or confusion today.
   - **The solution** — the smallest accepted approach, or the decision still required.
   - **Current status** — only a blocker, dependency, or abandoned path that changes the next action.
   - **Done when** — short, observable outcomes.
   - **Necessary boundaries** — constraints that prevent likely scope drift; keep them last. Completion: every retained section helps explain the problem, solution, next action, completion, or a necessary boundary.
5. Preserve accepted architecture. If the rewrite exposes duplicate ownership or a new management surface, flag it separately; change the decision only after the user agrees. Completion: accepted decisions remain unchanged unless the user authorized the change.
6. Prune copied mechanics only after locating their canonical owner in a repository, PR, plan, or gate. Link that owner. If no owner can be verified, retain the information or ask the user. Completion: every removed operational detail is either user-authorized or recoverable from its verified link.
7. Complete the selected mode:
   - Explain: return the human explanation without an external write.
   - Draft: return the proposed issue text.
   - Live edit: save only authorized fields, re-read the issue, and verify every **keep** section is exact, every **rewrite** preserves its original claims unless change was authorized, every **move** has a verified destination, and every **remove** was explicitly authorized. Verify status, relationships, and attachments are unchanged unless authorized. Completion: the selected mode's output and verification are complete.

## Editing Rules

Operational detail stays only when it changes the decision, constrains scope, or proves completion. Otherwise link its verified owner instead of copying command dumps, file allow-lists, coding sequences, test matrices, release algorithms, handoff inventories, or PR administration into Linear.

An open task does not need to narrate that it is unfinished. Historical detail stays only when it changes the current decision or prevents a known failed path from being repeated.

Every fact has one owner. Prefer reading or deriving owned facts over maintaining a second list, registry, overlay, document, or workflow.

## Writing Standard

Use short sentences and concrete examples. Introduce technical terms only after the human problem is clear.

Never insert manual soft returns or hard-wrap prose in Linear issues or documents. Keep each paragraph and list item on one physical line and let the app wrap it. Separate paragraphs with a blank line; preserve structural newlines for headings, tables, list items, and code blocks. Unwrap prose copied from repo Markdown before publishing, then re-read the saved content to check that paragraphs have no internal line breaks.

For example, prefer:

> The Starter accepts scope names typed by hand, so a typo fails later with a confusing error. Install the public catalog and validate the name immediately.

over:

> Create a scope-contract module, add a dependency update workflow, enumerate allowed files, and run the following command matrix.

## Done Gate

In every mode, the first screenful answers what is wrong, why it matters, and how it will be solved or which decision remains open. Unique operational information is retained or linked to a verified owner.

For Draft and Live edit of an existing issue, every original claim is accounted for. For Live edit, only authorized fields changed and the post-save issue was verified. For Explain, no external write occurred.
