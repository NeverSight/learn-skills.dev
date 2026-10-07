---
name: feature-orchestrator
description: Guide an iterative product and technical discussion, then turn the settled feature into a copy-ready orchestration prompt for a separate implementation session with a user-chosen model roster for its Implementer, Researcher, and Reviewer sub-agents. Use when the user wants to explore, narrow, summarize, or hand off a substantial feature without implementing it in the current session.
license: MIT
---

# Feature Orchestrator

This skill runs Session 1 of a two-session workflow. Session 1 thinks: it helps the user settle what to build and why. Session 2 builds: a fresh session receives the compiled prompt, plans against the live repository, and delivers.

The split exists because planning and implementation compete for the same context window and attention. Session 1 can explore freely and change its mind. Session 2 starts clean, with only the settled decisions. So the most valuable thing Session 1 produces is a prompt that carries every hard-won decision precisely. A thorough plan matters less.

Do not rush from the first idea to the prompt. The conversation is part of the work.

## Boundary

- Do not implement in Session 1. Read repository instructions, code, tests, dependencies, and docs freely, but do not modify source, config, dependencies, schemas, or tests. A reversible workflow action, such as creating a local branch, is fine when the user asks for it.
- Technical depth is welcome: likely APIs, data models, flows, risks, and candidate milestones all help settle the feature. None of it becomes Session 2's plan. Session 2 re-inspects the repository and plans for itself, because the code may have moved and Session 1's view was partial.
- If a product ambiguity would materially change behavior or scope, ask. Don't resolve it silently.
- Keep discussion, summaries, and prompts in the conversation unless the user asks to save them.

## Settle the model roster

Session 2 uses four roles:

- **Lead**: Session 2's main agent. It orchestrates, integrates, and does the final verification. Its model is whatever the user launches Session 2 with, so it is not part of the roster.
- **Implementer**: sub-agents that make bounded code changes and fixes.
- **Researcher**: sub-agents for docs, API checks, and read-only exploration. They also serve Session 1.
- **Reviewer**: independent, read-only sub-agents that review the integrated change.

The user chooses the model and effort for the three sub-agent roles. Session 2 runs as many agents of each role as the work supports.

Ask for the roster at handoff, every time you compile the prompt. Don't ask during the discussion. Session 1's own research sub-agents use the environment's preset Researcher. [references/model-roster.md](references/model-roster.md) covers how to ask (one question per role, recommended option first), how to check availability, and how to keep review independent.

## Work conversationally

### Explore

Answer the current question at its natural altitude. Don't force the whole workflow into every reply. Over the conversation, establish:

- what the product does today;
- who the feature is for and what outcome they need;
- the intended user journey;
- what is in scope now and what comes later;
- the stack and architecture that fit this repository;
- failure behavior, permissions, races, data ownership, cost, and operability, where they matter.

Keep observed repository facts, current external facts, user decisions, recommendations, and assumptions distinguishable. They carry different weight in the final prompt.

### Research when it changes a decision

- Delegate independent research, documentation checks, and codebase exploration to Researcher sub-agents. Run them in parallel when their questions are independent.
- Give each one a bounded question, the reason it matters, and the shape of the answer you want. For example: conclusions with `file:line` or source-link evidence, not file dumps.
- Prefer repository evidence and current primary sources. Keep links for claims that may go stale.
- Fold the findings into the conversation. Don't paste raw memos, and don't research just to look thorough.

### Refine with the user

Expect the user to narrow scope, reject complexity, reprioritize, or push back. Reconcile each correction with earlier decisions. Don't start over, and don't defend the previous recommendation.

Keep a mental decision ledger:

- accepted behavior;
- rejected or deferred scope;
- chosen technologies and deliberate exclusions;
- settled invariants;
- open questions;
- verification and delivery expectations.

Don't recite it every turn. Use it to keep later answers and the final prompt consistent, because a correction made in turn 5 is easy to lose by turn 30.

### Summarize on request

When the user asks for an overview, game plan, or recap, give a complete current synthesis. For a complex feature that means the stack, UX, data model, workflows, authorization boundaries, failure recovery, race protection, testing, and a sensible delivery order. It stays revisable until the user settles it.

## Compile only when asked

Compile the Session 2 prompt only when the user asks for it or clearly declares the plan settled.

1. Read [references/model-roster.md](references/model-roster.md) and ask the user for the roster: model and effort for Implementer, Researcher, and Reviewer. Draft nothing until they answer.
2. Read [references/execution-prompt-contract.md](references/execution-prompt-contract.md) and adapt it to the feature.
3. Preserve hard-won decisions in specific language. "Follow best practices" loses information that took the whole conversation to establish.
4. If a material choice is still open, ask for it. Don't disguise it as an instruction.

The prompt must encode these workflow choices:

- The Lead plans against the fresh repository, then implements without stopping for approval.
- Every sub-agent uses its role's chosen model and options exactly. No model choice is left for Session 2. The Lead runs as launched.
- Session 2 uses multiple sub-agents: parallel Researchers for independent questions, parallel Implementers on independent slices, and several Reviewers with distinct lenses.
- The Lead chooses the topology. It parallelizes independent work, staggers dependent work, and implements directly when delegation would not help. There is no arbitrary agent cap and no swarm for its own sake.
- Every sub-agent gets a context-rich brief: goal, why it matters, relevant decisions, owned files, interfaces with neighbors, done-condition, and checks to run. Implementers know they share the repository and must not revert each other or the user's changes.
- The Lead keeps a progress file so that plan, status, and decisions survive context compaction.
- Focused checks run during implementation. Whole-feature verification runs before review.
- For front-end or browser-observable work, the built-in browser is Session 2's vision. Every agent touching UI works in a write → look → interact → fix loop from the first change onward, not with one verification pass at the end.
- Reviewers take distinct risk lenses. The Lead confirms each finding before it is fixed and hands accepted fixes to Implementers. There are at most two review/remediation cycles.
- Session 2 prepares an evidence-backed PR proposal. It does not push or open PRs without explicit approval, and it ends with the exact permission question using its real PR count.

### Delivery and PR thinking

If the feature benefits from several PRs, include a provisional, outcome-oriented split with known dependencies, and have Session 2 validate it against the real change graph. Keep tests with the behavior they prove. Workstreams and PR boundaries are separate concepts, and a proposed split should never be forced when it would be unsafe.

### Output

Return a short introduction and one copy-ready prompt. Don't restate the spec outside the prompt unless an assumption needs the user's attention.

## Final self-check

Before returning the prompt, confirm:

- nothing was implemented in Session 1, and no suggestion is presented as Session 2's final plan;
- every later correction and scope reduction is reflected;
- facts, decisions, recommendations, and assumptions are distinguishable;
- behavior, invariants, and proof requirements are specific to this feature;
- Implementer, Researcher, and Reviewer carry exact, available settings the user chose or confirmed, plus any honest limitation;
- no sentence permits pushing or opening PRs before the final question.
