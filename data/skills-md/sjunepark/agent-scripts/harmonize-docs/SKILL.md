---
name: harmonize-docs
description: "Harmonize all repository docs and plans by default, or only the documentation affected by an explicitly stated change, file, topic, plan, subsystem, or comparison. Explicit invocation only."
---

# Harmonize Docs

Treat the repository's documentation as one system. Replace sediment with a
coherent account of present reality and future intent: each durable fact has
one canonical home, current implementation and target design remain visibly
distinct, each active plan reflects reality and remaining intent, and the
documents route readers without contradiction.

Use a light pruning bias: when alternatives preserve the same durable reader
value, prefer the leaner one. Treat concise, well-scoped documents as already
at their natural depth. Preserve or add detail when it materially improves
understanding, rationale, operational safety, or future decisions.

## Scope contract

- With no explicit scope, harmonize the repository's entire active documentation
  system.
- With an explicit scope, treat it as the seed for one bounded harmonization.
  The scope may be described naturally as changes, paths, a topic, a plan, a
  subsystem, or a comparison; do not require a fixed command vocabulary.
- When the scope is `changes`, use the change set named by the user or established
  by the current task. If neither identifies one, use current staged, unstaged,
  and untracked working-tree changes. If no meaningful change set can be
  identified, resolve the boundary instead of silently substituting unrelated
  branch history.
- Expand a scoped seed only to its necessary documentation impact closure: the
  canonical documents that own affected claims, active plans or status records
  that track the affected work, and navigation or cross-references that must
  change with them. Source files may supply evidence without entering the edit
  boundary.
- Do not inventory or reconcile the whole documentation system during a scoped
  run. Record a credible unrelated inconsistency for follow-up rather than
  broadening the run without user direction.

Apply the same state model and quality bar at either scale. Only discovery,
coverage, validation, and completion are bounded by the established scope.

## State contract

Treat project status as three independent questions:

- **Implementation reality:** What behavior, structure, and operational boundary
  are verifiably present now?
- **Target design:** What future behavior or structure is selected, proposed, or
  unresolved?
- **Delivery status:** What work connects reality to the target, and what is
  completed, active, blocked, deferred, or next?

Do not let one answer stand in for another. A target can be accepted without
being implemented; an implementation can exist without being validated,
supported, published, authorized, or production-ready. Preserve any such
readiness distinctions that matter to the repository instead of compressing
them into a single label such as `current` or `complete`.

Make the state of each material claim clear on first reading. Reserve
unqualified present-tense behavior for verified implementation reality. Future
or historical material needs visible framing through the document's opening,
section headings, a concise status map, tense, or an explicit date. A document
may span multiple states, but its boundaries must remain legible without
requiring readers to reconstruct them from several files.

## Coordination

Use subagents for bounded, independent documentation areas when delegation
materially improves coverage. Handle a small coherent scope directly. The
coordinating agent owns complete coverage of the established boundary, conflict
resolution, and the integrated result.

## Workflow

### 1. Establish the documentation boundary

- Read the effective repository instructions and inspect working-tree state.
- Determine whether the invocation supplies an explicit scope. If it does,
  identify the seed and trace only its necessary documentation impact closure.
  If it does not, discover documentation across the repository through its
  conventions, navigation files, links, and common documentation and planning
  names or extensions.
- For a repository-wide run, include all active, human-authored documentation:
  overview and contributor docs, plans and progress trackers, decisions,
  runbooks, instructions, and subsystem or tool documentation.
- For a scoped run, include only documents with claims, status, or routing
  materially affected by the seed. Do not include a document merely because it
  mentions the same broad area.
- Include documentation-specific navigation and configuration files needed to
  keep the in-scope documentation reachable and valid, even when they are not
  prose.
- Treat archives, generated output, vendored material, dependencies, and build
  artifacts as outside the boundary. Preserve immutable historical content, but
  include a record's reader-facing status and navigation when it remains part of
  the active documentation system within the established boundary.
- Preserve unrelated working-tree changes as intentional.

Complete this step when the boundary and its evidence are explicit. For a
repository-wide run, every plausible documentation file is classified as in
scope or outside it. For a scoped run, the seed and necessary impact closure are
accounted for without an exhaustive repository inventory.

### 2. Reconstruct truth by claim type

- Read every in-scope document completely. Use source files as evidence, not as
  additional editing scope.
- Verify claims about current behavior, availability, and readiness against
  code, configuration, tests, commands, releases, and repository state.
- Recover future intent from the latest confirmed user direction and active
  plans. Distinguish unfinished intent from a false current-state claim.
- Do not infer implementation from confident wording, present-tense design
  prose, or an accepted architecture. A selected design and an implemented
  system are independent states until repository evidence connects them.
- Recover decisions and rationale from decision records and confirmed context.
  Mark genuinely unresolved intent instead of inventing it.
- Time-scope historical material that remains in active reader paths. Preserve
  immutable records; use lifecycle framing or correct the current documents
  that route to them instead of silently rewriting decision-time assertions.
- Classify material claims along independent axes: verified implementation
  reality; design authority such as selected, proposed, or unresolved; and
  delivery status from the repository's planning vocabulary. A selected target
  may be unimplemented, partially implemented, or implemented. Separately mark
  durable rationale, obsolete or duplicate material, and unresolved conflict.

Complete this step when every in-scope document has been read, every material
claim has an evidence-backed classification, and every conflict is visible.

### 3. Design the target documentation system

- When the boundary includes creating, rewriting, splitting, merging, or
  relocating `ARCHITECTURE.md` files, read
  [Architecture documentation](guides/architecture-docs.md) before choosing
  their topology or contents. Apply that guide within this harmonization; do
  not route the work to a second skill or leave architecture claims
  unreconciled with the rest of the documentation system.
- Give each document a clear purpose, audience, scope, and lifecycle.
- Give each durable fact one canonical home. Let other documents link to it or
  carry only the local context their readers need.
- Give each mutable state within its scope one canonical owner: implementation
  reality, target design, and delivery status must not drift across competing
  status sources. Ensure repository entry points route readers to those owners.
- Treat tool-recognized instruction files as configuration: verify their
  filenames, scope, discovery, and precedence before changing their topology,
  and preserve the intended effective hierarchy.
- Assign every in-scope document a disposition: keep, rewrite, merge, split,
  move, delete, or replace. Create a document only when a distinct durable
  responsibility has no suitable home.
- Merge overlapping documents. Split a sprawling document when its parts have
  distinct audiences, ownership, scopes, or lifecycles. Keep parent documents
  concise and route detail to focused child documents.
- Keep implementation truth and target design separately legible without
  imposing fixed filenames or mandatory `AS-IS` and `TO-BE` sections. Target
  architecture may remain in durable architecture or design documents when its
  status and unimplemented boundaries are explicit. When one document spans
  both states, use concise document or section framing, or a status map linked
  to implementation evidence.
- Let the repository's roadmap, active plans, or equivalent progress records
  own delivery order, the implementation gap, progress, and next actions. Do
  not turn an architecture status map into a second roadmap.
- Shape active plans around current state, remaining work, blockers, decisions,
  and the next useful action. Compress completed history once its durable
  lessons and decisions have a proper home.

Complete this step when every in-scope document has one disposition and every
durable claim has one destination or an explicit reason for removal, with no
planned orphan or duplicate source of truth.

### 4. Apply one harmonious rewrite

- Apply the target topology directly, including justified file creation,
  merging, splitting, moving, and deletion.
- Rewrite each document as a coherent whole. Integrate new information at its
  natural location and reshape surrounding material so the result does not read
  like a sequence of appended updates.
- Remove stale statements, superseded plans, duplicate explanations, empty
  scaffolding, transcript-like discussion, and incidental detail that lacks
  durable reader value.
- Preserve useful intent, rationale, constraints, and unresolved questions even
  when their original wording or file no longer belongs.
- Preserve selected future design without presenting it as current behavior.
  Use visible state framing instead of repetitive sentence-level hedging, so a
  reader can tell what exists, which selected design boundaries remain
  unimplemented, what remains undecided, and where delivery is tracked.
- Update tables of contents, indexes, cross-references, links, paths, commands,
  terminology, and parent-child routing for the new topology.
- Keep non-documentation implementation files read-only. Documentation-specific
  navigation and configuration remain within the boundary from step 1. Leave
  staging, commits, and pushes to a separate explicit request.

Complete this step when every planned disposition is applied, each surviving
claim is in its canonical home, and all affected navigation follows the new
structure.

### 5. Reconcile the finished system

- Re-read the final documents together rather than reviewing only the diff.
- Search for old paths, renamed terms, stale commands, duplicated claims,
  conflicting statuses, broken references, and append-style sediment.
- Review durable documentation for hard-coded counts and other volatile facts,
  such as numbers of files or tests. Replace them with stable invariants or
  pointers to the source of truth.
- Recheck implementation-reality and delivery-status claims against repository
  evidence, and target-design claims against confirmed direction and decisions.
- Audit state transitions in both directions: verified completed work must be
  promoted into the canonical current-state account and its delivery records
  updated; unfinished target behavior must not be promoted merely because it
  is fully designed or scheduled.
- Reconcile direct-entry documents after each material state transition,
  including relevant overviews, package and release docs, operational guides,
  architecture maps, and active plans. Do not leave the precise state visible
  only in a low-level goal or progress record.
- Confirm that every target's implemented and unimplemented boundaries are
  visible, every unresolved possibility remains non-authoritative, and overview
  documents route readers to the canonical implementation, target-design, and
  delivery sources.
- Run available documentation, link, example, and repository validation that is
  relevant to the changed files. Inspect the final diff and working-tree state.
- Account for every initially discovered file and every earlier conflict.
  Report anything that cannot be verified and keep uncertainty explicit in the
  appropriate document when readers need it. In a scoped run, report credible
  out-of-scope conflicts separately without pursuing them.

Complete this step only when all in-scope files and material claims are
accounted for, all verifiable references and state claims have been
checked, no conflict is concealed, and validation passes or its limitation is
recorded.

### 6. Report the harmonization

Summarize topology changes, meaningful corrections, canonical ownership
decisions, unresolved uncertainties, and validation results. Keep the report
short and point to the changed documents instead of repeating their content.

Complete the run when the user can see what changed, where current
implementation, target design, and delivery status are authoritatively recorded,
and what—if anything—still needs a decision.
