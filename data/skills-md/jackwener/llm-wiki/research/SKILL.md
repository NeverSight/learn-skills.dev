---
name: research
description: Research a topic for an LLM Wiki vault. Use whenever the user invokes `/research`, asks for a sourced deep dive beyond the current wiki, or asks to discover external sources and integrate the resulting knowledge into the wiki.
---

# Research for an LLM Wiki

Research fills a scoped gap in the wiki, then preserves the evidence and its
useful conclusions. It combines query, source collection, and ingestion.

## Workflow

1. Read `wiki-purpose.md` and `wiki-schema.md`; decline or narrow requests
   outside the vault's scope.
2. Run the `query` workflow first to determine what is known and define a
   precise research question.
3. Gather 5–10 high-quality sources. Prefer primary materials, official
   documentation, papers, and authoritative recent analysis. Seek independent
   confirmation for important claims.
4. Save each collected source under `sources/YYYY-MM-DD/` before analysis.
   Include provenance when creating a research note:

   ```yaml
   ---
   title: Source Title
   url: https://original-url
   author: Author Name
   date: YYYY-MM-DD
   retrieved: YYYY-MM-DD
   type: article | paper | documentation | blog | video-transcript
   ---
   ```

   Treat files in `sources/` as immutable after saving.
5. Apply the `ingest` workflow to each source: update focused, attributable
   wiki pages and add wikilinks rather than compiling a detached report only.
6. Present a final report with this structure:

   ```markdown
   ## Research Report: Topic
   ### Question
   ### Findings
   ### Sources Added
   ### Wiki Pages Created/Updated
   ### Remaining Gaps
   ```

7. Create a query-synthesis page only when the cross-source conclusion is
   genuinely new and well supported. Then append a `research` entry to
   `wiki-log.md` and run `llm-wiki sync`.

## Guardrails

- Keep the research question bounded; list tangents as follow-ups.
- Attribute every material claim to saved sources or cited wiki pages.
- Flag outdated evidence for fast-moving topics.
- Never invent a source, citation, or conclusion.
