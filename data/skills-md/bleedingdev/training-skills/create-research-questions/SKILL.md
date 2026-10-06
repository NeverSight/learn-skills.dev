---
name: create-research-questions
description: Create a current-state research query plan from a task.
disable-model-invocation: true
---

# Create Research Questions

Create a **query plan** for a later research session. The artifact describes what the codebase and its dependencies do today; it does not design the requested change or answer the questions.

## 1. Establish the source boundary

Read every file the user explicitly names or `@`-mentions, in full, before exploring anything else. This includes a named `ticket.md`, `task.md`, or collateral document. Treat the user's request and those files as the task brief. Leave other task artifacts unopened unless the user explicitly includes them.

While reading, build a private pointer ledger containing every exact:

- URL or document/issue reference;
- repository name or path;
- library, dependency, package, or version;
- file or directory path.

Preserve pointer text verbatim. Also identify the requested outcome privately so it can guide scope without appearing as a proposed implementation in the question list.

**Complete when:** every explicitly supplied source has been read from beginning to end, every concrete pointer from those sources is present once in the ledger, and the task's research boundary can be stated without guessing.

## 2. Run reconnaissance, not the research phase

Collect only enough evidence to turn the brief into grounded questions. Keep the reconnaissance read-only.

### Repository evidence branch

When the task touches the current repository, inspect it with the available repository tools or delegate bounded read-only work to these specialist agents when present:

- `codebase-locator` — locate relevant source, configuration, migration, documentation, and test surfaces;
- `codebase-analyzer` — trace a current flow, contract, or component interaction that is needed to frame a question;
- `codebase-pattern-finder` — locate comparable implementations and the conventions they expose.

Use agents concurrently only for independent surfaces. Give each agent a narrow current-state query and require paths plus line references. Treat their findings as reconnaissance leads, not as the final research report. Stop once the major boundaries and likely evidence locations are known.

### External evidence branch

Use `web-search-researcher` or the available web tools when the brief contains an external URL, repository, SDK, library, protocol, hosted service, or version-sensitive capability whose documentation affects the query plan. Prefer official, current sources and retain direct URLs. Skip this branch for a wholly internal task whose questions can be anchored in repository evidence.

Add newly discovered high-signal paths, packages, repositories, and URLs to the pointer ledger. Mark discovered pointers separately from user-supplied pointers so only verbatim supplied pointers are guaranteed provenance.

**Complete when:** every in-scope system boundary has at least one evidence lead, each repository lead has a path (and line when available), each external lead has a direct authoritative URL, and no further exploration is required merely to phrase the questions precisely.

## 3. Build a coverage map

Map the task to the current-state dimensions that a researcher must explain. Consider each dimension and retain it only when material:

- entry points and end-to-end control or data flow;
- ownership, module boundaries, and component/service interactions;
- interfaces, schemas, storage, events, and cross-repository contracts;
- configuration, feature flags, runtime or deployment behavior;
- error paths, edge cases, lifecycle, concurrency, and state transitions;
- existing analogous patterns and their tests;
- test coverage, fixtures, mocks, and verification conventions;
- dependency or platform behavior documented outside the repository.

For frontend or visual work, always reserve coverage for the relevant design system: component library, color values, typography, spacing, borders, shadows, tokens, themes, and existing product-area composition patterns. This design-system question may be broader than the named screen or component.

Merge dimensions answered by the same evidence trail. Split dimensions whose answers require different systems or sources.

**Complete when:** every material dimension appears exactly once in the map, every map item names an evidence lead or pointer, and the map has no duplicate or orphaned item.

## 4. Turn the map into descriptive questions

Write a prioritized set of questions for the next agent. Default to 2–7 questions; exceed seven only for an unusually broad task or an explicit user request.

Each question must:

- ask what exists, where it exists, how it works, or how current parts interact;
- name the relevant scope and, when known, an evidence starting point;
- be broad enough to produce a coherent explanation but bounded enough to know when it is answered;
- cover current tests and edge behavior with the component they belong to;
- direct dependency questions to the exact library, version, repository, or official documentation when known.

Use neutral formulations such as “How does…?”, “Trace…”, “Explain…”, “Where is…?”, and “What contract…?”. Translate the requested future change into its surrounding current-state behavior. A proposed solution, desired architecture, improvement, root-cause theory, or implementation instruction is outside this query plan unless the user explicitly asks for that additional mode.

**Complete when:** every coverage-map item is owned by at least one question, every question has a recognizable answer boundary and evidence strategy, and the set contains no redundant question.

## 5. Run the current-state gate

Audit every question independently:

1. Could it be answered by documenting the system as it exists now?
2. Does it avoid revealing or endorsing the requested implementation?
3. Does it avoid asking what should change, what should be built, or which option is better?
4. Does it point the researcher toward concrete repository or authoritative external evidence?
5. Does it contribute unique coverage at the task's actual scale?

Rewrite or remove every question that fails any check. Confirm that frontend scope includes the design-system coverage from step 3.

**Complete when:** every retained question passes all five checks, the count is justified by task breadth, and all high-impact unknowns from the coverage map remain represented.

## 6. Write the artifact

Read [`references/research_questions_template.md`](references/research_questions_template.md) in full before writing.

Resolve the destination as follows:

1. Use the task artifact directory supplied by the environment when available.
2. Otherwise enumerate `.agent-work/tasks` while following symlinks and reuse the single directory matching the ticket identifier or task slug.
3. If no matching directory exists, create `.agent-work/tasks/<TICKET-ID>-<task-slug>/` when a ticket exists, or `.agent-work/tasks/<task-slug>/` otherwise.
4. If multiple directories plausibly match and the sources do not disambiguate them, ask the user which one owns the artifact before writing.
5. Inspect every filename in the chosen directory, take the highest leading two-digit `NN-` index, and increment it. Use `01` when none exists.
6. Write `NN-research-questions-DESCRIPTION.md`, where `DESCRIPTION` is a specific 2–4 word kebab-case slug.

For example, a ticket-backed first artifact may be `.agent-work/tasks/ENG-1478-parent-child-tracking/01-research-questions-parent-child-tracking.md`; a request without a ticket may use `.agent-work/tasks/authentication-flow/01-research-questions-auth-flow.md`.

Populate the template without placeholders. Include `Key Context Pointers` only when the ledger is non-empty. Preserve user-supplied pointer spelling exactly; label additional reconnaissance pointers clearly rather than presenting them as user-supplied. If the host returns a permalink for the written artifact, capture it; otherwise use the local artifact path as the navigation target.

**Complete when:** exactly one new artifact exists at the resolved path, its index is the next chronological index, its frontmatter is valid, every numbered entry passed the current-state gate, every pointer is categorized with correct provenance, and no template placeholder remains.

## 7. Hand off to research

Read [`references/research_questions_final_answer.md`](references/research_questions_final_answer.md) in full after the artifact is written. Render it exactly once, substituting the local artifact path and adding a host permalink only when one was actually returned. Keep `$create-research` as the next command; the user is not expected to answer the questions.

**Complete when:** the response identifies the local artifact path, explains that the next agent will answer it, contains `$create-research`, includes only a real optional host permalink, and contains no invented link or extra summary.
