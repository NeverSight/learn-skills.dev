---
name: ds-catchup
description: "Give the user a short plain-language catch-up on what changed since their last message, followed by every decision still waiting on them. Use when the user returns after a long or unattended run, asks 'where are we', 'what did I miss', or types /ds-catchup."
---

# ds-catchup

Bring the user back up to speed in a minute, and hand them every call only they can make.

## Steps

1. Keep this turn read-only. Do not change code, start jobs or post anything.
2. Collect what happened since the user's last message: your own work, subagent reports, and messages from others. Tool notifications are not user messages.
3. Check the current state of anything touched: tests, branches, PRs, running jobs. Use fresh command output, not memory. Fix any number that does not match the source and say you fixed it.
4. Write what changed in under 100 words. Say what it means for the user, for example "the login bug is fixed and its test passes". Leave out hashes, paths and commands unless the user needs one to act.
5. List decisions waiting on the user. A decision is something only they can do: a product choice, an approval, an irreversible action, or access you lack. Include old ones still open. For each give: what it changes, the evidence, the risk, your recommendation, and "unknown" for missing facts.
6. If nothing waits on them, say so plainly.

## Stop when

- The catch-up and the decision list are written. One reply, no follow-up work.

## Rules

- Never invent a decision to fill the list.
- Work you can still do yourself is not a decision for the user.
- Name things the way the user would, not by internal labels.
- Short sentences, no jargon.
