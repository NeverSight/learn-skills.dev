---
name: spice-search
description: Search data using vector similarity, full-text keywords, or hybrid methods with Reciprocal Rank Fusion (RRF). Use when setting up embeddings for search, configuring full-text indexing, writing vector_search/text_search/rrf SQL queries, using the /v1/search HTTP API, or configuring vector engines like S3 Vectors.
---

# Search Data

Spice provides integrated search capabilities: vector (semantic) search, full-text (keyword) search, and hybrid search with Reciprocal Rank Fusion (RRF) — all via SQL functions and HTTP APIs. Search indexes are built on top of accelerated datasets.

## Search Methods

| Method               | When to Use                                            | Requires                                    |
| -------------------- | ------------------------------------------------------ | ------------------------------------------- |
| **Vector search**    | Semantic similarity, RAG, recommendations              | Embedding model + column embeddings         |
| **Full-text search** | Keyword/phrase matching, exact terms                   | `full_text_search.enabled: true` on columns |
| **Hybrid (RRF)**     | Best of both — combines rankings from multiple methods | Multiple search methods configured          |
| **Lexical (LIKE/=)** | Exact pattern or value matching                        | Nothing extra                               |

## Set Up Vector Search

### 1. Define an Embedding Model

```yaml
embeddings:
  - name: local_embeddings
    from: huggingface:huggingface.co/sentence-transformers/all-MiniLM-L6-v2

  - name: openai_embeddings
    from: openai:text-embedding-3-small
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
```

### Supported Embedding Providers

| Provider       | From Format                                                         | Status            |
| -------------- | ------------------------------------------------------------------- | ----------------- |
| OpenAI         | `openai:text-embedding-3-large`                                     | Release Candidate |
| HuggingFace    | `huggingface:huggingface.co/sentence-transformers/all-MiniLM-L6-v2` | Release Candidate |
| Local file     | `file:model.safetensors`                                            | Release Candidate |
| Azure OpenAI   | `azure:my-deployment`                                               | Alpha             |
| Google AI      | `google:text-embedding-004`                                         | Alpha             |
| Amazon Bedrock | `bedrock:amazon.titan-embed-text-v1`                                | Alpha             |
| Databricks     | `databricks:endpoint`                                               | Alpha             |
| Model2Vec      | `model2vec:model-name`                                              | Alpha             |

### 2. Configure Dataset Columns for Embeddings

```yaml
datasets:
  - from: postgres:documents
    name: docs
    acceleration:
      enabled: true
    columns:
      - name: content
        embeddings:
          - from: local_embeddings
            row_id: id
            chunking:
              enabled: true
              target_chunk_size: 512
              overlap_size: 64
```

### Embedding Methods

| Method                 | Description                              | When to Use                                  |
| ---------------------- | ---------------------------------------- | -------------------------------------------- |
| **Accelerated**        | Precomputed and stored                   | Faster queries, frequently searched datasets |
| **JIT (Just-in-Time)** | Computed at query time (no acceleration) | Large or rarely queried datasets             |
| **Passthrough**        | Pre-existing embeddings used directly    | Source already has `<col>_embedding` columns |

### 3. Query via HTTP API

```bash
curl -X POST http://localhost:8090/v1/search \
  -H 'Content-Type: application/json' \
  -d '{
    "datasets": ["docs"],
    "text": "cutting edge AI",
    "where": "author=\"jeadie\"",
    "additional_columns": ["title", "state"],
    "limit": 5
  }'
```

| Field                | Required | Description                                |
| -------------------- | -------- | ------------------------------------------ |
| `text`               | Yes      | Search text                                |
| `datasets`           | No       | Datasets to search (null = all searchable) |
| `additional_columns` | No       | Extra columns to return                    |
| `where`              | No       | SQL filter predicate                       |
| `limit`              | No       | Max results per dataset                    |

To retrieve full documents (not just chunks), include the embedding column name in `additional_columns`.

### 4. Query via SQL UDTF

```sql
SELECT id, title, score
FROM vector_search(docs, 'cutting edge AI')
WHERE state = 'Open'
ORDER BY score DESC
LIMIT 5;
```

**`vector_search` signature:**

```sql
vector_search(
  table STRING,          -- Dataset name (required)
  query STRING,          -- Search text (required)
  col STRING,            -- Column (optional if single embedding column)
  limit INTEGER,         -- Max results (default: 1000)
  include_score BOOLEAN  -- Include score column (default: TRUE)
) RETURNS TABLE
```

> **Limitation**: `vector_search` UDTF does not yet support chunked embedding columns. Use the HTTP API for chunked data.

## Set Up Full-Text Search

Full-text search uses **BM25 scoring** (powered by Tantivy) for keyword relevance ranking.

### 1. Enable Indexing on Columns

```yaml
datasets:
  - from: postgres:articles
    name: articles
    acceleration:
      enabled: true
    columns:
      - name: title
        full_text_search:
          enabled: true
          row_id:
            - id
      - name: body
        full_text_search:
          enabled: true
```

### 2. Query via SQL UDTF

```sql
SELECT id, title, score
FROM text_search(articles, 'search keywords', body)
ORDER BY score DESC
LIMIT 5;
```

**`text_search` signature:**

```sql
text_search(
  table STRING,          -- Dataset name (required)
  query STRING,          -- Keywords/phrase (required)
  col STRING,            -- Column (required if multiple indexed columns)
  limit INTEGER,         -- Max results (default: 1000)
  include_score BOOLEAN  -- Include score column (default: TRUE)
) RETURNS TABLE
```

## Hybrid Search with RRF

Reciprocal Rank Fusion merges rankings from multiple search methods. Each query runs independently, then results are combined:

```
RRF Score = Σ(rank_weight / (k + rank))
```

Documents appearing across multiple result sets receive higher scores.

### Basic Hybrid Search

```sql
SELECT id, title, content, fused_score
FROM rrf(
    vector_search(documents, 'machine learning algorithms'),
    text_search(documents, 'neural networks deep learning', content),
    join_key => 'id'
)
ORDER BY fused_score DESC
LIMIT 5;
```

### Weighted Ranking

```sql
SELECT fused_score, title, content
FROM rrf(
    text_search(posts, 'artificial intelligence', rank_weight => 50.0),
    vector_search(posts, 'AI machine learning', rank_weight => 200.0)
)
ORDER BY fused_score DESC
LIMIT 10;
```

### Recency-Boosted Search

```sql
-- Exponential decay (1-hour scale)
SELECT fused_score, title, created_at
FROM rrf(
    text_search(news, 'breaking news'),
    vector_search(news, 'latest updates'),
    time_column => 'created_at',
    recency_decay => 'exponential',
    decay_constant => 0.05,
    decay_scale_secs => 3600
)
ORDER BY fused_score DESC
LIMIT 10;

-- Linear decay (24-hour window)
SELECT fused_score, content
FROM rrf(
    text_search(posts, 'trending'),
    vector_search(posts, 'viral popular'),
    time_column => 'created_at',
    recency_decay => 'linear',
    decay_window_secs => 86400
)
ORDER BY fused_score DESC;
```

### Cross-Language Search

```sql
SELECT fused_score, text, langs
FROM rrf(
    vector_search(posts, 'ultimas noticias', rank_weight => 100),
    text_search(posts, 'news'),
    time_column => 'created_at',
    recency_decay => 'exponential',
    decay_constant => 0.05,
    decay_scale_secs => 3600
)
WHERE trim(text) != ''
ORDER BY fused_score DESC LIMIT 15;
```

### `rrf` Parameters

| Parameter                 | Type        | Required | Description                                                  |
| ------------------------- | ----------- | -------- | ------------------------------------------------------------ |
| `query_1`, `query_2`, ... | Search UDTF | Yes (2+) | `vector_search` or `text_search` calls (variadic)            |
| `join_key`                | String      | No       | Column for joining results (default: auto-hash)              |
| `k`                       | Float       | No       | Smoothing parameter (default: 60.0, lower = more aggressive) |
| `time_column`             | String      | No       | Timestamp column for recency boosting                        |
| `recency_decay`           | String      | No       | `'exponential'` (default) or `'linear'`                      |
| `decay_constant`          | Float       | No       | Rate for exponential decay (default: 0.01)                   |
| `decay_scale_secs`        | Float       | No       | Time scale for exponential decay (default: 86400)            |
| `decay_window_secs`       | Float       | No       | Window for linear decay (default: 86400)                     |
| `rank_weight`             | Float       | No       | Per-query weight (specified inside search calls)             |

## Vector Engines

Store and index embeddings at scale using dedicated vector engines:

```yaml
datasets:
  - from: postgres:documents
    name: docs
    acceleration:
      enabled: true
    columns:
      - name: content
        embeddings:
          - from: embed_model
            row_id: id
        metadata:
          vectors: non-filterable
      - name: category
        metadata:
          vectors: filterable # enable filtering on this column
    vectors:
      enabled: true
      engine: s3_vectors
      params:
        s3_vectors_bucket: my-bucket
        s3_vectors_region: us-east-1
```

## Lexical Search (SQL)

Standard SQL filtering:

```sql
SELECT * FROM my_table WHERE column LIKE '%substring%';
SELECT * FROM my_table WHERE column = 'exact value';
SELECT * FROM my_table WHERE regexp_like(column, '^spice.*ai$');
```

## CLI Search

```bash
spice search "cutting edge AI" --dataset docs --limit 5
spice search --cache-control no-cache "search terms"
```

## Complete Example

```yaml
version: v1
kind: Spicepod
name: search_app

secrets:
  - from: env
    name: env

embeddings:
  - name: embeddings
    from: huggingface:huggingface.co/sentence-transformers/all-MiniLM-L6-v2

datasets:
  - from: file:articles.parquet
    name: articles
    acceleration:
      enabled: true
      engine: duckdb
    columns:
      - name: title
        full_text_search:
          enabled: true
          row_id:
            - id
      - name: content
        embeddings:
          - from: embeddings
        full_text_search:
          enabled: true
```

```sql
SELECT id, title, content, fused_score
FROM rrf(
    vector_search(articles, 'machine learning best practices'),
    text_search(articles, 'neural network training', content),
    join_key => 'id',
    time_column => 'published_at',
    recency_decay => 'exponential',
    decay_constant => 0.01,
    decay_scale_secs => 86400
)
WHERE fused_score > 0.01
ORDER BY fused_score DESC
LIMIT 10;
```

## Troubleshooting

| Issue                                     | Solution                                                             |
| ----------------------------------------- | -------------------------------------------------------------------- |
| `vector_search` returns no results        | Verify embeddings configured on column and model is loaded           |
| `text_search` returns no results          | Check `full_text_search.enabled: true`; acceleration must be enabled |
| Poor hybrid search relevance              | Tune `rank_weight` per query and adjust `k`                          |
| Results missing recent content            | Add `time_column` and `recency_decay` to RRF                         |
| Chunked vector search not working via SQL | Use HTTP API instead (UDTF doesn't support chunked columns yet)      |

## Documentation

- [Search Overview](https://spiceai.org/docs/features/search)
- [Vector Search](https://spiceai.org/docs/features/search/vector-search)
- [Full-Text Search](https://spiceai.org/docs/features/search/full-text)
- [Search SQL Reference](https://spiceai.org/docs/reference/sql/search)
- [Embedding Models](https://spiceai.org/docs/components/embeddings)
- [Vector Engines](https://spiceai.org/docs/components/vectors)
- [Search API](https://spiceai.org/docs/api/HTTP/post-search)
