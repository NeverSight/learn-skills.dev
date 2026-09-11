---
name: context-compress
description: |
  Use context-compress tools (execute, execute_file) instead of Bash/cat when processing
  large outputs. Trigger phrases: "analyze logs", "summarize output", "process data",
  "parse JSON", "filter results", "extract errors", "check build output",
  "analyze dependencies", "process API response", "large file analysis",
  "extract elements", "page snapshot", "browser snapshot", "take a snapshot",
  "DOM structure", "inspect page", "form fields", "element selectors",
  "web page structure", "accessibility tree", "Playwright snapshot",
  "run tests", "test output", "coverage report", "git log", "recent commits",
  "diff between branches", "list containers", "pod status", "disk usage",
  "fetch docs", "API reference", "index documentation", "hit endpoint",
  "call API", "check response", "query results", "show tables",
  "find TODOs", "count lines", "codebase statistics", "security audit",
  "outdated packages", "dependency tree", "cloud resources", "CI/CD output".
  Also triggers on ANY MCP tool output (Playwright, Context7, GitHub API) that
  may exceed 20 lines, and any operation where output size is uncertain.
  Subagent routing is handled automatically via PreToolUse hook — no manual tool names needed in prompts.
---

# Context Compress: Default for All Large Output

## MANDATORY RULE

**Default to context-compress for ALL commands. Only use Bash for guaranteed-small-output operations.**

Bash whitelist (safe to run directly):
- **File mutations**: `mkdir`, `mv`, `cp`, `rm`, `touch`, `chmod`
- **Git writes**: `git add`, `git commit`, `git push`, `git checkout`, `git branch`, `git merge`
- **Navigation**: `cd`, `pwd`, `which`
- **Process control**: `kill`, `pkill`
- **Package management**: `npm install`, `npm publish`, `pip install`
- **Simple output**: `echo`, `printf`

**Everything else → `execute` or `execute_file`.** Any command that reads, queries, fetches, lists, logs, tests, builds, diffs, inspects, or calls an external service.

**When uncertain, use context-compress.** Every KB of unnecessary context reduces the quality and speed of the entire session.

## Decision Tree

```
About to run a command / read a file / call an API?
│
├── Command is on the Bash whitelist?
│   └── Use Bash
│
├── Output MIGHT be large or you're UNSURE?
│   └── Use context-compress execute or execute_file
│
├── Fetching web documentation or HTML page?
│   └── Use fetch_and_index → search
│
├── Using Playwright (navigate, snapshot, console, network)?
│   └── ALWAYS use filename parameter to save to file, then:
│       browser_snapshot(filename) → index(path) or execute_file(path)
│
├── Processing output from another MCP tool?
│   ├── Output already in context? → Use it directly
│   ├── Need to search multiple times? → Save to file → index(path) → search
│   └── One-shot extraction? → Save to file → execute_file(path)
│
└── Reading a file to analyze/summarize (not edit)?
    └── Use execute_file (file loads into FILE_CONTENT, not context)
```

## When to Use Each Tool

| Situation | Tool | Example |
|-----------|------|---------|
| Hit an API endpoint | `execute` | `fetch('http://localhost:3000/api/orders')` |
| Run CLI that returns data | `execute` | `gh pr list`, `aws s3 ls`, `kubectl get pods` |
| Run tests | `execute` | `npm test`, `pytest`, `go test ./...` |
| Git operations | `execute` | `git log --oneline -50`, `git diff HEAD~5` |
| Read a log file | `execute_file` | Parse access.log, error.log, build output |
| Read a data file | `execute_file` | Analyze CSV, JSON, YAML, XML |
| Fetch web docs | `fetch_and_index` | Index React/Next.js/Zod docs, then search |

## Language Selection

| Situation | Language | Why |
|-----------|----------|-----|
| HTTP/API calls, JSON | `javascript` | Native fetch, JSON.parse, async/await |
| Data analysis, CSV, stats | `python` | csv, statistics, collections, re |
| Shell commands with pipes | `shell` | grep, awk, jq, native tools |
| File pattern matching | `shell` | find, wc, sort, uniq |

## Search Query Strategy

- BM25 uses **OR semantics** — results matching more terms rank higher automatically
- Use 2-4 specific technical terms per query
- **Always use `source` parameter** when multiple docs are indexed
- **Always use `queries` array** — batch ALL search questions in ONE call:
  - `search(queries: ["transform pipe", "refine superRefine"], source: "Zod")`
  - NEVER make multiple separate search() calls

## Critical Rules

1. **Always console.log/print your findings.** stdout is all that enters context.
2. **Write analysis code, not just data dumps.** Analyze first, print findings.
3. **Be specific in output.** Print bug details with IDs, line numbers, exact values.
4. **For files you need to EDIT**: Use the normal Read tool.
5. **For Bash whitelist commands only**: Use Bash. Everything else → context-compress.
6. **Never use `index(content: large_data)`.** Use `index(path: ...)` to read files server-side.
7. **Always use `filename` parameter** on Playwright tools.

## Subagent Usage

Subagents automatically receive context-compress tool routing via a PreToolUse hook. You do NOT need to manually add tool names to subagent prompts — the hook injects them.

## Anti-Patterns

- Using `curl` via Bash → Use `execute` with fetch or `fetch_and_index`
- Using `cat large-file` → Use `execute_file` instead
- Piping Bash output through `| head -20` → Use `execute` to analyze ALL data
- Running `npm test` via Bash → Use `execute` to capture and summarize
- Calling `browser_snapshot()` WITHOUT `filename` → Always use `filename` parameter
- Passing large data to `index(content: ...)` → Always use `index(path: ...)`
