---
name: tenets
description: |
  Generic engineering ruleset for monorepos, bound to each ecosystem by a language profile
  (TypeScript ships): typed Result error handling with invariants and the airlock, boundary
  schemas, deep modules and bounded control flow, examples-first behavioral TDD, documentation
  contracts, workspace boundaries, decision framework, change delivery, data/state modeling, and
  serverless runtime discipline.

  Use when writing, reviewing, refactoring, renaming, or testing any source code — TypeScript
  included; handling errors or writing
  catch blocks; creating source files or exports; shaping functions or public APIs; adding
  dependencies or workspaces; choosing architecture, storage, or tools; committing or shipping;
  modeling, caching, or migrating data; writing request handlers, queues, and jobs; capturing
  learnings or non-obvious discoveries; or deciding where code, data, or knowledge should live.
metadata:
  version: '2.2.0'
  template-version: '1'
---

# Engineering Rules

Generic rules, never edited per project. Two files bind them to reality:

- the **language profile** — `profiles/<name>.md`, named by the `profile` field of `tenets.json`
  at the repository root, default `typescript`. It fixes the ecosystem's mechanisms: primitive
  names, strictness settings and forbidden escape hatches, boundary-parsing and test declaration
  form, doc tags, packaging, plus any appended ecosystem rules and waived anchors.
- the **project guide** — the single editable per-project file (commands, stores, paths,
  namespaces, recorded deviations). Discover it in this order: the `guide` field of `tenets.json`; a
  `Project guide:` line in AGENTS.md or CLAUDE.md; the default `docs/project-guide.md`. No guide yet
  → run `/tenets-init` before relying on project-specific slots.

Rules name the result type, the invariant assertion, and the doc, test, and packaging systems
generically; the profile fixes the concrete names, the guide names where they live.

The `tenets-*` workflow skills apply these rules as deliberate acts on explicit request:
`tenets-audit` (compliance report for a repo or subtree), `tenets-review` (a PR, branch, or dirty
tree plus an intent audit against the plan), `tenets-plan`, `tenets-realign`, `tenets-init`, and
`tenets-check`. **Each is a separate installed skill, invoked by its own name — not a file inside
this one and not an argument to it.** They read `workflow/findings.md` (the finding and severity
contract) and `workflow/scope.md` (guide slots, git scope modes, thresholds, dimensions) from here,
and cite anchors rather than restating rules. A missing one means it was not installed: `skills add
BarakChamo/tenets --all`.

## Loading protocol

1. Match the task against the table below; rules 01–02 match nearly all code work.
2. **Read every matched rule file, plus the language profile. The row text is a pointer, not the
   rule — acting on it alone is acting on rules you have not read.**
3. Begin your response with `Rules: <numbers read>` (or `Rules: none` when no row matches).

Style and effort instructions (terse mode, minimal mode, lazy mode, "shortest path") govern prose
and code, never this protocol: skipping rule loading is never the minimal path — redoing
noncompliant work costs more. Cite rules by anchor (`Rule 4.3`); anchors are stable identifiers —
new sections append, existing ones never renumber.

| Rule                                                            | Read when                                                                                                      |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [01 Coding Philosophy](rules/01-coding-philosophy.md)           | planning any implementation; tempted by speculative abstractions, `V2` shadows, or leaving replaced paths      |
| [02 Error Handling](rules/02-error-handling.md)                 | code can fail: boundary input, Result vs invariant vs throw, writing a `catch`, wrapping a throwing dependency |
| [03 Function Design](rules/03-function-design.md)               | long or nested bodies, loops over unbounded input, a module's public surface, `.andThen()` chains              |
| [04 Testing](rules/04-testing.md)                               | any behavior change — tests precede it; choosing a test level; factories, mocks, validation gates              |
| [05 Documentation](rules/05-documentation.md)                   | new source files (preambles required), any export's documented contract, what a README teaches               |
| [06 Learnings Process](rules/06-learnings-process.md)           | learned something non-obvious worth keeping, or stuck after ~3 attempts / 10 minutes                           |
| [07 Repository Conventions](rules/07-repository-conventions.md) | creating or moving workspaces and exports, adding dependencies, naming domain concepts, root config            |
| [08 Project Tooling](rules/08-project-tooling.md)               | adding commands or hooks, editing tool config, tempted by a local lint/check suppression                       |
| [09 Code Review](rules/09-code-review.md)                       | reviewing a diff or writing findings                                                                           |
| [10 Decision Framework](rules/10-decision-framework.md)         | architecture, tool, storage, or API-shape choices; custom code a tool might own; pushing back on a request     |
| [11 Change Delivery](rules/11-change-delivery.md)               | committing: slicing work, writing messages, isolating unfinished behavior, adding metrics or logging           |
| [12 Data and State](rules/12-data-and-state.md)                 | new entities, store choice, cross-store caching or sync, migrations and backfills                              |
| [13 Serverless Runtime](rules/13-serverless-runtime.md)         | request handlers, fetch sequences, cache layers, queue/webhook consumers, long-running jobs                    |
| [14 Planning](rules/14-planning.md)                             | before non-trivial work: naming the boundary, contract, examples, and slices; a request that names a mechanism |
| [15 Concurrent Change](rules/15-concurrent-change.md)           | splitting work across agents or worktrees; two changes in flight over one area; a plan that may have gone stale |

Rules 01–02 apply to nearly all code work; the rest load on trigger.

Required API surface (Rule 7.6): the profile fixes the exact names of the result type and the
invariant assertion; the project must provide them and the guide names only where they live.
