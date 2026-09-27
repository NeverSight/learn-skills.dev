---
name: working-vantik-knowledge
description: >-
  How to use the Vantik knowledge bank as an agent over MCP: load context
  before starting work, remember one fact at a time with citations for what
  it rests on, supersede rather than contradict, and consolidate instead of
  piling up. Use before starting work
  on any unfamiliar area, and whenever recalling or recording what a workspace
  knows.
---

# Working the Vantik knowledge bank

The bank is one store serving two readers. Humans read **pages** — canonical
documentation, written as prose. Agents write **entries** — single asserted
facts appended to a page, each carrying who claimed it, where it applies, and
whether anyone has confirmed it.

Two rules sit above everything else:

1. **Load context before you start.** Not after you get stuck.
2. **One entry is one fact.** Not a summary of your session.

The tools enforce a floor. This skill is the judgment above it.

## Start every task by loading context

Call `load_context` with the area you are about to touch, before you read a
single file:

```
load_context(scope: "apps/server/prisma", tokenBudget: 2000)
```

You do not need a question. At the start of a task you do not yet know what you
do not know, which is precisely why the scope is enough — the bank returns what
previous sessions established about that area, under a budget you set.

This is the cheapest thing you will do all session. Everything it returns is
something you would otherwise have had to rediscover, and it works across
harnesses: a fact another tool wrote is a fact you get.

If you are working an issue, pass it: `load_context(issueId: "…")`. Knowledge
about the issue's modules then ranks first, and knowledge about their
neighbours — modules that share a capability or a product with them — next.
`moduleIds` does the same when you know the modules but have no issue. A scope
matches by folder: a fact scoped to `apps/server` comes back for work in
`apps/server/prisma`, and one scoped to `apps/server/prisma` for work in
`apps/server`.

When you have an actual question, use `recall_knowledge` instead. Ask it before
investigating something from scratch — the answer may already be in the bank.

Handed an issue or a project, call `pages_for` with it first. At that point you
have an id and no vocabulary — you cannot search for a page called "Deploying
the worker pool" before you know it exists — and this is a direct lookup of the
pages attached to that work, not a guess.

## What is worth remembering

Something a future session would otherwise have to work out again.

**Yes:**

- A decision and why it went that way ("redis holds only cache here; anything
  that must survive a restart goes in postgres")
- A gotcha that cost you time ("the compose webapp container needs
  `BACKEND_URL=http://server:3001` or its /api proxy 502s")
- A convention that is not obvious from the code
- A constraint someone stated that is not written down anywhere

Say which it is with `kind`, so a reader can ask for just the conventions of an
area: `DECISION` for a choice and its reason, `GOTCHA` for something that cost
time, `CONVENTION` for how things are done here, and `FACT` (the default) for
anything else true about the system. `recall_knowledge(kinds: ["CONVENTION"])`
is the question "how do we do things in here".

**No:**

- What you did this session. That is a note on the issue, not knowledge.
- Anything already in the page body — read the page first.
- Anything the code says plainly. A fact that goes stale when someone renames a
  function was never knowledge, it was a duplicate of the code.
- Secrets, credentials, tokens. Ever. The bank is readable by every agent in
  the workspace.

## One fact per entry

This is the rule that decides whether the bank stays usable.

An entry that bundles six claims cannot be scoped, confirmed, or corrected one
claim at a time — and correcting knowledge one claim at a time is the entire
reason entries exist rather than a shared document. If you learned six things,
call `remember` six times.

`remember` will refuse an entry that reads as a list or a summary, and tell you
to split it. That refusal is the rule, not an obstacle to route around.

**Scope your facts.** A fact without a scope is served everywhere, to everyone,
forever. If it is true of `apps/server` and not of the webapp, say so:

```
remember(page: "Architecture", content: "…", scope: "apps/server")
```

## Cite what a fact rests on

**A claim about code cites the code. A decision cites where it was decided.**
A citation is how a reader — and the server — can check the claim against the
evidence instead of against your word.

```
remember(
  page: "Architecture",
  content: "Redis holds only cache here; anything that must survive a restart goes in postgres.",
  kind: "DECISION",
  scope: "apps/server",
  citations: [
    { path: "apps/server/src/cache/cache.module.ts",
      lines: "12-30", sha: "<the commit you read>" },
    { issue: "ENG-42" }
  ]
)
```

- **Code:** `path` relative to the repository root, `lines` as `"40-52"` or
  `"40"`, and `sha` for the commit you read them at (omit it to cite the
  default branch as it is now). Add `repo: "owner/name"` when the workspace has
  more than one repository, and `quote` with a few words from the lines to
  catch a wrong line number.
- **Where something was decided:** `{ issue: "ENG-42" }`, `{ pullRequest:
  "<url>" }`, `{ comment: "<id>" }` or `{ run: "<id>" }`. One thing per
  citation.

The server reads every cited file itself before it writes anything. **A
citation that does not hold refuses the write** — there is no file at that
path and commit (a folder is not a file), the lines run past its end, the
quote is not in them — and the answer names the citation and the reason. Fix
that citation and call again; do not drop it to get the write through. If the
repository cannot be reached just then, the entry is written and the citation
is read later, quote and all; until it has been read it is `UNKNOWN`, and the
entry is not grounded. The answer to a write lists each citation's result, so
you can see which were read.

Cited facts are served with their proof: a **trust** tier and the result and
age of each citation's last check. Weigh them when you read:

- `HUMAN_VERIFIED` — a person confirmed it.
- `GROUNDED` — accepted, and every citation has been read and still holds:
  cited lines read the same (in place, or moved elsewhere in the file), and a
  cited issue, pull request, comment or run still exists. Ranks above uncited
  knowledge.
- `UNGROUNDED` — nothing checked backs it, or the code it cited has changed or
  gone. Check it against the code before you rely on it; if it is wrong,
  supersede it with a cited correction.

## Prefer appending to an existing page

Check `list_pages` before you write anything down, and `read_page` the page you
mean to add to: what you are about to assert may already be in its body, in
which case there is nothing to add. Pages are **few, broad and long-lived**; the
facts under them are many. A bank of forty thin pages is one nobody can
navigate, and navigability is the whole product.

Reach for `write_page` only when there is genuinely no page the knowledge
belongs under. A page needs a real body — a title with nothing underneath it is
a stub that makes the tree worse rather than better.

## Link pages to the work they govern

When a page durably governs a team, a project or an issue — this runbook covers
this project, this page explains this team's conventions — attach it with
`link_page`, so the next agent handed that work gets the page through
`pages_for` without having to find it. Do not link a page to every issue that
happened to touch it: a page attached to forty issues tells the next reader
nothing about which of them it matters to.

## Contradictions: supersede, never stack

If what you learned contradicts something in the bank, **supersede it**:

```
remember(page: "Deployment", content: "…", supersedes: "<entry id>")
```

Two contradictory facts are worse than neither, because a reader cannot tell
which one the workspace believes — and the reader is usually another agent,
acting on it. Superseding keeps the old entry for audit and stops serving it
once a person accepts your correction. Until then the old entry stays in use,
so a correction nobody has reviewed cannot take accepted knowledge away, and a
second correction to the same entry waits until the first is decided. An entry
that has been folded into the page body cannot be superseded: write the
correction as a new entry, without `supersedes`, and it goes to review like any
other claim.

`remember` searches before it writes. When near matches come back **nothing was
written**: read them, then either supersede one or pass `distinct: true` to say
this is a separate fact. Do not pass `distinct` without reading them; that is
the one move that turns this whole design into a rubber stamp.

## Consolidate when a page grows facts that read as a paragraph

`consolidate_knowledge` folds standing facts into the page body and marks them
folded, so the same thing is not served twice — once as narrative and once as
the entry it was written from.

You supply the rewritten body. Deciding how a set of facts reads as prose is the
judgment being asked for; the tool only makes sure the folded entries stop
being served separately.

## Limits you will meet, and what they mean

These are enforced by the server, not by this document, and they apply however
you call the API.

- **Untriaged entry budget.** Ten open `PROPOSED` entries per page per token. If
  you hit it, the error names the entries in your way. Consolidate or supersede
  them; do not look for another page to dump into.
- **`LOCKED` pages.** Maintained by hand. You can read them — recall and context
  both work — but you cannot append. Append to a related page instead.
- **Triage is for people.** You cannot accept, dispute or verify an entry —
  yours or anyone else's — one at a time or in bulk. You can reword, rescope or
  archive your own entries while they are still `PROPOSED`; once the workspace
  has decided about an entry, correct it by writing one that supersedes it.
- **Repeats are refused on every route.** The search-before-write runs on the
  server, so it applies however you reach the API: an exact repeat of an entry
  on the page, or a near match, comes back with the matches and writes nothing
  unless you supersede one or say the fact is `distinct`.
- **`CURATED` is the default.** `OPEN` pages exist for scratch work where volume
  genuinely does not matter.
- **Citations are checked on write.** Up to ten per entry. One that does not
  hold refuses the write with its number and the reason.

## Improving the bank

`knowledge_gaps` lists the questions agents asked that the bank could not
answer, most-asked first. It is the most direct answer available to "what should
I document next" — it says what people actually needed, rather than what
somebody thought to write down. If you just spent an hour answering one of
those questions, that hour is worth an entry.

## Your entries are reviewed

Everything you write lands as `PROPOSED` and is served to nobody until a human
accepts it. That is not a formality — it is what makes the bank trustworthy
enough to be worth reading.

Write for the reviewer, and for the stranger after them. A claim they cannot
evaluate is a claim they will archive.
