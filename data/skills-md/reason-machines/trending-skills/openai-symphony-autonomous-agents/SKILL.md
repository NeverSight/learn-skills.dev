---
name: openai-symphony-autonomous-agents
description: Symphony turns project work into isolated, autonomous implementation runs, allowing teams to manage work instead of supervising coding agents.
triggers:
  - set up Symphony for my repository
  - run autonomous coding agents on my project
  - integrate Symphony with Linear board
  - manage work with coding agents instead of supervising them
  - implement Symphony spec in my codebase
  - spawn isolated agent runs for tasks
  - configure Symphony Elixir implementation
  - automate PR workflow with Symphony agents
---

# OpenAI Symphony

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Symphony turns project work into isolated, autonomous implementation runs, allowing teams to **manage work** instead of **supervising coding agents**. Instead of watching an agent code, you define tasks (e.g. in Linear), and Symphony spawns agents that complete them, provide proof of work (CI status, PR reviews, walkthrough videos), and land PRs autonomously.

---

## What Symphony Does

- Monitors a work tracker (e.g. Linear) for tasks
- Spawns isolated agent runs per task (using Codex or similar)
- Each agent implements the task, opens a PR, and provides proof of work
- Engineers review outcomes, not agent sessions
- Works best in codebases using [harness engineering](https://openai.com/index/harness-engineering/)

---

## Installation Options

### Option 1: Ask an agent to build it

Paste this prompt into Claude Code, Cursor, or Codex:

```
Implement Symphony according to the following spec:
https://github.com/openai/symphony/blob/main/SPEC.md
```

### Option 2: Use the Elixir reference implementation

```bash
git clone https://github.com/openai/symphony.git
cd symphony/elixir
```

Follow `elixir/README.md`, or ask an agent:

```
Set up Symphony for my repository based on
https://github.com/openai/symphony/blob/main/elixir/README.md
```

---

## Elixir Reference Implementation Setup

### Requirements

- Elixir + Mix installed
- An OpenAI API key (for Codex agent)
- A Linear API key (if using Linear integration)
- A GitHub token (for PR operations)

### Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # OpenAI API key for Codex
export LINEAR_API_KEY="lin_api_..."      # Linear integration
export GITHUB_TOKEN="ghp_..."           # GitHub PR operations
export SYMPHONY_REPO_PATH="/path/to/repo"  # Target repository
```

### Install Dependencies

```bash
cd elixir
mix deps.get
```

### Configuration (`elixir/config/config.exs`)

```elixir
import Config

config :symphony,
  openai_api_key: System.get_env("OPENAI_API_KEY"),
  linear_api_key: System.get_env("LINEAR_API_KEY"),
  github_token: System.get_env("GITHUB_TOKEN"),
  repo_path: System.get_env("SYMPHONY_REPO_PATH", "./"),
  poll_interval_ms: 30_000,
  max_concurrent_agents: 3
```

### Run Symphony

```bash
mix symphony.start
# or in IEx for development
iex -S mix
```

---

## Core Concepts

### Isolated Implementation Runs

Each task gets its own isolated run:
- Fresh git branch per task
- Agent operates only within that branch
- No shared state between runs
- Proof of work collected before PR merge

### Proof of Work

Before a PR is accepted, Symphony collects:
- CI/CD pipeline status
- PR review feedback
- Complexity analysis
- (optionally) walkthrough videos

---

## Key Elixir Modules & Patterns

### Starting the Symphony supervisor

```elixir
# In your application.ex or directly
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      Symphony.Supervisor
    ]
    Supervisor.start_link(children, strategy: :one_for_one)
  end
end
```

### Defining a Task (Symphony Task struct)

```elixir
defmodule Symphony.Task do
  @type t :: %__MODULE__{
    id: String.t(),
    title: String.t(),
    description: String.t(),
    source: :linear | :manual,
    status: :pending | :running | :completed | :failed,
    branch: String.t() | nil,
    pr_url: String.t() | nil,
    proof_of_work: map() | nil
  }

  defstruct [:id, :title, :description, :source,
             status: :pending, branch: nil,
             pr_url: nil, proof_of_work: nil]
end
```

### Spawning an Agent Run

```elixir
defmodule Symphony.AgentRunner do
  @doc """
  Spawns an isolated agent run for a given task.
  Each run gets its own branch and Codex session.
  """
  def run(task) do
    branch = "symphony/#{task.id}-#{slugify(task.title)}"

    with :ok <- Git.create_branch(branch),
         {:ok, result} <- Codex.implement(task, branch),
         {:ok, pr_url} <- GitHub.open_pr(branch, task),
         {:ok, proof} <- ProofOfWork.collect(pr_url) do
      {:ok, %{task | status: :completed, pr_url: pr_url, proof_of_work: proof}}
    else
      {:error, reason} -> {:error, reason}
    end
  end

  defp slugify(title) do
    title
    |> String.downcase()
    |> String.replace(~r/[^a-z0-9]+/, "-")
    |> String.trim("-")
  end
end
```

### Linear Integration — Polling for Tasks

```elixir
defmodule Symphony.Linear.Poller do
  use GenServer

  @poll_interval Application.compile_env(:symphony, :poll_interval_ms, 30_000)

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def init(_opts) do
    schedule_poll()
    {:ok, %{processed_ids: MapSet.new()}}
  end

  def handle_info(:poll, state) do
    case Symphony.Linear.Client.fetch_todo_tasks() do
      {:ok, tasks} ->
        new_tasks = Enum.reject(tasks, &MapSet.member?(state.processed_ids, &1.id))
        Enum.each(new_tasks, &Symphony.AgentRunner.run/1)
        new_ids = Enum.reduce(new_tasks, state.processed_ids, &MapSet.put(&2, &1.id))
        schedule_poll()
        {:noreply, %{state | processed_ids: new_ids}}

      {:error, reason} ->
        Logger.error("Linear poll failed: #{inspect(reason)}")
        schedule_poll()
        {:noreply, state}
    end
  end

  defp schedule_poll do
    Process.send_after(self(), :poll, @poll_interval)
  end
end
```

### Linear API Client

```elixir
defmodule Symphony.Linear.Client do
  @linear_api "https://api.linear.app/graphql"

  def fetch_todo_tasks do
    query = """
    query {
      issues(filter: { state: { name: { eq: "Todo" } } }) {
        nodes {
          id
          title
          description
        }
      }
    }
    """

    case HTTPoison.post(@linear_api, Jason.encode!(%{query: query}), headers()) do
      {:ok, %{status_code: 200, body: body}} ->
        tasks =
          body
          |> Jason.decode!()
          |> get_in(["data", "issues", "nodes"])
          |> Enum.map(&to_task/1)
        {:ok, tasks}

      {:error, reason} ->
        {:error, reason}
    end
  end

  defp headers do
    [
      {"Authorization", System.get_env("LINEAR_API_KEY")},
      {"Content-Type", "application/json"}
    ]
  end

  defp to_task(%{"id" => id, "title" => title, "description" => desc}) do
    %Symphony.Task{id: id, title: title, description: desc, source: :linear}
  end
end
```

### Proof of Work Collection

```elixir
defmodule Symphony.ProofOfWork do
  @doc """
  Collects proof of work for a PR before it can be merged.
  Returns a map with CI status, review feedback, and complexity.
  """
  def collect(pr_url) do
    with {:ok, ci_status} <- wait_for_ci(pr_url),
         {:ok, reviews} <- fetch_reviews(pr_url),
         {:ok, complexity} <- analyze_complexity(pr_url) do
      {:ok, %{
        ci_status: ci_status,
        reviews: reviews,
        complexity: complexity,
        collected_at: DateTime.utc_now()
      }}
    end
  end

  defp wait_for_ci(pr_url, retries \\ 30) do
    case GitHub.get_pr_ci_status(pr_url) do
      {:ok, :success} -> {:ok, :success}
      {:ok, :pending} when retries > 0 ->
        Process.sleep(60_000)
        wait_for_ci(pr_url, retries - 1)
      {:ok, status} -> {:ok, status}
      {:error, reason} -> {:error, reason}
    end
  end

  defp fetch_reviews(pr_url), do: GitHub.get_pr_reviews(pr_url)
  defp analyze_complexity(pr_url), do: GitHub.get_pr_diff_complexity(pr_url)
end
```

---

## Implementing the SPEC.md (Custom Implementation)

When building Symphony in another language, the spec defines:

1. **Task Source** — poll Linear/GitHub/Jira for tasks in a specific state
2. **Agent Invocation** — call Codex (or another agent) with task context
3. **Isolation** — each run on a fresh branch, containerized if possible
4. **Proof of Work** — CI, review, and analysis before merge
5. **Landing** — auto-merge or present to engineer for approval

Minimal implementation loop in pseudocode:

```elixir
# Core symphony loop
def symphony_loop(state) do
  tasks = fetch_new_tasks(state.source)

  tasks
  |> Enum.filter(&(&1.status == :todo))
  |> Enum.each(fn task ->
    Task.async(fn ->
      branch = create_isolated_branch(task)
      invoke_agent(task, branch)         # Codex / Claude / etc.
      proof = collect_proof_of_work(branch)
      present_for_review(task, proof)
    end)
  end)

  Process.sleep(state.poll_interval)
  symphony_loop(state)
end
```

---

## Common Patterns

### Limiting Concurrent Agent Runs

```elixir
defmodule Symphony.AgentPool do
  use GenServer

  @max_concurrent 3

  def start_link(_), do: GenServer.start_link(__MODULE__, %{running: 0, queue: []}, name: __MODULE__)

  def submit(task) do
    GenServer.cast(__MODULE__, {:submit, task})
  end

  def handle_cast({:submit, task}, %{running: n} = state) when n < @max_concurrent do
    spawn_agent(task)
    {:noreply, %{state | running: n + 1}}
  end

  def handle_cast({:submit, task}, %{queue: q} = state) do
    {:noreply, %{state | queue: q ++ [task]}}
  end

  def handle_info({:agent_done, _result}, %{running: n, queue: [next | rest]} = state) do
    spawn_agent(next)
    {:noreply, %{state | running: n, queue: rest}}
  end

  def handle_info({:agent_done, _result}, %{running: n} = state) do
    {:noreply, %{state | running: n - 1}}
  end

  defp spawn_agent(task) do
    parent = self()
    spawn(fn ->
      result = Symphony.AgentRunner.run(task)
      send(parent, {:agent_done, result})
    end)
  end
end
```

### Manual Task Injection (No Linear)

```elixir
# In IEx or a Mix task
Symphony.AgentPool.submit(%Symphony.Task{
  id: "manual-001",
  title: "Add rate limiting to API",
  description: "Implement token bucket rate limiting on /api/v1 endpoints",
  source: :manual
})
```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Agents not spawning | Missing `OPENAI_API_KEY` | Check env var is exported |
| Linear tasks not detected | Wrong Linear state filter | Update query filter to match your board's state name |
| PRs not opening | Missing `GITHUB_TOKEN` or wrong repo | Verify token has `repo` scope |
| CI never completes | Timeout too short | Increase `retries` in `wait_for_ci/2` |
| Too many concurrent runs | Default pool size | Set `max_concurrent_agents` in config |
| Branch conflicts | Agent reusing branch names | Ensure task IDs are unique per run |

### Debug Mode

```elixir
# In config/dev.exs
config :symphony, log_level: :debug

# Or at runtime
Logger.put_module_level(Symphony.AgentRunner, :debug)
Logger.put_module_level(Symphony.Linear.Poller, :debug)
```

---

## Resources

- [SPEC.md](https://github.com/openai/symphony/blob/main/SPEC.md) — Full Symphony specification
- [elixir/README.md](https://github.com/openai/symphony/blob/main/elixir/README.md) — Elixir setup guide
- [Harness Engineering](https://openai.com/index/harness-engineering/) — Prerequisite methodology
- [Apache 2.0 License](https://github.com/openai/symphony/blob/main/LICENSE)
