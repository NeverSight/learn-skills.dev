---
name: ag2-overview
description: Map of AG2 capabilities and which sibling skill to reach for. Load first when the user mentions building with AG2 (ag2) but the specific feature isn't yet clear — agents, tools, model config, delegation, memory, observers, structured output, HITL, AG-UI, MCP server hosting, A2A protocol, realtime voice, telemetry, testing, or evaluation.
license: Apache-2.0
---

# AG2 — capability map

AG2 (`ag2`) is an async, protocol-driven agent framework. The full reference docs live under `website/docs/user-guide/`. This skill is the index of sibling skills that cover the common build paths.

## When to use

Read this file first when a request mentions "AG2", "ag2", or building agents in this repo and you don't yet know which feature is needed. Use the table below to pick the right specialised skill, then load that skill's `SKILL.md` for the recipe.

## Before you start

Anything you build with AG2 needs three things in place. Get these right once and the rest of the skills run cleanly:

1. **Install the right provider extra** — `pip install "ag2[openai]"`, `ag2[anthropic]`, `ag2[gemini]`, etc. The `*Config` class will raise `ImportError: ... requires optional dependencies` without it. **Run the install before delivering code.** If you cannot run commands, state the exact `pip install` command. This is a required step.
2. **Set the matching API key** — `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` (or `GOOGLE_API_KEY`). Loading from a project-root `.env` via `from dotenv import load_dotenv; load_dotenv()` is the common pattern.
3. **Sanity-check the install** — `python -c "import sys, ag2; from importlib.metadata import version; print(sys.executable, version('ag2'))"`. If you have multiple Python environments, this confirms which `ag2` your script will actually import.

Full per-provider table (install + env var + config class) lives in `ag2-quickstart` → "Prerequisites".

## Pick the right skill

| User intent | Skill | What it covers |
|---|---|---|
| Build an `Agent` from scratch, pick a model | `ag2-quickstart` | `Agent`, `ModelConfig`, `ask()` / `reply.ask()` chaining, providers, env vars |
| Give the Agent a custom Python tool | `ag2-add-custom-tool` | `@tool`, sync/async, `ToolResult`, `Context`, `Inject`, `Variable`, `Depends` |
| Use shipped tools (web search, code exec, MCP, etc.) | `ag2-use-builtin-tools` | `WebSearchTool`, `WebFetchTool`, `CodeExecutionTool`, `MCPServerTool`, `ImageGenerationTool`, `MemoryTool`, `FilesystemToolkit`, `DuckDuckSearchTool`, `ExaToolkit`, `TavilySearchTool` |
| Run shell commands from an agent | `ag2-shell-tool` | `SandboxShellTool` + `LocalEnvironment` (any provider), provider-side `ShellTool` (OpenAI Responses), sandboxing (`allowed`/`blocked`/`ignore`/`readonly`) |
| Get typed Pydantic / dataclass output | `ag2-structured-output` | `response_schema=`, `ResponseSchema`, `@response_schema`, `PromptedSchema`, `reply.content()`, retries |
| Multi-agent: parallel subtasks or named delegates | `ag2-subagent-delegation` | `tasks=TaskConfig()`, `run_subtasks(parallel=True)`, `Agent.as_tool()`, `persistent_stream` |
| Pause for human input or gate a tool with approval | `ag2-hitl` | `context.input()`, `hitl_hook`, `approval_required()` middleware |
| Logging, retry, history-trim, custom interception | `ag2-middleware` | `BaseMiddleware`, `LoggingMiddleware`, `RetryMiddleware`, `HistoryLimiter`, `TokenLimiter`, tool middleware |
| Test agents and tools | `ag2-testing` | `TestConfig`, mocking LLM responses, simulating `ToolCallEvent` |
| Evaluate / benchmark an agent offline, CI gate, scorers | `ag2-evaluation` | `Suite`, `run_agent`, `final_answer_matches` / `tool_called` / `agent_judge`, `@scorer`, `RunResult`, `TestConfig`, `evaluate_traces`, `diff().regressions` |
| Compare models / prompts — leaderboard or head-to-head | `ag2-eval-comparison` | `run_variants` (`Variants({name: Agent}, axis=...)`), `run_pairwise` + `pairwise_judge` (win-rate, Wilson CI, flips, κ), `human_pairwise` |
| Persistent memory across runs, history compaction, assembly | `ag2-knowledge-and-memory` | `KnowledgeStore`, `KnowledgeConfig`, `WorkingMemoryAggregate`, `AssemblyPolicy`, `SlidingWindowPolicy`, `TokenBudgetPolicy`, `TailWindowCompact`, `SummarizeCompact` |
| Observability, alerts, halts | `ag2-observers-and-alerts` | `BaseObserver`, `TokenMonitor`, `LoopDetector`, `EventWatch`, `CadenceWatch`, `AlertPolicy`, `HaltEvent` |
| Send images / audio / video / PDFs in | `ag2-multimodal-input` | `ImageInput`, `AudioInput`, `VideoInput`, `DocumentInput`, `FilesAPI` |
| Web frontend via the AG-UI protocol | `ag2-ag-ui` | `AGUIStream`, FastAPI mount, CopilotKit |
| Serve an agent as an MCP server (server side) | `ag2-mcp` | `MCPServer`, stdio / HTTP, prompts, resources, `SessionConfig`, `AskContext` |
| Expose an agent over the A2A protocol | `ag2-a2a` | `A2AServer`, `build_jsonrpc` / `build_rest` / `build_grpc`, `AgentCard`, `A2AConfig` (consume remote) |
| Realtime voice / live audio (talking agent, STT, TTS) | `ag2-live` | `LiveAgent`, `GeminiRealTimeConfig` / `OpenAIRealTimeConfig`, `SoundDeviceRecorder` / `Player`, `OpenAITranscriber`, `TTSObserver` |
| OpenTelemetry traces / metrics | `ag2-telemetry` | `TelemetryMiddleware`, GenAI semconv attributes, content capture |

## Multi-agent networks

Whenever two or more agents need to interact, load **`ag2-network-quickstart`** first — the network is the standard multi-agent pattern in AG2. It covers the `Hub` setup and the two 2-party channel adapters (`consulting` for strict 1Q1R and `conversation` for free-form). After the quickstart, route to the right deep-dive:

| User intent | Skill | What it covers |
|---|---|---|
| N-party round-robin / fixed turn order | `ag2-network-discussion` | `discussion` adapter, `ORDERING_ROUND_ROBIN` knob, `can_send` probe pattern, view-window sizing |
| Declarative orchestration / `TransitionGraph` / GroupChat migration | `ag2-network-workflow` | `workflow` adapter, `TransitionGraph.sequence` / `.round_robin`, `Handoff`, `ToolCalled`, `ContextEquals`, `context_vars`, 8 cookbook patterns, classic-`GroupChat` migration |
| Rate limits, access policy, expectations, audit, capability tracking | `ag2-network-governance` | `Rule` (`AccessBlock` / `LimitsBlock` / `RateBlock` / `InboxBlock`), `Expectation`s, audit log + `AUDIT_KIND_*`, task observation, `Resume.observed` |
| Custom envelope handlers, view policies, peer discovery, the LLM-facing network tools | `ag2-network-tools-and-views` | adapter-owned `say` + the five `NetworkPlugin` tools (`delegate` / `peers` / `channels` / `tasks` / `context`), `agent_client.on_envelope`, `ViewPolicy` (`FullTranscript` / `WindowedSummary` / `NamedWindowedSummary`), `skill_md` peer discovery, full `Envelope` / `EV_*` reference |

**Not a network task:** if the user has *one* agent recursively spawning its own sub-tasks (via `run_subtask` / `run_subtasks(parallel=True)`) or calling another agent as a lightweight tool, use **`ag2-subagent-delegation`** — no hub, no registry, no channels. The network is for *distinct, registered* agents collaborating through a shared hub.
