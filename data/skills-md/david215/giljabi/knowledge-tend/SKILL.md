---
name: knowledge-tend
description: Keep the knowledge layer's shape true — placement across docs/domain, docs/platform, docs/conventions and the entry point; the generated index; page size and grouping; claims re-verified against code; and a page drafted for a not-yet-documented entity. Every fix is proposed with file:line evidence and applied on approval. Use scoped before a grill, inside /migrate-docs, at a feature's close, or standalone — "tend the docs", "is organization.md still true", "document the seat module".
---

# Knowledge tend

`/knowledge` says what a page is. This skill checks whether the **layer** still fits the repo — the
questions no single page edit asks. Load `/knowledge` first; its layer table, page contract and
anti-inference test are the rules applied here and are not restated.

Five checks, each with a mechanical output and then a proposed fix. **Nothing is applied without
approval, with one exception: the generated indexes**, which are regenerated on sight — they are
output, not judgment, and the contract already says nobody edits them. Everything else is a
proposal: present it with its evidence (`file:line`, a diff, a count you read rather than grepped)
and apply the ones the user accepts; a layer that reshapes itself unsupervised is a feedback loop
with no test.

## Scope first

```
/knowledge-tend                        # whole layer: checks 1–3; 4 and 5 only when named
/knowledge-tend <entity | path | dir>  # entities named, or those whose code lives under the path
```

Check 4 (drift) reads code for every claim on a page and is the expensive one — it never runs
repo-wide unasked. Callers scope it:

| Caller | Scope | Runs |
| --- | --- | --- |
| `/grill`, before round one | every `docs/domain/` and `docs/platform/` page the plan will touch | 1–4 — a stale page makes the interview lie |
| `/review`, Knowledge axis | every page the diff touches, plus neighbourhood | 1–2 and 4 as pass/fail, 3 as proposals — the primary run |
| `/giljabi` phase 6, features of more than one slice | the feature's pages | 2 — index and relations after every slice landed |
| `/migrate-docs` | the cluster | 1, 4, 5 — its verify, place and repoint steps are these |
| standalone | as given | as given |

## 1. Placement

For every page in scope, and for every rule-shaped paragraph in `CLAUDE.md` / `AGENTS.md`, apply
the layer table's falsifier test: *what would make this false?* The business → `docs/domain/`; an
upgrade → `docs/platform/`; a reviewer → `docs/conventions/`; a command → `docs/agents/`. The entry
point keeps pointers only.

Misfiled → propose the move. A move repoints every reference in the same change: grep the old path
across code comments and the surviving docs (excluding `node_modules`, `.scratch`, `.git`), repoint
each, and close with the absence proof — the same grep returning nothing. A code comment that only
said "see the page" follows the page; one carrying a local why keeps it.

A convention living in a tool-native file that nothing indexes → propose one index line in
`docs/conventions/README.md`, not a copy. A tool-native file for a tool nobody uses any more →
propose moving its content into `docs/conventions/` and deleting the file.

## 2. Index and relations

```bash
diff <(bash <knowledge-skill-dir>/index.sh docs/domain) docs/domain/README.md
diff <(bash <knowledge-skill-dir>/index.sh docs/platform) docs/platform/README.md
```

plus `/knowledge`'s dangling-relation check. Any output is a finding: a stale index is regenerated
(the one exception above); a dangling relation names a page that was
renamed or never written, and the fix is the user's call. A page with no `context:` lands under
`uncategorised`, which is a finding too.

A **reciprocal pair** — `A → B` declared on A and `B → A` declared on B — is a finding: an edge is
declared once, on the page whose code enforces it (`/knowledge`). Propose removing the derived side;
the neighbourhood lookup keeps the reverse reachable.

```bash
for f in docs/domain/*.md docs/platform/*.md; do id=$(sed -n 's/^id: //p' "$f" | head -1)
  grep -o 'to: [a-z0-9-]*' "$f" | cut -d' ' -f2 | while read t
    do grep -qlE "to: $id\}" docs/domain/$t.md docs/platform/$t.md 2>/dev/null && echo "reciprocal: $id <-> $t"; done; done
```

## 3. Shape

Mechanical signals that a page wants splitting or regrouping — each a *proposal*, since a long page
can be a rich entity and a short one a thin one:

- **Size** — a page over 100 lines is *when you look*, not a limit: a central entity whose lines
  carry file paths and a Hazards section runs 100–140 by design. The rule is the **noun-section
  test**: a `##` section that names its own noun, cites its own code and has Hazards that reference
  it (`## Purge Job` inside `organization.md`) is a page waiting to be cut out. Propose the split
  and the relation that links them; a long page that fails the test is left alone.
- **Fan-out** — a page with more than ~6 `relations:` is usually a context, not an entity.
- **Context vs code** — a page whose `context:` names one boundary while every file it cites lives
  in another. Propose the regroup: a frontmatter edit and a regenerated index.
- **Empty groups** — a `context:` used by a single page, once the layer has several. Propose merging
  it into a neighbour or leave it, with the reason.

## 4. Drift

The conversion step from `/migrate-docs`, run on a page that already exists: **every claim is
re-minted**. Scope is the named pages **plus their neighbourhood** (`/knowledge`'s lookup): a
neighbour is checked only for the claims it makes about the named entity, since those are the ones
the named entity's code can have made stale. For each claim on each page in scope, check the code
still agrees — delegate the sweeps
to a read-only search subagent at the `fast` tier returning `file:line` and the quoted line, never a
bare count, and read the hits yourself. Three outcomes, each a proposal:

- the code agrees → nothing;
- the code disagrees and the code is right → rewrite the claim to what is true now;
- the code disagrees and the code is wrong → record it under `## Hazards` and, if a feature is in
  flight, a line in its `findings.md`.

A claim about something outside the repo (a frontend, a partner) is checked for the half the repo
holds and stated as external for the rest. Production data is read as `/grill` reads it — read-only,
aggregates first — and only when the claim is about a population.

## 5. Coverage — a page for an undocumented entity

When the user names an entity or module with no page, run `/migrate-docs`'s method with the **code as
the source**: sweep the module's call sites, guards, constraints and tests for the facts that pass
the anti-inference test — an invariant a reader would "fix", a constraint invisible in the code, a
deliberate omission, a rejected alternative still choosable — and draft the page under the layer and
`context:` the placement test gives. Most of what a module does fails the test and is not written;
a first draft of five lines is normal. Present the draft for approval, then regenerate the index.

Do not sweep a codebase for entities without pages. A page is earned by a fact that needs a home —
the first grill or implement that touches an entity writes one — so "document everything" is never
this skill's task.

## Report

One list, grouped by check, each item: what, evidence, proposed fix, and — after approval —
applied or declined. Finish with the two mechanical results (index diff, dangling relations) as
they stand after the applied fixes. No prose about checks that found nothing.
