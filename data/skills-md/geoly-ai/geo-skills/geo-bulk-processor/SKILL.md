---
name: geo-bulk-processor
description: >
  GEO bulk processing engine for large-scale, multi-page content optimization. Use this skill whenever the user mentions bulk GEO changes, batch content updates, large websites, sitemaps, content libraries, or needs to process many URLs/documents in one workflow, not just a single page.
---

## Overview

`geo-bulk-processor` is a GEO (Generative Engine Optimization) bulk processing orchestrator designed for **large sites and content libraries**. It helps an agent:
- Design and run **batch optimization pipelines** over thousands of pages or documents.
- Standardize **templates and patterns** for repeated page types.
- Track **progress, quality, and rollout phases** instead of treating each page as an isolated “single-shot” task.

Use this skill when the user:
- Manages a **large website**, multi-language site, or content library.
- Wants to **bulk retrofit** existing pages for GEO readiness, AI citations, or structured data.
- Provides **sitemaps, URL lists, spreadsheets, or exports** from CMS/analytics tools.
- Needs a **repeatable, scalable workflow** instead of one-off page edits.

This skill focuses on **planning, orchestration, and consistency**. It does not tie you to any specific GEO framework, but is optimized to work well with the family of `geo-*` skills (e.g. content optimizers, schema generators, local optimizers).

## When to use this skill

Always consider using `geo-bulk-processor` when:
- The user mentions **“bulk”, “batch”, “mass update”, “large site”, “thousands of pages”, “entire catalog”, “all blog posts”**, or similar language.
- The user shares **CSV/Excel exports, sitemaps, URL lists**, or folders of content files.
- The user wants to **apply similar GEO strategies across many items** (e.g., all product pages, all location pages, all support articles).
- The task obviously **cannot be solved efficiently by optimizing a single page at a time**.

If the request is clearly about **one page or a very small number of pages** (e.g., “fix GEO for this single article”), prefer the more focused single-page GEO skills instead of this bulk processor.

## High-level workflow

When this skill is invoked, follow this structured workflow:

1. **Clarify the bulk goal**
   - Identify the **primary GEO goals** (e.g., AI citations for specific queries, better structured data, consistent FAQ blocks, improved internal linking).
   - Ask what **content universe** is in scope (full site, one section, specific content types, language variants, etc.).
   - Ask about **constraints** (timelines, systems, headcount, tech stack, allowed file formats, risk tolerance).

2. **Ingest and profile the corpus**
   - Accept inputs such as:
     - URL lists or sitemaps (XML, CSV, plain text).
     - Content exports from CMS (CSV, JSON, Markdown/HTML files).
     - Analytics exports (top pages, landing pages, long-tail queries).
   - Build a **lightweight inventory summary**:
     - Number of items by content type, language, directory, or template.
     - Obvious **clusters** (e.g., `/blog/`, `/product/`, `/docs/`, `/locations/`).
     - Known **GEO gaps** (missing schema, thin pages, duplicated structures).

3. **Define content clusters and page types**
   - Group content into **clusters** that can share the same optimization strategy:
     - By URL pattern, content type, template ID, language, or topic.
   - For each cluster, define:
     - A **page-type definition** (what the pages are, who they serve, business role).
     - The **GEO opportunities** specific to that cluster.
     - Risks and **special constraints** (e.g., legal wording, regulated content).

4. **Design bulk GEO pipelines**
   - For each cluster, design a **pipeline** describing:
     - **Inputs** (fields from the CMS/CSV, existing content fields, metadata).
     - **Transformations** (rewrites, new sections, schema generation, FAQ extraction).
     - **External skills/tools** to call (e.g., schema generators, content optimizers).
     - **Outputs** (updated HTML/Markdown, JSON fields, CSV columns, migration specs).
   - Capture pipelines in a **structured, reusable format**, using the guidance in `references/bulk_pipelines.md`.

5. **Create reusable templates and patterns**
   - For each major page type, define:
     - A **content skeleton** (sections, headings, FAQs, schema blocks).
     - **Variable slots** tied to data fields (e.g., product name, city, category).
     - Style and tone expectations (aligned with GEO and brand constraints).
   - Make these templates **explicit** so they can be applied programmatically to many items.

6. **Plan execution and rollout**
   - Propose **phased rollout**:
     - Pilot set → expansion → full coverage.
   - For each phase, specify:
     - **Sample size**, selection criteria, and evaluation plan.
     - **Success metrics** (GEO readiness scores, AI citation coverage, traffic proxies).
     - **Feedback loop** and how to adjust templates/pipelines between phases.

7. **Generate concrete artifacts**
   - Depending on user needs, generate:
     - A **master plan document** summarizing clusters, pipelines, and rollout.
     - **CSV/JSON specs** for engineers or operators to implement changes.
     - Example **before/after** content and schema for each major page type.
   - Use `scripts/geo_bulk_pipeline.py` **conceptually** as a helper reference: it describes how to represent content items, clusters, and pipelines in code or data. You do not have to execute it, but you may mirror its structures.

8. **Quality assurance and risk management**
   - Recommend:
     - **Sampling and manual review** before full rollout.
     - **Regression checks** for critical pages (homepage, top products, legal pages).
     - **Monitoring plan** for GEO and traffic indicators after deployment.

## Input formats and expectations

Typical inputs for this skill:
- **URL lists / sitemaps**
  - Plain-text lists of URLs.
  - XML sitemaps (possibly multiple).
- **Spreadsheets / tables**
  - CSV or Excel exports listing URLs, titles, categories, traffic, etc.
- **Content exports**
  - Folders of HTML/Markdown files.
  - CMS exports with JSON per document.

When possible, normalize these into a **tabular or record-based view**:
- One row or record per content item.
- Columns / fields for URL, path, language, category, template, and any key metrics.

If files are not already in a structured format, design and describe a **simple manifest format** that the user’s team can produce (for example, a CSV with `id,url,type,cluster,language` columns).

## Output expectations

Unless the user asks for something highly specific, structure your main outputs as:

1. **High-level GEO bulk strategy**
   - Clear description of scope, goals, and constraints.
   - Overview of clusters, page types, and priorities.

2. **Cluster-by-cluster plan**
   - For each cluster:
     - Description and rationale.
     - Proposed pipeline steps and external skills/tools.
     - Suggested templates and content patterns.

3. **Implementation-ready specifications**
   - Tables or pseudo-schemas describing:
     - Required input fields and data sources.
     - Output fields/files and where they should be written.
     - Recommended automation approach (ETL, scripts, CMS workflows).

4. **Rollout and QA plan**
   - Phased rollout with criteria and success metrics.
   - QA checklists for sampling and sign-off.
   - Monitoring and iteration loops.

When the user explicitly requests machine-consumable artifacts (for example, “give me a CSV spec that my data team can use”), prioritize **precise, unambiguous formats** (clear column names, data types, and examples).

## Use of bundled resources

This skill ships with additional reference material and helper code:

- `references/bulk_pipelines.md`
  - Explains common GEO bulk pipeline patterns.
  - Provides example cluster definitions, pipeline step types, and rollout patterns.
  - Read this when you need inspiration for how to structure pipelines or explain them to the user’s team.

- `scripts/geo_bulk_pipeline.py`
  - Contains **lightweight data models and helper functions** that show one way to model content items, clusters, and pipelines.
  - You can mirror its structures when designing data formats, but you do **not** need to execute it to complete user requests.
  - If the environment allows executing scripts, they can be adapted into real automation helpers, but this skill does not require that.

When in doubt, prefer **clear written plans and specs** over over-engineered code. The primary value of this skill is in **designing scalable GEO bulk workflows**, not in implementing full production systems inside the skill.

## Style and collaboration guidelines

- **Think like a systems designer.**
  - Aim for solutions that will still work when the corpus doubles or triples.
  - Avoid plans that require per-page manual tweaking unless limited to a small, high-value subset.

- **Explain the “why”, not just the “what”.**
  - Connect GEO decisions (clusters, templates, schema types) to the user’s business goals and constraints.

- **Be opinionated but adaptable.**
  - Suggest defaults and best practices, but clearly mark them as such.
  - Offer alternative paths when user constraints are unclear or strict.

- **Make it easy to operationalize.**
  - Prefer concrete artifacts: specs, templates, checklists, and example records.
  - Avoid vague recommendations that cannot be turned into tickets or automation.

If the user already uses other `geo-*` skills, explicitly reference where they fit into each pipeline step (for example, “use `geo-schema-gen` here to generate Product and FAQ schema for this cluster”).

