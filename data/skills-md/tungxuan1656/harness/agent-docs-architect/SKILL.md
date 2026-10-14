---
name: agent-docs-architect
description: >-
  Design or audit the agent-facing repository knowledge system for a software
  project. Use when a user needs to decide which product, domain, architecture,
  integration, data, security, reliability, execution, generated-reference, or
  navigation documents a repository needs; their paths, names, ownership,
  reading routes, and maintenance contracts; or how that system should change
  with project stage, topology, stack, integrations, risk, and coordination.
  Use before writing a multi-document documentation set. Pair with
  agent-docs-writer to create approved documents. Do not use to write one
  already-selected document or to make unapproved product or architecture
  decisions.
---

# Agent Docs Architect

Design the smallest repository knowledge system that lets an agent find the
right truth, identify missing decisions, and act without loading the whole
repository into context.

## Promise and boundary

Return an evidence-backed answer to: what knowledge must live with this
repository, which document owns it, where the document belongs, when an agent
must read it, and how it stays current.

Use business-analysis and solution-architecture lenses to discover information needs. Do not
act as the product owner or solution architect.

| This skill does | This skill does not |
|---|---|
| Identify missing product rules, technical decisions, and operating constraints | Invent or approve those rules and decisions |
| Recommend a product spec, decision record, contract, or guide | Choose product behavior, system architecture, or a technology |
| State open questions and their decision owner | Present assumptions as accepted truth |
| Design artifact ownership, paths, routes, and lifecycle | Write document prose or templates owned by `agent-docs-writer` |

## Apply the core rules

- Give every durable fact one canonical owner. Link to that owner elsewhere.
- Keep `AGENTS.md` as a short router and repository-wide rule surface.
- Separate durable knowledge, active work, history, generated truth, and
  external references.
- Use a documented default convention for a new or materially incomplete
  repository. Treat it as a baseline, not a quota.
- Reuse a repository-native artifact when it already owns the required truth.
  Do not rename it only for uniformity.
- Create an artifact for a demonstrated failure, credible risk, or required
  decision. Do not create empty directories, placeholders, or generic guides.
- Start from no new document. Treat scale profiles as examples, not default
  trees to generate. Explain the smallest omission that keeps work safe.
- Record unresolved facts as questions with a decision owner. Do not fill gaps
  from typical industry practice.
- Prefer progressive disclosure: router -> one focused source -> code and
  tests.

## Run the workflow

### 1. Inventory evidence

Inspect before recommending a structure:

1. Read git status and preserve unrelated work.
2. Inspect the root tree, manifests, workspaces, entry points, tests, CI, and
   deployment shape.
3. Identify runtimes, frameworks, data stores, interfaces, event paths,
   external systems, generated surfaces, and operational tooling.
4. Find existing instructions, READMEs, specifications, decision records,
   plans, schemas, runbooks, issue trackers, and external knowledge sources.
5. Classify relevant facts as `Observed`, `Intended`, `Proposed`, or
   `Uncertain` when sources disagree.

For a greenfield repository, inventory the supplied brief, constraints, and
accepted decisions. Mark all unconfirmed design as `Proposed` or `Uncertain`.

### 2. Assess knowledge pressure

Read [assessment and profiles](references/scale-profiles.md). Assess project
stage, product and domain complexity, topology, stack diversity, integrations,
data, risk, delivery horizon, coordination, change rate, and generated
surfaces.

Select the nearest delivery profile only as a baseline. Promote or demote each
capability from its own pressure signals. Do not infer documentation needs from
lines of code alone.

### 3. Find truth and decision gaps

Read the [artifact catalog](references/artifact-catalog.md). For every required
knowledge class:

1. Name the current source and its status: canonical, duplicated, stale,
   missing, inaccessible, or external-only.
2. Identify the concrete failure or risk if an agent cannot access the truth.
3. Distinguish a missing document from a missing decision.
4. For a missing decision, record a concise question, affected artifacts, and
   decision owner instead of proposing an answer.
5. Preserve useful existing sources even when their filenames differ from the
   default convention.

### 4. Select artifacts and conventions

Read [repository conventions](references/repository-conventions.md). Start
with the baseline for the selected profile, then retain only artifacts justified
by the assessment. Use the convention's names and paths for new artifacts unless
an existing repository convention is stronger.

Treat cross-cutting guides as conditional. For example, create security,
reliability, data, frontend, or observability guidance only when a shared,
repository-specific invariant needs one canonical owner.

### 5. Design reading routes and maintenance

For each common task, define a shallow route:

```text
agent instruction entry point
  -> one focused document when needed
  -> relevant code, contract, and tests
  -> proportional verification
```

Add an index only when several focused documents need selection. Add nested
instructions only when a subtree has genuinely different tooling or invariants.
For each volatile artifact, define the event, owner, generator, or mechanical
check that keeps it current.

### 6. Produce a blueprint

Use [blueprint format](references/blueprint-format.md). Include the assessment,
knowledge gaps, proposed tree, artifact contracts, routes, intentional
omissions, maintenance contract, and writer handoff.

Default to a proposal. Do not mutate repository documentation unless the user
asks to apply the blueprint.

### 7. Apply through the writer

When the user accepts the blueprint:

1. Lock the artifact map, ownership table, open decisions, and naming
   convention.
2. Use `agent-docs-writer` for each approved document.
3. Give the writer the artifact responsibility, evidence sources, required
   routes, lifecycle, and size constraints.
4. Create canonical truth before indexes and the root router.
5. Check the final graph for duplicated truth, broken routes, unlabelled
   uncertainty, empty artifacts, and mixed durable or temporary state.
   Use `agent-docs-checker` when installed for a requested independent read-only
   assessment; do not require an extra agent or audit on every writing task.

If `agent-docs-writer` is unavailable, return the blueprint and handoff package.
Do not invent a competing document-writing standard inside this skill.

## Keep scope narrow

Do not:

- turn a documentation architecture request into a broad codebase rewrite;
- create a full documentation tree merely because a large-project baseline
  includes it;
- replace an issue tracker, schema generator, or external documentation system
  without an explicit migration decision;
- copy external material into the repository without a canonical ownership and
  freshness decision;
- prescribe document prose, sentence style, or templates owned by
  `agent-docs-writer`.

## Validate the architecture

Before delivery, verify that:

- each recommendation follows an observed need, credible risk, or explicitly
  stated greenfield constraint;
- project size is not the sole determinant of the document set;
- every artifact owns one class of truth and has an appropriate lifecycle;
- unresolved product or architecture choices remain visible as open decisions;
- the default convention is applied only where no adequate native convention
  exists;
- ordinary tasks need at most one focused document after the entry point;
- generated and external sources have reproducibility or freshness contracts;
- indexes route instead of duplicate their children;
- the writer handoff is sufficient to draft without redesigning the knowledge
  system.
