---
name: woostack-doctor
description: Diagnose and, after approval, repair a repository's local `.woostack/` workspace health with canonical GitHub policy validation.
---

# woostack-doctor

Diagnose — and, with explicit approval, repair — the health of a repository's `.woostack/`
workspace. Doctor is local integrity and convention checking; it never creates a workspace,
publishes planning artifacts, reconciles a feature board, or repairs remote resources.

It has two layers:

- The headless [`scripts/doctor.sh`](scripts/doctor.sh) engine is provider-free. Every check is
  static: it reads no credentials and makes no network call.
- The interactive repair layer proposes a local changeset and mutates nothing before approval.
  Route an explicitly approved repair through [`woostack-execute`](../woostack-execute/SKILL.md)
  with the approved scope and commit/publication limit, including a local-only limit when applicable.
  Remote and retained data are report-only.

## Commands

- `/woostack-doctor [path]` — diagnose the workspace, then offer a gated changeset for the local
  findings it can describe.
- `/woostack-doctor [path] --check` — diagnose only, print GitHub-style annotations, and exit
  nonzero when an `error` finding exists or a check could not complete. It mutates nothing.

The engine depends on [`woostack-init`](../woostack-init/SKILL.md) for the shipped template and
canonical resolver.

## Procedure

1. Capture the requested target without statting, reading, canonicalizing, or invoking Git before
   the workflow has admitted it.
2. Resolve the effective tracked plus primary-checkout local policy through
   `woostack-init/scripts/config/resolve-config.sh`. Doctor consumes that authoritative validation;
   it does not duplicate the GitHub schema.
3. Run static read-only checks for configuration, diagnostics, ignore drift, and retained data. OMP
   agent selection is host-owned; Doctor never inspects, creates, repairs, or removes project agent
   definitions. Legacy provider settings and mirror-era manifests are preserved and produce
   actionable retirement guidance only; they never select a destination, recreate a wrapper, or
   block unrelated local diagnosis.
4. If there is no `.woostack/`, stop and refer to
   [`woostack-init`'s local-support path](../woostack-init/SKILL.md#local-support), explicitly for
   support initialization only, without a document interview. Doctor never scaffolds.
5. Propose a changeset grouped by finding code, path, and exact local change. A finding may describe
   a repair; no check applies one.
6. **HARD GATE — approval.** Silence is not approval. Approval to edit a local file does not
   authorize commit, push, or PR creation. Hand the specific approved repair to `woostack-execute`
   with the user's actual delivery limit: explicitly qualify a local-only handoff as no commit,
   push, or PR; pass an authorized commit-only or PR request as given. No helper command contacts
   a provider or mutates retained data.
7. Confirm in the same static mode and report residual findings.

## Hard constraints

- Missing configuration is valid; absent `github` means no Project/Status policy is selected.
- The canonical top-level `github` object is validated once by Init's resolver. Legacy
  `artifacts.provider`, `artifacts.linear`, `artifacts.plane`, and older root provider settings are
  opaque historical data: preserve them, do not validate them as active policy, and report their
  retirement at the affected boundary.
- Static diagnosis is provider-free. Authorized GitHub capability evidence is read by the calling
  workflow through native host tools or host-authenticated `gh`; Doctor accepts no capability
  receipt and never opens a provider session.
- Never scaffold, migrate, import, mirror, create, repair, reparent, rewrite, close, or delete
  remote or retained records. Never read credentials or invoke custom HTTP/GraphQL transports.
- Gate every repair. Preserve symlink/no-follow, private-file, locking/CAS, dirty-worktree, and
  read-back safety. Never merge.
- Doctor never writes a `.woostack/` support file itself, and it never inspects, prunes, or removes
  Git worktree registrations. Workspace and worktree lifecycle belongs to the host or repository
  owner under the [init workspace guidance](../woostack-init/references/worktrees.md).
