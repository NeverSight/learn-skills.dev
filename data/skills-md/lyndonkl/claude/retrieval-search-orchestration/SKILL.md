---
name: retrieval-search-orchestration
description: Use when designing retrieval strategies for querying knowledge graphs in RAG systems. Invoke when user mentions retrieval strategy, search orchestration, global-first retrieval, local-first retrieval, U-shaped retrieval, query decomposition, multi-hop reasoning, provenance tracking, or citation in GraphRAG. Provides retrieval pattern selection, query rewriting, and provenance design.
---

## Table of Contents
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Step Descriptions](#step-descriptions)
- [Retrieval Pattern Selection Guide](#retrieval-pattern-selection-guide)
- [Query Decomposition Patterns](#query-decomposition-patterns)
- [Output Template](#output-template)

# Retrieval & Search Orchestration

## What Is It?

Design retrieval strategies for querying knowledge graphs in Retrieval-Augmented Generation (RAG) systems. This skill covers pattern selection for different query types, query decomposition for complex multi-hop questions, ranking and constraint configuration, and provenance tracking to ensure every generated answer can be traced back to its source evidence.

## Workflow

**COPY THIS CHECKLIST** and work through each step:

- [ ] 1. Analyze query types and requirements
- [ ] 2. Select retrieval pattern
- [ ] 3. Design query decomposition strategy
- [ ] 4. Configure ranking and constraints
- [ ] 5. Design provenance tracking
- [ ] 6. Define fallback strategies
- [ ] 7. Produce retrieval strategy specification

## Step Descriptions

### Step 1: Analyze Query Types and Requirements

Classify the queries your system must handle. Common categories include:
- **Factoid lookups**: single-entity, single-hop (e.g., "What is the capital of France?")
- **Exploratory/thematic**: broad questions requiring aggregation across many entities (e.g., "What are the main themes in this corpus?")
- **Multi-hop reasoning**: questions requiring traversal of multiple relationships (e.g., "Which drugs treat diseases caused by gene X?")
- **Temporal queries**: questions bounded by time ranges or requiring sequence understanding
- **Constrained queries**: questions with type or attribute filters (e.g., "List all clinical trials after 2020 for drug Y")

Identify the distribution of these query types in your use case to guide pattern selection.

### Step 2: Select Retrieval Pattern

Use the Retrieval Pattern Selection Guide below to choose the right approach for your query distribution. See `resources/methodology.md` for detailed implementation guidance on each pattern.

### Step 3: Design Query Decomposition Strategy

For complex queries, break them into sub-queries that can be independently resolved and then aggregated. Approaches include LLM-as-controller decomposition, self-ask chains, and ReAct-style interleaved reasoning and retrieval. See the Query Decomposition Patterns section below and `resources/methodology.md` for details.

### Step 4: Configure Ranking and Constraints

Define how retrieved results are scored, ranked, and filtered:
- Embedding similarity thresholds
- Graph distance penalties
- Type-based pre-filters or post-filters
- Confidence score minimums
- Temporal decay functions for time-sensitive data

### Step 5: Design Provenance Tracking

Ensure every piece of retrieved information carries metadata about its origin. This includes source document IDs, extraction timestamps, confidence scores, and evidence chain construction. See `resources/provenance-patterns.md` for annotation approaches, confidence scoring, and LLM integration patterns.

### Step 6: Define Fallback Strategies

Design what happens when primary retrieval fails or returns insufficient results:
- Iterative deepening (expand hop count)
- Query relaxation (remove constraints progressively)
- Parallel exploration (try multiple patterns simultaneously)
- Graceful degradation (return partial results with confidence indicators)

### Step 7: Produce Retrieval Strategy Specification

Compile the full specification using the Output Template below.

---

## Retrieval Pattern Selection Guide

| Pattern | Best For | Mechanism | Trade-offs | Section Ref |
|---|---|---|---|---|
| **Global-First** | Broad thematic queries, corpus-level summaries | Community detection, top-down traversal of summarized indexes | High-level coverage; may miss specific details | 3.1 |
| **Local-First** | Entity-centric lookups, neighborhood exploration | Seed entity linking, 1-2 hop neighborhood expansion with embedding gates | High precision for known entities; limited scope | 3.2 |
| **U-Shaped Hybrid** | Complex queries needing both breadth and depth | Coarse-to-fine bidirectional search, top-down then bottom-up refinement | Best coverage; higher latency and complexity | 3.3 |
| **Query Decomposition** | Multi-hop reasoning, composite questions | LLM breaks query into sub-queries, sequential retrieval, aggregation | Handles complex questions; depends on decomposition quality | 3.4 |
| **Temporal** | Time-bounded or sequence-dependent queries | Time-slice filtering, episodic windowing, time-decay ranking | Captures temporal dynamics; needs temporal metadata | 3.5 |
| **Constraint-Guided** | Type-filtered or rule-bounded queries | Pre-filter + vector search, symbolic query then neural re-rank | Reduces search space; requires well-typed schema | 3.6 |

**Selection heuristic**: Start with the dominant query type in your system. If queries are mixed, consider U-Shaped Hybrid as a default with fallback to specialized patterns.

---

## Query Decomposition Patterns

### LLM-as-Controller

The LLM receives the original query and generates a plan of sub-queries:

```
Original: "Which drugs treat diseases linked to mutations in BRCA1?"
Sub-query 1: "What diseases are linked to mutations in BRCA1?"
Sub-query 2: "What drugs treat [diseases from sub-query 1]?"
Aggregation: Combine results, deduplicate, rank by evidence strength
```

### Self-Ask Chain

The model iteratively asks itself follow-up questions, retrieving after each:

```
Q: "What is the relationship between company X and technology Y?"
Follow-up 1: "What products does company X produce?" -> retrieve
Follow-up 2: "Which of those products use technology Y?" -> retrieve
Follow-up 3: "What partnerships exist between X and Y providers?" -> retrieve
Synthesize: Combine all retrieved evidence into final answer
```

### ReAct Pattern

Interleave reasoning and retrieval actions:

```
Thought: I need to find the connection between entity A and entity C
Action: Search KG for paths between A and C (max 3 hops)
Observation: Found path A -> B -> C via relationship R1 and R2
Thought: I should verify this path with supporting evidence
Action: Retrieve source documents for edges A-B and B-C
Observation: Edge A-B supported by [doc1, doc2], edge B-C supported by [doc3]
Answer: A connects to C through B, supported by 3 source documents
```

### Tool-Augmented Retrieval

Generate formal queries (Cypher, SPARQL) for structured graph traversal:

```
LLM generates: MATCH (d:Drug)-[:TREATS]->(dis:Disease)<-[:CAUSES]-(g:Gene {name: 'BRCA1'})
               RETURN d.name, dis.name, g.name
Execute against graph database
Post-process results with LLM for natural language answer
```

---

## Output Template

```markdown
# Retrieval Strategy Specification

## System Context
- **Domain**: [e.g., biomedical, legal, financial]
- **Knowledge Graph Type**: [e.g., property graph, RDF, hybrid]
- **Primary Query Types**: [list dominant query categories]
- **Scale**: [approximate node/edge counts, query volume]

## Retrieval Pattern
- **Primary Pattern**: [selected pattern from guide]
- **Rationale**: [why this pattern fits the query distribution]
- **Secondary/Fallback Pattern**: [if applicable]

## Query Decomposition
- **Strategy**: [LLM-as-controller / self-ask / ReAct / tool-augmented / none]
- **Max Sub-queries**: [limit per original query]
- **Aggregation Method**: [union / intersection / ranked merge / LLM synthesis]

## Ranking & Constraints
- **Similarity Threshold**: [minimum embedding similarity score]
- **Max Hop Distance**: [maximum graph traversal depth]
- **Type Filters**: [entity/relationship type constraints]
- **Temporal Constraints**: [time windows, decay functions]
- **Confidence Minimum**: [minimum source confidence for inclusion]

## Provenance Design
- **Annotation Method**: [metadata fields / evidence nodes / named graphs / reification]
- **Confidence Scoring**: [source reliability tiers, aggregation rules]
- **Citation Format**: [inline / post-hoc / both]
- **Conflict Resolution**: [timestamp priority / source authority / LLM adjudication]

## Fallback Strategy
- **Primary Fallback**: [iterative deepening / query relaxation / parallel exploration]
- **Max Retry Depth**: [number of fallback attempts]
- **Degradation Policy**: [partial results with confidence / explicit uncertainty / escalation]

## Evaluation Criteria
- Reference: `resources/evaluators/rubric_retrieval.json`
- **Target Score**: [minimum acceptable weighted score]
```
