---
license: MIT
name: jj-patch-stack
description: Create additive Jujutsu patch graphs for fixes, redistribution of top changes, and insertion of new changes between existing revisions while preserving original history. Validate the intended final stack through a mapping to the graph without rebuilding it; provide squash instructions for patches that fold into existing targets.
---

# JJ Patch Stack

Represent fixes and new changes by adding `jj` changes while keeping original history untouched. The deliverable is a patched graph with a complete mapping to the intended final stack; constructing that final stack is not required. Include concrete squash instructions for patches intended to fold into existing targets. Preparing or approving patch content does not authorize applying it; execute the squash guide only when the user explicitly authorizes that history rewrite.

One goal is to prepare the absorption or dissolution of changes collected at the top of a stack into the earlier revisions that own them, without rewriting history during preparation. Reconstruct those changes as additive patches; keep the original top changes intact as source evidence. Folding patches into existing revisions belongs to the separately authorized application phase. Removing source changes is outside that phase's squash-only permission and requires its own explicitly authorized scope.

## Non-Negotiable Rules

These rules govern patch preparation. "Apply After Approval" permits only the described squash operations and their automatic descendant rewrites after explicit authorization; all other prohibitions remain in force.

- Use `jj` only. Do not run any `git` command.
- Do not run `jj squash`, `jj rebase`, `jj abandon`, `jj restore`, or `jj undo`.
- Never directly edit an already-built change, including your committed patches. Do not use `jj edit` to check out and modify an existing revision. Make corrections in a new additive patch on top of the affected patch; never squash it into an existing change. The only revision you may edit directly is the new patch change under construction while it is `@`.
- Original targets, source top changes, and committed patches keep the same change ID and commit ID throughout. Corrections remain separate additive patches.
- Process target revisions from oldest to newest.
- Add a patch only for a target that needs a fix or a substantive adaptation to earlier prepared work. Skip unrelated or already satisfied revisions when creating patches. Represent them in the mapping without creating a merge just to carry them forward.
- Every committed patch or insertion must have its own nonempty diff against its parent tree or automatically merged parent trees. Inherited changes and a description alone do not count as patch content.
- Resolve inherited merge conflicts only in the newly created patch change.
- Format every command, flag, revision name, and change or commit ID as code: inline backticks in prose, fenced `sh` blocks for command sequences. Never leave code unformatted.
- Every commit this workflow creates must be well formatted: formatted content and a proper description, per "Well-Formed Commits" below.
- If the requested result cannot be produced without a forbidden operation, stop and explain the constraint.

Read-only commands such as `jj status`, `jj log`, `jj show`, and `jj diff` are allowed. Additive commands such as `jj new`, `jj describe`, `jj commit`, and conflict-resolution commands are allowed only when they operate on the new patch change.

## Well-Formed Commits

A patch change must be complete and well formatted before you commit it and move on to the next target.

- Content: run the repository's formatter and linters on the changed files (for example `cargo fmt --check` and `cargo clippy` in a Rust repo) and fix any findings inside the same new change before committing. Never commit knowingly unformatted or failing code.
- Description: follow the repository's commit-message convention — check recent subjects with `jj log` to detect it (for example Conventional Commits). Use a concise, imperative subject line, and a body only when the reasoning is not obvious from the diff. Never leave the description empty or placeholder.
- A committed patch is an existing change: never edit it in place. If a check problem appears after committing, create a new additive patch on top, fix it there, verify, and commit it separately.

## Examples and Strategy Selection

Choose the strategy by ownership and dependencies, rather than assuming every fix is a direct copy of a diff. These examples illustrate different cases; they are not an exhaustive list of supported fixes.

Trust only substantive descriptions, checked against code and consumers.
A `refactor` may add a feature; assign patch ownership by actual effects.

- **A new bug fix:** an earlier revision introduces an incorrect boundary check, but no fix exists yet. Implement the correction and its regression test in a new child of that target, then carry it forward through the later targets.
- **A fix already collected at the top:** a top change repairs a parser introduced earlier. Reconstruct the parser fix and its test in a patch on the owning revision. Preserve the top change; do not invoke `jj absorb` or move its contents out of it during preparation.
- **Several independent fixes in one top change:** the top change repairs both parsing and caching introduced by different revisions. Separate the fixes by behavior and ownership, even when they touch the same file, then build patches from the older target to the newer one.
- **A fix with a prerequisite:** a top fix calls a helper introduced only in a later revision. Either express the fix using the earlier revision's existing facilities and adapt it later, or place it at the earliest target where the required behavior and helper coexist. Do not copy an unrelated later feature into an earlier target merely to make the patch compile.
- **A fix that changes shape across the stack:** an early correction touches an API that a later target renames or replaces. Implement the correction against the early API, then resolve the inherited conflict and preserve the same behavior in the new patch on the later target. An automatically merged result still needs behavior checks.
- **A partially redundant or mixed top change:** some top edits are already satisfied by earlier patches, while others introduce an independent feature. Do not duplicate the satisfied edits or silently discard the feature. Record which edits are covered and keep the remaining feature as an explicit residual change or separate follow-up scope.
- **A new change between existing revisions:** the intended order is `target-1`, `insert-1`, then `target-2`. Create `insert-1` on the prepared state of `target-1` and map `target-2` on top of it. Add a patch for `target-2` only if the insertion requires an adaptation there. Keep `insert-1` as a standalone final change with no squash destination.

For existing top changes, record the source commit IDs, map each relevant behavior to its target, and account for any residual work. Build from the intended targets, using the source changes as references rather than adding them as parents and inheriting all their edits. For pure redistribution, verify that the final mapped tree matches the original source tip's tree. If additional fixes or excluded work intentionally change the result, explain those differences and verify the intended behavior. Include any retained source changes and residual work in the application guide so that later integration does not apply the same fix twice.

## Mapping Validity Without Rebuilding

A patch graph is valid when every change in the intended final stack can be mapped from it. Record the final order and, for each entry, its role (unchanged target, patched target, or standalone insertion), the graph revisions representing it, the cumulative tree after it, and the intended delta from the preceding mapped tree. Record full change and commit IDs for the referenced revisions. For an unchanged boundary after prepared work, record the original revision and the preceding mapped tree. Its cumulative tree is the result of applying the original revision's delta to that tree. Compose and check that result in scratch files when needed, without adding a commit to represent it.

For example, in `target-1 -> target-2 -> target-3`, insert a change after `target-1`. The insertion leaves `target-2` independent and requires an adaptation in `target-3`.

```text
insert-1 = new(target-1) + insertion edits
patch-3 = new(target-3, insert-1) + adaptation for target-3
```

| Intended final change | Mapped cumulative tree | Delta to review |
| --- | --- | --- |
| `target-1` | `target-1` | Original `target-1` delta |
| Standalone `insert-1` | `insert-1` | `target-1` to `insert-1` |
| Unchanged `target-2` | `insert-1` with the original `target-2` delta applied | Original `target-2` delta |
| Adapted `target-3` | `patch-3` | Mapped tree after `target-2` to `patch-3` |

Review each mapped delta against its intended behavior and dependencies, and verify each mapped cumulative tree is conflict-free and passes its focused checks. For a merge patch, check both its own diff and the delta from the preceding mapped tree, which includes the original target's contribution. Account for all requested changes and any intentionally excluded or residual work. Tip-tree equality alone cannot establish valid intermediate boundaries.

Once this mapping is complete and verified, preparation is complete. Do not rebuild a separate linear stack, rebase existing revisions, or fold an insertion into a neighbor merely to demonstrate that the mapping can be realized. Correct missing or invalid mappings and add a new change only when a boundary requires its own delta. Retain this criterion for combinations of fixes, insertions, redistribution, and later extensions of the graph.

## Workflow

1. Run `jj status` and inspect the relevant graph with `jj log`. Preserve unrelated work. If the working copy contains changes whose ownership is unclear, stop and ask before proceeding.
2. Identify every target revision and order them by ancestry, oldest first. Record any standalone insertions at their intended boundaries in the final order. If the order is ambiguous, do not guess. When fixes already exist in top changes, map their ownership, dependencies, and residual work as described in "Examples and Strategy Selection" before constructing patches.
3. For the oldest target, call the immutable revision `target-1`. If it needs no fix, use it directly as the prepared prefix and proceed to the next insertion or target. Otherwise create a child:

   ```text
   jj new target-1
   ```

4. Make only the fix for `target-1` and run focused verification. Inspect the diff and commit with a well-formed description only if the diff contains the fix:

   ```text
   jj diff
   jj commit -m "<patch description>"
   ```

   Record the committed patch's change ID as `patch-1`. After `jj commit`, this is normally the revision at `@-`; confirm it with `jj log` rather than relying on memory.

5. For each remaining boundary, first decide whether it needs a fix, an adaptation, or a standalone insertion. Map an unchanged target without creating a new change. For a fix or adaptation, start from the original target. Include the latest committed patch or insertion as a second parent if its work is needed in the tree and is not already inherited. For example, if `target-2` is unchanged and `target-3` needs a patch, use:

   ```text
   jj new target-3 patch-1
   ```

6. For a standalone insertion, start from its mapped boundary. Use one parent when an existing revision already represents that tree. Otherwise use the original boundary revision and the latest committed patch or insertion as the parents of the insertion itself. Put the insertion's own edits in that change.

7. Inspect each new working-copy change and resolve relevant inherited conflicts there. Use `jj status` to find conflicted files and `jj resolve` (or the repository's normal file-level resolver) while `@` is the new change. Re-run the focused checks after resolution. Before committing, use `jj diff` to verify the change has its own substantive delta. If the candidate is empty, leave the working-copy change undescribed, omit it from the mapping, and continue from the last substantive revision. Otherwise commit it with a well-formed description and record its change ID.
8. Finish preparation with `jj status`, `jj log`, and focused diffs/tests. Verify the complete final-stack mapping as described above, confirm every original target and source change retains its change and commit IDs, and check the final mapped tree contains all intended earlier work. Do not construct a separate final stack for this validation.
9. Deliver the verified mapping and the applicable application guide described below, using actual revision IDs. Leave the graph intact unless applying changes has been explicitly authorized.

## Shape of the History

For fixes to `target-1` and `target-3` with an unchanged `target-2` between them:

```text
patch-1 = new(target-1) + fix for target-1
patch-3 = new(target-3, patch-1) + fix for target-3
```

`target-2` remains in the mapping. Its original changes reach `patch-3` through `target-3`'s ancestry.

## Apply After Approval

Always hand off the verified final-stack mapping and checks already run. For patches that fold into existing targets, include a squash guide listing every such patch, including corrective patches, its original destination target, and both revisions' full change IDs and current commit IDs. Record the full commit ID for the reviewed tree at the last patched boundary and how to derive any subsequent unchanged mapped trees. Provide concrete commands with those change IDs substituted for the labels below. Execute them only after explicit authorization to rewrite history.

Standalone insertions have no squash destination. Mark them as retained final changes in the mapping. The squash-only procedure below applies when the complete intended result can be obtained by folding patches into existing targets. For a graph containing insertions, the verified mapping is a sufficient completed deliverable. Any later request to materialize that final order needs an explicitly authorized scope covering the required history operations.

Explain that applying the patches rewrites target and descendant commit IDs, automatically rebases descendants, and normally abandons emptied patch changes. Target change IDs remain usable across these rewrites. This ends the preparation phase's commit-ID preservation guarantee. Approval must cover the affected history; it does not authorize pushing or bypassing configured immutable revisions.

### Script for conflict-free stacks

Use [squash_patches.py](scripts/squash_patches.py) from the target repository with Python 3.10+ and `jj` on `PATH`. Give it the reviewed full commit IDs as `PATCH_COMMIT:TARGET_COMMIT` pairs, oldest first. Use the same target for its corrective patches. Replace `<skill-dir>` with the installed skill directory.

```sh
python "<skill-dir>/scripts/squash_patches.py" PATCH_1_COMMIT:TARGET_1_COMMIT PATCH_3_COMMIT:TARGET_3_COMMIT
python "<skill-dir>/scripts/squash_patches.py" --apply REVIEWED_OPERATION PATCH_1_COMMIT:TARGET_1_COMMIT PATCH_3_COMMIT:TARGET_3_COMMIT
```

The first command previews the pairs and affected descendants. Review that output and use its operation ID with the same pairs only after the user authorizes the rewrite. Run with an empty working copy and exclusive access to the repository. The script uses change IDs across rewrites, keeps target descriptions, and compares each completed target with its reviewed patch tree. It stops on a mismatch or conflict and prints the starting operation ID. Earlier squashes can remain after a stop. Verify any trailing mapped revisions, affected bookmarks, and behavior after it succeeds, as in step 4 below.

Use the manual sequence for stacks that expect temporary conflicts, need updated target descriptions, or lack a single cumulative patch chain.

### Manual sequence

Once application is authorized:

1. Recheck `jj --no-pager status` and the relevant `jj --no-pager log`. Confirm that the patch/target mapping still matches the reviewed commit IDs, inspect affected descendants and bookmarks, and preserve unrelated working-copy edits. If the reviewed content or rewrite scope changed, refresh the guide and obtain approval for that change before applying. Record the pre-application operation ID with `jj --no-pager op log --limit 1` for recovery; do not run recovery commands automatically.
2. Squash from the oldest target to the newest, one explicit source/destination pair at a time:

   ```sh
   jj --no-pager squash --from patch-1 --into target-1 --use-destination-message
   jj --no-pager squash --from patch-3 --into target-3 --use-destination-message
   ```

   `patch-n` and `target-n` stand for the recorded change IDs. Use change IDs for these commands because earlier squashes change later commit IDs. Do not use bare `jj squash` or `jj squash -r patch-n`: later patches have multiple parents, and their destination must be explicit. Each command moves that patch's own delta; inherited earlier fixes move with the earlier target rewrites. Do not squash every patch into the final target.

   For a single target, run only its pair. For additional targets, extend the sequence in the same order. Fold a patch and then its corrective patches, in dependency order, into the same original target before moving to the next target; never use an emptied patch as the destination. Keep the target description with `--use-destination-message`, or replace that flag with `-m "<complete updated target description>"` when the approved fix changes the target's intent.
3. After each squash, inspect the rewritten target and pending patches with `jj --no-pager log`, `jj --no-pager show -r target-n`, and focused diffs. Re-resolve the remaining change IDs before continuing; stop if a source or destination is missing, divergent, or ambiguous. An early squash can temporarily conflict in a later target whose approved patch already carries the resolution. Continue only when that resolution is accounted for in the next planned squashes; stop on unexpected conflicts rather than inventing new fixes. Each target must be conflict-free and pass its focused checks after all its patches have been folded.
4. After the last squash, compare the last patched target with its reviewed tree and check the final mapped target for conflicts:

   ```sh
   jj --no-pager diff --from <reviewed-patch-commit-id> --to <last-patched-target-change-id>
   jj --no-pager log -r 'conflicts() & ancestors(<final-target-change-id>)'
   jj --no-pager status
   ```

   The diff and conflict query must be empty. Use the saved full commit ID for the reviewed patch, since its change may now be abandoned. Compare any subsequent unchanged targets, including the final target, with their reviewed mapped trees. Run the relevant behavior checks again, verify target descriptions and affected bookmarks/descendants, and report the rewritten target IDs and results. If validation fails, stop and report it; do not silently restore, undo, or create additional fixes under the squash approval.

The explicit source/destination flags and noninteractive description options are documented in the [Jujutsu squash reference](https://docs.jj-vcs.dev/latest/cli-reference/#jj-squash). Check `jj --no-pager squash --help` for the installed version before applying.
