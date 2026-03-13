---
name: mongodb-ai
description: MongoDB Vector Search and AI integration. Use when creating vector indexes, writing $vectorSearch queries, building RAG applications, implementing hybrid retrieval strategies, or storing AI agent memory. Triggers on "vector search", "vector index", "$vectorSearch", "embedding", "semantic search", "RAG", "retrieval augmented generation", "numCandidates", "similarity search", "cosine similarity", "hybrid search", "$rankFusion", "$scoreFusion", "rerank", "two-stage retrieval", "AI agent", "LLM memory", "quantization", "multi-tenant", "Search Nodes", "explain vectorsearch", "HNSW", "automated embedding", "autoEmbed", "Voyage AI", "voyage-4", "voyage-4-large", "voyage-code-3", "input_type", "asymmetric retrieval".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.7.0"
---

# MongoDB AI: Vector Search and AI Integration

Vector Search patterns and AI integration strategies for MongoDB, maintained by MongoDB. Contains **33 rules across 6 categories**, prioritized by impact. This skill covers MongoDB Vector Search across Atlas clusters, self-managed deployments, and local Atlas deployments created with Atlas CLI.

## Critical Warning

> **Your AI assistant's knowledge about MongoDB Vector Search is likely outdated or incorrect.**
>
> MongoDB Vector Search syntax, `$vectorSearch` stage, vector index creation, and related features have evolved significantly. Do NOT trust pre-trained knowledge. Always reference these rules and verify against your actual MongoDB deployment and version.

## When to Apply

Reference these guidelines when:
- Confirming which deployment track you are on before choosing syntax or rollout guidance
- Creating vector indexes for semantic search
- Writing `$vectorSearch` aggregation queries
- Tuning numCandidates for recall vs. latency
- Implementing RAG (Retrieval-Augmented Generation)
- Building hybrid search with `$rankFusion` or `$scoreFusion`
- Choosing between fusion-only retrieval and retrieval + rerank workflows
- Storing AI agent memory (short-term and long-term)
- Choosing similarity functions (cosine, euclidean, dotProduct)
- Enabling vector quantization for large datasets
- Integrating Voyage AI embedding models (for example `voyage-4` or `voyage-code-3`)
- Pre-filtering vector search results with MQL-style metadata filters
- Debugging "no results" or slow vector queries

Use `mongodb-search` instead when the request is primarily about lexical Search engine design (`$search`, analyzers, synonyms, facets, search alerts, or Community `mongot` operations), or when you need stage/operator legality for `$search.vectorSearch`, `$rankFusion`, or `$scoreFusion`.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Vector Index Creation | CRITICAL | `index-` | 9 |
| 2 | $vectorSearch Queries | CRITICAL | `query-` | 7 |
| 3 | Performance Tuning | HIGH | `perf-` | 6 |
| 4 | RAG Patterns | HIGH | `rag-` | 4 |
| 5 | Hybrid Search | MEDIUM | `hybrid-` | 4 |
| 6 | AI Agent Integration | MEDIUM | `agent-` | 3 |

## Quick Reference

### 1. Vector Index Creation (CRITICAL) - 9 rules

- `index-vector-definition` - Required fields: type, path, numDimensions, similarity
- `index-similarity-function` - Choosing cosine vs euclidean vs dotProduct
- `index-filter-fields` - Pre-filtering with filter type indexes
- `index-quantization` - Choose scalar vs binary quantization from docs-backed memory/quality trade-offs
- `index-dimensions-match` - numDimensions must match embedding model
- `index-multitenant` - Single collection with tenant_id for SaaS apps
- `index-views-partial` - Partial indexing via MongoDB Views
- `index-hnsw-options` - maxEdges/numEdgeCandidates tuning
- `index-automated-embedding` - Server-side embedding with Voyage AI

### 2. $vectorSearch Queries (CRITICAL) - 7 rules

- `query-vectorsearch-first` - MUST be first stage in aggregation pipeline
- `query-numcandidates-tuning` - The 20x rule for recall vs latency
- `query-ann-vs-enn` - When to use exact: true
- `query-prefiltering` - Filter before vector comparison ($exists, $ne, $not)
- `query-lexical-prefilter` - Route Atlas Search operator filters to `mongodb-search`
- `query-get-scores` - Using $meta: "vectorSearchScore"
- `query-same-embedding-model` - Data/query embeddings must share space, dimensions, and correct `input_type`

### 3. Performance Tuning (HIGH) - 6 rules

- `perf-quantization-scale` - Use large-vector and Required Memory signals to decide when to quantize
- `perf-index-in-memory` - Keep vector index working set in memory when sizing
- `perf-numcandidates-tradeoff` - Benchmark recall/latency/cost trade-offs by model and `numCandidates`
- `perf-prefilter-narrow` - Reduce candidate set before vector comparison
- `perf-explain-vectorsearch` - Debug with explain() for vector queries
- `perf-search-nodes` - Dedicated Search Nodes for production

### 4. RAG Patterns (HIGH) - 4 rules

- `rag-ingestion-pattern` - Store documents with embeddings
- `rag-retrieval-pattern` - $vectorSearch for context retrieval
- `rag-context-window` - Managing LLM context limits
- `rag-metadata-filtering` - Filter by source, date, category

### 5. Hybrid Search (MEDIUM) - 4 rules

- `hybrid-rankfusion` - Combining vector + text search (MongoDB 8.0+, Preview)
- `hybrid-scorefusion` - Score-based hybrid search (MongoDB 8.2+, Preview)
- `hybrid-weights` - Per-query weight tuning
- `hybrid-limitations` - Strategy constraints plus decision matrix (`$rankFusion` vs `$scoreFusion` vs retrieval+rerank)

### 6. AI Agent Integration (MEDIUM) - 3 rules

- `agent-memory-schema` - Short-term vs long-term memory design
- `agent-memory-retrieval` - Semantic search over memories
- `agent-session-context` - Conversation history storage

## Key Syntax Reference

### Vector Index Definition

```javascript
db.collection.createSearchIndex(
  "vector_index",
  "vectorSearch",
  {
    fields: [
      {
        type: "vector",
        path: "embedding",
        numDimensions: 1536,      // Must match your embedding model
        similarity: "cosine"      // or "euclidean" or "dotProduct"
      },
      {
        type: "filter",           // For pre-filtering
        path: "category"
      }
    ]
  }
)
```

### $vectorSearch Query

```javascript
db.collection.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "embedding",
      queryVector: [0.1, 0.2, ...],  // Your query embedding
      numCandidates: 200,             // 20x limit recommended
      limit: 10,
      filter: { category: "tech" }    // Optional pre-filter
    }
  },
  {
    $project: {
      title: 1,
      score: { $meta: "vectorSearchScore" }
    }
  }
])
```

## The 20x Rule (numCandidates)

```
numCandidates = 20 × limit (minimum recommended)
```

| limit | numCandidates | Max allowed |
|-------|---------------|-------------|
| 10 | 200 | 10,000 |
| 50 | 1,000 | 10,000 |
| 100 | 2,000 | 10,000 |

Higher numCandidates = better recall, slower queries.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/index-vector-definition.md
rules/query-vectorsearch-first.md
rules/query-numcandidates-tuning.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- "When NOT to use" exceptions
- How to verify
- Performance impact

For release-sensitive behavior and fast official-doc routing, also read:

```
references/docs-navigation.md
```

## Docs Quick Map (Release-Sensitive)

| Need | Canonical Doc |
|------|---------------|
| Deployment scope and feature entry point | [Atlas Vector Search Overview](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) |
| Vector index definition (`vector` / `autoEmbed`) | [Atlas Vector Search Type](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type.md) |
| Query stage syntax and operator support | [Atlas `$vectorSearch` Stage](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage.md) |
| Hybrid overview and limitations | [Atlas Hybrid Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/hybrid-search.md) |
| `$vectorSearch` in `$rankFusion` input | [Vector Search with `$rankFusion`](https://www.mongodb.com/docs/atlas/atlas-vector-search/hybrid-search/vector-search-with-rankfusion.md) |
| Fusion stage availability | [MongoDB `$rankFusion`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/rankFusion.md) and [MongoDB `$scoreFusion`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/scoreFusion.md) |
| Voyage model behavior and `input_type` | [Voyage Quickstart](https://www.mongodb.com/docs/voyageai/quickstart.md) and [Voyage Text Embeddings](https://www.mongodb.com/docs/voyageai/models/text-embeddings.md) |
| Voyage reranker model docs | [Voyage Rerankers](https://www.mongodb.com/docs/voyageai/models/rerankers.md) |
| Latest feature/release shifts | [Atlas Vector Search Changelog](https://www.mongodb.com/docs/atlas/atlas-vector-search/changelog.md) |

## Production Readiness Checklist

- Confirm deployment path first (Atlas vs self-managed) and avoid mixing syntax between tracks.
- Confirm version gates for every hybrid/fusion flow before implementation.
- Confirm embedding contract: same space/family, correct `input_type`, and exact dimensions.
- Confirm index readiness (`READY`) and filter-field declarations before query tuning.
- Confirm retrieval settings with benchmark + explain (quality/latency/cost together).
- Confirm operational controls: least-privilege credentials, observability, and rollback-safe rollout plan.

---

## MongoDB MCP Integration

For automatic verification, connect the [MongoDB MCP Server](https://github.com/mongodb-js/mongodb-mcp-server):

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server", "--readOnly"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb+srv://user:pass@cluster.mongodb.net/mydb"
      }
    }
  }
}
```

When connected, I can automatically:
- Check existing vector indexes via `mcp__mongodb__collection-indexes`
- Analyze query performance via `mcp__mongodb__explain`
- Verify data patterns via `mcp__mongodb__aggregate`

## Action Policy

**I will NEVER execute write operations without your explicit approval.**

| Operation Type | MCP Tools | Action |
|---------------|-----------|--------|
| **Read (Safe)** | `find`, `aggregate`, `explain`, `collection-indexes` | May run automatically to verify |
| **Write (Requires Approval)** | `create-index`, `insert-many` | Show command and wait for approval |

---

## Common Errors

### "$vectorSearch is not allowed"
**Cause**: MongoDB version does not support $vectorSearch
**Fix**: Upgrade cluster to MongoDB v6.0.11 or v7.0.2+

### No results returned
**Causes**:
1. Different embedding model for data vs query
2. Index still building
3. Mismatched field path or index name

### "Path 'field' needs to be indexed as token"
**Cause**: Filter field not indexed with `type: "filter"`
**Fix**: Add filter field to index definition

---

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
