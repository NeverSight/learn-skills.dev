---
name: analyze-codebase-for-mcp
description: >
  Analyze an arbitrary codebase to identify functions, APIs, and data sources
  suitable for exposure as MCP tools, producing a tool specification document.
  Use when planning an MCP server for an existing project, auditing a codebase
  before wrapping it as an AI-accessible tool surface, comparing what a codebase
  can do versus what is already exposed via MCP, or generating a tool spec to
  hand off to scaffold-mcp-server.
license: MIT
allowed-tools: Read Grep Glob Bash
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: mcp-integration
  complexity: advanced
  language: multi
  tags: mcp, analysis, tool-design, codebase
---

# Analyze Codebase for MCP

Scan a codebase to discover functions, REST endpoints, CLI commands, and data access patterns that are good candidates for MCP tool exposure, then produce a structured tool specification document.

## When to Use

- Planning an MCP server for an existing project and need to know what to expose
- Auditing a codebase before wrapping it as an AI-accessible tool surface
- Comparing what a codebase can do versus what is already exposed via MCP
- Generating a tool specification document to hand off to `scaffold-mcp-server`
- Evaluating whether a third-party library is worth wrapping as MCP tools

## Inputs

- **Required**: Path to the codebase root directory
- **Required**: Target language(s) of the codebase (e.g., TypeScript, Python, R, Go)
- **Optional**: Existing MCP server code to compare against (gap analysis)
- **Optional**: Domain focus (e.g., "data analysis", "file operations", "API integration")
- **Optional**: Maximum number of tools to recommend (default: 20)

## Procedure

### Step 1: Scan Codebase Structure

1.1. Use `Glob` to map the directory tree, focusing on source directories:
   - `src/**/*.{ts,js,py,R,go,rs}` for source files
   - `**/routes/**`, `**/api/**`, `**/controllers/**` for endpoint definitions
   - `**/cli/**`, `**/commands/**` for CLI entry points
   - `**/package.json`, `**/setup.py`, `**/DESCRIPTION` for dependency metadata

1.2. Categorize files by role:
   - **Entry points**: main files, route handlers, CLI commands
   - **Core logic**: business logic functions, algorithms, data transformers
   - **Data access**: database queries, file I/O, API clients
   - **Utilities**: helpers, formatters, validators

1.3. Count total files, lines of code, and exported symbols to gauge project size.

**Expected:** A categorized file inventory with role annotations.

**On failure:** If the codebase is too large (>10,000 files), narrow the scan to specific directories or modules using the domain focus input. If no source files are found, verify the root path and language parameters.

### Step 2: Identify Exposed Functions and Endpoints

2.1. Use `Grep` to find exported functions and public APIs:
   - TypeScript/JavaScript: `export (async )?function`, `export default`, `module.exports`
   - Python: functions not prefixed with `_`, `@app.route`, `@router`
   - R: functions listed in NAMESPACE or `#' @export` roxygen tags
   - Go: capitalized function names (exported by convention)

2.2. For each candidate function, extract:
   - **Name**: function or endpoint name
   - **Signature**: parameters with types and defaults
   - **Return type**: what the function produces
   - **Documentation**: docstrings, JSDoc, roxygen, godoc
   - **Location**: file path and line number

2.3. For REST APIs, additionally extract:
   - HTTP method and route pattern
   - Request body schema
   - Response shape
   - Authentication requirements

2.4. Build a candidate list sorted by potential utility (public, documented, well-typed functions first).

**Expected:** A list of 20-100 candidate functions/endpoints with extracted metadata.

**On failure:** If few candidates are found, broaden the search to include internal functions that could be made public. If documentation is sparse, flag this as a risk in the output.

### Step 3: Evaluate MCP Suitability

3.1. For each candidate, assess against MCP tool criteria:

   - **Input contract clarity**: Are parameters well-typed and documented? Can they be described in a JSON Schema?
   - **Output predictability**: Does the function return structured data (JSON-serializable)? Is the return shape consistent?
   - **Side effects**: Does the function modify state (files, database, external services)? Side effects must be clearly labeled.
   - **Idempotency**: Is the operation safe to retry? Non-idempotent tools need explicit warnings.
   - **Execution time**: Will it complete within a reasonable timeout (< 30 seconds)? Long-running operations need async patterns.
   - **Error handling**: Does it throw structured errors or fail silently?

3.2. Score each candidate on a 1-5 scale:
   - **5**: Pure function, typed I/O, documented, fast, no side effects
   - **4**: Well-typed, documented, minor side effects (e.g., logging)
   - **3**: Reasonable I/O contract but needs wrapping (e.g., returns raw objects)
   - **2**: Significant side effects or unclear contract, needs substantial adaptation
   - **1**: Not suitable without major refactoring

3.3. Filter candidates to those scoring 3 or above. Flag score-2 items as "future candidates" requiring refactoring.

**Expected:** A scored and filtered candidate list with suitability rationale for each.

**On failure:** If most candidates score below 3, the codebase may need refactoring before MCP exposure. Document the gaps and recommend specific improvements (add types, extract pure functions, wrap side effects).

### Step 4: Design Tool Specifications

4.1. For each selected candidate (score >= 3), draft a tool specification:

```yaml
- name: tool_name
  description: >
    One-line description of what the tool does.
  source_function: module.function_name
  source_file: src/path/to/file.ts:42
  parameters:
    param_name:
      type: string | number | boolean | object | array
      description: What this parameter controls
      required: true | false
      default: value_if_optional
  returns:
    type: string | object | array
    description: What the tool returns
  side_effects:
    - description of any side effect
  estimated_latency: fast | medium | slow
  suitability_score: 5
```

4.2. Group tools into logical categories (e.g., "Data Queries", "File Operations", "Analysis", "Configuration").

4.3. Identify dependencies between tools (e.g., "list_datasets" should be called before "query_dataset").

4.4. Determine if any tools need wrappers to:
   - Simplify complex parameter objects into flat inputs
   - Convert raw return values to structured text or JSON
   - Add safety guards (e.g., read-only wrappers for database functions)

**Expected:** A complete YAML tool specification with categories, dependencies, and wrapper notes.

**On failure:** If tool specifications are ambiguous, revisit Step 2 to extract more detail from source code. If parameter types cannot be inferred, flag for manual review.

### Step 5: Generate Tool Spec Document

5.1. Write the final specification document with these sections:
   - **Summary**: Codebase overview, language, size, and analysis date
   - **Recommended Tools**: Full specifications from Step 4, grouped by category
   - **Future Candidates**: Score-2 items with refactoring recommendations
   - **Excluded Items**: Score-1 items with exclusion rationale
   - **Dependencies**: Tool dependency graph
   - **Implementation Notes**: Wrapper requirements, authentication needs, transport recommendations

5.2. Save as `mcp-tool-spec.yml` (machine-readable) and optionally `mcp-tool-spec.md` (human-readable summary).

5.3. If an existing MCP server was provided, include a gap analysis section:
   - Tools in the spec but not yet implemented
   - Implemented tools not in the spec (possibly stale)
   - Tools with specification drift (implementation diverges from spec)

**Expected:** A complete tool specification document ready for consumption by `scaffold-mcp-server`.

**On failure:** If the document exceeds reasonable size (>200 tools), split into modules with cross-references. If the codebase has no suitable candidates, produce a "readiness assessment" document with refactoring recommendations instead.

## Validation

- [ ] All source files in the target codebase were scanned
- [ ] Candidate functions have extracted names, signatures, and return types
- [ ] Each candidate has a suitability score with written rationale
- [ ] Tool specifications include complete parameter schemas with types
- [ ] Side effects are explicitly documented for every tool
- [ ] The output document is valid YAML (parseable by any YAML library)
- [ ] Tool names follow MCP conventions (snake_case, descriptive, unique)
- [ ] Categories and dependencies form a coherent tool surface
- [ ] Gap analysis is included when an existing MCP server was provided
- [ ] Future candidates section lists refactoring steps needed for score-2 items

## Common Pitfalls

- **Exposing too many tools**: AI assistants work best with 10-30 focused tools. Prioritize breadth of capability over depth. Resist exposing every public function.
- **Ignoring side effects**: A function that "just reads" but also writes to a log or cache still has side effects. Audit carefully with `Grep` for file writes, network calls, and database mutations.
- **Assuming type safety**: Dynamic languages (Python, R, JavaScript) may have functions with no type annotations. Infer types from usage patterns and tests, but flag uncertainty in the spec.
- **Missing authentication context**: Functions that work in an authenticated web request may fail when called via MCP without session context. Check for implicit auth dependencies such as session cookies, JWT tokens, or environment-injected credentials.
- **Over-engineering wrappers**: If a function needs a 50-line wrapper to be MCP-compatible, it may not be a good candidate. Prefer functions that map naturally to tool interfaces.
- **Neglecting error paths**: MCP tools must return structured errors. Functions that throw untyped exceptions need error-handling wrappers.
- **Conflating internal and external APIs**: Internal helper functions called by other internal code are poor MCP candidates. Focus on functions designed for external consumption or clear boundary APIs.
- **Skipping the gap analysis**: If an existing MCP server is provided, always compare the spec against current implementation. Without gap analysis, you risk duplicating work or missing stale tools.

## Related Skills

- `scaffold-mcp-server` - use the output spec to generate a working MCP server
- `build-custom-mcp-server` - manual server implementation reference
- `configure-mcp-server` - connect the resulting server to Claude Code/Desktop
- `troubleshoot-mcp-connection` - debug connectivity after deploying the server
- `review-software-architecture` - architecture review for tool surface design
- `security-audit-codebase` - security audit before exposing functions externally
