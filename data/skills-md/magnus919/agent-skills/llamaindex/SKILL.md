---
name: llamaindex
description: >-
  Build LLM applications with the LlamaIndex framework. Use when working with LlamaIndex
  or comparing RAG and agent orchestration frameworks. Do not use this skill for unrelated
  requests; route to the nearest named specialist.
license: MIT
metadata:
  author: Magnus Hedemark
  version: 1.3.0
  source: https://github.com/run-llama/llama_index
---

# LlamaIndex Expert Skill

LlamaIndex is an MIT-licensed Python framework for building LLM applications over your data. In 2026, it has evolved from a RAG indexing library into an event-driven workflow framework with integrated production runtime (llama-deploy), agent orchestration (AgentWorkflow), knowledge graph construction (PropertyGraphIndex), and OpenTelemetry-native observability.

The framework is organized around seven core primitives: **Reader** (data loaders), **Document/Node** (chunked content model), **Index** (data structures over Nodes), **Retriever** (relevant Node selection), **Query Engine** (retriever + synthesis), **Agent** (LLM with tools), and **Workflow** (event-driven orchestration).

## Key Principles

> These principles govern every decision when building with LlamaIndex. Read them before proceeding to the reference guides.

1. **Decouple retrieval chunks from synthesis chunks.** The embedding representation that retrieves well differs from the context representation that generates well. Use `SentenceWindowNodeParser` + `MetadataReplacementNodePostProcessor` for this pattern.
2. **Rerank before you generate.** Hybrid retrieval + reranker is the minimum viable production RAG configuration.
3. **Agents are Workflows.** `FunctionAgent` and `AgentWorkflow` are pre-configured Workflows. Drop to raw `Workflow` when you need custom control flow.
4. **Graphs are not just vector stores.** `PropertyGraphIndex` adds structural path traversal that vector similarity cannot provide — combine both for maximum retrieval quality.
5. **Evaluate in the same process.** Span-attached evaluation preserves the connection between the output and the retrieval context that produced it.

## Where to Start

The pipeline has 9 phases from Ingest to Deploy. If you're joining mid-stream with existing work, find your entry point:

| You already have... | Start at phase | What to do |
|---|---|---|
| Nothing — blank project | **Ingest** | Set up data loading, then proceed through the full pipeline |
| Documents in a directory | **Chunk** | Choose a chunking strategy, build your index |
| A working vector index | **Retrieve** | Add hybrid search, reranking, metadata filters |
| An existing RAG pipeline to harden | **Deploy** | Add observability, llama-deploy, production debugging |
| A need to measure and improve quality | **Evaluate** | Set up evaluators, ParamTuner, span-attached scoring |
| Nothing — comparing frameworks | See Framework Routing Guide | Don't start the pipeline — pick the right tool first |

## Pipeline Mode

Different tasks need different levels of rigor. Match your scope to a mode:

| Mode | When | Phases to run | Skip |
|------|------|---------------|------|
| **Quick** | Single query, one source, exploration | Ingest → Chunk → Index → Retrieve | Reranking, metadata filters, observability, evaluation |
| **Full** | Production RAG, multiple sources, compliance | Ingest → Chunk → Index → Retrieve → Agent/Workflow → Deploy → Evaluate | Nothing — run all phases |
| **Evaluate** | Benchmarking, regression testing | Ingest → Chunk → Index → Evaluate | Retrieve, Agent, Workflow, Deploy (run offline) |
| **Graph** | Knowledge graph construction | Ingest → Chunk → Graph → Retrieve | Agent, Workflow, Deploy (query via graph index directly) |

Rule of thumb: if you're shipping to users, run Full mode. If you're exploring, run Quick. If you're measuring, run Evaluate.

## Quick Reference

| Phase | Task | Approach | Reference |
|-------|------|----------|-----------|
| Ingest | Load data | `SimpleDirectoryReader("./data").load_data()` | `references/architecture.md` |
| Chunk | Parse documents into nodes | `SentenceSplitter(chunk_size=1024)` | `references/rag-strategies.md` |
| Index | Build vector index | `VectorStoreIndex.from_documents(docs)` | `references/rag-strategies.md` |
| Retrieve | Hybrid search + rerank | `BM25Retriever` + `CohereRerank` | `references/rag-strategies.md` |
| Agent | Multi-agent orchestration | `AgentWorkflow(agents=[...])` | `references/agent-patterns.md` |
| Workflow | Event-driven pipeline | `class MyFlow(Workflow): @step` | `references/workflows.md` |
| Graph | Knowledge graph | `PropertyGraphIndex.from_documents(docs)` | `references/property-graph-index.md` |
| Evaluate | RAG evaluation | `FaithfulnessEvaluator().evaluate_response(...)` | `references/evaluation-observability.md` |
| Deploy | Production deployment | `deploy_workflow(workflow=MyFlow())` | `references/production-deployment.md` |

## When to Use This Skill

Load this skill any time you are:
- Building a RAG pipeline over enterprise or personal data
- Comparing LlamaIndex with LangChain, Haystack, or DSPy
- Designing multi-agent systems with handoff between specialist agents
- Deploying an LLM application to production with observability
- Constructing knowledge graphs from unstructured documents
- Debugging common LlamaIndex failures (retrieval miss, handoff bug, async issues)

## When NOT to Use LlamaIndex — Framework Routing Guide

This skill is part of a portfolio of framework skills. When deciding which framework fits, use this routing table:

| Scenario | Reach for | Why |
|----------|-----------|-----|
| I have documents I need to query | **LlamaIndex** | Data ingestion, hybrid retrieval, reranking, and knowledge graphs are first-class primitives |
| I have agents I need to orchestrate | **LangGraph** | State-machine semantics, time-travel debugging, and human-in-the-loop pauses are the core design |
| I have a tool I need to wrap as an agent | **PydanticAI** | Type-safe agent definitions with dependency injection, minimal abstraction over LLM calls |
| Data-heavy RAG over PDFs, SQL, Slack, 200+ sources | **LlamaIndex** | LlamaHub connectors, LlamaParse for documents, hybrid retrieval out of the box |
| Complex multi-agent state machines with checkpoints | **LangGraph** | Graph topology control — supervisor, subgraphs, hierarchical teams, built-in checkpointer |
| Agent-centric app where type safety matters more than data pipelines | **PydanticAI** | Agents as Pydantic models, DI, structured outputs — the data layer is your code |
| Document parsing quality matters (tables, charts, handwriting) | **LlamaIndex** | LlamaParse is purpose-built for this |
| Production NLP search pipelines | **Haystack** | Pipeline composition model is more mature for search-specific workloads |
| Optimization-driven prompt programming | **DSPy** | Compiled prompt programs, not retrieval pipelines |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| Core Architecture | Understanding the 7 primitives, Settings, data flow | `references/architecture.md` |
| RAG Strategies | Building RAG pipelines from basic to advanced | `references/rag-strategies.md` |
| Agent Patterns | Multi-agent orchestration with AgentWorkflow | `references/agent-patterns.md` |
| Workflows | Event-driven step composition and durable execution | `references/workflows.md` |
| Production & Deployment | llama-deploy, debugging, failure modes | `references/production-deployment.md` |
| Property Graph Index | Knowledge graph construction and hybrid retrieval | `references/property-graph-index.md` |
| Evaluation & Observability | Metrics, tracing, span-attached scoring | `references/evaluation-observability.md` |
| Integration Ecosystem | Vector stores, LlamaHub, LlamaParse, ecosystem | `references/integration-ecosystem.md` |
| FAQ & Troubleshooting | Common errors and their fixes | `references/faq-and-troubleshooting.md` |
| Worked RAG Example | Complete end-to-end pipeline from ingest to deploy | `references/example-rag-pipeline.md` |
| Evaluation Workflow | ParamTuner, evaluators, batch scoring, best practices | `references/evaluation-workflow.md` |

## Template Files

| Template | When to use | File |
|----------|-------------|------|
| Basic RAG | Single-source query, getting started | `templates/basic-rag.py` |
| Agentic RAG | Multi-source data with agent routing | `templates/agentic-rag.py` |
| Custom Workflow | Custom control flow, branching logic | `templates/custom-workflow.py` |
| Production Deploy | Wrapping a workflow as a microservice | `templates/production-deploy.py` |

## Scripts

| Script | Purpose | File |
|--------|---------|------|
| check-setup | Verify LlamaIndex installation and configuration | `scripts/check-setup.py` |

## Troubleshooting — Structured Recovery Guide

When something goes wrong, find your symptom and follow the recovery path:

### Retrieval & Answer Quality

| Symptom | Likely cause | Immediate fix | Permanent fix | Reference |
|---------|-------------|---------------|---------------|-----------|
| Answers are poor or hallucinated | No reranker on hybrid retrieval | Add `CohereRerank(top_n=5)` as `node_postprocessor` | Reranking is mandatory for any production RAG | `references/rag-strategies.md` |
| Retrieval misses obvious content | Default chunking breaks semantics | Switch to `SemanticSplitterNodeParser(breakpoint_percentile_threshold=95)` | Tune chunk size with ParamTuner | `references/rag-strategies.md` |
| Wrong tenant's data returned | Missing metadata filters | Add `MetadataFilters(filters=[ExactMatchFilter(key="tenant_id", ...)])` | Always wire metadata filters at retriever level | `references/rag-strategies.md` |
| Only one type of query works well | Single retrieval strategy | Combine BM25 + vector via hybrid retriever | Add RouterQueryEngine for query-type routing | `references/rag-strategies.md` |

### Agent & Workflow Failures

| Symptom | Likely cause | Immediate fix | Permanent fix | Reference |
|---------|-------------|---------------|---------------|-----------|
| Agent waits silently after handoff | AgentWorkflow handoff bug | Extend `FunctionAgent.take_step` to re-locate last user message | Apply the handoff fix on all production agents | `references/agent-patterns.md` |
| Workflow doesn't run | Forgot `await` | Add `await` before `w.run(...)` and all step calls | All step methods are async coroutines | `references/workflows.md` |
| Step executes but result is lost | State not persisted | Use `ctx.store.edit_state()` for shared state | Only `ctx.store` survives across steps | `references/workflows.md` |
| Crash loses all progress | No checkpoint snapshots | Add `Context.to_dict()` save on step completion | Durable workflows need explicit checkpointing | `references/workflows.md` |

### Deployment & Observability

| Symptom | Likely cause | Immediate fix | Permanent fix | Reference |
|---------|-------------|---------------|---------------|-----------|
| llama-deploy deployed but requests time out | Redis not running | Start `redis-server` | Redis is mandatory — control plane won't route without it | `references/production-deployment.md` |
| Spans missing in observability UI | Instrumentation called too late | Move `instrument()` call before workflow instantiation | Always instrument before creating any Workflow object | `references/production-deployment.md` |
| Wrong data returned (cross-tenant) | Missing metadata filters | Add tenant filter to all retrievers | Filter at retriever level, not in post-processing | `references/production-deployment.md` |

### Recovery Workflow

For any failure, follow this cycle:
1. **Identify the symptom** from the tables above
2. **Apply the immediate fix** — this gets you running
3. **Implement the permanent fix** — this prevents recurrence
4. **Verify with evaluation** — run `FaithfulnessEvaluator` on a held-out query set
5. **Document the fix** — add the root cause to `references/faq-and-troubleshooting.md`
