---
name: prd-to-issues
description: "Primary pipeline decomposition step after /write-a-prd. Use when a shaped PRD is ready to become implementation-ready slices with boundary maps and dependency order. Not for unresolved scope, appetite, or solution direction."
sources:
  primary:
    - "The Pragmatic Programmer — Andrew Hunt & David Thomas"
  secondary:
    - "Designing Web APIs — Jin, Sahni, Shevat"
    - "Software Estimation — Steve McConnell"
    - "Software Requirements — Karl Wiegers & Joy Beatty"
    - "Living Documentation — Cyrille Martraire"
    - "The Programmer's Brain — Felienne Hermans"
    - "Writing Effective Use Cases — Alistair Cockburn"
---

# PRD to Issues

Break a PRD into independently-grabbable GitHub issues using vertical slices (tracer bullets).

## Invocation Position

This is a primary pipeline skill that normally follows `/write-a-prd` and precedes `/execute`.

Use `/prd-to-issues` when a PRD is already shaped and you need implementation-ready slices with clear contracts between them.

Do not use it as a substitute for shaping. If the PRD is still changing at the level of solution direction, rabbit holes, or appetite, go back to `/write-a-prd` first.

## Process

### 1. Locate the PRD

Ask the user for the PRD GitHub issue number (or URL).

If the PRD is not already in your context window, fetch it with `gh issue view <number>` (with comments).

**Check for milestone.** After fetching the PRD, check whether it belongs to a GitHub milestone: `gh issue view <number> --json milestone`. If a milestone exists, note the milestone title for use in Step 6 — all slice issues should be attached to the same milestone.

### 2. Explore the Codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Draft Vertical Slices

Break the PRD into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- The first slice is the tracer bullet — it must prove the core architecture connects end-to-end with production-quality code before subsequent slices proceed. Subsequent slices adjust aim based on what the first slice reveals.
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Order the first slice to validate architecture, then remaining slices by risk
</vertical-slice-rules>

<wide-refactor-branch>
**When no vertical slice can land green — expand–contract.** The tracer-bullet rules above assume a thin slice can cut every layer and still pass CI. One class defeats that: a mechanical change whose blast radius breaks call sites repo-wide — renaming a widely-imported symbol, changing a shared signature, swapping a serialization format — where any partial change leaves the tree red. Do not force a tracer bullet here; decompose the refactor along the expand–contract sequence instead:

1. **Expand** — introduce the new form *beside* the old one. Nothing is removed yet, so CI stays green. One slice.
2. **Migrate** — move call sites to the new form in blast-radius-sized batches, each batch its own slice, each leaving CI green. Size batches for reviewability (§6's >500 LOC / >20 files signal), not for speed.
3. **Contract** — remove the old form once a grep confirms no call site still references it. One slice, ordered last in the dependency graph.

Each step is still a complete, verifiable slice — the seam it cuts is the migration boundary, not an end-user feature, so "demoable on its own" reads as "CI is green after this slice and the old and new forms coexist without conflict." This branch *adds to* the tracer-bullet path rather than replacing it: reach for it only when the default thin-slice decomposition would force a red tree, and state in the §9 decomposition summary why a tracer bullet could not land end-to-end here.
</wide-refactor-branch>

Always create a final QA issue with a detailed manual QA plan for all items that require human verification. This QA issue should be the last item in the dependency graph, blocked by all other slices. It should be HITL.

Because it is blocked by *every* other slice, the QA issue carries the largest fan-in edge set in any decomposition — and it is the one most likely to be under-wired by hand. §7's dependency-wiring step covers it explicitly: one edge per blocking slice, counted against the slice list. A QA issue with missing edges reports itself as takeable while implementation slices are still open.

### 4. Draft the Boundary Map

Before presenting slices to the user, draft a boundary map showing what each slice produces and what it consumes from upstream slices. This forces interface thinking before implementation and ensures slices actually connect.

Boundary maps are API contracts, not just dependency inventories — if a slice produces something another slice depends on, specify enough contract shape that downstream work will not invent incompatible assumptions.

For each slice, specify:

- **Produces:** The concrete outputs — exported functions, types/interfaces, API endpoints, database tables, UI components. Include file paths and function signatures where possible.
- **Consumes from #N:** What this slice needs from upstream slices — specific imports, API endpoints it calls, types it uses. Reference the producing slice by number. If the parent PRD's research lives in a `research`-labeled spike issue (see `/research` Phase 5d), you may also cite `Refs #<spike-issue-number>` here when the slice's interface decisions are bounded by a specific recommendation, callback contract, or version snapshot recorded in that spike. The `Refs #N` lineage syntax is the same one used elsewhere in the pipeline.
- **Contract notes:** The success shape, error shape, compatibility posture, and any versioning readiness concerns that matter to downstream consumers.

**Contract-shape rendering.** When the parent PRD locks a schema, type alias, function signature, or structured input/output shape in code form (per `/write-a-prd`'s Implementation Decisions guidance), the slice's `Produces` field should reference it by location rather than re-render it. Re-render only when the slice introduces a contract shape the PRD did not lock. This keeps the PRD as the single source of truth for locked contracts and avoids drift between two surface forms of the same artifact.

**On the Consumes side**, the same principle applies in mirror: when a slice consumes a contract shape produced by a sibling slice in a typed language (TypeScript, Rust, Python-with-stubs), the slice's `Consumes` field should **name the symbol and its location** — e.g. "From #N: `RunEvalResult` exported by `src/evals/run-experiment.ts`" — rather than re-render the shape in prose. The implementing agent then derives the consumer-side type via `import type` (or the equivalent), and the type system enforces N=1 between producer and consumer at compile time. The carve-out is cross-language Consumes — when the consumer cannot import the producer's type (e.g. a workflow YAML consuming a TS-defined constant), name the shared identifier and treat the prose as the contract; downstream review (`/pre-merge`'s Deep Modules dimension) is the safety net there.

Example — when the PRD's Implementation Decisions block locks a Drizzle schema:

```ts
// PRD #<prd-issue-number> §Implementation Decisions
export const dramaAssessments = sqliteTable("drama_assessments", {
  id: integer().primaryKey({ autoIncrement: true }),
  meetingId: integer("meeting_id").notNull().references(() => meetings.id),
  level: text().notNull(), // "routine" | "bumpy" | "heated" | "off-the-rails"
  confidence: real().notNull(),
  promptVersion: text("prompt_version").notNull(),
  model: text().notNull(),
  headline: text().notNull(),
  narrative: text().notNull(),
  evidenceQuotes: text("evidence_quotes", { mode: "json" }).$type<string[]>().notNull(),
  publishedAt: integer("published_at", { mode: "timestamp" }),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull().default(sql`(unixepoch())`),
}, (t) => [uniqueIndex("drama_assessments_meeting_prompt_model_unique").on(t.meetingId, t.promptVersion, t.model)]);
```

…the slice's `Produces` should read:

> - `src/db/schema.ts` — adds `dramaAssessments` and `dramaCategoryScores` tables per PRD #<prd-issue-number> §Implementation Decisions. No re-render here; consume the PRD's contract shape verbatim.

If the slice introduces additional types not locked by the PRD (e.g. an internal `DramaLevel` union the schema's `level` column will be narrowed to in TS), render those in the slice's `Produces` as the slice is the owning home.

The boundary map prevents the most common multi-slice failure: slices that are each internally correct but don't actually wire together because they made incompatible assumptions about interfaces.

**Orthogonality test:** After drafting the boundary map, check each slice: if this slice's internal implementation changed entirely, would any other slice need to change? If yes, the boundary is drawn wrong — either merge the coupled slices, or extract the shared concern into its own slice. Slices that pass this test can be implemented in any order by Ralph without risk of one slice's decisions breaking another.

**Scope completeness check:** After the orthogonality test, verify each slice's Produces list accounts for the full scope of that slice — not just the happy path. For each slice, check:

- Does it include error handling paths (not just success)?
- Does it include loading/empty/partial states (for UI slices)?
- Does it account for edge cases named in the PRD's Rabbit Holes section?
- Does the Produces list include all type exports that downstream slices consume?

If a forgotten deliverable surfaces, either add it to the current slice's Produces or create a new slice for it. Don't leave it as an implicit assumption — unscoped work is invisible to Ralph.

**Consumes plausibility check:** For each `Consumes` entry that references an already-closed upstream slice — not a sibling slice still being planned in this PRD — verify the claimed symbol exists at the declared path *before* finalizing this slice's boundary map. This catches upstream boundary-map drift during planning instead of execution.

For each such Consumes entry:

- Check the declared file path exists.
- Grep for the named export.
- If the declaration includes a shape (e.g. "Layer", "Zod schema", "React component"), confirm the export actually matches that shape, not just the name.

If a gap is found, don't just document it in this slice's `Consumes`. File a post-hoc correction comment on the upstream closed issue and note the correction in this slice's "Assumptions from Parent PRD" section as a verified check.

**Estimate-readiness check:** After the scope completeness check, verify that the decomposition made the work more legible rather than more performative. For each slice, ask:

- Is this slice small enough that its uncertainty can be explained in one or two sentences?
- Does the slice expose observable outputs and interfaces, or is it still hiding unknowns behind vague labels?
- If the decomposition revealed materially more work than the PRD implied, should the plan be reshaped or re-estimated before issue creation?

Do not force detailed schedule estimates into each issue. The goal is to surface slices that are still too ambiguous for credible commitment.

**Shape-sufficiency check.** For each new contract this slice introduces in `Produces` (Zod schema, exported type or interface, function signature, storage method parameter shape, server-function return type), confirm the *shape* is rendered as code in the issue body, not just the *name* listed. If only the name appears, render the shape inline before finalizing the boundary map.

The audit is binary: shape present or absent. Shape correctness is evaluated at the §6 Quiz step; shape presence is the prerequisite that lets the Quiz step do its job.

This check exists because PRDs frequently sketch contract shapes in prose without locking them in code form (e.g., "exports a Zod schema with category_scores keyed by …"). The Contract-shape rendering subsection above covers two cases — PRD locked in code (reference by location) and slice introduces a contract the PRD did not lock (re-render). The third case — PRD sketched in prose without locking in code — is where this check fires when the rule's "did not lock" wording is read narrowly. The slice issue is the durable contract `/execute` and `/pre-merge` inherit; the shape lives in code form in the slice's `Produces` regardless of the PRD's surface form for it.

**Context completeness check (AFK slices only).** After the shape-sufficiency check, confirm each slice marked AFK carries the pointers a cold reader needs — or explicitly declares them empty. HITL slices are exempt; they have a human in the loop to ask.

An AFK slice hands a fresh context window a task requiring search, comprehension, and transcription at once — the costliest kind to leave undecomposed (Hermans, *The Programmer's Brain* Ch. 11). This session already did the search, in §2. Write it down so the fresh window pays only comprehension and transcription. That is also the admission test for the block: a line earns its place only if it removes a search the implementer would otherwise run. "Useful background" does not qualify.

The audit is binary — pointer present or absent — for the same reason the shape-sufficiency check is: the author cannot grade their own clarity. Experts' estimates of novice difficulty do not improve even when they are prompted to recall being novices (Hinds 1999), because automatization erases the memory of what each step cost (Hermans Ch. 13). Presence is checkable; "does this feel legible?" is not.

Each AFK slice's `### Context` block must contain, or explicitly declare empty:

- **Anchors** — existing files to read or imitate, as `path — why`, or the line `Greenfield — no existing pattern to follow.` The anchor is a **path**, never a bare pattern name: "follow the repository pattern" helps only a reader who already recognizes it, while a path is readable by anyone. The `why` states the file's **purpose, or the pattern it exemplifies** ("owns the retry/backoff policy every outbound client uses") — never a line-level restatement, which gives the reader nothing to chunk against and is pure load (Fan 2010). Where the repo has an `UBIQUITOUS_LANGUAGE.md` and this slice leans on domain terms defined there, cite it as one more anchor.
- **Gotchas** — constraints known now that bear on this slice, drawn from the PRD's Rabbit Holes and the research artifact, or `None known.`
- **Research** — the research artifact's location (`Refs #<spike-issue-number>` or the archive path), cited in this slice so `/execute` need not walk the parent PRD to find it. Check an archive path with the bundled [references/sidecar.sh](references/sidecar.sh) `require <path> --from "PRD #<n>"` before citing it, and surface a `MISSING:` line instead of filing a dangling pointer.

These three labels are rendered verbatim in the `### Context` block of the issue template below. `scripts/test-context-block-contract.sh` pins the two lists against each other — changing a slot here without changing the template (or the reverse) fails the suite rather than shipping a check that asks for a field the template has no room for.

Pointers, not restatements — the code and the research artifact stay the truth; the block only says where to look. Slice size is a separate concern, already covered by the orthogonality and estimate-readiness checks above.

**Sunset clause for the context check.** It was added on audit grounds, without a triggering incident. If across a reasonable sample of AFK decompositions the block is consistently greenfield/none-known filler, or `/execute` iterations are observed skipping it despite its Step 1 instruction, remove it rather than leave it as ceremony — support that is never acted on becomes clutter, and clutter trains readers to skip the region it sits in (Hermans Ch. 11).

**Dependency-graph diagram (optional).** Before finalizing the boundary map, if it has ≥2 Produces/Consumes entries across the decomposition, consider invoking `/mermaid` to render the cross-slice dependency graph as a flowchart and embed it alongside the existing lists. The lists stay authoritative — the diagram is a reading aid for reviewers and resumed-session agents who otherwise have to mentally compile the bullet structure back into a graph. Skip the diagram when the boundary map is thin enough that the lists are already the cleanest rendering.

Once the issues exist and §7 has wired native dependency edges, a regenerated version of this diagram can be derived from the API rather than hand-transcribed from the boundary map — read each slice's `.../dependencies/blocked_by` list and render the edges directly. Deriving it removes the transcription step, which is the step that lets the diagram drift from the real graph.

### 5. Derive the Coverage Matrix

**Skip this step when the PRD decomposes into a single slice.** For single-slice PRDs the boundary map + user-stories-covered field already serve as coverage; a matrix would be pure ceremony.

For multi-slice PRDs, derive a requirement-to-slice coverage view from the PRD's existing user stories. This is a **derived view**, not a hand-maintained spec — its single source of truth is the PRD issue body. You regenerate the view from the PRD; you never edit the view directly.

For each user story in the PRD, classify and map it:

| PRD commitment | Classification | Covered by |
|----------------|----------------|------------|
| User story 1 ("As a user, I want X so that Y") | **Must** | Slice #2, Slice #4 |
| User story 2 ("As a user, I want Z so that W") | Want | Slice #3 |
| User story 3 ("As a user, I want Q so that R") | ~Tilde | — (consciously cut) |

- **Must** — comes from the PRD's *Must-haves* section. Every Must needs at least one covering slice before issue creation.
- **Want** — comes from the PRD's *Nice-to-haves (~)* section. Unmapped Wants are acceptable but get surfaced as a warning at the Quiz step.
- **~Tilde** — a Nice-to-have the user is consciously cutting under the appetite. No coverage required; silent.

**Coverage means the whole story, not the want clause.** An As-a/I-want/So-that sentence is three requirements on one line, so matching a slice against the middle clause certifies the middle clause and nothing else. Wiegers (Ch. 29) is exact about why that is not traceability: a requirement is traceable only when it has *"fine enough granularity to be linked unambiguously,"* and *"a large paragraph containing multiple requirements is untraceable regardless of how many link records exist."* Three slices listed against a story you only half-checked is three link records that pin to nothing. Test all three clauses before marking a Must covered:

- **Actor clause — name what guarantees the precondition: a slice in this PRD, or the existing system.** The actor clause usually carries one: something the system must ensure is true *before* this actor can begin. Cockburn's definition is the test — a precondition is *"what the system will ensure is true before letting the use case start,"* not a condition that merely tends to hold for typical users. Ask what guarantees it. Three answers, not two: a slice in this PRD guarantees it — covered. The pre-existing system already guarantees it and no slice here needs to re-deliver it — also covered; "As a logged-in user" names a precondition the already-shipped login system satisfies, and re-delivering it is not this PRD's job. That second answer is only honest when you can name the specific pre-existing mechanism doing the guaranteeing — not merely that the precondition usually holds for typical users, which is the same false-typical-for-guaranteed confusion Cockburn's definition rules out above, now applied to the existing system instead of a slice. Otherwise, if the honest answer is "the actor arranges it themselves" — nothing in this PRD and nothing already shipped actually guarantees it — the clause has been rewritten and the Must is **unmapped**.
- **Actor clause — check who the slices actually serve.** Separate the story's actor from whoever operates the interface. Cockburn's *ultimate primary actor* is the one who cares about the outcome, and collapsing the two misdirects the build: a use case named for the clerk *"gets built around clerk convenience instead of the customer's actual need."* Slices that serve only the operator do not cover a story written for the recipient, and the Must is **unmapped**.
- **Want clause — the mechanism.** The match this step already performed.
- **So-that clause — invert it.** Ask what would make this actor unhappy at the end of a *successful* run, then check whether the answer is already true of the planned slices. If it is, the Must is **unmapped** however well the want clause matches.

**Where flow rows exist under a Must, map at affordance granularity.** `/write-a-prd` attaches place/affordance rows to the Must-have story each realizes, so a Must carrying rows is covered only when the rows are, not merely when the sentence is. A row may sit under several Musts, and the PRD's unattributed residue (shared chrome, loading states) is not a commitment — do not treat an unattributed row as an unmapped Must.

**A PRD with a standalone `## Flow Sketch` section still parses — read it, do not reject it.** PRDs authored before the rows moved under their stories carry the section instead, and an in-flight PRD is not a malformed one. Read its rows as belonging to the Musts they plainly realize, and where a row's parent is genuinely ambiguous, raise it at the Quiz step rather than guessing. The relocation changed where an author puts a row, not whether this step reads it.

**This is not prose scanning.** Nothing here makes a §Solution sentence coverage-bearing, and no PRD is asked for content it does not already have. Flow rows are a bounded enumeration of places and affordances the author already wrote — the derivation reads them wherever the PRD puts them, and otherwise tests more of the one sentence it was already reading. Shape Up's roughness discipline is intact: the fix for a noisy matrix is still PRD refinement, never PRD restructuring to feed the matrix.

**Unmapped-Must backpressure.** Before proceeding to the Quiz step, halt if any Must is unmapped. Surface the list of unmapped Musts to the user and ask whether to (a) add a new slice covering them, (b) extend an existing slice to cover them, or (c) demote the commitment in the PRD (edit the PRD issue body, then regenerate this view). Do not create slice issues with unmapped Musts.

**Matrix-generation difficulty is a PRD-quality signal.** If many commitments resist clean classification or mapping — several Musts that could plausibly belong to any of three slices, or several items that feel like they are neither Must nor Want — *report this to the user*, do not push structure back into the PRD. Per Shape Up's roughness discipline, PRDs stay rough; matrix noise is the signal that the PRD is under-specified in one area, and the fix is PRD refinement (or accepting the rough classification), not PRD restructuring to feed the matrix.

### 6. Quiz the User

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories from the PRD this addresses
- **Produces**: key outputs from the boundary map
- **Consumes**: key inputs from upstream slices

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?
- Do the boundary map interfaces look right? (Are these the right function signatures, types, endpoints?)
- Does every shared type, endpoint, or data model have exactly one owning slice in the Produces column?
- For each AFK slice: if a fresh session knew nothing beyond this issue body and its links, would it have everything needed — anchor files, gotchas, research pointer? (This is the condition `/execute` names for AFK safety, and you are the only reader here who is not already holding the context.)
- For every `Consumes` entry that references an already-closed upstream slice: does the symbol actually exist at the declared path, in the declared shape?
- Does the total decomposition feel proportionate to the stated appetite? A small-batch appetite (1-2 weeks) with 10+ slices or 4+ dependency levels suggests scope grew beyond what was shaped. A big-batch appetite with only 2-3 trivial slices suggests the shaping was too aggressive. If the decomposition feels disproportionate, which slices should be merged, split, or cut?
- Does any non-tracer slice project to **>500 LOC or >20 files** at ship time? If so, can it split without breaking the vertical seam? Tracer bullets are exempt — they intentionally cut wide to prove end-to-end architecture. (Soft signal sourced from convergent code-review research: Tacke's engagement-degradation thresholds (≤500 lines / ≤20 files) and Rigby's 11–78 LOC convergent median across 13 projects (Microsoft, AMD, Android, Chrome OS, Apache, Linux). The mirror size signal at review time is `/pre-merge`'s Review-friendly Size dimension.)
- Did decomposition reveal any slice whose uncertainty is still too high for a credible commitment? If so, should it be split further, converted into a tracer bullet, or pushed back into PRD shaping?

- If the decomposition reveals the PRD needs reshaping — total scope materially exceeds the appetite, or a fundamental assumption is wrong — backtrack to `/write-a-prd`. If backtracking, close or comment on any already-created slice issues to mark them as superseded, and note in the PRD issue that it is being reshaped. Do not leave stale slice issues open for `/execute` to trust, whether they are being worked HITL or via Ralph's AFK loop.

Iterate until the user approves the breakdown.

### 7. Create the GitHub Issues

For each approved slice, create a GitHub issue using `gh issue create`. Use the issue body template below.

**Milestone propagation.** If the parent PRD belongs to a GitHub milestone (detected in Step 1), add `--milestone "<Milestone Name>"` to each `gh issue create` command so all slice issues are attached to the same milestone.

Create issues in dependency order (blockers first) so you can reference real issue numbers in the "Blocked by" field.

**Then wire each blocking relationship as a native GitHub issue dependency.** The create-then-reference structure above already gives you a second pass over the graph once real issue numbers exist; that pass now also POSTs one edge per `Blocked by` entry.

Both representations are written, and they have distinct jobs. The prose `## Blocked by` line documents *why* a slice is gated, is readable without API access, and survives a tracker migration. The native edge is the **gate**: it is what `/help`, `/execute`, and Ralph query to decide what is takeable, and it is authoritative for any automated selection. Writing only the prose leaves every downstream consumer parsing English to reconstruct a graph that GitHub can serve directly.

Wire each edge with `gh issue edit`, which takes issue **numbers** and accepts several blockers per call:

```bash
gh issue edit <blocked-number> --add-blocked-by <blocker-number>,<blocker-number>
```

Wire the §3 QA issue last and count its edges against the slice list — it is blocked by every other slice, so it is where a missed edge is least visible.

⚠️ **Never pass `--blocked-by` (or `--parent`, or `--type`) to `gh issue create`.** `create` applies relationships as a *deferred second mutation* after the issue exists. When that mutation fails — permissions, a feature unavailable on the host, GHES below the floor — `gh` reports the error, **suppresses the issue URL**, and offers a `--recover` prompt. The issue was still created, so an agent that follows the prompt files a **duplicate**. Creating bare and wiring in a second pass keeps a relationship failure isolated and retryable, which is why the create-then-reference structure above is load-bearing rather than incidental. (Verified live in `gh` 2.97.0; the fix, [cli/cli#13899](https://github.com/cli/cli/pull/13899), is open and unmerged.)

**Verify by reading the edges back, not the summary.** The `issue_dependencies_summary` counts can be served stale immediately after a mutation — a removed edge may still report `blocked_by: 1` for a short window. Confirm what you wrote by reading the edges themselves:

```bash
gh issue view <blocked-number> --json blockedBy \
  --jq '[.blockedBy.nodes[] | {number, state}]'
```

Each node carries `{id, number, state, title, url}`, and `state` is the GraphQL enum — **uppercase** `OPEN` / `CLOSED`, not the REST endpoint's lowercase. `blockedBy.totalCount` counts blockers in *every* state, so it is the CLI's equivalent of `total_blocked_by`.

**Reconcile the two representations before moving on.** Naming the edge authoritative settles *who wins* a disagreement; it does not stop one from happening. Because the prose line and the edge set encode the same fact — which issues gate this one — that fact is redundant, and redundant knowledge needs a divergence check rather than a declaration of authority (Martraire, *Living Documentation* Ch. 3: for unavoidably redundant knowledge, establish a reconciliation mechanism; Hunt & Thomas on DRY: "it isn't a question of whether you'll remember, it's a question of when you'll forget").

The check is cheap and belongs here, at the one moment both representations are being written together: for each slice, compare the issue numbers in its prose `## Blocked by` line against the numbers returned by the dependency list above. They must be the same set. A prose entry with no edge is a gate the pipeline will not enforce; an edge with no prose entry is a gate no human can explain. Fix whichever is wrong before finalizing.

This is the only place the two can be reconciled cheaply. Downstream, `/help` and Ralph read the edges and never see the prose, so a divergence introduced later stays invisible until someone hand-reads an issue body.

Three properties of this API are worth stating plainly, because each is a sharp edge that otherwise gets rediscovered by a failing agent:

- **Open blockers and total blockers are different questions, and you usually want both.** A closed blocker stays on the edge list but stops gating. Filtering nodes to `state == "OPEN"` answers *"is this takeable now"*; `totalCount` answers *"was this ever wired"*. Together they separate *"had blockers, all closed"* (`totalCount > 0`, no open nodes) from *"never wired"* (`totalCount == 0`) — a distinction downstream readers need, and one that reading open-blockers alone collapses. Closing a blocker un-gates its dependents with no bookkeeping, which is exactly what the prose line never does for itself.
- **`state` is uppercase on the CLI and lowercase on REST.** `--json blockedBy` returns the GraphQL enum (`OPEN` / `CLOSED`); `gh api …/dependencies/blocked_by` returns `open` / `closed`. A `jq` filter copied between the two silently matches nothing.
- **If you do drop to raw REST, two traps apply.** `GET /repos/{owner}/{repo}/issues` returns pull requests alongside issues, so it needs `select(has("pull_request") | not)` or a PR can surface as a takeable slice. And the summary objects (`issue_dependencies_summary`, `sub_issues_summary`) are served only by that *list* endpoint — they are **absent** from the single-issue `GET`, which yields null regardless of the real state and reads as "no dependencies" rather than as an error. `gh issue list` / `gh issue view` avoid both: the former excludes PRs by definition, and neither depends on the summary objects.

**Prefer the `gh` CLI over hand-rolled REST for this graph.** `gh` ≥ 2.94.0 exposes the whole relationship surface as flags and `--json` fields (see `README.md` § Installation for the version floor). `--json blockedBy,blocking,parent,subIssues` all work — the field that errors with `Unknown JSON field` is `isBlocked`, which does not exist and is easily mistaken for evidence that the whole family is unavailable.

<issue-template>
## Parent PRD

#<prd-issue-number>

## What to Build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation. Reference specific sections of the parent PRD rather than duplicating content. The plain-language walkthrough of the feature lives in the parent PRD (see `references/writing-for-humans.md`); slice bodies stay contract-focused so they complement the PRD instead of restating it.

## Boundary Map

### Produces

What this slice creates that downstream slices depend on:

- `path/to/file.ts` → `functionName()`, `TypeName` (interface)
- `path/to/api/route.ts` → `POST /api/endpoint` (returns `ResponseType`)

### Consumes

What this slice needs from upstream slices:

- From #<issue-number>: `path/to/file.ts` → `importedFunction()`, `ImportedType`
- Refs #<spike-issue-number>: research spike pinning the recommended approach or library callback contract this slice's interface depends on (cite only when a spike issue exists for this PRD's research and the slice is bounded by a specific recommendation in it)

Or "Nothing — this is a leaf node (no upstream dependencies)." if no dependencies.

### Context

*AFK slices only — what a fresh context window needs so it does not have to re-derive this. Omit the whole subsection for HITL slices.*

- **Anchors:** `path/to/existing.ts` — owns the retry/backoff policy every outbound client uses; imitate its error shape
- **Anchors:** `UBIQUITOUS_LANGUAGE.md` — defines the domain terms this slice's `What to Build` leans on
- **Gotchas:** the upstream API rejects batches larger than 50 (PRD Rabbit Holes)
- **Research:** `Refs #<spike-issue-number>` — or the absolute archive path the PRD cites, copied verbatim

Use the explicit empty declarations rather than dropping a bullet: `Greenfield — no existing pattern to follow.` and `None known.`

## Acceptance Criteria

Mark policy-driven criteria with `[POLICY]` — these encode current business rules that may change independently of the feature logic.

Mark quality-attribute criteria with `[QA-<attribute>]` where `<attribute>` is one of `PERF`, `RELI`, `SEC`, `USAB`, `MAINT`. These criteria carry the SMART quality-attribute discipline forward from the parent PRD's §Implementation Decisions — each must be specific, measurable, attainable, relevant, and time-bounded. Name the verification mechanism (load test, fault-injection test, log-capture assertion, etc.) so `/pre-merge` can verify implementation reflects the declared criterion.

Write a criterion in EARS form — `<condition>, the <module> shall <response>` — when the trigger condition is what makes the criterion falsifiable: the behavior is condition-dependent (error path, guard, state-dependent flow), or the criterion protects a failure direction of a classifier. Three keywords cover what slices carry: `When <trigger>` for a point event, `While <state>` for behavior sustained across a state, and `If <condition>, then` for deviations and failures. Route a deviation through `If … then` even when the prose doesn't frame it as a failure — omitted failure handling is the defect that keyword pair exists to prevent. Put the real module name in the `<module>` slot (it is already in the Boundary Map), and stack at most two keywords; a criterion needing three is two criteria.

Plain prose remains the default. A criterion that fails all three triggers is unconditional, which is already the notation's unconditional form — inventing a condition to satisfy a template produces a worse criterion than the prose it replaced.

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] If the feed returns a malformed row, then the parser shall reject the row and log a structured error
- [ ] While a sync is in flight, the scheduler shall reject new sync requests
- [ ] `[POLICY]` Criterion that reflects a current business rule rather than a stable requirement
- [ ] `[QA-PERF]` p95 search latency under 200ms with 100 concurrent users, verified by load test in this slice

## Assumptions from Parent PRD

List the 3-5 key assumptions from the parent PRD that this slice depends on. Before starting execution, spend 60 seconds confirming each is still true. If any assumption has changed, this slice gets a targeted `/research` → mini-PRD cycle before proceeding. If all hold, execute directly.

**Caution — spike artifacts vs. spike verdicts.** If an assumption depends on a spike's captured *artifact* (recorded responses, sample payloads, challenge-page HTML, golden files the slice will commit as a fixture) rather than the spike's *verdict*, do not assert it is "still available" — `/prototype` deletes spikes by default, so the artifact is gone unless it was deliberately preserved (committed as a fixture or recorded as a re-capture recipe; see `/prototype` "Preserve reusable captured output"). Confirm the artifact was actually persisted before writing the assumption. If it was not, scope the slice to re-capture the artifact rather than asserting it persists — otherwise the assumption is false the moment it is written and only `/execute`'s Assumptions-validation gate catches it, late and mid-flight.

- [ ] [Assumption 1 — e.g., "Turso free tier still provides 5GB storage"]
- [ ] [Assumption 2 — e.g., "better-sqlite3 is still the Drizzle driver in use"]
- [ ] [Assumption 3 — e.g., "Vercel auto-detects TanStack Start"]

## Blocked by

- Blocked by #<issue-number> (if any)

Or "None — can start immediately" if no blockers.

This block is written for humans: it records which slices gate this one, and why where that is not obvious. It is not what automated selection reads — the native GitHub dependency edge wired alongside it is authoritative for any "is this takeable" decision. If the two disagree, the edge wins and the prose is the thing to correct.

## User Stories Addressed

Reference by number from the parent PRD:

- User story 3
- User story 7

</issue-template>

Do not close or modify the PRD *body*. A decomposition-linking comment on the parent PRD issue is allowed — and required (see next step).

### 8. Link decomposition on the parent PRD

After all slice issues are created, post a single comment on the parent PRD issue in the form:

```
Decomposed into: #<slice-1>, #<slice-2>, #<slice-3>
```

This comment is the signal downstream skills read to know the PRD has been decomposed. `/execute`'s issue-shape detection gate checks for it before accepting a PRD-shaped issue as a slice task.

If a PRD is re-decomposed later (e.g., after `/correct-course`), post a new `Decomposed into:` comment; readers consume the most recent one. Keeping only one authoritative comment is this skill's responsibility.

### 9. Summary

After all issues are created, present a summary showing:

- Total number of issues created
- Dependency graph (which issues block which)
- Suggested implementation order
- The boundary map across all slices (a quick-reference view of what flows between them)
- The Coverage Matrix (multi-slice PRDs only) — a quick-reference view of which PRD commitments each slice addresses
- If a milestone was used: "All N issues attached to milestone: [milestone name]"

This summary helps the user (and Ralph) understand the full picture before execution begins. The Coverage Matrix remains a derived view — future readers regenerate it from the PRD issue body and the slice issues' `User Stories Addressed` sections rather than reading a stored matrix file.

**At the end of the summary, print the runtime handoff line** naming the first unblocked slice. Compute it with a query rather than re-reading the issue bodies you just wrote — the edges wired in §7 are what make this a lookup:

```bash
# Scope to THIS decomposition's slice numbers. An unscoped repo-wide min will
# happily return some unrelated ancient open issue.
gh issue list --state open --limit 100 --json number,blockedBy \
  --jq '[.[]
        | select(IN(.number; 101,102,103,104))
        | select([.blockedBy.nodes[] | select(.state == "OPEN")] | length == 0)
        | .number] | min'
```

Substitute the real slice numbers for `101,102,103,104`. When several slices qualify, `min` takes the lowest-numbered one — the same tiebreak as before. `gh issue list` excludes pull requests by definition, so no `has("pull_request")` guard is needed here.

Because this reads the edges themselves rather than a summary count, it is not subject to the post-write staleness window — the reason the previous version of this step needed a second confirming call. Filtering on `state == "OPEN"` means a closed blocker correctly does not gate the pick. This step is the only place in the pipeline where a frontier read follows its own writes closely enough for staleness to have been a concern at all; `/help`, `/execute`, and Ralph read a graph written in an earlier session.

```
**Next session:** /execute #<first-unblocked-slice-number>
**Input:** the slice issue body
```

If the query returns `null` — every slice reports a nonzero `blocked_by` — surface the dependency cycle to the user before printing. Do not pick arbitrarily.

## Handoff

- **Expected input:** a shaped PRD issue with clear user stories, rabbit holes, and no-gos
- **Produces:** implementation-ready GitHub issues with dependency order, boundary maps, and milestone attachment when the parent PRD belongs to a milestone
- **Comes next by default:** `/execute` for implementation, with Ralph optionally running the AFK execution loop for unblocked slices
- **Feeds downstream:** `/pre-merge` uses the slice lineage and boundary maps to review plan-vs-actual code
