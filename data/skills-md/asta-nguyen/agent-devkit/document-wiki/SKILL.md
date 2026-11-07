---
name: document-wiki
description: Use when a task changes behavior that an existing wiki documents, or when a standalone wiki must be created or refreshed from current source.
---

# Document Wiki

Create or refresh the target repository's `docs/llm/` from verified source
code. This is the one-stop wiki workflow; do not hand the user off elsewhere.

## Completion contract

An inventory of routes, files, or modules is baseline coverage, not deep
feature documentation. A selected feature is complete only when its page
explains current business behavior and its material claims are traceable to
source or tests read in the current run. Mark `[ ]` an undocumented feature and
`[x]` a feature verified against that evidence. Use `[~]` for either a `verification limit` (checks remain incomplete
or required evidence is inaccessible; the page may be correct, so it is not a
refresh candidate) or a `confirmed content gap` (completed checks prove a
material omission or a claim that contradicts source; a refresh candidate). State
which one and why; they are not equivalent. Never call unverified coverage
current.

## Task updates

When implementation calls this skill for an active task, use this
procedure instead of the whole-wiki Workflow below. The task's scope selects its
affected behavior automatically; no extra page-selection approval is needed.
Standalone wiki requests use the Workflow and its selection gate.

1. If `docs/llm/` is absent, return `not-applicable` without setup or wiki
   creation. Otherwise apply Workflow step 1's instruction preflight, without its
   missing-wiki setup, and read the index and relevant pages. Use approved scope,
   the diff, and the current impact map/caller trace to select changed behavior,
   including callers outside the diff. Inventory or document no neighboring
   feature and create no repository-wide overview.
2. Merge any task delta with `## Merge a task delta` before other content edits,
   preserving its exact after-merge blocks. If a delta block itself needs
   correction, reconcile the delta and wiki together using source and approved
   decisions; unresolved conflicts stop the update. A merge marker alone never
   proves the merge is correct.
3. Read current source and relevant tests and use the evidence matrix and page
   template for the selected behavior. Refresh stale content and add missing task
   behavior to the smallest relevant page. If its domain has no page, create a
   scoped page and register its prefix per Workflow steps 7-8; source-established
   domain boundaries need no approval. Reuse existing IDs/prefixes, preserve
   unrelated content, and report unrelated gaps as optional suggestions. A new
   page documents this task's behavior, not its module's every feature.
4. Ask only for unresolved behavior, conflicting requirements/source, domain
   boundaries not established by evidence, missing access, or work beyond the
   task's scope. Missing evidence for required task behavior keeps the task
   incomplete; do not invent it or mark it complete with an open question.
5. Update Sources, index links, and retired IDs as applicable and run
   `## Verify the wiki`. Report any legacy-link migration conflict or scope issue.
   Verify each changed claim against source and tests: a validator pass or an
   Evidence path alone does not prove behavior.
6. Return changed pages, covered behavior, checks, and blockers to the caller.
   Never archive, mark task progress, or change approval here; implementation and
   final review own those actions.

## Convert a legacy target page

Use this when a design or bug fix must write a delta against a page that still
uses `## Business rules`. It runs before the delta is written; the task's named
affected page is its selection, and conversion needs no other approval because
it changes format, not behavior. Read `references/legacy-conversion.md` before
converting. If any existing rule cannot be verified against current source, mark
the page `[~]` as a `verification limit`, leave it unchanged, return the exact
missing evidence, and stop; the caller stops too. A rule contradicted by source
is a `confirmed content gap`: report it and do not silently fix it.

## Merge a task delta

Use this only when a delta exists and the code checks pass. Run in the task's
branch before final review. Read `references/merge-task-delta.md` before merging.
These rules always hold:
- Check without editing first. If any pre-check fails, stop without editing and
  return the failing item to the caller as a blocker.
- Decide the merge state per block, by content. Apply only blocks still before
  merge; when every block is already after merge, verify side effects and add the
  marker, and never apply the whole delta again.
- A `MODIFIED` or `REMOVED` wiki block that matches neither its `Baseline:` nor
  its after-merge text was changed by another branch: never overwrite or delete
  it. Stop, report the exact difference, and inspect decisions and source.
- Run `## Verify the wiki` before final review; a failure keeps the change open.

## Workflow

1. Resolve the target repository from the user's path or the current directory
   and read its root `AGENTS.md`. Compare its wiki-maintenance rules with this
   workflow. If `docs/llm/` exists, read only `docs/llm/AGENTS.md` next and
   compare its active instructions too, before opening other wiki pages. If
   either file requires reading or writing `LOG.md`, source commits, hashes, or
   snapshots, or otherwise conflicts with current-source verification, report the
   exact conflicting paths and lines. When the user has already explicitly chosen
   current-source verification without a log for this task, continue: do not read
   or write `LOG.md`, preserve the existing instructions, and report that they
   need an update. Without that decision, stop before setup, opening `LOG.md`, or
   modifying wiki pages, and ask the user to resolve the conflict. If `docs/llm/`
   is missing after this preflight, run `setup-codebase` inline and preserve every
   existing file. Link internal pages relative to the linking file; never link to
   process artifacts from `docs/llm/`.
2. Read `INDEX.md` and all existing wiki content pages. Treat the wiki as
   **empty** when it is missing, holds only the setup skeleton, or its pages still
   contain placeholder text such as `Populate this page`. Preserve a legacy
   `docs/llm/LOG.md` byte-for-byte; never open, read, or use it as evidence. In this pass,
   convert every resolvable legacy `[[...]]` link in `docs/llm/` to a relative
   Markdown link, even on pages not being refreshed. Resolve a target from the
   nearest ancestor containing `.obsidian/`, or from the `docs/llm/` root, confirm
   the exact file, and report missing or ambiguous targets; never claim migration
   complete while one remains. If the repository has no application source, report
   that no verified behavior exists, preserve the skeleton, and stop; never create
   pages from proposed specs or plans.
3. Build a domain map and feature list from behavior, not filenames: inspect
   routes, commands, scripts, workers/jobs, public APIs, manifests, tests, and
   README instructions, using the tool table in `read-codebase-context`. Search
   results are navigation; direct source is evidence. Group by product domain only
   when evidence establishes the boundary. Establish each user-visible behavior
   and entry point; trace end to end only the features selected in step 6.
4. Determine coverage before writing deep pages: compare every material claim on
   each existing page with current source and tests, and mark each feature `[ ]`,
   `[x]`, or `[~]` as `## Completion contract` defines. Continue all feasible
   checks first: an unchecked source or caller is not evidence of a content gap;
   the working tree, uncommitted changes included, is authoritative; file
   existence or Git history alone never establishes freshness, and a source
   change alone does not make an accurate page stale. Read
   `references/inventory-and-report.md` for the inventory format and checks.
5. Create or refresh the baseline map. If `architecture/overview.md` is missing,
   create it; refresh an existing one only when completed current-source checks
   confirm a gap or contradiction. If verification is blocked, keep the content,
   mark it `[~]` as a `verification limit`, and report the exact missing evidence.
   Write the smallest source-grounded page with the repository purpose, major
   entry points, a domain table, cross-domain dependencies, and `## Sources`, and
   link it from `INDEX.md` with every discovered domain. The map is automatic even
   for an empty wiki, but it is orientation, not permission to document every
   feature in depth.
6. Present `[ ]` undocumented features and `[~]` `confirmed content gap` features
   as selectable create/refresh candidates grouped by domain. Separately offer a
   `## Business rules` page as a `format conversion` candidate once a fresh source
   check confirms it is accurate. Do not offer `[~]` items whose only cause is a
   `verification limit` for rewriting or conversion. If a check is blocked,
   report the exact missing evidence and ask only for the access or information
   needed. Do not create or refresh deep pages until the user selects eligible
   candidates; a generic request to document the repository is not selection, even
   for an empty wiki. "All" selects every eligible candidate. Record selected and
   verification-limited items separately.
7. Group selected behavior into evidence-backed categories (see
   `references/inventory-and-report.md`). When documenting or refreshing a
   selected feature, read `references/evidence-matrix-and-page-template.md` before
   continuing.
8. Update `docs/llm/INDEX.md` with working links. When a page registers a new
   domain prefix, create or update the `## Requirement prefixes` table (`Prefix`,
   `Domain`): reuse the domain's existing prefix, and register a new one only when
   the table has no row for that domain. When a refresh removes or renames a
   requirement, append its ID to `## Retired requirement IDs`; a retired ID is
   never reused. Each page keeps its business content, requirements, and a
   `## Sources` section of exact source/test paths. Create no source log or
   snapshot; update `docs/llm/FEATURES.md` only if it already exists.

## Verify the wiki

Run
`node "<this-skill-directory>/scripts/validate-llm-wiki.mjs" "<target-repository-root>"`
with absolute paths after the wiki edits. It checks source paths, links and
anchors, legacy wikilinks, and requirement syntax (unique, sorted IDs, one
`SHALL`, scenarios, Evidence paths listed in Sources, registered prefixes, retired
IDs); do not repeat those checks by hand. If the script is missing, cannot run, or
reports errors, keep verification incomplete and report the failure. Also run
`git diff --check`, confirm every index link resolves, and confirm each
`Tests: none found` claim has a recorded search with no match.

The validator cannot judge these; check them yourself: no two requirements that
share a prefix describe the same behavior, and each requirement's Evidence
actually supports its `SHALL` statement. Convert a refreshed legacy
`## Business rules` page per `references/evidence-matrix-and-page-template.md`
and record any dropped ID as retired. For a confirmed omission or contradiction,
mark `[~]` as `confirmed content gap` and report the source evidence. For an
incomplete or blocked check, mark `[~]` as `verification limit`, name the exact
missing evidence, and do not offer a rewrite. Never silently repair claims or
report unverified coverage as current. The final report follows
`references/inventory-and-report.md`'s `## Final report`.

Do not modify application code, install dependencies, or invent architecture.
`docs/llm/` describes only verified current behavior grounded in source and
tests, never proposed specs or plans.
