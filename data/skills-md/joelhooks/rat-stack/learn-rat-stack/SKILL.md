---
name: learn-rat-stack
updated: "2026-10-06"
description: Trace a capability through Effect, XState, five projections, the CLI, and Alchemy. Try hosted search and read.
plain: "Trace one action from its contract through a handler, a service, a machine, five surfaces, the CLI and the cloud."
diagram: |-
  contract
    │ handler
    │ service + machine
    ▼
  one capability
  ├ CLI
  ├ HTTP
  ├ MCP
  ├ code mode
  └ RPC
---

# Learn the stack

Start with `inspectFile`, a [capability](/systems/capabilities): one named action with a contract and a server-side handler. The [contract](/systems/capabilities) defines its name, input, output, failure, and metadata. The handler implements the action.

A service is a named interface for one job. A machine defines states and the events that permit movement between them. A [projection](/lore/one-capability-every-surface) builds a callable interface from capabilities.

Follow these parts, then try the hosted content tools.

Read [Effect basics](/lore/effect-basics) before this trace if the computation model is new. For implementation tasks, use [services](/lore/services-capture-dependencies), [Layer composition](/lore/layers-make-dependencies-explicit), and [testing](/lore/tests-that-earn-their-place).

## The pieces

- Effect describes work with typed failures and required dependencies.
- Schema defines accepted values and their runtime checks.
- A Layer builds services and supplies their construction dependencies.
- XState owns finite lifecycles. The Effect bridge runs their declared actors.
- TypeScript 7 and Effect diagnostics check types and Effect usage.
- Oxlint, Oxfmt, Vitest, and lefthook enforce [the fence](/lore/the-fence): checks and hooks that reject prohibited code and shortcuts.
- pnpm and Turborepo connect packages and cache checks.
- Alchemy declares the cloud. Follow [learn Alchemy](/skills/learn-alchemy) for the deployment graph.

## One action, five interfaces

```text
                     ┌─ CLI
                     ├─ HTTP
One Capability ──────┼─ MCP
                     ├─ code mode
                     └─ RPC
```

A [projection](/lore/one-capability-every-surface) exposes the same action through another interface. RPC serves browser clients. [Code mode](/lore/one-program-can-replace-several-tool-calls) lets agents compose calls in one program.

All five interfaces use one handler.

## Trace one action

The CLI uses `inspectFile`. The hosted site uses a separate content registry.

### 1. Define the contract

The [contract](/systems/capabilities) names the action and its input, output, and failure schemas.

```ts repo=rat-stack path=packages/core/src/contracts.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=155-163 {155,158-163}

```

`FileStatsError` belongs to the interface. The annotations mark a repeatable, read-only action.

### 2. Bind one handler

`implement` binds the contract to `runInspectMachine`. The registry includes the resulting [capability](/systems/capabilities).

```ts repo=rat-stack path=packages/core/src/inspect-file.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=7-11 {7-9,11}

```

The handler starts a machine to read the file.

### 3. Put file work in a service

`FileInspector.make` captures the file system. Its `inspect` method reads bytes and maps file errors to `FileStatsError`.

```ts repo=rat-stack path=packages/core/src/file-inspector.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=14-29 {15,20-24,28}

```

The service exposes its [Layer](/lore/layer-constructor-pattern) beside the implementation. This follows [hexagonal architecture](/lore/hexagonal-architecture): composition supplies the file-system dependency.

```ts repo=rat-stack path=packages/core/src/file-inspector.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=31-35 {34}

```

Callers ask the service to inspect a path. Composition chooses the file-system implementation.

### 4. Give the lifecycle named states

A declared `fromEffect` actor calls `FileInspector`.

```ts repo=rat-stack path=packages/core/src/inspect-machine.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=26-30 {26,28}

```

The machine starts in `reading`. It finishes in `inspected` or `unreadable`.

```ts repo=rat-stack path=packages/core/src/inspect-machine.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=40-64 {40,43,51,57,59,62}

```

### 5. Project the registered actions

The command-line interface (CLI) projects the same `capabilities` list for each server interface.

```ts repo=rat-stack path=apps/cli/src/surfaces.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=21-32 {21,23,25,29}

```

The RPC [projection](/lore/one-capability-every-surface) derives contracts from its supplied capabilities.

```ts repo=rat-stack path=packages/capability/src/to-rpc.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=24-27 {24,27}

```

A projection takes a registry and reuses its domain handlers.

### 6. Connect the CLI

`toCommand` derives each command. `inspectFile` also gets the `stats` alias.

```ts repo=rat-stack path=apps/cli/src/command.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=20-30 {23-27}

```

The entry point supplies the service [Layer](/lore/layer-constructor-pattern) and Node services. It denies [approval](/systems/capabilities) by default.

```ts repo=rat-stack path=apps/cli/src/cli.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=16-22 {18,20}

```

The command keeps the shared handler.

### 7. Compose the cloud

An Alchemy Stack groups one cloud infrastructure program and its outputs. Alchemy declares the Stack, Cloudflare providers, and state. The Stack includes `Mischief` and `Website`.

```ts repo=rat-stack path=apps/infra/alchemy.run.ts at=5c0f78e03d69ff9ea00f6b95d02cc36a3de91a0b lines=12-18,114-119 {12,15-16,114-115}

```

The Stack deploys the cloud applications. The Node file-inspection CLI runs separately.

## Try hosted search and read

Use [POST /api/execute](/llms.txt#run-code-one-program-instead-of-several-calls) for [code mode](/lore/one-program-can-replace-several-tool-calls). The [agent guide](/llms.txt) documents this search → read program:

```js
const found = await tools.search({ query: "cartridges", limit: 1 });
const page = await tools.read({ id: found.matches[0].id });
return { title: page.title, id: page.id };
```

Send it as a JSON `code` string:

```sh
curl --request POST 'https://ratstack.sh/api/execute' \
  --header 'content-type: application/json' \
  --data '{"code":"const found = await tools.search({ query: \"cartridges\", limit: 1 }); const page = await tools.read({ id: found.matches[0].id }); return { title: page.title, id: page.id };"}'
```

`read` takes the exact ID from `search`. This hosted program reads site content.

## Read before changing a piece

1. Read [`AGENTS.md`](/AGENTS.md) for pins, boundaries, and [the fence](/lore/the-fence).
2. Read [VISION.md](/VISION.md) for intent.
3. Read the package you plan to change.
4. Before Effect or XState work, read `node_modules/effect/AGENTS.md` and the pinned sources listed in repo law.

In a copied product repo, replace the template's product notes and rules. Keep the stack lessons that still serve the product.

Follow repo law and pinned code when an example is stale.

## Pick the next skill

- Add schemas and a shared action: [`add-a-capability`](/skills/add-a-capability).
- Model a lifecycle: [add a lifecycle machine](/skills/add-a-lifecycle-machine).
- Remove an interface: [keep or cut](/skills/keep-or-cut).
- Follow the cloud footprint: [learn Alchemy](/skills/learn-alchemy).

## Finish

Run the full gate:

```sh
pnpm turbo run check test build
```

Fix failures. Keep [the fence](/lore/the-fence) intact.

Check deployment separately from the gate.
