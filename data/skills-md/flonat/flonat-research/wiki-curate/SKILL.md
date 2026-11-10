---
name: wiki-curate
description: "Audit the Research Vault concept wiki read-only for fragmentation, missing tags, write-only concepts, and draft or anatomy conformance, producing a Markdown report. Use when assessing wiki quality before maintenance. Not for promoting or merging concepts; use $wiki-grow or $wiki-merge."
allowed-tools: Bash, Read
argument-hint: "(no arguments)"
skill-dependencies: [wiki-merge]
---

# Wiki Curate — Read-only Audit

> Reads the vault wiki and produces a triage report. Never writes.
> Detects four classes of issue: **overlap clusters** (fragmentation),
> **tag gaps** (untagged concepts + orphan/near-duplicate tags),
> **write-only concepts** (zero backrefs from the corpus), and
> **anatomy/lifecycle** issues (drafts awaiting curation + curated
> pages that regressed the concept anatomy). Companion to `wiki-grow`
> (which adds new concepts) and `wiki-merge` (which collapses overlap
> clusters).

## When to Use

- After a `wiki-grow` run, to check what the new stubs introduced.
- Before deciding which concepts to refine or merge.
- Monthly, to keep the wiki's signal-to-noise ratio high.

## When NOT to Use

- For project knowledge folders — those are audited via
  `knowledge-lint`.
- For atlas topics — that's `research-atlas-audit`.
- For mechanical edits — this skill never writes. Use `wiki-merge` to
  collapse overlap clusters and the planned tag-inference pass in
  `wiki-grow` to backfill missing tags.

---

## Architecture

```
scripts/wiki-curate-scan.py
  ├─ reads:  ~/vault/concepts/*.md
  │           ~/vault/atlas/<theme>/*.md         (for backref counts)
  │           ~/vault/books/<slug>/*.md         (for backref counts)
  │           <research-root>/<theme>/<proj>/CLAUDE.md   (for backref counts)
  └─ writes: /tmp/wiki-curate-report.md
             /tmp/wiki-curate.json
```

The skill is invoked by running the Python orchestrator. No Claude
dispatch — the audit is pure deterministic analysis.

---

## What it checks

### A. Overlap clusters (the headline feature)

Concept slugs are tokenised (kebab parts, stopwords removed, trailing
`s` stripped for crude singularisation). Any token shared by ≥2
concept slugs forms a **cluster**.

Within each cluster, the **canonical winner** is suggested by:

1. Human-curated (`auto_generated: false`) beats auto-generated.
2. Longer body beats shorter.
3. Alphabetically earliest slug breaks ties.

Pair-level **title-Jaccard ≥ 0.40** is flagged as 🔥 high confidence
(distinct from "shared keyword" — the slugs are substantively similar).

Example output from a recent run:

```
### `goodhart` (size 3)
- `goodhart-resistance`  — auto, 3533 chars
- `goodhart-taxonomy`    — auto, 3902 chars
- `goodharts-law`        — curated, 3111 chars  ← canonical (suggested)

Suggested action: wiki-merge goodharts-law goodhart-taxonomy goodhart-resistance
```

### B. Tag coverage

- **Untagged concepts** — frontmatter has no `tags:` field. Filters
  on `/concepts?tag=X` won't surface them.
- **Orphan tags** — used by exactly one concept. Either expand or
  retire.
- **Near-duplicate tags** — pairs differing only by case / hyphen /
  trailing `s` (e.g. `ml` vs `machine-learning`, `model` vs `models`).

### C. Backref health

For each concept, count:
- **Incoming wikilinks** — `[[slug]]` references from atlas topic
  bodies, book chapters, and project CLAUDE.md files.
- **Corpus mentions** — case-insensitive whole-word slug occurrences
  in the same corpus.

Concepts with **both counts zero** are flagged as write-only — they
don't surface anywhere. Two remedies:
1. Insert `[[slug]]` references in the atlas topics that should
   reference the concept (mechanism A from this session — body
   wikilinks auto-surface as chips on the topic page).
2. Add the slug to `~/vault/concepts/.denylist` and delete
   the file — accept the concept isn't carrying weight.

### D. Anatomy & lifecycle

The `status:` frontmatter field is the lifecycle axis: `draft`
(no guarantees, may be project-voiced) → `curated` (conforms to the
concept anatomy). Status is read from frontmatter with the same
fallback as atlas-workspace (`auto_generated: true` → draft, else
curated) so pages predating the field classify correctly. The
anatomy is defined in `packages/research-atlas-schema/schema.md` → "Concept
File Schema":

- `## In one line` — required definition block (machine-anchored).
- `## In my portfolio` — the boundary below which project-voiced
  prose ("the project", "this paper", "we propose", …) is allowed.

Two lists are reported:

- **Drafts awaiting curation** — every `status: draft` concept, with a
  ✓/— table showing which anatomy pieces already exist (`In one line`,
  `In my portfolio`) and how many project-voice phrases sit above the
  boundary. Higher counts mean more restructuring to do.
- **Curated pages violating the anatomy** — pages marked `curated` that
  regressed: missing the `In one line` definition, or project-voice
  prose above the `In my portfolio` boundary (including a portfolio
  section under a non-canonical heading). These are the priority fix —
  a curated page is supposed to conform.

The curation action itself is a Claude-driven restructuring edit (this
skill is read-only); see the triage workflow below.

---

## Output

`/tmp/wiki-curate-report.md` with three sections (A/B/C) and a
suggested triage order. Stdout from the script:

```
Concepts: 14 (6 curated, 8 draft)
Overlap clusters: 0
Drafts awaiting curation: 8
Curated pages violating anatomy: 1
Untagged: 8/14
Write-only (no backrefs): 0
Report: /tmp/wiki-curate-report.md
JSON:   /tmp/wiki-curate.json
```

The JSON sidecar feeds the planned `wiki-merge` skill so it can
read the suggested winner/fold-in lists without re-running the
detection.

---

## Modes

| Mode | Invocation | Behaviour |
|------|-----------|-----------|
| **Default** | `wiki-curate` (or `uv run python scripts/wiki-curate-scan.py`) | Run all three audits, write report + JSON, print summary to stdout. Read-only. |

There's no `--autonomous` flag here — the skill is already pure-read
and idempotent. Future cron integration: chained after the Saturday
06:45 `wiki-grow` run, the audit can land in
`log/audits/wiki-curate-YYYY-MM-DD.md` for a weekly health snapshot.

---

## Triage workflow

After running:

1. **Section D regressions first** — any curated page flagged as
   violating the anatomy is a bug: it claims `curated` but doesn't
   conform. Fix in place (add `## In one line`, or rename/add the
   `## In my portfolio` section and move project-voiced prose under it).
2. **Section A** — every overlap cluster fragments knowledge. Pick a
   canonical winner (often the suggestion) and run `wiki-merge
   <winner> <fold-in-slugs>` to collapse. Re-run `wiki-curate` to
   confirm the cluster is gone.
3. **Section D drafts** — curate each `draft` to the anatomy:
   - Extract a 2-4 sentence project-agnostic definition into
     `## In one line`.
   - Keep the cited, stable knowledge in encyclopedia voice.
   - Move all project-voiced prose under `## In my portfolio`.
   - Verify `references:` keys are canonical Paperpile keys
     (rekey hand-minted lookalikes).
   - Flip `status: draft` → `status: curated` in frontmatter and set
     `last_updated`.
4. **Section B** — untagged concepts won't surface in the tag filter.
   Until the planned `wiki-grow` tag-inference pass lands, add tags
   manually for the auto-promoted stubs you care about.
5. **Section C** — write-only concepts. Decide per-concept: link from
   a topic, denylist, or accept.

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| `wiki-grow` | Writes the auto-promoted concepts this skill audits. |
| `wiki-merge` | Acts on the overlap clusters this skill finds (planned — not yet built). |
| `compile-knowledge` | Upstream of `wiki-grow`; produces the project knowledge articles that get promoted. |
| `research-atlas-audit` | Audits atlas topics; complementary lens. |
| `knowledge-lint` | Audits per-project knowledge folders; complementary lens. |
