---
name: agno
description: "Build AI agents, multi-agent teams, and agentic workflows using the Agno framework. MANDATORY TRIGGERS: Agno, agno-agi, AgentOS, any mention of the Agno framework. Also trigger when the user wants to build AI agents with tools/memory/knowledge, create multi-agent systems, RAG pipelines, reasoning agents, agentic workflows, or deploy agents to production. Trigger even if the user just says 'build me an agent', 'create an AI assistant', or 'make a chatbot' — if Agno is anywhere in their stack or project dependencies. When in doubt about whether to use this skill for agent-building tasks, use it."
license: MIT
metadata:
  version: "1.2.0"
  author: Abhishek Sharma
  tags: ["agno", "ai-agents", "multi-agent", "agentos", "rag", "workflows", "mcp"]
---

# Agno Framework — Skill Router

Agno is an open-source framework for building, deploying, and managing multi-agent systems. This skill is organized into focused reference files. Read only what the current task requires.

## Reference Files

| Reference | File | Read When |
|-----------|------|-----------|
| **Agents** | `references/agents.md` | Creating agents, tools, structured output, storage, memory, knowledge, state, streaming |
| **Teams** | `references/teams.md` | Multi-agent coordination, team modes (coordinate, route, broadcast, tasks), delegation |
| **Workflows** | `references/workflows.md` | Orchestrating agents/teams/functions as repeatable pipelines with sequential, parallel, conditional, loop, and router patterns |
| **Workflow Patterns** | `references/workflow-patterns.md` | Full code examples for every workflow pattern (sequential, parallel, conditional, loop, router, mixed, background execution, conversational) |
| **Input / Output** | `references/input-output.md` | Structured input (Pydantic validation), structured output (typed responses), multimodal (images, audio, video, files), streaming, output/parser models, expected output |
| **Models** | `references/models.md` | Model providers (40+ supported), model-as-string syntax ("provider:model_id"), error handling & retries, response caching, multimodal compatibility matrix, OpenAI-compatible models (OpenAILike, OpenResponses) |
| **Database** | `references/database.md` | All storage backends (Postgres sync/async, MongoDB, Redis, Supabase, SQLite, DynamoDB, MySQL), chat history, session management, connection strings |
| **Memory** | `references/memory.md` | Automatic vs agentic memory, MemoryManager, MemoryTools, memory optimization, multi-user isolation, agents sharing memory, teams with memory, best practices |
| **Knowledge** | `references/knowledge.md` | RAG pipelines, vector databases (PgVector, Chroma, LanceDB, Pinecone, Qdrant, 20+ options), embedders, readers (PDF, CSV, web, YouTube, etc.), chunking strategies, search types (vector/keyword/hybrid), filtering, reranking, custom retrievers, contents DB |
| **Learning** | `references/learning.md` | Learning Machines, 6 learning stores (user profile, user memory, session context, entity memory, learned knowledge, decision log), learning modes (Always/Agentic/Propose), custom schemas, namespaces, curator maintenance |
| **Skills & Tools** | `references/agno-skills.md` | Agno Skills (SKILL.md packages, scripts, references, progressive loading), quick tool overview |
| **Tools (Deep Dive)** | `references/tools.md` | Comprehensive tools reference — creating tools, @tool decorator, custom Toolkits, hooks, exceptions, caching, RunContext, MCP, and all 120+ pre-built toolkits organized by category (search, data, web, dev, comms, media, productivity) |
| **Reasoning** | `references/reasoning.md` | Three reasoning approaches: Reasoning Models (GPT-5, DeepSeek-R1, Claude extended thinking), ReasoningTools (think/analyze), Reasoning Agents (reasoning=True), split reasoning+response models, KnowledgeTools, MemoryTools, WorkflowTools, streaming events |
| **Multimodal** | `references/multimodal.md` | Image input/generation (DALL-E, Gemini), audio input/output (transcription, speech, voice config), video analysis (Gemini), file/PDF processing, media classes (Image, Audio, Video, File), cross-modal pipelines, model compatibility |
| **Context & Sessions** | `references/context.md` | Sessions, chat history (3 patterns), session summaries, context engineering (system/user message building, few-shot), workflow sessions, persistence (database backends, schema) |
| **State Management** | `references/state.md` | Session state across agents/teams/workflows — basic state with tools, agentic state (auto), team shared state, workflow step state, multi-user isolation, overwrite vs merge, state hooks, cross-session search |
| **Context Management** | `references/context-mgmt.md` | System message construction, context enrichment flags, chat history controls, context compression (BETA), dependency injection, few-shot learning, prompt caching, token tracking, debug mode |
| **Guardrails** | `references/guardrails.md` | Input validation and safety — PII detection/masking, prompt injection defense, OpenAI content moderation, custom guardrails (BaseGuardrail), hooks integration, exceptions (InputCheckError, CheckTrigger), agent + team usage |
| **Human-in-the-Loop** | `references/hitl.md` | Human oversight of agent execution — user confirmation (approve/reject tools), user input (collect field values), dynamic user input (UserControlFlowTools, agent-driven), external tool execution (sandboxed), async/streaming, while-loop pattern |
| **Evals** | `references/evals.md` | Evaluation framework — accuracy (LLM-as-a-judge), performance (latency/memory), reliability (tool call verification), agent-as-judge (custom criteria scoring), AgentOS integration, database persistence |
| **Hooks** | `references/hooks.md` | Pre-hooks and post-hooks — execute custom logic before/after Agent/Team runs, input validation/transformation, output validation/transformation, @hook decorator, background execution, exceptions (InputCheckError, OutputCheckError, CheckTrigger) |
| **Tracing** | `references/tracing.md` | OpenTelemetry-based observability — setup_tracing(), traces & spans, agent/team/workflow tracing, batch processing, DB query functions (get_trace, get_traces, get_span, get_spans), AgentOS tracing, performance monitoring |
| **Run Cancellation** | `references/run-cancellation.md` | Cancel running agent/team/workflow executions — cancel_run(run_id), streaming cancellation events (RunEvent.run_cancelled, TeamRunEvent.run_cancelled, WorkflowRunEvent.workflow_cancelled), RunStatus.cancelled, API endpoints |
| **AgentOS** | `references/agentos.md` | Production runtime — AgentOS class, 50+ API endpoints, SSE streaming, control plane (os.agno.com), configuration (YAML/AgentOSConfig), security (Basic Auth, RBAC/JWT), background hooks, custom lifespan, Registry for visual builder |
| **Culture** | `references/culture.md` | Experimental shared knowledge layer — universal principles, best practices, 3 management modes (automatic, agentic, manual), CultureManager, CulturalKnowledge data model, seeding organizational standards |
| **Custom Logging** | `references/custom-logging.md` | Custom loggers — configure_agno_logging(), per-component loggers (agent/team/workflow), file logging, named loggers (agno, agno-team, agno-workflow convention) |
| **Observability** | `references/observability.md` | Third-party monitoring platforms — AgentOps, Arize Phoenix, Atla, LangDB, Langfuse, LangSmith, Langtrace, LangWatch, Maxim, OpenLIT, Traceloop, Weave (WandB), OpenInference instrumentation, OTLP export |
| **Integrations** | `references/integrations.md` | Platform integrations — Discord bot (DiscordClient, thread creation, media support), Memori (open-source memory layer, fact extraction, entity search) |
| **Migrations** | `references/migrations.md` | Database migrations (MigrationManager, AgentOS endpoints, upgrade/downgrade, v1→v2), Workflows 2.0 migration (class-based → step-based, state management, streaming) |
| **Deploy** | `references/deploy.md` | Deployment templates (Docker, Railway, AWS ECS), pre-built solutions (Dash, Scout, Gcode), apps (10 agent apps, team apps, workflow apps), interfaces (Slack, Discord, WhatsApp, Telegram, MCP, AG-UI) |
| **Database Providers** | `references/database-providers.md` | All 18 database backends — PostgreSQL/MySQL/SQLite (sync+async), MongoDB, Redis, DynamoDB, Firestore, SurrealDB, Neon, Supabase, SingleStore, GCS, JSON, In-Memory — classes, imports, connection strings, Docker commands |
| **Vector Store Providers** | `references/vector-store-providers.md` | All 14+ vector databases — PgVector, ChromaDB, LanceDB, Pinecone, Qdrant, Weaviate, Milvus, MongoDB Atlas, SingleStore, Cassandra, ClickHouse, Upstash, AstraDB — classes, imports, search types |
| **Embedder Providers** | `references/embedder-providers.md` | All 12+ embedding providers — OpenAI, Azure OpenAI, Google, Voyage, Cohere, Mistral, Ollama, HuggingFace, Together, Fireworks, SentenceTransformer, FastEmbed — classes, imports, default models |
| **FAQs** | `references/faqs.md` | Common troubleshooting — env vars setup, Workflow vs Team decision guide, structured outputs vs JSON mode, TPM rate limiting, model switching, AgentOS connection issues, Docker errors, JWT auth, TablePlus |

## Install Agno

```bash
uv pip install -U agno          # Core
uv pip install -U agno openai   # + OpenAI
uv pip install -U agno anthropic # + Anthropic
uv pip install -U 'agno[os]'   # + AgentOS runtime
```

## Install This Skill

```bash
# Via Smithery (any platform)
smithery install agno

# Manual — copy this folder to your platform's skill directory:
# Claude Code:   .claude/skills/agno/    or ~/.claude/skills/agno/
# Antigravity:   .agent/skills/agno/     or ~/.gemini/antigravity/skills/agno/
# Gemini CLI:    .gemini/skills/agno/    or ~/.gemini/skills/agno/
# Cursor:        .cursor/skills/agno/    or ~/.cursor/skills/agno/
# Codex:         .codex/skills/agno/     or ~/.codex/skills/agno/
# Windsurf:      .windsurf/skills/agno/  or ~/.codeium/windsurf/skills/agno/
# Trae:          .trae/skills/agno/      or ~/.trae/skills/agno/

# Agno native (load from code)
# from agno.skills import Skills, LocalSkills
# agent = Agent(skills=Skills(loaders=[LocalSkills("/path/to/agno-skill")]))
```

## Version Tracking

- **Skill version:** 1.2.0 | **Agno tracked:** 2.5.3 | **Snapshot:** 2026-02-21
- Version metadata: `VERSION.json`
- Update checker: `python scripts/check-updates.py` (checks PyPI, docs sitemap, stale files, integrity)
- Changelog: `CHANGELOG.md`

## Docs

- https://docs.agno.com/introduction
- https://docs.agno.com/examples/introduction (2000+ examples)
- https://github.com/agno-agi/agno
