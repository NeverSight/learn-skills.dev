---
name: knowledge-graph-construction
description: Use when designing and building knowledge graphs from unstructured data. Invoke when user mentions entity extraction, schema design, LPG vs RDF, graph data model, ontology alignment, knowledge graph construction, or building a KG for RAG. Provides extraction pipelines, schema patterns, and data model selection guidance.
---

## Table of Contents
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Architecture Selection Guide](#architecture-selection-guide)
- [Schema Patterns](#schema-patterns)
- [Output Template](#output-template)

# Knowledge Graph Construction

## What Is It?

This skill helps you **design and build knowledge graphs from unstructured or semi-structured data sources**. Given a domain and data corpus, it guides you through data model selection, schema design, entity/relation extraction pipelines, and layered architecture construction.

**The payoff**: Well-constructed knowledge graphs provide structured, verified facts that ground LLM reasoning, reduce hallucination, enable explainable retrieval, and support complex multi-hop queries that flat vector search cannot handle.

## Workflow

**COPY THIS CHECKLIST** and work through each step:

```
KG Construction Progress:
- [ ] Step 1: Identify data sources and domain scope
- [ ] Step 2: Select graph data model
- [ ] Step 3: Design schema and ontology
- [ ] Step 4: Configure extraction pipeline
- [ ] Step 5: Define layered architecture
- [ ] Step 6: Validate and quality-check the graph
```

**Step 1: Identify data sources and domain scope**

Catalog the input data: document types (papers, clinical notes, web pages, logs), volume, update frequency, and language. Define the domain boundary -- what entity types and relation types matter for the target use case. Determine whether the KG will serve RAG retrieval, reasoning/inference, analytics, or a combination. This scoping step prevents over-extraction and keeps the schema focused.

**Step 2: Select graph data model**

Choose the underlying data model using the [Architecture Selection Guide](#architecture-selection-guide). Key trade-offs: LPG for flexibility and rapid prototyping, RDF/OWL for standards-based interoperability and inference, Hypergraphs for complex N-ary relations, Temporal Graphs for time-evolving knowledge. Consider query language, tooling maturity, and vector integration needs. For detailed model comparisons, see [Data Models Reference](./resources/data-models.md).

**Step 3: Design schema and ontology**

Define node types (entity classes), edge types (relation classes), and property schemas. Apply patterns from [Schema Patterns](#schema-patterns): entity-relation for simple domains, event reification for N-ary relations, layered tiers for multi-source integration. Decide on controlled vocabularies, cardinality constraints, and whether to adopt or extend an existing ontology (e.g., Schema.org, UMLS, SNOMED). For methodology details, see [Methodology Reference](./resources/methodology.md).

**Step 4: Configure extraction pipeline**

Build the pipeline that populates the graph. Core components: LLM-assisted entity extraction with multi-round verification, relation extraction via prompt-based or dependency-parsing methods, entity normalization (synonym merging, ontology linking), and schema enforcement through post-processing validation. Use few-shot examples in prompts to improve extraction consistency. Include a second-pass LLM verification to catch missed entities. For full pipeline design, see [Methodology Reference](./resources/methodology.md).

**Step 5: Define layered architecture**

Structure the KG into tiers for maintainability and trust. A common pattern: Layer 1 (instance data) holds user-specific or case-specific entities and relations; Layer 2 (domain knowledge) holds curated facts from literature or domain experts; Layer 3 (canonical ontology) holds the formal schema and upper ontology. Add provenance and evidence layering so every fact traces back to its source document, extraction method, and confidence score. Temporal subgraphs capture time-indexed state for domains where knowledge evolves.

**Step 6: Validate and quality-check the graph**

Run validation at multiple levels: schema conformance (do all nodes and edges match declared types?), coverage (are expected entity types populated?), consistency (no contradictory edges), and completeness (sample-based human review). Use a second LLM as a validator to fact-check extracted triples against source documents. Compute graph statistics (node degree distribution, connected components, orphan nodes) to identify extraction gaps. Quality criteria are defined in [Quality Rubric](./resources/evaluators/rubric_kg_construction.json).

## Architecture Selection Guide

### By Use Case

| Model | Flexibility | Standardization | Reasoning | Vector Integration | Query Language | Best For |
|-------|-------------|-----------------|-----------|-------------------|----------------|----------|
| LPG | High | Low | Limited | Native (Neo4j) | Cypher, Gremlin | Rapid development, RAG pipelines |
| RDF/OWL | Medium | High | Full (OWL-DL) | Via extensions | SPARQL | Interoperability, ontology-heavy domains |
| Hypergraph | High | Low | Limited | Custom | Custom APIs | N-ary relations, multi-entity events |
| Temporal | Medium | Low | Time-based | Via extensions | Temporal Cypher | Evolving knowledge, episodic memory |

### By Domain

| Domain | Recommended Model | Rationale |
|--------|-------------------|-----------|
| Biomedical / Clinical | RDF/OWL | UMLS/SNOMED ontologies, reasoning needed |
| Enterprise / RAG | LPG | Fast iteration, vector search integration |
| Event-centric (news, logs) | Hypergraph or Temporal | Multi-participant events, time evolution |
| Legal / Compliance | RDF/OWL | Formal reasoning, provenance chains |
| Scientific Literature | LPG + Layered | Flexible extraction, layered trust |

## Schema Patterns

### Entity-Relation Pattern

The simplest pattern. Nodes represent entities, edges represent binary relations. Properties on nodes hold attributes; properties on edges hold relation metadata (confidence, source, timestamp).

```
(:Person {name, role}) -[:WORKS_AT {since}]-> (:Organization {name, type})
(:Drug {name, class})  -[:TREATS {efficacy}]-> (:Disease {name, icd_code})
```

Best for: domains with primarily binary relationships and moderate complexity.

### Event Reification Pattern

Model N-ary relations and complex events as first-class nodes. An event node connects to all participants via typed role edges. This avoids information loss from forcing N-ary relations into binary edges.

```
(:ClinicalTrial {id, phase, start_date})
  -[:HAS_DRUG]->     (:Drug {name})
  -[:HAS_CONDITION]-> (:Disease {name})
  -[:HAS_OUTCOME]->   (:Outcome {measure, value})
  -[:CONDUCTED_BY]->  (:Organization {name})
```

Best for: events with multiple participants, clinical data, news events, financial transactions.

### Layered Tier Pattern

Separate the graph into trust-differentiated layers that can be queried independently or together.

```
Layer 3 (Canonical Ontology): Formal class hierarchy, relation definitions, constraints
Layer 2 (Domain Knowledge):   Curated facts from literature, expert-validated
Layer 1 (Instance Data):      Extracted from user documents, case-specific, lower confidence
```

Cross-layer edges link instances to domain concepts and domain concepts to ontology classes. Provenance metadata on every edge records: source document, extraction method, confidence score, and timestamp.

Best for: multi-source integration, RAG with trust scoring, enterprise knowledge management.

## Output Template

```
KNOWLEDGE GRAPH CONSTRUCTION SPECIFICATION
============================================

Domain: [Target domain and scope]
Use Case: [RAG / Reasoning / Analytics / Hybrid]
Data Sources: [List of input data types and volumes]

Data Model: [LPG / RDF / Hypergraph / Temporal]
Query Language: [Cypher / SPARQL / Gremlin / Custom]
Storage Backend: [Neo4j / Amazon Neptune / Virtuoso / etc.]

Schema Definition:
  Node Types:
  1. [EntityType] - [description]
     Properties: [list with types]
  2. [EntityType] - [description]
     Properties: [list with types]
  3. [Continue for each node type...]

  Edge Types:
  1. [RelationType] (source -> target) - [description]
     Properties: [list with types]
  2. [Continue for each edge type...]

  Constraints:
  - [Cardinality, uniqueness, required properties]

Extraction Pipeline:
  1. Entity Extraction
     - Method: [LLM-assisted / NER / Hybrid]
     - Prompt template: [summary or reference]
     - Verification: [Multi-round / Second-LLM / Manual sample]
  2. Relation Extraction
     - Method: [Prompt-based / Dependency parsing / Hybrid]
     - Few-shot examples: [count and source]
  3. Normalization
     - Deduplication: [method]
     - Ontology linking: [target ontology]
     - Synonym resolution: [approach]

Layered Architecture:
  Layer 1 (Instance): [description of instance-level data]
  Layer 2 (Domain):   [description of curated domain knowledge]
  Layer 3 (Ontology): [description of formal schema]
  Provenance: [How source/confidence/timestamp are tracked]

Validation Plan:
  - Schema conformance: [automated checks]
  - Coverage: [expected entity/relation counts]
  - Consistency: [contradiction detection method]
  - Human review: [sampling strategy]

Estimated Scale: [node count, edge count, properties per node]
Key Dependencies: [libraries, APIs, ontologies]

NEXT STEPS:
- Implement extraction pipeline on sample data
- Populate graph and run validation suite
- Iterate schema based on extraction results
- Integrate with downstream application (RAG, reasoning, etc.)
```
