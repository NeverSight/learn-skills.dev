---
name: haystack
description: >-
  Build production search and NLP pipelines with Haystack. Pipeline DAG composition,
  document stores, retrievers, PromptBuilder (Jinja2), generators, evaluation, Hayhooks
  deployment. Use when building search pipelines or comparing NLP application frameworks.
  Do not use this skill for unrelated requests; route to the nearest named specialist.
license: MIT
metadata:
  author: Magnus Hedemark
  version: 1.1.0
  source: https://docs.haystack.deepset.ai
---

# Haystack Expert Skill

Haystack (by deepset) is a production-oriented framework for building search and NLP pipelines. Its core abstraction is the **Pipeline** — a directed acyclic graph of typed components with explicit connections. Unlike LangChain's LCEL (pipe operator) or LlamaIndex's query engines, Haystack pipelines are **declared upfront with add_component and connect**, giving validated, debuggable DAGs.

## Core Paradigm

```python
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.document_stores.in_memory import InMemoryDocumentStore

# Build a pipeline
document_store = InMemoryDocumentStore()
pipeline = Pipeline()
pipeline.add_component("embedder", SentenceTransformersTextEmbedder())
pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store))
pipeline.add_component("prompt_builder", PromptBuilder(template="Answer using: {{documents}}\n\nQuestion: {{question}}"))
pipeline.add_component("generator", OpenAIGenerator())

# Connect components
pipeline.connect("embedder.embedding", "retriever.query_embedding")
pipeline.connect("retriever.documents", "prompt_builder.documents")
pipeline.connect("prompt_builder", "generator")

# Run
result = pipeline.run({"embedder": {"text": "What is Haystack?"}, "prompt_builder": {"question": "What is Haystack?"}})
```

## Core Principles

1. **Pipelines are validated DAGs.** add_component + connect. Pipeline validation catches errors BEFORE execution — leverage this during development.
2. **Components are typed.** Each component has input/output slots. Connections must match types. This prevents runtime errors.
3. **PromptBuilder uses Jinja2.** Templates are Jinja2 strings, not f-strings. `{{documents}}`, `{{query}}`, `{{question}}` are variable placeholders.
4. **Indexing and query are separate pipelines.** One pipeline loads/cleans/embeds/writes documents. Another retrieves/generates answers. They share the DocumentStore.
5. **Evaluation is a pipeline too.** Add evaluator components to measure faithfulness, relevancy, or custom metrics.

## Where to Start

| You already have... | Start here |
|---|---|
| Nothing — exploring Haystack | Build a basic indexing + query pipeline |
| Documents to index | Build an indexing pipeline (converters, splitter, embedder, writer) |
| A search use case | Build a query pipeline (embedder, retriever, prompt, generator) |
| A production deployment | Add Hayhooks + evaluation pipeline |

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Build indexing pipeline | add_component -> connect -> run | `references/pipeline-design.md` |
| Build query pipeline | retriever -> prompt_builder -> generator | `references/pipeline-design.md` |
| Choose document store | InMemory (dev), Elasticsearch/Pinecone (prod) | `references/document-stores.md` |
| Embedding retrieval | SentenceTransformersTextEmbedder + EmbeddingRetriever | `references/retrievers.md` |
| Hybrid retrieval | BM25 + Embedding in parallel, DocumentJoiner | `references/retrievers.md` |
| Prompt templates | Jinja2 in PromptBuilder | `references/pipeline-design.md` |
| Evaluation | DeepEvalEvaluator, SASEvaluator | `references/evaluation.md` |
| Deploy | Hayhooks REST API | `references/deployment.md` |

## Framework Routing Guide

| Scenario | Reach for | Why |
|----------|-----------|-----|
| Search / NLP pipelines | **Haystack** | Pipeline DAG model is most mature for retrieval-heavy workloads |
| Documents to query / RAG | **LlamaIndex** | Data ingestion is the primary primitive |
| Chain/agent composition | **LangChain** | LCEL pipe operator for general chain building |
| Compiled prompt programs | **DSPy** | Auto-optimizes prompts against a metric |
| Role-based multi-agent | **CrewAI** | Higher-level agent abstraction |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Pipeline Design | Building indexing and query pipelines | `references/pipeline-design.md` |
| Document Stores | Store selection and configuration | `references/document-stores.md` |
| Retrievers | Embedding, BM25, hybrid retrieval | `references/retrievers.md` |
| Validation Audit | Research validation of all API claims | `references/validation-audit.md` |
| File Converters | Multi-format indexing, YAML serialization, component types | `references/file-converters.md` |
| Evaluation | Metrics, evaluators, pipeline evaluation | `references/evaluation.md` |
| Deployment | Hayhooks, containerization, production | `references/deployment.md` |
| FAQ & Troubleshooting | Common errors and fixes | `references/faq-and-troubleshooting.md` |

## Templates

| Template | When to use | File |
|----------|-------------|------|
| Indexing Pipeline | Load, split, embed, write to store | `templates/indexing-pipeline.py` |
| Query Pipeline | Retrieve, prompt, generate answer | `templates/query-pipeline.py` |
| Hybrid RAG | BM25 + embedding in parallel | `templates/hybrid-rag.py` |

## Troubleshooting

| Symptom | Likely cause | Fix | Reference |
|---------|-------------|-----|-----------|
| Pipeline run errors | Component connection mismatch | Check component input/output slot types | `references/pipeline-design.md` |
| No documents retrieved | Empty document store | Run indexing pipeline first | `references/pipeline-design.md` |
| Prompt not rendering | Wrong variable name in Jinja2 template | Check {{variables}} match pipeline input | `references/pipeline-design.md` |
| Slow retrieval | Full scan instead of ANN | Configure approximate nearest neighbor index | `references/retrievers.md` |
| Embedding mismatch | Different models for indexing vs query | Use same model in both pipelines | `references/retrievers.md` |
| Hayhooks not starting | Port conflict or missing config | Check port, run with --help for options | `references/deployment.md` |
