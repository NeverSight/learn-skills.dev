---
name: pygraphistry
description: "TOC router for PyGraphistry tasks. Use when a request involves PyGraphistry and you need to choose the right workflow: loading/ETL shaping, visualization/layout/sharing, GFQL or hop/chain traversal/search, AI/UMAP/embed/semantic-search workflows, or connector-specific ingestion."
---

# PyGraphistry Router

Use this skill as a dispatcher to specialized skills.
Treat this as the Python SDK entrypoint; for a cross-interface entrypoint use `graphistry`.

## Route By Intent
- Setup/auth/first plot from tables: use `pygraphistry-core`.
- Direct Graphistry REST endpoint requests (`curl`, `/api/v2/...`, JWT/Bearer, upload/session/url params): immediately use `graphistry-rest-api` and skip ReadTheDocs discovery.
- Styling/layout/static output/privacy and sharing: use `pygraphistry-visualization`.
- Pattern matching, hops/chains, predicates, remote graph queries: use `pygraphistry-gfql`.
- UMAP/DBSCAN/embedding/anomaly and graph-AI notebooks: use `pygraphistry-ai`.
- Database/platform integrations (Neo4j, Splunk, Kusto, Databricks, SQL, etc.): use `pygraphistry-connectors`.

## Fast Targeted Fetch Protocol
- REST-intent exception: do not run this protocol for REST tasks routed to `graphistry-rest-api`.
- Start from `references/pygraphistry-readthedocs-toc.md`; do not crawl broad docs first.
- Use `references/pygraphistry-readthedocs-top-level.tsv` for section-level shortcuts.
- Pick exactly one primary skill and at most two secondary docs before fetching content.
- Do one batched discovery read first (TOC + top-level index), then pick targets.
- After discovery, do at most one deep-page read per iteration.
- Prefer section indexes (`.../gfql/index.html`, `.../visualization/index.html`) before deep pages.
- For routing replies, prefer ReadTheDocs URLs (`https://pygraphistry.readthedocs.io/...`) over GitHub/local file paths unless the user explicitly asks for source code links.
- Keep the first routing response compact (typically 3-5 lines): selected skill + top links.
- Escalate to deeper page fetches only after the user confirms direction or asks for detail.
- Avoid serial micro-reads across many files when one batched lookup can answer routing.
- Avoid blind full dumps (`cat *`, full sitemap dumps) that bloat context without improving routing quality.
- For canonical URL verification, prefer local snapshot evidence first; use web fallback when the user requests freshness or local mapping is missing.

## Default Safety Rules
- Read credentials from environment variables; do not hardcode secrets in tracked files.
- Prefer `api=3` for modern features.
- Prefer a plain `type` column on both nodes and edges for legend/category defaults.
- Set explicit privacy mode before sharing links for sensitive data.
- For large graphs, reduce columns/rows before upload and visualize focused subgraphs first.

## Canonical Docs
- Main docs: https://pygraphistry.readthedocs.io/en/latest/
- Docs TOC snapshot: `references/pygraphistry-readthedocs-toc.md`
- ReadTheDocs version sitemap: https://pygraphistry.readthedocs.io/sitemap.xml
- 10 minutes core: https://pygraphistry.readthedocs.io/en/latest/10min.html
- Visualization: https://pygraphistry.readthedocs.io/en/latest/visualization/index.html
- GFQL: https://pygraphistry.readthedocs.io/en/latest/gfql/index.html
- Plugins/connectors: https://pygraphistry.readthedocs.io/en/latest/plugins.html
