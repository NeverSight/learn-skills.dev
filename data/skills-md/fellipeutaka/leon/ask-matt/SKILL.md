---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask Matt

You don't remember every skill, so ask.

A **flow** is a path through the skills. Most paths run along one **main flow**,
and two **on-ramps** merge onto it. Everything else is standalone, or a
vocabulary layer that runs underneath. Delivery tooling, including stacked PRs,
sits underneath the main flow rather than replacing it.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`/grill-with-docs`** sharpens the idea by interview. Start here whenever
   you are **working in a working directory**: it's stateful, retaining what it
   learns in `CONTEXT.md` and ADRs. (No working directory? Use `/grill-me`
   instead, covered under Standalone. Both run the same `/grilling` primitive;
   `grill-with-docs` is the one that leaves a paper trail.)
2. **Branch: can you settle every question in conversation?** If a question
   needs a runnable answer (state, business logic, a UI you have to see), detour
   through a prototype, bridged by `/handoff` in both directions:
   - `/handoff` out, then open a fresh session against that file;
   - `/prototype` to answer the question with throwaway code;
   - `/handoff` back what you learned, and reference it from the original idea
     thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → `/to-spec` (turn the thread into a spec), then `/to-tickets` to
     split it into tracer-bullet tickets, each declaring its **blocking edges**.
     On a local tracker that's one file per ticket under
     `.scratch/<feature>/issues/`, worked blockers-first by hand; on a real
     tracker the edges become native blocking links, so any ticket whose
     blockers are done can be grabbed: kick off `/implement` per ticket,
     clearing context between each one. Each ticket is self-contained, so the
     last one's context is disposable.
   - **No** → `/implement` right here, in the same context window.

   `/implement` is the user-invoked **orchestrator**. For non-trivial tickets it
   dispatches one isolated implementer subagent, which drives TDD at the agreed
   seams; the orchestrator then calls the Skill tool with "code-review" against
   the fixed point before delivery. Reach for `/tdd` on its own when you just
   want to build a concrete behaviour test-first without a full spec, and
   `/code-review` on its own whenever you want to review a branch or PR against
   a fixed point.

## Delivery topology

After `/to-tickets` has produced and the user has approved the real blocker
graph, choose the PR delivery topology:

- **Linear dependency chain** → invoke `/implement` in stacked mode and use the
  `gh-stack` skill for branch and PR operations.
- **Fork or join with one final merge into trunk** → invoke `/implement` in
  integration mode. Create one durable integration branch and target parallel
  ticket PRs at it; the final integration PR targets trunk and closes the
  spec/PRD.
- **Fork or join without a final integration PR** → ask whether to serialize the
  work into one linear stack or preserve parallelism with independent/dependent
  PRs. `gh-stack` supports only one parent and one child per stack.
- **Existing PR or branch** → adopt compatible existing state with
  `gh stack init <branch>` or use `gh stack link` only when branches are already
  managed by an external tool. Never recreate an existing PR just to introduce
  a stack.

The issue dependency graph remains the source of truth. A stack ordering is a
delivery decision and must not silently rewrite a ticket's `Blocked by` edges.

When the user asks for parallel worktrees and a single final PRD merge, the
integration branch is the default delivery topology. Child PRs target the
integration branch and use `Refs #<ticket>`; only the final PR targets trunk and
uses `Closes #<spec>`.

When using a stack, each fresh `/implement` context must run
`gh stack view --json` and verify the current parent before coding. When using
integration delivery, each fresh context must verify the integration branch and
that all ticket blockers are merged into it. The branch state is durable;
conversation context is not.

## Context hygiene

Keep steps 1–3 in **one unbroken context window** (don't compact or clear until
after `/to-tickets`) so the grilling, spec, and tickets all build on the same
thinking. Each `/implement` then starts fresh, working from the ticket and the
durable repository/issue state.

The limit on this is the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**:
the window (~150k tokens on state-of-the-art models) within which the model
still reasons sharply. If a session approaches it before `/to-tickets`, don't
push on degraded: compact at the nearest phase boundary and carry on.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → `/triage`. It moves issues through triage
  roles and produces agent-ready issues, which `/implement` later picks up.

  Triage is only for issues **you didn't create**: bug reports, incoming
  feature requests, anything that arrives raw. Tickets that `/to-tickets`
  produced are already agent-ready, so don't triage them.

- **Something's broken** → `/diagnosing-bugs`. For the hard ones: the bug that
  resists a first glance, the intermittent flake, the regression that crept in
  between two known-good states. It refuses to theorise until it has a **tight
  feedback loop** (one command that already goes red on *this* bug), then fixes
  with a regression test.

- **A huge, foggy effort: a greenfield project or a huge feature build, too big
  for one session** → `/wayfinder`, the most cognitively demanding flow here.
  When the way from here to the destination isn't visible yet, it charts a
  **shared map** of **decision tickets** on the issue tracker and resolves them
  one at a time, producing **decisions, not deliverables**, until the fog is
  pushed back and the way is clear. Where `/grill-with-docs` sharpens an idea
  you can hold in one session, wayfinder is for the idea you can't, and it's
  slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, it hands off, it doesn't build: merge onto the main flow
  at `/to-spec`, which collapses the map's linked decisions into a buildable
  plan, then `/to-tickets` and `/implement` as usual. Looping the map straight
  into `/implement` skips that collapse and throws the linked detail away, so go
  straight to `/implement` only when the effort turned out genuinely small.

## Codebase health

Not feature work, just upkeep.

- `/improve-codebase-architecture` runs whenever you have a spare moment to keep
  the codebase good for agents to operate in. It surfaces **deepening
  opportunities**; picking one _generates an idea_ you can take into the main
  flow at `/grill-with-docs`. It's the survey that finds the candidates;
  `/codebase-design` is the bench you design the chosen one on.

## Vocabulary underneath

Two model-invoked references that run **beneath** the other skills, each the
single source of truth for its vocabulary. Reach for them directly when the
**words**, not the process, are the problem; or let the skills above pull them
in.

- `/domain-modeling` sharpens the project's *domain* language: challenge a
  fuzzy term, resolve an overloaded word ("account" doing three jobs), and
  record a hard-to-reverse decision as an ADR. It's the active discipline
  `/grill-with-docs` drives to keep `CONTEXT.md` a clean glossary.
- `/codebase-design` is the deep-module vocabulary (module, interface, depth,
  seam, adapter, leverage, locality) for designing a module's *shape*: a lot of
  behaviour behind a small interface at a clean seam. `/tdd` and
  `/improve-codebase-architecture` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the
implementation, the QA. At the **boundary** between two of them you have five
options, and picking between them is the fuzziest decision in this whole map.

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window when nothing here matters to what's next.
- **`/handoff`**: write a portable markdown file for a new harness, directory,
  colleague, or side task.
- **Subagent**: send a tightly scoped task to its own window and get a report
  back.
- **`/compact`**: compress this context and seed a fresh session. It is the
  default at the bottom of the tree, not the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree. Make the
decision at the boundary; mid-phase, continue or split the remaining work into
subagents.

## Standalone

Off the main flow entirely.

- `/grill-me` is the same relentless interview as `/grill-with-docs`, but
  **stateless**: it saves nothing locally and builds no `CONTEXT.md`. Reach for
  it when you are not working in a working directory.
- `/grilling` is the interview primitive itself: rounds, the frontier, facts are
  the agent's job and decisions are yours. Reach for it directly only when you
  want the interview with no wrapper around it.
- `/resolving-merge-conflicts` works an in-progress merge or rebase conflict
  hunk by hunk, resolving by **intent** traced to each side's primary source.
- `/prototype` is a small, throwaway program that answers one design question.
  Its answer folds into the real code; keep the prototype as a primary source
  when the implementation issue points to it.
- `/research` delegates reading legwork to a **background agent** and leaves a
  cited Markdown file in the repo. Research feeds the main flow; it does not
  replace it.
- `/to-questionnaire` writes a questionnaire when the missing information is in
  someone else's head rather than yours or the codebase.
- `/wizard` covers steps only a human can perform, such as provisioning,
  credentials, or a one-off cutover.
- `/wait-what` re-pitches a message that did not land, using the project's
  vocabulary.
- `/teach` supports learning a concept over multiple sessions in the current
  directory.
- `/writing-for-agents` is the reference for writing documents agents consume:
  skills, `AGENTS.md`, and pointed-at docs.

## Precondition

`/setup-matt-pocock-skills` runs before the first engineering flow to configure
the issue tracker, triage labels, and doc layout the other skills assume. Custom
issue trackers also work.
