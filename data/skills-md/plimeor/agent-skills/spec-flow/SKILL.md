---
name: "spec-flow"
description: "Manage a repo's docs for plans, specs, structure, and decisions. Use when setting up the docs layout; planning a feature or change; reviewing a plan's skeleton or spec change files; checking finished work against its plan; archiving a shipped plan; recording, superseding, or consolidating a decision record; tidying existing specs or decisions; or building or checking docs/architecture.md against the code. Near miss: a principle-based judgment of a design outside a plan is code-design-review; a review of a diff with no plan is code-review."
---

# Spec Flow

Keep a trace of intent, structure, and decisions in the repo without letting stale documents pass as current truth. Three ideas govern it. **A document's location states its status**: a reader, human or agent, knows from the directory alone whether a file describes intent, reality, or history. **A spec states promises, not behavior**: it holds what the project would owe users a fix or a migration note for, and stays silent on everything else, however visible. **Structure comes before detail**: a change that alters the structure states its skeleton — the units, what each owns, the interfaces between them, the paths through them — and reviews it before anything below it is written; the top level of that structure stays in force in `docs/architecture.md`, and the code holds the rest.

This file is the map: the layout, how to read a repo's state, which operation a request maps to, and the contract of each document type. Each operation's steps, stops, and templates are in its own file under `references/`; read that file before running the operation.

A feature moves through `propose → (implementation) → verify → archive`. `init` runs once per repo. `decide` applies at any point. `tidy` and `architecture-review` run on request, outside any plan. `skeleton-review` runs inside `propose`, `spec-review` inside `propose` and `verify`; both also run on request. `readability-review` is the last part of `skeleton-review`, of `spec-review` when it fixes, of `architecture-review`, and of `propose`'s check of `plan.md` and the design; it also runs on request.

Sources: plan and spec formats adapted from OpenSpec's `spec-driven` schema — https://github.com/Fission-AI/OpenSpec/blob/main/schemas/spec-driven/schema.yaml · the interview in `propose` adapted from Matt Pocock's `grilling` skill — https://github.com/mattpocock/skills · the architecture doc adapted from matklad's `ARCHITECTURE.md` — https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html — and arc42's building block view — https://docs.arc42.org/section-5/ · the skeleton's inclusion test adapted from BMAD-METHOD's architecture spine — https://github.com/bmad-code-org/BMAD-METHOD

## Layout

- `AGENTS.md` / `CLAUDE.md` — the conventions block, and the overview loaded every session
- `docs/overview.md` — one to two pages: what, principles, current focus, next, non-goals
- `docs/architecture.md` — reality: the structure in force at the top level — the units, what each owns, how they depend on each other, the invariants between them
- `docs/specs/[<area>/]<feature>.md` — reality: the promises a shipped feature makes to its users
- `docs/plans/<slug>/` — intent: one directory per feature being built or queued
  - `plan.md` — why, what changes, out of scope, tasks; the design too when it is short
  - `skeleton.md` — the structure the change builds on: units, interfaces, ownership, paths, and the changes to `docs/architecture.md`
  - `design.md` — how: the rest of the technical design, once it outgrows `plan.md`
  - `design/<topic>.md` — a large design split by topic, with `design.md` as its index
  - `specs/[<area>/]<feature>.md` — proposed changes to `docs/specs/[<area>/]<feature>.md`
  - attachments — a review page, a schedule, or another file `plan.md` or the design links to
- `docs/archive/YYYY-MM-DD-<slug>/` — history: a shipped plan's directory without its `specs/` and the skeleton's Architecture changes, kept as it was
- `docs/decisions/NNNN-slug.md` — live: cross-feature decisions in force (`Accepted`) or ruled out (`Rejected`)
- `docs/decisions/superseded/` — history: replaced decision records, not read by default

The `## Docs conventions` block in the repo's instruction file is authoritative for paths. Read it first; a repo may place these directories elsewhere. Use the defaults above only when the block is absent.

Write documents in the language the repo's existing docs use. The structural keywords `Type:`, `Budget:`, `Requirement:`, `Scenario:`, `ADDED`, `MODIFIED`, `REMOVED`, `WHEN`, `THEN`, `AND`, `Owns:`, `Depends on:`, `Called by:`, `Lives in:`, `Checked against the code:`, and the type names `feature`, `api`, and `format` stay as written.

## Reading a repo's state

Before any operation, and to answer any question about where a project stands, read in this order. Each location answers one question and no other.

- **The `## Docs conventions` block** in `AGENTS.md` / `CLAUDE.md`: where the directories below live in this repo. It says nothing about the project. A missing block means `init` has not run.
- **`docs/overview.md`**: what the project is, its principles, the current focus, what is next, the non-goals. Not what is shipped; the specs directory is the inventory.
- **`docs/architecture.md`**: the structure in force at the top level: the units a maintainer navigates by, what each owns, how they depend on each other, and the invariants between them. Not behavior, which is the specs'; not why, which is the decisions' and the archive's; nothing below the top level, which is the code's.
- **`docs/specs/`**: the promises in force, one file per shipped feature. Not how the code does it, nor anything a spec is silent on.
- **`docs/plans/`**: live intent. Every directory is a feature being built or queued; the unticked Tasks in its `plan.md` are the open work; its skeleton and design are how the work is meant to be built; its `specs/` are proposals. Not how the system behaves today.
- **`docs/decisions/`**, the files directly in it: decisions in force (`Accepted`) and approaches ruled out (`Rejected`). Not feature behavior; that is the spec's.
- **`docs/archive/`** and **`docs/decisions/superseded/`**: why things came to be as they are. Not current behavior or open work; read only when the question is why.

The code is authoritative over the specs and the architecture doc. A spec or an architecture entry that disagrees with it is the defect, except where the code breaks a guarantee users rely on or an invariant the architecture doc states; that is a suspected bug to report, not to write into the document.

## Routing

Identify which operation the request maps to, then read that operation's file before doing anything else; it holds the steps, the stops, and the templates the operation writes. When a request maps to none, say so rather than improvising a new transition.

- **Set up the docs layout** in a repo that has none, or complete a partial one: `init`, in `references/init.md`.
- **Plan a feature or a change** ("I want to add", "let's build", "propose"): `propose`, in `references/propose.md`.
- **Review a plan's skeleton** ("review the skeleton", "check the plan's structure"): `skeleton-review`, in `references/skeleton-review.md`.
- **Review a plan's spec change files** against the spec contract: `spec-review`, in `references/spec-review.md`.
- **Review a document's readability** ("the plan is hard to read", "clean up the skeleton's prose", "can a newcomer follow the architecture doc"): `readability-review`, in `references/readability-review.md`.
- **Check finished work against its plan** ("is it ready", "verify", "review against the plan"): `verify`, in `references/verify.md`.
- **Ship a verified plan** ("archive", "merge the spec changes"): `archive`, in `references/archive.md`.
- **Record, change, or consolidate a cross-feature decision**: `decide`, in `references/decide.md`.
- **Tidy, shorten, or consolidate existing specs or decisions**: `tidy`, in `references/tidy.md`.
- **Create, refresh, or check the architecture doc** ("update the architecture doc", "does the architecture doc still match the code"): `architecture-review`, in `references/architecture-review.md`.

Three requests map to no operation:

- **Implement a plan's tasks.** Read the plan's Tasks to find what is open, tick each task as its work lands, follow its skeleton and design, keep `plan.md`, the skeleton, the design, and the spec change files consistent, and write the code against the spec change files and the specs the plan leaves untouched.
- **A question about the project's state**: what is shipped, what is open, why something is the way it is. Read the state as above and answer; open the archive and `superseded/` only when the question is why.
- **Drop a plan.** See Abandoned plans.

## How plan, skeleton, design, and spec relate

A feature is worked out top-down:

1. `plan.md` sets the goal and the direction: why, which capabilities, and where the boundary lies.
2. The skeleton fixes the structure those capabilities are built on, when the change alters it: the units, what each owns, the interfaces between them, the paths a request takes through them, and the invariants they keep. It is reviewed before anything below it is written: every later level is built on it, so a wrong skeleton is paid for at every level.
3. The design works out the rest of how: flows inside a unit, external contracts and how the client consumes them, migration, rollout, and why the skeleton is the one chosen. Many details of behavior are settled here, such as a fallback after a timeout or how an old state maps to a new one.
4. Spec change files are extracted from the plan, the skeleton, and the design. They take only what passes the promise test; the design grows down toward implementation detail, and the spec does not follow it there. A large design therefore does not make a large spec, and structure does not enter one.
5. Tasks are cut from the skeleton and the design, the walking skeleton first.

The promise line decides what may enter a spec, not what may be written down. A detail below it never enters a spec. It may be written in the design, which is intent and is archived as history. A detail the implementer can settle in the code without a reviewer needing to see it first is written nowhere but the code and tests.

Changes flow down. A design change that alters a promise updates the spec change files in the same edit; one that alters the structure goes into the skeleton first. A gap found lower down, such as a spec that cannot be written or contradicts itself, is fixed upstream first, in the design, the skeleton, or the plan, then carried down. Between levels the upper one decides; when the upper one is itself in doubt, the question goes to the user.

After archive, `plan.md`, the skeleton, and the design are history; the spec is the only contract still in force, and `docs/architecture.md` states the structure in force.

## Document contracts

Each type has a template: the spec's under Templates below, the others in the file of the operation that writes them (overview, architecture doc, and conventions block in `init`, plan, skeleton, design, and spec change file in `propose`, decision record in `decide`). A document follows its template's sections in order; a section with nothing to say is omitted, not filled. The design is the exception: it uses the sections its change calls for, in the order that reads best.

### Overview — `docs/overview.md`

One to two pages, dated. Principles and non-goals are trade-off rules an agent applies when choosing an implementation. Status points at `docs/specs/` and lists no features: the directory is the inventory. The file is loaded every session, so length is a cost.

### Architecture — `docs/architecture.md`

The structure in force, at the top level only: what a maintainer needs to find where a change belongs and which rules between units it must not break. The document names what the code holds; it does not mirror it.

- **Bird's eye**: what goes into the system and what comes out, and the main path between them, in a few lines.
- **Codemap**: one entry per top-level unit — a crate, package, service, or directory group a maintainer would name — headed by the unit's name: its responsibility in one sentence, what it owns (state it alone writes, or a decision it hides), the units it depends on, and where it lives, named and not linked.
- **Invariants**: rules between units the project keeps on purpose, each with a short name, mostly written as absences: `<unit> never <calls | imports | writes> <what>`. An invariant a decision record set names the record.
- **Cross-cutting**: concerns that span units, such as errors, configuration, and authorization, one line each naming the unit that owns it.

The inclusion test for every entry: would a change confined to one unit's internals leave it true? Yes: it may stay. No: it is below the top level and belongs to the code, or to the skeleton of the plan that changes it. File trees, full data shapes, links, line numbers, and the paths of a single feature stay out.

- **Invariants are decided, not observed.** An absence found in the code becomes an invariant only when the user confirms it, a decision record sets it, or a shipped skeleton introduces it.
- **Who edits it.** `init` creates it empty; `archive` merges a shipped skeleton's Architecture changes; `architecture-review` builds the document from the code and corrects drift. Nothing else edits it.
- **Code is authoritative.** An entry that disagrees with the code is a defect in the document and is corrected to the code, with one exception: code that breaks an invariant is a suspected violation. The invariant is not rewritten to describe it; report it and let the user decide whether the code or the invariant changes.
- **Broken invariants block shipping.** An invariant the code breaks, as a plan leaves it — kept, introduced, or changed — makes `verify` return `Not ready` and stops `archive`, unless the user accepts it by name.
- **Checked date.** The line after the title reads `Checked against the code: YYYY-MM-DD`, the last day `architecture-review` compared the whole document with the code.
- **Length is a signal.** Past about 300 lines, the document likely holds entries below the top level; `architecture-review` lists them.

### Spec — `docs/specs/[<area>/]<feature>.md`

A spec is the set of promises one feature, named as a user would name it, makes to its users. It is not a description of behavior, a copy of the test suite, or an index of the code. Every statement the spec could carry lands in one of four places:

| The statement | Where it goes |
|---|---|
| A promise: if it changed, users would be owed a fix or a migration note | A requirement |
| Pinned but not promised: regression protection the project wants without owing anyone | The tests only; the spec is silent |
| Structure: the units, what each owns, the interfaces between the project's own units, dependency direction | Nowhere in the spec; a plan's skeleton while planned, then the top level in `docs/architecture.md` and the rest in the code |
| Left to the implementation | Nowhere in the spec; a plan's design may record it. When silence would mislead, one unspecified clause closing the requirement it qualifies |

The test for every sentence: if this changed, would users be owed a fix or a migration note? Yes: it is a requirement. No: it is not in the spec, however visible the behavior is.

- **Location.** `docs/specs/<feature>.md`, or `docs/specs/<area>/<feature>.md` when one feature area a user would name holds several specs. A spec's name is its path under `docs/specs/` without `.md`, such as `quick-buy/entry`; plans, tests, references, and archive searches use that name. An area directory needs no index file.
- **Type.** The line after the title reads `Type: feature`, `Type: api`, or `Type: format`. The type sets where the promise line lies.
  - `feature`: a capability users act on. The promise is what the user can do and what follows, at the grain the user would describe it. Orderings, tiebreaks, algorithm steps, and the format of internal values are the implementation's unless the user named them in the interview. Layout, icons, and styling stay out.
  - `api`: a library or interface that code outside the project calls, such as a published package, a public endpoint, or an extension point. An interface only the project's own code calls is structure, not a promise: its callers change with it in the same change, and nobody is owed a fix. The promise is signatures and types, guaranteed semantics, error conditions, and stability constraints such as versioning rules, build targets, and minimum toolchain. Exact outputs for given inputs, offsets, and the absence of panics under generated input are tests. Where an external specification is the authority, the spec names it and lists the extensions and divergences; it does not restate it. Examples show usage.
  - `format`: a data format, on-disk layout, or interop contract other tools read and write. The field table is the promise, written as a table under `## Fields`, one row per field: name, type, default, handling when invalid. Rows are not requirements. How leniently the format is read is one requirement.
- **Purpose**: one or two sentences on what the feature is for. Which unit implements it is the codemap's to say.
- **Requirements**: each is `### Requirement: <name>` followed by one normative statement using SHALL or MUST (or the equivalent in the repo's language). One rule per requirement, where a rule is what a reader applies as a unit: its input checks, error variants, and edge cases stay in the same requirement. A requirement that mixes several rules is split only along rules that pass the promise test; a split does not make the spec longer.
- **Unspecified clauses.** The default for what the spec does not promise is silence.
  - A clause such as `; the order within a tier is unspecified` closes a requirement's statement only when a reader of that rule would assume a finer rule exists and go looking or fill it in, or when the user placed the matter below the promise line in the interview.
  - The clause names what is left open and says nothing about what the implementation does today. What the agent alone judged below the line is not written.
  - There is no `Unspecified` section: a list of what is not promised grows the way a list of scenarios does.
- **Scenarios**: `#### Scenario: <name>` in WHEN / THEN form. A scenario exists only when the rule would be misread without it: the case that shows what the rule means, or the edge where it turns. Combinations, boundaries, and error variants are tests. Every scenario is a test case; most test cases are not scenarios.
- **Tests name requirements.** Each requirement is named by at least one test, in the test's name or a comment beside it. The name is the link from the promise to its evidence; `verify` checks it.
- **Details with another authoritative source.** When the repo already holds the authority for a detail — a data table in the code, a visual baseline, a design file, a generated schema, an external specification — the spec states the rule that defines it and shows at most one or two values. It does not enumerate the values or give counts derived from them.
- **Paths.** The spec names a concept, not the file that implements it. Where readers need the location, the codemap in `docs/architecture.md` maps the concept to it, in one place. A path stays in a spec only when it is itself observable: a path the user types, one printed in output, or a file whose presence the feature checks.
- **Budget.** Forty requirements. A `format` spec's field table is outside the budget.
  - `verify` returns `Not ready` and `archive` stops for a spec that would be over budget once a plan is merged; the finding names the cuts that bring it back: requirements that demote to tests or merge into one rule.
  - Length is a signal, not a limit. A spec past about 600 lines likely holds text the contract keeps out; `verify` and `tidy` list it with the lines that belong elsewhere. Length alone does not make `verify` return `Not ready` or stop `archive`.
  - A spec that holds more promises than the budget allows is usually two features a user would name separately; split it, under an area directory when the parts share one. When it is one feature, the line after `Type:` reads `Budget: <N> requirements, because <reason>`, so the exception is visible to every reader.
- **Requirement names are handles.** Other specs, tests, code comments, and docs cite a requirement by name. A change that renames, merges, or removes a requirement updates every such reference in the same change, except in `docs/archive/` and `docs/decisions/superseded/`, which stay as written.
- Code is authoritative. A spec that disagrees with the code is a defect in the spec, with one exception: when the code breaks a guarantee users rely on, such as data kept, state consistent across commands, or a security constraint, the disagreement is a suspected bug. The spec is not rewritten to describe it; report it and let the user decide whether the code or the spec changes.

**Bringing existing specs in line** is the `tidy` operation: a direct edit to `docs/specs/`, not a plan. It changes no behavior and states nothing the spec did not already state; what leaves the spec is in the tests or in git history, not lost.

### Plan — `docs/plans/<slug>/`

One plan covers one shippable feature or one change to shipped features. It may take months to build and touch any number of specs; all of it ships, and merges into the specs, together. Every directory in `docs/plans/` is live intent. Nothing under `docs/plans/` is evidence of how the system behaves.

**`plan.md`**
- **Why**: the problem or opportunity in one or two sentences. A large plan may follow it with up to five one-line summary bullets: scope, delivery dates, the largest risks, where the blocking questions are.
- **What changes**: one line per requirement added, modified, or removed, naming the spec and the requirement; a removed requirement's line gives the reason. The spec change file holds the content; What changes does not restate it. Lines may be grouped under headings by area.
  - Work that changes no spec, such as a change in another repository, gets one line per change.
  - When a target spec is new but the feature already runs, a `Differences from current behavior` list gives one line per way the promised behavior departs from what runs today; the spec states only the new promise and cannot show the difference.
  - Lists each affected spec by name as new or modified; each has a spec change file. A plan with no behavior change says so in one line.
- **Out of scope**: see the rule below.
- **Design**: the design inline, or one line pointing to `design.md`; a plan with a skeleton also points to `skeleton.md`. See Skeleton and Design below.
- **Tasks**: numbered groups of checkboxes, `- [ ] 1.1 <task>`, ordered by dependency, each small enough for one session. Each task is one sentence stating how its completion is verified; its details go in sub-bullets or name the section of the skeleton or design it follows. In a plan with a skeleton, group 1 is the walking skeleton: the interfaces and types the skeleton declares, wired along its first path with the thinnest behavior that lets one end-to-end test along that path pass. Each later group delivers a slice through the units it needs. Each group lands the tests its own work calls for; a final group holds integration checks only. A preamble before the first group holds only conventions specific to this plan, test drops, dependencies and parallel lanes between tasks, and the dates of external dependencies.

**Out of scope** records boundary decisions, not a description of what the feature is not. An item earns its place when leaving it unsaid would cause a wrong assumption:
- a reader of What changes would expect the plan to include it, or
- the implementer, already in that code, would be tempted to do it.

Every item comes from the interview, where the user ruled it out or deferred it, and is written as `<the work left out> — <why, or where it goes instead>`. An item with no such reason to give does not belong.

What stays out of the section:
- Things nobody would have assumed were included. A plan to build an aircraft does not list "not a rocket, not a train".
- Restatements of the feature's category or title in the negative.
- The overview's Non-goals; they already apply to every plan.
- Items invented while writing to make the section look complete.

The section has no minimum length. With no real boundary decision to record, it is omitted.

Tasks is the working checklist during implementation. A task is ticked the moment its work lands. An agent picking the work up, after a break or in a new session, reads Tasks first to find what is open.

**Skeleton — `skeleton.md`**

Written when the change adds, removes, or changes a unit, an interface between units, which unit owns a piece of state, or a dependency between units. A change confined to one unit's internals has none. A unit is what the codemap in `docs/architecture.md` names, or, while the codemap is empty or missing, a top-level module a maintainer would name; one level down, a unit's own parts.

Its sections, in this order:
- **Units**: one entry per unit the change adds or changes, marked new or changed: its responsibility in one sentence, what it owns, the units it depends on, for a changed interface the units that call it today, and its interface — the signatures and types other units call, in a code block, and nothing else. One level down, the parts of at most two units: those that are new or carry the change's largest risk.
- **Paths**: at most three paths a request takes through the units, as numbered steps, each naming a unit and a call in its interface, with a failure branch where the path turns. The first path is the walking skeleton: it runs from an entry a user or caller triggers to an end someone can observe.
- **Invariants**: the rules between units the change relies on or introduces, written as absences. Each invariant of `docs/architecture.md` a path crosses is named, as kept or changed.
- **Architecture changes**: the entries of `docs/architecture.md` the plan adds, modifies, or removes, as final text under `ADDED`, `MODIFIED`, and `REMOVED`, the way a spec change file proposes requirements: MODIFIED and REMOVED name an existing entry, and a REMOVED entry gives its reason. Only top-level entries enter; a part one level down never does.

The inclusion test for every entry: if the units on either side were built independently, could they choose incompatibly? Yes: it belongs in the skeleton. No: it belongs in the design or only in the code. Bodies, algorithms, file trees, fields no other unit reads, and UI stay out. Why the structure is this one, and the alternatives turned down, are the design's Decisions.

**Budget**: 300 lines, three paths, and two units refined one level down. `skeleton-review` counts them.

**Design**

Written only when the change has a skeleton, is cross-cutting, adds a dependency or changes the data model, carries security, performance, or migration complexity, or has ambiguity worth settling before coding.

- Up to 100 lines, it is `plan.md`'s `## Design` section.
- Longer, it is `design.md`, and `plan.md`'s Design section is one line pointing to it.
- A design file past 800 lines is split into `design/<topic>.md`, one file per topic, with `design.md` as the index: each file and one line on what it settles. Decisions, Risks, and Open questions stay in `design.md`.

Its sections, each used only when the change calls for it:
- **Overview** (`design.md` only): one page on scope, delivery, and the largest risks.
- **Flows**: the steps and failure branches inside a unit, below the skeleton's paths.
- **External contracts**: what each interface is used for and the fields the client relies on, linking the full contract; then the assumptions the implementation makes that the contract does not state, each checkable at integration.
- **Migration**: mapping tables that implementation and tests check row by row.
- **UI details**: what the spec keeps out and the design file does not settle, written as differences from the current UI or from the design file.
- **Rollout**: gray release, fallbacks, and rollback.
- **Tracking**: events and fields whose values or meaning change.
- **Test scope**: the categories, combinations, accounts, and environments to cover. The checks themselves are tasks in the integration group.
- **Later phases**: only to explain why this plan is cut where it is. A later phase becomes its own plan when its turn comes.
- **Decisions**: each a choice a later reader would ask why about, with its reason and the alternative turned down. A choice the implementer makes in the code without a reviewer needing to see it is not a decision.
- **Risks**: `[risk] → mitigation`.
- **Open questions**, of two kinds:
  - Non-blocking: unknowns that can be answered later without changing the requirements, the approach, or the tasks.
  - Blocking: a question that would change them, whose answer lies outside the conversation (another team, product, a third party), assigned by the user to an owner. Written as `Blocking, <latest answer date>: <question> — <owner> — <what it affects>` and listed first. Each task that depends on one names it.

  A question the user can answer is asked, not recorded.

**What stays out of `plan.md` and the design.** Each has a home elsewhere, and a copy goes stale over a plan's life:
- Rules a spec states: name the spec and the requirement.
- Structure the skeleton or `docs/architecture.md` states: name the unit.
- Fields and values copied from another authoritative source, such as an interface contract, a design file, or a data table: link it.
- Line numbers in the code: name the symbol.
- Conventions that hold across the repo: they belong in the instruction file.

**Budget.** Why holds at most two sentences and five bullets. The skeleton stays within its own budget, an inline Design holds at most 100 lines, and a design file at most 800 before it splits. What changes, Out of scope, and Tasks have no line count: What changes grows with the requirements it names, which the spec budget bounds. `verify` lists a plan over its budget and each line that belongs elsewhere.

**Spec change files — `specs/[<area>/]<feature>.md`**

One file per affected spec, at the same path under the plan's `specs/` as its target under `docs/specs/`: `docs/plans/<slug>/specs/quick-buy/entry.md` proposes changes to `docs/specs/quick-buy/entry.md`. Requirements and scenarios use the same heading levels and wording rules as a spec, so a block moves between the two unchanged.

- The `Type:` line and `## Purpose`: present only when the target spec does not exist yet.
- `## ADDED Requirements`: new requirements, complete with scenarios.
- `## MODIFIED Requirements`: the full updated requirement block under its existing name. The name is the handle that locates the requirement in the spec.
- `## REMOVED Requirements`: the requirement's heading followed by `**Reason**:`.
- A rename is a REMOVED entry for the old name and an ADDED entry for the new one.
- The file is written against the merged budget: the target spec's requirements plus ADDED minus REMOVED fit the spec budget, or the file carries the REMOVED entries that make it fit, each with its reason. A requirement that leaves the spec for the tests is a REMOVED entry whose reason says so.

A plan with no behavior change (refactor, tooling) has no `specs/` directory and touches no spec.

**Attachments**

Any other file in the plan directory is an attachment: a review page rendered for stakeholders, a schedule and workload breakdown, an asset the design cannot hold as text. Each is linked from `plan.md` or the design. An attachment states no requirement or design decision that the markdown does not; where the two disagree, the markdown is right and the attachment is corrected or regenerated.

The plan is edited as understanding changes during implementation. `plan.md`, the skeleton, the design, the spec change files, and the attachments are kept consistent, with changes flowing as How plan, skeleton, design, and spec relate describes.

### Archive — `docs/archive/YYYY-MM-DD-<slug>/`

A shipped plan's directory, moved and dated with the day it was archived. It holds everything except the spec change files and the skeleton's Architecture changes: `plan.md`, the skeleton, the design, and the attachments. Together they record why the feature was built, what was left out, the structure it was built on, how it was built and the alternatives turned down, and the tasks as they were carried out.

The spec change files stay out of the archive. After the merge their content lives in `docs/specs/`, and the change each one made is in the git history of its target spec, in the commit that lands the plan on the default branch under any merge strategy. The one part a spec diff cannot show, the reason a requirement was removed, is kept in `plan.md`'s What changes. Kept, they would add several files per shipped plan and leave stale copies of requirements beside the contract, where a search finds them. Earlier plans on a feature are found by the spec's name in their `Specs:` list. The skeleton's Architecture changes leave for the same reason: their content lives in `docs/architecture.md` and its git history.

An archived plan is history. Its files stay as they were at archive time and carry no authority over behavior or structure; the spec and `docs/architecture.md` are in force.

### Decision — `docs/decisions/NNNN-slug.md`

One decision per file, one to three pages. Numbers are sequential and never reused; the next number is one past the highest in `docs/decisions/` and `docs/decisions/superseded/` together.

The directory states the status:
- `docs/decisions/` holds the live set: records with `Status: Accepted`, which are in force, and records with `Status: Rejected`, which stay so the approach is not proposed again.
- `docs/decisions/superseded/` holds history: a replaced record, moved with `git mv` under its own number and file name, its status line reading `Superseded by NNNN`. It is read only to trace why a decision changed.

A record is written once the user has decided. A choice still under discussion lives in the conversation or in a plan's design.

**Published records.** A record is published once it is on the repo's default branch, where other branches and downstream readers can cite it. Before that it belongs to the branch that adds it: it is edited in place, renumbered when another branch published the same number first, or deleted when the decision is dropped. A published record's body is fixed; changing the decision means a new record that supersedes it.

**Superseding.** The new record restates everything still in force from the records it replaces, so the live set reads complete without opening `superseded/`, and names them on its `Supersedes:` line, a line other records omit. A record that is partly outdated is superseded whole, with its still-valid part carried forward.

**Consolidation.** The live set grows with the number of topics, not with time. A topic is a set of records a reader would need together to apply any one of them. Write one consolidated record that supersedes the others when a topic holds three or more live records, or when an Accepted record is partly outdated. It carries the parts still in force, leaves out what is outdated, and may fold the topic's `Rejected` records into its Considered options, each with its reason. It restates decisions that already passed the decision gate; the gate is not reapplied.

**Budget.** The live set stays small enough to read in one sitting: about 20–30 records. A larger set signals that consolidation is due; it is not a hard limit.

Decision gate — write a record only when all three hold:
1. Hard to reverse.
2. Surprising without context: a future reader would wonder why.
3. A real trade-off: genuine alternatives existed.

## Abandoned plans

An abandoned plan's directory is deleted, not archived: the archive holds plans that produced a shipped feature. The deleted text remains in git history.

What outlives an abandoned plan is the reason it was dropped, and only when that reason is durable:
- A lasting product boundary becomes one line in the overview's Non-goals.
- A technical approach rejected for reasons that will still hold later becomes a decision record with `Status: Rejected` (through `decide`, subject to the decision gate).

A plan dropped for lack of time or interest leaves nothing behind. Ask the user which case applies; record their reason, not an inferred one.

## Stops

An operation runs through to its end and stops only where nothing can move without the user. Each operation's file lists its stops and the pauses that do not belong to it. In every operation, ending the turn with a summary that announces the next step instead of taking it is not a stop. A status note goes in the same message as the next action.

## Boundaries

- Commit or push only when the user asks.
- The body of a published decision record and the contents of `docs/archive/` and `docs/decisions/superseded/` are left as written; superseding changes only the replaced record's location and status line.
- A directory the conventions block does not name is outside this skill's remit.
- Report every file created, moved, edited, or deleted at the end of an operation.

## Templates

### Spec

```markdown
# <Feature>
Type: feature | api | format

## Purpose

## Fields
| Field | Type | Default | When invalid |
|---|---|---|---|

## Requirements

### Requirement: <name>
The system SHALL <one rule>.

#### Scenario: <name>
- **WHEN** <condition>
- **THEN** <expected outcome>
```

`## Fields` appears in a `format` spec only. A scenario appears only where the rule would be misread without it.
