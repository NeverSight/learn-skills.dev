---
name: elixir-essentials
description: MANDATORY for ALL Elixir code changes. Invoke before writing any .ex or .exs file.
file_patterns:
  - "**/*.ex"
  - "**/*.exs"
auto_suggest: true
---

# Elixir Essentials

## RULES — Follow these with no exceptions

1. **Use pattern matching over if/else** for control flow and data extraction
2. **Add @impl true** before every callback function (mount, handle_event, handle_info, etc.)
3. **Return {:ok, result} | {:error, reason} tuples** for fallible operations
4. **Use `with` for 2+ sequential fallible operations** instead of nested case
5. **Use the pipe operator** for 2+ chained transformations
6. **Never nest if/else statements** — use case, cond, or multi-clause functions
7. **Predicate functions end with `?`**, dangerous functions end with `!`
8. **Let it crash** — don't write defensive code for impossible states

---

## Pattern Matching

Pattern matching is the primary control flow mechanism in Elixir. Prefer it over conditional statements.

### Prefer Pattern Matching Over if/else

**Bad:**
```elixir
def process(result) do
  if result.status == :ok do
    result.data
  else
    nil
  end
end
```

**Good:**
```elixir
def process(%{status: :ok, data: data}), do: data
def process(_), do: nil
```

### Use Case for Multiple Patterns

**Bad:**
```elixir
def handle_response(response) do
  if response.status == 200 do
    {:ok, response.body}
  else if response.status == 404 do
    {:error, :not_found}
  else
    {:error, :unknown}
  end
end
```

**Good:**
```elixir
def handle_response(%{status: 200, body: body}), do: {:ok, body}
def handle_response(%{status: 404}), do: {:error, :not_found}
def handle_response(_), do: {:error, :unknown}
```

## Pipe Operator

Use the pipe operator `|>` to chain function calls for improved readability.

### Basic Piping

**Bad:**
```elixir
String.upcase(String.trim(user_input))
```

**Good:**
```elixir
user_input
|> String.trim()
|> String.upcase()
```

### Pipe into Function Heads

**Bad:**
```elixir
def process_user(user) do
  validated = validate_user(user)
  transformed = transform_user(validated)
  save_user(transformed)
end
```

**Good:**
```elixir
def process_user(user) do
  user
  |> validate_user()
  |> transform_user()
  |> save_user()
end
```

## With Statement

Use `with` for sequential operations that can fail.

**Bad:**
```elixir
def create_post(params) do
  case validate_params(params) do
    {:ok, valid_params} ->
      case create_changeset(valid_params) do
        {:ok, changeset} ->
          Repo.insert(changeset)
        error -> error
      end
    error -> error
  end
end
```

**Good:**
```elixir
def create_post(params) do
  with {:ok, valid_params} <- validate_params(params),
       {:ok, changeset} <- create_changeset(valid_params),
       {:ok, post} <- Repo.insert(changeset) do
    {:ok, post}
  end
end
```

### With Statement - Inline Error Handling

Handle specific errors in the else block.

```elixir
def transfer_money(from_id, to_id, amount) do
  with {:ok, from_account} <- get_account(from_id),
       {:ok, to_account} <- get_account(to_id),
       :ok <- validate_balance(from_account, amount),
       {:ok, _} <- debit(from_account, amount),
       {:ok, _} <- credit(to_account, amount) do
    {:ok, :transfer_complete}
  else
    {:error, :insufficient_funds} ->
      {:error, "Not enough money in account"}

    {:error, :not_found} ->
      {:error, "Account not found"}

    error ->
      {:error, "Transfer failed: #{inspect(error)}"}
  end
end
```

## Guards

Use guards for simple type and value checks in function heads.

```elixir
def calculate(x) when is_integer(x) and x > 0 do
  x * 2
end

def calculate(_), do: {:error, :invalid_input}
```

## List Comprehensions

Use `for` comprehensions for complex transformations and filtering.

**Bad (multiple passes):**
```elixir
list
|> Enum.map(&transform/1)
|> Enum.filter(&valid?/1)
|> Enum.map(&format/1)
```

**Good (single pass):**
```elixir
for item <- list,
    transformed = transform(item),
    valid?(transformed) do
  format(transformed)
end
```

## Naming Conventions

- Module names: `PascalCase`
- Function names: `snake_case`
- Variables: `snake_case`
- Atoms: `:snake_case`
- Predicate functions end with `?`: `valid?`, `empty?`
- Dangerous functions end with `!`: `save!`, `update!`

## Tagged Tuples for Error Handling

The idiomatic way to handle success and failure in Elixir.

```elixir
def fetch_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end

# Usage
case fetch_user(123) do
  {:ok, user} -> IO.puts("Found: #{user.name}")
  {:error, :not_found} -> IO.puts("User not found")
end
```

## Case Statements

Pattern match on results.

```elixir
def process_upload(file) do
  case save_file(file) do
    {:ok, path} ->
      Logger.info("File saved to #{path}")
      create_record(path)

    {:error, :invalid_format} ->
      {:error, "File format not supported"}

    {:error, reason} ->
      Logger.error("Upload failed: #{inspect(reason)}")
      {:error, "Upload failed"}
  end
end
```

## Bang Functions

Functions ending with `!` raise errors instead of returning tuples.

```elixir
# Returns {:ok, user} or {:error, changeset}
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end

# Returns user or raises
def create_user!(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert!()
end

# Usage
try do
  user = create_user!(invalid_attrs)
  IO.puts("Created #{user.name}")
rescue
  e in Ecto.InvalidChangesetError ->
    IO.puts("Failed: #{inspect(e)}")
end
```

## Try/Rescue

Catch exceptions when needed (use sparingly).

```elixir
def parse_json(string) do
  try do
    {:ok, Jason.decode!(string)}
  rescue
    Jason.DecodeError -> {:error, :invalid_json}
  end
end
```

## Supervision Trees

Let processes fail and restart (preferred over defensive coding).

```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      MyApp.Repo,
      MyAppWeb.Endpoint,
      {MyApp.Worker, []}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

## GenServer Error Handling

Handle errors in GenServer callbacks.

```elixir
def handle_call(:risky_operation, _from, state) do
  case perform_operation() do
    {:ok, result} ->
      {:reply, {:ok, result}, update_state(state, result)}

    {:error, reason} ->
      Logger.error("Operation failed: #{inspect(reason)}")
      {:reply, {:error, reason}, state}
  end
end

# Let it crash for unexpected errors
def handle_cast(:dangerous_work, state) do
  # If this raises, supervisor will restart the process
  result = dangerous_function!()
  {:noreply, Map.put(state, :result, result)}
end
```

## Validation Errors

Return clear, actionable error messages.

```elixir
def validate_image_upload(file) do
  with :ok <- validate_file_type(file),
       :ok <- validate_file_size(file),
       :ok <- validate_dimensions(file) do
    {:ok, file}
  else
    {:error, :invalid_type} ->
      {:error, "Only JPEG, PNG, and GIF files are allowed"}

    {:error, :too_large} ->
      {:error, "File must be less than 10MB"}

    {:error, :invalid_dimensions} ->
      {:error, "Image must be at least 100x100 pixels"}
  end
end
```

## Changeset Errors

Extract and format Ecto changeset errors.

```elixir
def changeset_errors(changeset) do
  Ecto.Changeset.traverse_errors(changeset, fn {msg, opts} ->
    Enum.reduce(opts, msg, fn {key, value}, acc ->
      String.replace(acc, "%{#{key}}", to_string(value))
    end)
  end)
end

# Usage
case create_user(attrs) do
  {:ok, user} -> {:ok, user}
  {:error, changeset} ->
    errors = changeset_errors(changeset)
    {:error, errors}
end
```

## Early Returns

Use pattern matching in function heads for early returns.

```elixir
def process_data(nil), do: {:error, :no_data}
def process_data([]), do: {:error, :empty_list}
def process_data(data) when is_list(data) do
  # Process the list
  {:ok, Enum.map(data, &transform/1)}
end
```

## Avoid Defensive Programming

Don't check for things that can't happen. Let it crash.

**Bad (defensive):**
```elixir
def get_username(user) do
  if user && user.name do
    user.name
  else
    "Unknown"
  end
end
```

**Good (trust your types):**
```elixir
def get_username(%User{name: name}), do: name
```

If the user is nil or doesn't have a name, it's a bug that should crash and be fixed.

## Documentation

Use `@doc` for public functions and `@moduledoc` for modules.

```elixir
defmodule MyModule do
  @moduledoc """
  This module handles user operations.
  """

  @doc """
  Fetches a user by ID.

  Returns `{:ok, user}` or `{:error, :not_found}`.
  """
  def fetch_user(id), do: # ...
end
```

## Immutability

All data structures are immutable. Functions return new values rather than modifying in place.

```elixir
# Always returns a new list
list = [1, 2, 3]
new_list = [0 | list]  # [0, 1, 2, 3]
# list is still [1, 2, 3]
```

## Testing

When writing test files for Elixir modules, invoke `elixir-phoenix-guide:testing-essentials` before writing any `_test.exs` file.

## Anonymous Functions

Use the capture operator `&` for concise anonymous functions.

**Verbose:**
```elixir
Enum.map(list, fn x -> x * 2 end)
```

**Concise:**
```elixir
Enum.map(list, &(&1 * 2))
```

**Named function capture:**
```elixir
Enum.map(users, &User.format/1)
```
