---
name: keep-or-cut
description: Learn which pieces depend on each other, then keep only the ones your project needs.
plain: "Learn which pieces depend on each other, then cut the surfaces your project does not need."
diagram: |-
  smallest: CLI only
  cut code mode
  cut HTTP
  cut MCP
    code mode needs MCP
  cut XState
  cut devtools
  then fix what the
  compiler finds
---

# Keep or cut rat-stack

Delete interfaces your product will not use. Do not keep code because you might need it one day.

A capability is one named action with a contract and a server-side handler. The contract defines its name, input, output, failure, and metadata. A projection builds a callable interface from capabilities.

CLI means command-line interface. MCP (Model Context Protocol) lets an agent discover and call tools. Effect describes work with typed failures and required dependencies.

Read `AGENTS.md` first. Keep unrelated product work. Check imports and tests before deleting files.

## Smallest version: command line only

Keep these files:

- `packages/capability/src/contract.ts`
- `packages/capability/src/implement.ts`
- `packages/capability/src/to-command.ts`
- `packages/capability/src/call-watch.ts` and `packages/capability/src/actor-watch.ts`
- every module imported by these files or retained core code, and their tests
- all of `packages/core`
- the CLI composition needed by the projected command

`defineContract`, `implement`, and `toCommand` keep the shipped `stats` command working. `contract.ts` does not depend on the other interfaces.

For CLI only, delete:

- unused projections and their matching tests in `packages/capability/src` and `packages/capability/test`, only after tracing imports from the keep list

Keep `apps/cli/src/surfaces.ts` with only the `toCommand` composition and its imports. Remove these unused CLI interfaces:

- `catalog`, `openapi`, `serve`, and `mcp` commands from `apps/cli/src/command.ts`
- `apps/cli/test/serve.test.ts`
- catalog, OpenAPI, MCP, and code-mode cases from `apps/cli/test/cli.e2e.test.ts`

## Cut code mode

Delete:

- `packages/capability/src/catalog.ts`
- `packages/capability/src/code-mode.ts`
- `packages/capability/src/sandbox-error.ts`
- `packages/capability/src/sandbox-service.ts`
- `packages/capability/src/sandbox-subprocess.ts`
- `packages/capability/src/to-code-mode.ts`
- `packages/capability/test/catalog.test.ts`
- `packages/capability/test/sandbox.test.ts`
- `packages/capability/test/to-code-mode.test.ts`
- `codeMode` and `mcpServer.codeMode` from `apps/cli/src/surfaces.ts`
- the `catalog` command and `--code-mode` flag from `apps/cli/src/command.ts`
- catalog and code-mode cases from `apps/cli/test/cli.e2e.test.ts`
- the `./sandbox` and `./code-mode` exports from `packages/capability/package.json`

## Cut HTTP

Delete:

- `packages/capability/src/to-http-api.ts`, `packages/capability/src/http-api.ts`, and the HTTP adapter test
- the `./http-api` export from `packages/capability/package.json`
- `http`, `routes`, and `webServer` from `apps/cli/src/surfaces.ts`
- the `openapi` and `serve` commands from `apps/cli/src/command.ts`
- `apps/cli/test/serve.test.ts`
- the OpenAPI case from `apps/cli/test/cli.e2e.test.ts`

## Cut MCP

Delete:

- `packages/capability/src/to-toolkit.ts`, `packages/capability/src/toolkit.ts`, and the MCP adapter test
- `packages/capability/test/mcp-harness.ts`
- `tools` and `mcpServer` from `apps/cli/src/surfaces.ts`
- the `mcp` command from `apps/cli/src/command.ts`
- MCP cases from `apps/cli/test/cli.e2e.test.ts`
- the `./toolkit` export from `packages/capability/package.json`

Code mode imports `to-toolkit.ts`. Cutting MCP therefore cuts code mode too; apply both lists.

## Cut XState

This recipe applies only to a clone that has already removed interest and every other lifecycle except file inspection. `packages/core/src/interest-machine.ts` also depends on XState and `@xstate/effect`; replacing file inspection alone cannot remove those dependencies. Find every remaining import before removing either package. Keeping a lifecycle means keeping its runtime and `actor-watch.ts`.

Delete:

- `packages/core/src/inspect-machine.ts` and its test
- `xstate` and `@xstate/effect` from `packages/core/package.json`
- their `minimumReleaseAgeExclude` entries from `pnpm-workspace.yaml`
- `scripts/oxlint-plugin-xstate-effect.ts`
- its entry in `oxlint.config.ts`

Then call `FileInspector.inspect` directly from the capability handler in `packages/core/src/inspect-file.ts`.

## Cut devtools

Delete:

- `packages/devtools`
- `@rat-stack/devtools` from `apps/cli/package.json`
- `devtoolsRoutes`, `devtoolsWebServer`, `mcpServer.devtools`, and `mcpServer.devtoolsCodeMode` from `apps/cli/src/surfaces.ts`
- the `--devtools` flag from `apps/cli/src/command.ts`
- the devtools cases from `apps/cli/test/serve.test.ts` and `apps/cli/test/cli.e2e.test.ts`

In `apps/web`, swap `devtoolsRoutes` for `contentRoutes` in `src/dev/backend.ts`, point the `development` condition of `#devtools-overlay` in `apps/web/package.json` at `./src/features/shared/no-devtools.tsx`, and delete `src/dev/devtools`, `src/dev/client`, and `src/dev/features`. `vite dev` keeps serving search and read; `test/dev-content-routes.test.ts` covers that path.

`CallWatch`, `aroundHandlers`, `invokerFor`, and `watchActor` stay in `packages/capability`. Devtools supplies `CallWatch` when the application is assembled. It observes calls without wrapping capability lists; its default does nothing. `aroundHandlers` remains the explicit policy wrapper over one list. `invokerFor` calls capabilities for code mode. `watchActor` lets machines report to devtools without depending on it.

## Clean up after each cut

1. Remove stale exports from `packages/capability/src/index.ts` and any affected package barrel.
2. Remove stale imports, Layers, commands, and tests found by the compiler. A Layer builds services and supplies their construction dependencies. A service is a named interface for one job.
3. Update the package table in `AGENTS.md` so repo law matches the clone.
4. Refresh the lockfile and format intentional changes:

```sh
pnpm install
pnpm fix
pnpm turbo run check test build
```

Let the compiler and checks find every stale reference. Do not silence errors or delete unrelated tests.
