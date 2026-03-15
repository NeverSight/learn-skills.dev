---
name: pygraphistry-connectors
description: "Select and use PyGraphistry connector and plugin workflows for graph databases, SQL/data platforms, SIEM/log sources, and layout/compute plugins. Use when requests involve Neo4j/Neptune/Splunk/Kusto/Databricks/SQL/TigerGraph and similar integrations."
---

# PyGraphistry Connectors

## Doc routing (local + canonical)
- First route with `../pygraphistry/references/pygraphistry-readthedocs-toc.md`.
- Use `../pygraphistry/references/pygraphistry-readthedocs-top-level.tsv` for section-level shortcuts.
- Only scan `../pygraphistry/references/pygraphistry-readthedocs-sitemap.xml` when a needed page is missing.
- Use one batched discovery read before deep-page reads; avoid `cat *` and serial micro-reads.
- In user-facing answers, prefer canonical `https://pygraphistry.readthedocs.io/en/latest/...` links.

## Strategy
- Prefer dataframe-first ingestion when practical, then bind with `edges()/nodes()`.
- Use connector-specific notebook patterns when auth/query semantics are specialized.
- For very large datasets, push filtering/aggregation upstream before plotting.
- Keep connector and Graphistry credentials in env vars or secret stores; no hardcoded keys.
- Never use placeholder literals like `username='user'` / `password='pass'` / `username='...'`; use `os.environ[...]` or `os.environ.get(...)`.
- For concise tasks, respond with a single compact code block and minimal prose.
- In concise snippets, prefer explicit privacy literals (`'private'` or `'organization'`) over placeholder variables.

## Connector triage rubric
- Use native graph-db connectors (`cypher`, Neptune/TigerGraph flows) when traversal is best expressed upstream.
- Use SQL/log source extraction when your source is tabular or SIEM-centric, then bind in PyGraphistry.
- If unsure, start with source-native query -> dataframe -> `edges()/nodes()`, then optimize connector depth.

## Connector families
- Graph DBs: Neo4j, Neptune, TigerGraph, Memgraph, Arango.
- Data/SQL: Databricks, PostgreSQL, Spanner, warehouse-style pipelines.
- Logs/SIEM: Splunk, Kusto, AlienVault.
- Compute/layout plugins: networkx, graphviz, cugraph, igraph, hypernetx.

## Minimal examples
```python
# Neo4j-style cypher path (example)
g = graphistry.cypher('MATCH (a)-[r]->(b) RETURN a,b,r')
g.plot()
```

```python
# Graphistry org/service-account auth before connector workflows
graphistry.register(
    api=3,
    org_name=os.environ.get('GRAPHISTRY_ORG_NAME'),
    personal_key_id=os.environ.get('GRAPHISTRY_PERSONAL_KEY_ID'),
    personal_key_secret=os.environ.get('GRAPHISTRY_PERSONAL_KEY_SECRET')
)
```

```python
# Generic dataframe path after source-specific query/extract
# edges_df: src,dst,...
g = graphistry.edges(edges_df, 'src', 'dst')
graphistry.privacy(mode='private')
plot_url = g.plot(render=False)
```

```python
# Connector-oriented flow with explicit nodes + focused GFQL slice
# Example source can be Neo4j/Splunk -> dataframe extraction
g = graphistry.edges(edges_df, 'src', 'dst').nodes(nodes_df, 'id')
g_focus = g.gfql([...]).name('connector-slice')
graphistry.privacy(mode='organization')
plot_url = g_focus.plot(render=False)
```

## Canonical docs
- Plugins overview: https://pygraphistry.readthedocs.io/en/latest/plugins.html
- Connector notebooks: https://pygraphistry.readthedocs.io/en/latest/notebooks/plugins.connectors.html
- Compute/layout plugin notebooks: https://pygraphistry.readthedocs.io/en/latest/notebooks/plugins.compute.html
- Notebooks index: https://pygraphistry.readthedocs.io/en/latest/notebooks/index.html
