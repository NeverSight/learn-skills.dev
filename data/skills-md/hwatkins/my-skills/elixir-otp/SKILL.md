---
name: elixir-otp
description: OTP patterns for Elixir — GenServer, Agent, Task, ETS, supervision trees, Registry, and process design. Use when designing concurrent systems, stateful processes, or deciding when (and when NOT) to use processes.
---

# OTP Patterns

Expert guidance for process design, supervision, and concurrency in Elixir/OTP.

## The Golden Rule

**Database is the source of truth for domain entities. Processes are for infrastructure.**

Don't reach for a GenServer to hold domain state (users, orders, tasks). Use PostgreSQL. Use processes for:
- Connection pools
- Caches (ETS)
- Rate limiters
- PubSub / event buses
- Background workers
- Real-time session state

```elixir
# ❌ Bad: GenServer for domain entity
defmodule MyApp.TaskServer do
  use GenServer
  # Holds task state in process memory
  # Lost on crash, hard to query, doesn't scale
end

# ✅ Good: Database for domain, process for infrastructure
defmodule MyApp.Tasks do
  def get_task!(id), do: Repo.get!(Task, id)
  def update_task(task, attrs), do: task |> Task.changeset(attrs) |> Repo.update()
end

defmodule MyApp.RateLimiter do
  use GenServer
  # Rate limiting IS infrastructure — process is appropriate
end
```

## When to Use What

| Abstraction | Use When | Don't Use When |
|-------------|----------|----------------|
| **GenServer** | Need stateful process with request/response | Just storing domain data |
| **Agent** | Simple state wrapper, no complex logic | Need handle_info, timeouts, or complex state |
| **Task** | One-off async work, fire-and-forget or await | Need persistent state or retries |
| **Task.Supervisor** | Concurrent tasks that might fail | Tasks must all succeed atomically |
| **ETS** | Fast concurrent reads, shared cache | Data must survive node restart |
| **Registry** | Dynamic process lookup by name | Static, known-at-compile-time processes |
| **Oban** | Reliable background jobs with retries | Simple in-process async work |
| **No process** | Pure functions, Repo calls, pipelines | — |

## GenServer

Use for stateful infrastructure with request/response semantics:

```elixir
defmodule MyApp.Cache do
  use GenServer

  # Client API — called by other processes
  def start_link(opts) do
    name = Keyword.fetch!(opts, :name)
    ttl = Keyword.get(opts, :ttl, :timer.minutes(5))
    GenServer.start_link(__MODULE__, %{ttl: ttl}, name: name)
  end

  def get(server, key) do
    GenServer.call(server, {:get, key})
  end

  def put(server, key, value) do
    GenServer.cast(server, {:put, key, value})
  end

  # Server callbacks
  @impl true
  def init(state) do
    schedule_cleanup()
    {:ok, Map.put(state, :store, %{})}
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    case Map.get(state.store, key) do
      {value, expires_at} when expires_at > System.monotonic_time(:millisecond) ->
        {:reply, {:ok, value}, state}
      _ ->
        {:reply, :miss, state}
    end
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    expires_at = System.monotonic_time(:millisecond) + state.ttl
    {:noreply, put_in(state, [:store, key], {value, expires_at})}
  end

  @impl true
  def handle_info(:cleanup, state) do
    now = System.monotonic_time(:millisecond)
    store = Map.reject(state.store, fn {_k, {_v, exp}} -> exp <= now end)
    schedule_cleanup()
    {:noreply, %{state | store: store}}
  end

  defp schedule_cleanup, do: Process.send_after(self(), :cleanup, :timer.minutes(1))
end
```

### GenServer Best Practices

- Keep `handle_call` fast — don't do heavy work while blocking the caller
- Use `handle_cast` for fire-and-forget, `handle_call` for request/response
- Use `handle_info` for self-sent messages, timers, and external messages
- Use `handle_continue` for post-init work that shouldn't block `start_link`
- Always define `@impl true` on callbacks
- Return `{:stop, reason, state}` for clean shutdown

```elixir
# ✅ Good: Use handle_continue for expensive init
@impl true
def init(opts) do
  {:ok, %{data: nil}, {:continue, :load_data}}
end

@impl true
def handle_continue(:load_data, state) do
  data = expensive_load()
  {:noreply, %{state | data: data}}
end
```

## Agent

Simple state wrapper — use when you just need get/update with no complex logic:

```elixir
# ✅ Good: Agent for simple shared counter
{:ok, counter} = Agent.start_link(fn -> 0 end, name: MyApp.Counter)
Agent.get(MyApp.Counter, & &1)           # => 0
Agent.update(MyApp.Counter, &(&1 + 1))   # => :ok
Agent.get(MyApp.Counter, & &1)           # => 1

# ❌ Bad: Agent for complex logic — use GenServer instead
Agent.update(agent, fn state ->
  # 50 lines of complex business logic here...
  # This runs INSIDE the agent process, blocking all other callers
end)
```

## Task

For one-off concurrent work:

```elixir
# Fire-and-forget
Task.start(fn -> send_welcome_email(user) end)

# Await result (with timeout)
task = Task.async(fn -> fetch_external_data(url) end)
result = Task.await(task, 5_000)

# Multiple concurrent tasks
tasks = Enum.map(urls, fn url ->
  Task.async(fn -> fetch(url) end)
end)
results = Task.await_many(tasks, 10_000)
```

## Task.Supervisor

For tasks that might fail — isolates crashes from the caller:

```elixir
# In your supervision tree
children = [
  {Task.Supervisor, name: MyApp.TaskSupervisor}
]

# Spawn tasks that can crash safely
Task.Supervisor.start_child(MyApp.TaskSupervisor, fn ->
  send_notification(user)  # If this crashes, caller is unaffected
end)

# Async with supervisor
task = Task.Supervisor.async(MyApp.TaskSupervisor, fn ->
  fetch_external_data(url)
end)
result = Task.await(task)

# Concurrent stream with backpressure
MyApp.TaskSupervisor
|> Task.Supervisor.async_stream(urls, &fetch/1, max_concurrency: 10, ordered: false)
|> Enum.reduce([], fn
  {:ok, result}, acc -> [result | acc]
  {:exit, _reason}, acc -> acc
end)
```

## ETS

Fast concurrent reads, shared across processes:

```elixir
# ✅ Good: ETS for read-heavy cache
defmodule MyApp.ConfigCache do
  use GenServer

  @table :config_cache

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, [], name: __MODULE__)
  end

  def get(key) do
    case :ets.lookup(@table, key) do
      [{^key, value}] -> {:ok, value}
      [] -> :error
    end
  end

  def put(key, value) do
    :ets.insert(@table, {key, value})
    :ok
  end

  @impl true
  def init(_) do
    table = :ets.new(@table, [:set, :public, :named_table, read_concurrency: true])
    {:ok, %{table: table}}
  end
end
```

### ETS vs GenServer State

| | ETS | GenServer state |
|---|-----|-----------------|
| **Reads** | Concurrent, no bottleneck | Serialized through process |
| **Writes** | Atomic per-row | Serialized (safe) |
| **Survives crash** | Only if heir set | No (state lost) |
| **Query** | Match specs, select | Full Elixir |
| **Best for** | Read-heavy cache, counters | Complex state machines |

## Registry

Dynamic process lookup by key:

```elixir
# In supervision tree
children = [
  {Registry, keys: :unique, name: MyApp.Registry},
  {DynamicSupervisor, name: MyApp.RoomSupervisor}
]

# Start a named process dynamically
def start_room(room_id) do
  DynamicSupervisor.start_child(
    MyApp.RoomSupervisor,
    {MyApp.Room, room_id: room_id, name: via(room_id)}
  )
end

def via(room_id) do
  {:via, Registry, {MyApp.Registry, room_id}}
end

# Look up and call
def get_room_state(room_id) do
  GenServer.call(via(room_id), :get_state)
end
```

## Supervision Trees

### Design Principles

- **One-for-one**: Restart only the crashed child (default, most common)
- **One-for-all**: Restart all children if one crashes (tightly coupled)
- **Rest-for-one**: Restart crashed child and all children started after it

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      # Start order matters — dependencies first
      MyApp.Repo,                                          # Database
      {Phoenix.PubSub, name: MyApp.PubSub},               # PubSub
      MyApp.ConfigCache,                                   # Cache (depends on nothing)
      {Registry, keys: :unique, name: MyApp.Registry},     # Registry
      {DynamicSupervisor, name: MyApp.RoomSupervisor},     # Dynamic processes
      {Task.Supervisor, name: MyApp.TaskSupervisor},       # Task supervisor
      {Oban, Application.fetch_env!(:my_app, Oban)},       # Background jobs
      MyAppWeb.Endpoint,                                   # Web server (last)
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

### Child Spec

```elixir
# Customize restart behavior
defmodule MyApp.CriticalWorker do
  use GenServer, restart: :permanent  # Always restart (default)
end

defmodule MyApp.OptionalWorker do
  use GenServer, restart: :transient  # Only restart on abnormal exit
end

defmodule MyApp.OneShot do
  use GenServer, restart: :temporary  # Never restart
end
```

## Background Jobs with Oban

For reliable, persistent background work — NOT Task or GenServer:

```elixir
# Define a worker
defmodule MyApp.Workers.SendEmail do
  use Oban.Worker, queue: :mailers, max_attempts: 3

  @impl Oban.Worker
  def perform(%Oban.Job{args: %{"user_id" => user_id, "template" => template}}) do
    user = Accounts.get_user!(user_id)
    MyApp.Mailer.deliver(user, template)
    :ok
  end
end

# Enqueue a job
%{user_id: user.id, template: "welcome"}
|> MyApp.Workers.SendEmail.new()
|> Oban.insert()

# Schedule for later
%{user_id: user.id, template: "reminder"}
|> MyApp.Workers.SendEmail.new(scheduled_at: DateTime.add(DateTime.utc_now(), 3600))
|> Oban.insert()

# Unique jobs (prevent duplicates)
%{report_id: report.id}
|> MyApp.Workers.GenerateReport.new(unique: [period: 300, fields: [:args]])
|> Oban.insert()
```

### When to Use Oban vs Task

| | Oban | Task |
|---|------|------|
| **Persisted** | Yes (database) | No (in-memory) |
| **Retries** | Built-in with backoff | Manual |
| **Survives deploy** | Yes | No |
| **Scheduling** | Built-in | Manual with Process.send_after |
| **Monitoring** | Oban Web dashboard | None |
| **Use for** | Emails, reports, webhooks, imports | Quick async, fan-out, parallel fetch |

## When NOT to Use Processes

```elixir
# ❌ Don't use a process just to "hold" a value
defmodule MyApp.CurrentUser do
  use Agent
  def start_link(user), do: Agent.start_link(fn -> user end)
  def get(pid), do: Agent.get(pid, & &1)
end
# Just pass the user as a function argument!

# ❌ Don't use GenServer for sequential data transformation
defmodule MyApp.DataPipeline do
  use GenServer
  def process(data), do: GenServer.call(__MODULE__, {:process, data})
  def handle_call({:process, data}, _from, state) do
    result = data |> step1() |> step2() |> step3()
    {:reply, result, state}
  end
end
# Just use a regular function pipeline!
def process(data), do: data |> step1() |> step2() |> step3()

# ❌ Don't use processes for domain entities
# Users, orders, tasks, etc. belong in the database

# ✅ DO use processes for:
# - Connection pools (Repo, HTTP clients)
# - Caches (ETS-backed GenServer)
# - Rate limiters
# - Real-time session state (LiveView, channels)
# - Periodic work (GenServer with send_after)
# - Dynamic workers (DynamicSupervisor + Registry)
```

## Common Mistakes

```elixir
# ❌ Don't call GenServer from within its own callbacks
def handle_call(:get_data, _from, state) do
  other = GenServer.call(self(), :other)  # DEADLOCK!
  {:reply, other, state}
end

# ❌ Don't do heavy work in handle_call (blocks all callers)
def handle_call(:generate_report, _from, state) do
  report = generate_huge_report()  # All other callers wait!
  {:reply, report, state}
end

# ✅ Offload heavy work
def handle_call(:generate_report, from, state) do
  Task.start(fn ->
    report = generate_huge_report()
    GenServer.reply(from, report)
  end)
  {:noreply, state}
end

# ❌ Don't forget to handle unexpected messages
# Unhandled messages in handle_info will crash the GenServer in OTP 27+

# ✅ Add a catch-all
@impl true
def handle_info(msg, state) do
  Logger.warning("Unexpected message: #{inspect(msg)}")
  {:noreply, state}
end
```
