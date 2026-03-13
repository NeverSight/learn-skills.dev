---
name: brainstorm
description: Brainstorm competing solutions to a problem using parallel agents. Use when you need to explore multiple different approaches to the same problem, compare trade-offs, and choose the best path forward. Spawns parallel proposer agents who each design an independent solution, then peer-review each other's work before a structured comparison.
---

# Brainstorm

Generate and evaluate competing solutions to a problem using parallel agents. Each proposer independently designs an approach, then all proposers critique each other's work. The lead synthesizes everything into a structured comparison for the user to choose from.

## When to Use

- "What's the best way to..." — open-ended design questions
- Multiple valid approaches exist and trade-offs are unclear
- You want to explore the solution space before committing to an implementation
- Architecture or design decisions that will be hard to reverse
- The user explicitly asks to brainstorm, compare approaches, or evaluate options

## When NOT to Use

- The problem has one obvious solution — just do it
- Debugging — use `competing-hypotheses` instead
- Multi-part problems that need parallel research — use `team-solve` instead

---

## Instructions for Claude

You are the **facilitator** orchestrating a structured brainstorm.

### Coordination Protocol

Messages between teammates are **asynchronous** — a message sent now may not be read until the recipient finishes their current work. You cannot rely on message timing for coordination. Instead, **task status is the shared state** that tells every agent where things stand.

#### Task Status as Position Marker

When a teammate receives a message, they determine where it sits in the conversation by checking their task status — not by assuming it arrived "just now."

| Status | Who sets it | Meaning |
|--------|------------|---------|
| `pending` | Lead | Not started, waiting for assignment |
| `in_progress` | Teammate | Working, or finished and **parked** waiting for lead to acknowledge |
| `completed` | **Lead only** | Lead has read the teammate's report — this IS the acknowledgment |

**The lead marks tasks `completed` — not the teammate.** When a teammate sees their task marked `completed`, they know the lead has processed their report and any new message is current.

#### Teammate Protocol

Include these rules in every teammate's spawn prompt:

1. Mark your task `in_progress` when you begin work
2. **Read your task with `TaskGet`** — the task description contains everything you need (proposals to review, feedback to incorporate, etc.). Do NOT search the filesystem or other agents' files for this content.
3. If your task description is missing required content (e.g., a review task with no proposals), tell the lead immediately and park. Do not improvise.
4. When done, send your report via `SendMessage`, then **park** — stop all work, do not check `TaskList` or claim new tasks. Just wait.
5. Before acting on any received message, **check your task status via `TaskGet`**:
   - Still `in_progress` → lead hasn't acknowledged your report yet. This message may pre-date your report. Reply with your current state instead of re-executing.
   - `completed` → lead has processed your report. If a new task is assigned to you, this message contains current instructions — proceed.
6. Wait for all spawned subagents to finish before sending your report. Do not leave background work running.

#### Lead Protocol

1. After reading a teammate's report, mark their task `completed` (your acknowledgment)
2. Before sending new instructions, ensure the previous task is `completed` and the new task is created/assigned
3. Verify phase completion via `TaskList` — check that all relevant tasks show the expected status, don't track messages mentally

### Phase 1: Problem Framing

Before spawning any agents, establish a clear problem frame.

1. Parse the user's input to understand:
   - **The problem**: What needs to be solved or decided?
   - **Constraints**: Budget, timeline, tech stack, compatibility, team skill set, etc.
   - **Goals**: What does success look like? Performance, maintainability, simplicity, extensibility?
   - **Context**: What exists today? What's already been tried or ruled out?
2. If the problem is underspecified, ask clarifying questions — good brainstorming needs clear constraints
3. Define **evaluation criteria** — the dimensions proposals will be compared on. Common ones:
   - Complexity (implementation effort)
   - Risk (what could go wrong)
   - Performance / scalability
   - Maintainability (long-term cost)
   - Flexibility (how well it adapts to future changes)
   - Adjust these based on what matters for this specific problem
4. Decide the **spread** — aim for a range of approaches, not N variations of the same idea. For example:
   - One **direct/simple** approach (least effort, fewest moving parts)
   - One **robust/thorough** approach (handles the most edge cases, most future-proof)
   - One **unconventional** approach (different paradigm, creative reframing)
   - Adjust based on the problem — not every brainstorm needs a radical option, and some problems deserve two pragmatic approaches over a forced creative one
5. Present the framing to the user:
   - Problem statement, constraints, and evaluation criteria
   - Planned number of proposers (2-4) and the angle each will take
   - Ask: "I'll spin up N proposers to design competing approaches. Proceed?"

### Phase 2: Parallel Proposals

Proposals are developed **in parallel** and **independently** — no cross-pollination.

1. Create a team with `TeamCreate`
2. Create a proposal task per proposer with `TaskCreate`
3. Spawn one `general-purpose` teammate per proposal using `Task` with `team_name`
   - Name them after their angle (e.g., `simple-approach`, `event-driven-approach`, `plugin-architecture`)
   - Each proposer's prompt must include:
     - The full problem statement, constraints, and evaluation criteria from Phase 1
     - Their assigned angle/direction (but emphasize they should follow the evidence — if research shows their angle is a bad fit, say so rather than forcing it)
     - Instruction to **research the codebase/context and design an approach, do not make changes**
     - The **Teammate Protocol** from the Coordination Protocol above (copy it into their prompt verbatim)
     - The subagent guidance below (copy it into their prompt)
     - Instruction to report their proposal via `SendMessage` using the proposal format below
   - **Spawn all proposers in parallel**
4. As proposers report back, mark each proposal task `completed` (acknowledging the report) and give the user brief progress updates
5. **Do NOT shut down proposers when they report back** — they are needed for Phase 3 and 4

#### Subagent Guidance for Proposers

Include the following in each proposer's prompt:

> **Use subagents (`Task` tool) to keep your context focused.** Spawn subagents for:
> - Exploring the codebase to understand existing patterns, dependencies, and constraints
> - Researching specific libraries, APIs, or approaches you're considering
> - Checking feasibility of a particular direction before committing to it
> - Investigating how similar problems have been solved elsewhere in the codebase
>
> Each subagent should report back:
> 1. **Relevant findings** — what it discovered that matters to your proposal
> 2. **Dead ends** (1-2 sentences) — approaches that *look* viable but *aren't*, and why
>
> When choosing subagent types, prefer read-only or exploration-focused types for codebase searches, and full-capability types for targeted analysis needing deeper tool access (e.g., running commands to test feasibility) — but no changes to files.

#### Proposal Format

Each proposer should structure their report as:

```
## Proposal: {title}

### Summary
{2-3 sentence overview of the approach}

### Design
- {how it works, key components, data flow}
- {which files/modules would be created or changed}
- {key implementation decisions and why}

### Strengths
- {what this approach does well}
- {which evaluation criteria it scores highest on}

### Weaknesses
- {known limitations or downsides}
- {which evaluation criteria it scores lowest on}

### Risks & Open Questions
- {what could go wrong}
- {unknowns that would need to be resolved during implementation}

### Effort Estimate
{relative sizing: small / medium / large, with brief justification}

### Confidence: {high/medium/low}
{how confident are you this approach would work well?}
```

### Phase 3: Peer Review

Each proposer reviews **all other proposals** — not just votes, but substantive critique.

1. Once all proposal tasks show `completed` in `TaskList`, collect all proposals
2. For each proposer, create a review task with `TaskCreate`. **Include in the task description:**
   - The full text of all OTHER proposals (not the proposer's own)
   - The evaluation criteria from Phase 1
   - The review instructions and format below
3. Assign each review task to its proposer and send them a message saying their review task is ready — the task description contains everything they need
4. **Send all review messages in parallel** — proposers review simultaneously
5. As reviewers report back, mark each review task `completed` (acknowledging the report) and give the user brief progress updates

#### Review Instructions

Include the following in each review message:

> Review each of the other proposals below. For each one, provide an honest assessment — you are not competing, you are helping the user make a good decision. Be specific and constructive.
>
> **Important:**
> - Identify genuine strengths even in approaches very different from yours
> - Flag gaps or risks the proposer may have missed
> - Note if a proposal overlaps significantly with yours or could be combined — but do NOT advocate for merging unless it's genuinely better. Distinct good options are more valuable than a forced compromise.
> - If you see something in another proposal that makes you want to revise your own approach, note it — you'll get a chance to revise next

#### Review Format

Each reviewer should structure their report as:

```
## Reviews by {your proposal title}

### Review of "{other proposal title}"
**Strengths I see:**
- {what this approach does well that's worth preserving}

**Gaps or risks missed:**
- {things the proposer didn't address}

**Questions:**
- {things that are unclear or need more detail}

**Would I adopt any of this?**
{yes/no — and what specifically, if yes}

### Review of "{another proposal title}"
...

### Self-reflection
{After seeing the other proposals, what would you change about your own? Be specific.}
```

### Phase 4: Revision

Proposers get one chance to strengthen their proposal based on peer feedback.

1. Once all review tasks show `completed` in `TaskList`, collect all reviews
2. For each proposer, create a revision task with `TaskCreate`. **Include in the task description:**
   - The full text of all reviews OF their proposal from other proposers
   - Their own self-reflection from Phase 3
   - The revision instructions below
3. Assign each revision task to its proposer and send them a message saying their revision task is ready — the task description contains everything they need
4. **Send all revision messages in parallel**
5. As revised proposals come back, mark each revision task `completed` (acknowledging the report) and give the user brief progress updates

#### Revision Instructions

Include the following in each revision message:

> You've received feedback from the other proposers. Revise your proposal to address legitimate gaps — but **do not abandon your core approach** to converge with others. The goal is to make YOUR approach as strong as possible, not to become a hybrid of all approaches.
>
> Specifically:
> - Address gaps and risks that reviewers flagged (if they're valid)
> - Clarify anything reviewers found unclear
> - Incorporate good ideas from other proposals **only if** they genuinely improve your approach without fundamentally changing it
> - If a reviewer's criticism doesn't apply or is based on a misunderstanding, briefly explain why
>
> Use the same Proposal Format as before, but mark what changed. Add a "Changes from v1" section at the end listing what you revised and why.

### Phase 5: Structured Comparison

The lead synthesizes everything into a clear comparison for the user.

1. Once all revision tasks show `completed` in `TaskList`, gather final proposals
2. Build a **trade-off matrix** — evaluate each proposal against the criteria from Phase 1:

   | Criteria | Proposal A | Proposal B | Proposal C |
   |----------|-----------|-----------|-----------|
   | Complexity | ... | ... | ... |
   | Risk | ... | ... | ... |
   | ... | ... | ... | ... |

3. For each proposal, summarize:
   - Core idea (1-2 sentences)
   - Key strength (what makes it worth considering)
   - Key risk (the biggest thing that could go wrong)
   - Peer consensus (what did other proposers agree on about this approach?)
4. Note any **surprising agreements** — if all proposers flagged the same risk or praised the same aspect across proposals, highlight it
5. If proposals exist at different points on a genuine trade-off spectrum (e.g., simple-but-limited vs complex-but-flexible), present them as distinct options — do NOT try to merge them into a compromise unless the user asks for a hybrid
6. Provide a **recommendation** if one proposal clearly dominates, or frame the choice if it's genuinely a matter of preference/priorities
7. Present to the user and ask which direction they'd like to go (or if they want to explore further)

### Phase 6: Handoff

This skill ends at recommendation — it does not implement.

1. Once the user chooses an approach, summarize it as a clear brief:
   - The chosen proposal (final revised version)
   - Key decisions and rationale
   - Known risks and mitigations
   - Suggested implementation order or first steps
2. Send shutdown requests to all teammates and **wait for each to confirm** before wrapping up
3. The user can then implement directly, or hand the brief to `team-solve` for structured implementation

### Rules

- **Independence during proposals** — proposers must not see each other's work until Phase 3
- **Honest peer review** — reviewers should be constructive critics, not competitors trying to undermine alternatives
- **Preserve diversity** — the goal is distinct good options, not convergence. Two proposals at opposite extremes are better than one lukewarm compromise
- **Revision, not revolution** — Phase 4 strengthens proposals, it doesn't replace them. If a proposer wants to fundamentally change their approach, that's a signal the original angle was wrong, not that they should morph into someone else's proposal
- **2-4 proposers** — fewer than 2 isn't a brainstorm; more than 4 produces diminishing returns and review fatigue
- **Task status is the source of truth** — coordinate through `TaskUpdate` status, not message timing. Always check `TaskList` to verify state.
- **Teammates park after reporting** — after sending a report, stop and wait. Do not self-assign new work or act on queued messages without checking task status first.
- **Lead owns `completed`** — only the lead marks tasks `completed`. This is the acknowledgment that closes the loop.
- **Subagents are cheap, context is expensive** — proposers should offload research to subagents rather than doing everything inline
- **Finish subagents before reporting** — wait for all spawned subagents to complete before sending your report
- **Tasks carry the content** — review and revision tasks must include the full text of proposals/feedback in the task description. Teammates should `TaskGet` their assigned task to find everything they need. Do NOT search the filesystem, team config, or other agents' scratch files for proposals or feedback.
- **Missing content? Park and ask.** — if a teammate receives a review or revision task but the task description doesn't contain the proposals/feedback they need, they should immediately tell the lead "Task is missing required content, parking until provided" and stop. Do not improvise by searching for the content elsewhere.
- **No implementation** — this skill produces a recommendation, not code. Hand off to `team-solve` or direct implementation.
- If a teammate goes idle, that's normal — send them a message when it's their turn
- **Unresponsive teammate?** — if a teammate hasn't reported within a reasonable timeframe, check their task status. If stuck, spawn a replacement and inform the user.
