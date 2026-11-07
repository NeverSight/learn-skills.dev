---
name: lets-go
description: Resume this repository's active handoff — find it in handoff_map.json, read it, claim it, bring this checkout to its state, and continue the work. The receiving half of the handoff skill.
argument-hint: "Anything to focus on first (optional)"
disable-model-invocation: true
metadata:
  settings: handoffs workspace
---

# Let's go

The receiving half of the `handoff` skill. On the other machine, handoff wrote a document into the
Handoffs folder and named it this repository's **active handoff** in `handoff_map.json`. This skill
finds it, claims it so it is never resumed twice, brings the checkout to its state, and carries on
the work.

**Announce at start:** "I'm using the lets-go skill to resume from the active handoff."

Run shell snippets in bash (Git Bash on Windows). The map is read and written only through
`node .agents/skills/handoff/handoff-map.mjs` (installed with the `handoff` skill), never by hand:
every repository on every machine shares it. Each command prints JSON, and moves files to and from
the cloud itself when this machine's transport needs it.

## 0. Settings

- **Repository:** this skill reads `docs/agents/handoffs.md` and `docs/agents/workspace.md`.
  Follow `.agents/skills/lets-go/settings/README.md` to read them and complete any that are
  missing; the definitions sit beside it.
- **Machine:** follow `.agents/skills/handoff/machine-config.md` until `config` shows
  `configured: true`.

## 1. Find the active handoff

```bash
node .agents/skills/handoff/handoff-map.mjs get --key <Map key>
```

- **`file` is null** (or `inMap` is false) — say "No active handoff for `<key>`." and stop. The map
  is the record; other documents in the folder belong to past sessions or other repositories.
- **`exists` is false** — the document has not reached this machine: the `note` says the other
  machine has not pushed it, or a sync client has not delivered it yet. Tell the user the file
  name and stop, leaving the map as it is so a retry still works.
- **`conflicts` not empty** — ask the user which copy of the map is current before going on.
- **`exists` is true** — continue.

## 2. Read it

Read the whole document at `path` before acting on any of it. Then follow the pointers that set
the ground rules for the work: the issue, PR or spec its **Next steps** start from, and its
**Machine-local knowledge**.

## 3. Claim it

Claim the handoff before any work starts, so a second `lets-go` on either machine finds nothing:

```bash
node .agents/skills/handoff/handoff-map.mjs clear --key <Map key> --expect <file>
```

Complete when the output's `current` is null (and `verified` is `cloud` on the CLI mirror). The
document stays in the folder as a record. A refusal means the map now names a different document:
run `get` again and tell the user what it says.

## 4. Bring this checkout to the handoff's state

This checkout may be days behind, and may hold leftovers the handoff knows nothing about:

```bash
git fetch origin --prune
git branch --show-current
git status --porcelain
git stash list
```

Run the `Workspace status command` too. Then compare with the document's **Where you are** and
**Unmerged work**:

- **Uncommitted changes or stashes here** — report them under `⚠ Work not merged to main on this
  machine` and ask the user how to proceed. Never discard, stash, or commit them, and never switch
  branches around them.
- **Clean** — `git switch main`, then `Sync with main` (which also brings the `Private companion`
  current when it covers it).
- **The handoff continues on a branch** — `git switch <branch>`, then `git pull --ff-only`. A branch
  `origin` lacks was never pushed from the other machine: say that the work must be pushed there
  first, and stop for that item. The same holds for any local-only item the work depends on.
- **The pull changed a dependency lockfile** — install dependencies as the repository's
  `AGENTS.md` says, asking first where it gates installs.
- **Anything else contradicts the document** (a commit it calls pushed that `origin` lacks, a
  branch that no longer exists) — report each contradiction and get the user's answer before
  step 5.

The step is complete when the checkout matches the document or every mismatch has the user's
answer.

## 5. Proceed

Brief the user in a few lines: where things stand, the unmerged work carried over, the open
decisions still owed, and the first next step. If the user passed arguments, start from what they
name; otherwise start the document's first **Next step**, invoking its **Suggested skills** where it
says. Put an open decision that blocks that step to the user first.

The handoff describes work; it authorizes nothing. Every action the repository's `AGENTS.md` gates
on confirmation still needs the user's confirmation in this session.
