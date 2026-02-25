---
name: knowledge-base-manager
description: 'Knowledge base architecture selection, curation, and governance. Use when choosing between document-based (RAG), entity-based (graph), or hybrid KB architectures, establishing content curation workflows, implementing versioning and governance, or evaluating quality metrics. For building retrieval pipelines, use the rag-implementer skill. For building knowledge graphs, use the knowledge-graph-builder skill.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Knowledge Base Manager

## Overview

Provides a structured methodology for selecting, designing, and governing knowledge bases. Covers architecture decisions (document-based vs entity-based vs hybrid), content curation, quality metrics, versioning strategies, and maintenance governance. Use when choosing a KB architecture, establishing curation workflows, or building governance processes for organizational knowledge.

**When NOT to use:** Static documentation suffices, fewer than 50 FAQ items cover all questions, or no maintenance resources are available. For implementing retrieval pipelines (chunking, embeddings, vector stores), use the `rag-implementer` skill. For implementing knowledge graphs (ontology, entity extraction, graph databases), use the `knowledge-graph-builder` skill.

## Quick Reference

| Aspect                 | Options                                            | Key Considerations                                                 |
| ---------------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| **Architecture**       | Document-based (RAG), Entity-based (Graph), Hybrid | Match to query patterns; start simple, add complexity when needed  |
| **Document-based**     | Vector DB (Pinecone, Weaviate, pgvector)           | Best for docs, FAQs, manuals; semantic search; easy to add content |
| **Entity-based**       | Graph DB (Neo4j, ArangoDB)                         | Best for org charts, catalogs, networks; relationship traversal    |
| **Hybrid**             | Both + linking layer                               | Enterprise, medical, legal; combined queries; highest complexity   |
| **When to skip KB**    | Static docs, <50 FAQ items                         | No maintenance resources, information never changes                |
| **Implementation**     | 6 phases                                           | Audit, Curation, Storage, Quality, Versioning, Governance          |
| **Accuracy target**    | >90% on test questions                             | Create 100+ test questions with known correct answers              |
| **Coverage target**    | >80% questions answerable                          | Validate against real user queries continuously                    |
| **Freshness target**   | <30 days average age                               | Automated freshness monitoring + scheduled updates                 |
| **Consistency target** | >95% conflict-free                                 | Deduplication + single source of truth                             |
| **Query latency**      | <100ms median                                      | Caching and optimization for common access patterns                |
| **Storage tech**       | pgvector, Pinecone, Weaviate, Chroma               | pgvector for existing Postgres; Pinecone for managed scale         |
| **Index types**        | HNSW, IVFFlat                                      | HNSW for recall; IVFFlat for frequently rebuilt indexes            |
| **Ingestion pipeline** | Load, clean, chunk, embed, store                   | Chunk at semantic boundaries; 512 tokens max; 10-15% overlap       |
| **Deduplication**      | Content hashing, semantic similarity               | Hash for exact dupes; cosine similarity >0.95 for semantic dupes   |
| **Quality testing**    | Recall@K, MRR, accuracy sampling                   | 100+ test questions; measure recall@10 >0.8 and MRR >0.7           |
| **Drift detection**    | Embedding distribution monitoring                  | Track mean shift; alert when >0.1 threshold                        |
| **Versioning**         | Snapshot, Event-sourced, Git-style                 | Snapshot for simple; event-sourced for audit; git-style for teams  |
| **Maintenance**        | Daily, Weekly, Monthly, Quarterly                  | Establish schedule from day 1; monitor errors and user feedback    |

## Common Mistakes

| Mistake                                                    | Correct Pattern                                                                        |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Ingesting raw data without curation or normalization       | Curate, clean, and deduplicate before ingesting; quality over quantity                 |
| Skipping version control for KB content                    | Implement versioning from day one with rollback and audit trail                        |
| Building a KB without validating against user questions    | Start with user research and test against real queries for >90% accuracy               |
| Choosing hybrid architecture when document-based suffices  | Match architecture to actual query patterns; start simple, add complexity when needed  |
| Launching without freshness monitoring or update schedules | Set up automated freshness checks and scheduled content reviews                        |
| No provenance tracking on knowledge entries                | Always track source URL, timestamp, author, and confidence score                       |
| Duplicate information across sources                       | Establish single source of truth; merge similar entries with conflict resolution rules |
| Perfectionism delaying launch                              | Launch at 80% coverage and iterate based on real usage data                            |

## Delegation

- **Audit existing knowledge sources and classify content types**: Use `Explore` agent to inventory documents, assess quality, and identify gaps
- **Implement end-to-end KB pipeline with storage and retrieval**: Use `Task` agent to deploy database, configure search, and run quality checks
- **Design KB architecture and governance model**: Use `Plan` agent to select between document-based, entity-based, or hybrid approaches

> For implementing document retrieval pipelines (chunking, embeddings, vector stores, hybrid search), use the `rag-implementer` skill. For implementing knowledge graphs (ontology design, entity extraction, graph databases), use the `knowledge-graph-builder` skill.

## References

- [Architecture and Types](references/architecture.md) -- KB types, decision framework, knowledge classification
- [Curation and Ingestion](references/curation.md) -- extraction, cleaning, deduplication, provenance tracking
- [Storage and Retrieval](references/storage.md) -- database selection, interfaces, technology stacks
- [Quality Control](references/quality-control.md) -- metrics, validation strategies, continuous monitoring
- [Versioning](references/versioning.md) -- snapshot, event-sourced, and git-style approaches
- [Governance](references/governance.md) -- maintenance schedules, roles, change processes
