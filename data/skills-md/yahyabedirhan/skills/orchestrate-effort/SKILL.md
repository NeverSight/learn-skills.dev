---
name: orchestrate-effort
description: Build an effort by orchestrating sub-agents, and deliver a pull request. Use when asked to build or orchestrate an effort from its spec and tickets.
argument-hint: "Path to the effort folder, or to the spec and tickets"
---

# Orchestrate Effort

Build one effort from its spec and tickets, as its orchestrator, following `/orchestrating`. Work in the current checkout: the effort's worktree and branch were chosen when it started. Treat the design as settled: where the spec, the handoff or a ticket leaves a question open, decide it yourself within that design rather than redesigning. Run tickets in parallel by default, and have them verified in the real app wherever the machine allows it.

## Flow

1. **Read the effort.** The argument points at the effort folder or at the spec and tickets. Read the spec, the handoff and every ticket in full, for each ticket's blockers, its acceptance criteria and any input only the user can give.
   - **With no argument:** ask for one.
   - **With no tickets:** tell the user so and stop: the tickets come from `/to-tickets`, in a session they run or ask for.
2. **Start from a clean worktree.** Commit whatever is uncommitted in its own commit and push, so no delegate finds files it may not touch and has to work around them.
3. **Show the plan** with `/show-me`, as a tree: blockers first, which tickets run in parallel, which use an input from the user, and each ticket's review depth. Go on without waiting for a reply: the plan informs the user and asks them nothing.
   - Serialise only the step that uses a shared resource, such as an installed app, a single real UI, a port or a database, not the whole ticket. Overlapping files are no reason to serialise: conflicts are cheap to resolve at integration.
   - Give a large or risky ticket its own `/code-review`. A small, low-risk ticket gets none, because the one review of the whole branch at delivery covers it.
4. **Delegate each unblocked ticket** to a sub-agent with `/implement`, in its own git worktree, where it makes one commit and doesn't push. The brief gives:
   - the paths to the ticket, the spec and the handoff;
   - the ticket's review depth;
   - the shared resources it leaves to you;
   - the report you want back: its commit, the files it changed, the evidence for each acceptance criterion, proof that no temporary verification code is left, anything left running, and any open question.

   Leave out the recipes and conventions the repository already documents, its commit rules included, since the delegate reads them there. Have the delegate verify in the real app, with real screenshots and clicks, rather than with off-screen renders: off-screen renders cost time, and have missed a bug that the first real-screen check caught.

   Write how to verify into every brief that checks a UI, the final review's and any walk-through's included, and follow it in your own real-app checks. Verify with a headless browser the agent runs itself, such as the project's own Playwright tests or `npx playwright` against the real dev server, saving screenshots to files: real clicks there count as the real app. Use the user's Chrome through the Claude in Chrome extension only when the user asks for it in the current task, because it takes over the browser they are working in; the harness advertises the extension, so a brief that names no tool ends up using it. Keep off the user's screen and clipboard: don't open Finder windows or files with `open`, don't script apps through System Events, which needs an Accessibility permission the user won't grant, and don't use `pbcopy` or `pbpaste`; read what the page writes to the clipboard inside the page instead.
   - **When the real app is a shared resource:** have the delegate verify what it can in its worktree, and run the real-app check yourself once per batch at integration.
5. **Integrate each batch of reports.** Note how long each delegate took; a ticket that took far longer than the others goes on your list for the pull request's description, so the user sees where a run lost time. Cherry-pick each delegate's commit onto the effort branch with `--no-commit`, tick each criterion the report shows evidence for, and commit it as the ticket's own commit. Then run the tests, the install and the real-app check once for the whole batch, and push. After the push, release an integrated delegate's worktree only through the configured worktree tool's fresh identity, occupancy and lease checks; use `/treehouse` when that is the tool. Keep occupied or uncertain worktrees and report why, leaving all session-host topology open. Bind the integration proof to the delegate branch tip, and recheck it immediately before release and branch deletion; if the tip changed, prove the new tip landed or preserve the target. Delete the delegate's branch only after its worktree release succeeds: the ticket's commit on the pushed effort branch is the proof its work landed, and git can't show the delegate's branch as merged, because the cherry-pick, with its ticked criteria, no longer matches the delegate's commit by patch. Inspect state before retrying a failed or uncertain release. Tell the user in a line what landed.
   - **On a local tracker:** the ticked boxes and the status go in the ticket's own commit, with its code: done, or waiting for the user's QA when the ticket goes to them.
   - **On a hosted tracker:** tick the issue's checklist the same way once the commit is pushed, and close the issue once every box is ticked. A ticket that goes to the user for QA stays open.
   - **When a criterion is shown only outside the checkout,** such as on a copy of the branch, in another environment or after an install: leave it unticked with a one-line note saying where it was shown and what confirms it. The ticket stays open until it is confirmed.
   - **When a permission check refuses a removal:** leave that worktree or branch for `/settle-effort`.
6. **Hand usable tickets to the user for QA,** only in a project whose instructions opt in to it and say how a build reaches the user. Read `user-qa.md` before the first one. The merge doesn't wait for QA.
   - **When the spec says "QA: blocking":** the pull request waits until the user closes each QA ticket; say so in the pull request.

   Repeat steps 4 to 6 until every ticket is committed and pushed, with its criteria ticked or noted, or deferred by the user.
7. **Deliver.** Delegate the final review to a sub-agent: the full checks and `/code-review` over the whole branch against its base. Delegate the fixes for what it finds the same way, then commit them. Open the pull request with `/to-pr`, and put in its description your running list of decisions and the surprises and skipped checks delegates reported. Besides the diff, the description is the only report the user reads, so whatever you learned and leave out of it stays behind in this session. Leave the worktree clean: commit and push any effort work `git status` still shows, or leave a file out on purpose.
8. **Report** the pull request, each ticket's commit, anything deferred, the tickets waiting for the user's QA and whether the merge waits for them, and the `git status` result: clean, or each file left out with its reason. Besides any QA, the user's only step is to review and approve the pull request. List what you will do once told, as your own steps: merge the pull request, run the effort's post-merge follow-ups such as installs or updates, try what can only be tried after the merge and report the result, and settle the effort with `/settle-effort`.

## References

- [user-qa.md](user-qa.md): handing a ticket to the user for QA, and what its "Ready for you to try" comment holds.
