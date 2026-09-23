---
name: just-enough-engineering
description: >-
  Reduce accidental complexity and cognitive load while preserving required
  behavior, safety, and quality. Use when writing, reviewing, refactoring, or
  explaining code, documentation, repository research, architectures,
  integrations, MCP servers, agent graphs, loops, workflows, and technical
  plans that risk becoming redundant, over-engineered, repetitive, or hard to
  navigate. Also use when the user asks to simplify, make something concise,
  remove boilerplate, avoid unnecessary abstractions, or find the smallest
  sufficient solution. Do not use to remove essential complexity or explicit
  requirements merely to make an artifact shorter.
metadata:
  summary: >-
    Choose the smallest sufficient solution across code, documentation,
    integrations, and agent workflows without sacrificing essential quality.
---

# Just Enough Engineering

Just Enough Engineering helps AI coding agents build and explain software with
only the complexity each task requires. It applies to code, documentation,
repository research, integrations, architecture, and agent workflows, keeping
the result clear and maintainable while preserving behavior, safety, and quality.

## Core standard

Every component must earn its cost. A file, abstraction, dependency, service,
tool, integration, workflow step, diagram, or documentation section earns its
place only when it satisfies a current requirement more clearly or safely than
a simpler option.

Preserve essential complexity. Security boundaries, error handling,
accessibility, compatibility, observability, data integrity, and explicit user
requirements are not clutter. Remove accidental complexity around them.

When the user explicitly requests a particular architecture or deliverable,
respect it. Simplify within that boundary and mention a materially leaner
alternative only when it helps the decision.

## Working method

1. State the outcome in one sentence. Identify the user-visible behavior,
   decision, or question that must be resolved.
2. Read the local rules and the smallest relevant slice of the project. Reuse
   existing conventions before inventing new ones.
3. Separate non-negotiable constraints from assumptions and speculative future
   needs. Ask only when an unresolved choice would materially change the result.
4. Inventory the proposed moving parts and their costs: concepts, files,
   dependencies, configuration, external calls, failure modes, maintenance, and
   explanation burden.
5. Choose the lowest-complexity option that meets the current constraints.
6. Implement or explain it directly. Keep related logic and information
   together until a real boundary justifies separation.
7. Validate the promised behavior in proportion to risk. Stop when the outcome
   and relevant checks are satisfied; do not add polish passes without a
   concrete defect.
8. Report the outcome first, then verification and any meaningful caveat. Do
   not produce a process diary unless requested.

## Decision ladder

Prefer options in this order, moving down only with evidence:

1. Remove the unnecessary work or concept.
2. Use the platform, language, or repository as it already exists.
3. Write the direct local solution.
4. Extract a small helper when it clarifies a stable responsibility or removes
   meaningful duplication.
5. Add a reusable abstraction when multiple real consumers share the same
   concept and are likely to evolve together.
6. Add a dependency, service, MCP, graph, or framework only when its capability
   outweighs setup, context, failure, security, and maintenance costs.

Do not build extension points for hypothetical consumers. Prefer a reversible
local choice over a generalized system designed from guesses.

## Apply by artifact

### Code and refactors

- Preserve behavior unless the user asked to change it.
- Delete dead code, redundant branches, pass-through layers, duplicated state,
  and comments that merely narrate syntax.
- Flatten control flow and make names reveal intent.
- Prefer readable, explicit code over dense tricks or compressed one-liners.
- Do not split code solely to make functions or files smaller. Extract around a
  coherent responsibility or an independently changing boundary.
- Avoid wrappers, factories, registries, configuration knobs, generic helpers,
  and new dependencies without a current use that simpler code cannot serve.
- Test externally meaningful behavior. Avoid tests coupled only to incidental
  implementation details.
- Keep the change scoped. Do not turn a local task into a repository-wide
  rewrite unless the broader change is necessary for correctness.

### Documentation and explanations

- Lead with what the reader needs to know or do.
- Give one canonical path first. Put optional detail after it through headings,
  links, or examples.
- Explain decisions, constraints, surprising behavior, and failure recovery;
  omit obvious narration and repeated summaries.
- Prefer one maintained source of truth over parallel documents that drift.
- Use a diagram only when relationships are harder to understand in prose or a
  small table.
- Match depth to the audience and task. Concise means high signal, not missing
  prerequisites.

### Repository exploration and research

- Begin with the user's question, not a tour of the repository.
- Trace only the entry points, dependencies, and evidence needed to answer it.
- Distinguish verified facts from inference.
- Present the conclusion before supporting details. Cite exact files, symbols,
  commands, or sources rather than dumping raw discovery logs.
- Stop searching when additional evidence is unlikely to change the answer.

### Integrations and MCPs

- Treat every external boundary as a recurring cost: authentication,
  configuration, permissions, versioning, latency, errors, security, and
  operations.
- Prefer an existing connector, native capability, direct API call, or small
  adapter before creating another service or MCP server.
- Expose the smallest useful tool surface with clear inputs and outputs.
- Avoid proxy tools that merely rename another API without adding validation,
  policy, composition, or a meaningful usability improvement.
- Add retries, caching, queues, webhooks, or synchronization only for observed
  reliability or scale requirements, with explicit limits and failure behavior.

### Agent graphs, loops, and workflows

- Start with one linear path.
- Add a branch only for a real decision with meaningfully different handling.
- Add parallel work only for independent tasks whose coordination cost is
  lower than the time or quality gained.
- Add a loop only when there is a measurable improvement signal, a termination
  condition, and a bounded iteration or resource budget.
- Avoid multiple agents when one agent with the right context can complete the
  task reliably.
- Keep state explicit and minimal. Do not persist intermediate artifacts unless
  they are needed for recovery, audit, handoff, or reuse.
- Prefer deterministic checks over extra critique or planning stages.

### Plans and architecture

- Design for current requirements and the nearest credible change.
- Use concrete modules and data flow before patterns or platform layers.
- Record important tradeoffs without manufacturing a formal document for every
  decision.
- Separate components when ownership, deployment, security, scaling, or change
  cadence genuinely differs—not merely because separation is possible.
- Identify what can be deferred. A smaller decision made with evidence is often
  safer than a large speculative design.

## Simplification tests

Before keeping any non-trivial element, ask:

- What current requirement does it satisfy?
- What breaks if it is removed or inlined?
- Does an existing component already do this?
- Is the abstraction clearer at both its definition and call sites?
- Does it reduce total concepts, or only move complexity elsewhere?
- Is its operational and documentation cost proportionate to its value?
- Can a future change add it safely when evidence appears?

If the answers are weak, remove or defer it.

## Guardrails against false simplicity

Do not:

- hide behavior to reduce visible code;
- collapse distinct domain concepts into vague generic utilities;
- remove validation, useful errors, security controls, accessibility, or
  required observability;
- trade maintainability for novelty or brevity;
- centralize unrelated logic merely to eliminate similar-looking lines;
- claim an architecture is simple while shifting burden to operators or users;
- repeat recommendations, conclusions, or documentation in multiple forms.

The goal is lower total burden across readers, maintainers, operators, and
users—not a locally smaller artifact.

## Completion format

Keep the final response proportional to the task. Usually include only:

1. the outcome;
2. the material change or decision;
3. the validation performed;
4. a remaining risk or next step only when it matters.

Do not add sections, files, diagrams, abstractions, integrations, or follow-up
work merely to make the result appear comprehensive.
