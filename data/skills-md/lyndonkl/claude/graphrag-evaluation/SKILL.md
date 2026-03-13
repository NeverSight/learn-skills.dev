---
name: graphrag-evaluation
description: Use when evaluating GraphRAG system quality across knowledge graph completeness, retrieval relevance, answer correctness, and reasoning verification. Invoke when user mentions evaluate GraphRAG, quality metrics, benchmark, hallucination reduction, answer correctness, multi-step reasoning evaluation, test my GraphRAG, or measure RAG performance. Provides evaluation frameworks, metric selection, and testing protocols.
---

## Table of Contents
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Evaluation Dimensions](#evaluation-dimensions)
- [Metric Selection Guide](#metric-selection-guide)
- [Output Template](#output-template)

# GraphRAG Evaluation

## What Is It?

Evaluate GraphRAG systems across multiple dimensions -- KG quality, retrieval effectiveness, answer correctness, reasoning depth, and hallucination prevention. This skill provides structured evaluation frameworks, metric selection guidance, and testing protocols to systematically measure and improve GraphRAG system performance.

GraphRAG systems combine knowledge graphs with retrieval-augmented generation, introducing unique evaluation challenges beyond standard RAG. The knowledge graph itself must be assessed for completeness and accuracy, retrieval must be measured for both recall and precision across multi-hop paths, answers must be verified for correctness and grounding, and reasoning chains must be validated step by step. This skill guides you through each dimension with concrete metrics and testing protocols.

## Workflow

**COPY THIS CHECKLIST** and work through each step:

- [ ] Step 1. Identify Evaluation Scope
- [ ] Step 2. Select Metrics
- [ ] Step 3. Design Test Protocol
- [ ] Step 4. Test Reasoning Capabilities
- [ ] Step 5. Measure Hallucination Rate
- [ ] Step 6. Compare Against Baselines
- [ ] Step 7. Produce Evaluation Report

### Step 1. Identify Evaluation Scope

Define what aspects of your GraphRAG system you need to evaluate and why. Determine whether you are evaluating the full pipeline or specific components (KG construction, retrieval, generation). Clarify the use case context: domain, query complexity, expected reasoning depth.

See [methodology.md](resources/methodology.md) for the full evaluation dimensions framework.

### Step 2. Select Metrics

Choose metrics appropriate to your evaluation scope. Not every evaluation requires every metric. Match metrics to your system's maturity and the questions you need answered.

See the **Metric Selection Guide** below and [methodology.md](resources/methodology.md) for detailed metric definitions.

### Step 3. Design Test Protocol

Build test sets that cover your evaluation dimensions. Include single-hop factual queries, multi-hop reasoning queries, constraint satisfaction queries, temporal reasoning queries, comparative queries, and negative queries (questions the system should not answer).

See [methodology.md](resources/methodology.md) for baseline comparison approaches and statistical significance testing.

### Step 4. Test Reasoning Capabilities

Evaluate how well your system handles multi-step reasoning. Verify that each reasoning step is grounded in retrieved KG evidence. Check for error propagation where an incorrect intermediate step leads to wrong conclusions.

See [reasoning-patterns.md](resources/reasoning-patterns.md) for chain validation, pattern matching, hypothesis verification, and causal reasoning evaluation.

### Step 5. Measure Hallucination Rate

Quantify both intrinsic hallucination (contradicts retrieved evidence) and extrinsic hallucination (claims not supported by any retrieved source). Measure the KG grounding rate: what percentage of generated claims are traceable to knowledge graph entities and relations.

See [methodology.md](resources/methodology.md) for hallucination detection approaches and comparison protocols.

### Step 6. Compare Against Baselines

Run identical test sets against baseline systems: pure vector RAG, LLM-only (no retrieval), and alternative graph configurations. Use controlled ablation studies to isolate the contribution of each component.

See [methodology.md](resources/methodology.md) for baseline comparison and ablation study design.

### Step 7. Produce Evaluation Report

Compile findings into the structured output template below. Include metric values, baseline comparisons, identified weaknesses, and prioritized recommendations.

See [rubric_evaluation.json](resources/evaluators/rubric_evaluation.json) for the scoring rubric (minimum passing score: 3.0).

## Evaluation Dimensions

| Dimension | What It Measures | Key Metrics | Priority |
|---|---|---|---|
| KG Quality | Completeness and accuracy of the knowledge graph | Entity coverage, relation completeness, schema consistency | High |
| Retrieval Quality | Effectiveness of graph-based retrieval | Context recall (C-Rec), context precision, multi-hop coverage | High |
| Answer Correctness | Accuracy and completeness of generated answers | Factual accuracy, answer completeness, citation accuracy | Critical |
| Hallucination Rate | Frequency of unsupported or contradicted claims | Intrinsic hallucination rate, extrinsic hallucination rate, KG grounding rate | Critical |
| Reasoning Depth | Ability to perform multi-step reasoning correctly | Multi-hop accuracy, stepwise verification score, error propagation rate | Medium-High |

## Metric Selection Guide

Choose metrics based on your evaluation goals:

**Quick Health Check** (minimal effort):
- Answer correctness on a curated test set (20-50 questions)
- KG grounding rate (sample 20 responses)
- Single baseline comparison (pure vector RAG)

**Standard Evaluation** (recommended):
- All five dimensions with standardized test sets
- Context recall and context precision
- Multi-hop reasoning tests
- Hallucination rate measurement
- Two or more baseline comparisons

**Comprehensive Benchmark** (production readiness):
- Full metrics suite across all dimensions
- Statistical significance testing with confidence intervals
- Controlled ablation study
- Process-oriented reasoning evaluation (stepwise correctness)
- Automated evaluation pipeline for reproducibility

## Output Template

```markdown
# GraphRAG Evaluation Report

## 1. System Under Evaluation
- System name and version:
- Domain:
- KG size (entities/relations):
- Evaluation date:

## 2. Evaluation Scope
- Dimensions evaluated:
- Test set size and composition:
- Baseline systems:

## 3. KG Quality Results
- Entity coverage: ____%
- Relation completeness: ____%
- Schema consistency score: ____
- Notable gaps:

## 4. Retrieval Quality Results
- Context recall (C-Rec): ____
- Context precision: ____
- Multi-hop coverage: ____%
- Latency (p50/p95/p99): ____

## 5. Answer Correctness Results
- Factual accuracy: ____%
- Answer completeness: ____%
- Citation accuracy: ____%

## 6. Hallucination Analysis
- Intrinsic hallucination rate: ____%
- Extrinsic hallucination rate: ____%
- KG grounding rate: ____%
- Comparison with/without graph augmentation:

## 7. Reasoning Depth Results
- Single-hop accuracy: ____%
- Multi-hop accuracy: ____%
- Stepwise reasoning correctness: ____%
- Error propagation incidents: ____

## 8. Baseline Comparison
| Metric | GraphRAG | Pure Vector RAG | LLM Only |
|--------|----------|-----------------|----------|
| Answer correctness | | | |
| Hallucination rate | | | |
| Multi-hop accuracy | | | |

## 9. Statistical Significance
- Test used:
- Confidence level:
- Significant improvements:
- Non-significant differences:

## 10. Identified Weaknesses
1.
2.
3.

## 11. Recommendations
| Priority | Recommendation | Expected Impact | Effort |
|----------|---------------|-----------------|--------|
| | | | |

## 12. Rubric Score
- Metric Coverage: __ / 5
- Measurement Rigor: __ / 5
- Baseline Comparison: __ / 5
- Reasoning Depth: __ / 5
- Actionable Recommendations: __ / 5
- **Weighted Total: __ / 5.0** (minimum passing: 3.0)
```
