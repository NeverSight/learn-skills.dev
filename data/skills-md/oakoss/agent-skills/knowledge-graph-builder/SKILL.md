---
name: knowledge-graph-builder
description: >
  Implements knowledge graphs for AI-enhanced relational knowledge. Covers ontology design, graph database selection (Neo4j, Neptune, ArangoDB, TigerGraph), entity extraction, hybrid graph-vector architecture, query patterns, and AI integration.

  Use when implementing knowledge graphs, designing ontologies, extracting entities and relationships, selecting a graph database, or building hybrid graph-vector search. Use for knowledge graph, ontology design, entity resolution, graph RAG, hallucination detection. For architecture selection and governance, use the knowledge-base-manager skill. For document retrieval pipelines, use the rag-implementer skill.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Knowledge Graph Builder

## Overview

Knowledge graphs make implicit relationships explicit, enabling AI systems to reason about connections, verify facts, and reduce hallucinations. They combine structured entity-relationship modeling with semantic search for powerful knowledge retrieval.

**When to use:** Complex entity relationships central to the domain, verifying AI-generated facts against structured knowledge, semantic search combined with relationship traversal, recommendation systems, fraud detection, or pattern recognition.

**When NOT to use:** Simple tabular data (use a relational database), purely document-based search with no relationships (use the `rag-implementer` skill), read-heavy workloads with no traversal needs, or when the team lacks graph modeling expertise. For KB architecture selection and governance, use the `knowledge-base-manager` skill.

## Quick Reference

| Pattern             | Approach                                                                                   | Key Points                                                          |
| ------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Ontology first      | Define entity types, relationships, properties before ingesting data                       | Changing schema later is expensive; validate with domain experts    |
| Entity resolution   | Deduplicate aggressively during extraction                                                 | "Apple Inc" = "Apple" = "Apple Computer" must resolve to one entity |
| Confidence scoring  | Attach 0.0-1.0 score + source to every relationship                                        | Enables filtering by reliability, critical for AI grounding         |
| Hybrid architecture | Graph traversal (structured) + vector search (semantic)                                    | Vector finds candidates, graph expands context via relationships    |
| Incremental build   | Core entities first, validate against target queries, then expand                          | Avoid building the full graph before testing with real queries      |
| Database selection  | Neo4j (general), Neptune (AWS managed), ArangoDB (multi-model), TigerGraph (massive scale) | Match database to scale, infrastructure, and query complexity       |

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                              |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Ingesting entities before designing the ontology            | Define and validate the ontology with domain experts first; changing later is expensive      |
| Skipping entity resolution and deduplication                | Deduplicate aggressively so "Apple Inc", "Apple", and "Apple Computer" resolve to one entity |
| Omitting confidence scores on relationships                 | Attach a 0.0-1.0 confidence score and source to every relationship                           |
| Using only graph traversal without vector search            | Implement hybrid architecture combining graph traversal with semantic vector search          |
| Building the full graph before validating with real queries | Start with core entities, test against target queries, then expand incrementally             |
| Choosing a database before understanding scale requirements | Evaluate query patterns, data volume, and infrastructure constraints before selecting        |

## Delegation

- **Extract entities and relationships from unstructured text**: Use `Task` agent to run NER pipelines and build relationship triples
- **Evaluate graph database options for project requirements**: Use `Explore` agent to compare Neo4j, Neptune, ArangoDB, and TigerGraph against scale and query needs
- **Design ontology and hybrid architecture for a new domain**: Use `Plan` agent to define entity types, relationship schemas, and graph-vector integration strategy
- For hybrid KG+RAG systems, delegate to the `rag-implementer` skill
- For knowledge-graph-powered agent workflows, delegate to the `agent-patterns` skill

## References

- [Ontology Design](references/ontology-design.md) — Entity types, relationships, properties, RDF schema, validation
- [Database Selection](references/database-selection.md) — Neo4j, Neptune, ArangoDB, TigerGraph comparison and setup
- [Entity Extraction](references/entity-extraction.md) — NER pipeline, relationship extraction, LLM-based extraction
- [Hybrid Architecture](references/hybrid-architecture.md) — Graph + vector integration, hybrid search implementation
- [Query Patterns](references/query-patterns.md) — Cypher queries, API design, common traversal patterns
- [AI Integration](references/ai-integration.md) — KG-RAG, hallucination detection, grounded response generation
