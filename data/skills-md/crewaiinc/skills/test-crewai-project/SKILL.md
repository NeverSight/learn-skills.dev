---
name: test-crewai-project
description: "Deterministic, offline testing of CrewAI crews and flows with pytest: a stub BaseLLM (shipped in references/stub_llm.py) that drives text, structured output and tool calls with no API key, asserting on the prompts crewai built, testing guardrails and flow routing, what `crewai test` really does, event listeners for debugging, and the exact tracing/telemetry env var values. Use when writing tests for a crewai project, mocking or stubbing the LLM, writing a custom BaseLLM, seeing `TypeError: ... call() got an unexpected keyword argument 'from_task'`, `ValueError: OPENAI_API_KEY is required` in CI, `TraceGrantError` in pytest, running `crewai test`, adding a BaseEventListener, or setting CREWAI_TRACING_ENABLED / CREWAI_DISABLE_TELEMETRY / OTEL_SDK_DISABLED."
---

# Test a CrewAI Project

How to test crews and flows deterministically, without API keys, and how to debug real runs with events and traces.

Verified against crewai 1.15.22 and 1.15.23 on 2026-10-01.
Live-tested with real LLMs on 2026-10-01.
Run `crewai version` first; if the major/minor differs, re-verify the version-sensitive rows with the `ask-docs` skill.

---

## 1. Why tests need a stub LLM

A real LLM gives different text on every run, costs money, and needs a key. Every Agent without an explicit `llm` resolves to `gpt-4.1-mini` and fails at kickoff with `ValueError: OPENAI_API_KEY is required` when no key is set, so a CI run with no secrets cannot even start. You cannot assert on output you cannot predict.

A stub LLM fixes the responses, so assertions are exact. It keeps every real crewai code path: prompt building, `{placeholder}` interpolation, task context, tool execution, guardrail retries, pydantic conversion and flow routing. It also records every call, so you can assert on the prompts crewai built. That is where most bugs show up: a missing input, a dropped context, a tool that was never listed.

Test in tiers:

| Tier | Needs | What it proves |
|---|---|---|
| Unit: stub LLM, plain pytest | nothing | wiring, prompts, routing, parsing, guardrail logic |
| Guardrail truth tables | nothing | each guardrail accepts and rejects the right outputs |
| Real-model runs (`crewai test`, smoke kickoffs) | provider key, money | prompt quality; mark them `@pytest.mark.credentialed` and run offline suites with `pytest -m "not credentialed"` |

---

## 2. The custom BaseLLM contract in 1.15

`from crewai import BaseLLM`. The only abstract method is `call`. crewai passes `from_task`, `from_agent` and (for structured tasks) `response_model` as keyword arguments, so `call` must accept them.

| | `call` signature | Result |
|---|---|---|
| Bad (the public custom-LLM docs example) | `def call(self, messages, tools=None, callbacks=None, available_functions=None)` | `TypeError: MyLLM.call() got an unexpected keyword argument 'from_task'` at kickoff |
| Good | `def call(self, messages, tools=None, callbacks=None, available_functions=None, from_task=None, from_agent=None, response_model=None, **kwargs)` | runs |

| Requirement | What happens if you skip it |
|---|---|
| Accept `from_task`, `from_agent`, `response_model` (or `**kwargs`) | `TypeError` at the first LLM call |
| Pass a non-empty `model=` (e.g. `MyLLM(model="my-model")`) | `ValidationError` at construction |
| Call `self._emit_call_started_event(...)` / `self._emit_call_completed_event(...)` inside `with llm_call_context():` (from `crewai.llms.base_llm`) | event listeners and traces never see the LLM calls (see section 9) |
| Forward only `role` and `content` if you pass `messages` to a provider SDK | crewai adds `cache_breakpoint: True` to each message; the Anthropic API rejects it with `400 ... messages.0.cache_breakpoint: Extra inputs are not permitted` |
| `supports_function_calling()` returning False | crewai uses the ReAct text loop for tools (`Thought / Action / Action Input`) |
| Return a validated model instance when `response_model` is passed | native providers do this; returning text also works, but see section 6 for how a guardrail then sees `output.pydantic` |

`references/stub_llm.py` implements all of this. Copy it; do not write your own unless you need to.

---

## 3. Set up the test harness

1. Copy `references/stub_llm.py` to `tests/stub_llm.py` in the project.
2. `uv add --dev pytest`, then run tests with `uv run pytest`.
3. Do not run `uv run test` to mean pytest. In a scaffolded crew project `test` is a project script that runs `crewai test` (section 8), which calls a real model.
4. Add `tests/.crewai-test-storage/` to `.gitignore`.

```python
# tests/conftest.py
import os
import socket
from pathlib import Path

# Optional, test-only switches. The AGENTS.md that `crewai create` writes leaves
# turning observability off to the user, so ask before uncommenting them.
# Without them the socket guard below does not cover everything:
# - crewai telemetry is still sent to telemetry.crewai.com when the test process
#   exits, after the guard has been undone;
# - if tracing is on (CREWAI_TRACING_ENABLED=true or tracing=True) and a CrewAI
#   credential exists (CREWAI_USER_PAT, or just a saved `crewai login` on the
#   machine), kickoff requests a trace grant, the guard refuses it, and the test
#   fails with TraceGrantError.
# If uncommented, they must run before crewai is imported; never put them in the project's .env.
# os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
# os.environ["CREWAI_TRACING_ENABLED"] = "false"
# os.environ["OTEL_SDK_DISABLED"] = "true"
# Absolute path: crewai's SQLite files and memory store go here instead of your user data dir.
os.environ["CREWAI_STORAGE_DIR"] = str(Path(__file__).parent / ".crewai-test-storage")

import pytest


@pytest.fixture(autouse=True)
def offline(monkeypatch, tmp_path):
    def refuse(*args, **kwargs):
        raise RuntimeError("test tried to use the network")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.chdir(tmp_path)  # output_file= and flow file writes land in a temp dir
```

Why each line:

- `import crewai` alone creates `<platform user data dir>/<cwd name>/`. On macOS that is `~/Library/Application Support/<cwd name>/`. Kickoffs write SQLite files there. An absolute `CREWAI_STORAGE_DIR` set before the import redirects all of it.
- The socket guard turns any accidental real-LLM call into an immediate failure instead of a hang or a bill.
- crewai's own internals emit `DeprecationWarning`s on every kickoff. To quiet them:

```toml
# pyproject.toml
[tool.pytest.ini_options]
filterwarnings = ["ignore::DeprecationWarning:crewai.*"]
```

---

## 4. Driving the stub

`StubLLM` picks each response from three sources, in this order:

| Source | Use for |
|---|---|
| `responses=[...]` | One item per LLM call, in call order. An item is a str, a dict/list (sent as JSON), a pydantic model, or `f(messages, response_model)` |
| `responder=f(messages, response_model)` | Used once the queue runs out. Decide by prompt content or schema instead of by call order |
| `default_response="..."` | Used after both. If you leave it unset and crewai asked for a `response_model`, the stub returns a skeleton JSON of that model |

Tool calls go through the ReAct loop. `tool_call(name, args)` builds the `Thought/Action/Action Input` text. The real tool `_run` executes, and its result comes back to the next LLM call as `Observation: ...`.

```python
# tests/test_structured_and_tools.py
from pydantic import BaseModel

from crewai import Agent, Crew, Task
from crewai.tools import tool
from stub_llm import StubLLM, prompt_text, tool_call


class Brief(BaseModel):
    title: str
    bullets: list[str]


tool_inputs = []


@tool("Word Counter")
def word_counter(text: str) -> int:
    """Count the words in a piece of text."""
    tool_inputs.append(text)
    return len(text.split())


def test_tool_call_then_structured_answer():
    llm = StubLLM(responses=[
        tool_call("Word Counter", {"text": "bees make honey"}),  # researcher: use the tool
        "Final Answer: 3 words",                                 # researcher: answer
        {"title": "Bees", "bullets": ["honey"]},                 # writer: JSON for Brief
    ])
    researcher = Agent(role="Researcher", goal="Count words", backstory="Careful.",
                       tools=[word_counter], llm=llm)
    writer = Agent(role="Writer", goal="Write briefs", backstory="Concise.", llm=llm)
    count = Task(description="Count the words", expected_output="A count", agent=researcher)
    brief = Task(description="Write a brief", expected_output="Title and bullets",
                 agent=writer, output_pydantic=Brief)

    out = Crew(agents=[researcher, writer], tasks=[count, brief]).kickoff()

    assert tool_inputs == ["bees make honey"]               # the real tool ran
    assert "Observation: 3" in prompt_text(llm.calls[1])    # its result went back to the LLM
    assert llm.calls[0]["response_model"] is None           # agents WITH tools get no response_model
    assert llm.calls[2]["response_model"] is Brief
    assert out.pydantic == Brief(title="Bees", bullets=["honey"])
```

Rules that keep stub tests stable:

| Rule | Why |
|---|---|
| Queue valid JSON (a dict) for every `output_pydantic` / `output_json` task | An unparseable answer makes crewai spend extra converter LLM calls, which eat later queue items, and then it raises `ConverterError` |
| `output_pydantic` is what fills `out.pydantic` | `Task(response_model=X)` alone sends the schema to the LLM but leaves `out.pydantic` as `None` |
| Count calls with `len(llm.calls)`, not `out.token_usage` | Crew usage is summed per agent over each LLM object's lifetime: one stub shared by 2 agents is counted twice, and a stub reused for a second crew carries the first crew's tokens |
| When the call order is hard to predict, use `responder` and decide on `response_model` or prompt text | A queue only works if you know the exact call order |
| Build a fresh crew for `kickoff_for_each` | On a crew that was already kicked off, every item silently reuses the previous kickoff's inputs |

---

## 5. Testing a crew and asserting on prompts

Make the LLM injectable. For a factory function, take `llm=None` and pass it to every Agent (None means crewai's default model in production). For a scaffolded `@CrewBase` class, swap the LLM after `.crew()`:

```python
# tests/test_crew.py
from pathlib import Path

from acme_research.crew import AcmeResearch
from stub_llm import StubLLM, prompt_text


def crew_with(llm):
    crew = AcmeResearch().crew()
    for agent in crew.agents:
        agent.llm = llm
    return crew


def test_research_crew_output_and_prompts():
    llm = StubLLM(responses=["- bees pollinate crops", "# Bees report"])
    out = crew_with(llm).kickoff(inputs={"topic": "bees", "current_year": "2026"})

    assert out.raw == "# Bees report"
    assert [t.raw for t in out.tasks_output] == ["- bees pollinate crops", "# Bees report"]
    assert len(llm.calls) == 2

    first = prompt_text(llm.calls[0])
    assert "bees Senior Data Researcher" in first                   # {topic} filled in agents.yaml
    assert "the current year is 2026" in first                      # {current_year} in tasks.yaml
    assert "- bees pollinate crops" in prompt_text(llm.calls[1])    # task 1 output is task 2 context
    assert Path("report.md").read_text() == "# Bees report"         # output_file, in tmp cwd
```

`llm.calls[i]` holds `messages` (a snapshot of the system+user messages crewai sent), `response_model`, `tools` and `response`. `prompt_text(call)` joins the message contents. Useful things to assert on:

| Assert | Catches |
|---|---|
| An input value appears in the prompt | a kickoff with no `inputs` (the literal `{topic}` stays in the prompt; a dict that misses one key raises `ValueError` instead) |
| The previous task's output appears in the next prompt | broken `context=` |
| `Tool Name: <snake_case name>` appears | a tool not attached. `@tool("Word Counter")` renders as `word_counter`; `Action: Word Counter` still resolves |
| The guardrail error appears in the retry prompt | a guardrail whose feedback never reaches the model |
| `llm.calls == []` on a branch | a flow branch that should not call the model |

---

## 6. Testing guardrails

A function guardrail returns `(True, value)` to accept or `(False, "error for the LLM")` to reject. Test it two ways: as a plain function over a truth table of outputs, and inside a crew to check the retry. A guardrail that keeps failing raises `Task failed guardrail validation after N retries` after `guardrail_max_retries` retries (default 3). The truth-table and give-up tests are in [example-tests.md](references/example-tests.md) section 1.

```python
# tests/test_guardrails.py
from pydantic import BaseModel

from crewai import Agent, Crew, Task
from crewai.tasks.task_output import TaskOutput
from stub_llm import StubLLM, prompt_text


class Brief(BaseModel):
    title: str
    bullets: list[str]


def max_three_bullets(output: TaskOutput):
    try:  # output.pydantic can be None here, so fall back to parsing raw
        brief = output.pydantic or Brief.model_validate_json(output.raw)
    except ValueError:
        return (False, "Return JSON matching the Brief schema.")
    if len(brief.bullets) > 3:
        return (False, f"Use at most 3 bullets, you used {len(brief.bullets)}.")
    return (True, output.raw)  # a string: crewai re-runs the pydantic conversion


def brief_crew(llm):
    writer = Agent(role="Writer", goal="Write briefs", backstory="Concise.", llm=llm)
    task = Task(description="Write a brief", expected_output="Title and up to 3 bullets",
                agent=writer, output_pydantic=Brief,
                guardrail=max_three_bullets, guardrail_max_retries=2)
    return Crew(agents=[writer], tasks=[task])


def test_retry_feeds_the_error_back():
    llm = StubLLM(responses=[{"title": "T", "bullets": ["a", "b", "c", "d"]},
                             {"title": "T", "bullets": ["a"]}])
    out = brief_crew(llm).kickoff()
    assert out.pydantic == Brief(title="T", bullets=["a"])
    assert "Use at most 3 bullets, you used 4." in prompt_text(llm.calls[1])
```

Two traps:

- **`output.pydantic` may be `None` inside the guardrail.** When a task has a guardrail and the LLM returned text, crewai skips the pydantic conversion before the first guardrail call. An LLM returns text whenever the agent has tools, or when it is a custom LLM that returns strings. Parse `output.raw` yourself.
- **`return (True, output)` can silently lose `out.pydantic`.** If `output.pydantic` was `None`, crewai keeps that TaskOutput as-is. Return `(True, output.raw)` and crewai converts the string. Then assert `out.pydantic is not None` at the boundary.

---

## 7. Testing a flow

Flow methods are plain methods, so call them directly to test one step. Use `kickoff(inputs=...)` to test routing end to end. `kickoff` returns the return value of the last method that ran, and `inputs` keys overwrite state fields before `@start` runs.

```python
# tests/test_flow_routing.py
from pydantic import BaseModel

from crewai.flow import Flow, listen, or_, router, start


class State(BaseModel):
    topic: str = ""
    log: list[str] = []


class TopicFlow(Flow[State]):
    @start()
    def normalize(self):
        self.state.topic = self.state.topic.strip().lower()

    @router(normalize)
    def choose(self):
        return "has_topic" if self.state.topic else "no_topic"  # labels differ from method names

    @listen("has_topic")
    def research(self):
        self.state.log.append("research")

    @listen("no_topic")
    def skip(self):
        self.state.log.append("skip")

    @listen(or_(research, skip))
    def finish(self):
        return f"done:{self.state.topic or '-'}"


def test_step_directly():
    flow = TopicFlow()
    flow.state.topic = "  Bees "
    flow.normalize()
    assert flow.state.topic == "bees"
    assert flow.choose() == "has_topic"


def test_both_branches_via_kickoff():
    flow = TopicFlow()
    assert flow.kickoff(inputs={"topic": " Bees "}) == "done:bees"
    assert flow.state.log == ["research"]

    flow = TopicFlow()
    assert flow.kickoff(inputs={"topic": "   "}) == "done:-"
    assert flow.state.log == ["skip"]
```

When a flow step builds a crew itself, as the `crewai create flow` scaffold does with `ContentCrew().crew()`, there is no parameter to pass a stub through. `monkeypatch.setattr` the crew class's `crew` method with a wrapper that calls the original and then sets `agent.llm = stub` on every agent. The full test is in [example-tests.md](references/example-tests.md) section 2.

`Flow` is a pydantic model. If you own the flow code, declaring `llm: Any = None` on the flow class and passing `MyFlow(llm=stub)` is a cleaner seam than patching. A `@listen("x")` on a method named `x` raises when the flow is instantiated, so a test that only builds the flow catches it.

---

## 8. What `crewai test` actually does

`crewai test` is a model-graded evaluation, not a unit-test runner.

| Fact | Detail |
|---|---|
| What it runs | `uv run test <n> <model>`, i.e. the project's `main.test()`, which calls `Crew.test(n_iterations, eval_llm=model, inputs=...)` |
| Defaults | `-n 3`, `-m gpt-5.4-mini` (older docs say 2 and `gpt-4o-mini`) |
| Judge model | `-m` takes any provider string, although `--help` says only OpenAI models: `crewai test -m anthropic/claude-haiku-4-5` works when the project has the provider extra (`uv add "crewai[anthropic]"`) |
| Each iteration | a full real kickoff of the crew with its own LLMs, plus one judge call per task |
| Scoring | an evaluator agent driven by the `-m` model scores every task from 1 to 10 and prints a `Tasks/Crew/Agents` table: one row per task, a `Crew` row, `Execution Time (s)`, one column per run and `Avg. Total` |
| Needs | keys for the crew's model AND the judge model. The judge runs after the first task, so that task has already run (and billed) when a missing judge key fails: `An error occurred while testing the crew: OPENAI_API_KEY is required`, or `Error code: 401` for an invalid key |
| Exit code | `0` even when the run fails, so CI cannot rely on it |
| Side effects | it replaces each task's `callback` on the copy of the crew it runs; logs `Sync handler error in on_crew_test_result` once per task score, which does not fail the run |
| Flow projects | the flow scaffold has no `test` script, so `uv run test` hits the shell's `test` builtin: `test: 1: unexpected operator` |

Use it for a periodic prompt-quality check against a real model. Do not use it as CI, because it costs money and its scores are not deterministic. `Crew.test` accepts a `BaseLLM` as `eval_llm`, so with stubs for both the crew and the judge it runs offline. That checks only the wiring ([example-tests.md](references/example-tests.md) section 4).

---

## 9. Event listeners for debugging

Every kickoff emits typed events on `crewai_event_bus`: crew, task, agent, LLM call, tool, flow and memory events. Import them from `crewai.events`. `crewai.utilities.events` no longer exists.

Subclass `BaseEventListener`, implement `setup_listeners(self, bus)`, and register handlers inside it with `@bus.on(EventClass)`. Each handler has the signature `handler(source, event)`. Instantiating the listener registers its handlers. [example-tests.md](references/example-tests.md) section 3 has a debug listener (`ToolUsageFinishedEvent`, `LLMCallCompletedEvent`, `TaskFailedEvent`) and a recorder test.

In tests, register listeners inside `with crewai_event_bus.scoped_handlers():` so they are removed afterwards. Call `crewai_event_bus.flush()` before asserting, because handlers run on worker threads.

- To debug a real run, put the listener in its own module and import it from `main.py`, so it is instantiated once. Other useful events: `LLMCallFailedEvent`, `MemorySaveFailedEvent`, `CrewKickoffStartedEvent`, `FlowFinishedEvent`.
- `LLMCallCompletedEvent.response` is the text, or for a native tool call the provider's list of tool-use blocks. `event.model` and `event.usage` carry the model and token counts.
- **A custom `BaseLLM` must emit its own LLM call events.** The built-in providers emit `LLMCallStartedEvent` / `LLMCallCompletedEvent`. A subclass that only returns text emits nothing, and the trace listener subscribes to the same events, so listeners and traces both miss every LLM call.

---

## 10. Tracing and telemetry switches

They are two separate systems. **Telemetry** is anonymous usage stats sent to CrewAI. **Tracing** is the execution trace (prompts, inputs, outputs, tool calls) you view in CrewAI AMP.

| Variable | Accepted values (1.15.22-1.15.23) | Effect |
|---|---|---|
| `CREWAI_DISABLE_TELEMETRY` | `true`, `1`, `yes`, `on` (any case, trimmed) disable. `false`, `0`, `no`, `off`, empty leave it on. Anything else is ignored with a warning | turns off CrewAI telemetry |
| `CREWAI_DISABLE_TRACKING` | same as above | turns off CrewAI telemetry |
| `OTEL_SDK_DISABLED` | the same set disables CrewAI telemetry. Only `true` (any case) also blocks execution tracing and disables the OpenTelemetry SDK itself | `1` is not a full kill switch |
| `CREWAI_TRACING_ENABLED` | `true` / `1` force tracing on. `false` / `0` force it off. `yes`, `on`, `no`, `off` are **ignored** and fall through to saved consent | per-process tracing gate |
| `tracing=True/False` on `Crew(...)` or `Flow` | bool | beats the env var |

Tracing precedence: the `tracing=` argument, then `CREWAI_TRACING_ENABLED`, then the consent saved by `crewai traces enable|disable`. Saved consent is stored per project directory name (or per `CREWAI_STORAGE_DIR`), so renaming the checkout resets it. `crewai traces status` shows the env var (`false` when unset) and the saved consent, not whether you are logged in.

Rules:

- **Disable observability only in tests, and only when the user chooses to.** Put the switches in `tests/conftest.py` or the CI test job's environment. Never put them in the project's `.env`, `main.py`, or a deployment's env vars, because that blinds production debugging.
- Spell the values `true` / `false`. `true` is the only spelling every disable switch fully honors, and `CREWAI_TRACING_ENABLED` ignores `yes`/`no`/`on`/`off`.
- To debug one run, use `CREWAI_TRACING_ENABLED=true crewai run` or `tracing=True`. Where the trace goes depends on whether a CrewAI credential exists: `CREWAI_USER_PAT`, or a saved `crewai login` (no PAT needed).
  - **With a credential:** kickoff first requests a trace grant, then uploads the trace to CrewAI AMP under that login, with or without a terminal. 1.15.23 then prints a `View traces:` link; 1.15.22 prints none. If the grant request fails, kickoff raises `TraceGrantError` before the crew runs.
  - **Without a credential, 1.15.23, interactive terminal:** turning tracing on counts as consent. The trace uploads as an ephemeral trace with no prompt and an `Ephemeral Execution Traces` link is printed. Nothing is saved as consent.
  - **Without a credential, 1.15.22, interactive terminal:** crewai asks `Share this execution trace with CrewAI? [y/N]` after the run.
  - **Without a credential, no terminal (CI, pytest, `< /dev/null`):** the trace is discarded, on both releases.
  - **No switch at all, first run:** crewai auto-collects locally, asks `Share this execution trace with CrewAI? [y/N] (20s timeout)` in a terminal, and saves the answer as consent.
- From 1.15.23, crewai wraps every `BaseLLM` subclass's `call` in a rate-limit retry: a stub that raises an error mentioning "rate limit" or 429 is called 3 times over about 3 s before the error surfaces. To test your own rate-limit handling, raise a different error type, or assert on the retried call count.
- Traces contain task text, inputs and outputs. Use synthetic data in traced runs unless your data may leave the machine.

---

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `TypeError: ... call() got an unexpected keyword argument 'from_task'` | custom LLM copied from the docs example signature | accept `from_task`, `from_agent`, `response_model`, `**kwargs` |
| `ValueError: OPENAI_API_KEY is required` in CI | an agent kept the default `gpt-4.1-mini` | inject the stub into every agent (section 5) |
| Test hangs or bills an account | a real LLM call slipped through | the socket guard in `conftest.py` |
| `uv run test` calls OpenAI | `test` is the scaffold's `crewai test` script | `uv run pytest` |
| Queue answers land on the wrong task | an extra converter call or guardrail retry consumed one | queue valid JSON; use `responder` keyed on `response_model` |
| `out.pydantic is None`, run "succeeded" | `response_model=` without `output_pydantic=`, or the guardrail returned `(True, output)` | use `output_pydantic`; guardrails return `(True, output.raw)`; assert not None |
| Guardrail rejects valid JSON on the first try | it read `output.pydantic`, which was None | parse `output.raw` |
| Listener or trace shows no LLM calls | custom LLM does not emit events | emit them inside `llm_call_context()` (the stub does) |
| Listener counts grow across tests | handlers registered globally | `crewai_event_bus.scoped_handlers()` + `flush()` |
| `token_usage` is double the call count, or grows from test to test | one LLM instance shared by several agents, or reused across crews | a fresh stub per crew; assert on `len(llm.calls)` |
| New dirs under the user data dir after tests | `CREWAI_STORAGE_DIR` unset at import time | set it to an absolute path at the top of `conftest.py` |
| `TraceGrantError: AMP trace grant request failed (RuntimeError)` in pytest | tracing on + a saved `crewai login` or `CREWAI_USER_PAT` + the socket guard | `CREWAI_TRACING_ENABLED=false` in `conftest.py` (tests only) |
| `crewai test` "passed" in CI but scored nothing | it exits 0 even when the run fails | check its output for the score table |
| Tracing still runs with `OTEL_SDK_DISABLED=1` | `1` disables telemetry only; only `true` also blocks tracing | `CREWAI_TRACING_ENABLED=false` (tests only) |

---

## Checklist

- [ ] `tests/stub_llm.py` copied from `references/stub_llm.py`; pytest added as a dev dependency
- [ ] `conftest.py` sets an absolute `CREWAI_STORAGE_DIR` before importing crewai and blocks the network; the observability switches are uncommented only if the user chose them
- [ ] Every agent's LLM is injectable (factory parameter, swap after `.crew()`, or patched crew class)
- [ ] Each structured task gets valid JSON from the stub, and tests assert `out.pydantic is not None`
- [ ] At least one test asserts on prompt text (inputs, context, tool listing)
- [ ] Each guardrail has a truth-table test plus a retry test
- [ ] Each flow router branch has a kickoff test; key steps are also called directly
- [ ] Real-model tests are marked `credentialed` and excluded from default CI
- [ ] Observability switches appear only in test config, never in `.env` or deployment env vars

---

## References

- [stub_llm.py](references/stub_llm.py) - the offline deterministic `StubLLM`, plus `tool_call()` and `prompt_text()` helpers. Copy into `tests/`.
- [Example tests](references/example-tests.md) - guardrail truth tables and retry exhaustion, a scaffolded flow that builds its crew inside a step, an event-listener test, and an offline `Crew.test` wiring check
- Public docs: https://docs.crewai.com/en/concepts/event-listener, https://docs.crewai.com/en/observability/tracing, https://docs.crewai.com/en/telemetry

For related skills:

- **check-crewai-api** - current Agent/Task/Crew API, structured output fields, guardrail contract
- **build-flow** - flow state, routers, `or_`/`and_`, persistence
- **connect-tools-and-mcp** - building the tools your stub drives
- **design-task** - writing guardrails and expected_output worth testing
- **ask-docs** - query the live docs when a version-sensitive row may have changed
