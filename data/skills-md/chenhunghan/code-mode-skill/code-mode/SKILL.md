---
name: code-mode
description: >
  Add a "code mode" tool to an existing MCP server so LLMs can write small
  processing scripts that run against large API responses in a sandboxed
  runtime — only the script's compact output enters the LLM context window.
  Use this skill whenever someone wants to add code mode, context reduction,
  script execution, sandbox execution, or LLM-generated-code processing to
  an MCP server. Also trigger when users mention reducing token usage, shrinking
  API responses, running user-provided code safely, or adding a code execution
  tool to their MCP server — in any language (TypeScript, Python, Go, Rust, etc.).
---

# Code Mode for MCP Servers

## What is Code Mode?

When an MCP tool returns a large API response (e.g. listing 500 Kubernetes pods,
200 SCIM users, or thousands of GitHub issues), that entire payload enters the
LLM's context window — consuming tokens and degrading performance.

Code mode flips the approach: instead of dumping raw data into context, the LLM
writes a small processing script. The MCP server runs the script in a **sandboxed
runtime** against the raw data, and only the script's stdout enters context.

This works especially well with well-known APIs (SCIM, Kubernetes, GitHub, Stripe,
Slack, AWS, etc.) because the LLM already knows the response schema from training
data — it can write the extraction script in one shot without inspecting the data.

**Typical results: 65–99% context reduction.**

### Inspiration

- [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode-mcp/)
- [claude-context-mode](https://github.com/mksglu/claude-context-mode)

---

## How This Skill Works

This is an **interactive planning skill**. Work with the user step-by-step:

1. **Understand** their MCP server (language, framework, what tools return large data)
2. **Select** a sandbox that fits their server language and security needs
3. **Plan** the implementation together
4. **Implement** the code mode tool, sandbox executor, and benchmark
5. **Verify** with benchmarks comparing before/after context sizes

Do not jump ahead. Confirm each step with the user before proceeding.

---

## Step 1: Understand the Existing MCP Server

Ask the user (or discover by reading their codebase):

- **Server language**: TypeScript/JavaScript, Python, Go, Rust, or other?
- **MCP framework**: XMCP, FastMCP, mcp-go, custom, etc.?
- **Which tools return large responses?** (e.g. list users, get pods, search issues)
- **What APIs do they call?** Well-known APIs (SCIM, K8s, GitHub, Stripe) are ideal
  candidates because the LLM already knows the schema.
- **What languages should the sandbox support for script execution?**
  Usually JavaScript is sufficient. Python is a common second choice.

Summarize your understanding back to the user and confirm before moving on.

---

## Step 2: Select a Sandbox

The sandbox must be **isolated from the host filesystem and network by default**
and **secure by default**. Present the user with options that match their server
language, using the reference in `references/sandbox-options.md`.

### Quick Selection Guide

**If the server is TypeScript/JavaScript:**

| Sandbox | Script Language | Isolation | Size | Notes |
|---|---|---|---|---|
| `quickjs-emscripten` | JavaScript | WASM (no fs/net) | ~1MB | Lightweight, actively maintained, best default |
| `pyodide` | Python | WASM (no fs/net) | ~20MB | Full CPython in WASM, heavier |
| `isolated-vm` | JavaScript | V8 isolate (no fs/net) | ~5MB native | Fast, separate V8 heap, not WASM |

**If the server is Python:**

| Sandbox | Script Language | Isolation | Size | Notes |
|---|---|---|---|---|
| `RestrictedPython` | Python | AST-restricted compile | Tiny | Compiles to restricted bytecode, no I/O by default |
| `pyodide` (in-process WASM) | Python | WASM | ~20MB | Heavier but stronger isolation than RestrictedPython |
| `quickjs` (via `quickjs` PyPI) | JavaScript | WASM/native | Small | Run JS from Python |

**If the server is Go:**

| Sandbox | Script Language | Isolation | Size | Notes |
|---|---|---|---|---|
| `goja` | JavaScript | Pure Go interpreter | Zero CGO | No fs/net, widely used (used by Grafana) |
| `Wazero` | WASM guest (JS/Python compiled to WASM) | WASM runtime, pure Go | Zero CGO | Strongest isolation, runs any WASM module |
| `starlark-go` | Starlark (Python dialect) | Pure Go interpreter | Zero CGO | Deterministic, no I/O, used by Bazel |

**If the server is Rust:**

| Sandbox | Script Language | Isolation | Size | Notes |
|---|---|---|---|---|
| `boa_engine` | JavaScript | Pure Rust interpreter | No unsafe deps | ES2024 support, embeddable |
| `wasmtime` / `wasmer` | WASM guest | WASM runtime | Strong | Run any WASM module, strongest isolation |
| `deno_core` | JavaScript/TypeScript | V8-based | Larger | Full V8, powerful but heavier |
| `rustpython` | Python | Pure Rust interpreter | Moderate | Less mature but functional |

Read `references/sandbox-options.md` for detailed tradeoffs on each option.

**Present 2–3 options** to the user (filtered to their server language), explain
the tradeoffs briefly, and let them choose. If they're unsure, recommend the
lightest WASM-based option for their language.

---

## Step 3: Plan the Implementation

Once the sandbox is selected, create a concrete plan with the user. The plan
should cover these components:

### 3a. Code Mode Tool

A new MCP tool (e.g. `code_mode` or `<domain>_code_mode`) that accepts:

- **`command`** or **`args`**: The underlying API call / query to execute
  (e.g. kubectl args, SCIM endpoint + params, GraphQL query)
- **`code`**: The processing script the LLM writes
- **`language`** (optional): Script language, defaults to `javascript`

The tool handler:
1. Executes the underlying API call (reusing existing logic)
2. Passes the raw response as a `DATA` variable into the sandbox
3. Runs the script in the sandbox
4. Returns only the script's stdout, plus a size measurement line:
   `[code-mode: 18.0KB -> 6.2KB (65.5% reduction)]`

### 3b. Sandbox Executor

A utility module that:
- Initializes the chosen sandbox runtime
- Injects `DATA` (the raw API response as a string) into the sandbox
- Executes the user-provided script
- Captures stdout and returns it
- Enforces a timeout (e.g. 10 seconds)
- Handles errors gracefully (script syntax errors, runtime errors)

### 3c. Wiring

- Register the new tool in the MCP server's tool list
- Optionally gate behind an env var (ask the user if they want this)

### 3d. Benchmark

A benchmark script that compares tool output size vs. code-mode output size
across realistic scenarios. See `references/benchmark-pattern.md` for the
template.

**Present the plan to the user and confirm before implementing.**

---

## Step 4: Implement

Follow the confirmed plan. Implement in this order:

1. **Install the sandbox dependency** (e.g. `npm i quickjs-emscripten`)
2. **Create the executor module** — the sandbox wrapper
3. **Create the code mode tool** — the MCP tool handler
4. **Wire it into the server** — register the tool
5. **Create the benchmark script**

Keep the implementation minimal — don't over-abstract. The executor and tool
can each be a single file.

### Implementation Tips

- The `DATA` variable should always be a **string** (JSON-serialized). The
  script is responsible for parsing it if needed (`JSON.parse(DATA)` in JS,
  `json.loads(DATA)` in Python).
- Include the reduction measurement in every response so the user/LLM can
  see the savings: `[code-mode: {before}KB -> {after}KB ({pct}% reduction)]`
- Set a reasonable default timeout (10s) and memory limit if the sandbox
  supports it.
- Return clear error messages if the script fails — the LLM will use the
  error to fix its script on the next call.

---

## Step 5: Benchmark and Verify

After implementation, run the benchmark to verify code mode actually reduces
context size. Read `references/benchmark-pattern.md` for the full template.

The benchmark should:

1. **Generate or fetch realistic test data** — use faker/mock data if no live
   API is available, or hit a real endpoint if the user has one.
2. **Run each scenario through both paths:**
   - Regular tool response (full JSON)
   - Code mode with a representative extraction script
3. **Print a comparison table** showing before/after sizes and reduction %
4. **Print a total** across all scenarios

Present the benchmark results to the user. Typical expectations:
- Simple list extractions: 60–80% reduction
- Filtered queries (e.g. "only inactive users"): 90–99% reduction
- Aggregations (e.g. "count per department"): 95–99% reduction

---

## Reference Files

- `references/sandbox-options.md` — Detailed comparison of all sandbox options
  by server language, with security analysis and setup instructions
- `references/benchmark-pattern.md` — Benchmark script template and methodology
