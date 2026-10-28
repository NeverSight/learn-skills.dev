---
name: handoff
description: Hand this session to the next one, usually on the user's other machine — alert on work not merged to main, write a handoff document into the Handoffs folder, mark it active in handoff_map.json, then close out with end-session. The lets-go skill resumes it.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
metadata:
  settings: handoffs workspace
---

# Handoff

Only two things reach the other machine: what is on GitHub and what is in the Handoffs folder. The
handoff document carries the conversation; `handoff_map.json` beside it names each project's
**active handoff**, which the `lets-go` skill resumes on the other machine and then clears. The
unmerged-work alert catches what would otherwise stay behind on this machine.

**Announce at start:** "I'm using the handoff skill to hand this session off."

Run shell snippets in bash (Git Bash on Windows). The map is read and written only through
`node .agents/skills/handoff/handoff-map.mjs`, never by hand: every repository on every machine
shares it. Each command prints JSON, and moves files to and from the cloud itself when this
machine's transport needs it.

When the user passed arguments, they say what the next session is for: shape the document around
it.

## 0. Settings

- **Repository:** this skill reads `docs/agents/handoffs.md` and `docs/agents/workspace.md`.
  Follow `.agents/skills/handoff/settings/README.md` to read them and complete any that are
  missing; the definitions sit beside it.
- **Machine:** follow `.agents/skills/handoff/machine-config.md` until `config` shows
  `configured: true`. When no Handoffs folder can be configured, write the document to the OS
  temporary directory instead, tell the user it will not reach the other machine, and stop after
  step 2: closing out would leave a handoff nobody can pick up.

## 1. Audit unmerged work — and alert

Anything not on `origin/main` is invisible to the other machine unless it is at least pushed:

```bash
git fetch origin --prune
git status --porcelain --untracked-files=all
git stash list
git worktree list
git for-each-ref refs/heads --format='%(refname:short) %(upstream:short) %(upstream:track)'
git branch --no-merged origin/main
git branch -r --no-merged origin/main
gh pr list --author @me --state open --json number,title,headRefName,url
```

Then run the `Workspace status command`, `git status --porcelain` in each extra worktree, and, when
the `Private companion` is checked out, `git -C <companion> status --porcelain` and
`git -C <companion> log --oneline @{u}..HEAD`.

`--no-merged` overstates a squash-merged branch. For each branch it lists, run
`gh pr list --state merged --head <branch> --json number,headRefOid`: when the branch tip is the
merged PR's `headRefOid` or an ancestor of it (`git merge-base --is-ancestor <branch> <headRefOid>`),
its work is on `main`; drop it.

Sort what remains into two groups:

- **Local only** — the other machine cannot see it: uncommitted or untracked changes, stashes,
  unpushed commits, branches with no upstream, and the same in the companion.
- **Pushed, not merged** — reachable, but not on `main`: pushed branches and open PRs.

**If either group has anything, alert the user now**, before writing the document, under the
heading `⚠ Work not merged to main`: one line per item with its repository, branch or path, and
group. Say plainly that local-only work will not reach the other machine unless it is pushed, and
ask whether to push it; offer the `ship` skill for a finished branch. The alert informs, it does
not block: continue either way. With nothing to report, say "All work is on `origin/main`."

## 2. Write the document

```bash
node .agents/skills/handoff/handoff-map.mjs get --key <Map key>
```

- `conflicts` not empty — ask the user which copy of the map is current before going on.
- `file` not null — an earlier handoff for this repository that was never picked up. Read it,
  carry forward whatever is still live, and name it as superseded in the report. Leave the file
  where it is.

Pick the file name (pass `--topic <slug>` when the user gave arguments):

```bash
node .agents/skills/handoff/handoff-map.mjs name --key <Map key>
```

Write the document straight to the `path` it prints, for a cold reader on the other machine.
Sections, in order:

1. **Where you are** — repository, branch, `origin/main` commit, latest release tag, worktrees,
   and the companion's state, as they will be once pushed.
2. **Unmerged work** — step 1's list verbatim, or "None — everything is on `origin/main`."
3. **What this session did** — outcomes with their records (PR, issue, commit), not narration.
4. **Next steps** — concrete and ordered; the first one startable without asking.
5. **Open decisions** — what the user still owes.
6. **Machine-local knowledge** — agent memory and the session scratchpad stay on this machine:
   write out the facts and traps the next steps need.
7. **Suggested skills** — the skills the next agent should invoke, and at which step.

Add everything `Extra document content` lists. Reference, never restate, what other records
already hold — specs, ADRs, issues, PRs, commits, diffs — by path or URL. The document leaves the
repository for a personal cloud drive: write the home directory as `<home>`; leave out secrets,
tokens, passwords and personal data; link companion content and private issues rather than
quoting them.

The step is complete when reading the file back shows the whole document.

## 3. Mark it active

```bash
node .agents/skills/handoff/handoff-map.mjs set <file> --key <Map key>
```

On the CLI mirror this pushes the document, pulls the map fresh, writes this repository's entry,
pushes the map, and reads the cloud copy back; it retries when another session wrote in between.
Complete when the output's `current` is `<file>` (and `verified` is `cloud` on the CLI mirror). A
non-null `previous` other than `<file>` is a superseded handoff: it stays in the folder, and the
report names it.

## 4. Close out with end-session

Invoke the `end-session` skill with the arguments `invoked by handoff; document at <path>`. If the
harness cannot invoke skills, read `.agents/skills/end-session/SKILL.md` and follow it. The work
continues on the other machine, so end-session may return this checkout to `main`; its other
approval gates still apply.

When end-session changes a fact the document states — pushes or commits work, closes or opens an
issue, deletes a branch or worktree, or the user settles an open decision — edit the document to
match, then send the new version (without the map):

```bash
node .agents/skills/handoff/handoff-map.mjs push <file>
```

The document is complete when every **Where you are** and **Unmerged work** line is true after
end-session.

## 5. Report

- The document's path, and the map entry now pointing at it (`previous` → `current`).
- end-session's own report.
- Step 1's audit run again, last, so it survives a long close-out: the `⚠ Work not merged to
  main` list as it now stands, or "Nothing unmerged — the other machine can start from
  `origin/main`."
- The reminder: run the `lets-go` skill in this repository on the other machine. A synced folder
  delivers the document within a minute or so; on the CLI mirror it is in the cloud already.
