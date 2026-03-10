---
name: code-trace
description: |
  Interactive code execution path tracer that explains how code flows from entry point to output.
  Uses step-by-step navigation with AskUserQuestion to explore conditional branches and function calls.

  Use when:
  - User asks "How does X work in this codebase?"
  - User wants to understand HTTP request/response flow
  - User asks about middleware execution order
  - User wants to trace a function call chain
  - User asks "What happens when..." questions
  - User wants to learn how code paths connect

  Keywords: trace, flow, execution, path, call chain, middleware, request handling,
  what happens, how does, step through, follow the code
---

<essential_principles>
## How Code Tracing Works

This skill traces code execution paths interactively, letting you navigate through the codebase
like a debugger stepping through code - but with rich explanations at each step.

### Principle 1: Application Boundary

Trace ONLY application code. External dependencies (node_modules, vendor/) receive:
- A summary of what they do
- Link to official documentation
- NOT deep-traced into their internals

**Why**: External libraries can be 100K+ lines. Tracing into them wastes context and obscures
the actual application logic. The goal is understanding YOUR code, not library internals.

### Principle 2: Interactive Navigation

Every conditional branch becomes a user choice:

| Code Pattern | Presentation |
|--------------|--------------|
| `if/else` | "Path A: condition true" vs "Path B: condition false" |
| `switch` | One choice per case |
| `try/catch` | "Success path" vs "Error path" |
| `async/await` | Option to trace into called functions |

**Why**: Linear traces miss important paths. Interactive navigation lets users explore
exactly what they're interested in.

### Principle 3: Progressive Explanation

Each step includes:
1. **Location**: File + line range + function name
2. **Code**: Full source (no abbreviation)
3. **What**: Brief summary of what the code does
4. **Why**: Why this step exists in the flow
5. **Next**: What happens next (or choices if branching)

Use thinking markers (🤔🎯⚡📊💡🔐) for clarity.

### Principle 4: State Persistence

Trace state is stored in Serena Memory to enable:
- Resuming interrupted traces
- Backtracking to previous decision points
- Saving completed traces for future reference
</essential_principles>

<intake>
## What would you like to trace?

1. **Trace a request flow** - Follow HTTP request from receipt to response
2. **Trace a function call** - Follow a specific function through the codebase
3. **Resume previous trace** - Continue from where you left off

Please provide additional context:
- For request tracing: Which endpoint? (e.g., "POST /api/users")
- For function tracing: Which function? (e.g., "validateUser" or "src/utils/auth.ts:checkToken")

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "request", "HTTP", "route", "API", "endpoint", "POST", "GET" | `workflows/trace-request.md` |
| 2, "function", "call", specific function name | `workflows/trace-function.md` |
| 3, "resume", "continue", "previous" | Read Serena memory for `trace_session_*` |

## Before Starting Any Workflow

1. **Detect Framework**: Run `scripts/detect-framework.sh` to identify:
   - Express, Next.js (App/Pages), Fastify, Hono, NestJS, Koa, or generic

2. **Load Framework Patterns**: Read `references/framework-patterns.md` section for detected framework

3. **Prepare Serena**: Ensure Serena MCP is available for:
   - `find_symbol()` - Locate functions/handlers
   - `find_referencing_symbols()` - Find callers
   - `get_symbols_overview()` - Map module structure
   - `write_memory()` / `read_memory()` - State persistence

**After determining intent and framework, read the appropriate workflow and follow it.**
</routing>

<reference_index>
## References

All in `references/`:

| File | Content |
|------|---------|
| framework-patterns.md | Entry point detection and request flow for Express, Next.js, Fastify, etc. |
| control-flow-types.md | How to present if/switch/try/loops as interactive choices |
| explanation-style.md | Thinking markers, step format, summary format |
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| trace-request.md | Trace HTTP request from entry to response |
| trace-function.md | Trace a specific function's call chain |
</workflows_index>

<scripts_index>
## Scripts

| Script | Purpose |
|--------|---------|
| detect-framework.sh | Auto-detect project framework from package.json |

Usage:
```bash
./scripts/detect-framework.sh /path/to/project
# Output: express | nextjs-app | nextjs-pages | fastify | hono | nestjs | koa | generic
```
</scripts_index>

<success_criteria>
A successful code trace:
- [ ] Entry point correctly identified and explained
- [ ] Framework detected and appropriate patterns applied
- [ ] At least one branch point presented as interactive choice
- [ ] External dependencies summarized (not deep-traced)
- [ ] User navigated to terminal point OR chose to stop
- [ ] Path history shown in ASCII flowchart format
- [ ] Key insights collected and displayed
- [ ] Trace state available for resume (if user chose to save)
</success_criteria>

<boundaries>
## Boundaries

**Will:**
- Trace application code with full source display
- Explain each step with thinking markers
- Present conditional branches as interactive choices
- Summarize external dependencies at the boundary
- Persist trace state for resume capability

**Will Not:**
- Deep-trace into node_modules or external libraries
- Execute or run the code (read-only analysis)
- Modify any source files
- Make assumptions about runtime values (present all branches)
</boundaries>
