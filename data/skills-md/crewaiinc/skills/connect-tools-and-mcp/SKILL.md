---
name: connect-tools-and-mcp
description: "Giving crewAI agents tools and MCP servers on crewai 1.15.x: custom BaseTool with args_schema and @tool, which crewai_tools names really exist, tool caching, max_usage_count, ToolFailure, Agent(mcps=[...]) string and MCPServerStdio/HTTP/SSE forms, rewritten MCP tool names, MCPServerAdapter, timeouts, and what works on a hosted deployment. Use when writing or debugging a tool or MCP connection, when you see 'cannot import name BaseTool from crewai_tools', 'You are missing the mcp package', 'MCPConnectionError', 'Operation timed out after 30 seconds', 'reached its usage limit', 'Invalid MCP reference', 'Anthropic function name ... must start with a letter', an agent that never calls an MCP tool, mcps=[...] that yields no tools (for example an https:// string under akickoff or on CrewAI AMP), or a stdio MCP server that works locally but not after deploy."
---

# Connect Tools and MCP Servers to CrewAI Agents

Give an agent working tools - custom Python, prebuilt `crewai_tools`, or MCP servers - without the 0.x-era mistakes that fail silently.

Verified against crewai 1.15.22 and 1.15.23 on 2026-10-01.
Live-tested on CrewAI AMP and real LLMs on 2026-10-01.
Run `crewai version` first; if the major/minor differs from 1.15, re-verify version-sensitive rows with the `ask-docs` skill before trusting them.

---

## 1. Pick the mechanism

| You need | Use | Section |
|---|---|---|
| A quick Python function as a tool | `@tool` from `crewai.tools` | 3 |
| A tool with config, state, or a documented input schema | `BaseTool` subclass with `args_schema` | 3 |
| A prebuilt search/scrape/file tool | `crewai_tools` - but import it once to prove the name exists | 5 |
| A remote MCP server | `Agent(mcps=[MCPServerHTTP(...)])` - not an `https://` string if the crew is deployed or uses `akickoff()` | 6, 8 |
| An MCP server that ships with your code | `Agent(mcps=[MCPServerStdio(...)])` - also works on CrewAI AMP when the server is in the package | 6, 10 |
| An integration connected in your CrewAI AMP account | `mcps=["<slug>"]` or `"<slug>#<tool>"` | 6 |
| Bare MCP tool names or a manual start/stop lifecycle | `MCPServerAdapter` (needs `crewai-tools[mcp]`) | 9 |

`mcp` is already a core dependency of crewai 1.15.x - native `mcps=` needs no extra install.

---

## 2. Imports

| You probably wrote | Current form | What happens with the old form |
|---|---|---|
| `from crewai_tools import BaseTool` | `from crewai.tools import BaseTool` | `ImportError: cannot import name 'BaseTool' from 'crewai_tools'` |
| `from crewai_tools import tool` | `from crewai.tools import tool` | `ImportError: cannot import name 'tool' from 'crewai_tools'` |
| `from crewai_tools import CodeInterpreterTool` | a sandbox tool: `E2BPythonTool`, `DaytonaPythonTool` | `ImportError` - removed |
| `from crewai_tools import ZapierActionsAdapter` | `from crewai_tools.adapters.zapier_adapter import ZapierActionsAdapter` (or top-level `ZapierActionTools`) | `ImportError` at top level |
| `from crewai.mcp import ...` for the adapter | `from crewai_tools import MCPServerAdapter` | adapter lives in crewai_tools; native configs live in `crewai.mcp` |

```python
from crewai.tools import BaseTool, tool, ToolFailure, ToolExecutionFailedError
from crewai.mcp import (
    MCPServerStdio, MCPServerHTTP, MCPServerSSE,
    create_static_tool_filter, create_dynamic_tool_filter,
)
from crewai.mcp.exceptions import MCPConnectionError
```

---

## 3. Custom tools

```python
from pydantic import BaseModel, Field
from crewai.tools import BaseTool, tool

class PriceInput(BaseModel):
    sku: str = Field(..., description="Product SKU, e.g. 'A-100'")
    currency: str = Field("EUR", description="ISO currency code")

class PriceTool(BaseTool):
    name: str = "price_lookup"
    description: str = "Return the unit price for a SKU. Use before quoting a price."
    args_schema: type[BaseModel] = PriceInput

    def _run(self, sku: str, currency: str = "EUR") -> str:
        return f"{sku} costs 9.99 {currency}"

@tool("Unit Converter")
def convert(km: float) -> str:
    """Convert kilometres to miles."""
    return f"{km * 0.621371:.1f} mi"

print(PriceTool().run(sku="A-100"))   # args are validated against PriceInput first
print(convert.run(km=10))
```

Rules that prevent real failures:

| Rule | Failure it prevents |
|---|---|
| Always define `_run`, even for an async tool | `_run` is abstract: `TypeError: Can't instantiate abstract class ... without an implementation for abstract method '_run'` |
| Put async code in `async def _run(...)` | Agents execute tools through `_run` in both `kickoff()` and `akickoff()`; an `_arun` override is only used when you call `tool.arun()` yourself |
| Give `@tool` functions a docstring | `ValueError: Function must have a docstring` at decoration time |
| Write the description for the LLM: what it does and when to use it | The agent picks tools by description; MCP tools in particular have opaque names (section 7) |
| Expect the displayed name to be sanitized | `@tool("Unit Converter")` is offered to the LLM as `unit_converter` (seen in a live run with claude-haiku-4-5) |
| Return a `ToolFailure` instead of an error string | An error string looks like data; a `ToolFailure` is recorded in `TaskOutput.tool_failures` and can abort the run (below) |

Per-tool options (all on `BaseTool` and accepted by `@tool(...)` where noted):

| Field | Effect (verified) |
|---|---|
| `max_usage_count=N` (also `@tool("x", max_usage_count=N)`) | After N runs **within one task** the agent gets `Tool '...' has reached its usage limit of N times and cannot be used anymore.` The next task or kickoff gets a fresh allowance, so enforce "once per run" side effects yourself. `0` or negative is a ValidationError |
| `result_as_answer=True` (also on `@tool`) | The tool's return value becomes the task output; no further LLM call |
| `cache_function=lambda args, result: bool` | Decides per call whether the result may be cached (section 4) |
| `tool_failure_policy="ignore" \| "warn" \| "raise"` | Also on Agent, Task and Crew; default `warn`. `raise` aborts with `ToolExecutionFailedError` |

Failures: a tool that raises does not fail the crew. The exception text is fed back to the agent and recorded as a tool failure, and the crew finishes "successfully". When downstream code must know, return `ToolFailure(...)` and set `tool_failure_policy="raise"`, or inspect `result.tasks_output[i].tool_failures`. Full examples: [references/custom-tools.md](references/custom-tools.md).

`Task(tools=[...])` replaces the agent's tools for that task; it does not add to them.

---

## 4. Tool result caching

| Setting | Default in 1.15.22-1.15.23 | Effect |
|---|---|---|
| `Crew(cache=...)` | `False` | Opt-in. With `True`, a repeat call with identical arguments returns the first result without running the tool |
| `Agent(cache=...)` | `True` | Only *permits* participation; `False` opts that agent out even when the crew caches |
| `BaseTool(cache_function=...)` | always cache | Return `False` to keep a result out of the cache |

Through crewai 1.15.2 the crew cached tool results by default; from 1.15.3 it is opt-in. If you relied on the old behaviour, set `Crew(cache=True)` explicitly. Never enable it for live-data or state-changing tools unless their `cache_function` returns `False`.

A separate guard is not caching: if the agent repeats the exact same call twice in a row, crewai refuses the second call ("I tried reusing the same input...") whether or not caching is on.

---

## 5. crewai_tools: names that exist

crewai-tools 1.15.22-1.15.23 exports 118 names. Import a tool before you write code around it. Models routinely invent these:

| Hallucinated name (ImportError) | Real 1.15.22-1.15.23 name |
|---|---|
| `CodeInterpreterTool` | removed - use `E2BPythonTool` / `DaytonaPythonTool` |
| `BedrockKBRetriever` | `BedrockKBRetrieverTool` |
| `GitHubSearchTool`, `GithubTool` | `GithubSearchTool` |
| `ArxivTool` | `ArxivPaperTool` |
| `ComposioToolSet` | `ComposioTool` |
| `GoogleSearchTool`, `WebSearchTool`, `DuckDuckGoSearchTool` | `SerperDevTool`, `BraveSearchTool`, `TavilySearchTool`, `EXASearchTool` |
| `PDFTextWritingTool`, `PGSearchTool` | none |
| `WikipediaTool`, `PythonREPLTool`, `ShellTool`, `CalculatorTool`, `HumanTool`, `LangChainTool`, `SeleniumTool` | none (`SeleniumScrapingTool` exists) - write a custom tool |

Many tools need a third-party package. When it is missing, constructing the tool asks `You are missing the '<pkg>' package. Would you like to install it? [y/N]` (verified for `EXASearchTool`, `TavilySearchTool`, `FirecrawlSearchTool`, `SeleniumScrapingTool`). With a terminal attached that blocks forever; with stdin closed it raises `click.exceptions.Abort`. Install the extra up front, e.g. `uv add "crewai-tools[exa-py]"`. Prebuilt tools are offered to the LLM under their sanitized display name, not the class name: `DirectoryReadTool` appears as `list_files_in_directory`, `FileReadTool` as `read_a_files_content`. RAG tools (`WebsiteSearchTool`, `PDFSearchTool`, ...) fail at construction without an embedder key. Full list and extras: [references/crewai-tools-names.md](references/crewai-tools-names.md).

---

## 6. Native `Agent(mcps=[...])`

```python
from crewai import Agent
from crewai.mcp import MCPServerHTTP, MCPServerSSE, MCPServerStdio, create_static_tool_filter

agent = Agent(
    role="Inventory analyst",
    goal="Answer stock questions",
    backstory="Careful with numbers.",
    mcps=[
        MCPServerHTTP(url="https://mcp.example.com/mcp",
                      headers={"Authorization": "Bearer <your-key>"}),
        MCPServerSSE(url="https://legacy.example.com/sse"),
        MCPServerStdio(command="uvx", args=["mcp-server-time"],
                       tool_filter=create_static_tool_filter(allowed_tool_names=["get_current_time"])),
        "https://docs.example.com/mcp#search_docs",   # https string, one tool (sync kickoff only - section 8)
        "acme#lookup_stock",                           # AMP-connected integration, one tool
        "acme#list_warehouses",                        # second tool = second ref
    ],
)
```

String refs are validated at construction; nothing connects until a task runs.

| Form | Rule (all verified) |
|---|---|
| `MCPServerStdio(command, args, env, tool_filter, cache_tools_list)` | Spawns a subprocess where the crew runs. The server does **not** inherit your environment: it gets only `HOME, LOGNAME, PATH, SHELL, TERM, USER` plus `env=`, so pass its API keys in `env` explicitly. No `cwd` or timeout field |
| `MCPServerHTTP(url, headers, streamable=True, tool_filter, cache_tools_list)` | Streamable HTTP; `http://` and `https://` both work. Use a hostname, not an IP: `http://127.0.0.1:8765/mcp` makes tool names start with a digit and Anthropic models reject them (`ValueError: Anthropic function name '127_0_0_1_8765_mcp_lookup_stock' must start with a letter or underscore`); `http://localhost:8765/mcp` works |
| `MCPServerSSE(url, headers, tool_filter, cache_tools_list)` | Legacy SSE servers (usually a `/sse` path) |
| `"https://host/path"` string | Must start with `https://`. Optional `#tool` keeps one tool. Resolves to **zero tools, silently,** inside a running event loop - `await crew.akickoff()` and crews deployed on CrewAI AMP (section 8) |
| `"slug"` / `"slug#tool"` string | An integration connected in a CrewAI AMP account; legacy `"crewai-amp:slug"` also works. A slug the account has not connected gives zero tools and the run continues (seen on AMP) |
| `"http://localhost:8000/mcp"` or any string that is neither `https://` nor a slug | `ValidationError: ... Invalid MCP reference: 'http://...'. String references must be an 'https://' URL or a valid slug` when the Agent is built. Use `MCPServerHTTP` for `http://` |
| `"slug#a,b"` | Same `Invalid MCP reference` ValidationError. One ref per tool |
| `"https://...#a,b"` | Accepted, but selects **zero** tools (`#` takes one name). One ref per tool |
| `tool_filter` names | Matched against the **sanitized** tool name: a server tool `getForecast` must be listed as `get_forecast` |

Full examples for each transport, dynamic filters and the AMP form: [references/mcp-connections.md](references/mcp-connections.md).

---

## 7. MCP tool names are rewritten - never hard-code them

Native MCP tools are offered to the LLM as `<server name>_<tool name>`, then sanitized: lowercase, non-alphanumerics become `_`, camelCase is split, max 64 characters.

| Source | Name the LLM sees for tool `lookup_stock` |
|---|---|
| `MCPServerStdio(command="python", args=["servers/inventory.py"])` | `python_servers_inventory_py_lookup_stock` |
| `MCPServerStdio` with absolute paths, e.g. `/opt/app/.venv/bin/python` + `/opt/app/servers/inventory_server.py` | `opt_app_venv_bin_python_opt_app_servers_inventory_serve_a87662e9` - over 64 chars, so it is truncated and hashed and the tool name is gone. `command=sys.executable` does the same, locally and on AMP |
| `MCPServerHTTP(url="http://localhost:8765/mcp")` | `localhost_8765_mcp_lookup_stock` (an IP host would start the name with a digit - section 6) |
| `MCPServerHTTP(url="https://mcp.example.com/mcp")` or the same `https://` string | `mcp_example_com_mcp_lookup_stock` |
| `"acme#lookup_stock"` (AMP) | built from the server URL the account returns, not from `acme` - only the `_lookup_stock` suffix is stable |
| `MCPServerAdapter` | `lookup_stock` (bare) |

Consequences:
- Do not write "call the `lookup_stock` tool" in a task description or backstory. Describe the capability ("check stock levels with the inventory tool"), or derive the exact name at runtime. A native function-calling model usually copes (claude-haiku-4-5 told "call the lookup_stock tool" called `python_mcp_server_py_lookup_stock`), but a model on the text ReAct path fails with `Action 'lookup_stock' don't exist`, and a hashed name leaves only the description to go on.
- Keep stdio `command`/`args` short (`"uvx"`, `"npx"`, a relative script path) so names stay readable and under 64 characters. Absolute paths also put your filesystem layout into every prompt. A scoped npx package already uses about 45 characters: `npx -y @modelcontextprotocol/server-filesystem ./data` hashed `list_allowed_directories` to `..._data_list_4ab656ee`; use `MCPServerAdapter` when bare names matter.
- In code, identify a resolved native MCP tool by `tool.original_tool_name`, not by `tool.name`.

---

## 8. Timeouts, retries and failure behaviour

| Path | Connect | Per tool call | Retries | When the server is down |
|---|---|---|---|---|
| `MCPServerStdio/HTTP/SSE` config and AMP slugs | 30 s | 30 s | 3 attempts on timeout - **the tool runs again each time**. Live run: a 35 s tool ran 3 times (~99 s); the agent got `Error executing tool: Error executing MCP tool slow_report: Operation timed out after 30 seconds` as its observation, a tool failure was recorded and the crew finished. A direct `tool.run()` raises `RuntimeError` instead | kickoff raises `MCPConnectionError` |
| `"https://..."` string | 10 s, 15 s discovery | 60 s | 3 attempts (a 65 s tool ran 3 times, ~198 s) and then returns the error **as a string** | agent runs with **no MCP tools**, no error |
| `MCPServerAdapter` | `connect_timeout=` (default 30) | no crewai timeout (a 35 s call completed) | none | constructor raises `RuntimeError: Failed to initialize MCP Adapter` |

In 1.15.22-1.15.23 the native timeouts are module constants. No field on `MCPServerStdio`, `MCPServerHTTP`, `MCPServerSSE` or `Agent` changes them. So:
- Keep MCP tool calls well under 30 s. Make them idempotent, because a timed-out call is re-sent. For long jobs, return a job id from one tool and poll with another.
- Prefer config objects to `https://` strings in production: they fail loudly at kickoff instead of silently dropping tools.
- `https://` strings discover tools with `asyncio.run()`. Inside a running event loop that fails and the agent gets **zero tools with no error** (only `RuntimeWarning: coroutine 'MCPToolResolver._get_mcp_tool_schemas_async' was never awaited`). Seen live with `await crew.akickoff()` and on a CrewAI AMP deployment - the agent runs without the tools, and its answer may describe tool calls it never made. The same server as `MCPServerHTTP(url=...)` worked in both places. Sync `crew.kickoff()`, including from a sync Flow step, resolves strings fine.
- An MCP result with `isError: true` reaches the agent as text. It is recorded as a `mcp_error` tool failure, and `tool_failure_policy="raise"` turns it into `ToolExecutionFailedError`.

---

## 9. MCPServerAdapter and `@CrewBase` `mcp_server_params`

`MCPServerAdapter` needs the extra: `uv add "crewai-tools[mcp]"` (it installs `mcpadapt`; `mcp` itself is already present). Without the extra, constructing it asks `You are missing the 'mcp' package. Would you like to install it? [y/N]`. Under a terminal that blocks forever; with stdin closed (typical CI) it raises `click.exceptions.Abort`. Install the extra explicitly.

```python
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter

params = StdioServerParameters(command="python", args=["mcp_server.py"])
with MCPServerAdapter(params, "lookup_stock", connect_timeout=60) as tools:
    print([t.name for t in tools])   # ['lookup_stock'] - bare names, filtered by name
    # build agents with tools=tools and kick off INSIDE the with-block
```

The server starts in the constructor and stops when the `with` block exits. Tools used after that fail. For a remote server pass a dict and name the transport: `{"url": "https://<host>/mcp", "transport": "streamable-http"}`. Without `"transport"` the adapter speaks SSE, and against a streamable-HTTP `/mcp` endpoint it fails with `Couldn't connect to the MCP server after <connect_timeout> seconds`.

In a `@CrewBase` class, set `mcp_server_params` (and optionally `mcp_connect_timeout`, default 30) and call `self.get_mcp_tools("name", ...)` in an `@agent` method. crewai stops that adapter after every kickoff. Calling `.crew().kickoff()` a second time on the **same instance** made every MCP call return `Event loop is closed`, yet the crew still "succeeded". Build a fresh instance per run: `InventoryCrew().crew().kickoff()`.

---

## 10. Hosted deployments: what works on CrewAI AMP

Measured on a CrewAI AMP deployment (ZIP deploy, crewai 1.15.23, `anthropic/claude-haiku-4-5`), one kickoff per form:

| Form in the deployed crew | Result |
|---|---|
| `MCPServerHTTP(url="https://<public host>/mcp")` | Works - the model called `<host>_mcp_<tool>` |
| `"https://<public host>/mcp#tool"` string | **Zero tools, run SUCCESS** - the model made up a tool call in its answer (section 8) |
| `MCPServerStdio(command="python", args=["-m", "<pkg>.inv_server"])`, server module inside `src/<pkg>/` | Works - a stdio server shipped in the package runs inside the deployment |
| Same with `command=sys.executable` | Works (tool name hashed, section 7) |
| `MCPServerStdio(..., env={"X": os.environ["X"]})` with `X` a deployment env var | Server sees `X`; without `env=` it does not |
| `MCPServerAdapter(StdioServerParameters(...))` with `crewai-tools[mcp]` in `pyproject.toml` | Works, bare tool names |
| `MCPServerStdio` pointing at a file that is not in the deployment (a laptop path) | Run fails with `MCPConnectionError` |
| `MCPServerStdio(command="npx", ...)` | Run fails the same way - the deployment only has what your Python project installs |
| `MCPServerHTTP` at a wrong path (HTTP 404) | Run fails the same way |
| `"<slug>#tool"` not connected in the account | Zero tools, run SUCCESS |

How a failed MCP connection looks from the API: for each `MCPConnectionError` run above, `GET /status/{kickoff_id}` answered **HTTP 500 `Internal Server Error`** (plain text) on every poll, minutes later too, instead of a JSON `FAILED` state. A plain exception in the same crew gave the documented shape: `{"state": "FAILED", "status": "ValueError: ..."}`. Treat a persistent 500 from `/status` as "the run failed", and check the MCP connection first.

Rules:
- A stdio server runs as a child process wherever the crew runs. Ship it inside the package (`src/<pkg>/server.py`, started with `python -m <pkg>.server`) and its Python dependencies in `pyproject.toml`/`uv.lock`; a laptop path or a Node/npx server is not there.
- For remote servers use `MCPServerHTTP(url="https://<host>/mcp")` (or `MCPServerSSE`), never an `https://` string. Point deployments at a stable hostname you control, require auth on it, and do not leave temporary tunnels running.
- Health check: a bare `curl -s -o /dev/null -w "%{http_code}" https://<host>/mcp` returns **406** from a healthy streamable-HTTP MCP endpoint (seen on a public server and locally). **404** means wrong path; `000`/connection refused means it is down.
- Put tokens in `headers` read from environment variables (`os.environ["ACME_MCP_TOKEN"]`), never in the URL string or in code. A stdio server gets deployment env vars only through `env=`.

---

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `cannot import name 'BaseTool' from 'crewai_tools'` | 0.x import path | `from crewai.tools import BaseTool, tool` |
| `Can't instantiate abstract class ... '_run'` | Only `_arun` defined | Define `_run` (it may be `async def`) |
| `Action 'lookup_stock' don't exist, these are the only available Actions: ...`, or the agent never uses the MCP tool | Prompt names the bare tool (`lookup_stock`) but the LLM sees `python_..._lookup_stock` | Describe the capability; derive names at runtime |
| `ValidationError ... Invalid MCP reference: 'github#a,b'` | `#` takes one tool name | `["github#a", "github#b"]` |
| `mcps=["https://...#a,b"]` gives no tools | Same, but https strings are not validated | One ref per tool |
| `ValidationError ... Invalid MCP reference: 'http://localhost:8000/mcp'` | Strings must be `https://` or a slug | `MCPServerHTTP(url="http://localhost:8000/mcp")` |
| `Anthropic function name '127_0_0_1_...' must start with a letter or underscore` | MCP server URL uses an IP address | Use a hostname (`localhost`) |
| `https://` string MCP gives no tools under `akickoff()` or on AMP; the answer invents tool calls | String refs cannot resolve inside a running event loop | `MCPServerHTTP(url=...)` |
| `GET /status` keeps failing or the run never completes | The run may have hit `MCPConnectionError` (stdio command or file missing, wrong URL) | Run the crew locally to see the error; fix the MCP connection |
| `tool_filter` keeps nothing | Filter used the server's camelCase name | Use the sanitized name (`get_forecast`) |
| Run hangs at "Would you like to install it? [y/N]" | Missing optional package (`crewai-tools[mcp]`, `exa-py`, ...) | Install the extra before running |
| Tool ran 3 times / side effect repeated | Native MCP call exceeded 30 s and was retried | Keep calls short and idempotent |
| Crew "succeeds" but the answer says the tool errored | Tool exceptions are fed to the agent, not raised | Return `ToolFailure`; set `tool_failure_policy="raise"`; check `tool_failures` |
| Stale results after enabling `Crew(cache=True)` | Live-data tool cached | `cache_function=lambda a, r: False` or `Agent(cache=False)` |
| Repeated identical calls now hit the API every time | Crew cache is opt-in in 1.15.x | `Crew(cache=True)` |
| Second kickoff of the same `@CrewBase` instance: `Event loop is closed` | Adapter stopped after the first kickoff | New crew instance per kickoff |
| stdio MCP server says its API key is missing although it is in your `.env` | stdio servers get a minimal environment, not yours | `MCPServerStdio(..., env={"X_API_KEY": os.environ["X_API_KEY"]})` |
| Works locally, fails after deploy | stdio server file or command (`npx`, a laptop path) not in the deployment | Ship the server inside the package, or serve it over HTTP at a stable URL |

---

## Checklist

- [ ] `BaseTool`/`tool` imported from `crewai.tools`; every `crewai_tools` name imported once to prove it exists
- [ ] Custom tools define `_run`, have an `args_schema` (or typed `@tool` signature) and an LLM-oriented description
- [ ] Failures returned as `ToolFailure`; `tool_failure_policy` chosen deliberately
- [ ] `Crew(cache=...)` set explicitly; live-data tools excluded from caching
- [ ] Optional packages and `crewai-tools[mcp]` installed up front, so no interactive prompt can block
- [ ] One `"slug#tool"` ref per tool; `http://` servers via `MCPServerHTTP`, not a string; hostnames, not IP addresses
- [ ] No `https://` string refs in deployed crews or with `akickoff()` - use `MCPServerHTTP`
- [ ] No prompt or code depends on a bare MCP tool name; stdio commands kept short
- [ ] stdio servers get their keys through `env=` (they do not inherit the crew's environment)
- [ ] MCP tool calls finish well under 30 s and are idempotent
- [ ] Deployed crews use HTTP/SSE MCP servers at a stable URL that returns 406 on a bare GET, or stdio servers shipped inside the package
- [ ] A fresh `@CrewBase` instance per kickoff when using `mcp_server_params`

---

## References

- [Custom Tools](references/custom-tools.md) - BaseTool, `@tool`, async, ToolFailure and failure policy, caching, usage limits, with runnable examples
- [MCP Connections](references/mcp-connections.md) - every `mcps=` form, filters, name derivation, timeouts, MCPServerAdapter, `@CrewBase`, deployment
- [crewai_tools Names](references/crewai-tools-names.md) - the full 1.15.22-1.15.23 export list, hallucinated names, extras and construction behaviour
- Public docs: https://docs.crewai.com/en/concepts/tools and https://docs.crewai.com/en/mcp/overview

For related skills:

- **check-crewai-api** - current Agent/Task/Crew API and imports beyond tools
- **design-agent** - choosing how many tools an agent gets and writing role/goal/backstory
- **test-crewai-project** - driving tool calls offline with a stub LLM
- **deploy-to-amp** - getting a project with MCP connections onto CrewAI AMP
- **ask-docs** - query the live docs when the installed version differs
