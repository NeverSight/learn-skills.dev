---
name: rag-implementer
description: 'Implements retrieval-augmented generation pipelines. Use when building document retrieval systems, choosing chunking strategies, selecting embedding models, configuring vector stores, implementing hybrid search, or evaluating RAG quality. Use for embedding strategy, vector stores, retrieval pipelines, chunking, hybrid search, re-ranking, multi-query retrieval, parent document retrieval, contextual compression, MMR diversity selection, reciprocal rank fusion, and evaluation. For KB architecture selection and governance, use the knowledge-base-manager skill. For knowledge graphs, use the knowledge-graph-builder skill.'
license: MIT
metadata:
  author: oakoss
  version: '1.2'
  source: https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation
---

# RAG Implementer

Build production-ready retrieval-augmented generation systems. RAG = Retrieval + Context Assembly + Generation. Use RAG when LLMs need access to fresh, domain-specific, or proprietary knowledge not in their training data. Do not use RAG when simpler alternatives (FAQ pages, keyword search, semantic search) suffice. For KB architecture selection and governance, use the `knowledge-base-manager` skill. For knowledge graph implementation, use the `knowledge-graph-builder` skill.

## Overview

Before building RAG, validate the need: try FAQ pages, keyword search, concierge MVP, or simple semantic search first. Only proceed with RAG for 50k+ documents with validated user demand and $200-500/month budget. RAG systems range from Naive (prototype) through Advanced (production) to Modular (enterprise), each tier adding complexity and cost.

The RAG pipeline has three core stages. First, **retrieval** finds relevant documents using hybrid search (semantic + keyword). Second, **context assembly** ranks, deduplicates, and compresses retrieved chunks into an optimal prompt. Third, **generation** produces a grounded response with source attribution. Each stage has distinct failure modes: retrieval can miss relevant documents (low recall), context assembly can overwhelm the model (lost in the middle), and generation can hallucinate despite good context (low faithfulness).

Modern RAG extends beyond basic vector similarity. Hybrid search combining dense embeddings with sparse BM25 is now the baseline. Re-ranking with cross-encoders improves precision after initial retrieval. Contextual chunking and late chunking preserve document-level semantics that fixed-size chunking loses. GraphRAG enables multi-hop reasoning over entity relationships by building knowledge graphs from documents. Proposition chunking breaks documents into atomic facts for precise retrieval of individual claims.

Choose techniques based on your query complexity and document structure. Start with hybrid search and re-ranking as the foundation, then layer contextual chunking, GraphRAG, or query expansion as needed. Measure everything: Precision@K, Recall@K, faithfulness, and end-to-end latency. The difference between a good and bad chunking strategy alone can create a 9% gap in recall performance.

## Quick Reference

| Phase                     | Goal                            | Key Actions                                               |
| ------------------------- | ------------------------------- | --------------------------------------------------------- |
| 1. Knowledge Base Design  | Structured knowledge foundation | Map sources, define chunking, add metadata                |
| 2. Embedding Strategy     | Semantic understanding          | Select model, benchmark on domain data                    |
| 3. Vector Store           | Scalable storage                | Choose DB, configure index, plan scaling                  |
| 4. Retrieval Pipeline     | Beyond simple similarity        | Hybrid retrieval, query enhancement, re-ranking           |
| 5. Context Assembly       | Optimal LLM context             | Rank, synthesize, compress, mitigate "lost in the middle" |
| 6. Evaluation             | Measure performance             | Precision@K, Recall@K, faithfulness, latency              |
| 7. Production Deploy      | Enterprise reliability          | Containerize, cache, graceful degradation, security       |
| 8. Continuous Improvement | Ongoing enhancement             | Auto-updates, fine-tuning, optimization                   |

| Decision                      | Options                                                |
| ----------------------------- | ------------------------------------------------------ |
| Vector DB (managed)           | Pinecone                                               |
| Vector DB (self-hosted)       | Weaviate, Qdrant                                       |
| Vector DB (lightweight)       | Chroma                                                 |
| Vector DB (existing Postgres) | pgvector                                               |
| Vector DB (billion-scale)     | Milvus / Zilliz                                        |
| Embedding (general)           | `text-embedding-3-large` (3072 dim)                    |
| Embedding (cost-optimized)    | `text-embedding-3-small` (1536 dim)                    |
| Embedding (code)              | Voyage Code 3                                          |
| Embedding (multilingual)      | `multilingual-e5-large`, Cohere embed-v4               |
| Chunking (fixed)              | 500-1000 tokens, 50-100 overlap                        |
| Chunking (semantic)           | Paragraph/section/topic boundaries                     |
| Chunking (recursive)          | Markdown headers, code blocks                          |
| Chunking (contextual)         | LLM-generated summaries prepended to each chunk        |
| Chunking (late)               | Full-document embedding, then pool by chunk boundaries |

| Cost Tier                 | Time      | Monthly Cost | Scale            |
| ------------------------- | --------- | ------------ | ---------------- |
| Naive RAG (prototype)     | 1-2 weeks | $50-150      | <10k documents   |
| Advanced RAG (production) | 3-4 weeks | $200-500     | 10k-1M documents |
| Modular RAG (enterprise)  | 6-8 weeks | $500-2000+   | 1M+ documents    |

| Advanced Technique     | When to Use                                                   |
| ---------------------- | ------------------------------------------------------------- |
| Hybrid search          | Always -- combine semantic + keyword (BM25) for better recall |
| Re-ranking             | When initial retrieval returns noisy results                  |
| Contextual retrieval   | Documents with ambiguous references or pronouns               |
| Late chunking          | Efficiency-focused pipelines with anaphoric references        |
| GraphRAG               | Multi-hop reasoning over structured knowledge relationships   |
| Proposition chunking   | Fact-dense documents requiring atomic retrieval units         |
| Query expansion / HyDE | Queries that are short, ambiguous, or under-specified         |

## Common Mistakes

| Mistake                                                                     | Correct Pattern                                                                                           |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Building RAG before validating user need                                    | Try simpler alternatives first (FAQ, keyword search, concierge MVP); only build RAG with validated demand |
| Using a single retrieval method (semantic only)                             | Implement hybrid retrieval combining semantic search with keyword (BM25) for better recall                |
| Dumping all available data into the knowledge base                          | Curate data sources carefully; filter noise, select authoritative content, and maintain quality           |
| Ignoring the "lost in the middle" problem                                   | Place critical information at the start and end of context; compress mid-section                          |
| Skipping evaluation metrics before production                               | Establish baselines for Precision@K, Recall@K, faithfulness, and hallucination rate before deploying      |
| Using `text-embedding-3-large` at full 3072 dimensions without benchmarking | Test at reduced dimensions (1024 or 1536) first -- often comparable accuracy at lower cost                |
| Fixed-size chunking for all document types                                  | Match chunking strategy to document structure; use semantic or recursive chunking for structured content  |
| Ignoring metadata filtering                                                 | Attach rich metadata (source, date, category) and filter before or during vector search                   |

## Embedding Model Notes

`text-embedding-3-large` (3072 dimensions) remains OpenAI's most capable embedding model. It supports Matryoshka dimensionality reduction via the `dimensions` API parameter -- 1024 dimensions often delivers near-full accuracy at one-third storage cost. `text-embedding-3-small` (1536 dimensions) is a cost-effective alternative at $0.02 per million tokens. For code search, Voyage Code 3 outperforms general-purpose models. For multilingual workloads, consider `multilingual-e5-large` or Cohere embed-v4. Always benchmark on your domain data; general benchmarks do not predict domain-specific performance.

## Vector Store Notes

Pinecone for managed simplicity, Weaviate or Qdrant for self-hosted with hybrid search, Chroma for prototyping, pgvector for teams already on PostgreSQL (practical limit around 10-100M vectors), and Milvus/Zilliz for billion-scale deployments. Choose index type based on tradeoffs: HNSW for speed (higher memory), IVF for scale (requires training), flat for exact search on small datasets only.

Most vector databases now achieve 10-100ms query latency on 1-10M vector datasets. Start with the simplest option that fits your scale requirements and migrate only when you hit concrete performance limits.

## Delegation

- **Discover data sources and assess knowledge base quality**: Use `Explore` agent to catalog documents, evaluate data freshness, and identify authoritative content
- **Implement retrieval pipeline with hybrid search and re-ranking**: Use `Task` agent to build embedding, indexing, retrieval, and evaluation components
- **Design RAG architecture and vector store topology**: Use `Plan` agent to select embedding models, vector databases, chunking strategies, and deployment architecture

> For KB architecture selection, curation workflows, and governance, use the `knowledge-base-manager` skill. For knowledge graph implementation (ontology, entity extraction, graph databases), use the `knowledge-graph-builder` skill.

## References

- [Architecture patterns and prerequisites](references/architecture-patterns.md)
- [Chunking strategies and knowledge base design](references/chunking-strategies.md)
- [Retrieval methods and pipeline design](references/retrieval-methods.md)
- [Evaluation metrics and quality gates](references/evaluation.md)
- [Production deployment and continuous improvement](references/production-deployment.md)
