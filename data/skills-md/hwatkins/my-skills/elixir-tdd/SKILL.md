---
name: elixir-tdd
description: Test-driven development enforcement for Elixir and Phoenix. Requires failing tests before implementation. Use when implementing features, fixing bugs, or when code quality discipline is needed.
---

# Elixir TDD Enforcement

Strict test-driven development practices for Elixir and Phoenix projects.

## The Golden Rule

**No Code Without a Failing Test First**

This is not optional. This is not negotiable. Every feature, every bug fix, every change starts with a test.

## The TDD Cycle

1. **Red**: Write a test that describes the behavior you want. Run it. It must fail.
2. **Green**: Write the minimum code to make the test pass. Nothing more.
3. **Refactor**: Clean up while keeping tests green.
4. **Repeat**

```elixir
# Step 1: Write the failing test
test "create_user/1 with valid attrs creates a user" do
  attrs = %{email: "test@example.com", name: "Test User"}
  assert {:ok, %User{} = user} = Accounts.create_user(attrs)
  assert user.email == "test@example.com"
end

# Step 2: Run it - it MUST fail
# $ mix test test/my_app/accounts_test.exs:10
# ** (UndefinedFunctionError) function Accounts.create_user/1 is undefined

# Step 3: Write minimum code to pass
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end

# Step 4: Run test again - it passes
# Step 5: Refactor if needed, keeping tests green
```

## Test File Structure

Match your source structure:

```
lib/my_app/accounts/user.ex      → test/my_app/accounts/user_test.exs
lib/my_app/accounts.ex           → test/my_app/accounts_test.exs
lib/my_app_web/live/task_live.ex → test/my_app_web/live/task_live_test.exs
lib/my_app_web/controllers/      → test/my_app_web/controllers/
```

## Mandatory Test Cases

For every function, test:

### 1. Happy Path
Valid input produces expected output.

```elixir
test "create_task/1 with valid attrs creates task" do
  attrs = %{title: "Test Task", status: :todo}
  assert {:ok, %Task{} = task} = Tasks.create_task(attrs)
  assert task.title == "Test Task"
  assert task.status == :todo
end
```

### 2. Validation Failures
Invalid input returns error changeset.

```elixir
test "create_task/1 with missing title returns error" do
  assert {:error, %Ecto.Changeset{} = changeset} = Tasks.create_task(%{})
  assert %{title: ["can't be blank"]} = errors_on(changeset)
end

test "create_task/1 with invalid status returns error" do
  attrs = %{title: "Test", status: :invalid_status}
  assert {:error, changeset} = Tasks.create_task(attrs)
  assert %{status: ["is invalid"]} = errors_on(changeset)
end
```

### 3. Edge Cases
Boundary conditions and unusual inputs.

```elixir
test "create_task/1 with empty string title returns error" do
  assert {:error, changeset} = Tasks.create_task(%{title: ""})
  assert %{title: ["can't be blank"]} = errors_on(changeset)
end

test "create_task/1 with whitespace-only title returns error" do
  assert {:error, changeset} = Tasks.create_task(%{title: "   "})
  assert %{title: ["can't be blank"]} = errors_on(changeset)
end

test "list_tasks/0 returns empty list when no tasks exist" do
  assert [] = Tasks.list_tasks()
end
```

### 4. Authorization
Users can only access their own resources.

```elixir
test "get_task/2 returns error when task belongs to another user" do
  other_user = user_fixture()
  task = task_fixture(user_id: other_user.id)
  user = user_fixture()

  assert {:error, :not_found} = Tasks.get_task(user, task.id)
end

test "update_task/3 returns error when user doesn't own task" do
  owner = user_fixture()
  other_user = user_fixture()
  task = task_fixture(user_id: owner.id)

  assert {:error, :unauthorized} = Tasks.update_task(other_user, task, %{title: "Hacked"})
end
```

### 5. State Transitions (if applicable)
Valid and invalid state changes.

```elixir
describe "transition_task/2" do
  test "allows todo -> in_progress" do
    task = task_fixture(status: :todo)
    assert {:ok, task} = Tasks.transition_task(task, :in_progress)
    assert task.status == :in_progress
  end

  test "allows in_progress -> done" do
    task = task_fixture(status: :in_progress)
    assert {:ok, task} = Tasks.transition_task(task, :done)
    assert task.status == :done
  end

  test "rejects todo -> done (must go through in_progress)" do
    task = task_fixture(status: :todo)
    assert {:error, :invalid_transition} = Tasks.transition_task(task, :done)
  end

  test "rejects done -> todo" do
    task = task_fixture(status: :done)
    assert {:error, :invalid_transition} = Tasks.transition_task(task, :todo)
  end
end
```

## Testing LiveView

Use `Phoenix.LiveViewTest` for integration tests.

```elixir
import Phoenix.LiveViewTest

describe "TaskLive.Index" do
  test "renders task list", %{conn: conn} do
    task = task_fixture(title: "My Task")
    {:ok, view, html} = live(conn, ~p"/tasks")
    
    assert html =~ "My Task"
    assert has_element?(view, "#task-#{task.id}")
  end

  test "creates new task", %{conn: conn} do
    {:ok, view, _html} = live(conn, ~p"/tasks")

    view
    |> form("#task-form", task: %{title: "New Task"})
    |> render_submit()

    assert has_element?(view, "#tasks", "New Task")
  end

  test "validates task on change", %{conn: conn} do
    {:ok, view, _html} = live(conn, ~p"/tasks/new")

    html =
      view
      |> form("#task-form", task: %{title: ""})
      |> render_change()

    assert html =~ "can't be blank"
  end

  test "deletes task", %{conn: conn} do
    task = task_fixture(title: "Delete Me")
    {:ok, view, _html} = live(conn, ~p"/tasks")

    view
    |> element("#task-#{task.id} button", "Delete")
    |> render_click()

    refute has_element?(view, "#task-#{task.id}")
  end
end
```

## Test Data

Use factories or fixture functions. Keep them minimal.

```elixir
# test/support/fixtures/accounts_fixtures.ex
defmodule MyApp.AccountsFixtures do
  def user_fixture(attrs \\ %{}) do
    {:ok, user} =
      attrs
      |> Enum.into(%{
        email: "user#{System.unique_integer()}@example.com",
        name: "Test User"
      })
      |> MyApp.Accounts.create_user()

    user
  end
end

# Or with ExMachina
defmodule MyApp.Factory do
  use ExMachina.Ecto, repo: MyApp.Repo

  def user_factory do
    %MyApp.Accounts.User{
      email: sequence(:email, &"user#{&1}@example.com"),
      name: "Test User"
    }
  end
end
```

## What NOT to Do

### ❌ Don't write tests after the code

```elixir
# WRONG: Code first, then tests
def create_task(attrs), do: ...  # Written first
test "create_task works" do ...  # Added later to "cover" it
```

### ❌ Don't skip tests for "simple" functions

```elixir
# WRONG: "It's too simple to test"
def full_name(user), do: "#{user.first_name} #{user.last_name}"
# Still needs tests! What if first_name is nil?
```

### ❌ Don't test private functions directly

```elixir
# WRONG: Testing private implementation
test "parse_date/1 parses ISO format" do
  assert MyModule.parse_date("2024-01-01") == ~D[2024-01-01]
end

# RIGHT: Test through the public API
test "create_event/1 accepts ISO date strings" do
  assert {:ok, event} = Events.create_event(%{date: "2024-01-01"})
  assert event.date == ~D[2024-01-01]
end
```

### ❌ Don't mock Ecto or database in context tests

```elixir
# WRONG: Mocking the repo
expect(Repo, :insert, fn _ -> {:ok, %User{}} end)

# RIGHT: Use the sandbox, test real behavior
assert {:ok, %User{}} = Accounts.create_user(valid_attrs)
assert Repo.get(User, user.id)  # Actually in database
```

### ❌ Don't write tests that pass regardless of implementation

```elixir
# WRONG: Test always passes
test "does something" do
  result = MyModule.do_thing()
  assert result  # What if result is {:error, ...}? Still truthy!
end

# RIGHT: Assert specific expectations
test "returns ok tuple with user" do
  assert {:ok, %User{email: "test@example.com"}} = MyModule.do_thing()
end
```

## Pre-Implementation Checklist

Before writing ANY code, ask yourself:

1. ☐ Have I written a failing test?
2. ☐ Does the test describe the behavior I want?
3. ☐ Have I run the test and confirmed it fails?
4. ☐ Does it fail for the RIGHT reason?

Only after checking all boxes: write the implementation.

## Test Organization

```elixir
defmodule MyApp.TasksTest do
  use MyApp.DataCase

  alias MyApp.Tasks
  alias MyApp.Tasks.Task

  import MyApp.AccountsFixtures
  import MyApp.TasksFixtures

  describe "create_task/1" do
    test "with valid attrs creates task" do
      # ...
    end

    test "with invalid attrs returns error changeset" do
      # ...
    end

    test "with empty title returns error" do
      # ...
    end
  end

  describe "update_task/2" do
    setup do
      task = task_fixture()
      %{task: task}
    end

    test "with valid attrs updates the task", %{task: task} do
      # ...
    end
  end

  describe "delete_task/1" do
    # ...
  end
end
```

## Mocking External Dependencies with Mox

Use behaviours + Mox for external services. Never mock Ecto or internal modules.

```elixir
# 1. Define a behaviour
defmodule MyApp.WeatherAPI do
  @callback get_forecast(String.t()) :: {:ok, map()} | {:error, term()}
end

# 2. Create the real implementation
defmodule MyApp.WeatherAPI.Client do
  @behaviour MyApp.WeatherAPI

  @impl true
  def get_forecast(city) do
    Req.get("https://api.weather.com/forecast", params: [city: city])
  end
end

# 3. Configure the mock in test_helper.exs
Mox.defmock(MyApp.MockWeatherAPI, for: MyApp.WeatherAPI)

# 4. Configure in config/test.exs
# config :my_app, weather_api: MyApp.MockWeatherAPI

# 5. Use in your context (reads from config)
defmodule MyApp.Weather do
  def weather_api, do: Application.get_env(:my_app, :weather_api, MyApp.WeatherAPI.Client)

  def get_forecast(city) do
    weather_api().get_forecast(city)
  end
end

# 6. Test with mock
import Mox

test "get_forecast returns weather data" do
  expect(MyApp.MockWeatherAPI, :get_forecast, fn "London" ->
    {:ok, %{temp: 15, condition: "cloudy"}}
  end)

  assert {:ok, %{temp: 15}} = Weather.get_forecast("London")
end
```

## Property-Based Testing with StreamData

Test properties that hold for all inputs, not just specific examples:

```elixir
use ExUnitProperties

# ✅ Good: Test a property that always holds
property "User.full_name/1 always returns a string" do
  check all first <- string(:alphanumeric, min_length: 1),
            last <- string(:alphanumeric, min_length: 1) do
    user = %User{first_name: first, last_name: last}
    result = User.full_name(user)
    assert is_binary(result)
    assert String.contains?(result, first)
    assert String.contains?(result, last)
  end
end

# ✅ Good: Roundtrip property
property "encoding then decoding returns the original" do
  check all data <- map_of(string(:alphanumeric), integer()) do
    assert data == data |> MyApp.Encoder.encode() |> MyApp.Encoder.decode()
  end
end

# ✅ Good: Invariant property
property "sorting is idempotent" do
  check all list <- list_of(integer()) do
    sorted = Enum.sort(list)
    assert sorted == Enum.sort(sorted)
  end
end

# ✅ Good: Custom generators for domain types
property "valid emails are accepted, invalid rejected" do
  valid_email = gen all name <- string(:alphanumeric, min_length: 1),
                        domain <- string(:alphanumeric, min_length: 1) do
    "#{name}@#{domain}.com"
  end

  check all email <- valid_email do
    assert {:ok, _} = Accounts.validate_email(email)
  end
end
```

## Running Tests

```bash
# Run all tests
mix test

# Run specific file
mix test test/my_app/tasks_test.exs

# Run specific test by line number
mix test test/my_app/tasks_test.exs:42

# Run with coverage
mix test --cover

# Run failed tests only
mix test --failed

# Run tests matching a pattern
mix test --only integration
```
