---
name: steady-do
description: Develop features in an existing project within the current session with ponytail taste. Use when explicitly requested, or automatically for ordinary feature, plugin, extension, and cross-module work that needs project understanding and clarification before implementation. Survey the real flow, grill only unresolved decisions, then implement and verify here without plan or handoff documents. Prefer quick-do for clear, bounded changes; prefer plan-brief when long-horizon work needs planning and separate-session execution.
---

# Steady Do: understand → clarify → implement here → verify

## When this skill applies

- Ordinary feature, plugin, extension, and cross-module work in an existing project, implemented and verified in this session.
- The user's explicit choice wins — never switch workflows silently; if the chosen one cannot fit the task, say why and ask. Bounded and clear → `quick-do`; long-horizon work needing a durable plan and a separate-session handoff → `plan-brief` (propose it when a handoff would help but was not requested).
- These workflows govern requested development work, not every explanation or read-only question. Skill instructions are in English; replies and deliverables follow the user's language (Chinese by default).

## 1. Understand the request and project

- Read the complete requirement and decisions already settled in this conversation. Separate explicit requirements from open questions; investigate before modifying files.
- Read project rules, README, relevant entry points and modules. Trace the real flow, reuse opportunities, affected callers, and compatibility boundaries. Expand by relevance, not a whole-repo tour or a single-function guess.
- **Look at the live site first (seconds, no approval):** activation command and interpreter, dependency versions that actually import now, launch commands, input/output formats, config paths, and whether anything relevant is already running. Inspect instead of assuming an interpreter or system Python. One cheap look buys the avoidance of a whole round of avoidable errors — skipping ceremony is the point, skipping this is not.
- Briefly state the goal, scope, non-goals, and observable completion criteria in chat. Do not create a plan document.

## 2. Grill the unresolved decisions

Use the bounded, round-based grilling method below; it is self-contained and does not require a separate skill or document workflow.

- **Find facts yourself; ask the user for decisions.** Consult code, config, project memory, and docs first. For uncertain external APIs or platform limits, check upstream docs, source, or issues instead of presenting guesses as constraints.
- Ask only questions that affect behavior, scope, compatibility, risk, or acceptance. Give a recommendation and a brief trade-off for each. Resolve ordinary implementation details using project conventions.
- Group independently answerable questions in one round; defer questions that depend on unanswered ones. Use structured questions when available, otherwise numbered questions in chat, then wait for answers.
- After each round, recompute what its answers unblocked and ask the next round. Rounds continue while a further question would still change behavior, scope, compatibility, risk, or acceptance; the stopping rule is nothing material left open, not one round done.
- Do not repeat settled questions or invent a question quota. If the request and context already resolve the decisions, proceed to the recap.
- **Verification mode — mandatory decision; name it in the recap and justify it in one line:**
  - **TDD mode** — only when the feedback loop is fast and tests are cheap (frontend/UI, product services, library code with instant unit tests); invoke the `tdd` skill.
  - **Smoke-and-read mode** (default for research, long-running, or heavy-compute work): the smallest real execution path + rereading your own change + checking the adjacent behavior it touches; the user runs the real workload afterwards. No test scaffolding, no wrapper harnesses.
  - Rule of thumb: if writing and running the test costs more than the failures it would catch, don't write it.
- **Acceptance and responsibility** — what is observed, the expected result, and who runs/verifies what at the end. Reuse an agreed verification approach instead of asking again.
- Stop when implementation-critical and acceptance-critical ambiguity is resolved and understanding is shared. Do not grill speculative future requirements or ask the user to design each function.

## 3. Recap and implement here

- Briefly recap the agreed scope, approach, and verification, then begin without an extra plan-approval gate. If the recap introduces an unresolved material choice, wait for its answer first.
- Keep primary implementation in this session; do not hand it to a fresh session or execution sub-agent. Optional read-only research or review may be delegated when useful, not as a default multi-agent pipeline.
- No plan documents, launcher prompts, development reports, or review reports. Track multi-step work with a session todo; required product docs and project memory still apply.
- If new evidence invalidates the agreed approach or requires broader scope or changed external behavior, pause the affected work and realign. Resolve ordinary local implementation issues yourself.
- Before destructive or irreversible actions, show the impact and obtain explicit authorization. Permission to start does not permit overwriting secrets or changing unrelated environments.

## 4. Keep ponytail taste

- Keep the smallest working change: reuse existing code, then stdlib/native features, then installed dependencies. Do not add dependencies for simple problems.
- No over-encapsulation, speculative abstractions, defensive boilerplate, redundant checks, future scaffolding, or unrelated cleanup.
- Fix root causes along the real call chain, not just the reported symptom; inspect sibling callers of shared logic.
- Preserve necessary trust-boundary validation, security, accessibility, data protection, and error handling that prevents data loss.

## 5. Verify and finish

- Default to the smallest real execution path plus a reread of the change and affected adjacent behavior. Check the agreed observable outcome, not merely the absence of errors. For documentation-only changes, inspect content and applicable format checks.
- Do not add tests, TDD, or verification scripts by default. Follow explicit user requests and mandatory project checks; feature work does not automatically imply TDD.
- Distinguish static checks, successful loading, local calls, and complete user interaction. A loadable plugin is not a working feature; injected input is not a physical terminal interaction.
- If execution needs the user's environment or is blocked, state what remains unverified and give concrete steps and expected observations. **Blocked is a legitimate outcome** — say so with the exact check the user must run; never invent completion or silently omit blocked work.
- Briefly report what changed, what actually ran, and what needs user confirmation. One line when sufficient; no separate report or summary essay.
