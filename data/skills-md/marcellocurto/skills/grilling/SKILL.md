---
name: grilling
description: Stress-test an idea or decision through focused questions about consequential assumptions and tradeoffs.
---

# Grilling

Help the user resolve the decision they actually need to make. Challenge assumptions and tradeoffs that could materially change that outcome, rather than exploring every possible branch of the idea.

## Set the decision boundary

Identify the requested decision, constraints, and what must be understood to choose a path. Reuse answers and accepted decisions from the conversation. Track dependencies between open questions so later questions build on settled inputs.

Keep optional refinements and unrelated decisions outside the active interview. Park a branch when it may matter later but does not affect the current choice; note it only when useful, without turning it into a blocker or creating a ticket.

## Ask focused rounds

- Select a small set of consequential questions whose prerequisites are settled. Prioritize questions that eliminate materially different outcomes or unlock dependent decisions. The set of answerable questions is a pool to choose from, not a list to ask all at once.
- Follow the user's requested pace or the calling workflow's focus. Ask one question when the tradeoff needs sustained attention; group short, independent questions when they are easy to answer together. Do not hide a large questionnaire inside a single numbered item.
- Make each question concrete and explain why its answer matters. Give a recommendation with a brief reason when the evidence supports one. Keep recommendations distinct from the user's decisions.
- Wait for the user's answers before settling those choices or asking questions that depend on them. Silence, an unanswered question, or your own recommendation is not agreement.
- After each round, incorporate the answers and choose the next useful questions. Reopen a settled answer only when the user revises it or new material evidence challenges it; explain why it needs attention again.

## Establish facts

Look up discoverable facts in the available code, documentation, and tools before asking the user to supply them. Handle small lookups directly. Delegate a bounded factual investigation when delegation is available, the work can run independently, and it is likely to save time or improve the evidence; otherwise continue locally. Do not require a subagent merely because a question needs research.

A pending investigation delays only questions that depend on its result. Continue independent questions while it runs, then reconcile the findings before using them. If a necessary fact cannot be obtained, name the gap and ask for the specific information or access needed.

Product choices, preferences, and tradeoffs requiring the user's judgment remain theirs. Do not use factual research or delegated agents to answer on the user's behalf.

## Finish at the requested decision

Finish when the material choices needed for the requested decision are settled, or when the user pauses. Summarize the agreed path, consequential rationale, and any remaining blocker or useful deferred branch. Do not prolong the interview to exhaust optional questions or ask for blanket reconfirmation of clear answers.

Agreement on a decision does not itself authorize implementation, documentation writes, or external actions. Honor authorization already present in the user's request, including a requested documentation workflow, without asking for it again.
