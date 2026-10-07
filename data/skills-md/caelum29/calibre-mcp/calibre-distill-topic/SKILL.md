---
name: calibre-distill-topic
description: "Synthesize ONE topic across MULTIPLE Calibre books into a single, concept-keyed agent skill — original multi-source authorship (decision frameworks, cross-source config tables, an explicit where-authors-agree/disagree section), with a full ISBN bibliography that doubles as a live-source binding for later deep dives. Drives the calibre-mcp server (chapter maps, in-book keyword + semantic search) to pull a thin topic slice from each source; no temp files, no Python. Use when the user wants a topic study aid built from several books (\"kafka reliability from my Kafka shelf\", \"database indexing across these 3 books\"). Requires ≥3 sources; works on EN + RU/UK books. Sibling of calibre-distill — single-book requests belong there."
---

<!--
Provenance: extends the calibre-distill recipe (this repo, skills/calibre-distill/) into the
D1.7 topic-aggregate artifact class (docs/dev/PRODUCT-DECISIONS.md). Reuses calibre-distill's
Step 1 (resolve), Step 2/2.6 (chapter map + targeted in-book access), and Step 9.5
(write-back) patterns; the synthesis is concept-keyed multi-source authorship, NOT a
per-book recount. Validated hand-run: docs/prompts/ideas/distill-samples/topic-kafka-reliability/.

Cross-agent notes (informational; ignored by host agents):
  - Compatible skill roots: Claude Code (~/.claude/skills, .claude/skills), GitHub
    Copilot CLI (~/.copilot/skills, ~/.agents/skills, .github/skills), Amp
    (.agents/skills, ~/.config/agents/skills).
  - `allowed-tools` intentionally omitted to stay agent-neutral. The skill needs the
    calibre-mcp tools (calibre_search, calibre_get_content, calibre_semantic_search,
    calibre_get_book, and — for optional write-back — calibre_update_book) plus file
    read/write for the generated skill.
  - Argument hint: <topic phrase> [book ids/titles/query] [skill-name-slug]
  - Sibling skill: calibre-distill (single-book distiller). This skill is for the
    multi-book topic-synthesis case; single-book requests belong there.
-->

# Calibre Distill — Topic

Synthesize a **single topic** across **several books** in your Calibre library into one
concept-keyed agent skill. Where `calibre-distill` mirrors one book, this skill mirrors
**nobody's structure**: it takes a thin topic slice from each of ≥3 sources and re-authors
them into original, multi-source knowledge — a decision framework, per-concept sections, a
cross-source config table, and an explicit **"where the sources disagree or complement"**
section (the whole point of the aggregate class).

## Why this is a different skill from calibre-distill

- **calibre-distill** = one book → one skill, organized by the book's chapters. Private
  study aid (raw material).
- **calibre-distill-topic** = N books → one skill, organized by **concept**. This is the
  distributable D1.7 artifact class: no single book contributes its "heart", so it's
  original synthesis (what every textbook does), not an abridgment of any one work.

If you have exactly one book, or the user wants a faithful per-book distill, use
`calibre-distill` instead — route single-book requests there.

## What it produces

A skill directory with:
- **`SKILL.md`** (~2.5–4K tokens) — concept-keyed synthesis (layered overview → decision
  framework → per-concept sections → cross-source config table → disagree/complement →
  L4 bibliography). No chapter files by default: the topic skill IS the pre-synthesized
  bundle.
- **`distill.manifest.yaml`** — a `kind: topic-aggregate` provenance sidecar (D2.8 shape),
  never loaded into L1 context.

---

## Skill Locations

Pick a destination the user's host agent can discover (same roots as calibre-distill).
Probe in order:

1. Claude Code personal: `~/.claude/skills/`
2. GitHub Copilot CLI personal: `~/.copilot/skills/` → `~/.agents/skills/`
3. Amp global: `~/.config/agents/skills/`
4. Project-local: `.claude/skills/` → `.github/skills/` → `.agents/skills/`

When more than one valid root exists, ask once and remember for the session — do not
silently default. **L1-budget note (E5):** every installed skill adds its description to
the always-loaded metadata level; when the target is a global root, warn the user and offer
a per-project install or symlink for selective activation.

**This skill itself** lives in the calibre-mcp repo (`skills/calibre-distill-topic/`).
Install it by copying or symlinking to `~/.claude/skills/calibre-distill-topic/`. The
calibre-mcp MCPB bundle **cannot** ship skills — install separately from the MCP server.

---

## Step 1 — Input & out-of-scope check

Parse the input into a **topic phrase**, optional **book references** (ids / titles /
query), and an optional `SKILL_NAME` slug.

If no topic phrase is provided, stop:
> "calibre-distill-topic needs a topic — give me a topic phrase, optionally with book refs
> and a skill slug. Example: `calibre-distill-topic "kafka reliability" 187 182 571 186
> kafka-reliability` or `calibre-distill-topic "database indexing"`."

Requires the **calibre-mcp** server connected. If its tools aren't available, say so and
stop.

---

## Step 2 — Source discovery (enforce the ≥3-source rule)

Find candidate books for the topic:
- If the user named book refs, resolve each (`calibre_get_book` for numeric ids;
  `calibre_search` for titles/queries) and confirm title/authors.
- Otherwise `calibre_search` the library on the topic (search `title`, `tags`, and
  `comments`; e.g. `calibre_search(query="kafka")` then narrow) and present candidates.

Present the candidate set with **id / title / authors** and ask the user to confirm or
edit the source set.

**Enforce the D1.7 minimum: 3 sources.** With fewer than 3 confirmed sources, do not build
a topic skill — offer either:
- proceed as a plain per-book distill (**hand off to `calibre-distill`**), or
- stop and let the user add more sources.

A ~90%-one-book "topic" skill re-enters the per-book legal analysis, which is why the floor
is load-bearing (D1.7 validity condition 1).

Record `SOURCES = [{ id, title, authors, formats }]`.

---

## Step 3 — Per-source topic location

For **each** source, find where the topic lives — do NOT read whole books.

1. **Chapter map:** `calibre_get_content(id=<id>, structure=true)` → `chapters:
   [{ n, heading, startChar, endChar, approxTokens, cursor }]`, plus `hasToc`, `detector`,
   `totalChars`, `format`, `backend`.
2. **Rank chapters by topic relevance:**
   - `calibre_search(scope=book, id=<id>, query="<topic terms>")` (FTS) → hit offsets; map
     each hit to a chapter by finding the chapter whose `[startChar, endChar)` contains it.
     Chapters with the most hits rank highest.
   - and/or `calibre_semantic_search(scope=book, bookId=<id>, query="<topic>")` → ranked
     passages with offsets → same offset→chapter mapping. (Needs the book indexed via
     `calibre_build_index bookId=<id>`; if not indexed, use FTS and say so.)
3. **Vocabulary adaptation — this matters.** Books approach a topic from different angles
   (an ops book ≠ a reference book ≠ a how-to). If the topic's default terms return few
   hits for a book, **re-probe with book-appropriate synonyms** before concluding the book
   is thin. The Kafka prototype needed different term sets per book (e.g. "reliability /
   durability / acks" for the reference book vs "data loss / retention / disk" for the ops
   book).
4. **Select the top 1–3 chapters per source** — the topic slice. Record
   `topic_chapters` as `{ n, heading }` pairs (both together — bare "ГЛАВА N" headings
   don't discriminate).

If a source has no relevant chapters after vocabulary adaptation, drop it (and re-check the
≥3 floor).

---

## Step 4 — Pre-flight estimate

Before reading anything, present the plan and get confirmation:

```
📚 Topic: <topic phrase>
🗂  Sources (<N>):
   [<SRC>] <Title> — <Authors>   (id <id>) → chapters <n(heading), …>  ~<K> tokens
   …
📄 Topic slice total: ~<K> tokens (vs ~<K> tokens whole-book — reading only the slices)
📁 To generate: SKILL.md (~3K tokens) + distill.manifest.yaml

➡  Proceed?
```

Assign each source a short citation tag (`SRC`) up front — e.g. `DG2`, `KiA`, `KTiP`,
`KS` — from author/title initials; these tags carry through every extract and the final
skill. Wait for confirmation.

---

## Step 5 — Per-source extraction (topic slices only)

For each source, read **only its selected chapters** via their `cursor`
(`calibre_get_content(id=<id>, cursor=<chapter.cursor>, maxChars=<budget>)`; follow
`nextCursor` within a chapter, stop at the next chapter's `startChar`). Nothing else from
the book enters context.

If the host supports subagents, run the per-source extractions in parallel (one subagent
per source, each returning its structured extract); otherwise do them sequentially.

Produce a **structured extract per source** — not prose:
- **Decision rules** — "When X, do Y, because Z."
- **Config facts** — parameter names, values, defaults, thresholds (these are facts —
  keep them **exact**).
- **Named concepts** — the source's own terminology, precisely.
- **Anti-patterns** — what fails and why.

Each item cited `(SRC chN)`.

**HARD RULES per extract (D1.3, applied per source):**
- **Own words only. Zero verbatim sentences.** Close paraphrase of distinctive expression
  still counts as copying.
- **No lifted code or tables.** Re-author any example/table on a fresh scenario; parameter
  names, values, and numbers are facts and stay exact, but the prose and composition are
  re-expressed.
- **Verbatim quote budget** (if you must quote at all): ≤ 25 words per quote, ≤ 200 quoted
  words total across the whole skill, non-contiguous, always attributed.
- **RU/UK sources → extract in English.** Read natively, write the extract in English.

---

## Step 6 — Synthesize the SKILL.md (concept-keyed, never source-keyed)

Merge the per-source extracts into one SKILL.md (~2.5–4K tokens), organized by **concept**.
Required sections (from the validated prototype):

1. **Layered overview** ("read this first") — the topic as a stack/system the reader
   assembles, noting which source is strongest for each layer.
2. **A decision framework** — a questionnaire/table that turns the topic into per-case
   choices, with the rules the sources commit to.
3. **Per-concept sections** — one section per major concept, weaving sources together under
   the concept, each claim cited `(SRC chN)`.
4. **A cross-source config quick-reference table** — parameter | value the sources commit
   to | source(s). Facts stay exact.
5. **"Where the sources disagree or complement"** — **required; the aggregate class's whole
   point.** Always hunt for at least 2 genuine tensions or complements (e.g. one book's
   ordering advice vs another's; one book's mechanism vs another's failure mode; the angle
   split — "book A = how to choose, book B = what it is, book C = how it breaks"). If you
   can't find real tensions, the sources may be too similar — reconsider the set.
6. **Bibliography & going deeper (L4)** — Step 7.

**Balance:** no single source may dominate. Track a rough `contribution_frac` per source;
**no source > 0.50** (D1.7 validity condition 1). If one book is carrying the skill,
either broaden the other sources' slices or reconsider whether this is really a topic skill.

---

## Step 7 — L4 bibliography block (ISBN binding)

The bibliography is mandatory (attribution is an EU/UA precondition, not a courtesy) and it
**doubles as the live-source binding**: a recipient who owns a source gets depth on demand.

For **each source**, list:
- **Title**, **authors**, **ISBN-13** (from library metadata; if missing and **writes are
  enabled**, backfill once with `calibre_extract_isbn(id, apply=true)` — an offline front-matter
  scan — else fall back to the `fallback_key` below — E2).
- **Topic chapters** as `{ n, heading }` pairs (n + heading TOGETHER — bare "ГЛАВА N"
  doesn't discriminate across chapters).
- **The resolve recipe** so the reader can open the exact slice in THEIR copy:
  `calibre_search(identifiers:isbn:<isbn>)` → local id →
  `calibre_get_content(id, structure=true)` → match the chapter headings/ordinals → mint
  **fresh** cursors on their own extraction.

**No-ISBN source →** provide a `fallback_key` (`title:"…" AND authors:"…"` query) and mark
it unverified. **NEVER put char-offset cursors in the artifact** (D1.3 #5 / D2.4 — cursors
are non-portable across machines/editions and are inducement-optics risk).

Close the bibliography with: all prose is original synthesis; if a book isn't in the
reader's library the skill stands alone; consider buying each book (each covers far more
than this one topic).

---

## Step 8 — Emit the manifest

Write `distill.manifest.yaml` next to SKILL.md, following the prototype's D2.8 shape
exactly:

```yaml
manifest_schema: 1
kind: topic-aggregate
skill:
  name: <skill_name>
  digest: "sha256:TBD"          # sha256 of the distillate tree at publish time
  revision: 1
identity:
  topic: <topic-slug>           # the topic IS the identity
  language: en
sources:                        # each ≤ the contribution cap
  - isbn13: "<isbn or null>"
    title: "<Full Title>"
    work: "<author:work-slug>"  # discovery grouping only (optional)
    authors: ["<Author>", …]
    edition_note: "<e.g. RU translation of …>"   # optional
    topic_chapters: [{ n: <N>, heading: "<heading>" }, …]
    contribution_frac: <0..1>
    source_content_hash: "sha256:TBD"            # hash of the extracted text read
    # no-ISBN source additionally carries:
    # fallback_key: 'title:"…" AND authors:"…"'
    # identity_confidence: unverified
distillate:
  license: "CC-BY-4.0"
  transform: "multi-source-topic-synthesis"
  files: [SKILL.md]
  quote_budget: { max_words_per_quote: 25, max_total_words: 200, used: <N> }
provenance:
  generator: "calibre-mcp"
  generator_version: "<x.y.z>"
  recipe: "calibre-distill-topic"
  recipe_version: "1.0.0"
  distiller_model: "<model id>"
  generated_at: "<YYYY-MM-DD>"
  method: "per-source topic-slice extraction -> concept-keyed cross-source synthesis"
quality:
  structural: pass              # bibliography + per-source citations present
  legal_gate:                   # D1.4 checks — NOT YET AUTOMATED (manual until prompt 04)
    shingle: not-run
    compression_floor: pass
    heading_match: pass         # concept-keyed; no source ToC mirrored
    cursors: pass               # no char-offset cursors in the artifact
  grounding: not-run
comparison:
  identity_key: "topic:<topic-slug>"
  sources_fingerprint: "sha256(sorted ISBN list + work slugs)"
  schema: 1
  distiller_family: "<model family>"
  recipe_version: "1.0.0"
  revision: 1
```

Leave `sha256:TBD` placeholders where a digest isn't computed at generation time; fill
`quote_budget.used` with the actual quoted-word count. The `legal_gate` checks stay
`not-run` (shingle/grounding) or manually-assessed (`pass`) until prompt 04's verifier ships.

---

## Step 9 — Self-check before reporting

Manual until the automated verifier lands. Scan your own output:

- **Verbatim leakage:** re-read each section for sentences you may have carried over from a
  source. Any distinctive phrasing that could be the author's → re-author it. (When the
  verifier ships, it runs an 8-gram shingle probe with a title/attribution allowlist — the
  bibliography's own titles are the known false-positive, per D1.7 finding a.)
- **Contribution balance:** confirm no source contributes > 0.50; the set should feel
  genuinely multi-voiced.
- **Quote budget:** ≤ 25 words per quote, ≤ 200 quoted words total; every quote attributed.
- **Cursors:** zero char-offset cursors anywhere in SKILL.md or the manifest — only ISBN +
  `{ n, heading }` bindings.
- **Disagree/complement section present** with ≥2 real tensions/complements.

Any failure → fix before reporting.

---

## Step 10 — Report (and optional write-back)

Report:

```
✅ Topic skill created: $SKILLS_HOME/<skill_name>/

📚 Topic: <topic phrase>   (<N> sources)
   [<SRC>] <Title> — contribution ~<frac>   chapters <n(heading), …>
   …

Files generated:
  SKILL.md               — concept-keyed synthesis   (~X tokens)
  distill.manifest.yaml  — provenance sidecar (topic-aggregate)

Self-check: contribution balance <ok/flag> · quote budget <used>/200 · cursors none
```

**Optional Step-9.5-style write-back** (opt-in; requires the write gate
`CALIBRE_MCP_ENABLE_WRITE=1`): offer to tag each source book with the topic tag (+ marker
`distilled-topic`) and append a short distill note to `comments`, so
`calibre_search "tags:<topic>"` later finds the whole source set. **Preview-first** — show
the proposed tag/comment diff and **ask before applying**. **Read → union → write** (
`set_metadata` replaces the whole field, so merge existing tags first — never clobber). If
the write tools are absent, report "skipping library stamping (writes disabled)" and finish.

---

## Quality Rules

1. **Concept-keyed, never source-keyed** — sections are topics/concepts, not "what Book A
   says". Source-keyed structure re-enters the per-book analysis.
2. **≥3 sources, no source > 0.50 contribution** — else it's a per-book skill wearing a
   topic name (hand off to `calibre-distill`).
3. **Own words only, per source** — zero verbatim sentences; parameter names/values/numbers
   are facts and stay exact. Close paraphrase counts as copying.
4. **No lifted code or tables** — re-author on fresh scenarios; keep the facts exact.
5. **RU/UK sources read natively, written in English.**
6. **The disagree/complement section is mandatory** — it's the evidence of original
   multi-source authorship; a per-book recount structurally can't produce it.
7. **Bibliography with ISBNs is mandatory** — attribution + buy-the-book optics + it's the
   L4 binding. `{ n, heading }` together; never char-offset cursors.
8. **Verify before you claim** — use `calibre_search scope=book` to confirm a config value
   or framework is really in that source before attributing it.
9. **Front-load SKILL.md** — most important content first (overview → framework); keep the
   body under ~4,000 tokens.
