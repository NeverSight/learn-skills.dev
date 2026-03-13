---
name: vercel-ai-sdk
description: Vercel AI SDK (Python) - patterns for building LLM-powered apps with streaming, tools, hooks, and structured output
---

# Vercel AI SDK (Python)

```bash
uv add vercel-ai-sdk
```

```python
import vercel_ai_sdk as ai
```

## Core workflow

`ai.run(root, *args, checkpoint=None, cancel_on_hooks=False)` is the entry point. It creates a `Runtime` (stored in a context var), starts `root` as a background task, processes an internal step queue, and yields `Message` objects. All SDK functions (`stream_step`, `execute_tool`, hooks) require this Runtime context -- they must be called within `ai.run()`.

The root function is any async function. If it declares a param typed `ai.Runtime`, it's auto-injected.

```python
@ai.tool
async def talk_to_mothership(question: str) -> str:
    """Contact the mothership for important decisions."""
    return "Soon."

async def agent(llm: ai.LanguageModel, query: str) -> ai.StreamResult:
    return await ai.stream_loop(
        llm,
        messages=ai.make_messages(system="You are a robot assistant.", user=query),
        tools=[talk_to_mothership],
    )

llm = ai.ai_gateway.GatewayModel(model="anthropic/claude-opus-4.6")
async for msg in ai.run(agent, llm, "When will the robots take over?"):
    print(msg.text_delta, end="")
```

**`@ai.tool`** turns an async function into a `Tool`. Schema is extracted from type hints + docstring. If a tool declares `runtime: ai.Runtime`, it's auto-injected (excluded from LLM schema). Tools are registered globally by name.

**`ai.stream_step(llm, messages, tools=None, label=None, output_type=None)`** -- single LLM call. Returns `StreamResult` with `.text`, `.tool_calls`, `.output`, `.usage`, `.last_message`.

**`ai.stream_loop(llm, messages, tools, label=None, output_type=None)`** -- agent loop: calls LLM → executes tools → repeats until no tool calls. Returns final `StreamResult`.

Both are thin convenience wrappers (not magical -- they could be reimplemented by the user). `stream_step` is a `@ai.stream`-decorated function that calls `llm.stream()`. `stream_loop` calls `stream_step` in a while loop with `ai.execute_tool()` between iterations.

**`ai.execute_tool(tool_call, message=None)`** runs a tool call by name from the global registry. Handles malformed JSON / invalid args gracefully -- reports as a tool error so the LLM can retry rather than crashing.

### Multi-agent

Use `asyncio.gather` with labels to run agents in parallel:

```python
async def multi(llm: ai.LanguageModel, query: str) -> ai.StreamResult:
    r1, r2 = await asyncio.gather(
        ai.stream_loop(llm, msgs1, tools=[t1], label="researcher"),
        ai.stream_loop(llm, msgs2, tools=[t2], label="analyst"),
    )
    return await ai.stream_loop(
        llm,
        ai.make_messages(user=f"{r1.text}\n{r2.text}"),
        tools=[],
        label="summary",
    )
```

The `label` field on messages lets the consumer distinguish which agent produced output (e.g. `msg.label == "researcher"`).

### Messages

`ai.make_messages(system=None, user=str)` builds a message list.

`Message` is a Pydantic model with `role`, `parts` (list of `TextPart | ToolPart | ReasoningPart | HookPart | StructuredOutputPart`), `label`, and `usage`. Serialize with `msg.model_dump()`, restore with `ai.Message.model_validate(data)`.

Key properties for consuming streamed output:
- `msg.text_delta` -- current text chunk (use for live streaming display)
- `msg.text` -- full accumulated text
- `msg.tool_calls` -- list of `ToolPart` objects
- `msg.output` -- validated Pydantic instance (when using `output_type`)
- `msg.is_done` -- true when all parts finished streaming
- `msg.get_hook_part()` -- find a hook suspension part (for human-in-the-loop)


## Customization

### Custom loop

When `stream_loop` doesn't fit (conditional tool execution, approval gates, custom routing), use `stream_step` in a manual loop:

```python
async def agent(llm: ai.LanguageModel, query: str) -> ai.StreamResult:
    messages = ai.make_messages(system="...", user=query)
    tools = [get_weather, get_population]

    while True:
        result = await ai.stream_step(llm, messages, tools)
        if not result.tool_calls:
            return result
        messages.append(result.last_message)
        await asyncio.gather(*(ai.execute_tool(tc, message=result.last_message) for tc in result.tool_calls))
```

### Custom stream

`@ai.stream` wires an async generator (yielding `Message`) into the Runtime's step queue. This is what makes streaming visible to `ai.run()` and enables checkpoint replay -- calling `llm.stream()` directly would bypass both.

```python
@ai.stream
async def custom_step(llm: ai.LanguageModel, messages: list[ai.Message]) -> AsyncGenerator[ai.Message]:
    async for msg in llm.stream(messages=messages, tools=[...]):
        msg.label = "custom"
        yield msg

result = await custom_step(llm, messages)  # returns StreamResult
```

Tools can also stream intermediate progress via `runtime.put_message()`:

```python
@ai.tool
async def long_task(input: str, runtime: ai.Runtime) -> str:
    """Streams progress back to the caller."""
    for step in ["Connecting...", "Processing..."]:
        await runtime.put_message(
            ai.Message(role="assistant", parts=[ai.TextPart(text=step, state="streaming")], label="progress")
        )
    return "final result"
```


## Hooks

Hooks are typed suspension points for human-in-the-loop. Decorate a Pydantic model to define the resolution schema:

```python
@ai.hook
class Approval(pydantic.BaseModel):
    granted: bool
    reason: str
```

Inside agent code -- blocks until resolved:
```python
approval = await Approval.create("approve_send_email", metadata={"tool": "send_email"})
if approval.granted:
    await ai.execute_tool(tc, message=result.last_message)
else:
    tc.set_error(f"Rejected: {approval.reason}")
```

From outside (API handler, iterator loop):
```python
Approval.resolve("approve_send_email", {"granted": True, "reason": "User approved"})
Approval.cancel("approve_send_email")
```

**Long-running mode** (`cancel_on_hooks=False`, default): `create()` blocks until `resolve()` or `cancel()` is called externally. Use for websocket/interactive UIs.

**Serverless mode** (`cancel_on_hooks=True`): unresolved hooks are cancelled, the run ends. Inspect `result.pending_hooks` and `result.checkpoint` to resume later.

Consuming hooks in the iterator:

```python
async for msg in ai.run(agent, llm, query):
    if (hook := msg.get_hook_part()) and hook.status == "pending":
        answer = input(f"Approve {hook.hook_id}? [y/n] ")
        Approval.resolve(hook.hook_id, {"granted": answer == "y", "reason": "operator"})
        continue
    print(msg.text_delta, end="")
```

### Checkpoints

`Checkpoint` records completed steps (LLM calls), tool executions, and hook resolutions. On replay, cached results are returned without re-executing.

```python
data = result.checkpoint.model_dump()  # serialize (JSON-safe dict)
checkpoint = ai.Checkpoint.model_validate(data)  # restore
result = ai.run(agent, llm, query, checkpoint=checkpoint)  # replay completed work
```

Primary use case is serverless hook re-entry.


## Adapters

### Providers

```python
# Vercel AI Gateway (recommended)
# Uses AI_GATEWAY_API_KEY env var
llm = ai.ai_gateway.GatewayModel(model="anthropic/claude-opus-4.6", thinking=True, budget_tokens=10000)

# Direct
llm = ai.openai.OpenAIModel(model="gpt-5")
llm = ai.anthropic.AnthropicModel(model="claude-opus-4-6", thinking=True, budget_tokens=10000)
```

All implement `LanguageModel` with `stream()` (async generator of `Message`) and `buffer()` (returns final `Message`). Gateway routes Anthropic models through the native Anthropic API for full feature support, others through OpenAI-compatible endpoint.

### AI SDK UI

For streaming to AI SDK frontend (`useChat`, etc.):

```python
from vercel_ai_sdk.ai_sdk_ui import to_sse_stream, to_messages, UI_MESSAGE_STREAM_HEADERS

messages = to_messages(request.messages)
return StreamingResponse(to_sse_stream(ai.run(agent, llm, query)), headers=UI_MESSAGE_STREAM_HEADERS)
```


## Other features

### Structured output

Pass a Pydantic model as `output_type`:

```python
class Forecast(pydantic.BaseModel):
    city: str
    temperature: float

result = await ai.stream_step(llm, messages, output_type=Forecast)
result.output.city  # validated Pydantic instance

# Also works directly on the model:
msg = await llm.buffer(messages, output_type=Forecast)
```

### MCP

```python
tools = await ai.mcp.get_http_tools("https://mcp.example.com/mcp", headers={...}, tool_prefix="docs")
tools = await ai.mcp.get_stdio_tools("npx", "-y", "@anthropic/mcp-server-filesystem", "/tmp", tool_prefix="fs")
```

Returns `Tool` objects usable in `stream_step`/`stream_loop`. Connections are pooled per `ai.run()` and cleaned up automatically.

### Telemetry

```python
ai.telemetry.enable()  # OTel-based, emits gen_ai.* spans for runs/steps/tools
```
