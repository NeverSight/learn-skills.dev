---
name: cross-repo-standard-sync
description: >-
  Find the canonical owner of a development standard, audit drift, or propagate
  an approved standard across repositories and agent configurations. Use when
  the user says their preferred workflow is out of sync, wants common rules
  synchronized, or asks which copy is authoritative. Separate personal defaults,
  organization policy, and repository facts; preserve local commands and
  exceptions, and never overwrite ambiguous differences without approval.
---

# Cross-repository standards synchronization

Keep a development rule consistent without pretending every repository has the
same owner, stack, commands, or exceptions. A canonical source is selected by
who owns the rule, not by which copy happens to be easiest to find.

Read and apply [`task-completion`](../task-completion/SKILL.md) using the skill
loader or sibling file. Track each approved target through verification; an
audit is complete with findings, while a synchronization also requires the
authorized writes and read-back checks. Report an unavailable dependency.
This workflow does not expand the approved targets or authorize publication.

## Classify ownership before choosing a source

For each rule, identify its scope:

- **Personal defaults:** preferences the user wants applied across their work.
  Store them in a user-owned, private, versioned source when they include
  personal or confidential context.
- **Organization policy:** rules owned by a team or organization. Use that
  organization's maintained source; do not recast it as an individual
  preference or move it into a public repository.
- **Repository facts:** actual commands, dependencies, CI, local services,
  architecture, and approved exceptions. These remain authoritative in the
  repository that owns them.
- **Public reusable guidance:** portable, sanitized practices only. A public
  skills collection is not the canonical home for private preferences or
  organization-specific policy.

One rule may combine a shared default with repository-specific facts. Keep the
shared principle in its owner source and keep local values in the repository;
do not duplicate the whole document just to carry a few local differences.

## Discover the canonical source

When asked to find or define a source of truth:

1. Inventory candidate documents, skill files, generated copies, repository
   remotes, and configured agent skill/rule locations. Start read-only.
2. Compare content and metadata, but do not treat matching hashes, newest
   timestamps, a global install, or a public catalog as proof of ownership.
3. For each rule, record its owner, canonical path/repository, audience, and
   intended targets. Distinguish source files from generated or installed
   copies.
4. If ownership is unclear or two sources conflict, show the conflict and ask
   the user which source should win. Do not silently appoint a canonical copy.
5. Keep secrets, private identifiers, and confidential source text out of
   command output, reports, and public files.

## Audit drift

Compare each target with only the rules that apply to it. Classify differences
as:

- stale shared guidance that should be updated;
- valid repository-specific facts or exceptions that must remain local;
- an intentional team or project override with an identified owner; or
- an unresolved conflict requiring a decision.

Report drift with file/section references and a concise description. Redact
private paths, URLs, identifiers, and sensitive content when the report may be
shared. An audit is read-only unless the user also authorizes changes.

## Synchronize only approved targets

Before writing, establish the canonical revision, target repositories and agent
configurations, and which files/sections are managed. Then:

1. Show a per-target plan or diff before broad propagation.
2. Prefer a generator, package/install mechanism, or clearly marked generated
   blocks over manually editing many copies. Use symlinks only where the target
   agent and deployment environment support them reliably.
3. Never overwrite repository-specific commands, facts, credentials, or
   intentional exceptions with generic text. Preserve unmanaged content exactly.
4. Do not modify a dirty file or a target with an unresolved ownership conflict
   without resolving the conflict with the user first.
5. Apply only to the repositories and configuration roots the user approved.
   Synchronizing a policy does not authorize committing, pushing, publishing,
   or installing globally.
6. Validate generated files, links, frontmatter, and relevant local checks.
   Provide a `check`/dry-run mode or drift report when the existing tooling
   supports it; do not invent a command and claim it ran.

## Precedence and exceptions

Do not impose one universal precedence for every organization. Use the owners'
documented hierarchy. In general:

- mandatory security, legal, and organization policy cannot be weakened by a
  personal preference;
- a repository's verified technical facts determine its local commands and
  setup;
- personal preferences apply where compatible with those constraints;
- exceptions should be local, explicit, narrowly scoped, and have an owner or
  reason so they do not become accidental forks of shared policy.

If two applicable rules cannot be reconciled, stop before changing files and
ask which policy governs.

## Completion report

Summarize the canonical source selected (or state that it remains undecided),
the targets audited or changed, local exceptions preserved, unresolved conflicts,
and validation performed. Do not claim synchronization is complete if any
approved target was skipped or could not be verified.
