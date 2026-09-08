---
name: knowledge
description: Maintain the repo's knowledge layer — one current-state page per domain entity (docs/domain/) or platform behaviour (docs/platform/), rewritten in place, git as the ledger, the index generated from frontmatter. Use when recording a design decision, defining or sharpening domain terminology, updating docs after a code change, or when another skill needs the page contract. Legacy-doc migration is /migrate-docs; layer maintenance is /knowledge-tend.
---

# Knowledge

The knowledge layer is **one page per entity, stating how the repo is now.** No ADRs, no
known-issues ledger, no append-only anything. When a fact changes, the page is rewritten in place;
git history is the only record of what it used to say. A page asserts present tense, which makes it
falsifiable — a wrong page is a bug you can find by reading the code, not an old memo with an excuse.

## Layers

A repo's prose about itself splits by **what falsifies it**, and each layer has one home:

| Home | Holds | Falsified by |
| --- | --- | --- |
| `docs/domain/` | what a business entity is and what must hold of it | the business changing |
| `docs/platform/` | how the stack behaves *here* — the ORM, the database, the framework, the host | an upgrade or a re-platform |
| `docs/conventions/` | how code is written here — naming, layout, patterns to reach for and avoid | a reviewer disagreeing |
| `docs/agents/` | how work moves here — commit, test, track, ship | a command that stops working |
| `docs/runbook/` | manual procedures with no self-service path | the end state changing |
| `CLAUDE.md` / `AGENTS.md` | the entry point: what this repo is, and pointers to the layers above | drift from them |

`docs/domain/` and `docs/platform/` are the **knowledge pages** and share the contract below; only
the subject differs. The placement test: *is the entity a business noun or a technology?* A page
about `Subscription` is domain; a page about `Prisma undefined filters` or `Korean collation` is
platform even when a business need caused it. The entry point holds **pointers only** — a rule that
lives in `CLAUDE.md` has no falsifier but drift, so it moves to the layer that can prove it wrong.

`docs/conventions/` is an index of conventions **wherever they live**: a convention kept in a
tool-native file (an eslint config, a lint rule's rationale) gets one index line pointing there
rather than a copy. Same for pages — one home per fact, pointers elsewhere.

## Layout

```
docs/domain/
├── README.md            ← generated index, grouped by context — never hand-edited
├── subscription.md
└── …
docs/platform/
├── README.md            ← generated the same way
└── …
```

Create pages lazily — an entity earns a page when the first fact about it needs a home.

## Page format

```markdown
---
id: subscription
status: built                # intended | built — page-level; a wholly-new entity starts intended
context: billing             # the group this page is indexed under; one per page
relations:
  - {rel: classified-by, to: subscription-type}
  - {rel: reduced-by, to: scheduled-seat-reduction}
---
# Subscription

One or two sentences: what this entity IS. This opening is the term's definition — the glossary
and the page are the same document, and its first sentence is the page's index line.
_Avoid_: plan, contract    ← synonyms this repo deliberately does not use

## Lifecycle
States and transitions, as prose or a short list.

## Invariants
The rules that must hold, each with the line that defends it when a reader would break it.

## Hazards
Known defects and traps in this entity's territory — current, open, and stated plainly.
```

Sections beyond the opening definition appear only when there is content for them; an entity with no
hazards has no Hazards section. Use `Lifecycle`, `Invariants`, `Hazards` as the section names when
they apply — a fixed vocabulary is what lets an update land in the right place instead of appending
at the bottom.

**Frontmatter is an index, never a summary.** It holds only what the prose does not state — the id,
the lifecycle status, the context, machine-greppable relations. Never restate a prose claim in
frontmatter: what is stated once cannot disagree with itself.

**`context:` is a grouping claim and meets the same bar as any other.** The first cut is whatever
boundary the code already enforces — an app, a bounded context, a package — so a reader can check
it. A page belongs to one context; an entity two contexts share sits where its code lives and is
reached from the other through `relations:`. Regrouping is a frontmatter edit plus a regenerated
index, which is why the index is generated: hand-maintained grouping is the one drift nothing else
detects. On a platform page, `context:` names the technology (`prisma`, `postgres`, `nest`).

**A relation is declared once, on the page whose code enforces it** — the foreign key, the `CHECK`,
the view SQL, the service that performs the action — and labelled from that page's viewpoint
(`withdrawal --soft-deletes--> organization`, never also `organization --soft-deleted-by-->
withdrawal`). The reverse direction is derived, not written: a fact has one home and an edge is a
fact. A page's **neighbourhood** is the union of the edges it declares and the edges declared at it;
the index renders it on every line, and the lookup below computes it.

## The four rules

1. **Current state only.** The page says what is true now. How it got that way, what it replaced,
   who decided — `git log` on the page answers all of it. When a decision changes, overwrite and
   delete the reference to what was there before.
2. **One home per fact.** Every fact lives on exactly one page; other pages that need it carry a
   pointer (`see subscription.md`), never a copy. When a fact could live on two pages, it lives on
   the entity whose code defends it.
3. **Same diff as the code.** A change that alters an entity's behaviour updates that entity's page
   in the same commit — and regenerates the index. A doc update deferred to later is a doc update
   that does not happen; a deferral pile was tried and became a graveyard.
4. **`(intended)` marks the unbuilt.** Planning commits claims about code that does not exist yet.
   Tag each such claim inline with `(intended)` — on the sentence, never on a heading, so a ticket
   that builds half a section removes exactly the markers it made true; a wholly-new entity takes
   `status: intended` page-level instead. `grep -rn '(intended)' docs/domain/ docs/platform/` is the
   list of promised-but-unbuilt work. Implementation removes each marker in the diff that makes the
   claim true; a marker found on a heading is first moved onto each claim beneath it still unbuilt.

## What a page keeps — the anti-inference test

Every line must pass:

> **Would a competent reader, working from the code alone, arrive at the opposite?**

If no, cut it. A name, a type, or a test already carries most facts; the page earns its length only
with what code cannot show. The highest-value line is a decision the obvious reading actively
fights — where the textbook answer is the wrong one here. Spend words there and nowhere else.

**Keep:** invariants a reader would "fix" into bugs; constraints invisible in code (a client keying
on a status code, a measured population, a partner's rate limit, a deployment topology); deliberate
omissions; a rejected alternative *only while a reader starting from the current code could still
choose it* — once the code forecloses it, it is history, and history goes.

**Cut:** motivation, narrative, how a fact was learned (minimal provenance: keep the failure mode,
cut the story); anything restating the code; references to anything ephemeral — tickets, specs,
`.scratch/` paths, feature slugs. State the fact, not where it was decided: *no ticket asked for
it* → *nobody asked for it*.

A claim about a system the repo does not contain — the host, a managed database's extension policy,
a partner's API — has no code to falsify it, so the page names the primary source it was read from
beside the claim, or tags it `(unverified)`. A source is something a reader can open: vendor
documentation, a support case, a measured run. This holds on every layer in the table, runbooks
included.

Point at a page from code in **one line**. The code site may add a short *local* why — why this
ordering, what breaks if a reader "fixes" this line — when that fact passes the anti-inference test
at the line and has no home on the page. Never restate the page's argument at the call site: two
copies drift, and the code copy is the one nobody updates.

## Sharpening, while designing

When maintaining the model live (a grill session, a design discussion):

- **Challenge terms against the pages.** A term used contrary to its page's definition gets called
  out immediately: "subscription.md defines X — you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** Propose one canonical term; record the losers under `_Avoid_`.
- **Cross-reference the code.** When the user states how something works, check whether the code
  agrees, and surface contradictions rather than recording the claim.
- **Write inline, the moment a term or decision crystallises.** Batching is how it gets lost.

## The index is generated

`README.md` in each knowledge directory is built from frontmatter and each page's first sentence,
grouped by `context:`, and is never edited by hand — an edited index is a second home for the
definition. Regenerate after any page edit (`/knowledge-tend` runs it and diffs; the review's
Knowledge axis fails a stale one). The script is [index.sh](./index.sh) in this skill's directory:

```bash
bash <path-to-this-skill>/index.sh docs/domain > docs/domain/README.md
bash <path-to-this-skill>/index.sh docs/platform > docs/platform/README.md
```

It writes the preamble too, so the whole file is output. A page whose first sentence makes a poor
index line has a poor definition — fix the sentence, not the index.

## Integrity check

```bash
grep -rho 'to: [a-z0-9-]*' docs/domain/ docs/platform/ | sed 's/to: //' | sort -u | while read id; do
  grep -qrl "^id: $id$" docs/domain/ docs/platform/ || echo "dangling relation: $id"
done
```

```bash
grep -rlE "to: <id>\}" docs/domain docs/platform   # the pages declaring an edge at <id>
```

Dangling relations and reciprocal pairs fail the review's Knowledge axis. The checks validate
references, not truth — truth is checked by reading, which is why pages stay short enough to read.
The second command is the **neighbourhood** lookup: together with the page's own `relations:` it
names every page that asserts something about `<id>` — the pages a change to `<id>`'s code can make
stale, and the scope `/implement`, `/review`, `/grill` and `/knowledge-tend` read one hop out to. Shape and placement
drift — a page in the wrong layer, an oversized page, a stale index — are `/knowledge-tend`'s job.

## Migrating and tending

A repo arriving with prose about itself — ADRs, design docs, known-issues files, glossaries —
converts through `/migrate-docs`: one checkpointed inventory, one entity cluster per run. Keeping
the layer's *shape* right afterwards — placement, grouping, page size, drift against code, entities
still without a page — is `/knowledge-tend`. Neither is restated here: this file is loaded on every
page edit and carries the contract only.
