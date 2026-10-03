---
name: handoff
description: Compact the current conversation into a handoff document another agent picks up — a new harness, a Claude Code cloud session (claude.ai/code), another machine or repo, a colleague, or a side task forked off mid-phase. Say `cloud` and the document is committed and pushed instead of written to temp, because a cloud session clones from GitHub and cannot see this machine. Manual invocation only.
argument-hint: "[cloud] what will the next session be used for?"
disable-model-invocation: true
---

# handoff

Write a handoff document summarising the current conversation so a fresh agent
can continue the work.

**Portability, not compression.** Reach for this only when the work has to
*travel*. Staying in the same session, your harness's own in-session
compaction or reset (`/compact`, `/clear` in Claude Code) covers the ordinary
end-of-phase case. Five situations are the whole trigger:

| situation | why a file |
|---|---|
| swapping harness (Claude Code → Codex, Antigravity, …) | the new harness cannot see this context |
| moving to another directory or repo | a prototype directory is the common case |
| sending the work to a colleague | they need something they can read cold |
| forking a side task found mid-phase | you keep working; a second agent takes the fork |
| **a Claude Code cloud session** (`cloud`) | the cloud machine clones the branch from GitHub — it sees nothing on this machine, and no plugin installed here |

If the user passed arguments, treat them as a description of what the next
session will focus on and tailor the document to it. `cloud` selects the cloud
destination only as the first word of the argument —
`/dev-workflows:handoff cloud <what next>`; the same word later in the text is
just text.

## What goes in

- **One small Mermaid diagram at the top** — done → in flight → next — so a
  reader sees where the work stands before the prose (this repo's diagram
  convention).
- **The live thread**: what is in flight, why, what is next, and every decision
  taken in this conversation that no artifact records yet.
- **A "Suggested skills" section** naming which skills the next agent should
  load — the way its harness loads skills — by plugin-qualified name, and what
  each one is for in this piece of work.
- **References, not copies.** Specs, plans, ADRs, issues, commits and diffs are
  named by path or URL, never pasted. That keeps the file small and keeps the
  settled detail in one place instead of two that drift.
- **Beliefs downgraded.** The next agent treats the document as a contract and
  will not re-check it. Anything this session assumed but never verified —
  "X is not built", "Y already works" — is written as *assumed, not verified*.
- **Nothing secret.** Redact API keys, tokens, passwords and personal data.

## Where it goes — the destination decides

| destination | where the file lands | why |
|---|---|---|
| default | the OS temporary directory, as `<YYYY-MM-DD>-<slug>.md` (same slug rule as `cloud`) — print the full path back, the user keeps it | a transit document, not an artifact to maintain; temp is cleared on some systems, so copy it somewhere durable if the next session is not within the hour |
| `cloud` | `docs/superpowers/handoffs/<YYYY-MM-DD>-<slug>.md` in this repo, on the current working branch, **committed and pushed** | the cloud session clones the branch from GitHub; a file on this machine, in temp or not, does not exist there |

How the next agent picks it up, either way: open the fresh session and point it
at the path — *read this file, then continue*. Point at the file rather than
pasting the summary into a shell command: a summary containing backticks or
`$(...)` is mangled when interpolated, and the usual failure is silent
truncation, not an error.

## The cloud destination, step by step

1. **Everything must be on the branch.** Run `git status`. If the current
   branch is `main`, **stop** — say "branch first" — and do nothing further
   until a branch exists; never push `main`. If the spec, plan or ADRs this
   session produced are uncommitted, commit them before the handoff file (offer
   the commit — assisted git, never automatic).
2. **Write the file.** Create `docs/superpowers/handoffs/` if it does not
   already exist, and write
   `docs/superpowers/handoffs/<YYYY-MM-DD>-<slug>.md`. `<slug>` is a
   lowercase-kebab of the argument's subject (≤ 5 words), or of the current
   branch name when no argument is given. Then **offer** the commit — an
   explicit path list — and, on a yes, commit it; then **offer** the push
   (`git push -u origin <branch>` on a first push) and, on a yes, push. Never
   run the commit or the push without a yes — assisted git, never automatic.
   Tell the user the branch name — it is what the cloud session is created
   from.
3. **The plugins are not there.** The cloud machine starts without this
   machine's marketplaces or user-scope plugins. The "Suggested skills" section
   therefore says so — *may be absent on cloud* — and the document has to stand
   on its own: when a plan exists, name its path and say the plan is
   self-contained (every task carries its own code, commands and checks). Do not
   promise a review loop that depends on a skill the cloud session cannot load.
4. **Give the launch, both ways.** Web: claude.ai/code → *Create session* → this
   repo → this branch. CLI: `claude --cloud "Read <path to the handoff file> and
   continue from it."` If `claude` is not on the PATH, the web route is the one
   that works.
5. **Say how the result comes back.** The cloud session works on its own
   `claude/…` branch and can open a pull request. Locally: `claude --teleport
   <session>` or `git fetch` and check the branch out. Name what must be re-run
   on this machine before merging — the repo's own checks, and any number
   (ADR, version) that must be re-verified against every branch.
6. **The file stays.** A dated handoff under `docs/superpowers/handoffs/` is a
   record of the crossing; it is not deleted when the work lands.

## It's working if

- the document is a small fraction of the conversation, and the specs, plans,
  issues and diffs appear as paths and URLs, not as copied text;
- it reads cold — without this session open, the next agent knows what to do;
- the fresh agent starts working instead of asking the setup to be re-explained;
- in the fork case, this session is still sitting here untouched when you return;
- on `cloud`, the branch the document names is on GitHub and holds the file;
- nothing in it is a key, a token or a password;
- the *Suggested skills* section names the skills you would have reached for
  yourself, and says which may be absent on cloud;
