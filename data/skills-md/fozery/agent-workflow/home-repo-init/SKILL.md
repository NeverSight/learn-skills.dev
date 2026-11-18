---
name: home-repo-init
description: Set up a navigation and shared-material home for a project with several repositories.
disable-model-invocation: true
---

# Home repo initialization

Create or update a **home repo**: navigation to related repositories and a location for explicitly approved shared material.
Keep child code, history, remotes, trackers, and repository-specific instructions where they are.
This skill configures navigation and access, not task workflows or implementation plans.
Read applicable project instructions. Use the project's chosen tools, including Orca when configured. No other skill or client is required.

## 1. Bound the inventory

Stay read-only until approval in step 4. Keep inventory and proposals in the conversation meanwhile.
Start within explicitly authorized roots. If scope is missing, propose roots and obtain approval before searching.
Record roots, traversal depth, and exclusions. Skip dependencies, builds, caches, and unrelated worktrees.
Obtain approval before widening scope, including to user-level skill folders. Do not scan the entire home directory by default.

Leave `.env`, credentials, tokens, and other secret files unread. Never store secrets in the home.
Before displaying or storing remote URLs, redact embedded authentication and sensitive parameters. Never print raw remote configuration.
If sanitization is uncertain, omit the URL and report that fact.

Recognize `.git` directories and files. Use read-only Git metadata to resolve roots, common Git directories, and worktrees.
Resolve aliases only within scope. Group worktrees by repository identity, retaining each path and branch.
Record separate clones separately, even with matching remotes. Identify submodules and their parents without initializing or updating them.

For each repository, record:

- Local identity, canonical root, worktree/submodule relationships, and purpose from existing documentation.
- Sanitized remote, branch or detached state, and dirty/untracked state without exposing contents.
- Instruction entrypoints, existing home configuration, and name/path collisions.
- Visibility and its authoritative provider metadata source, or `unknown`. A remote URL does not prove visibility.

Do not change authentication or contact unapproved services to resolve unknowns. Commit dates are context, not selection or authority rules.

**Done when:** every discovered repository has an entry, and every inaccessible or excluded search area has a reason.

## 2. Resolve missing choices

Discover facts before asking. Reuse supplied answers and authoritative configuration.
Ask numbered questions in dependency rounds, with recommendations and consequences. Defer questions whose prerequisites remain unresolved.
Resolve only missing choices:

1. Selected repositories and the intended local clone/worktree for each.
2. New or existing home, location, personal/team ownership, and intended publication visibility.
3. Actual clients, session start locations, startup files, and supported instruction/skill loading mechanisms.
4. Portable paths and the location/ownership of cross-repository task artifacts.

Use available client configuration and support documentation within scope. Separate observed behavior from proposed integration.
A new local Git repository has no public/private provider setting. Keep intended publication separate from observed remote visibility.
Unknown visibility blocks broader exposure of repository metadata or material until the owner resolves access, not a local-only navigation proposal.

**Done when:** every discovered repository is selected, excluded, or blocked with a reason, and home/client choices permit a concrete proposal.

## 3. Inventory material

Find skills, instruction files, and agent documentation within selected repositories and other approved roots.
Follow relevant in-scope pointers, including standards, glossaries, decisions, and navigation. Do not assume all documentation should move.
For each item, record source, owner, current authority, consumers, and two independent classifications:

- **Scope:** shared, repository-specific, or published/installed package, based on content and provenance.
- **Relationship:** unique, exact duplicate, or divergent variant, based on complete relevant contents rather than names or dates.

Default to reuse and pointers. Keep installed packages installed and repository-specific material in place.
Duplicates do not establish ownership. Compare divergent variants and ask their owner to select or reconcile them.
Never choose authority from the newest modification time or commit alone.
Ask about shared ownership, conflicting rules, copying, migration, and cleanup only where applicable.
Existing documents remain authoritative until an approved migration.
Before planning copies, migrations, or removals, read [migration safeguards](references/migration.md).

**Done when:** every in-scope item has both classifications, a proposed disposition, and resolved ownership or an explicit blocker.

## 4. Preview and obtain approval

Read [home structure and loading](references/home-structure.md) before drafting files or client integration.
Prefer a short index and existing sources. Do not create empty memory files, task templates, or workflow policies to fill a layout.

Give plan rows stable IDs. Cover every selected repository, material item, and configuration change.
Each row needs its source, destination, and action: keep, point, create, copy, migrate, or recoverably remove.
For changed rows, specify exact files, collision handling, authority before/after, integrity checks, readers, branch/worktree state, and recovery.
Use `none` or `unchanged` where applicable. Group unchanged items only when all members are listed.
Include every affected client, start location, worker, and reference among the readers.

Preview the actual home `AGENTS.md`, repository pointers, and startup-file changes. Resolve all placeholders.
Show existing-file changes as deltas. Identify visibility restrictions, unknown clients, and excluded or blocked rows.
Request explicit approval of executable row IDs, previews, and operations.
Cleanup, Git initialization, branches/worktrees, cloning, commits, remote creation, and publication require distinct permissions.
A pointer grants none of these permissions. Cloning requires an approved sanitized source and destination.
Never automatically commit, create remotes, push, fetch, or pull.

**Done when:** the user approves a specific executable subset, with other rows excluded, deferred, or blocked.

## 5. Apply approved rows

1. Recheck source identity, destination collisions, and dirty state before each write.
2. If state differs from the preview, stop the affected row and request approval of the delta.
3. Apply approved changes through targeted edits, following migration safeguards where applicable.

Preserve unrelated content and dirty changes. Never reset, stash, switch over user work, or overwrite collisions to force success.
For child edits, use the approved new local branch/worktree where needed, or report the row blocked.
On reruns, show and apply only new deltas. Do not recreate files, branches, or copies that already satisfy the approved state.

**Done when:** every approved row is applied, already satisfied, or blocked with its reason and recovery state.

## 6. Verify and report

Check every approved row. Verify pointers from the home, supported child-start locations, and selected worker contexts.
Verify content integrity, package completeness, legal notices, and current authority. Confirm unchanged installed skills remain available.
Distinguish readable links from actual client loading/discovery. Use observed evidence, not assumed sibling-home inheritance.
Report unsupported or unverified capabilities. Live probes require separate permission and must not start substantive project work.

Give every repository, material item, and row a final status: verified, unchanged, excluded, deferred, or blocked, with reasons as needed.
List branches/worktrees, retained originals, recovery locations, and unverified behavior. Do not call a partial migration complete.
Explain home startup and the explicit context handoff for child-start sessions.

**Done when:** every inventory item and row has a final status, and every claimed working route has observed evidence.

## Source

Conceptually informed by [The Home Repo Pattern](https://www.aihero.dev/the-home-repo-pattern), updated November 12, 2026.
This original procedure does not copy its setup prompt. Routine use requires no article reread.
