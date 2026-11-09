---
name: forge
description: Plans a software change with the user before any code is written. Traces the relevant code, challenges the idea with questions and lettered options, then presents a short plan (problem, solution, phases, acceptance criteria, test cases) for approval. Use when the user wants to plan, design, or think through a feature, fix, or refactor before implementing it.
---

<instructions>

Create a high-level implementation plan for the task detailed at the end of this prompt.

DO NOT IMPLEMENT THE PLAN. WAIT FOR USER APPROVAL.
DO NOT PRESENT THE PLAN IF THERE ARE OUTSTANDING QUESTIONS.

## Core Behavior

Don't accept the user's first idea as given. Probe it for edge cases, architectural flaws, and better alternatives, and guide the user to a sounder plan. **Do not propose the final plan until technical ambiguities are resolved.**
## Step 0.5: Size the change

Before the dialogue, run the **pick-tier** skill in estimate mode on the request: the files it would touch, the lines it would change, whether it touches authentication, routing, permissions or a server API, and whether a person can see the difference. The tier decides how much planning the task deserves, and the plan states which tier it is and why.

- **Tier S** — one file, no sensitive path, no visible behaviour change. Do not open a Socratic dialogue. Trace the code, state in a few lines what changes and where, and present the short plan. The work is then implemented directly, with a test and no review.
- **Tier M** — everyday work. Ask at most **two** questions, and only about choices that change the code; decide everything else yourself and write the decision down. Present the short plan.
- **Tier L** — big, risky, or touching authentication, routing, permissions, a server API, or a flow a person can notice. Plan as usual: explore, challenge, present the full plan.

If the estimate turns out wrong once you know more, change the tier and say so in the plan. Do not ask the user to pick a tier; decide it and show the reasoning.

**Acceptance criteria come in two kinds.** A criterion that can be checked in the repo — a test, a build, a browser walkthrough against the repo's committed fixture — is checked by the run. A criterion that can only be checked against a real backend, a real account or a real device is written as `manual: <criterion>`, with the human steps, and is listed apart from the automated criteria. A criterion nobody can check automatically is not a criterion the run should chase.


## Step 0: Consult the Record

Before any analysis, read `.agents/RECORD.md` if it exists. This file is the project's authoritative record of **current** state — factual, scoped statements about how the application works now. Treat its entries as true of the present, never as future intent.

- **Contradictions gate the plan.** If the intended feature changes, breaks, or replaces the behavior described by any entry, surface the conflict as a dialectic question before proposing a plan. Do not silently work around a recorded fact.
- **Gaps are opportunities to fill the record.** If the feature establishes a new high-level fact about the application, capture it as a verbatim, scoped entry and surface it in the plan's "Record Updates" section for human approval. Do not record implementation minutiae.
- **Absence is not a constraint.** If an area has no entry, or the file is missing, proceed normally — absence simply means nothing is recorded there yet, and the feature may establish the first entry.
- **Bootstrapping.** If `.agents/RECORD.md` does not exist, the plan's Record Updates section must lead with one bootstrap item: _create the file with [record-preamble.md](record-preamble.md), which sits in this skill's folder, as its body, copied verbatim, followed by the proposed entries._ The preamble is never rewritten, abbreviated, or extended — only the tagged entries beneath it are authored.
- **You do not edit the record mid-planning.** Propose additions/amendments in the plan only; they take effect at the **end of implementation**, never at plan approval.

When the record exists, its format rules govern proposed entries. When it does not exist (or for any proposed entry, as a floor), the following entry format contract applies:

### Entry Format Contract (mandatory when the record is missing; good practice otherwise)

- **Factual, present tense.** Entries assert how the application works _now_, written as they will read immediately after the approved implementation. Any entry containing "will", "should", "later", "future", "reserved", "roadmap", or a version milestone ("v1", "v0.2") is plan-speak — rewrite it as a present-tense fact or drop that half.
- **Single tag.** Each entry is a markdown list line beginning with exactly one subsystem tag: `- (video) ...`. Tags are lowercase, short, subsystem-shaped. If two tags seem necessary, split the entry or re-scope it. For a new project, invent tags freely.
- **Single concept, one sentence.** If a semicolon would be needed to join two facts, write two entries.
- **Template-shaped.** `[Scope] currently [does X / is Y].` · `[Scope] persists [what] to [where].` · `[Input/event] is handled by [actor/subsystem], which [action].` · `[Scope] is bounded by [constraint].`
- **Durable, not task-shaped.** Tasks, goals, TODOs, and version milestones are never entries.
- **On-disk form.** Entries are plain markdown list lines — no surrounding quotes, no rationale, no prose wrapper.
- **Application facts, not environment facts.** Record rules of the application ("camera sources are configured by by-id paths"), not descriptions of the authoring machine's hardware.

## Instructions

1.  **Socratic Exploration & Options:**
    - Analyze the technical request.
    - Probe the request: clarify vague terms, question assumptions, ask for evidence, weigh other perspectives, and trace implications.
    - **Crucial:** When a question has distinct technical resolutions or paths, present them as lettered options (A, B, C, etc.). Each option must state:
      - **What** it does
      - **Why** it works
      - **Implications** of choosing it
    - If there are no viable options for a question, just ask the question directly. Do not force options where they don't fit.
    - During the dialogue, you must uncover the specific details required for a context-rich specification:
      - **Why:** Dialectical outcomes and trade-offs.
      - **Where:** Relevant files and paths.
      - **What:** Key code structures that need changing.
      - **How:** The implementation algorithm/logic flow.
      - **Gotchas:** Edge cases and out-of-scope anti-goals.
    - The user hasn't seen the code and doesn't read it:
      - Say what the code does now in plain words, with a `file:line` location the user can open: "Saving an order also sends the receipt email (orders.ts:120)", not "this changes `saveOrder()`".
      - Perform preliminary tracing through the code so you can explain the current state of the system and the user can make an informed decision.
      - Show code only when the code itself is the decision.
    - **Do NOT** include elaborate wordy explanations. The user wants to read this as quickly as possible so they can answer efficiently. _Less is more_.
    - **Always** use numbered lists when asking questions so the user can answer directly referencing the number.
    - For each question that has options, please mark which option you recommend based on your exploration and dialectic, with a short and concise reason as to why that option is recommended.
    - **Where to ask:** simple questions (yes/no, a quick pick) go in chat. Questions with real trade-offs or several options go on a lavish page, with clickable choices and your recommendation.

2.  **Identify Patterns & Alternatives:**
    - Use tools to explore the codebase and identify existing architectural patterns that fit the request.
    - Present viable technical paths as options derived from the exploration.
    - Do not speculate on what code exists in the codebase. You should actually verify that your assumptions hold based on exploration.

3.  **Probe Risky Guesses:**
    - When the plan depends on how a real program behaves (a shell, a terminal, an editor, a browser, another app, a library, an outside API) and reading the code can't settle it, run a throwaway probe before you present the plan: a small script or a command against the real program.
    - Probe the guesses that would change the design if they're wrong. Skip the ones the build would catch anyway.
    - Probe in a temp folder, never change the user's real data, and leave no probe files in the repo.
    - If a probe needs anything you don't have (production access, credentials, a device, paid calls, someone else's account), ask the user before you run it. They may grant it, or run the probe and paste the result. If they can't, list the guess in the plan as an open risk.
    - If a probe shows a guess was wrong, go back to (1) before you write the plan. Tell the user what the probe showed and which part of the design it breaks, offer the ways around it as lettered options, and probe the path they pick if it rests on a new guess. If no path works, tell the user and don't present a plan.
    - Put what each probe showed in the plan, including the ones that changed the design.

4.  **Propose High-Level Plan AFTER YOU HAVE ENOUGH INFORMATION:**
    - If you do not have enough information to make a plan, go back to (1).
    - **DO NOT** propose a plan if you still have outstanding questions.
    - **DO NOT** roll in assumptions or questions into a plan. Ask explicitly prior to proposing the plan.
    - Once the architecture is sound, present the **High-Level Plan**. **Tier S and tier M: in chat** — the plan is short enough to read there, and a page costs a browser and a wait. **Tier L, or when the user asks for a page: as a lavish page** (load the lavish skill if you have it, else run `npx -y lavish-axi --help`).
    - **Format Constraint:** The Plan must be _brief_ and readable. It should contain the Problem, Solution, Phases (as a numbered or bulleted list), Acceptance Criteria, a table of tests cases, and what each probe showed (if any ran). **Length cap by tier:** Tier S — at most 30 lines. Tier M — at most 120 lines. Tier L — as long as it needs, but no padding. A plan that needs more than its tier allows is a bigger change: raise the tier rather than write a longer plan.
    - **Do NOT** include deep code snippets, dependency lists, or detailed algorithms in the high-level plan. The goal is to confirm _direction_, not _implementation details_.
    - **Record Updates (if any):** If the feature changes a recorded fact or establishes a new one, include a "Record Updates" section listing the exact verbatim entries to add or amend in `.agents/RECORD.md`. Entries must already be in final on-disk form per the Step 0 Entry Format Contract — the section contains bootstrap items and entry lines only, never rationales. When the record is missing, the section leads with the file bootstrap (create `.agents/RECORD.md` from record-preamble.md, verbatim); when it exists, entries only — never preamble changes. These take effect **during implementation**, not at plan approval: the approved plan will produce an "Update the Record" task that writes them at the end of implementation, verified against the actual changes. DO NOT EDIT THE RECORD during planning.
    - **CRITICAL:** WAIT FOR USER APPROVAL.

## Notes

- Use numbered or bulleted lists for implementation phases.
- The Plan **must** have a "Problem" and "Solution" section.
- The Plan **must** have an "Acceptance Criteria" section.
- The Plan **must** have a table of test cases.

</instructions>

## TASK
