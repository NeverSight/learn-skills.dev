---
name: langchain
description: >-
  Build LLM applications with LangChain. Use when working with LangChain or comparing LLM
  application frameworks. Do not use this skill for unrelated requests; route to the
  nearest named specialist.
license: MIT
metadata:
  author: Magnus Hedemark
  version: 1.1.0
  source: https://github.com/langchain-ai/langchain
---

# LangChain Expert Skill

LangChain is an MIT-licensed Python framework for building LLM-powered applications. Since v1.0 (October 2025), it provides a layered architecture: high-level chain composition via LCEL (LangChain Expression Language), agent creation via `create_agent` (running on the LangGraph runtime underneath), and production observability via LangSmith. With 1000+ integrations and 100K+ GitHub stars, it is the most widely adopted LLM orchestration framework.

**Key v1.0 change:** All new LangChain agents run on the LangGraph runtime. AgentExecutor is in maintenance mode until December 2026. Use `create_agent` for new agents. Drop to LangGraph directly when you need full state-machine control.

> **⚠️ CRITICAL: Do NOT use AgentExecutor for new code.** It is in maintenance mode until December 2026. Use `create_agent(model, tools, prompt)` instead — it generates a LangGraph state machine with streaming, persistence, and observability out of the box.

## Core Principles

> These principles govern every decision when building with LangChain. Read them before proceeding to the reference guides.

1. **LCEL is the composition primitive.** The pipe operator (`|`) chains Runnables. Every component — prompt, model, parser, retriever — implements the Runnable interface. Build everything in LCEL.
2. **Agents run on LangGraph.** Since v1.0, `create_agent` generates a LangGraph state machine underneath. You get streaming, persistence, and observability without writing graph code. Drop to LangGraph when you need branching, cycles, or human-in-the-loop.
3. **RAG is a chain, not a framework.** `retriever | prompt | model | parser` is the canonical RAG pattern. Document loaders, splitters, and vector stores are all interchangeable components.
4. **LangSmith is production observability.** Enable tracing at startup. 89% of production teams use observability — without it, debugging agent behavior is guesswork.
5. **The ecosystem is the moat.** 1000+ integrations mean model providers, vector stores, and tools are swappable with one line. Build against the interface, not the implementation.

## Where to Start

| You already have... | Start here |
|---|---|
| Nothing — blank project | Install LangChain, build a basic LCEL chain |
| Documents to query | Build a RAG chain (load, split, embed, retrieve, generate) |
| A need for agentic behavior | Use `create_agent` with tools |
| Existing AgentExecutor code | Migrate to `create_agent` — see `references/agent-patterns.md` |
| A production deployment | Add LangSmith tracing + LangServe deployment |
| Comparing frameworks | See the Framework Routing Guide |

## Pipeline Mode

| Mode | When | Phases to run | Skip |
|------|------|---------------|------|
| **Quick** | Single chain, exploration | prompt → model → parser | Retrieval, agents, production hardening |
| **RAG** | Document Q&A | load → split → embed → retrieve → generate | Agent orchestration, deployment |
| **Agent** | Tool-using agents | create_agent + tools + LangGraph runtime | If simple chain suffices |
| **Production** | Shipping to users | RAG/Agent + LangSmith + LangServe | Nothing |

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Basic chain | `prompt \| model \| parser` | `references/lcel-reference.md` |
| RAG pipeline | `retriever \| prompt \| model \| parser` | `references/rag-strategies.md` |
| Create agent | `create_agent(model, tools, prompt)` | `references/agent-patterns.md` |
| Tool definition | `@tool` decorator | `references/agent-patterns.md` |
| Multi-agent | LangGraph supervisor pattern | `references/agent-patterns.md` |
| Observability | Set LANGCHAIN_TRACING_V2=true | `references/production-deployment.md` |
| Deployment | LangServe or LangSmith Deployment | `references/production-deployment.md` |
| Vector store | One-line swap (Chroma, Pinecone, pgvector) | `references/integration-ecosystem.md` |

## When to Use This Skill

Load this skill any time you are:
- Building LCEL chains for LLM-powered applications
- Implementing RAG pipelines over enterprise or personal data
- Creating agents with tool-calling and multi-step reasoning
- Deploying LLM applications to production with observability
- Comparing LangChain with LlamaIndex, Haystack, or raw API calls

## Framework Routing Guide

This skill is part of a portfolio of framework skills. When deciding which fits:

| Scenario | Reach for | Why |
|----------|-----------|-----|
| I have chains to compose | **LangChain** | LCEL is the cleanest pipe-based composition model |
| I have documents to query | **LlamaIndex** | Data ingestion and retrieval are first-class primitives |
| I have agents to orchestrate | **LangGraph** | State-machine semantics, subgraphs, human-in-the-loop |
| I have a tool to wrap as an agent | **PydanticAI** | Type-safe agent definitions with dependency injection |
| I have search pipelines | **Haystack** | Pipeline model is more mature for search workloads |
| Fast prototype of any kind | **LangChain** | Fastest path from zero to working chain |

## Reference Files

| Reference | Load when | File |
|-----------|-----------|------|
| LCEL Reference | Building chains with the pipe operator | `references/lcel-reference.md` |
| Architecture | Understanding package structure, Runnable, v1.0 | `references/architecture.md` |
| RAG Strategies | Building RAG pipelines | `references/rag-strategies.md` |
| Agent Patterns | Creating agents with tools and multi-agent | `references/agent-patterns.md` |
| Production & Deployment | LangServe, LangSmith, deployment | `references/production-deployment.md` |
| Integration Ecosystem | Model providers, vector stores, tools | `references/integration-ecosystem.md` |
| FAQ & Troubleshooting | Common errors and fixes | `references/faq-and-troubleshooting.md` |
| Callbacks System | Custom logging, monitoring, agent auditing | `references/callbacks.md` |
| Validation Audit | Research validation of all API claims | `references/validation-audit.md` |

## Template Files

| Template | When to use | File |
|----------|-------------|------|
| Basic Chain | Single prompt→model→parser chain | `templates/basic-chain.py` |
| RAG Pipeline | Document Q&A with retrieval | `templates/rag-pipeline.py` |
| Agent with Tools | Tool-using agent with LangGraph runtime | `templates/agent-with-tools.py` |
| Production Deploy | LangServe deployment with LangSmith | `templates/production-deploy.py` |

## Scripts

| Script | Purpose | File |
|--------|---------|------|
| check-setup | Verify LangChain installation | `scripts/check-setup.py` |

## Troubleshooting Guide

| Symptom | Likely cause | Fix | Reference |
|---------|-------------|-----|-----------|
| Chain returns nothing | Output parser not connected | Add `.pipe(StrOutputParser())` or equivalent | `references/lcel-reference.md` |
| Agent not calling tools | Tool schema mismatch | Check tool has docstring and type hints | `references/agent-patterns.md` |
| LangSmith traces missing | LANGCHAIN_TRACING_V2 not set | Set env var before any chain execution | `references/production-deployment.md` |
| Deprecation warning | Using AgentExecutor | Migrate to `create_agent` (LangGraph runtime) | `references/agent-patterns.md` |
| Model not found | Integration package missing | Install `langchain-openai`, `langchain-anthropic`, etc. | `references/integration-ecosystem.md` |
| Streaming not working | LCEL chain not streaming-native | Ensure all components implement `stream()` | `references/lcel-reference.md` |
| Vector store connection fails | Wrong credentials or missing package | Install `langchain-community` + provider package | `references/integration-ecosystem.md` |

## When NOT to Use LangChain

- Single-model, single-prompt application — raw API calls are simpler and more debuggable
- Maximum transparency needed — LangGraph (which LangChain uses underneath) provides more visibility
- Pure multi-agent state machines — LangGraph directly is the correct tool, not the high-level API
- Stateless microservice with no LLM orchestration — LangChain adds overhead without benefit
