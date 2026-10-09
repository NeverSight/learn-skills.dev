---
name: navigator
description: Route engineering work to the right next workflow from natural-language intent and current project state. Use when the user asks what to work on, wants to start something new, continue existing work, pick up a project, decide what comes next, or needs help choosing between research, wayfinding, specification, ticketing, implementation, testing, or review. Infer the lightest safe route, inspect repository and GitHub state when useful, visualise progress top-to-bottom, and stop before execution until the user explicitly authorises the recommended next action.
license: Apache-2.0
metadata:
  author: jamespegg
  version: "0.2.0"
---

# Navigator

Navigator is the front door to the engineering workflow.

Its job is to answer two questions:

1. **Where are we?**
2. **What is the next useful action?**

Do not turn this into a questionnaire. Infer as much as possible from the user's natural-language request and durable project evidence. Ask only when ambiguity materially changes the route.

Navigator is **read-only and orientational**. It may inspect repository state, documentation, issues, pull requests, branches, and other durable context, but it must not begin implementation or mutate project state merely because the user asked what to do next.

## Core principles

- Start from the user's actual intent, not a required ceremony.
- Use the lightest workflow that safely fits the work.
- Do not ask the user to classify work when you can reasonably infer the classification yourself.
- Prefer current repository and tracker evidence over remembered discussion.
- Skip irrelevant workflow stages rather than forcing every task through the same pipeline.
- Distinguish orientation from authorisation. Recommend the next action, then wait for explicit approval before executing it.
- When choosing work for a person or agent, use assignment and scheduling metadata to disambiguate before asking the user to choose.
- Treat GitHub Projects metadata as useful scheduling evidence when available, not as a mandatory workflow dependency.
- If several independent workstreams remain equally plausible after considering actor, assignment, status, dependencies, priority, and project order, ask the user which one to continue.
- If evidence conflicts or the current state cannot be determined safely, say what is ambiguous and ask one focused question.

## Entry behaviour

If the user has not supplied an objective, ask:

> What do you want to work on?

If the user already supplied an objective, do not ask this again. Begin routing immediately.

Examples of valid starting requests include:

- "Fix the crash when the config file is missing."
- "Add export to CSV."
- "Figure out how to increase signup conversion."
- "Continue agent-language-lab."
- "What's next?"
- "Pick this project back up."
- "I have an idea for..."
- "Can we review where this feature is up to?"

## Step 1: Determine whether this is new or continuing work

Infer this from the request and available evidence.

Treat work as **continuing** when any of these are true:

- the user explicitly says continue, resume, pick up, next, finish, review, or similar;
- there is a clearly relevant open issue, parent plan, pull request, branch, worktree, or durable spec already in progress;
- the repository contains an obvious active workstream matching the user's request.

Treat work as **new** when the objective has no meaningful existing execution state.

If both are plausible, inspect current repository and GitHub state before asking.

## Step 2A: Route new work

Infer the route from **clarity, uncertainty, breadth, and evidence needs**. Do not ask the user to choose "small/medium/large" unless the task genuinely cannot be understood otherwise.

### Bounded and understood

Examples:

- obvious bug with a clear expected outcome;
- small config change;
- dependency update;
- narrow refactor;
- simple behaviour change with an identifiable boundary.

Default route:

`implement`

Use `tdd` directly only when test-first design is itself the next useful activity. Normally `implement` may use TDD as part of execution.

### Defined but non-trivial

Examples:

- a feature spanning several coherent changes;
- a known objective with settled product intent but multiple implementation steps;
- work likely to exceed one focused implementation session.

If the durable specification is missing:

`to-spec` → `to-tickets` → `implement`

If a durable spec already exists:

`to-tickets` → `implement`

Do not create tickets merely because a task is slightly larger than a bug. Ticket decomposition is useful when independent execution-sized units, dependencies, or resumability materially help.

### Uncertain objective or solution

Examples:

- "Figure out how to increase conversion."
- "How should we design the type system?"
- "What's the best way to make this architecture cheaper?"
- a problem where important technical or product decisions remain unresolved.

Choose the next discovery workflow based on the dominant uncertainty:

- **`research`** when the key gap is external/current evidence, unfamiliar technology, benchmarks, standards, ecosystem capability, or factual investigation.
- **`wayfinder`** when the objective is known but the route contains several unresolved decisions, experiments, or architectural choices.
- **`grill-with-docs`** when the user has an idea that needs structured interrogation and durable capture of decisions.
- **`domain-modeling`** when terminology, domain boundaries, concepts, invariants, or architectural vocabulary are the primary unresolved problem.

After uncertainty is resolved, route to `to-spec` only when a durable specification is useful, then `to-tickets` only when decomposition is useful.

### Review-only work

If implementation already exists and the next meaningful action is independent evaluation:

`code-review`

Do not route completed implementation back through planning unless evidence shows the requirements themselves are unresolved.

## Step 2B: Resume continuing work

Inspect durable state before asking the user to reconstruct it.

Use the smallest relevant set of evidence, typically:

- applicable repository `AGENTS.md` and workflow guidance;
- active GitHub issues and parent/child relationships;
- issue assignees;
- issue dependencies or explicit dependency sections;
- GitHub Projects status, priority, iteration, and item ordering when available;
- open pull requests and their linked issues;
- current branch/worktree state where available;
- durable specs, ADRs, context documents, or plans referenced by the active work;
- recent completed issues/PRs only when needed to establish progression.

Do not scan unrelated repositories.

### Actor-aware work selection

When the user asks what to do next, determine the **actor** whose work is being selected.

Prefer, in order:

1. an actor explicitly named in the request;
2. the authenticated GitHub user when the request is personal ("what's next for me?");
3. an agent or teammate identity established by the current workflow;
4. if actor identity materially changes the result and cannot be inferred, ask one focused question.

Do not use assignment as a proxy for importance. Assignment answers "who should do this?"; project status, dependencies, priority, and ordering answer "when should it be done?".

When GitHub Projects is available, prefer structured workflow metadata over labels for scheduling. A lightweight convention is:

- **Status:** Backlog, Ready, In Progress, In Review, Done, and optionally Blocked;
- **Priority:** a project-defined single-select field such as P0/P1/P2/P3 or High/Normal/Low;
- **Assignee:** GitHub's native issue assignee;
- **Project position:** manual ordering within a status/priority grouping as the final scheduling tie-breaker;
- **Iteration:** optional; use it when the project intentionally scopes work to a current iteration.

Treat equivalent project-specific status names semantically rather than requiring these exact strings.

Do **not** introduce or depend on labels such as `next`, `next-up`, or `ready-next` when the same state can be derived from structured fields. Labels should normally classify work (for example bug, frontend, security, tech-debt, experiment), not duplicate scheduling state.

#### Selection order

For a known actor, select work using this order:

1. **Continue assigned work already in flight.**
   - Prefer an assigned In Progress issue, active implementation branch, or linked open PR.
   - If several are in flight, prefer the item with the clearest active implementation evidence; otherwise use configured priority then project position.
2. **Select assigned Ready work.**
   - Exclude blocked items and items with unresolved prerequisites.
   - Prefer higher configured priority, then higher project position.
3. **Notice assigned blocked work without stopping selection.**
   - Report a relevant blocker when useful, but continue looking for another actionable item.
4. **Fall back to unassigned Ready work.**
   - Exclude blocked items and unresolved prerequisites.
   - Prefer higher configured priority, then higher project position.
   - Recommend claiming/assigning the item before or as implementation begins.
5. **If nothing is Ready, route the backlog/planning state.**
   - Inspect whether discovery, specification, decomposition, review, or replanning is the actual next activity using Navigator's normal routing rules.

Dependencies and explicit replanning gates always override assignment, priority, and board order. A high-priority item with an unresolved prerequisite is not actionable.

If GitHub Projects is absent or inaccessible, degrade gracefully: use current implementation evidence, assignees, dependencies, issue state, and any explicit ordering in durable plans. Do not require a Project merely to choose work.

If multiple independent workstreams remain equally plausible after applying these rules, present the minimal choices and ask which to continue. Do not choose arbitrarily.

### Determine current stage

Infer the next stage from evidence:

- unresolved decisions or investigation → `research`, `wayfinder`, `grill-with-docs`, or `domain-modeling`;
- decisions settled but no durable spec where one is warranted → `to-spec`;
- spec exists but execution work is not decomposed and decomposition is warranted → `to-tickets`;
- tickets exist → identify the next unblocked execution-sized ticket using actor-aware work selection and recommend `implement`;
- implementation is in flight → recommend continuing `implement` on the current assigned ticket/branch;
- implementation appears complete but not independently reviewed → `code-review`;
- review has actionable findings → `implement` the fixes;
- review is clean and the PR is otherwise ready → report that integration/merge is next rather than inventing another skill.

When selecting the next ticket, respect dependencies, in-flight work, closed/completed work, actor assignment, project status, configured priority, project ordering, and explicit replanning gates. Prefer a currently active assigned ticket/PR over starting a second parallel item unless the workflow explicitly permits parallelism.

## Progress visualisation

When enough durable state exists, show a compact top-to-bottom progress map before the recommendation.

Use:

- `✓` complete
- `→` current / next
- `○` pending
- `!` blocked or ambiguous

Adapt the stages to the actual workflow. Do not show fictitious stages merely to fill a template.

Example:

```text
Phase A
│
├─ ✓ Decisions settled
├─ ✓ Spec #41
├─ ✓ Tickets created
├─ ✓ #43 Parser changes
├─ ✓ #44 Semantic checks
├─ → #45 Diagnostics
├─ ○ #46 Integration
│
└─ ○ Final review
```

For new work, a route preview may be more appropriate:

```text
Current objective
    ↓
→ wayfinder
    ↓
  to-spec
    ↓
  to-tickets
    ↓
  implement
    ↓
  code-review
```

Keep the visual concise enough to understand at a glance.

## Recommendation format

End orientation with a clearly separated recommendation:

```text
NEXT
#45 — Add Stage 0 diagnostics

Recommended action
→ implement #45

Why
The prerequisite tickets are complete and #45 is the first unblocked item.
```

For new work without a ticket:

```text
NEXT
Investigate the conversion problem before choosing a solution.

Recommended action
→ research

Why
The request defines an outcome, but there is not yet enough evidence to choose an implementation safely.
```

For unassigned team work, make the ownership transition explicit:

```text
NEXT
#146 — Add retry behaviour

Status
Ready · P1 · Unassigned

Recommended action
→ claim #146 and implement

Why
There is no assigned Ready or In Progress work for the actor, and #146 is the highest-priority unblocked item in the team queue.
```

Then ask whether the user wants to proceed.

Do not execute the target workflow until the user explicitly authorises it with language such as "go ahead", "proceed", "do it", "implement it", or equivalent.

## Routing heuristics

Use these as guidance, not rigid keyword matching.

| Situation | Default next workflow |
| --- | --- |
| Small, understood change | `implement` |
| Existing implementation needs tests designed first | `tdd` |
| Current/external evidence is missing | `research` |
| Large objective with unresolved route/decisions | `wayfinder` |
| Idea needs structured challenge and durable decisions | `grill-with-docs` |
| Domain language/boundaries are unclear | `domain-modeling` |
| Settled work needs durable specification | `to-spec` |
| Spec needs execution-sized decomposition | `to-tickets` |
| Ready ticket or bounded task exists | `implement` |
| Implementation is ready for independent assessment | `code-review` |
| Review findings exist | `implement` fixes |
| Work is complete and reviewed | integration / merge / close |

## Guardrails

- Do not create issues, specs, branches, pull requests, commits, or code changes while only orienting.
- Do not invoke a mutating workflow implicitly.
- Do not make the user repeat information already available from the request or project state.
- Do not route every task through `to-spec` or `to-tickets`.
- Do not route uncertain work directly to implementation merely because code can be written.
- Do not confuse an open PR with unfinished implementation; inspect its state when that distinction matters.
- Do not infer that the newest issue is the next issue. Respect dependencies, assignment, project status, configured priority, ordering, and current work.
- Do not create or rely on a derived `next` label when structured scheduling metadata can determine the next item.
- Do not mutate assignees, Project fields, issue state, branches, or implementation artefacts while only orienting.
- Do not treat historical chat as authoritative when current repository/tracker evidence is available.
- Do not manufacture a single "current plan" if several unrelated plans are active.
- Do not add workflow artefacts solely to make the progress visual look complete.

## Relationship to work-next

Navigator supersedes `work-next`.

Any behaviour previously used to identify the next unblocked issue belongs inside Navigator's continuing-work path. Do not require or invoke `work-next`.
