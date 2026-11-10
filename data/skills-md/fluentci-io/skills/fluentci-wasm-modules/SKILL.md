---
name: fluentci-wasm-modules
description: "Build and publish reusable CI/CD plugins as typed WebAssembly components with FluentCI. Use for pipeline as code, fluentci-module.toml, SDK-generated WIT, named function arguments, module dependencies, registry publishing, or migrating an explicitly selected Extism module."
license: MIT
---

# FluentCI modules

## Start from the project contract

Inspect existing module manifests, source, SDK lockfiles, runtime, and build
scripts. Respect local execution restrictions. New modules default to native
Wasm components; preserve an existing Extism runtime unless migration is requested.

When commands are permitted, use the installed CLI's help before scaffolding:

```sh
fluentci modules add --help
fluentci init --help
```

Create a workspace module with `fluentci modules add ci --sdk typescript`, or a
standalone module with `fluentci init ci --standalone --sdk typescript`. Use the
user's requested SDK. Rust, PureScript, ClojureScript, TypeScript, Python, Gleam,
Elixir, and ReScript are supported; check the installed CLI for later additions.
Do not introduce an Extism guest compiler into a component starter.

## Keep the compiled interface authoritative

Edit the generated source entry point and keep the starter's build tools and
lockfiles. Define typed input fields and return values, with source descriptions
for the function and its arguments. Rebuild to regenerate WIT, wrappers, and
metadata; do not manually maintain a second signature in JSON or WIT when the SDK
can derive it. See [component authoring](references/components.md).

Inspect both module help and function help after building when execution is allowed:

```sh
fluentci modules ci --json
fluentci run ci --help
fluentci run ci check --help
```

These can build/download modules; they are not effect-free validation commands.
Use an authorized, harmless function or a fixture to validate execution. For SDK
changes, use that SDK's formatter/typechecker/tests and the existing project build;
do not run unrelated publishing or deployment functions as a smoke test.

## Metadata and dependencies

Keep the module's own name, version, runtime, license, and optional metadata in
`fluentci-module.toml`. The workspace `[[modules]]` entry supplies its source and
local alias. See [manifests and dependencies](references/manifest-and-dependencies.md)
for installation, locks, Git subdirectories, and cross-module calls.

Wasm holds orchestration; commands run on the host. Provide required tools and
explicit task environment rather than assuming a module download installs them.
Use native task plans for dependency graphs and parallel work; an array of workflow
commands is sequential.

## Publish only within the requested scope

Publishing uploads an artifact and writes a release record to the account's PDS.
Prepare metadata and verify the selected account, artifact, and version before an
authorized publish. See [publishing](references/publishing.md) for credentials,
required fields, immutable releases, and recovering from an uncertain upload result.

[Components](https://docs.fluentci.io/guides/components/)
[SDK build commands](https://github.com/fluentci-io/fluentci#sdk-build-commands)
