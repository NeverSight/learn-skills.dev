---
name: migrate-docs
description: Convert a repo's legacy prose about itself — ADR directories, design docs, known-issues files, glossaries, CONTEXT.md, wiki exports — into the docs/domain/ knowledge layer, one entity cluster per run, resumable from a checkpointed inventory. Use once per repo when /setup reports legacy docs, or whenever ADRs and knowledge pages coexist.
---

# Migrate docs

Convert a repo's existing prose about itself into the knowledge layer `/knowledge` defines. Load
`/knowledge` first — the layer table, the page contract, the anti-inference test and the four rules
all apply here and are not restated. Steps 2 and 5 below are `/knowledge-tend`'s drift and placement
checks run on a cluster; that skill holds their method.

The conversion is one focused effort with an end date, never a gradual drift: while ADRs and pages
coexist, every reader must consult both systems for every entity. This skill bounds that period by
the size of the legacy-doc set.

## Scope

**Existing docs only.** An entity with no legacy prose is not this skill's concern — it earns a page
the first time `/grill` or `/implement` surfaces a fact about it, which is the layer's normal lazy
path. "Migrate the whole codebase" is therefore never the task; the inventory is bounded by what was
written down, and most of a large codebase never was.

**One entity cluster per run.** The inventory below yields clusters; a run converts one and ships it
as one docs-only PR. A cluster a human could not review in one sitting is two clusters.

## 1. Inventory — once, checkpointed

Find every doc, then classify each piece by what it *is*, never by where it lives:

- **Domain facts** (decisions, invariants, lifecycles, defects, terms about a business entity) →
  absorb into `docs/domain/` pages. Cluster by the entity whose code defends each fact; the clusters
  are the page list.
- **Platform facts** (how the ORM, database, framework or host behaves here — a trap, a blind spot,
  a default nobody overrode) → `docs/platform/` pages, same contract, clustered by technology.
- **Conventions** (how code is written here) → `docs/conventions/`; a convention already in a
  tool-native file the team still uses gets an index line there, not a copy.
- **Repo facts** (how to commit, test, open PRs here) → `docs/agents/`.
- **Procedures and event records** (runbooks, postmortems, changelogs) → not facts about the domain;
  leave them where they are.
- **External-audience docs** (published guides, API references) → out of scope entirely.
- **Dead text** (nothing above applies) → propose for deletion; list it in the PR.

**Order the clusters by proximity to planned work** — the entities the next features touch convert
first, so the earliest PRs pay for themselves. Write the inventory to
`.scratch/migrate-docs/inventory.md`: clusters in order, each with its source docs and per-claim
status (`unverified | verified | dropped | hazard`). The inventory is the checkpoint: a later run
reads it, takes the first unconverted cluster, and continues. Never re-inventory a repo that has one.

## 2. Verify before converting — the step that cannot be skipped

A page asserts present tense, so conversion *mints every claim fresh*: a doc that drifted since it
was written becomes a false current-state assertion the moment it is transcribed. Run
`/knowledge-tend`'s drift check over the cluster's claims — sweeps delegated to a read-only search
subagent returning `file:line`, hits read here. A claim the code no longer supports is dropped or
rewritten to what is true now; where the *code* turns out to be the wrong side, record a hazard.
Update the claim's status in the inventory as you go.

## 3. Write each page through the anti-inference test

Most source prose dies here — motivation, history, superseded clauses, alternatives the current code
forecloses. Expect an order-of-magnitude shrink; a conversion that keeps most of the source text has
skipped the test. Give each page its `context:` and regenerate the index; a hand-edited index line is
a second home for the definition.

## 4. Delete the absorbed sources in the same commit

A surviving source beside a page is two homes for every fact, and the source is the copy nobody
updates. A source shared by two clusters is deleted with the last cluster that drains it; until
then, strike the absorbed sections and leave a one-line pointer to the page.

## 5. Repoint stranded references in that same commit

Grep for the identifiers and paths of whatever was deleted — `ADR-NNNN`-style ids, relative doc
paths, wiki links — across code comments *and* the surviving docs. Repoint each to the absorbing
page; drop the comment instead where the page adds nothing the code doesn't now say. A comment may
keep a short *local* why — what breaks if a reader "fixes" this line — but never the page's
argument (`/knowledge` states the rule). Close with the absence proof: the same grep returning
nothing.

## 6. Ship

One docs-only PR per cluster. The review is reading pages against code, and the user decides any
claim the code contradicts: either the doc lied or the code is bugged, and only they know which.
Mark the cluster converted in the inventory.

When every cluster is converted, the **entry point is the last source**: run `/knowledge-tend`'s
placement check over `CLAUDE.md` / `AGENTS.md` so every rule-shaped paragraph moves to the layer
that can falsify it and a pointer stays behind, delete the emptied legacy files, delete
`.scratch/migrate-docs/`, and the repo has one system.
