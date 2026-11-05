---
name: why-sleeping
description: Why is the agent loop sleeping? Splits what stands between the agents and their next work into agent work (what the loop takes on its next pass, or an agent here does when told) and your work (the merge, approval, answer or brief only you can give), each ranked by how much it frees. Use when the user asks why the agents or the loop are sleeping, idle or stuck, or what unblocks them.
---

# Why sleeping

The loop sleeps when it sees nothing it's allowed to do. The user's question is **what gets the agents working again, and who does it?** Answer only that, in two lists: the moves an agent can make, which the user can hand to you, and the moves only the user can make.

`/whats-next` covers the whole project (setup, drift, reviews, the next step in the flow). This skill covers one thing: the moves between the agents and their next piece of work. It only reads, until the user hands you the agent work.

## 1. Read

Run [scripts/blockers.mjs](./scripts/blockers.mjs) from the repo root: `node <this skill>/scripts/blockers.mjs`. It takes every held piece of work (each `ready-for-agent` ticket, each autopilot epic, each issue waiting on triage or an answer) and follows its blocked-by chain down to the next move. Each move gets an owner:

- **Agent work**: building a ready ticket, triage, cutting tickets from an approved spec, working a wayfinder map, verifying an epic PR, fixing its failing checks, resolving an epic's conflicts with `main`, clearing a stuck label or claim. A move marked `[loop]` is one the loop makes on its next pass. If it's waiting, the loop is asleep or not running, and an agent here can make the move now.
- **Your work**: merging a verified epic PR, reviewing a spec, answering an `agent:asked` or `needs-info` question, deciding a `ready-for-human` item, briefing an epic, taking a blocker out of `backlog`. Each one quotes the loop's last comment, so the user sees what is asked.

When the project's loop is new enough, the script also asks the loop itself. Its status file says what the loop is doing: asleep until when, building what, which jobs are backed off after failing, and why the last pass started nothing. Its dry run (`npm run agents -- --dry-run`) says what its next pass would do. A `[loop]` mark then means the loop's own reading agrees. A move the loop wouldn't make loses the mark. A job the loop has backed off becomes agent work: find out why it keeps failing. The dry run reads the whole queue, so the script can take a minute or two.

The script ranks each list by how much held work a move frees, and lists what's already being built. It takes fast and supersonic modes into account: what the loop decides on its own there is agent work.

Read a line further only when the script can't settle it, such as a failing check whose cause you need to name.

## 2. Answer

Reply in this shape and nothing else. No recap of the loop, no "it has nothing to do".

```markdown
**Loop**: <the problem, one line> → <fix>

**Agent work**, say "do the agent work" and I'll start with 1:
1. **<move>** → `<command>`. Frees <numbers>. <"The loop's next pass takes it." when [loop]>

**Your work**:
1. **<move>** → <link>. <what it asks, in a few words>. Frees <numbers>.
```

- Put a loop problem first only when there is one (Docker down, the loop not running, asleep with agent work waiting, a stop requested).
- At most five moves per list, most freed first, one line each. Say how many more there are, if any.
- An empty list gets one line: "none". When both are empty, the queue is truly empty, and the next brief is the way to give the agents work (`/brief <n>`).

## 3. Do the agent work

When the user hands you the agent work (all of it, or by number), make the moves in the listed order, with the command each one names. Building a ticket is a whole `/claim` then `/implement` (or `/debug-and-fix`) run. Before you start a second build, check with the user. After each move, run the script again: one move can free others or change their order. Never make a move from **Your work**, even when you could do it with `gh`. Merging, approving and answering are the user's decisions.
