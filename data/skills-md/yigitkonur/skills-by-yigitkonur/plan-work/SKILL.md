---
name: plan-work
description: Use skill if you are framing a vague request, comparing approaches, prioritizing a backlog, or defining risks, checkpoints, and decision criteria before acting.
---

# Plan Work

Use this skill to turn ambiguous or high-stakes work into a decision, sequence, or safe-to-learn experiment.

## Trigger boundaries

Use it when the main deliverable is:
- a clearer problem frame
- a decision with trade-offs
- a ranked or sequenced backlog
- a risk-aware execution plan
- a root-cause hypothesis for a recurring issue

Do not use it as a substitute for:
- external information gathering (`run-research`) -- use plan-work for reasoning over available context; hand off to run-research when the decision requires external data, benchmarks, or literature you do not have
- code writing or refactoring (`build-*`, `develop-*`)
- PR review (`review-*`)
- debugging or verification (`debug-*`, `test-*`)

If another skill owns execution, use this skill to structure the decision first, then hand off.

## Operating stance

1. Frame before fix.
2. Use the smallest method stack that improves clarity.
3. Match analysis depth to reversibility, evidence quality, and blast radius.
4. Prefer a concrete recommendation or next experiment over abstract discussion.
5. Always separate facts, assumptions, unknowns, and preferences (surface user preferences in step 2 framing).

## Reference router

Start with one file. Add a second only when it answers a different question. For a full overview of the reference library structure, see `references/README.md`.

| Need | Start with | Add only if |
|---|---|---|
| Vague, broad, or conflicting request | `references/01-intake-and-framing.md` | `references/09-thinking-methods-catalog.md` if method choice is unclear |
| Recurring failure or root-cause dispute | `references/02-root-cause-and-problem-solving.md` | `references/05-systems-thinking.md` if system effects dominate |
| Comparing options, technology, or architecture | `references/03-option-design-and-decision-quality.md` | `references/06-technical-strategy-and-architecture.md` for ADRs or technical strategy |
| Backlog overload or sequencing | `references/04-prioritization-and-sequencing.md` | `references/08-execution-risk-and-learning.md` if changing conditions threaten delivery |
| Side effects across teams or systems | `references/05-systems-thinking.md` | `references/07-communication-and-alignment.md` if alignment is the real bottleneck |
| Stakeholder alignment or decision communication | `references/07-communication-and-alignment.md` | `references/01-intake-and-framing.md` if goals or scope are still fuzzy |
| Execution risk, checkpoints, retros, or pivot triggers | `references/08-execution-risk-and-learning.md` | `references/04-prioritization-and-sequencing.md` if scope cuts or re-sequencing are needed |
| Unsure which thinking method fits | `references/09-thinking-methods-catalog.md` | the single domain file that matches the actual planning job |

## Default workflow

### 1. Classify the planning job

Pick one dominant job first:
- frame the problem *(see `references/01-intake-and-framing.md`)*
- diagnose a cause *(see `references/02-root-cause-and-problem-solving.md`)*
- compare options *(see `references/03-option-design-and-decision-quality.md`)*
- prioritize work *(see `references/04-prioritization-and-sequencing.md`)*
- align people *(see `references/07-communication-and-alignment.md`)*
- de-risk execution *(see `references/08-execution-risk-and-learning.md`)*

Precedence when multiple jobs apply: `diagnose > compare > prioritize > frame > align > de-risk`. Resolve the higher-precedence job first; the others often collapse once it is answered. When still tied, choose the job whose output the next decision-maker needs first.

State it explicitly in the output: `This is primarily a ___ decision/problem.`

Do not try to run every planning mode at once. If a second job emerges mid-workflow, complete the first fully, then start a second pass.

### 2. Frame the mission before proposing solutions

Capture:
- mission sentence: `We need to ___ so that ___ within ___ constraints.`
- success criteria and failure signals (success is observable when there is a metric, test, or outcome you could check)
- constraints and non-negotiables
- facts vs. assumptions (a fact has observable evidence you can point to; an assumption is an unverified belief -- label each)
- preferences: stakeholder or user priorities that are not hard constraints
- scope: in / out / unknown

Stop here and do not recommend a plan yet if any of these are true:
- the decision-maker is unknown
- success cannot be observed (no metric, test, or outcome you could check)
- 3+ core 5W2H questions are unanswered (5W2H = Who, What, Where, When, Why, How, How-much -- see `references/01-intake-and-framing.md` for template)
- critical unknowns have no owner or resolve-by date (for AI agents: owner = who can answer; resolve-by = can planning proceed without it?)

If blocked, return a decision-ready gap list instead of pretending the plan is ready. Format each gap as: (a) what is missing, (b) who can provide it, (c) what it blocks, (d) suggested default if no answer comes. If framing stays blocked after gap list, consult recovery paths below.

### 3. Choose the smallest useful method

Consult the reference router above to load the reference file matching your chosen method. The reference file contains templates, worked examples, and edge-case guidance essential for correct execution.

Use one primary method. Add one companion only if the primary method cannot answer a question the user explicitly asked.

| Situation | Use | Avoid |
|---|---|---|
| Several measurable options | Decision matrix *(ref 03)* | Hard choice model unless the real conflict is values |
| Values or principles conflict | Hard choice model *(ref 03)* | Fake precision with weighted scores |
| Single incident | 5 Whys *(ref 02)* | Full systems mapping unless evidence says the cause is systemic |
| Recurring or multi-cause issue | Iceberg / Ishikawa / hypothesis-driven RCA *(ref 02, 05)* | Stopping at `human error` or `bad communication` |
| Backlog overload | RICE or Impact-Effort, then MoSCoW for scope *(ref 04)* | Heavy scoring when the list is small or the data is fictional |
| Fast-changing execution | OODA + confidence-based pacing *(ref 08)* | Long upfront optimization loops |
| Executive communication | Minto Pyramid *(ref 07)* | Leading with background instead of the recommendation |

Method rule: if the first method already makes the choice clear, stop. Do not stack extra frameworks just to look rigorous. If the method table does not clearly match, see `references/09-thinking-methods-catalog.md` for the full method selection flowchart, or consult recovery paths below.

### 4. Build evidence and apply the method

Use evidence in this order:
1. local context (artifacts, prior attempts, observed behavior -- for codebases: config files, test results, git history, error logs)
2. direct signals (current outcomes, constraints, failure signatures)
3. external research only when it can change the decision

Execute the chosen method on gathered evidence. Concretely: if you chose a decision matrix, fill in the rows (options) and columns (criteria) with scored values. If you chose 5 Whys, write the chain of why questions. If you chose RICE, calculate each item's score. The reference file loaded in step 3 contains the template -- fill every cell.

Depth rules:
- **Type 2 (reversible, low blast radius):** bias to action. Recommend the simplest safe experiment and a short feedback loop.
- **Type 1 (hard to reverse, high blast radius):** require 2-4 viable options, explicit criteria, risks, fallback, and a review date.
- **Urgent but unclear situations:** make bounded assumptions, label them, and choose the smallest reversible step that will generate better evidence.
- If new evidence is not changing the recommendation, stop researching.

Evidence is enough when you can fill every cell of the method template AND articulate why the leading option wins over the second-best.

For technical work, document current architecture, failure modes, and performance characteristics before recommending structural change.

### 5. Decide, prioritize, or diagnose

For decision and prioritization jobs, generate 2-4 distinct options (including a minimal/fallback option) before selecting one. For root-cause jobs, generate 2-4 competing hypotheses. For framing jobs, proceed directly to the output shape below.

Apply the output shape that matches the job:
- **Decision:** include the selected option, why it wins, and why the others do not.
- **Prioritization:** force trade-offs. If more than 60% of items are `Must`, rework the categories.
- **Root cause:** trace to a system cause that can be changed, not just a symptom or person.
- **Execution planning:** define phases, dependencies, owners, checkpoints, verification, and pivot triggers.
- **Frame the problem:** deliver a completed mission sentence, prioritized gap list (distinct from step 2's blocking gap list -- this is the finished deliverable, not a blocker signal), and recommended next step to close the biggest remaining gap.
- **Align people:** deliver shared understanding document with points of agreement, open disputes, and proposed resolution process.

### 6. Package the answer for action

Follow the 9-section output contract below. The first four sections serve as the decision brief (recommendation, framing, and core logic); sections 5-9 provide execution detail.

If audience is known, lead with the recommendation for decision-makers and lead with sequence and ownership for executors. If audience is unknown, use the output contract section order as-is.

## Anti-derail guardrails

| Do this | Not that |
|---|---|
| Start with one reference file and one method | Load all references or stack 4 methods up front |
| Label assumptions and unknowns explicitly | Smuggle guesses in as facts |
| Use reversibility to decide how much analysis is enough | Wait for certainty on a reversible decision |
| Timebox framing and comparison work | Research forever because one more artifact might appear |
| Switch to a simpler method when a framework adds no clarity | Keep a method running because you already started it |
| End with checkpoints, pivot triggers, and verification | End with vague advice like `monitor progress` |
| Hand off to the execution skill once the plan is decision-ready | Keep planning after the useful planning work is done |

## Recovery paths

- If the request stays vague after framing, return:
  - a mission draft
  - the top missing inputs
  - the next best questions
  - the reference file to open first
- If options remain tied, use reversibility as the tiebreaker and choose the easier-to-undo path.
- If debate is really about values, stop scoring and switch to the hard choice model (see `references/03-option-design-and-decision-quality.md`).
- If conditions change faster than the plan, shift into OODA + checkpoint/pivot mode via `references/08-execution-risk-and-learning.md`.
- If a plan depends on unknowns you cannot resolve yet, recommend a safe-to-learn experiment or an explicit research task instead of a fake commitment.

## Steering experiences

Real execution mistakes discovered through derailment testing. Read these before your first run.

### SE-01: Reference files exist but agents never load them
The reference router table maps needs to files, but nothing in the workflow forces you to open them. Always consult the reference router in step 3 to load the file matching your chosen method. If you skip this, you will use method names without understanding their templates.

### SE-02: Method execution falls into a gap
Steps go: choose method, gather evidence, decide. But actually executing the method (filling in the matrix, running 5 Whys) is part of step 4. If you gather evidence without applying it to the method template, you produce generic analysis instead of structured output.

### SE-03: Two output structures both claim to be default
Step 6 describes "decision brief + execution detail" and the output contract defines 9 sections. These are not competing. The first 4 output contract sections ARE the decision brief; sections 5-9 are execution detail. Follow the output contract.

### SE-04: Domain terms used without definition
5W2H, Type 1/Type 2, Decision Frame are defined inline in the workflow steps above. If you encounter a term you do not recognize, re-read the step definitions before consulting reference files.

### SE-05: "Enough evidence" has no threshold
Evidence is enough when you can fill every cell of the method template AND articulate why the leading option wins over the second-best. If you cannot do both, you need more evidence.

### SE-06: AI agents lack organizational context
When the skill says "owner" or "audience," translate for your context: owner = who can answer this question. Audience = if unknown, use the output contract section order as-is. Resolve-by = can planning proceed without this answer?

### SE-07: Agents stack methods for rigor theater
The skill says "use one primary method." Agents add 2-3 companions "to be thorough." The companion rule is strict: add one ONLY if the primary cannot answer a question the user explicitly asked. If the primary already answers the question, stop.

## Output contract

Unless the user asks otherwise, respond in this order:

1. Mission Snapshot
2. Planning Job + Chosen Method(s)
3. Facts, Assumptions, and Unknowns
4. Decision Frame (the decision to be made, who decides, constraints, and deadline), Root Cause, or Priority Logic
5. Options or Ranked Work
6. Recommendation and Why Not the Alternatives
7. Execution Plan
8. Risks, Checkpoints, Pivot Triggers, and Verification
9. Immediate Next Actions or Open Questions

## Done conditions

Planning is complete (substantive completeness) when:
- the problem or decision is stated in one sentence (check: can you say it in under 15 seconds?)
- the chosen method is justified (check: can you explain why the alternatives were worse fits?)
- the recommendation or next experiment is clear (check: could someone act on it without asking you a follow-up?)
- trade-offs are visible (check: would a reader know what they are giving up?)
- verification and revisit conditions exist (check: is there a specific metric, date, or trigger?)
- unresolved unknowns are explicit, owned, and time-bounded

If you cannot meet those conditions, stop with a decision-ready gap list instead of pretending the plan is complete.

## Final quality gate

Before finalizing, check communication quality:

- [ ] Are we solving the right problem?
- [ ] Did we choose the smallest useful method?
- [ ] Are facts, assumptions, unknowns, and preferences clearly separated?
- [ ] Did we match analysis depth to reversibility and risk?
- [ ] Are trade-offs and rejected alternatives visible?
- [ ] Does the answer include verification, checkpoints, and pivot triggers where needed?
- [ ] Is the plan communicated in the right order for the audience?
- [ ] Did I load the reference file for my chosen method?
- [ ] Can I fill every cell of the method template with evidence I gathered?

If any answer is `no`, revise before finalizing.

## Final reminder

Before delivering, verify you loaded only the reference files you actually used. If any reference was opened but not cited in the output, drop it. Stop planning once the next action is decision-ready. Every reference file contains a "Steering experiences" section at its end -- read it when you load the file.
