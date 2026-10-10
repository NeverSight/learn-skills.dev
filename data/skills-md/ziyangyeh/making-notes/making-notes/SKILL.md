---
name: making-notes
description: Use this skill when turning Zotero papers into grounded Obsidian notes using NotebookLM, with Zotero annotations as evidence links. It covers PDF ingestion into NotebookLM through any client, user/context/template-guided questions, evidence extraction, Zotero underline/highlight/box annotations, annotation comments, and Obsidian in-text references that jump back to Zotero annotations.
---

# Making Notes

Create grounded Obsidian notes from one or many Zotero papers with NotebookLM answers and Zotero annotations as evidence links.

## Core Contract

- Zotero metadata is the source of truth for paper identity, attachment keys, PDF paths, authors, years, and in-text citation labels.
- NotebookLM `source_id` is authoritative for source-level routing. Do not auto-move evidence to another paper because cross-PDF fuzzy matching looks better.
- NotebookLM `cited_text` is the primary evidence seed. Clean and expand it to a complete sentence or paragraph before creating a Zotero annotation.
- NotebookLM answer quotes are fallback evidence only, used when `cited_text` cannot be made annotation-ready.
- Ask user-provided questions verbatim.
- When a paper-reading template is provided, derive a question plan from its sections before asking NotebookLM, unless the user asks for explicit questions only.
- When personal research context is provided, use it to frame relevance and "why this matters to my research" questions. Do not treat that context as paper evidence or create Zotero annotations for it.
- Preserve every cited evidence item. One answer claim may cite multiple papers; each evidence item gets its own Zotero annotation.
- Default annotation style is red underline. Users may override with `--annotation-type` and `--color`, or per-evidence `type` and `color`.
- Zotero annotation's `annotationComment` must be non-empty and should be the exact sentence or concise claim that will be cited in the note.
- Before creating annotations, ensure every evidence object has a `comment` value. Do not rely on empty default comments.
- Obsidian citation text must be Zotero-derived, e.g. `(Xing et al., 2025, p. 4)`, and link directly to the Zotero annotation key.

## Template-Guided Notes

Use `references/template-guided-notes.md` when the user provides an Obsidian paper-reading template, asks to fill a template, or wants notes connected to their own research plan.

Template-guided mode adds a planning step before NotebookLM questions:

1. Read the template headings, callouts, tables, and placeholders.
2. Convert template sections into a small question plan.
3. Preserve explicit user questions verbatim; generated questions fill only the unstated template needs.
4. Render the final Obsidian note in the template's structure, keeping frontmatter, callouts, tables, and section order where practical.

## Token Discipline

- Keep this file in context; load references only when needed.
- Before reasoning over NotebookLM JSON, run `scripts/filter_notebooklm_refs.py` to deduplicate and discard uncited references.
- Prefer script outputs and audit files over pasting raw NotebookLM responses into context.

## Minimal Workflow

1. Resolve Zotero paper(s), PDF attachment(s), and metadata.
2. Create/select a NotebookLM notebook, upload PDFs, and save a `source_id → Zotero PDF` source map. Fetch source fulltext for each source.
3. Ask the explicit or template-derived question(s) and obtain answer + references.
4. Deduplicate and filter references with `scripts/filter_notebooklm_refs.py`.
5. Prepare evidence with `scripts/prepare_notebooklm_evidence.py`.
6. Create Zotero annotations with `scripts/zotero_evidence.py`.
7. Write the Obsidian note with Zotero annotation links as in-text references.
8. Validate evidence count, non-empty annotation comments, style/color, links, and fuzzy-match audit points.

## Required Skill

**This skill requires the `notebooklm` skill (notebooklm-py).** All NotebookLM operations — notebook creation, source upload, `ask --json` — must use the notebooklm skill. Verify `notebooklm status` before starting.

## Companion Skills

Cooperate with companion skills instead of duplicating their domain logic:

- `notebooklm`: required (see above).
- `pyzotero`: Zotero API work.
- `obsidian-cli`: vault-aware Obsidian operations.
- `obsidian-markdown`: Obsidian Markdown syntax.
- `zotero-obsidian-bridge`: vault folder conventions.

Read `references/skill-cooperation.md` before integrating with those skills.

## Load As Needed

- `references/pipeline.md`: end-to-end checklist and validation.
- `references/notebooklm.md`: NotebookLM data contract, reference filtering, `source_id`, `cited_text`, `chunk_id`.
- `references/template-guided-notes.md`: derive NotebookLM questions from Obsidian paper-reading templates and personal research context.
- `references/zotero-annotations.md`: annotation style, coordinate rules, matching, comments, links.
- `references/skill-cooperation.md`: optional companion-skill protocol.
- `scripts/prepare_notebooklm_evidence.py`: prepare evidence text JSON from NotebookLM JSON + source map; fill `comment` before creating annotations.
- `scripts/zotero_evidence.py`: create annotations, update comments, and generate Zotero links.
