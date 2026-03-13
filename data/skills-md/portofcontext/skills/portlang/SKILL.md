---
name: portlang
description: "portlang - the environment-first agent framework. Use when creating field.toml files, defining boundaries and verifiers, adding custom tools (shell, Python, MCP), debugging trajectories, measuring convergence, configuring structured JSON output with output_schema, running batch evals, viewing HTML trajectory dashboards, or analyzing agent behavior across runs. portlang manages environments not loops - you define the search space, the agent finds the path."
license: MIT
metadata:
  author: portofcontext
  version: 1.2.6
---

# portlang Skill

## Core Concept

portlang treats agent behavior as **search through a conditioned space**. You don't script loops—you declare the search space:
- **Boundaries:** What the agent cannot do (enforced by sandbox)
- **Verifiers:** What success looks like (runtime reward signals)
- **Context budget:** Hard token ceiling
- **Environment:** What the agent can observe

The runtime executes the search. Every run produces a **trajectory** (complete event log).

## Prerequisites

portlang currently only runs on apple devices.
Before running portlang fields:

1. **Install portlang:**
```bash
brew tap portofcontext/homebrew-tap
brew install portlang
```

2. **Set API key** (choose one):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENROUTER_API_KEY=sk-or-v1-...
```

3. **Verify installation:**
```bash
portlang init  # Check container support 
```

**Model naming by provider:**
- Anthropic API: `anthropic/claude-sonnet-4.6`, `anthropic/claude-opus-4.5`
- OpenRouter: `anthropic/claude-3.5-sonnet`, `anthropic/claude-3-opus`, anything on openrouter that support tool calling
- Provider auto-detected from API key

## field.toml Structure

All sections are optional unless marked (required). Fields marked `"inherit"` pull their value from a parent `field.toml` one directory up (auto-detected if `../field.toml` exists).

```toml
name = "my-task"        # (required) identifier, used in trajectory storage
description = "..."     # human-readable summary

[model]                 # (required), or: model = "inherit"
name = "anthropic/claude-sonnet-4.6"  # (required)
temperature = 0.5       # default: 0.5

[prompt]                # (required)
goal = "..."            # (required) initial task, enters context at step 0
system = "..."          # optional system prompt prepended to all interactions
re_observation = ["echo '=== workspace ===' && ls -1", ...]  # refresh context each step

[environment]           # optional; all fields have defaults
root = "./workspace"    # working dir (maps to /workspace in container)
packages = ["nodejs"]   # apt packages to install; list "uv" to get uv/pip
dockerfile = "./Dockerfile"  # custom Dockerfile (overrides packages)
image = "custom:tag"    # pre-built image (overrides dockerfile)

[boundary]              # optional, or: boundary = "inherit"
allow_write = ["*.py"]  # glob patterns for writable paths; default: none
network = "deny"        # "deny" | "allow"; default: allow
max_tokens = 150000     # hard ceiling on total context tokens
max_cost = "$2.00"      # hard ceiling on total cost
max_steps = 30          # hard ceiling on agent steps

tools = "inherit"       # optional; inherit [[tool]] list from parent instead of defining inline

[[tool]]                # repeatable; type = "python" | "shell" | "mcp"; bash/glob/write are built-in defaults

# Shell verifier (default when type is omitted):
[[verifier]]
type = "shell"          # default; type can be omitted for shell verifiers
name = "..."            # (required)
command = "..."         # shell command; exit 0 = pass, nonzero = fail
trigger = "on_stop"     # "on_stop" | "always" | "on_write"; default: on_stop
description = "..."     # injected into context on failure

# Levenshtein verifier (normalized edit distance):
[[verifier]]
type = "levenshtein"
name = "..."
file = "output.txt"     # workspace-relative path to actual output
expected = "..."        # reference string to compare against
threshold = 0.9         # similarity [0.0–1.0] required to pass; default: 1.0

# JSON structure verifier:
[[verifier]]
type = "json"
name = "..."
file = "output.json"    # workspace-relative path to validate
schema = '{"type": "object"}'  # optional JSON Schema string

# Semantic similarity verifier (cosine via embeddings):
[[verifier]]
type = "semantic"
name = "..."
file = "output.txt"
expected = "..."        # reference string to embed and compare
threshold = 0.85        # cosine similarity [0.0–1.0]; default: 0.8
embedding_model = "bge-small-en-v1.5"  # local model (~67 MB, downloaded once)
# embedding_url = "https://..."  # use OpenAI-compatible endpoint instead

[output_schema]         # optional; native TOML — JSON schema for structured output
```

## Minimal field.toml

```toml
name = "my-task"

[model]
name = "anthropic/claude-sonnet-4.6"

[prompt]
goal = "Create hello.py that prints 'Hello, World!'"

[environment]
root = "./workspace"

[boundary]
allow_write = ["hello.py"]
max_tokens = 80000
max_cost = "$1.00"
max_steps = 10

[[verifier]]
name = "works"
command = "python hello.py 2>&1 | grep -q 'Hello, World!'"
trigger = "on_stop"
description = "Must print 'Hello, World!'"
```

## Essential Commands

```bash
portlang new field.toml              # Scaffold a new field.toml using the flags to configure
portlang run field.toml              # Execute once
portlang check field.toml            # Validate configuration
portlang converge field.toml -n 10   # Run N times, measure reliability
portlang eval ./examples/            # Run all fields in a directory
portlang eval ./examples/ --resume   # Resume a previous eval, skipping fields that already passed
portlang list trajectories [field]   # List trajectories (--converged, --failed, --limit)
portlang list evals [dir]            # List eval runs (--limit)
portlang replay <id>                 # Step through a trajectory (q=quit, n=next, p=prev)
portlang diff <id-a> <id-b>          # Compare two trajectories
portlang report <field-name>         # Adaptation analysis across runs
portlang view trajectory <id>        # Open trajectory as interactive HTML
portlang view eval <id-or-dir>       # Open eval results dashboard (by run ID or directory)
portlang view diff <id-a> <id-b>     # Open trajectory comparison HTML
portlang view field <field-name>     # Open field adaptation report HTML
```

Add `--html` to `replay`/`diff` for HTML output. Add `--no-open` to any `view` command to skip opening the browser. See **reference/CLI.md** for full flag details.

## Key Patterns

### 1. Field Inheritance (shared model/boundary/tools across a suite)

If `../field.toml` exists, a child field can inherit from it automatically:

```toml
# parent/field.toml — shared config for all child fields
name = "parent"

[model]
name = "anthropic/claude-sonnet-4.6"
temperature = 0.5

[boundary]
network = "deny"
max_tokens = 100000
max_cost = "$1.00"
max_steps = 20

[[tool]]
type = "python"
file = "./tools/shared_utils.py"
```

```toml
# parent/task-a/field.toml — inherits model, boundary, and tools
name = "task-a"
model = "inherit"
boundary = "inherit"
tools = "inherit"

[prompt]
goal = "Do task A using the shared tools."
```

Inheritance eliminates duplication across eval suites. Override any section by defining it inline.

### 2. Structured Output (agent produces validated JSON)

Define `output_schema` as a JSON string. Schema validation is automatic — no separate verifier needed:

```toml
output_schema = '''
{
  "type": "object",
  "required": ["status", "file_count", "files", "summary"],
  "properties": {
    "status": {"type": "string", "enum": ["success", "failure"]},
    "file_count": {"type": "integer", "minimum": 0},
    "files": {"type": "array", "items": {"type": "string"}},
    "summary": {"type": "string"}
  }
}
'''
```

portlang validates the output against the schema, writes `output.json` to `/workspace`, and reports schema violations as failures. Add `[[verifier]]` entries only for additional business logic checks beyond schema conformance.

### 3. Multi-Layer Verifiers (fail fast with precise feedback)

Layer verifiers from coarse to fine — each one assumes the previous passed:

```toml
[[verifier]]
name = "compiled"
command = "python script.py 2>/dev/null"
trigger = "on_stop"
description = "script.py must run without errors"

[[verifier]]
name = "correct-output"
type = "levenshtein"
file = "output.txt"
expected = "42"
threshold = 1.0
trigger = "on_stop"
description = "output.txt must contain exactly '42'"
```

Verifiers run in order, stop on first failure. Use `output_schema` instead of json verifiers when the agent produces structured JSON output.

### 4. Smart Verifier Types

**Prefer typed verifiers.** They run in the portlang runtime — no packages required, no container dependencies. Fall back to shell verifiers only for logic that can't be expressed with a typed verifier, and only use tools guaranteed in the container baseline (see section 7).

```toml
# Fuzzy text match (tolerates minor differences)
[[verifier]]
type = "levenshtein"
name = "close-enough"
file = "output.txt"
expected = "The answer is 42."
threshold = 0.9
trigger = "on_stop"
description = "Output must be at least 90% similar to expected"

# Semantic match (meaning, not exact text)
[[verifier]]
type = "semantic"
name = "right-idea"
file = "summary.txt"
expected = "The model achieved high accuracy on the test set."
threshold = 0.85
trigger = "on_stop"
description = "Summary must convey the correct conclusion"
```

Local embedding model downloaded automatically (~67 MB, no API key required).

### 5. Scoped Boundaries

```toml
[boundary]
allow_write = ["output.json", "logs/*.txt"]
network = "deny"
max_tokens = 100000
max_cost = "$1.00"
max_steps = 20
```

### 6. Re-observation (keep context fresh)

```toml
[prompt]
goal = "..."
re_observation = [
  "echo '=== workspace ===' && ls -1 *.py *.txt 2>/dev/null | cat",
  "echo '=== tests ===' && python -m pytest --tb=no -q 2>&1 | tail -5",
]
```

Commands run before each agent step, injecting fresh state into context.

### 7. Custom Environment

```toml
[environment]
root = "./workspace"
packages = ["nodejs", "npm"]    # Install apt packages

# Or use a custom Dockerfile:
dockerfile = "./Dockerfile"

# Or a pre-built image:
image = "myregistry/myimage:latest"
```

**Default container baseline:** The container is minimal. Available by default: standard POSIX shell builtins, `bash`, `curl`, `wc`, `grep`, `cat`, `ls`, `find`. **Not available** unless added to `packages` or a custom image: `python3`, `node`, `jq`, `git`, and most other tools.

Shell verifiers run inside the container and are subject to the same constraints. **Prefer typed verifiers** (`type = "json"`, `"levenshtein"`, `"semantic"`) over shell verifiers whenever possible — they run natively in the portlang runtime and require nothing installed. Only use shell verifiers for checks that require container-side execution, and only invoke tools you've declared in `packages`.

### 8. Custom Tools

**Default tools (always available, no `[[tool]]` entry needed):**
- `bash` — run shell commands in the container
- `glob` — find files by pattern
- `write` — write files to allowed paths

Define `[[tool]]` entries only to add capabilities beyond these three.

**Shell tool:**
```toml
[[tool]]
type = "shell"
name = "word_count"
description = "Count words in a file"
command = "wc {path}"
input_schema = '{"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}'
```

**Python tool (auto-schema from type hints):**
```python
# tools/calculator.py
# /// script
# dependencies = [requests]
# ///
# uv auto-installs dependencies — no packages needed in field.toml

def execute(expression: str) -> dict:
    """Evaluate a math expression and return the result."""
    return {"result": eval(expression)}
```

```toml
[[tool]]
type = "python"
file = "./tools/calculator.py"   # relative to field.toml, not workspace
function = "execute"  # schema auto-extracted from type hints; omit to expose all functions
```

> **Python tool rules:**
> - Each tool file runs in isolation — tool files cannot import each other. Put all related logic in one file.
> - Declare third-party dependencies with a `# /// script` PEP 723 block at the top; `uv` installs them automatically.
> - File paths in `file =` are relative to `field.toml`, not the workspace root.

**Tool-first design for complex tasks:** For tasks involving multi-step API calls, data aggregation, or web scraping, write Python tools that encapsulate that logic before writing the field. The agent's `goal` should then be: call the tool, write the output file. This keeps steps under 5, cost under $0.05, and `allow_write` naturally minimal. Agents that try to do complex work through raw shell commands (curl pipes, temp files, bash scripts) burn budget and fail more often.

**MCP server (stdio):**
```toml
[[tool]]
type = "mcp"
name = "filesystem"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
transport = "stdio"
```

**MCP server (HTTP/SSE):**
```toml
[[tool]]
type = "mcp"
name = "stripe"
url = "https://mcp.stripe.com"
transport = "http"
headers = { Authorization = "Bearer ${STRIPE_KEY}" }
```

### 9. Batch Evaluation

```bash
portlang eval ./examples/
portlang view eval ./examples/   # Open interactive HTML dashboard
```

Useful for regression testing after changes.

## Debugging Workflow

1. **Run fails** → `portlang replay <id>` to see what happened
2. **Find failure point** → Check which verifier failed and at which step
3. **Non-determinism** → `portlang diff <id-a> <id-b>` to find divergence
4. **Visual debugging** → `portlang view trajectory <id>` for HTML view
5. **Optimize** → `portlang converge -n 10` to measure reliability
6. **Patterns** → `portlang report <field-name>` for adaptation analysis

## Common Issues

**Budget exhausted:**
- Start conservative: `max_cost = "$0.25"` for simple tasks, `$1.00` for network-heavy tasks; increase after profiling
- Increase `max_tokens` or reduce `max_steps` in `[boundary]`
- Simplify `re_observation` commands
- Check for tool error loops
- Move complex logic into Python tools so the agent does orchestration, not implementation

**Low convergence rate (<70%):**
- Strengthen verifiers (make expectations explicit)
- Tighten boundaries (restrict file access)
- Clarify goal in `[prompt]`
- Lower `temperature` (e.g., `temperature = 0.0`)

**Verifier always passes/fails:**
- Weak signal (>95% or <10% pass rate) — adjust verifier command

**Structured output not valid:**
- Add an explicit `[[verifier]]` to check `output.json`
- Ensure `[prompt].goal` names the required fields explicitly
- Use `temperature = 0.0` for consistent JSON output

## Reference Documentation

- **reference/CLI.md** - Full CLI reference (all commands and flags)
- **reference/verifier_patterns.md** - 20 real-world verifier examples
- **reference/custom_tools.md** - Shell, Python, MCP guides
- **reference/trajectory_analysis.md** - Advanced debugging
- **reference/field_recipes.md** - 8 complete field.toml examples

## Core Principles

1. **Boundaries are topology, not policy** - Make bad actions impossible, not discouraged
2. **Verifiers are runtime reward signals** - Not post-hoc checks, they steer behavior
3. **Context is finite** - Hard ceiling, no magic compression
4. **Trajectories are data** - Replay, diff, analyze distributions
5. **Engineer the space, not the searcher** - Agent policy is opaque, environment is yours

---

*GitHub: https://github.com/portofcontext/portlang*
