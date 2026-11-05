---
name: claim
description: Claim a ticket to build it yourself - the next available one, or a given number - and set up its branch the way the agent loop would, then say what to do next. Use when the user wants to work a ticket by hand, pick up the next ticket, take one from the agent queue, or says "claim" or "claim #42".
---

# Claim

Take a ticket out of the agent queue and make it yours, then put its branch in place exactly as the agent loop would, so the work lands where the loop expects it. Everything after the claim is the user's, in this session or another: `/claim` only sets up and says what's next.

The steps it saves are in the loop's own order (see [Building a ticket yourself](https://github.com/imick-io/skills/blob/main/docs/build-a-ticket-yourself.md)): claim, then branch off the epic (after bringing `main` into it) or off `main`, then switch to it.

## 1. Claim and branch

Run [scripts/claim.mjs](./scripts/claim.mjs) from the repo root:

- `node <this skill>/scripts/claim.mjs` for the **next available** ticket,
- `node <this skill>/scripts/claim.mjs <n>` for ticket **#n**.

"Next available" is the loop's queue: open, `ready-for-agent` or `ready-for-agent-debugging`, unassigned, no open blocker, not a spec, epic or `backlog`, its epic not waiting on another epic. Tickets of a `manual` epic count too: they're meant for a person. Earliest epic milestone first, then the oldest ticket.

The script:

1. **Assigns the user**, re-reads, and backs off if someone (or the loop) claimed it at the same moment. An assignee is how the loop knows a ticket is taken.
2. **Finds its epic** through the milestone every issue under an epic carries, and the epic's branch from the epic's body.
3. **Under an epic:** merges `origin/main` into the epic branch and pushes it, in a temporary worktree, because the loop may hold the epic branch in a worktree of its own. Then branches `agent/issue-<n>` off it. **No epic:** branches `feat/<n>` (`fix/<n>` for a bug) off `origin/main`. An existing branch for the ticket is reused, with its earlier work.
4. **Switches** the checkout to that branch.

It refuses to start when the checkout has uncommitted changes, and never discards anything.

Add `--dry-run` to see which ticket it would take and what it would do, changing nothing. Use it first when the user only asked what's available.

## 2. When it stops

The script prints a `## Not claimed` or `## Claimed #n, but its branch isn't ready` heading with the reason. Relay it in plain words with the fix it gives; don't work around it:

- **Uncommitted changes**: ask whether to commit or stash them, then run it again.
- **No ticket available**: the script says why, by reason (in development, blocked, held back by its epic, left in a loop worktree), and names the blockers that would free the most tickets, with where each stands. Relay that, lead with the blocker that frees the most, and offer `/why-sleeping` for what only the user can unblock.
- **#n is blocked**: name the blockers. Pass `--force` only when the user says to build it anyway.
- **#n is assigned to you and the loop looks to be on it**: the loop claims with the user's own GitHub account, so an assignee alone can't tell them apart. Suggest stopping the loop (`npm run agents:stop`) or picking another ticket. `--force` only on the user's word that the loop isn't running.
- **`main` conflicts with the epic branch**: the ticket stays theirs. Offer to resolve the merge with them, then run `/claim <n>` again.
- **The branch is checked out in a loop worktree**: a sandbox left it there. Removing that worktree is the user's call: check no sandbox is running first.
- **Untracked files in the way**: an untracked file here has the same path as one on the ticket's branch. It lists them; moving or deleting them is the user's call.

## 3. Say what's next

On success the script prints what it did and a **Next** list for this exact ticket: services, `/implement #n` (or `/debug-and-fix #n`), `/code-review` against the right base, the checks, and the commands to land it (merged onto the epic branch without checking it out, or a `Fixes #n` PR), plus how to hand it back to the loop halfway. Show that list to the user as it is, then offer to start the first step.
