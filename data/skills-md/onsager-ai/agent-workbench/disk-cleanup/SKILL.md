---
name: disk-cleanup
description: Inspect and reclaim local disk space from regenerable caches, completed worktrees, build artifacts and task leftovers. Use when storage is filling up or the user asks to clean local disk space.
---

# Clean up local disk space

Recover space left behind by completed work while preserving source, user data and running work. Use existing filesystem, Git and cache-management tools; read [targets.md](references/targets.md) for the target types involved.

## Establish scope and measure

- Distinguish an inspection request from permission to delete. Asking what uses space or explicitly asking to hold deletion authorizes inspection only. A request to clean up authorizes the clearly disposable items within its scope; reuse that authority without repeatedly asking. Ask only when a useful next action crosses that scope, destroys valuable data or requires stopping another task.
- Start with `df -h` on the requested location to identify the full filesystem and record available space. An artifact on another mount will not help that filesystem. Ask for a space target only if the next decision depends on it; otherwise prioritize a useful batch of cold, regenerable leftovers.
- Follow the applicable host and repository resource rules, including any required current temperature readings and limits on local checks. Do not substitute a historical policy or invent a threshold. Carry applicable restrictions into any delegation.
- Begin with known artifact/cache locations, worktree registrations and task metadata. Query one selected location at a time; bound metadata walks by time and scope, avoid crossing mounts or following symlinks, and stop when sufficient evidence is available. Do not recursively scan the whole home, filesystem, repository contents or personal logs. Respect the one-file parsing/search limit; do not upload private local trees to CI to measure them. If a recursive size scan would exceed the permitted local work, use an existing size report or report the measurement limit.

## Choose what to reclaim

For each candidate, identify its exact path, type, owning tool/task, known size, regeneration cost and evidence that it is no longer needed. Age, an old branch name and a directory called `cache` are hints, not proof. Mark unknown sizes as unknown; prefer allocated/reclaimable bytes over apparent size, and avoid counting shared layers or hard links twice.

Prefer completed-task build outputs, expired scratch outputs with known ownership and tool-managed unused cache entries. Preserve source, credentials, databases, user exports, session history, backups and unknown content. Separate them from disposable outputs even when they share a directory.

Before removing a Git worktree:

- Check its registration/lock, tracked changes, untracked files and meaningful ignored content. Git's clean status can omit ignored databases or other valuable files.
- Confirm its commits are delivered remotely using fresh remote/PR evidence. A clean tree can still hold local-only commits. A stale remote-tracking ref is insufficient. Account for a verified squash-merged PR rather than assuming only an identical branch tip proves delivery. Do not commit/push unrelated work merely to make it eligible for deletion.
- Check task ownership and current use: running harnesses/builds, process working directories, and installed skill/instruction/config symlinks that reference it. Preserve the primary checkout, locked worktrees and anything still referenced or whose use cannot be established. A merged PR alone does not make a worktree unused.
- Use Git's worktree removal for an eligible tree, then prune stale registration metadata only when appropriate. Avoid force removal, manual deletion of `.git` metadata and branch deletion unless separately in scope.

## Clean in bounded batches

State the selected items, available size estimates and why they are disposable. Proceed within the user's existing cleanup authority; an unresolved candidate does not block other clearly authorized items.

Recheck identity, path boundaries and current use immediately before deletion. A symlink or changed task state can invalidate an earlier plan. Prefer the owning tool's supported selective clean/prune operation; inspect the installed tool's help for its actual scope and version. Broad options such as “all,” volumes, force or deletion of an entire cache root need their own justification and authority.

Clean one class or small batch at a time. Do not run builds, reinstall dependencies, regenerate artifacts or restart services to validate cleanup. Preserve a private record of paths/actions and skipped reasons outside repositories; do not copy personal log contents into the report. Removing regenerable data is generally irreversible; moving it to trash on the same filesystem does not free space until it is emptied.

## Verify and stop

Recheck `df` on the same filesystem and report actual space recovered, remaining available space, actions taken and significant skipped items. Deduplication, snapshots and open deleted files can make estimates differ from recovery. Investigate that discrepancy before expanding the deletion scope; do not kill processes or delete snapshots without authority.

Stop when the user's space goal is met, the selected safe batch is complete, or temperature/ownership/permission limits prevent more work. Never invent recovered byte counts or call unknown content safe. Include any concrete next choice only when it is needed.
