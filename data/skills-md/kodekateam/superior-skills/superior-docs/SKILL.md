---
name: superior-docs
description: Create, reconstruct, synchronize, or automatically record durable repository documentation from current code, configuration, tests, existing docs, and Git history. Use for project context, architecture, decisions, implementation change records, timelines, build and distribution guides, maintenance handoffs, or cross-session continuity. After verified material implementation work, record the outcome by default unless the user explicitly opts out. Do not use for incidental comments or non-material edits.
---

# Superior Docs

Build documentation that lets a future maintainer recover the project's current shape, important decisions, and safe operating procedures without relying on chat history. Documentation is a maintained view of evidence, not a second source of invented truth.

## Select the mode

- **Bootstrap:** establish a useful `docs/` system where none exists.
- **Record:** capture a verified implementation, fix, refactor, configuration change, or feature outcome in the implementation timeline.
- **Synchronize:** update affected documents after verified project changes.
- **Reconstruct:** derive architectural evolution, releases, or maintenance history from repository evidence.
- **Handoff:** capture the current implementation, boundaries, risks, and next work at the end of a substantial effort.

Do not ask the user to choose when the request already determines the mode.

## Record implementation work by default

After verified material changes to code, configuration, schema, API behavior, security controls, build behavior, or user-visible functionality, create or update an implementation record unless the user explicitly asks not to create or update documentation.

Read [references/automatic-change-recording.md](references/automatic-change-recording.md) whenever another implementation skill completes material work. It defines the default path, minimum bootstrap, entry schema, opt-out behavior, and exclusions.

Do not wait for a separate documentation request and do not ask for routine permission. Treat an explicit opt-out such as “skip docs,” “do not document this,” or an equivalent project instruction as authoritative. An opt-out for one task is not a permanent preference unless the user says so.

## Establish evidence

Inspect the relevant code paths, configuration, tests, scripts, deployment files, existing documentation, and repository instructions. Use Git history when historical sequence or releases are in scope.

Inspect repository status and the task's actual diff before attributing a change. In a dirty worktree, preserve unrelated user edits and do not describe pre-existing changes as outcomes of the current task.

Classify statements as:

- **Current fact:** proven by the present repository or runtime evidence;
- **Accepted decision:** recorded in an authoritative decision source or explicitly confirmed by the user;
- **Historical fact:** supported by a commit, tag, release, migration, or dated artifact;
- **Planned work:** explicitly proposed but not yet implemented;
- **Unknown:** unresolved and stated as such.

Never turn a commit message, stale document, unused file, or plausible architecture into a current fact without corroboration.

## Build the smallest useful documentation map

Read [references/documentation-map.md](references/documentation-map.md) when bootstrapping or reorganizing `docs/`. Always create an index and the three core documents when the user requests the full continuity system. Add specialized sections only when the repository has corresponding evidence and maintenance value.

Automatic change recording is a smaller bootstrap: when no documentation system exists, create only `docs/README.md`, `docs/implementation-timeline/README.md`, a stable feature-domain subfolder with its index, and the first verified change record. Do not fabricate the three core documents merely to satisfy the recording default.

Do not create empty directories, placeholder guides, or one file per imagined subsystem. A smaller linked set that stays accurate is better than an impressive tree nobody can trust.

## Write for retrieval

- Put one durable subject in each document and give it a stable path.
- Start each document with purpose, scope, and last verified revision or date.
- Link to authoritative code, configuration, commands, decisions, and related docs.
- Record ownership and boundaries, not exhaustive file inventories that immediately go stale.
- Use exact commands only after verifying them in repository sources or by safe execution.
- Separate current state from history and future work.
- Prefer concise tables for mappings, decisions, interfaces, or commands; use prose for rationale and constraints.
- Name the authoritative source for volatile contracts and avoid manually duplicating generated schemas, command output, or configuration inventories.
- Preserve ownership and update triggers: a document should make clear what event can make it stale and where a maintainer verifies it.

Read [references/core-files.md](references/core-files.md) when writing the documentation index, project context, architecture, or decisions ledger.

## Reconstruct history carefully

Read [references/history-and-handoff.md](references/history-and-handoff.md) when using commits, releases, migrations, or earlier documentation to build timelines and handoffs.

Summarize change by outcome and architectural consequence. Do not dump every commit, treat commit order as causality, or claim a feature shipped because a branch once contained related code. Link facts to commits or tags when stable identifiers are available.

## Synchronize without rewriting everything

After a change, update only documents whose claims became incomplete or false. Preserve useful history and append decisions when the repository follows an append-oriented record. Replace current-state descriptions when reality changed; do not retain both versions as if both remain active.

If documentation conflicts with working code or configuration:

1. verify that the code path is active;
2. check for an accepted pending migration or exception;
3. update the stale document when authorized;
4. report unresolved conflicts rather than choosing a preferred story.

Recording and synchronization are related but distinct. A material implementation receives a concise timeline record by default. Update current-state architecture, decisions, guides, or build documents only when their claims or procedures actually changed.

## Verify

- Re-open every changed document and follow its relative links.
- Confirm commands, paths, names, versions, and ownership against current sources.
- Check that the root index reaches every maintained document and does not point to placeholders.
- Review the diff for secrets, credentials, private infrastructure details, personal data, or copied logs.
- Confirm the document attributes only work supported by the current task's evidence and does not absorb unrelated dirty-worktree changes.
- Report the evidence inspected, documents changed, historical limits, and unresolved unknowns.
