---
name: architecture-review
description: General-purpose architecture review for any code repository. Use when Codex needs to assess concept ownership, authoritative sources, module boundaries, architecture decisions, architecture drift, duplicated concepts, scattered rules, hidden assumptions, over-engineering, architectural change surface, phased refactor planning, or how architecture exposes ownership and change boundaries to future coding agents. Do not use for ordinary code review, testing review, implementation review, framework review, style review, narrow bug diagnosis, or a standalone agent-legibility audit unless the user explicitly asks for architecture assessment.
---

# Architecture Review

Review repository architecture from local evidence. The goal is to identify what concepts exist, who owns them, where authority lives, which boundaries matter, where responsibilities are unclear, and what small architectural improvement would reduce future change cost.

Do not modify code during review unless the user explicitly asks for implementation. If the user asks for both review and changes, complete the architecture review first, then make only the agreed or clearly requested changes.

Examples:

- [notification preferences boundary review](examples/notification-preferences-boundary.md)
- [repository layout ownership review](examples/repository-layout-ownership.md)

## Scope

Architecture review is about ownership, authority, boundaries, concept consistency, architecture decisions, drift, and change surface.

It is not:

- code review focused on bugs, style, or local implementation quality
- testing review focused on coverage strategy or test design
- language or framework review focused on idioms, performance, or ecosystem practices
- general maintainability review unless the issue changes ownership, authority, boundaries, or concept lifecycle
- agent-legibility review focused on making future agent tasks easier outside an architectural concern

## Core Principles

- One concept should have one authoritative location.
- Important concepts need both a clear owner and a canonical source.
- A module should have one primary reason to change.
- Boundaries should preserve meaning, not only separate files.
- Rules should live with the concept owner or be explicitly delegated.
- Architecture decisions should remain traceable from rationale to implementation.
- Drift matters when implementation no longer follows the repository's stated or implied architecture.
- Change surface is architectural when one concept change requires many unrelated modules to change.
- Do not recommend abstraction unless it reduces real duplication, clarifies ownership, or narrows a boundary.
- Match review-document structure to review complexity. A small, bounded review may be best kept in one concise document; multiple files are not a requirement by themselves.
- Split a large review only when independent owners, lifecycles, decision axes, or validation boundaries make separate documents materially easier to find, maintain, or update.
- For a genuinely cross-cutting review, use a small entry document for navigation and frozen cross-module points, with one cohesive document per meaningful module. Do not turn the entry document into a duplicate of every module.
- Do not split documents merely because a file is long, and do not merge independent modules merely to keep a single-file convention. The boundary must reduce ambiguity or change surface.
- Do not repeatedly report intentional architecture debt as a new defect; record its rationale and retirement condition.
- Prefer local evidence over intended architecture: inspect code, docs, configs, generated artifacts, runtime wiring, validation signals, and recent diffs when relevant.
- Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.

## Architecture Quality Criteria

Evaluate architecture by how it assigns responsibility and contains change, not
by its file tree:

1. **Clear ownership:** Each important concept, rule, and lifecycle has an
   authoritative owner. Competing sources of truth are absent or explicitly
   reconciled.
2. **Stable boundaries:** Responsibilities that change for different reasons
   are separated, and dependency direction prevents lower-level details from
   owning higher-level policy.
3. **Cohesion:** Responsibilities grouped under one owner naturally evolve
   together. Technical proximity alone is not evidence that they belong
   together.
4. **Change locality:** A change to one concept primarily affects its owner,
   explicit contracts, and direct consumers rather than unrelated modules.
5. **Explicit rules:** Important invariants, policies, and transitions are
   named and attached to an identifiable owner instead of being reconstructed
   from scattered call sites.
6. **Evolution path:** A likely new capability has an obvious owner and
   extension path without requiring a parallel manager, generic helper, or
   duplicate concept.

Treat these criteria as architectural questions, not a scorecard. Repository
layout may provide evidence about ownership and boundaries, but it is an
expression of architecture rather than architecture itself. Use
`repository-layout-refactor` only after the ownership decision is sufficiently
clear to implement.

## Agent Legibility As An Architecture Concern

Architecture is also consumed by future coding agents. Clear ownership and
boundaries should make it possible for an agent to identify the authoritative
owner of a concept, select the smallest useful context, localize a change, and
discover likely downstream effects.

Treat agent legibility as a consequence of architecture quality, not as a
replacement for architecture review:

- `architecture-review` asks where authority and responsibility should live,
  whether the current boundary is coherent, and how a structural change should
  be sequenced.
- `agent-legibility-review` asks whether a future agent can discover, interpret,
  and safely modify the repository as it exists.

Use the standalone legibility skill when the primary question is navigation,
hidden conventions, or future-agent modification risk rather than an
architecture decision.

Do not infer architecture quality from file length or folder count alone. A
large cohesive module can be a valid deep module; many small files can still
hide authority behind indirection. File size and flat layout are investigation
signals only. Report an architecture finding when evidence shows mixed reasons
to change, ambiguous authority, fragmented lifecycle ownership, or a broad
change surface.

## Review Documentation Shape

Choose the documentation shape after the architecture map and finding
disproof pass, not before:

- **Simple review:** Keep one document when the scope is narrow, the owner is
  clear, the evidence is small, and the decision can be understood without
  unrelated context.
- **Complex review:** Use one entry document plus cohesive module documents
  when the review crosses independent owners, lifecycles, decision axes, or
  validation boundaries. The entry document should provide reading order,
  module links, and a short cross-module summary.
- **Existing repository convention:** Follow the repository's established
  documentation or ADR convention when one exists. Do not create a new
  hierarchy just to satisfy a preferred format.

For a modular review, each module document should state its scope, owner,
authoritative evidence, decision, prohibited behavior, validation boundary,
and revisit trigger. Cross-reference the other modules instead of copying
their full conclusions. When one later finding changes only one module, update
that module and the entry index; update the aggregate review only when the
cross-module conclusion actually changes.

This is a complexity-sensitive option, not a mandatory multi-file workflow.
The goal is high cohesion and low coupling in the review record, while keeping
small reviews compact and easy to consume.

## Review Process

Follow this order. Do not jump to recommendations before building the architecture map.

1. Read local architecture evidence.
   - Inspect top-level structure, package boundaries, entrypoints, build/config files, generated or vendored areas, and major integration points.
   - Read local guidance if available: architecture docs, ADRs, specs, contribution docs, runbooks, and decision records.
   - Treat docs as evidence to compare against code, not as unquestioned truth.

2. Build a concise architecture map.
   - Identify major modules, what each appears to own, and which boundaries separate transport, persistence, orchestration, domain rules, presentation, infrastructure, policy, and external integrations.
   - Record main data/control flow only where it explains ownership or boundaries.
   - For important concepts, record the likely future-agent edit path: where an agent would start, which owner it should trust, and which consumers it must discover. Keep this architectural; use `agent-legibility-review` for a full navigation audit.

3. Identify important concepts and authorities.
   - List recurring domain nouns, state concepts, lifecycle concepts, external actors, resources, policies, and data shapes.
   - For each important concept, identify its owner, authoritative source, and places it is redefined, translated, validated, mutated, persisted, or removed.
   - Flag authority conflicts where multiple files, modules, schemas, configs, or docs appear canonical for the same concept.

4. Review boundaries and lifecycle ownership.
   - Ask what each module owns, what it should not own, and what would cause it to change.
   - Check whether concept meaning stays consistent across layers, packages, generated artifacts, services, and external integrations.
   - Flag boundary drift such as persistence owning lifecycle decisions, transport layers owning core rules, shared utilities becoming hidden domain owners, or adapters redefining internal concepts.

5. Detect architectural risks.
   - Duplicated concepts: repeated status groups, mappings, validation rules, defaults, policy checks, lifecycle transitions, or schema assumptions.
   - Scattered rules: a rule that can only be understood by reading several call sites or call order.
   - Hidden assumptions: invariants implied by defaults, defensive branches, comments in unrelated files, generated artifacts, or undocumented data contracts.
   - Over-engineering: abstraction, compatibility layers, generic helpers, or configuration that obscures ownership without proven variation.
   - Architecture drift: implementation that conflicts with documented or clearly implied architecture decisions.

6. Assess architectural change surface.
   - Ask how many modules must change for one important concept change, such as a new state, provider, workflow step, domain field, policy, validation rule, or integration.
   - Treat large change surface as architectural only when it reveals fragmented ownership, unclear authority, or excessive coupling.

7. Run the Finding Disproof Pass.
   - Challenge each candidate finding with counter-evidence before reporting it.
   - Reject, downgrade, or preserve uncertainty when local rationale, ownership evidence, tests, or scope limits weaken the claim.

8. Produce findings and a phased refactor plan.
   - Prioritize issues by correctness risk, authority conflict, boundary erosion, drift, and change cost.
   - Recommend the smallest useful architectural improvement.
   - Favor changes that can be reviewed one concept or boundary at a time.
   - Separate new findings from known or intentional architecture debt.

## Finding Heuristics

Use these checks to decide whether something is an architecture finding:

- Ownership: Can two places both change or define the same concept?
- Authority: Which source should reviewers trust when sources disagree?
- Boundary: Did a module take responsibility for a concept owned elsewhere?
- Meaning: Does a concept keep the same meaning when it crosses a boundary?
- Lifecycle: Are create, validate, transform, transition, persist, and remove responsibilities owned coherently?
- Rule location: Does a rule live with the concept owner, or is it scattered across callers?
- Decision consistency: Does implementation still follow documented or clearly implied architecture decisions?
- Change surface: Would one concept change require broad edits because ownership is fragmented?
- Schema and configuration authority: Does a component that only stores,
  routes, exposes, or validates extensible data also redefine the owner's field
  sets, enums, combinations, or lifecycle semantics?
- New-variant test: When the authoritative owner adds one valid variant, which
  components must change, and do any passive consumers change without owning or
  interpreting the new meaning?
- Abstraction fit: Does an abstraction clarify ownership or hide it?
- Debt lifecycle: Is a known architecture compromise documented with rationale and a retirement condition?
- Agent-facing boundary: Can a future agent identify the concept owner and expected impact surface from the architecture, or must it infer authority from unrelated files?

Avoid turning local implementation concerns into architecture findings unless they affect ownership, authority, boundaries, concept lifecycle, architecture drift, or change surface.

### Persistence Error Ownership

When the reviewed architecture includes a persistence boundary, evaluate error
translation as an ownership concern:

- Database driver and ORM exception types, SQLSTATE values, constraint names,
  and diagnostic objects belong inside the persistence adapter. Application or
  domain services should not parse or depend on those details.
- Translate expected constraint, uniqueness, and concurrency outcomes at the
  repository, DAO, persistence-adapter, or unit-of-work boundary into semantic
  outcomes or exceptions. Let the application/service layer map those semantics
  to business errors, and let the transport layer serialize the public contract.
- Keep unexpected persistence failures distinguishable from expected conflicts;
  do not turn every integrity or database failure into a business conflict.
- Raw persistence diagnostics may support safe internal logging or debugging
  inside the persistence boundary, but should not become business or public API
  fields.
- Judge the responsibility boundary rather than requiring a module or class
  literally named `Repository`; transaction scripts and other architectures may
  assign the same responsibility differently.

Use this only as an illustrative flow, not a required naming scheme or fixed
error taxonomy:

`Database/ORM detail -> persistence semantic outcome -> service business error -> transport response`

## Finding Disproof Pass

Generate candidate findings first, then validate them adversarially before reporting them.

For each candidate:

- Search for counter-evidence in code ownership, docs, ADRs, tests, runtime wiring, generated artifacts, and recent local conventions.
- Ask whether this is intentional architecture debt with rationale and a retirement condition.
- Ask whether the issue is actually a local implementation concern rather than architecture.
- Check whether a single authoritative owner or source was missed.
- Check whether apparent duplication is necessary boundary translation rather than conflicting authority.
- Check whether the proposed abstraction would reduce ownership ambiguity or merely add indirection.
- Downgrade or reject findings when counter-evidence is strong; preserve uncertainty when the repository evidence is incomplete.
- Avoid letting the same reasoning path both create and validate the finding without challenge.

When useful, list rejected candidates under "Known Architecture Debt" or "Non-Issues / Intentionally Not Flagged" instead of reporting them as findings.

## Priority Scale

- P0: Architectural issue can cause severe correctness, security, data integrity, deployability, or operational failure and needs immediate attention.
- P1: High-impact authority, ownership, boundary, hidden-rule, drift, or change-surface issue likely to cause regressions or block important work.
- P2: Meaningful concept duplication, scattered-rule, lifecycle, or boundary issue worth scheduling soon.
- P3: Low-risk architecture clarification, documentation, or small structural cleanup.

## Output Format

Use this structure unless the user asks for a different format. Keep it concise; omit sections with no meaningful findings.

### Executive Summary

- architecture health
- biggest architectural risks
- smallest useful improvement

### Architecture Map

- major modules and responsibilities
- key concepts and owners
- authoritative sources
- important boundaries
- major architecture decisions and drift, if any
- future-agent edit paths for architecturally important concepts, when relevant

### Findings

Use a table:

| Priority | Location | Issue | Architectural reason | Smallest useful action | Risk if unchanged |
|---|---|---|---|---|---|
| P0/P1/P2/P3 | file/module/function/doc or repo-wide | concrete issue | ownership, authority, boundary, lifecycle, drift, or change-surface reason | targeted action | likely consequence |

Every finding must cite a concrete location or clearly state that it is inferred from repository-wide structure.

### Concept And Boundary Notes

Use only when it adds signal beyond the findings:

- duplicated concepts or scattered rules
- authority conflicts
- hidden assumptions
- unclear lifecycle ownership
- boundary drift

### Change Surface

For important concepts, state what would need to change and why the surface is large or small. Keep this focused on architectural coupling, fragmented ownership, or unclear authority.

### Known Architecture Debt

List only deliberate, documented, or accepted architecture debt that would otherwise be repeatedly reported:

- debt
- rationale
- retirement condition

### Non-Issues / Intentionally Not Flagged

Use only when it prevents repeated false positives. Briefly list candidate findings rejected by the disproof pass and the evidence that invalidated them.

### Refactor Plan

- Phase 1: smallest low-risk ownership, authority, or boundary clarification
- Phase 2: structural consolidation that needs broader validation
- Phase 3: longer-term architecture direction, only if supported by evidence

For each phase, name expected blast radius, validation needs, and rollback shape when non-trivial.

## Quality Bar

- Findings must be architectural, not ordinary implementation nits.
- Findings must be evidence-backed. Say what was inspected and what remains uncertain when evidence is incomplete.
- Findings must survive the Finding Disproof Pass; do not report candidates invalidated by local rationale, ownership evidence, tests, or scope limits.
- Prefer targeted ownership, authority, boundary, or concept-lifecycle fixes over broad rewrites.
- Do not recommend compatibility aliases, re-exports, adapters, or migration layers unless real consumers or rollout constraints justify them.
- Do not include technology-specific rules unless they come from the current repository's own docs or code.
- For non-trivial recommendations, identify likely owner, expected blast radius, validation needs, and rollback shape.
- Do not recommend splitting a large file or adding directories unless the new boundary gives a concept a clearer owner or materially narrows its change surface.

## Source and License

Created by Ray Carter (ruicore). Free and open source under Apache-2.0.

- Source: https://github.com/ruicore/codex-skills/tree/main/skills/architecture-review
- License: [Apache-2.0](LICENSE), included with this skill directory.
