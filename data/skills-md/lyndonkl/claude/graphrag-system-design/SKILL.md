---
name: graphrag-system-design
description: Use when designing complete GraphRAG systems that combine graph retrieval with LLM reasoning. Invoke when user mentions GraphRAG system, technology stack, Neo4j with LLM, LangChain graph, LlamaIndex knowledge graph, community detection for RAG, hybrid symbol-vector integration, production GraphRAG, or domain-specific graph RAG. Provides architecture design, technology selection, and domain customization guidance.
---

## Table of Contents
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [GraphRAG Pattern Selection](#graphrag-pattern-selection)
- [Integration Architecture](#integration-architecture)
- [Output Template](#output-template)

# GraphRAG System Design

## What Is It?

This skill helps you **design complete GraphRAG systems integrating graph databases, vector stores, orchestration frameworks, and LLM reasoning**. Given a domain and retrieval requirements, it guides you through pattern selection, technology stack decisions, integration pipeline design, and domain-specific customizations.

**The payoff**: GraphRAG systems overcome fundamental limitations of flat vector RAG by adding relational structure for multi-hop reasoning, provenance tracking for explainability, and structured retrieval that preserves semantic context across connected entities.

## Workflow

**COPY THIS CHECKLIST** and work through each step:

```
GraphRAG System Design Progress:
- [ ] Step 1: Analyze domain requirements
- [ ] Step 2: Select GraphRAG pattern
- [ ] Step 3: Choose technology stack
- [ ] Step 4: Design integration pipeline
- [ ] Step 5: Apply domain customizations
- [ ] Step 6: Define deployment strategy
- [ ] Step 7: Produce specification
```

**Step 1: Analyze domain requirements**

Characterize the retrieval problem: query complexity (single-hop vs multi-hop), data volume and update frequency, compliance constraints, latency requirements, and explainability needs. Determine whether graph structure adds value over flat retrieval -- multi-hop reasoning, entity disambiguation, and relationship-aware context assembly are strong signals for GraphRAG. Define the user personas and query patterns the system must serve.

**Step 2: Select GraphRAG pattern**

Choose the core retrieval architecture using the [GraphRAG Pattern Selection](#graphrag-pattern-selection) guide. Match your query patterns to the appropriate pattern: Hybrid Symbol-Vector for mixed structured/unstructured queries, Subgraph-on-Demand for focused context assembly, or Community-Based Global Summarization for broad thematic queries. For detailed pattern descriptions, see [Methodology Reference](./resources/methodology.md).

**Step 3: Choose technology stack**

Select components for each architectural layer: graph database, vector database, orchestration framework, and LLM provider. Use the [Technology Stacks Reference](./resources/technology-stacks.md) for component-by-component comparison. Key decisions: single-system vs multi-system hybrid, managed vs self-hosted, framework-based vs custom pipeline. Consider team expertise, budget constraints, and existing infrastructure.

**Step 4: Design integration pipeline**

Define the end-to-end data flow from ingestion through generation. The core pipeline stages: Ingest (raw data) -> Extract (entities and relations) -> Build KG (populate graph) -> Index (vector embeddings + graph indices) -> Retrieve (hybrid graph+vector search) -> Generate (LLM with graph-grounded context) -> Cite (provenance from graph paths). Design the query routing logic that determines when to use graph traversal, vector search, or both. See [Methodology Reference](./resources/methodology.md) for pipeline design considerations.

**Step 5: Apply domain customizations**

Adapt the generic architecture to domain-specific requirements: ontology selection (UMLS for healthcare, FIBO for finance), compliance patterns (HIPAA access control, regulatory audit trails), and domain retrieval patterns (temporal graphs for finance, layered patient graphs for clinical). See [Domain Patterns Reference](./resources/domain-patterns.md) for domain-specific guidance.

**Step 6: Define deployment strategy**

Specify the deployment architecture: graph database sizing and clustering, vector index configuration, caching strategy, batch vs real-time ingestion, monitoring and observability, and scaling plan. Define performance SLAs for query latency, throughput, and freshness. Plan for graph maintenance: incremental updates, schema evolution, and data quality monitoring.

**Step 7: Produce specification**

Compile the complete system design specification using the [Output Template](#output-template). Validate against the quality rubric at [System Design Rubric](./resources/evaluators/rubric_system_design.json). Ensure all components are connected end-to-end with clear data flows, error handling, and fallback strategies.

## GraphRAG Pattern Selection

| Pattern | Query Type | Mechanism | Best For | Trade-offs |
|---------|-----------|-----------|----------|------------|
| **Hybrid Symbol-Vector** | Mixed structured + semantic | Pre-filter by graph type/constraint then rank by embedding similarity; or broad vector search then graph-guided expansion | Systems needing both precise structural queries and fuzzy semantic search; enterprise QA with entity disambiguation | Higher complexity; requires synchronized graph + vector indices; latency depends on filter-then-rank vs expand strategy |
| **Subgraph-on-Demand** | Focused multi-hop | Build temporary query-specific subgraphs rather than querying one monolithic graph; extract relevant neighborhood, embed, retrieve | Real-time applications needing focused context; systems with frequent updates; cost-sensitive deployments | Cold-start latency for subgraph construction; requires efficient subgraph extraction; context may miss distant but relevant nodes |
| **Community-Based Global Summarization** | Broad thematic / global | Detect communities/clusters in graph, embed summaries of each community, retrieve relevant community then drill into entity details; Microsoft GraphRAG pattern | Broad "what is X about?" queries; corpus-level summarization; thematic exploration across large knowledge bases | Requires periodic community detection (batch); summaries may lose detail; community boundaries can split related concepts |

### Choosing a Pattern

- **If queries need both "find entities of type X" and "find semantically similar content"** -> Hybrid Symbol-Vector
- **If queries are focused and context window cost matters** -> Subgraph-on-Demand
- **If queries are broad, thematic, or corpus-spanning** -> Community-Based Global Summarization
- **If requirements span multiple patterns** -> Combine patterns with a query router that dispatches to the appropriate retrieval path

## Integration Architecture

A complete GraphRAG system integrates four core component layers:

```
+------------------+     +------------------+     +----------------------+     +-----------+
|  Graph Database  |     |  Vector Database |     |  Orchestration       |     |    LLM    |
|  (Structure)     |<--->|  (Semantics)     |<--->|  Framework           |<--->| (Reason)  |
|                  |     |                  |     |                      |     |           |
|  Neo4j / Tiger   |     |  Pinecone /      |     |  LangChain /         |     |  GPT-4 /  |
|  Graph / Neptune |     |  Weaviate /      |     |  LlamaIndex /        |     |  Claude / |
|  / GraphDB       |     |  Qdrant / pgvec  |     |  LangGraph / Custom  |     |  Llama   |
+------------------+     +------------------+     +----------------------+     +-----------+
        |                        |                          |
        v                        v                          v
  Graph Traversal          Embedding Search           Pipeline Logic
  Multi-hop Paths          Semantic Ranking           Query Routing
  Schema Filtering         Similarity Scores          Context Assembly
  Provenance Chains        Hybrid Re-ranking          Citation Generation
```

**Key integration decisions:**
- **Graph-first vs text-first pipeline**: Does the query first hit the graph (structured filter) or the vector store (semantic search)?
- **Single-system vs multi-system**: Use Neo4j vector index (single system) or Neo4j + Pinecone (multi-system)?
- **Framework vs custom**: LangChain/LlamaIndex for rapid development, or custom pipeline for maximum control?
- **Synchronization**: How are graph and vector indices kept consistent during updates?

## Output Template

```
GRAPHRAG SYSTEM DESIGN SPECIFICATION
======================================

Project: [Project name]
Domain: [Target domain]
Date: [Date]
Author: [Author]

1. DOMAIN REQUIREMENTS
   Query Patterns: [Single-hop / Multi-hop / Thematic / Mixed]
   Data Volume: [Document count, entity count estimates]
   Update Frequency: [Real-time / Daily / Weekly / Batch]
   Latency Requirements: [p50, p95, p99 targets]
   Compliance: [HIPAA / GDPR / SOX / None]
   Explainability: [Required / Nice-to-have / Not needed]

2. GRAPHRAG PATTERN
   Primary Pattern: [Hybrid Symbol-Vector / Subgraph-on-Demand / Community-Based]
   Secondary Pattern: [If hybrid approach, specify]
   Query Router: [How queries are dispatched to retrieval paths]
   Rationale: [Why this pattern fits the requirements]

3. TECHNOLOGY STACK
   Graph Database: [Product, version, deployment mode]
     Justification: [Why this choice]
   Vector Database: [Product, version, deployment mode]
     Justification: [Why this choice]
   Orchestration: [Framework or custom pipeline]
     Justification: [Why this choice]
   LLM Provider: [Model, API or self-hosted]
     Justification: [Why this choice]
   Supporting Infrastructure: [Cache, queue, monitoring tools]

4. INTEGRATION PIPELINE
   Ingestion:
     - Source types: [Documents, APIs, databases]
     - Processing: [Chunking strategy, metadata extraction]
   Extraction:
     - Entity extraction: [Method, model, confidence threshold]
     - Relation extraction: [Method, schema enforcement]
   Knowledge Graph Build:
     - Schema: [Node types, edge types, properties]
     - Population: [Batch / streaming, deduplication strategy]
   Indexing:
     - Graph indices: [Index types, query optimization]
     - Vector indices: [Embedding model, dimension, index type]
   Retrieval:
     - Graph retrieval: [Traversal strategy, depth limits]
     - Vector retrieval: [Top-k, similarity threshold]
     - Hybrid fusion: [How graph and vector results combine]
   Generation:
     - Context assembly: [How retrieved data becomes LLM context]
     - Prompt template: [Structure for graph-grounded generation]
   Citation:
     - Provenance: [How sources are tracked and surfaced]

5. DOMAIN CUSTOMIZATIONS
   Ontology: [Domain ontology or taxonomy used]
   Compliance Controls: [Access control, audit, encryption]
   Domain-Specific Patterns: [Temporal graphs, layered architecture, etc.]

6. DEPLOYMENT STRATEGY
   Infrastructure: [Cloud provider, regions, HA configuration]
   Scaling Plan: [Graph DB scaling, vector DB scaling, LLM scaling]
   Monitoring: [Metrics, alerts, dashboards]
   Maintenance: [Graph update strategy, schema evolution plan]

7. PERFORMANCE TARGETS
   Query Latency: [p50, p95, p99]
   Throughput: [Queries per second]
   Freshness: [Time from data change to queryable]
   Accuracy: [Retrieval precision/recall targets]

8. RISK AND MITIGATION
   - [Risk 1]: [Mitigation strategy]
   - [Risk 2]: [Mitigation strategy]
   - [Risk 3]: [Mitigation strategy]

NEXT STEPS:
- Build proof-of-concept with sample data
- Benchmark retrieval quality against baseline RAG
- Load test with production-scale data
- Iterate schema and retrieval strategy based on evaluation
```
