---
name: ballerina
description: Writes, runs, tests, debugs, and deploys Ballerina programs and integrations.
  Use when the user asks to write, create, implement, update, or fix Ballerina code; create
  or set up a new Ballerina project or package; build an HTTP service, API, GraphQL service,
  or integration in Ballerina; run, test, or build a Ballerina project; add a library or
  dependency; debug, diagnose, or explain a Ballerina compile error, runtime panic, stack
  trace, or failing integration; work with a .bal file, Ballerina.toml, Dependencies.toml,
  or Config.toml; run a bal command; generate Ballerina code from an OpenAPI or proto
  specification; deploy a Ballerina service to Docker, Kubernetes, or a GraalVM native
  image; or when the user does not have Ballerina installed and needs help setting it up.
---

## Creating a New Project

When the user asks to create a new project, service, or program from scratch:

```bash
bal new <project-name>   # scaffolds main.bal + Ballerina.toml
cd <project-name>
```

- Read the generated `Ballerina.toml` to understand the package (name, org, version)
- For a workspace (multiple packages in one repo), see [code-rules.md](code-rules.md) and the workspace rules it routes to

## Writing Ballerina Code

**Step 1 — Read existing code and plan file layout**: Read `.bal` files and `Ballerina.toml` to understand the project and its existing layout. Place new code in the file that fits its concern rather than everything in `main.bal` (see [code-rules.md](code-rules.md) for file organization).

**Step 2 — Discover libraries if needed**: If the task needs an external connector or library you don't know, invoke the `library` agent — give it the full task (including auth and trigger/event details) so its first summary already covers the client or `listener` constructor and the auth/connection config you'll need. Add the returned `import` to your `.bal` file; `bal build` resolves the dependency from Central. Trust the summary's API shapes — don't `bal pull` or read package source to double-check them; if a detail is genuinely missing, ask the `library` agent rather than guessing.
- Need several libraries? Invoke the `library` agent for each **in parallel** (multiple agent calls in one step, or run them in the background) — the lookups are independent. Meanwhile keep doing other independent work (scaffold the project, read existing `.bal` files, plan the file layout), and fold in each summary as it returns. Don't block on one lookup before starting the next.
- When both a `ballerinax/*` connector (with its own listener) and a standalone `trigger.*` package cover the same events, always prefer the connector — `trigger.*` packages are being superseded (don't judge by modified date).
- No `library` agent (non–Claude Code agents)? Use `bal` directly: `bal search <keyword>`, then `bal pull <org/name>` and read its sources under `~/.ballerina/repositories/central.ballerina.io/bala/<org>/<name>/<version>/<platform>/modules/<name>/` — glob both `<version>` and `<platform>` (`any` for pure-Ballerina packages, otherwise a JDK target such as `java21`, `java17` or `java11`), and grep for the symbol rather than assuming a filename.

**Step 3 — Write the code**: **Strictly follow the rules in [code-rules.md](code-rules.md)** — check your code against them as you write. That file covers every Ballerina program and ends with a table routing to domain rules (`rules/http.md`, `rules/messaging.md`, `rules/sql.md`, `rules/workspace.md`, `rules/tests.md`); read the ones your task touches **before** writing that part, and only those. If the Ballerina language server (LSP) is available, use the `LSP` tool while writing — `hover` to confirm a symbol's type/signature, `goToDefinition`/`goToImplementation` to inspect an API's real shape, `documentSymbol`/`workspaceSymbol` to locate declarations. It provides navigation/intelligence; `bal build` in Step 4 is the error check. Key rules:
- Use records for all data — never `json` or `map<json>` directly
- Descriptive identifiers — no single letters or bare abbreviations; two-word camelCase is the norm
- Named arguments for every function/method call

**Step 4 — Validate**: Run `bal build`. Fix every error before moving on. Repeat until clean. If an error is about a library's own API (wrong method, listener, or service signature), re-consult the `library` agent's API summary — or ask it for the specific detail you're missing — rather than re-guessing.

For langlib API quick reference: [langlib-reference.md](langlib-reference.md)

## Running and Testing

- Test request → `bal test`; otherwise → `bal run`
- Always run `bal build` first — if errors, stop and report each one with file and line number
- A service started with `bal run` does not exit on its own — stop it when done
- On test: fix failures and re-run until clean

When the program needs a broker, database, or other server, see [rules/integration-testing.md](rules/integration-testing.md) before calling the work done.

## Ballerina Not Installed

If a `bal` command fails because Ballerina is not installed, read [setup.md](setup.md) for installation instructions.

## Errors and Unexpected Behavior

When `bal build` reports an error, a program panics at runtime, or behavior is unexpected, read [troubleshooting/index.md](troubleshooting/index.md) to find the matching topic file. **Do not preload every troubleshooting file** — the index is a router that points to the one relevant file for the symptom.
