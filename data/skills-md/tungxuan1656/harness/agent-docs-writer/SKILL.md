---
name: agent-docs-writer
description: >-
  Write, rewrite, or maintain concise agent-facing repository
  documentation. Use for AGENTS.md, architecture and subsystem guides, product
  or domain specs, task and handoff records, implementation plans, durable
  decisions, or a bounded repair of known stale documents. Use only when each
  document's canonical responsibility and location are known. Do not use to
  redesign documentation ownership or hierarchy.
---

# Agent Docs Writer

Write the smallest document that supports correct action.

## Output contract

Every document must be:

- **Scoped**: own one class of truth.
- **Routed**: link to deeper canonical sources.
- **Explicit**: state rules, boundaries, and exceptions directly.
- **Structured**: prefer short sections, lists, tables, maps, and flows.
- **Evidence-based**: use repository facts; label uncertainty.
- **Concise**: remove text that does not help the reader locate, relate, constrain, decide, verify, or navigate.

Do not add generic introductions, tutorials, duplicated rules, or low-value history.
Do not add abstractions, options, dependencies, or plan phases without a concrete need.
Prefer the smallest complete solution using existing patterns. Preserve required
security, data-integrity, accessibility, and recovery constraints.

## Workflow

1. Inspect the relevant code, configuration, existing documents, and commands.
2. Choose the document type and its canonical responsibility.
3. Read the template linked in the document ownership table.
4. Draft the minimum sections from that template.
5. Put the map, flow, state, or rule before its explanation.
6. Link to canonical truth instead of copying it.
7. Apply the language rules below.
8. Run the quality gate. Delete low-value text before delivery.

For read-only consistency, drift, or complexity assessment, use
`agent-docs-checker` when available. This writer implements bounded repairs;
it does not choose architecture or resolve missing product decisions.

Do not invent architecture, commands, product rules, or intended design. If evidence conflicts, label `Observed`, `Intended`, `Proposed`, or `Uncertain`.

For a rewrite, preserve repository facts and required behavior. Remove generic policy that conflicts with this guide. Do not impose commit, branch, review, tool, or release rules without repository evidence or user instruction.

## Maintenance mode

Use this mode for a bounded docs-only repair when the selected files and their
canonical owners are already known.

1. State the selected files, the source each must agree with, and the repair
   boundary.
2. Classify each issue as stale, duplicate, broken-route, or unverified.
3. Update the canonical document first, then repair links or remove only
   duplicate text that has a clear canonical replacement.
4. Preserve repository-native names, paths, and generated sources.
5. Verify affected routes and commands. Report unresolved conflicts instead of
   choosing a new owner.

Do not use `repo-gardening` merely because prose is stale. If ownership,
location, or the document graph is unclear, stop the repair. Hand the case to
`agent-docs-architect` when it is installed; otherwise return the unresolved
ownership question without redesigning the system.

## Document ownership

| Document | Owns | Template |
|---|---|---|
| `AGENTS.md` | Repository navigation and repository-wide operating rules | [Entry documents](references/entry-documents.md) |
| `ARCHITECTURE.md` | System topology, code map, boundaries, and major flows | [Entry documents](references/entry-documents.md) |
| Subsystem guide | Patterns, boundaries, examples, and verification for one subsystem | [System documents](references/system-documents.md) |
| Product or domain spec | Durable behavior, states, rules, and edge cases | [System documents](references/system-documents.md) |
| Task or handoff record | Bounded scope, acceptance, task-local state, evidence, and next action | [Work documents](references/work-documents.md) |
| Execution plan | Necessary sequencing, verification, coordination, and recovery | [Work documents](references/work-documents.md) |
| Decision record | Rationale for one durable decision | [Decision document](references/decision-document.md) |

Do not let two documents own the same fact. Choose one source and link to it.

Keep durable facts separate from work state. Do not put active tasks, branch names, or session notes in architecture documents.

## Default style

Follow the compact style used by effective operating guides:

- Use short, descriptive headings.
- Start an instruction with a verb.
- Put one rule or action in each bullet.
- Split a list item when it contains several actions or conditions.
- Put a condition before its instruction.
- State the rule before the reason.
- Use one term for one concept.
- Use exact paths, symbols, and commands.
- Keep paragraphs to one topic and no more than three sentences.
- Use a shallow map instead of a directory dump.
- Use an example only when it changes a decision.

Use `MUST` only for a non-negotiable invariant. Use `CAN` for an option or capability. Avoid `should`, `may`, `might`, and `could` when they make a rule optional or ambiguous.

### Simple English pass

Use pragmatic Simplified Technical English for the final pass:

- Procedures: use the imperative and one action per sentence.
- Descriptions: use active voice and one fact per sentence.
- Put `if` and `when` conditions before the action.
- Use 20 words or fewer for an instruction.
- Use 25 words or fewer for a descriptive sentence.
- Remove filler, hedges, synonym rotation, and unmeasured adjectives.
- Preserve code, identifiers, commands, paths, configuration keys, and quoted errors exactly.

Use clear, direct language. Preserve identifiers, commands, quoted errors,
and technical meaning; do not impose controlled aerospace vocabulary.

## Information form

Use the form with the highest useful information density:

- **Map** for location and ownership.
- **Flow** for ordered interactions.
- **Dependency edges** for allowed and forbidden access.
- **Decision tree** for conditional choices.
- **State transition** for lifecycle behavior.
- **Table** for cases, ownership, or trade-offs.
- **Bullets** for independent invariants.

Do not add a diagram when a short list is clearer. See [information patterns](references/information-patterns.md) for notation and examples.

## Size limits

Treat these as default limits, not writing targets:

| Document | Default limit |
|---|---:|
| Task document | 300 words |
| Handoff block | 150 words |
| Decision record | 500 words |

Exceed a limit only when the extra text prevents a concrete error and cannot move to a canonical linked document.

For architecture and subsystem guides, split the document when it contains more than one class of truth. Do not split only to satisfy a word count.

## Quality gate

Before delivery, make sure that:

- The title and first section reveal the document's responsibility.
- A fresh agent can find the relevant code or deeper source.
- Important relationships and forbidden edges are visible.
- Rules and exceptions are explicit.
- Commands and paths are exact.
- Repository policy comes from evidence or user instruction.
- Temporary state is outside durable documents.
- No fact has two canonical owners.
- Each section supports action or navigation.
- Specs state observable behavior, boundaries, edge cases, and acceptance.
- Plans cover acceptance without speculative abstractions or duplicated future code.
- Proposed choices and unresolved decisions are not written as accepted truth.
- The Simple English pass is complete.
- The document stays within its default size limit, or the reason is clear.

For a rewrite or multi-document review, use the full [review checklist](references/review-checklist.md).

## References

- [Entry documents](references/entry-documents.md): read for `AGENTS.md` or `ARCHITECTURE.md`.
- [System documents](references/system-documents.md): read for subsystem guides or product and domain specs.
- [Work documents](references/work-documents.md): read for tasks, plans, or handoff records.
- [Decision document](references/decision-document.md): read for durable decision records.
- [Information patterns](references/information-patterns.md): read when relationships, states, evidence conflicts, or diagrams need clarification.
- [Review checklist](references/review-checklist.md): read for audits, rewrites, or final multi-file review.
