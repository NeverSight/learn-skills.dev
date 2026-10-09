---
name: build-flow
description: "Building CrewAI Flows on crewai 1.15.x: structured (Pydantic) vs dict state and state.id, @start/@listen/@router wiring, or_/and_ semantics, router labels vs method names, @persist (correct import, where it stores state, restore_from_state_id), checkpointing with CheckpointConfig, @human_feedback and HumanFeedbackResult.feedback, plot(), calling crews and agents from flow methods, kickoff inputs, and the `crewai create flow` scaffold. Use when writing or debugging a Flow subclass or main.py with `from crewai.flow import ...`, when a listener never fires or fires twice, or when you see errors like \"listen condition 'x' references the handler name 'x'\", \"cannot import name 'persist'\", \"'StateWithId' object is not subscriptable\", \"Flow state model must have an 'id' field\", \"--inputs requires a declarative flow definition\", \"invoked synchronously from within a running event loop\", or HumanFeedbackCollapseError."
---

# Build a CrewAI Flow

How to write a Flow that wires correctly, keeps typed state, persists and resumes, and calls crews and agents, on the current API.

Verified against crewai 1.15.22 and 1.15.23 on 2026-10-01.
Live-tested on CrewAI AMP and real LLMs on 2026-10-01.
Run `crewai version` first; if the major/minor differs from 1.15, re-verify version-sensitive rows with the `ask-docs` skill before trusting them.

---

## 1. Scaffold and run a flow project

```bash
crewai create flow lead-router      # the package is still lead_router
cd lead_router
crewai install                      # uv sync; writes uv.lock
crewai run                          # runs the `kickoff` script in pyproject.toml
crewai flow plot                    # runs the `plot` script
```

What the scaffold gives you:

| File | Contents |
|---|---|
| `pyproject.toml` | `[project.scripts]` `kickoff`, `run_crew` (both `<pkg>.main:kickoff`), `plot`, `run_with_trigger`; `[tool.crewai] type = "flow"` |
| `src/<pkg>/main.py` | A `Flow[ContentState]` subclass plus `kickoff()` and `plot()` functions; `from crewai.flow import Flow, listen, start` |
| `src/<pkg>/crews/content_crew/` | A classic `@CrewBase` crew with `config/agents.yaml` and `config/tasks.yaml`; its agents set no `llm`, so they use the default OpenAI model |
| `.env` | `OPENAI_API_KEY=YOUR_API_KEY` - a placeholder; a run with it fails with `401 ... Incorrect API key provided`. An `OPENAI_API_KEY` exported in the shell takes precedence over `.env`: with a valid key exported, the unmodified scaffold's `crewai run` ran its three agents on `gpt-4.1-mini` and wrote `output/post.md` |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` (plus `CURSOR.md` from 1.15.23), `README.md`, `tests/` | Coding-assistant instructions and an empty tests folder |
| `.git/` | `crewai create` runs `git init` (no commit, no remote) |

To use another provider, set `llm: anthropic/claude-haiku-4-5` (for example) on each agent in `agents.yaml`, run `uv add "crewai[anthropic]"`, and put `ANTHROPIC_API_KEY=<your-key>` in `.env` - `crewai run` read the key from `.env` with nothing exported in the shell.

Rules the scaffold implies:

- Keep `[tool.crewai] type = "flow"`. The CLI uses it to decide that `crewai run` means `uv run kickoff`.
- The template's `plan_content()` overwrites `self.state.topic` with `"AI Agents"` unless a trigger payload is present, so `kickoff(inputs={"topic": ...})` (and a deployed kickoff's `inputs`) is ignored. Delete that assignment before relying on inputs.
- The template's `plot()` calls `plot()` with the default `show=True`, so `crewai flow plot` opens a browser. Change it to `plot("<name>.html", show=False)` for headless use.
- Import with the absolute package path (`from lead_router.crews.content_crew.content_crew import ContentCrew`), as the template does.
- `kickoff()` in `main.py` must return `None`. The generated console script does `sys.exit(kickoff())`, so returning the flow result (a dict, say) makes the process exit with status 1 and prints the value to stderr, and `crewai run` prints "An error occurred while running the flow" - yet `crewai run` itself still exits 0, so a CI step that only checks its exit code passes.
- `crewai run --inputs '{...}'` is rejected for a Python flow: `Error: --inputs requires a declarative flow definition ([tool.crewai].definition) or --definition`. Pass inputs in code (`flow.kickoff(inputs=...)`), or read them from `sys.argv` in your `kickoff()` and call `uv run kickoff '<json>'`.
- `crewai flow kickoff` still works but prints "deprecated. Use 'crewai run' instead."
- A placeholder or invalid key makes the flow fail, yet `crewai run` still exits 0 (it prints `An error occurred while running the flow: Command '['uv', 'run', 'kickoff']' returned non-zero exit status 1.`). Check for that line, not the exit code.

---

## 2. State: structured or dict

| | Structured (recommended) | Unstructured |
|---|---|---|
| Declare | `class MyFlow(Flow[MyState])` with `MyState(BaseModel)` | `class MyFlow(Flow)` |
| Access | `self.state.topic` | `self.state["topic"]` |
| `id` | Added for you (`self.state.id`, a UUID string) | `self.state["id"]` |
| Validation | `kickoff(inputs=...)` values are type-checked | none |

```python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start


class ReportState(BaseModel):
    topic: str = ""          # give every field a default
    draft: str = ""
    notes: list[str] = []


class ReportFlow(Flow[ReportState]):
    @start()
    def plan(self):
        self.state.notes.append(f"planning {self.state.topic}")
        return self.state.topic.upper()

    @listen(plan)
    def write(self, plan_output):          # receives plan()'s return value
        self.state.draft = f"Draft about {plan_output}"
        return self.state.draft


flow = ReportFlow()
result = flow.kickoff(inputs={"topic": "bees"})   # inputs set state BEFORE @start runs
print(result)           # "Draft about BEES" - kickoff returns the last method's output
print(flow.state.id)    # UUID string, generated per run
```

State rules (each one prevents a real failure):

| Rule | What happens if you break it |
|---|---|
| Do not declare `id` on your model; `Flow[MyState]` adds it | A declared `id` default is silently replaced by a generated UUID |
| Use `Flow[MyState]`, not `initial_state = MyState` | `initial_state` with a plain `BaseModel`: `ValidationError ... Flow state model must have an 'id' field` |
| Give every field a default | A required field: `ValidationError` when the flow is instantiated, before `kickoff` |
| Use attribute access on structured state | `self.state["topic"]`: `TypeError: 'StateWithId' object is not subscriptable` |
| Spell `inputs` keys exactly like the model fields | Unknown keys are **silently dropped** on structured state |
| Pass `inputs` of the right type | `inputs={"topic": 5}`: `ValueError: Invalid inputs for structured state` |
| Never set `self.state.id` by hand | It is the persistence key; use `restore_from_state_id` (section 6) |

On a deployed flow (tested on CrewAI AMP, 2026-10-01), `GET /inputs` lists the state model's declared fields (the generated `id` is not listed; a model that declares `id` itself gets it listed too), and the `inputs` object of `POST /kickoff` is applied to state exactly like `kickoff(inputs=...)`. A body without the `inputs` wrapper (`{"text": "..."}`) was still accepted (`200` and a `kickoff_id`) and the run succeeded on default state - the value never reached the flow. The run's `state.id` equalled its `kickoff_id`. Calling patterns: the **call-deployed-crew** skill.

---

## 3. Wiring: `@start`, `@listen`, `@router`

```python
from typing import Literal
from pydantic import BaseModel
from crewai.flow import Flow, listen, router, start


class TicketState(BaseModel):
    text: str = ""
    queue: str = ""


class TicketFlow(Flow[TicketState]):
    @start()
    def receive(self):
        return self.state.text

    @router(receive)
    def triage(self) -> Literal["urgent", "normal"]:   # labels, not method names
        return "urgent" if "outage" in self.state.text else "normal"

    @listen("urgent")
    def page_oncall(self):
        self.state.queue = "oncall"

    @listen("normal")
    def file_ticket(self):
        self.state.queue = "backlog"


flow = TicketFlow()
flow.kickoff(inputs={"text": "outage in eu-west"})
print(flow.state.queue)   # oncall
```

| Rule | Why |
|---|---|
| A router label must not equal the name of the method that listens for it | `@listen("go") def go` raises at instantiation: `Invalid flow definition for ...: methods.go.listen listen condition 'go' references the handler name 'go'. A listener triggered by its own completion creates an infinite loop.` Labels and method names share one namespace |
| Pick labels that match no method name at all | A label is just an event name, and so is every method name. A router that returns the name of the method that triggers it re-runs that branch until `RecursionError: Method 'r' has been called 100 times in this flow execution` |
| Make sure every label the router can return has a listener | An unmatched label ends the flow silently; `kickoff()` returns the label string itself |
| Declare labels with a `Literal[...]` return type or `@router(x, emit=[...])` | Only for `plot()` edges and static checks; `emit=` is not enforced at runtime (a router returning a label outside `emit` still ran) |
| `@listen(method_ref)` is safer than `@listen("method_name")` | A typo in a string is just an event nobody emits |

---

## 4. `or_` and `and_`

```python
from crewai.flow import Flow, and_, listen, or_, start

calls = []


class FanIn(Flow):
    @start()
    def fetch_a(self):
        return "A"

    @start()
    def fetch_b(self):
        return "B"

    @listen(or_(fetch_a, fetch_b))
    def first_result(self, value):
        calls.append(("or", value))

    @listen(and_(fetch_a, fetch_b))
    def all_results(self, value):
        calls.append(("and", value))


FanIn().kickoff()
print(calls)   # e.g. [('or', 'A'), ('and', 'B')] - the start methods run concurrently, so the values (and order) can vary
```

- **`or_` fires once per kickoff**, on the first condition to complete. It does not run again when the second one completes, so you do not need a "seen" flag.
- `or_` re-arms when a router emits one of its labels again. That is what makes a revision loop work (`@listen(or_(write_draft, "needs_revision"))` runs on the first draft and again on every `needs_revision`; see [routing-patterns](references/routing-patterns.md)).
- Do not let a separate revise step listen to the same label as the review step: two `@listen("needs_revision")` methods run in parallel on that label, so the review re-checks the unrevised draft (verified on 1.15.22 and 1.15.23: three reviews all saw `v1`). Make the revise step a router that returns a new label (`@router("needs_revision") def revise(...): ...; return "revised"`) and have the review listen to `or_(write_draft, "revised")`.
- **`and_` fires once, after all conditions complete**, and receives the output of the last one to finish. Read the others from `self.state`.
- A typical join after a router: `@listen(or_(page_oncall, file_ticket))` runs exactly once, whichever branch ran.

---

## 5. Calling crews and agents from flow methods

```python
from crewai import Agent, Crew, Task
from crewai.flow import Flow, listen, start


class ResearchFlow(Flow):
    @start()
    def research(self):
        researcher = Agent(role="Researcher", goal="Research {topic}",
                           backstory="You find facts.", llm="openai/gpt-4o-mini")
        task = Task(description="List three facts about {topic}.",
                    expected_output="Three bullets.", agent=researcher)
        out = Crew(agents=[researcher], tasks=[task]).kickoff(inputs={"topic": "bees"})
        return out.raw                       # CrewOutput: .raw .pydantic .json_dict

    @listen(research)
    def summarize(self, facts):
        writer = Agent(role="Writer", goal="Summarize", backstory="Concise.",
                       llm="openai/gpt-4o-mini")
        return writer.kickoff(f"One sentence summary: {facts}").raw   # LiteAgentOutput
```

| Method kind | Call | Wrong form |
|---|---|---|
| `def` | `crew.kickoff(inputs=...)`, `agent.kickoff(...)` | - |
| `async def` | `await crew.akickoff(inputs=...)` | `crew.kickoff()` inside `async def`: `RuntimeError: Agent execution was invoked synchronously from within a running event loop` |

- Under `await crew.akickoff()`, an agent's `mcps=["https://..."]` string refs resolve to **zero tools with no error** (they need to start their own event loop). Use `MCPServerHTTP(url=...)` from `crewai.mcp` in async methods; details in the **connect-tools-and-mcp** skill.
- Crew `{placeholders}` are filled from the crew's own `kickoff(inputs=...)`, not from flow state. A crew kicked off with no inputs sends the literal `{topic}` to the LLM. Pass the state values you need explicitly.
- Build the crew inside the method (or call `MyCrew().crew()` from a `@CrewBase` class each time), so each run gets fresh objects.
- Flow methods are plain methods: `ReportFlow().plan()` can be called directly in a unit test.

---

## 6. Persistence with `@persist`

```python
from pydantic import BaseModel
from crewai.flow import Flow, persist, start   # or: from crewai.flow.persistence import persist


class CounterState(BaseModel):
    count: int = 0


@persist()                      # class level: state saved after every method
class CounterFlow(Flow[CounterState]):
    @start()
    def bump(self):
        self.state.count += 1
        return self.state.count


first = CounterFlow()
first.kickoff()                                        # count == 1
second = CounterFlow()
second.kickoff(restore_from_state_id=first.state.id)   # count == 2
print(second.state.id != first.state.id)               # True: a fork with a new id
```

| You want | Do | Not |
|---|---|---|
| Import | `from crewai.flow import persist` or `from crewai.flow.persistence import persist` | `from crewai.flow.flow import persist` (ImportError) |
| Decorate | `@persist()` - always with parentheses | Bare `@persist` on a class: the class is replaced by a function and instantiating it raises `TypeError: persist.<locals>.decorator() missing 1 required positional argument: 'target'`. Bare `@persist` on a method: **no error at all** - the method body never runs, `kickoff()` returns the flow object, nothing is saved |
| Seed a new run from a saved state | `kickoff(restore_from_state_id=sid)` - hydrates, then writes under a fresh `state.id` | `kickoff(inputs={"id": sid})` - deprecated; resumes under the same id and gives no warning |
| Save only at a checkpoint-worthy step | `@persist()` on that method (stack it above `@listen`) | Class-level when you only need the final state |
| Change some fields on the restored run | Pass them in `inputs` with `restore_from_state_id`; inputs are applied after hydration | Editing the SQLite file |

Where it stores state, and the silent cases:

- Default backend: `SQLiteFlowPersistence`, file `flow_states.db` in `appdirs.user_data_dir(<CREWAI_STORAGE_DIR or current dir name>, "CrewAI")` - on macOS `~/Library/Application Support/<name>/`, on Linux `~/.local/share/<name>/`. Set `CREWAI_STORAGE_DIR` to an **absolute path** and the file lands directly in that directory. Or pass a path: `@persist(SQLiteFlowPersistence("/abs/path/flows.db"))`.
- An unknown `restore_from_state_id` does not raise: it logs "No flow state found ... proceeding without hydration" and runs from defaults.
- `restore_from_state_id` on a flow **without** `@persist` is ignored silently.
- Locally `@persist` is a SQLite file. For durable state you control, implement `FlowPersistence` against your own database ([persistence-and-checkpoints](references/persistence-and-checkpoints.md)).

On CrewAI AMP (tested 2026-10-01 with a class-level `@persist()` flow deployed by ZIP upload), send the id as a top-level `restoreFromStateId` beside `inputs` in `POST /kickoff`:

| Kickoff body | Observed |
|---|---|
| `{"inputs": {...}, "restoreFromStateId": "<state_id>"}` | State restored (counter and list carried over, fields not in `inputs` kept), `inputs` applied on top, new `state.id` (= the new `kickoff_id`) |
| Same, after two `crewai deploy push` redeploys | Still restored - the saved state survived the redeploys |
| `restoreFromStateId` that matches nothing | No error; the run starts from defaults |
| `{"inputs": {"id": "<state_id>", ...}}` (deprecated) | Restored and kept the **old** `state.id`, which then differs from the `kickoff_id` |

Return `self.state.id` from the last method (or read the `kickoff_id`) so callers have the id to restore from.

---

## 7. Checkpointing (resume after a crash)

Checkpoints are separate from `@persist`: they snapshot the run (state, completed methods, outputs) to files so a failed run can continue.

```python
from crewai import CheckpointConfig
from crewai.flow import Flow, listen, start


class EtlFlow(Flow):
    @start()
    def extract(self):
        return "rows"

    @listen(extract)
    def load(self, rows):
        return f"loaded {rows}"


flow = EtlFlow(checkpoint=CheckpointConfig(
    location="./.checkpoints",
    on_events=["method_execution_finished"],   # required for flows, see below
))
flow.kickoff()
```

Resume: `EtlFlow().kickoff(from_checkpoint=CheckpointConfig(restore_from="./.checkpoints/<branch>/<file>.json"))`. Completed methods are skipped. To change state before continuing (for example to clear a flag that caused the failure), use `flow = EtlFlow.from_checkpoint(CheckpointConfig(restore_from=path))`, edit `flow.state`, then `flow.kickoff()`.

- **On a Flow, set `on_events=["method_execution_finished"]`.** The default `["task_completed"]` (and `checkpoint=True`) wrote no checkpoint at all for a flow, even one whose method ran a crew.
- Files are written under `location/<branch>/` as `<timestamp>_<id>_p-<parent>.json`, one per finished method. The timestamp has one-second resolution and the id is random, so **sorting file names does not find the latest** when several methods finish in the same second (a sorted list picked the second-to-last). Use `max(files, key=os.path.getmtime)`, or `crewai checkpoint list <location>` (newest first).
- **Resume does not continue past a router.** A checkpoint taken after a `@router` (or a `@human_feedback` method with `emit`) has finished resumes, runs nothing, and returns the router's label (or `None`) with no error - the label's listeners never run. A crash anywhere downstream of a router therefore cannot be resumed from the latest checkpoint; only checkpoints taken before the router finished continue through it. Verified on 1.15.22 and 1.15.23. Keep crash-prone work upstream of routers, or make the downstream steps idempotent and re-run the flow.
- `kickoff(from_checkpoint=..., restore_from_state_id=...)` raises `ValueError: Cannot combine ...`. Pick one system.

---

## 8. Human feedback (`@human_feedback`)

```python
from crewai.flow import Flow, HumanFeedbackResult, human_feedback, listen, start


class ReviewFlow(Flow):
    @start()
    @human_feedback(
        message="Approve this draft?",
        emit=["needs_revision", "approved"],
        llm="openai/gpt-4o-mini",            # maps free-text feedback to one label
        default_outcome="needs_revision",    # used when feedback is empty
    )
    def draft(self):
        return "Draft v1"

    @listen("approved")
    def publish(self, result: HumanFeedbackResult):
        return f"published: {result.output} ({result.feedback})"

    @listen("needs_revision")
    def revise(self, result: HumanFeedbackResult):
        return f"revise: {result.feedback}"
```

- `HumanFeedbackResult` fields: `output`, `feedback`, `outcome`, `timestamp`, `method_name`, `metadata`. The text is **`result.feedback`** (`feedback_text` raises AttributeError). Also on the flow: `self.last_human_feedback`, `self.human_feedback_history`.
- Empty feedback -> `default_outcome`, or `emit[0]` if no default. Put the safe outcome first and set it as `default_outcome`, so pressing Enter never approves.
- Non-empty feedback that the LLM cannot map to a label raises `HumanFeedbackCollapseError` - it does not fall back.
- Non-empty feedback is mapped by `llm`: with `anthropic/claude-haiku-4-5`, "Looks good to me, ship it." became `approved` and "No, the tone is wrong - please rewrite it more politely." became `needs_revision`; the original text stays in `result.feedback`.
- `default_outcome` without `emit` raises `ValueError: default_outcome requires emit to be specified.`
- Without `emit`, the next listener gets the `HumanFeedbackResult` and no routing happens.
- The default provider reads the console. Pass `provider=` (an object with `request_feedback(context, flow) -> str`) for tests or a UI; raise `HumanFeedbackPending` from it to pause, then `MyFlow.from_pending(flow_id, persistence).resume(feedback)` later ([persistence-and-checkpoints](references/persistence-and-checkpoints.md)). With no stdin (CI, `< /dev/null`, a background job) the console provider raises `EOFError: EOF when reading a line` and the flow fails. Never use `input()` in a deployed flow.

---

## 9. `plot()`

```python
path = TicketFlow().plot("ticket_flow.html", show=False)
print(path)   # /tmp/.../crewai_flow_xxxx/ticket_flow.html
```

- `plot(filename="crewai_flow.html", show=True)` writes **interactive HTML (plus a .js and .css) into a new temp directory** and returns the absolute path. Nothing is written to the current directory and there is no PNG. Copy the files if you need to keep them.
- The filename is used as given: `plot("my_flow")` writes a file named `my_flow` with no `.html` extension.
- `show=True` opens a browser; use `show=False` in CI and headless runs.
- Routers without a `Literal[...]` return type or `emit=[...]` log "Router events for 'r' are dynamic or not statically inferable" and the graph may omit their edges. The graph data lives in the `.js` file, not the `.html`.

---

## 10. Conversational flows

For multi-turn chat, import from `crewai.flow` (`ConversationConfig`, `ConversationState`, `RouterConfig`); `crewai.experimental.conversational` is a deprecated alias of the same module. Drive turns with `flow.handle_turn(message, session_id=...)`, not `kickoff(user_message=...)` (TypeError). There is no `ChatSession` class. Details and a tested example: [conversational-flows](references/conversational-flows.md).

---

## 11. Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `ImportError: cannot import name 'persist'` | `from crewai.flow.flow import persist` | `from crewai.flow import persist` |
| `TypeError: persist.<locals>.decorator() missing 1 required positional argument: 'target'`, or a method that never runs | Bare `@persist` without parentheses | `@persist()` |
| `listen condition 'x' references the handler name 'x'` | Router label equals the listening method's name | Rename the label or the method |
| `RecursionError: Method 'r' has been called 100 times` | Router returned a label equal to a method name (often its own trigger) | Use labels that are not method names |
| Flow stops after the router, no error | Router returned a label with no `@listen` | Listen for every label; type the router `-> Literal[...]` |
| Listener runs only once though both upstreams finished | That is `or_` | Use `and_` to wait for all |
| Input value ignored | Key misspelled; structured state drops unknown keys | Match field names exactly |
| `'StateWithId' object is not subscriptable` | Dict access on structured state | `self.state.field` |
| `Flow state model must have an 'id' field` | `initial_state = MyModel` | `class F(Flow[MyModel])` |
| `crewai run` says the flow errored but output looks right | `kickoff()` in main.py returned a value | Return `None` |
| `--inputs requires a declarative flow definition` | `crewai run --inputs` on a Python flow | Pass inputs in code or via `uv run kickoff '<json>'` |
| `invoked synchronously from within a running event loop` | `crew.kickoff()` inside `async def` | `await crew.akickoff()` or make the method sync |
| Resumed run starts from defaults | Unknown id, or no `@persist` on the class | Check the id and decorator; both cases are silent |
| Same execution id reused across runs | `inputs={"id": ...}` | `restore_from_state_id=` |
| No checkpoint files for a flow | Default `on_events=["task_completed"]` | `on_events=["method_execution_finished"]` |
| Checkpoint resume returns a label (or `None`) and runs nothing | The checkpoint was taken after a router finished | Resume from a checkpoint before the router, or re-run |
| `EOFError: EOF when reading a line` in `@human_feedback` | Console provider with no stdin | Pass `provider=` |
| Scaffolded flow ignores the `topic` input | Template `plan_content()` hard-codes `"AI Agents"` | Remove the assignment |
| `AttributeError: ... 'feedback_text'` | Old field name | `result.feedback` |
| `HumanFeedbackCollapseError` | Feedback matched no `emit` label | Clear labels, a capable `llm`, catch the error |
| `plot()` file not in the project | It writes to a temp dir | Use the returned path |

---

## 12. Checklist

- [ ] State is `Flow[MyState]` with defaults on every field; no hand-set `id`
- [ ] Every router label differs from every method name and has a listener
- [ ] Router return type is `Literal[...]` (or `emit=[...]`) so `plot()` shows the edges
- [ ] Joins use `or_` (first wins, once) or `and_` (all) deliberately
- [ ] `async def` methods `await crew.akickoff()`; sync methods call `kickoff()`
- [ ] `persist` imported from `crewai.flow` and written `@persist()`; resume uses `restore_from_state_id` (`restoreFromStateId` over HTTP)
- [ ] `CREWAI_STORAGE_DIR` set to an absolute path where state must be found again
- [ ] Checkpointed flows use `on_events=["method_execution_finished"]`; the latest file is picked by mtime; crash-prone steps sit before routers
- [ ] `@human_feedback` has the safe outcome first and as `default_outcome`; code reads `.feedback`
- [ ] `main.kickoff()` returns `None`; `[tool.crewai] type = "flow"` is present
- [ ] Ran `crewai flow plot` (or `plot(show=False)`) and checked the graph

---

## References

- [Routing patterns](references/routing-patterns.md) - revision loops with `or_` + router, nested conditions, multiple routers, a complete router/or_/persist sample flow
- [Persistence and checkpoints](references/persistence-and-checkpoints.md) - storage paths, fork vs resume, custom `FlowPersistence`, checkpoint resume and edit, paused human feedback
- [Conversational flows](references/conversational-flows.md) - `handle_turn`, `ConversationConfig`, routing turns

Public docs: https://docs.crewai.com/en/concepts/flows, https://docs.crewai.com/en/concepts/checkpointing, https://docs.crewai.com/en/learn/human-feedback-in-flows, https://docs.crewai.com/en/guides/flows/inputs-id-deprecation

For related skills:

- **getting-started** - choosing between a crew and a flow, project layout
- **check-crewai-api** - current Agent/Task/Crew/LLM API vs remembered 0.x forms
- **design-task** - task descriptions, structured output and guardrails for the crews a flow calls
- **test-crewai-project** - running flows offline with a stub LLM and asserting on state
- **deploy-to-amp** - project shape and entry points the hosted build expects for `type = "flow"`
- **call-deployed-crew** - kicking off a deployed flow over HTTP
- **ask-docs** - query the live docs when a row here does not match your version
