---
name: check-crewai-api
description: "Current crewai 1.15.x API versus the 0.x API that coding assistants remember: imports, Agent/Task/Crew parameters and defaults, kickoff variants, CrewOutput fields, LLM model strings and provider extras, structured output (output_pydantic, response_model, response_format), guardrails, unified Memory, knowledge embedders, the `crewai create crew` wizard vs --classic, reset-memories flags, and removed features. Use when writing, reviewing, or debugging any crewai code, before trusting remembered crewai syntax, or when a user pastes errors like `cannot import name 'BaseTool' from 'crewai_tools'`, `cannot import name 'persist'`, `ShortTermMemory`, `Anthropic native provider not available`, `LiteLLM fallback package is not installed`, `got an unexpected keyword argument 'response_format'`, `OPENAI_API_KEY is required`, `If return type is annotated, it must be Tuple[bool, Any]`, or `result.pydantic is None`."
---

# Check CrewAI API

Load this before writing or reviewing crewai code: it maps what you probably remember to what crewai 1.15.x actually accepts.

Verified against crewai 1.15.22 and 1.15.23 on 2026-10-01.
Live-tested with real LLMs on 2026-10-01.
Run `crewai version` first; if the major/minor differs from 1.15, re-verify version-sensitive rows with the `ask-docs` skill before trusting them.

---

## 1. Three rules before you write anything

1. **Unknown keyword arguments are silently ignored.** `Agent`, `Task` and `Crew` accept and drop parameters that do not exist. `Crew(memory_config={...})` and `Task(response_format=Model)` construct fine and do nothing. A stale parameter name never raises, so check it exists:

   ```python
   from crewai import Agent, Crew, Task

   assert "response_model" in Task.model_fields      # real field
   assert "response_format" not in Task.model_fields  # silently dropped if passed
   assert "memory_config" not in Crew.model_fields    # silently dropped if passed
   print(sorted(Agent.model_fields)[:5])
   ```

2. **The installed source wins over any doc, tutorial, or memory.** That includes the `AGENTS.md` that `crewai create` writes into new projects. When a row below matters, check the installed signature (see [verify-installed-api.md](references/verify-installed-api.md)).
3. **Assert on structured output at the boundary.** Several mistakes below fail quietly with `out.pydantic is None` while the run reports success.

---

## 2. Imports

| You probably wrote | Current 1.15.x form | What the wrong form does |
|---|---|---|
| `from crewai_tools import BaseTool, tool` | `from crewai.tools import BaseTool, tool` | `ImportError: cannot import name 'BaseTool' from 'crewai_tools'` |
| `from crewai.flow.flow import Flow, start, listen, persist` | `from crewai.flow import Flow, start, listen, router, or_, and_, persist` | `ImportError: cannot import name 'persist'` |
| `from crewai.task import ConditionalTask` | `from crewai.tasks.conditional_task import ConditionalTask` | `ImportError` |
| `from crewai.memory import ShortTermMemory, LongTermMemory, EntityMemory` | `from crewai import Memory` | `ImportError` (the classes are gone) |
| `from crewai.utilities.events import crewai_event_bus` | `from crewai.events import BaseEventListener, crewai_event_bus` | `ModuleNotFoundError: No module named 'crewai.utilities.events'` |
| `from crewai_tools import CodeInterpreterTool` | No replacement in crewai - use a sandbox tool or service | `ImportError` (removed) |

The current top-level and project imports:

```python
from crewai import Agent, BaseLLM, Crew, CrewOutput, Flow, LLM, Memory, Process, Task, TaskOutput
from crewai.project import CrewBase, after_kickoff, agent, before_kickoff, crew, llm, task, tool
from crewai.tools import BaseTool, tool
from crewai.flow import Flow, and_, listen, or_, persist, router, start
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.mcp import MCPServerHTTP, MCPServerSSE, MCPServerStdio
from crewai.events import BaseEventListener, crewai_event_bus
```

---

## 3. Agent, Task, Crew parameters and defaults

| Parameter | Current value | Note |
|---|---|---|
| `Task.expected_output` | **required** | `Task(description=...)` alone raises `ValidationError ... expected_output Field required` |
| `Agent.max_iter` | `25` | Do not assume 15 or 20 |
| `Agent.llm` | `None` -> resolved at construction | From env `MODEL`, then `MODEL_NAME`, then `OPENAI_MODEL_NAME`, else `gpt-4.1-mini` |
| `Agent.cache` | `True` | Only *permits* caching; it does not turn it on |
| `Crew.cache` | `False` | Tool-result caching is opt-in: set `Crew(cache=True)` |
| `Crew.memory` | `False` | |
| `Crew.process` | `Process.sequential` | Only `sequential` and `hierarchical` exist |
| `Task.guardrail_max_retries` | `3` | `max_retries` is deprecated (DeprecationWarning) |

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `Process.consensual` | `Process.sequential` or `Process.hierarchical` | `AttributeError` |
| `Crew(process=Process.hierarchical, ...)` with no manager | add `manager_llm="openai/gpt-4.1-mini"` or `manager_agent=...` | `ValidationError: Attribute manager_llm or manager_agent is required` |
| `Crew(memory=True, memory_config={...})` | `Crew(memory=Memory(...))` | `memory_config` is silently ignored |
| `Agent(allow_code_execution=True)` / `code_execution_mode="unsafe"` | Remove; use a sandbox tool | Deprecated no-ops; `allow_code_execution=True` emits a `DeprecationWarning` |
| `Crew(function_calling_llm=...)` | Remove, or set `llm` per agent | Deprecated, `DeprecationWarning` |
| Two `async_execution=True` tasks with the same `agent` | One agent per concurrent async task | `RuntimeError: Executor is already running. Cannot invoke the same executor instance concurrently.` |

```python
from crewai import Agent, Crew, Process, Task

researcher = Agent(
    role="Researcher",
    goal="Find facts about {topic}",
    backstory="A careful researcher.",
    llm="openai/gpt-4.1-mini",
)
research = Task(
    description="List three facts about {topic}.",
    expected_output="Three bullet points.",
    agent=researcher,
)
crew = Crew(agents=[researcher], tasks=[research], process=Process.sequential, cache=True)
out = crew.kickoff(inputs={"topic": "honey bees"})
print(out.raw)
```

---

## 4. Running a crew and reading the result

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `crew.kickoff("honey bees")` | `crew.kickoff(inputs={"topic": "honey bees"})` | `TypeError: inputs must be a dict or Mapping, got str` |
| `await crew.kickoff_async(...)` for native async | `await crew.akickoff(...)` | Works, but `kickoff_async` runs the sync `kickoff` in a thread (`asyncio.to_thread`) |
| `result.output` / `result.final_output` / `result.result` | `result.raw` | `AttributeError: 'CrewOutput' object has no attribute ...` |
| `crew.kickoff(...)` then `crew.kickoff_for_each(...)` on the same `Crew` | Build a fresh `Crew` for `kickoff_for_each` (or call it before any `kickoff`) | No error, but every run reuses the first kickoff's inputs: the per-run copies keep the already-interpolated task text |
| `Agent(mcps=["https://..."])` in a crew run with `await crew.akickoff()` | `mcps=[MCPServerHTTP(url="https://...")]` (from `crewai.mcp`) | No error, but the agent gets **zero** MCP tools: string refs resolve with `asyncio.run()`, which fails inside a running event loop (see connect-tools-and-mcp) |

`CrewOutput` fields: `raw`, `pydantic`, `json_dict`, `tasks_output` (a list of `TaskOutput`), `token_usage`. `out["field"]` reads from `pydantic`/`json_dict`. `kickoff_for_each(inputs=[...])` returns a list of `CrewOutput`.

`token_usage` is summed over each agent's `LLM` object for that object's whole lifetime, not per run. One `LLM(...)` instance shared by two agents counts every call twice, and one reused across crews carries the earlier crews' tokens (verified with `anthropic/claude-haiku-4-5`: a second one-call crew on the same `LLM` reported 148 tokens and 2 requests, a fresh `LLM` 73 and 1). For per-run cost, give each crew its own `LLM` objects, or count `LLMCallCompletedEvent`s (`event.usage`).

```python
import asyncio

from crewai import Agent, Crew, Task



def make_crew() -> Crew:
    writer = Agent(role="Writer", goal="Write", backstory="Writes short text.", llm="openai/gpt-4.1-mini")
    task = Task(description="One line on {topic}.", expected_output="One line.", agent=writer)
    return Crew(agents=[writer], tasks=[task])


out = make_crew().kickoff(inputs={"topic": "bees"})
print(out.raw, out.token_usage.total_tokens, [t.raw for t in out.tasks_output])

many = make_crew().kickoff_for_each(inputs=[{"topic": "bees"}, {"topic": "ants"}])
print([o.raw for o in many])


async def main():
    return await make_crew().akickoff(inputs={"topic": "wasps"})

print(asyncio.run(main()).raw)
```

---

## 5. LLMs, model strings, and provider extras

LiteLLM is no longer a dependency. `LLM(model=...)` is a factory that returns a native provider class; only the OpenAI SDK ships with core crewai.

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `llm="anthropic/claude-sonnet-4-5"` with plain `crewai` installed | `uv add "crewai[anthropic]"`, then the same string | `ImportError: Anthropic native provider not available, to install: uv add "crewai[anthropic]"` |
| `llm="gemini/gemini-2.5-flash"` with plain `crewai` | `uv add "crewai[google-genai]"` | `ImportError: Google Gen AI native provider not available` |
| `llm="groq/llama-3.3-70b-versatile"` (or `mistral/...`, any non-native provider) | `uv add "crewai[litellm]"` | `ImportError: Unable to initialize LLM with model '...'. The model did not match any supported native provider (...), and the LiteLLM fallback package is not installed.` |
| No `llm=` and assuming `gpt-4` | Default is `gpt-4.1-mini`; set `MODEL=...` or `llm=` | |
| `llm.call(messages, response_format=Model)` | `llm.call(messages, response_model=Model)` | `TypeError: ... unexpected keyword argument 'response_format'. Did you mean 'response_model'?` |
| Custom `BaseLLM.call(self, messages, tools=None, callbacks=None, available_functions=None)` | Also accept `from_task=None, from_agent=None, response_model=None` (or `**kwargs`) | `TypeError: call() got an unexpected keyword argument 'from_task'` at kickoff |

Native providers: openai, anthropic/claude, azure, google/gemini, bedrock/aws, openrouter, deepseek, ollama, hosted_vllm, cerebras, dashscope, snowflake. Extras: `crewai[anthropic]`, `crewai[google-genai]`, `crewai[bedrock]`, `crewai[azure-ai-inference]`, `crewai[litellm]`. Construction never checks the key; kickoff does (`ValueError: OPENAI_API_KEY is required`, or `ANTHROPIC_API_KEY is required`; a wrong key gets the provider's `AuthenticationError ... 401`). The `crewai create` scaffolds never add a provider extra, even with `--provider anthropic/...`: run `uv add "crewai[anthropic]"` yourself.

```python
from crewai import LLM

gpt = LLM(model="openai/gpt-4.1-mini", temperature=0.2)  # core install
local = LLM(model="ollama/llama3")                        # core install, OpenAI-compatible route
claude = LLM(model="anthropic/claude-sonnet-4-5")         # needs: uv add "crewai[anthropic]"
print(type(gpt).__name__, type(local).__name__, type(claude).__name__)
```

A custom LLM subclasses `BaseLLM` and implements `call` with the full signature. If `call` forwards `messages` to a provider SDK, send only each message's `role` and `content`: crewai adds a `cache_breakpoint: True` key to some messages, and the Anthropic API rejects it with `400 ... messages.0.cache_breakpoint: Extra inputs are not permitted`.

```python
from typing import Any

from crewai import Agent, BaseLLM, Crew, Task


class EchoLLM(BaseLLM):
    def call(self, messages, tools=None, callbacks=None, available_functions=None,
             from_task=None, from_agent=None, response_model=None, **kwargs: Any) -> str:
        return "echo: " + str(messages[-1]["content"])[:40]


agent = Agent(role="Echo", goal="Echo", backstory="Echoes.", llm=EchoLLM(model="echo"))
task = Task(description="Say hi", expected_output="Anything", agent=agent)
print(Crew(agents=[agent], tasks=[task]).kickoff().raw)
```

---

## 6. Structured output

| Where | Use | Result lands in |
|---|---|---|
| `Task(output_pydantic=Model)` | Parsed model on the task and crew output | `out.pydantic`, `out["field"]` |
| `Task(output_json=Model)` | Dict output | `out.json_dict` |
| `Task(response_model=Model)` | Native provider structured output only | `out.raw` (JSON text); `out.pydantic` stays `None` |
| `Agent.kickoff(messages, response_format=Model)` | Standalone agent | `LiteAgentOutput.pydantic` |
| `llm.call(messages, response_model=Model)` | Direct LLM call | the parsed model |
| `LLM(model=..., response_format=Model)` | Constructor-level default | |

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `Task(response_format=Model)` | `Task(output_pydantic=Model)` | Silently ignored |
| `Agent.kickoff(msg, response_model=Model)` | `Agent.kickoff(msg, response_format=Model)` | `TypeError: ... Did you mean 'response_format'?` |
| `Task(output_pydantic=M, output_json=M)` | Pick one | `ValidationError: Only one output type can be set` |
| `Task(output_pydantic=M, output_file="report.md")` expecting prose in the file | Drop `output_pydantic`, or render the model yourself | The file gets the model's JSON, whatever the extension |
| `output_file="/abs/path/report.md"` | A relative path (or `output_file="{out_dir}/report.md"` via inputs) | The leading `/` is stripped, so the file lands under the current directory |
| `output_pydantic: Report` in `tasks.yaml` | Set `output_pydantic=Report` in the `@task` method in Python | With no matching `@output_pydantic` class: `KeyError: 'Report'`. With one: silently dropped, `out.pydantic is None` |

```python
from pydantic import BaseModel

from crewai import Agent, Crew, Task


class Report(BaseModel):
    title: str
    points: list[str]


analyst = Agent(role="Analyst", goal="Summarise", backstory="Concise.", llm="openai/gpt-4.1-mini")
task = Task(description="Summarise {topic}.", expected_output="A title and points.",
            agent=analyst, output_pydantic=Report)
out = Crew(agents=[analyst], tasks=[task]).kickoff(inputs={"topic": "bees"})
assert out.pydantic is not None, "structured output was dropped"
print(out.pydantic.title, out["points"])

standalone = analyst.kickoff("Summarise bees.", response_format=Report)
print(standalone.pydantic)
```

In a `@CrewBase` project keep the model in Python even when the rest of the task is YAML:

```python
@task
def research_task(self) -> Task:
    return Task(config=self.tasks_config["research_task"], output_pydantic=Report)
```

---

## 7. Guardrails

A function guardrail takes one argument (`TaskOutput`) and returns a tuple `(bool, value)`. On `False` the value is fed back to the agent as the error and the task retries, up to `guardrail_max_retries` (default 3); then the task raises `Task failed guardrail validation after N retries`. A string guardrail is checked by an extra LLM call.

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `def g(out) -> bool: return True` | `def g(out: TaskOutput) -> tuple[bool, Any]` returning `(True, out.raw)` | Annotated: `ValidationError: If return type is annotated, it must be Tuple[bool, Any]` at `Task(...)`. Unannotated: `TypeError: cannot unpack non-iterable bool object` at kickoff |
| `-> tuple[bool, object]` | `-> tuple[bool, Any]` (or `str`, `TaskOutput`) | Same `ValidationError` at `Task(...)` |
| `Task(max_retries=2)` | `Task(guardrail_max_retries=2)` | `DeprecationWarning` |
| Relying on `HallucinationGuardrail` | Write a function guardrail | In open-source crewai it is a no-op that always passes |

```python
from typing import Any

from crewai import Agent, Crew, Task, TaskOutput


def under_50_words(output: TaskOutput) -> tuple[bool, Any]:
    if len(output.raw.split()) > 50:
        return (False, "Keep it under 50 words.")
    return (True, output.raw)


writer = Agent(role="Writer", goal="Write", backstory="Brief.", llm="openai/gpt-4.1-mini")
task = Task(description="Describe {topic}.", expected_output="A short paragraph.", agent=writer,
            guardrails=[under_50_words, "Must not mention prices"], guardrail_max_retries=2)
print(Crew(agents=[writer], tasks=[task]).kickoff(inputs={"topic": "bees"}).raw)
```

`guardrails=[...]` runs each guardrail in order; a successful string result replaces `out.raw` for the next one.

---

## 8. Memory and knowledge

Memory is one `Memory` class (LanceDB storage). Its defaults call OpenAI: `text-embedding-3-large` for embeddings and `gpt-5.4-mini` for analysis. `Crew(memory=True)` analyses with the first agent's `llm` instead, and knowledge with no `embedder` embeds with `text-embedding-3-small`. Live with an OpenAI key: a `memory=True` crew stored a codename in one process and a new crew recalled it in the next; crew and agent knowledge both answered from the source.

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `ShortTermMemory()`, `LongTermMemory()`, `EntityMemory()` | `Memory(...)` | `ImportError` |
| `Crew(memory=True)` with no (or an invalid) `OPENAI_API_KEY` | Set the key, or pass `Memory(llm=..., embedder=...)` | Crew **completes**; every save fails silently (only a `MemorySaveFailedEvent` is emitted) and nothing is stored |
| `memory.remember(...)` with no key | Same | `RuntimeError: Memory requires an embedder for vector search` (an invalid key: `AuthenticationError ... 401`) |
| `Agent(knowledge_sources=[...])` with no key or embedder, agent in a crew | Pass `embedder={...}` on the Agent or Crew | `ValueError: Invalid Knowledge Configuration: The OPENAI_API_KEY environment variable is not set.` at crew kickoff (an invalid key: `AuthenticationError ... 401`) |
| `agent.kickoff(...)` on an agent with `knowledge_sources` | Run the agent as a task in a `Crew`, or put the facts in the prompt | No error with or without a key: `Agent.kickoff()` never queries agent knowledge, so the answer ignores it |
| `Crew(knowledge_sources=[...])` with no key or embedder | Same | Logs `Failed to upsert documents`; crew runs with **no** knowledge |
| Changing the knowledge `embedder` after a run stored knowledge | `crewai reset-memories -kn` (or `crew.reset_memories(command_type="knowledge")`), then run | `Embedding function conflict: new: <x> vs persisted: openai`; the crew runs with no knowledge |
| Adding `embedder={"provider": "openai"}` after knowledge was stored with no `embedder` (or changing the OpenAI embedding model) | Same reset | `Failed to upsert documents: Collection expecting embedding with dimension of 1536, got 3072` (the explicit provider defaults to `text-embedding-3-large`); the crew answers without its knowledge |

The embedder config shape is `{"provider": <name>, "config": {...}}`; the OpenAI model key is `model_name`. `"model"` raises `TypeError: ... unexpected keyword argument 'model'` in `Memory`, and for knowledge it is silently ignored (the crew embeds with `text-embedding-3-large`). The `ollama` provider below also needs `uv add ollama` and a running Ollama server with the model pulled; without the package, crew knowledge is silently `None`. `{"provider": "onnx"}` is a local, key-free embedder that core crewai can already run (chromadb's `onnxruntime`; about 80 MB of model downloaded on first use) - the design-agent skill's memory-and-knowledge reference has working examples. For a deterministic embedder in tests, use a callable (`Memory`) or a custom class (knowledge) - see [verify-installed-api.md](references/verify-installed-api.md).

```python
from crewai import Agent, Crew, Memory, Task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

embedder = {"provider": "ollama", "config": {"model_name": "nomic-embed-text"}}  # needs: uv add ollama
memory = Memory(llm="openai/gpt-4.1-mini", embedder=embedder)
facts = StringKnowledgeSource(content="acme was founded in 2020.")

agent = Agent(role="Analyst", goal="Answer", backstory="Uses knowledge.", llm="openai/gpt-4.1-mini")
task = Task(description="When was acme founded?", expected_output="A year.", agent=agent)
crew = Crew(agents=[agent], tasks=[task], memory=memory, knowledge_sources=[facts], embedder=embedder)
if crew.knowledge is None:
    print("knowledge failed to initialise - is the ollama package installed and the server running?")
```

Reset stored data from the project directory with `crewai reset-memories -m` (memory; errors with `Memory memory system is not initialized` if the crew has no memory), `-kn` (knowledge), `-akn` (agent knowledge), `-k` (latest kickoff outputs), `-a` (all). The old `-s`, `-l`, `-e` flags are hidden deprecated aliases that print a warning and reset the unified memory. Storage path and offline embedders: [verify-installed-api.md](references/verify-installed-api.md).

---

## 9. Project scaffold and CLI

| You probably wrote | Current form | What the wrong form does |
|---|---|---|
| `crewai create crew my_crew` expecting `crew.py` + YAML | `crewai create crew my_crew --classic` | Starts an interactive wizard that writes a JSON project (`crew.jsonc`, `agents/*.jsonc`); with no TTY it prints `Aborted!`. Scripts that only need a crew should use `--classic --skip-provider`. |
| `crewai run` on a JSON crew in CI or a script | For CI, create the crew with `crewai create crew <name> --classic` and run it with `uv run run_crew` | Opens a full-screen run view that waits for the user to quit, even with no TTY, so the command never exits. An environment variable, `CREWAI_DMN=1`, skipped the run view on crewai 1.15.x, but it is unsupported and undocumented; may change |
| Leaving `"memory": true` from the JSON scaffold with no `OPENAI_API_KEY` | Set the key, set `"memory": false`, or configure an embedder | The crew completes; memory recall and saves fail silently |
| `crewai run --inputs '{...}'` on a classic crew | Put inputs in `main.py` `run()` | `Error: --inputs is only supported for declarative flows and crews` |
| `crewai reset-memories -s -l -e` | `crewai reset-memories -m` | Deprecated aliases, warning printed |
| `return crew.kickoff(...)` from `main.run()` | Do not return the output | The `run_crew` script calls `sys.exit(<CrewOutput>)` and exits 1 after a successful run; `crewai run` prints `An error occurred while running the crew: ... non-zero exit status 1` |
| Trusting `crewai run`'s exit code in CI on a classic crew (`--classic`) or a Python flow | Run `uv run run_crew` (exit code propagates) or check the output | There `crewai run` exits 0 even when the crew or flow process failed; JSON (wizard) crews have no `run_crew` script, so create CI crews with `--classic` |

```bash
crewai version
crewai create crew research_crew --classic --skip-provider
cd research_crew && uv add "crewai[anthropic]"   # only if an agent uses an anthropic/ model
crewai install && crewai run
crewai reset-memories --help
```

The classic layout: `src/<name>/crew.py` (`@CrewBase` class), `src/<name>/config/agents.yaml` and `tasks.yaml` (keys match the `@agent`/`@task` method names), `main.py`, and `pyproject.toml` with `[tool.crewai] type = "crew"` and dependency `crewai[tools]`. In YAML, `llm: <name>` resolves to an `@llm` method of that name, otherwise it is used as a model string. `crewai create flow` also writes a `.env` with a placeholder `OPENAI_API_KEY` - replace it, never commit it.

---

## 10. Removed and deprecated

| Feature | Status in 1.15.22-1.15.23 | Do instead |
|---|---|---|
| `CodeInterpreterTool` | Removed from `crewai_tools` | Sandbox tool or service |
| `Agent(allow_code_execution=...)`, `code_execution_mode` | Deprecated no-ops | Same |
| `ShortTermMemory`, `LongTermMemory`, `EntityMemory`, `memory_config` | Removed / ignored | `Memory(...)` |
| `crewai.utilities.events` | Removed | `crewai.events` |
| `Crew(function_calling_llm=...)` | Deprecated | Per-agent `llm` |
| `Task(max_retries=...)` | Deprecated | `guardrail_max_retries` |
| `crewai.cli` module | Deprecation shim | `crewai_cli` (the CLI is its own package) |
| LiteLLM as a core dependency | Optional extra | `crewai[litellm]` only for non-native providers |

---

## 11. Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| A parameter has no effect and no error | Unknown kwargs are dropped by Agent/Task/Crew | Check `"name" in Task.model_fields` |
| `out.pydantic is None` | `output_pydantic` set in YAML, or `response_model` used instead of `output_pydantic` | Set `output_pydantic=Model` in Python; assert non-None |
| `ImportError: ... native provider not available` | Provider SDK extra missing | `uv add "crewai[anthropic]"` (or `[google-genai]`, `[bedrock]`, `[litellm]`) |
| `ValueError: OPENAI_API_KEY is required` at kickoff | No `llm=` set, so the default `gpt-4.1-mini` was used | Set `llm=` or `MODEL`, plus the provider key |
| Crew finishes but nothing was remembered | `memory=True` with no embedder key | Pass `Memory(embedder=...)` or set the key; listen for `MemorySaveFailedEvent` from `crewai.events` |
| Knowledge never appears in prompts | Crew-level knowledge failed to embed | Set `embedder=`; look for `Failed to upsert documents` |
| `TypeError: ... unexpected keyword argument 'from_task'` | Custom `BaseLLM.call` with the old signature | Accept `from_task`, `from_agent`, `response_model`, `**kwargs` |
| `Tuple[bool, Any]` ValidationError at `Task(...)` | Guardrail annotated `-> bool` or `tuple[bool, object]` | Annotate `-> tuple[bool, Any]` and return a tuple |
| `crewai create crew` hangs or prints `Aborted!` | It is an interactive JSON wizard now | Add `--classic` for the `@CrewBase` layout; use it for CI and scripts |
| `crewai run` never returns on a JSON crew | The run view waits for a keypress | For CI, use `crewai create crew <name> --classic` plus `uv run run_crew` |
| `kickoff_for_each` results all answer the first topic | The `Crew` was already kicked off | Build a fresh `Crew` per batch |
| `token_usage` larger than the run could have used | An `LLM` object shared by several agents or reused across crews | One `LLM` per agent per crew, or count `LLMCallCompletedEvent`s |
| Agent never uses its MCP tools under `akickoff()` | `https://` string in `mcps` inside a running event loop | `MCPServerHTTP(url=...)` |
| `Embedding function conflict ... persisted: openai` | Knowledge was stored with another embedder | `crewai reset-memories -kn` |
| `Collection expecting embedding with dimension of 1536, got 3072` | Knowledge was stored with another OpenAI embedding model | `crewai reset-memories -kn` |
| `crewai run` reports `non-zero exit status 1` after the crew succeeds | `run()` returns the `CrewOutput` | Do not return it |

---

## 12. Checklist

- [ ] `crewai version` checked; rows re-verified if not 1.15.x
- [ ] Every `Agent`/`Task`/`Crew` kwarg exists in `model_fields`
- [ ] Tools import from `crewai.tools`, flow decorators and `persist` from `crewai.flow`
- [ ] Every task has `expected_output`
- [ ] Every non-OpenAI model string has its extra in `pyproject.toml`
- [ ] Structured output set in Python with `output_pydantic`, and `out.pydantic` asserted non-None
- [ ] Guardrails return `(bool, value)` and are annotated `tuple[bool, Any]` or not at all
- [ ] Memory and knowledge have an explicit embedder or a provider key in the environment
- [ ] No `CodeInterpreterTool`, `allow_code_execution`, `ShortTermMemory`, `memory_config`
- [ ] Classic projects created with `crewai create crew <name> --classic`; provider extra added with `uv add`
- [ ] CI and scripts use classic crews (`crewai create crew <name> --classic`) run with `uv run run_crew`

---

## References

- [Verify the installed API](references/verify-installed-api.md) - one-liners to check fields, defaults and signatures in the installed crewai; storage paths; an offline embedder for memory and knowledge
- [Source receipts](references/source-receipts.md) - the crewai source file and line behind each row, so you can re-check after an upgrade
- Public docs: https://docs.crewai.com

For related skills:

- **ask-docs** - query the live CrewAI docs when a row may have changed
- **getting-started** - project scaffolding and choosing crews vs flows
- **design-agent** / **design-task** - tuning agents and tasks once the API is right
- **build-flow** - Flow state, routers, `@persist`, human feedback
- **connect-tools-and-mcp** - `BaseTool`, `@tool`, `mcps=[...]`
- **test-crewai-project** - offline stub LLM and deterministic tests
- **deploy-to-amp** / **call-deployed-crew** - shipping and calling a crew
