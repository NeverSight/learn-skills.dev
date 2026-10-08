---
name: ag2-testing
description: Test AG2 agents and tools without hitting a real LLM provider. Pass `TestConfig(...)` from `ag2.testing` as the agent's config (or per-`ask`) to mock LLM responses, inject `ToolCallEvent`s to simulate tool execution, and assert success / error paths. Use when the user is writing pytest tests for an Agent or Tool.
license: Apache-2.0
---

# Testing agents and tools

## When to use

Writing tests for code that builds AG2 `Agent`s, custom `@tool` functions, middleware, or response schemas — anywhere you don't want to make real LLM API calls.

## 60-second recipe — mock an LLM response

```python
import pytest
from ag2 import Agent
from ag2.testing import TestConfig

@pytest.mark.asyncio
async def test_mocked_response():
    agent = Agent("test_agent")
    reply = await agent.ask("Hi!", config=TestConfig("This is a mocked response."))
    assert reply.body == "This is a mocked response."
```

`TestConfig(*responses)` replaces the model client. Each positional arg is the mocked response for the next LLM call *within an `ask()`* — strings for text replies, `ToolCallEvent` for tool dispatches. (The cursor is per-`ask()`; see "Multi-turn mock" below for what that means across multiple turns.)

## Simulate a successful tool call

Pass a `ToolCallEvent` first (the model "decides" to call the tool), then the final answer:

```python
import pytest
from ag2 import Agent
from ag2.events import ToolCallEvent
from ag2.testing import TestConfig

@pytest.mark.asyncio
async def test_tool_success():
    def my_tool() -> str:
        return "tool execution result"

    agent = Agent("test_agent", tools=[my_tool])
    config = TestConfig(
        ToolCallEvent(name="my_tool"),
        "final result",
    )
    reply = await agent.ask("Please use my_tool", config=config)
    assert reply.body == "final result"
```

## Test tool error paths

If a tool raises, the exception propagates to `ask()`:

```python
@pytest.mark.asyncio
async def test_tool_raises():
    def failing_tool() -> str:
        raise ValueError("Something went wrong")

    config = TestConfig(
        ToolCallEvent(name="failing_tool"),
        "result",
    )
    agent = Agent("test_agent", config=config, tools=[failing_tool])

    with pytest.raises(ValueError, match="Something went wrong"):
        await agent.ask("Hi!")
```

## Tool not found

If the LLM calls a tool the agent doesn't have, the framework raises `ToolNotFoundError`:

```python
from ag2.exceptions import ToolNotFoundError

@pytest.mark.asyncio
async def test_tool_not_found():
    config = TestConfig(ToolCallEvent(name="unregistered_tool"))
    agent = Agent("test_agent", config=config)
    with pytest.raises(ToolNotFoundError, match="Tool `unregistered_tool` not found"):
        await agent.ask("Hi!")
```

## Useful test patterns

### Override `Depends` dependencies

```python
def get_production_db():
    raise Exception("Do not call in tests!")

@tool
def read_data(db: Annotated[object, Depends(get_production_db)]) -> str:
    return "Data"

agent = Agent("test", tools=[read_data])
agent.dependency_provider.override(get_production_db, lambda: "mock_db")
```

### Override `Inject` dependencies

Just pass `dependencies={...}` to `agent.ask(...)`:

```python
await agent.ask("Read", dependencies={"database_pool": fake_pool})
```

### Capture stream events

```python
from ag2 import MemoryStream
from ag2.events import ToolCallEvent

stream = MemoryStream()
collected: list[ToolCallEvent] = []
stream.where(ToolCallEvent).subscribe(lambda e: collected.append(e))

await agent.ask("Test", stream=stream)
assert collected[0].name == "expected_tool"
```

### Multi-turn mock — the response list is per-`ask()`, not per-conversation

`TestConfig(...)`'s response list is consumed **within a single `ask()`**, across that round's repeated LLM calls — that's why `TestConfig(ToolCallEvent("my_tool"), "final result")` works for a tool-using turn (the LLM emits the tool call, the tool runs, the LLM is called again and gets `"final result"`). Internally, `TestConfig.create()` hands back a fresh client whose iterator starts at `responses[0]`, and that's done once **per `ask()`** — so every new `ask()` (a `reply.ask(...)` chain, or each turn the network adapters / an auto-replying agent drive) **restarts the cursor at the first response**. Listing more responses does *not* let you say "conversational turn 2 differs from turn 1".

For variation across multiple `ask()` calls, either:

- pass a fresh `TestConfig(...)` per turn via the per-`ask()` `config=` override (`await agent.ask("…", config=TestConfig("turn-2 reply"))`), or
- mock the model with a `ToolCallEvent` and put the per-turn logic in a **stateful tool** — a closure or class instance that tracks how many times it's been called and returns accordingly. (Useful when something *other than your test code* drives the turn loop — e.g. a `workflow` / `discussion` channel — so you can't inject a per-turn `config=`.)

## Going deeper

- Source doc: `website/docs/user-guide/testing.mdx`.
- Test markers / async config — repo `pyproject.toml`. Use `@pytest.mark.asyncio` (the project uses pytest-asyncio).
- Streams (for asserting events): `website/docs/user-guide/advanced/stream.mdx`.

## Common pitfalls

- **Forgetting `@pytest.mark.asyncio`** — the test will skip or fail oddly.
- **Mismatched response count** — `TestConfig` runs out of responses if the agent makes more LLM calls than you expect *within one `ask()`* (e.g. tool error → another LLM call); `StopIteration` propagates. Add more positional args or assert the call sequence. (The cursor is per-`ask()`, so the count you need is "LLM calls in one round", not "turns in the conversation" — see *Multi-turn mock* above.)
- **Mocking the LLM but not the tool** — your tool function still runs (and may hit real APIs / disk). Mock the *tool* if you're isolating LLM behaviour, or override its `Depends` to inject test doubles.
- **Asserting on `reply.body` when you set a `response_schema`** — `body` is the raw text. Use `await reply.content()` for the validated value.
- **Sharing `Agent` instances across async tests** — agents carry mutable state (variables, dependencies). Construct fresh agents per test for isolation.
- **Using real provider clients in CI** — wrap the provider config with `TestConfig` per-test or via a fixture; never rely on `OPENAI_API_KEY` etc. being available in test environments.
