---
name: agents-gen
description: Mandatory AGENTS.md lifecycle gate for direct requests to create, update, organize, audit, or fix project AGENTS.md files and for every implementation task that creates, modifies, renames, or deletes project files. Create a minimal root, give independent subprojects scoped instructions, route conditional guidance through discoverable .agent-guides, and report unchanged when no durable instruction impact exists. Skip pure discussion, research, planning, and other read-only tasks.
metadata:
  short-description: Create and maintain scoped AGENTS.md files
---

# Agents Gen

Treat `AGENTS.md` as scarce, persistent instruction context. Curate it from current project evidence; do not turn it into a project encyclopedia or a filesystem map.

## Apply the lifecycle gate

Run this Skill in either situation:

1. The user directly asks to create, update, organize, audit, or fix `AGENTS.md`.
2. The current task changes any project file. Run the gate after the implementation is complete and before final handoff, even when the user did not mention `AGENTS.md`.

Skip the maintenance gate for pure discussion, research, planning, status, or review work that makes no project-file changes. A direct audit request remains read-only unless the user also asks for changes.

## Protect scope and ownership

1. Use the runtime-provided workspace/current directory as the project root. Resolve it to an absolute path. Do not substitute an ancestor repository or a guessed subdirectory.
2. Read every applicable parent, root, and nested `AGENTS.md` before deciding. Detect `AGENTS.override.md`, `CLAUDE.md`, and other instruction files, but do not modify them in v1.
3. Treat existing text and dirty worktree changes as user-owned. Make minimal edits and preserve the file's useful voice and organization.
4. If ownership is unclear, applicable instructions genuinely conflict, or a proposed edit would choose a new team policy, stop the write and report the decision needed.

## Inspect fresh evidence

Run the bundled read-only inventory when available:

```bash
python3 <skill-root>/scripts/inspect_agents_context.py <absolute-project-path>
```

Also inspect the relevant manifests, workspace configuration, lockfiles, task definitions, CI, tests, docs, and the files changed in the current task. Discover the current independent apps, packages, services, and plugins afresh; never rely on a persisted directory map. Do not ask the user for facts the repository answers. Never assume a conclusion from a previous run is still current.

Before creating or changing instructions, read [the rule admission and placement policy](references/rule-policy.md). For the mandatory post-change gate and module evolution rules, also read [the maintenance policy](references/maintenance.md).

Read [the progressive-disclosure policy](references/progressive-disclosure.md) when any `.agent-guides` directory exists, the root file triggers size review, or the user asks to organize, shorten, split, or progressively disclose instructions. Do not load it for an ordinary unchanged maintenance gate.

## Choose the outcome

### Create

When the root `AGENTS.md` is missing and repository evidence is sufficient, create the smallest useful version. This applies both to a direct creation request and to the first qualifying implementation task in an unconfigured project. In the same pass, create a minimal nested `AGENTS.md` for every evidenced independent subproject that does not already have its own usable local instructions. Create `.agent-guides` only for supported durable rules that are conditional inside an established instruction scope; never create empty guide structures.

Match the language of the project's maintained documentation. If the repository gives no language signal, use concise English. Render only sections with real content; use the [root skeleton](assets/root-minimal.md) and [nested skeleton](assets/nested-minimal.md) as pruning aids, not forms to fill. A multi-project root may say that each independent subproject has local guidance, but must not enumerate volatile implementation paths.

If the project is empty or its purpose and commands cannot be established without guessing, do not fabricate them. Report `AGENTS.md: blocked` and ask only for the missing durable project decision.

### Maintain

Compare the final project state with the applicable instruction hierarchy. Update only when the change creates, removes, or alters durable guidance that future tasks need. Ordinary feature implementation usually produces `AGENTS.md: unchanged`.

Create and maintain a nested `AGENTS.md` for each evidenced independent subproject. Its stable purpose and technology boundary are sufficient local context even before it accumulates additional conventions. For an ordinary directory that is not an independent subproject, create a nested file only when distinct, stable instructions apply to nearly every task in that subtree.

Keep each `AGENTS.md` small. Rules needed by nearly every task in its scope stay in that file. Conditional language, testing, API, release, security, migration, or Git guidance belongs in the matching scope's `.agent-guides`; the root carries the one project-wide discovery protocol. Reuse existing authoritative documents instead of copying their policy. During an explicit reorganization, move supported existing policy into guides without changing its meaning. Never invent a convention to fill a guide.

Safe, evidence-backed maintenance may be written automatically within the authorized project task. Ask before semantic deletion or rewriting of user policy, resolving a real conflict, changing ownership, or introducing a new team convention.

### Audit

For a read-only audit, classify each existing instruction as keep, rewrite, move, automate elsewhere, ask, or remove. Include missing independent-subproject coverage, missing guide discovery, invalid guide metadata, broken progressive-disclosure links, brittle implementation paths, and directory maps. Report evidence and destination without writing files.

## Verify the accepted artifact

After a write:

1. Re-read every changed `AGENTS.md`.
2. Re-run the inventory and confirm relative links and the focused-document tree resolve.
3. Trace commands to current project evidence. State whether a command was merely verified as declared or actually executed.
4. Check the effective hierarchy for duplicate or contradictory root and nested rules.
5. When guides exist, confirm the root discovery protocol, entry descriptions, scope pairing, one-level reference structure, and all guide links are valid.
6. Confirm personal preferences, one-off task notes, volatile implementation paths, brittle directory maps, and copied reference material did not enter persistent context.
7. Run the gate a second time conceptually: without new evidence, the result must be `unchanged`.

Do not report completion from a file write alone. End with exactly one lifecycle result and a short evidence-based reason:

- `AGENTS.md: created`
- `AGENTS.md: updated`
- `AGENTS.md: unchanged`
- `AGENTS.md: blocked`
