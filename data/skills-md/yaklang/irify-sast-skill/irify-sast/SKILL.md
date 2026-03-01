---
name: irify-sast
description: >
  IRify SAST — AI-powered static application security testing.
  Compile source code into SSA IR, then use SyntaxFlow DSL to trace data flow across function boundaries,
  detect vulnerabilities (SQLi, RCE, XXE), and answer questions like "where does user input go?".
  Supports 7 languages (Java, PHP, JS, Go, Python, C, Yak) and incremental compilation via ProgramOverLay.
  Requires yaklang MCP server: yak mcp -t ssa
allowed-tools:
  - mcp__yaklang-ssa__ssa_compile
  - mcp__yaklang-ssa__ssa_query
  - Read
  - Glob
  - Grep
---

# IRify SAST

Deep static analysis skill powered by IRify's SSA compiler and SyntaxFlow query engine.

## Prerequisites

This skill requires the yaklang MCP server. Configure it in your agent's MCP settings:

```toml
# Codex: ~/.codex/config.toml
[mcp_servers.yaklang-ssa]
command = "yak"
args = ["mcp", "-t", "ssa"]
```

```json
// Claude Code / Cursor / others
{ "command": "yak", "args": ["mcp", "-t", "ssa"] }
```

## Workflow: Engine-First (sf → read → rg)

**CRITICAL**: Always follow the **Engine-First** funnel model. The SSA engine sees cross-procedure data flow across all files simultaneously — grep cannot. Do NOT use grep/rg to build a "candidate file pool" before querying. Instead, let the engine be your radar first.

### Step 1: Compile (once per project, auto-cached)

```
ssa_compile(target="/path/to/project", language="java", program_name="MyProject")
→ full compilation, returns program_name
```

**Auto Cache**: If the program was already compiled and source files haven't changed, the engine returns `[Cache Hit]` instantly — no recompilation. Always provide a `program_name` to enable caching.

### Step 2: Query — use SyntaxFlow as the global radar

Directly compose and execute SyntaxFlow rules against the compiled IR. Do NOT pre-scan with grep to find candidates.

```
ssa_query(program_name="MyProject", rule="<SyntaxFlow rule>")
```

The engine traverses the entire SSA graph in memory, crossing all file boundaries. One query covers what would take dozens of grep commands, with zero false positives on data flow.

### Step 3: Read — use Read as the microscope

After `ssa_query` returns concrete file paths and line numbers, use `Read` to examine surrounding context (±20 lines). Verify whether the hit is real business code or dead/test code.

### Step 4: Grep — use Grep/Glob only for non-code files

Use Grep/Glob **only** for content that the SSA engine does not process:
- Configuration files (`.yml`, `.xml`, `.properties`, `logback.xml`)
- Static resources, templates, build scripts
- Quick name/path lookups when you already know the exact string

**NEVER** use Grep to search for data flow patterns in source code — that is what `ssa_query` is for.

### Incremental Compile (when code changes)

```
ssa_compile(target="/path/to/project", language="java", base_program_name="MyProject")
→ only changed files recompiled, ProgramOverLay merges base + diff layers
→ returns NEW program_name for subsequent queries
```

**IMPORTANT**: Use `base_program_name` for incremental compilation. `re_compile=true` is a full recompile that discards all data — only use it to start completely fresh.

### Self-Healing Query (auto-retry on syntax error)

When `ssa_query` returns a SyntaxFlow parsing error:
1. **DO NOT** apologize to the user or ask for help
2. Read the error message — it contains the exact parse error position and expected tokens
3. Fix the SyntaxFlow rule based on the error
4. Re-invoke `ssa_query` with the corrected rule
5. Repeat up to **3 times** before reporting failure
6. If all retries fail, show the user: the original rule, each attempted fix, and the final error

## Critical: Follow User Intent

**DO NOT** automatically construct source→sink vulnerability rules unless the user explicitly asks for vulnerability detection.

- User asks "find user inputs" → write a **source-only** rule, list all input endpoints
- User asks "find SQL injection" → write a **source→sink** taint rule
- User asks "where does this value go" → write a **forward trace** (`-->`) rule
- User asks "what calls this function" → write a **call-site** rule

### Source-Only Query Examples (Java)

When the user asks about user inputs, HTTP endpoints, or controllable parameters:

```syntaxflow
// Find all Spring MVC controller handler methods
*Mapping.__ref__?{opcode: function} as $endpoints;
alert $endpoints;
```

```syntaxflow
// Find all user-controllable parameters in Spring controllers
*Mapping.__ref__?{opcode: function}<getFormalParams>?{opcode: param && !have: this} as $params;
alert $params;
```

```syntaxflow
// Find GetMapping vs PostMapping endpoints separately
GetMapping.__ref__?{opcode: function} as $getEndpoints;
PostMapping.__ref__?{opcode: function} as $postEndpoints;
alert $getEndpoints;
alert $postEndpoints;
```

### Source→Sink Query Examples (only when user asks for vulnerability detection)

```syntaxflow
// RCE: trace user input to exec()
Runtime.getRuntime().exec(* #-> * as $source) as $sink;
alert $sink for {title: "RCE", level: "high"};
```

```syntaxflow
// SQL Injection (MyBatis): detect ${} unsafe interpolation in XML mappers / annotations
// <mybatisSink> is a dedicated NativeCall that finds all MyBatis ${} injection points
<mybatisSink> as $sink;
$sink#{
    until: `* & $source`,
}-> as $result;
alert $result for {title: "SQLi-MyBatis", level: "high"};
```


## Proactive Security Insights

After running a query and finding results, **proactively** raise follow-up questions and suggestions. Do NOT just dump results and stop.

### When vulnerabilities are found:

1. **Suggest fix**: "This exec() call receives unsanitized user input. Consider using a whitelist or ProcessBuilder with explicit argument separation."
2. **Ask related questions**:
   - "Should I check if there are other endpoints that also call `Runtime.exec()`?"
   - "Want me to trace whether any input validation/sanitization exists between the source and sink?"
   - "Should I look for similar patterns in other controllers?"
3. **Cross-reference**: If one vulnerability type is found, proactively scan for related types:
   - Found RCE → "I also checked for SSRF and found 2 potential issues. Want details?"

### When no results are found:

1. Don't just say "no results" — explain WHY:
   - "No direct `exec()` calls found, but I see `ProcessBuilder` usage. Want me to check those instead?"
   - "The query matched 0 sinks. This could mean the code uses a framework abstraction — want me to search for framework-specific patterns?"
2. Suggest alternative queries

### When results are ambiguous:

1. Ask for clarification: "I found 8 data flow paths to `executeQuery()`, but 5 use parameterized queries (safe). Want me to filter to only the 3 using string concatenation?"

## Companion Reference Files

When writing SyntaxFlow rules, read these files using the `Read` tool for syntax help and real-world examples:

| File | When to Read | Path (relative to this file) |
|---|---|---|
| **NativeCall Reference** | When writing rules that need `<nativeCallName()>` functions — all 40+ NativeCall functions with syntax and examples | `nativecall-reference.md` |
| **SyntaxFlow Examples** | When writing new rules — 20+ production rules covering Java/Go/PHP/C, organized by vulnerability type | `syntaxflow-examples.md` |

**Workflow**: 
1. Read `syntaxflow-examples.md` to find a similar rule pattern
2. Need a NativeCall? Read `nativecall-reference.md`
3. Compose and execute via `ssa_query`

## SyntaxFlow Quick Reference

### Search & Match

```
documentBuilder          // variable name
.parse                   // method name (dot prefix)
documentBuilder.parse    // chain
*config*                 // glob pattern
/(get[A-Z].*)/           // regex pattern
```

### Function Call & Parameters

```
.exec()                           // match any call
.exec(* as $params)               // capture all params
.parse(*<slice(index=1)> as $a1)  // capture by index
```

### Data Flow Operators

| Operator | Direction | Use |
|----------|-----------|-----|
| `#>` | Up 1 level | Direct definition |
| `#->` | Up recursive | **Trace to origin** — "where does this COME FROM?" |
| `->` | Down 1 level | Direct usage |
| `-->` | Down recursive | **Trace to final usage** — "where does this GO TO?" |

```
.exec(* #-> * as $source)            // trace param origin
$userInput --> as $sinks              // trace where value goes
$sink #{depth: 5}-> as $source       // depth-limited trace
$val #{
  include: `*?{opcode: const}`
}-> as $constSources                  // filter during trace
$sink #{
  until: `* & $source`,              // stop when reaching source
}-> as $reachable
```

### Filters `?{...}`

```
$vals?{opcode: call}                // by opcode: call/const/param/phi/function/return
$vals?{have: 'password'}            // by string content
$vals?{!opcode: const}              // negation
$vals?{opcode: call && have: 'sql'} // combined
$factory?{!(.setFeature)}           // method NOT called on value
```

### Variable, Check & Alert

```
.exec() as $sink;                                      // assign
check $sink then "found" else "not found";             // assert
alert $sink for { title: "RCE", level: "high" };       // mark finding
$a + $b as $merged;                                    // union
$all - $safe as $vuln;                                 // difference
```

### NativeCall (40+ built-in functions)

Most commonly used — see `nativecall-reference.md` for full list:

```
<include('rule-name')>         // import lib rule
<typeName()>                   // get short type name
<fullTypeName()>               // get full qualified type name
<getReturns>                   // function return values
<getFormalParams>              // function parameters
<getFunc>                      // enclosing function
<getCall>                      // find call sites
<getCallee>                    // get called function
<getObject>                    // parent object
<getMembers>                   // object members
<name>                         // get name
<slice(index=N)>               // extract by index
<mybatisSink>                  // MyBatis SQL injection sinks
<dataflow(include=`...`)>      // filter data flow paths
```

## Tips

1. `#->` = "where does this come from?", `-->` = "where does this go?"
2. Use `*` for params, don't hardcode names
3. SSA resolves assignments: `a = getRuntime(); a.exec(cmd)` = `getRuntime().exec(cmd)`
4. Use `opcode` filters to distinguish constants / parameters / calls
5. Combine `check` + `alert` for actionable results
6. After code changes, use `base_program_name` (not `re_compile`) for fast incremental updates
7. Before writing a new rule, **read `syntaxflow-examples.md`** to find similar patterns
8. When unsure about a NativeCall, **read `nativecall-reference.md`** for usage and examples
