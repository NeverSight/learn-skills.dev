---
name: implement-spec
description: "Implement an entire spec and its tickets on an integration branch, then deliver a verified pull request ready for review."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

Read `docs/agents/issue-tracker.md` before starting or resuming. Follow its ownership, Project mapping, pause/release procedure, and final PR policy. If tracker configuration is absent, tell the user to run `/setup-matt-pocock-skills`.

The goal is the entire spec implemented on a single **integration branch**, delivered through a **pull request ready for review**. A local branch or pushed commits alone do not complete the work. PR delivery is required regardless of which issue tracker holds the spec and tickets.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Start every subagent with a fresh context window.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency. The main agent owns PR publication, verification, assignment, and Project updates. Resolve the driving developer, read current assignees and parent reservations, and preserve existing ownership unless reassignment was requested. Claim unassigned work according to the tracker policy. Ownership of this PRD reserves the scope of this integration run; subagents return evidence without reassigning or completing tracker items.

## Implementation progress and tracker completion

Track ticket progress separately from issue status. A ticket is **integrated** when its implementation commit is present on the integration branch; use that evidence to release dependent tickets, even while its issue remains open. Reconstruct this progress from commits and the task graph when resuming.

The spec/PRD and its sub-issues remain open and outside terminal tracker states such as `Done`, `Completed`, or `Resolved` until the **final integration PR is merged into its intended base**. Implementation, commits, pushes, merges of ticket branches into integration, and opening or marking the final PR ready are progress, not tracker completion. This rule applies to the main agent, every subagent, local ticket files, issue state, and project-board status. Include it in every subagent brief; subagents report implementation and integration evidence rather than closing work in the tracker.

Use `Refs #<number>` or ordinary links in implementation commits and any intermediate PRs. Reserve automatic closing references for the **final integration PR body**, using a mechanism that closes work only after that PR merges. If the tracker or selected base does not support this, leave the items open, link them to the final PR, and report that closure requires a verified merge. Creating the PR is not permission to close the items manually.

## Steps

1. Read the spec and tickets to understand the task graph. Identify the hosting repository, push remote, and PR base branch from the user's instructions or repository policy; otherwise use the repository's actual default branch. Verify that the available hosting tool is authenticated and can push branches and open PRs. Read current ownership and configured Project state. Reconstruct resumed progress from the remote PR and integration commits before changing Status. Report concrete access or tracking blockers separately, preserving existing URLs and progress.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch from the selected base, or resume the existing integration branch for this spec. Record its head branch and intended PR base. Reuse an existing open PR for that head and base. After the first merge in step 5, push the integration branch and open a draft PR if none exists: an empty integration branch cannot open one. Link the spec and every ticket in the body, following the tracker completion rule above. For GitHub issues in this repository, use a separate `Closes #<number>` in this final PR's body when its base supports closure on merge.

4. When implementation starts, set the PRD to `in-progress` through the tracker policy. Set each ticket to `in-progress` as it is dispatched; queued tickets retain their current Status. Use a fresh **implementer subagent** for each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - merges the integration branch tip into its own branch before reporting its implementation commit, leaving tracker items open

5. Once an **implementer subagent** returns its implementation, merge its work to the integration branch with a **merger subagent** and record the ticket as integrated in the execution progress. Publish the first draft as described in step 3, and keep the remote integration branch updated after subsequent merges. After each push, fetch the spec/PRD and sub-issue states, including project-board status when configured, and verify that they remain open and non-terminal. If an automation or agent action completed them prematurely, report the affected items and observed transition as a blocker; preserve the branch and worktrees and identify the run as incomplete until the premature completion is corrected.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once every ticket's implementation is integrated, call the Skill tool with `code-review` on the integration branch against the selected base. Fix all issues raised by the code review in a single fresh **implementer subagent**, integrate those fixes, and run the relevant checks on the integrated result. Continue to delivery once the review findings are resolved and those checks pass.

8. **Deliver the PR.** Push the final integration branch, including review fixes. Query the hosting service for an open PR from the integration head to the intended base; create it now if the earlier draft was never opened. Update its body with the spec, all tickets, a summary of the delivered behavior, and validation results. Mark it ready for review if it is a draft. Once the final PR is ready, set the PRD and its delivered tickets to `waiting-validation` through the tracker policy. Fetch the PR and configured Project items again and verify all of the following from remote state:
   - the PR is open and ready for review, rather than a draft;
   - its head and base match the recorded integration branch and selected base;
   - its head commit matches the final local integration commit;
   - its body links the spec and every implemented ticket, with closing references where supported;
   - the spec/PRD and sub-issues remain open and outside terminal project-board states while the PR is unmerged;
   - when Project tracking is configured, the PRD and every delivered ticket belong to the selected Project with the expected assignees and mapped `waiting-validation` Status.

   This step is complete only with a verified PR URL and the configured tracking verification. If pushing, creating, updating, marking ready, or verifying the PR fails, preserve the integration branch and worktrees, report the failed operation and concrete blocker, and identify publication as incomplete. If only tracking fails, report the verified PR URL and tracking as incomplete. A branch name is not a substitute for the PR. On a retry, query for the existing PR before creating another.

9. After successful PR and tracker-state verification, clean up the implementer and merger worktrees created by this run, preserving unrelated worktrees and the integration branch. Report the PR URL, its base and head, validation results, and any remaining non-blocking limitations. Describe the result as **implemented and awaiting PR merge**, with the spec/PRD and sub-issues still open. Leave the PR open for review; merging it requires a separate user instruction. A later merge workflow may close tracker items only after fetching remote evidence that this final PR was merged into the intended base; a closed-but-unmerged PR does not qualify.
