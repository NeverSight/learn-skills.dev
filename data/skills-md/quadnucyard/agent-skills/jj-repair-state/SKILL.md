---
license: MIT
name: jj-repair-state
description: Diagnose and repair corrupt Jujutsu (jj) operation or working-copy state in a colocated Git repository. Use when jj reports missing Git commits or trees, operation-head or checkout-operation mismatches, failed working-copy snapshots, or requests to preserve reachable Git commits while repairing jj metadata.
---

# Jujutsu State Repair

Repair existing Jujutsu metadata in place. Preserve the Git worktree and every Git-reachable commit unless the user explicitly authorizes a broader recovery.

## Guardrails

- Start with read-only evidence. Do not run normal `jj status`, `jj op log`, `jj git import`, or other mutating jj commands while the active state is broken.
- Never use `git log --all` as a diagnostic: stale `refs/jj/keep/*` may themselves reference missing objects. Inspect `HEAD` and named commits only.
- Record the exact Git commits the user requires preserved. Verify each with `git log -1 <id>` and that it is reachable from `HEAD` before changing jj metadata.
- Never reinitialize, delete, garbage-collect, reset, clean, or checkout unless the user explicitly authorizes that exact action.
- Treat `.jj/repo/op_heads/heads/*`, `.jj/working_copy/checkout`, and `.jj/working_copy/tree_state` as metadata. Back up every file before changing it. Do not change source files or `.git` while repairing jj metadata.
- Stop if Git is not in the state the user described. Existing conflicts or changes are data to preserve, not cleanup work.

## Diagnose

Run the bundled inspector first:

```powershell
& "<installed-skill-directory>/scripts/inspect-jj-state.ps1" -Repository .
```

Replace `<installed-skill-directory>` with the directory containing this `SKILL.md`; resolve it from the available skill catalog rather than assuming an agent or home path. The inspector requires PowerShell 7 or newer.

It prints the Git `HEAD`, the recent reachable history, operation-head IDs, the checkout operation ID, and the stored view/parent IDs of each active operation. It does not invoke `jj` or write files.

Then validate an operation candidate without consulting the damaged current state:

```powershell
jj --at-op <full-operation-id> status
```

`--at-op` implies `--ignore-working-copy`. A usable candidate prints its working-copy and parent commits. Prefer the direct parent of a corrupt active operation, but only if it contains every required Git commit.

## Repair Decision

Use the smallest matching repair.

| Evidence | Repair |
| --- | --- |
| Active head is corrupt, checkout already names a valid predecessor | Replace only the active head marker with that predecessor. |
| Active head and checkout both name the same corrupt operation, and a valid predecessor is selected | Replace both pointers with the predecessor. |
| Active operation and checkout agree, but `jj debug working-copy` reports a missing `TreeId` in its current tree | Back up only `.jj/working_copy/tree_state`, remove it, then let normal `jj status` rebuild it from the existing worktree. |
| The selected valid operation predates a valid Git `HEAD` that must be used | From that explicit operation, run `jj --at-op <id> --ignore-working-copy git import`; verify the imported commit explicitly, then use `jj --at-op <new-id> --ignore-working-copy edit <git-head>`. |

Do not combine these repairs speculatively. Reinspect after each one.

## Pointer Format

`op_heads/heads/` is a set of zero-byte files named by full operation IDs. The current local checkout stores its operation ID in `.jj/working_copy/checkout` as protobuf field `0x12`, length `0x40`, followed by 64 identifier bytes. The inspector verifies this format.

When replacing a head, create the verified-good marker first, then move the corrupt marker to a uniquely named backup outside `.jj`. When replacing `checkout`, copy the 75-byte file first, verify the header and current ID, then replace only bytes `2..65` with the full selected operation ID. Do not hand-edit an operation record under `op_store`.

## Verify

After a pointer repair, run these in order:

```powershell
jj status
git status --short --branch
git log -n 3 --format='%H%x09%s' HEAD
```

If normal `jj status` fails with a sibling-operation message, compare the active head and checkout operation using the inspector. If it fails with a missing `TreeId` while those IDs agree, rebuild only `tree_state` as above. If it returns clean, confirm each required commit remains reachable from `HEAD` and report the backup paths created.
