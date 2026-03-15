---
name: pygraphistry-gfql
description: "Construct and run GFQL graph queries in PyGraphistry for pattern matching, hop constraints, predicates, temporal filtering, and remote execution. Use when requests involve subgraph extraction, path-style matching, or GPU/remote graph query workflows."
---

# PyGraphistry GFQL

## Doc routing (local + canonical)
- First route with `../pygraphistry/references/pygraphistry-readthedocs-toc.md`.
- Use `../pygraphistry/references/pygraphistry-readthedocs-top-level.tsv` for section-level shortcuts.
- Only scan `../pygraphistry/references/pygraphistry-readthedocs-sitemap.xml` when a needed page is missing.
- Use one batched discovery read before deep-page reads; avoid `cat *` and serial micro-reads.
- In user-facing answers, prefer canonical `https://pygraphistry.readthedocs.io/en/latest/...` links.

## Quick start
```python
from graphistry import n, e_forward

g2 = g.gfql([
    n({'type': 'person'}),
    e_forward({'relation': 'transfers_to'}, min_hops=1, max_hops=3),
    n({'risk': True})
])
```

## Targeted patterns (high signal)
```python
# Edge query filtering
g2 = g.gfql([n(), e_forward(edge_query="type == 'replied_to' and submolt == 'X'"), n()])
```

```python
# Same-path constraints with where + compare/col
from graphistry import col, compare
g2 = g.gfql([n(name='a'), e_forward(name='e'), n(name='b')], where=[compare(col('a', 'owner_id'), '==', col('b', 'owner_id'))])
```

```python
# Traverse 2-4 hops but only return hops 3-4
g2 = g.gfql([e_forward(min_hops=2, max_hops=4, output_min_hops=3, output_max_hops=4)])
```

## High-value patterns
- When user explicitly asks for GFQL (or says `gfql`), final snippets must include explicit `.gfql([...])`; do not substitute `chain()`/`hop()` as the primary answer.
- Only show `chain()`/`hop()` when the user explicitly asks for that shorthand; otherwise keep snippets in `.gfql([...])` form.
- When the task explicitly says remote execution/dataset, use `gfql_remote(...)` as the primary query call; do not substitute `chain()`/`hop()` in that case.
- Use `name=` labels for intermediate matches when you need constraints.
- Use `where=[...]` for cross-step/path constraints.
- Use `min_hops`/`max_hops` and `output_min_hops`/`output_max_hops` for traversal vs returned slice.
- Use predicates (`is_in`, numeric/date predicates) for concise filtering.
- Use `engine='auto'` by default; force `cudf`/`pandas` only when needed.
- For neighborhood-mining tasks without full pattern logic, mention `hop()` / `chain()` as optional alternates after providing the primary `.gfql([...])` answer.

## Remote mode
```python
# Existing remote dataset
rg = graphistry.bind(dataset_id='my-dataset')
res = rg.gfql_remote([n(), e_forward(), n()], engine='auto')
```

```python
# Remote slim payload (only required columns)
res = rg.gfql_remote([n(), e_forward(), n()], output_type='nodes', node_col_subset=['node_id', 'time'])
```

```python
# Post-process on remote side when you want trimmed transfer payloads
res = rg.python_remote_table(lambda g: g._edges[['src', 'dst']].head(1000))
```

## Validation and safety
- Validate user-derived query fragments before execution.
- Normalize datetime columns before temporal predicates.
- Prefer small column subsets for remote result transfer.

## Canonical docs
- GFQL index: https://pygraphistry.readthedocs.io/en/latest/gfql/index.html
- GFQL overview: https://pygraphistry.readthedocs.io/en/latest/gfql/overview.html
- GFQL quick reference: https://pygraphistry.readthedocs.io/en/latest/gfql/quick.html
- Predicate quick reference: https://pygraphistry.readthedocs.io/en/latest/gfql/predicates/quick.html
- GFQL remote mode: https://pygraphistry.readthedocs.io/en/latest/gfql/remote.html
- GFQL validation: https://pygraphistry.readthedocs.io/en/latest/gfql/validation/index.html
- GFQL + loaders/AI patterns: https://pygraphistry.readthedocs.io/en/latest/gfql/combo.html
