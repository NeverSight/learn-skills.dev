---
name: pygraphistry-ai
description: "Apply PyGraphistry graph ML/AI workflows such as UMAP, DBSCAN, embedding-based anomaly analysis, and fit/transform pipelines on nodes or edges. Use for feature-driven exploration, clustering, anomaly triage, and graph-AI notebook workflows."
---

# PyGraphistry AI

## Doc routing (local + canonical)
- First route with `../pygraphistry/references/pygraphistry-readthedocs-toc.md`.
- Use `../pygraphistry/references/pygraphistry-readthedocs-top-level.tsv` for section-level shortcuts.
- Only scan `../pygraphistry/references/pygraphistry-readthedocs-sitemap.xml` when a needed page is missing.
- Use one batched discovery read before deep-page reads; avoid `cat *` and serial micro-reads.
- In user-facing answers, prefer canonical `https://pygraphistry.readthedocs.io/en/latest/...` links.

## Typical workflow
1. Build graph from nodes/edges.
2. Run feature/embedding method (`umap`, `embed`, optional `dbscan`).
3. Inspect derived columns/features and visualize.
4. Iterate on feature columns and sampling strategy.

## Baseline examples
```python
# Similarity embedding / projection
g2 = graphistry.nodes(df, 'id').umap(X=['f1', 'f2', 'f3'])
g2.plot()
```

```python
# Fit/transform flow for consistent projection on new batches
g_train = graphistry.nodes(df_train, 'id').umap(X=['f1', 'f2'])
g_batch = g_train.transform_umap(df_batch, return_graph=True)
g_batch.plot()
```

```python
# Semantic search over embedded features
g2 = graphistry.nodes(df, 'id').umap(X=['text_col'])
results_df, query_vector = g2.search('suspicious login pattern')
```

```python
# Text-first workflow: featurize then search/cluster
g2 = graphistry.nodes(df, 'id').featurize(kind='nodes', X=['title', 'body']).umap(kind='nodes').dbscan()
hits, qv = g2.search('credential stuffing campaign')
```

```python
# Precomputed embedding columns
embedding_cols = [c for c in df.columns if c.startswith('emb_')]
g2 = graphistry.nodes(df, 'id').umap(X=embedding_cols)
g_new = g2.transform_umap(df_new, return_graph=True)
```

## Practical guardrails
- Start with small/representative samples before full runs.
- Keep explicit feature lists (`X=...`) for reproducibility.
- Track engine/dataframe type for CPU vs GPU behavior.
- For anomaly workflows, document thresholds and false-positive assumptions.
- For graph ML tasks, route deeper model workflows to RGCN/link-prediction references.
- For text workflows, prefer `featurize(...).umap(...).search(...)` when queries are natural language.
- If users already have embeddings, reuse them via explicit embedding column lists (`X=[...]`) before recomputing.
- When user asks for a concise workflow snippet, prefer one short code block and avoid long narrative wrappers.

## Canonical docs
- GFQL + AI combos: https://pygraphistry.readthedocs.io/en/latest/gfql/combo.html
- API AI reference: https://pygraphistry.readthedocs.io/en/latest/api/ai.html
- AI notebook index: https://pygraphistry.readthedocs.io/en/latest/notebooks/ai.html
- Example RGCN notebook: https://pygraphistry.readthedocs.io/en/latest/demos/more_examples/graphistry_features/embed/simple-ssh-logs-rgcn-anomaly-detector.html
