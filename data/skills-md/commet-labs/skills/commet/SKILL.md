---
name: commet
description: Integrate and maintain Commet billing with the installed Node, Python, Go, Java, or PHP SDK and the Next.js, AI SDK, Better Auth, or CLI integrations. Use for subscriptions, usage, seats, checkout, customer portal, webhooks, feature access, payments, migrations, errors, or any repository that imports a Commet package. Resolve the version-matched installed documentation before editing and use doctor evidence when the local Commet CLI is available.
---

# Commet integration

Treat the installed SDK as the contract. This skill sequences the work; it does not carry a copy of the API surface.

## Resolve installed context

Before changing an integration:

1. Inspect dependency manifests and lockfiles for every Commet SDK, integration package, CLI, direct REST call, and explicit API or webhook version.
2. Identify the package actually imported by the target application. If multiple versions are installed, do not assume the newest one is active.
3. Resolve `docs/manifest.json` from that installed artifact, read the manifest entrypoint, and then read only the relevant generated reference and Platform documents named by the manifest.
4. Read generated types from the same installed artifact when the task depends on an exact request, response, error, or webhook shape.
5. If the installed artifact has no documentation, stop and report the exact package and version. Do not silently substitute current web documentation for an older installed contract.

Use the package manager rather than a source checkout to locate the artifact:

| Ecosystem | Installed documentation |
| --- | --- |
| Node | `node_modules/@commet/node/docs/` plus the installed integration package README |
| Python | Resolve the installed `commet` module, then use its `docs/` directory |
| Go | Read the Commet module path from `go.mod`, resolve it with `go list -m -f '{{.Dir}}'`, then use `docs/` |
| Java | Resolve the `co.commet:commet-java` dependency and read `commet/docs/` from its JAR resources |
| PHP | `vendor/commet/commet-php/docs/` |

For a new integration with no SDK installed, install the requested language package first when the user asked for implementation. Then read the documentation from that installed package before writing integration code.

## Use Node diagnostics

When the `commet` CLI executable is present, run from the project root:

```bash
commet doctor --output agent
```

Parse the JSON even when the command exits non-zero. Use its `status`, `apiVersion`, check `code`, `evidence`, `impact`, and `action`; never inspect or print secret values. Resolve failed package, documentation, compatibility, API-version, or project-context checks before relying on the integration.

If a Node package is installed but the CLI is not, report that doctor evidence is unavailable and continue with the installed package documentation. Do not install or execute a package implicitly. When the user asks to add the CLI, resolve its compatible installation from the installed documentation first.

Do not run `commet agents setup` merely because doctor reports stale rules. It writes to the repository and requires an explicit user request.

## Implement

1. Trace the existing integration and preserve its language, framework, customer identity, API-version, and idempotency boundaries.
2. Use only operations and fields present in the installed manifest, generated reference, and types.
3. Prefer direct subscription and feature-access queries for authorization decisions. Use webhooks for asynchronous work, not as a replicated source of billing truth.
4. Preserve caller-owned logical event identifiers and explicit idempotency keys where the installed documentation requires them.
5. Handle the installed error contract and preserve the server request ID exactly for support correlation.
6. Run the repository's formatter, typecheck or compile, tests, and a focused integration check proportional to the change.

## Guard effects

Repository inspection, code edits, builds, and local tests do not require remote organization context. Any action that creates, updates, deletes, pushes, migrates, forwards, or tests Commet resources does.

Before a remote effect:

1. Name the exact organization and whether it is `sandbox` or `live`.
2. In Node projects where doctor is available, require a passing `PROJECT_CONTEXT_VALID` check and use its evidence.
3. Otherwise, require the organization and mode from explicit project configuration or the user; never infer mode from an API-key prefix.
4. State the target before executing. Do not perform a live write unless the user's request explicitly authorizes that effect.
5. Prefer a documented dry run or sandbox verification when available. Do not invent flags or remote behavior that the installed documentation does not expose.

Never expose API keys, webhook secrets, authorization tokens, or full environment values in output, patches, logs, or tests.
