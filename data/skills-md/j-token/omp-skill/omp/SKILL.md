---
name: omp
description: Use whenever the user asks about Oh My Pi, the omp.sh terminal coding agent, the `omp` CLI/TUI, `.omp/` or `~/.omp/` configuration, providers and model roles, sessions and run modes, built-in tools, subagents, browser/computer/GitHub integrations, context files, skills, hooks, MCP, plugins/extensions, marketplaces, or the SDK/RPC/ACP APIs. Covers installation, operation, troubleshooting, configuration, customization, automation, and extension authoring from the complete official OMP documentation.
compatibility: Requires an OMP installation for local commands; internet access is optional and only needed to check newer live documentation.
metadata:
  source: https://omp.sh/docs
  docs-snapshot: "2026-08-25"
---

# OMP

Use this playbook to answer questions and make changes involving the Oh My Pi coding agent. Treat bundled references as a task-oriented map of the official documentation, not as permission to invent behavior that the docs do not describe.

## Route the request

Read only the references needed for the request:

| Request | Read first |
| --- | --- |
| Install, first run, TUI controls, slash commands, keybindings, settings, run modes | [Start and sessions](references/start-and-sessions.md) |
| Resume/branch sessions, memory, compaction, plan, goal, handoff | [Start and sessions](references/start-and-sessions.md) |
| Files, LSP, debugger, structural edits, review, commits, security scans | [Coding and integrations](references/coding-and-integrations.md) |
| Subagents, advisor, vibe, collab, web/browser, computer, GitHub | [Coding and integrations](references/coding-and-integrations.md) |
| Providers, model roles, custom providers/models, prewalk | [Models and customization](references/models-and-customization.md) |
| Context files, skills, prompt templates, magic keywords, hooks, custom tools, subagent authoring | [Models and customization](references/models-and-customization.md) |
| MCP, themes, TTSR, plugins, extension APIs, marketplaces | [Extension ecosystem](references/extension-ecosystem.md) |
| SDK, RPC, ACP, CLI flags, environment variables, secrets, approvals, session format, tool schemas | [Programmatic reference](references/programmatic-reference.md) |
| Unknown topic or documentation coverage check | [Complete docs index](references/docs-index.md) |

For a request spanning several rows, read every relevant reference before deciding. Do not load all references for a narrow question.

## Work from installed reality

1. Identify whether the task concerns interactive use, project/user configuration, an extension, or an embedding API. These surfaces have different schemas and trust boundaries.
2. Inspect the installed version and existing configuration before editing when local access exists. Prefer `omp --version`, `omp config path`, `omp <command> --help`, and the repository's current files over remembered defaults.
3. Resolve scope explicitly: CLI-only override, project configuration, profile, or user configuration. Preserve the documented precedence instead of creating a second competing setting.
4. Make the smallest complete change. Keep existing YAML/JSON/TypeScript style and migrate every affected reference when renaming a role, tool, skill, agent, or extension.
5. Exercise the actual surface: start or resume the relevant session, invoke the slash/CLI command, load the extension, or exchange one SDK/RPC/ACP request. Report exactly what was observed.

If the installed version disagrees with the bundled snapshot, follow the installed command help and the matching live page from `https://omp.sh/docs`. State the version-dependent difference rather than blending two interfaces.

## Preserve the product boundaries

- A skill supplies instructions and supporting files. It does not grant permissions or add an executable tool.
- Context files provide persistent rules; prompt templates create reusable user prompts; magic keywords rewrite matching input; hooks observe or alter lifecycle events; custom tools expose callable capabilities. Choose the mechanism that matches the behavior.
- Extensions and plugins run in-process and may modify agent behavior. MCP servers and host integrations cross separate protocol/trust boundaries. Review source and scope before enabling them.
- The TypeScript SDK is an in-process Bun API. RPC is framed NDJSON for process isolation or other languages. ACP is an editor-hosted stdio child process. Do not substitute one integration mode for another.
- Model roles are routing indirection. Providers supply authentication and model inventory. Keep role selection separate from provider credentials.
- Session files are append-oriented runtime state. Use documented session APIs and commands rather than hand-editing them unless the task is explicitly format analysis or recovery.

## Apply safety defaults

- Keep normal tool approvals for untrusted repositories, plugins, extensions, MCP servers, and shared sessions. Use `yolo`/auto-approval only when the user explicitly accepts the wider execution boundary.
- Never place long-lived secrets in committed settings, prompts, session exports, logs, or command examples. Prefer the documented auth flow, secret store, or environment variable for the provider.
- Remember that prompts and selected context are sent to the configured model provider; web, GitHub, MCP, browser, and computer integrations may contact their corresponding services.
- Treat extension, plugin, hook, custom-tool, and marketplace code as executable local code. Inspect provenance and use the narrowest user/project scope that satisfies the task.
- Do not claim that aborting a model turn automatically undoes filesystem or process side effects. Verify repository and process state afterward.

## Diagnose by layer

When OMP fails, locate the layer before changing configuration:

1. **Launch:** binary/PATH, current working directory, terminal capabilities, version.
2. **Authentication/model:** provider login or secret, model availability, selected model/role, gateway or local endpoint.
3. **Configuration:** active config path/profile, later override files, project/user scope, include/ignore filters.
4. **Capability:** tool enabled, approval policy, LSP/debug adapter/browser relay/MCP process available.
5. **Extension:** discovery path, trust, dependency load, plugin feature/config state, hook or tool schema.
6. **Session/protocol:** selected session, compaction/retry state, RPC negotiation/framing, ACP client callback support.

Change one layer at a time and rerun the smallest command or interaction that proves it.

## Answer and change format

For guidance, provide:

1. the recommended command or configuration;
2. the scope/path it affects;
3. why that surface is correct;
4. security or persistence implications;
5. one focused verification step;
6. the exact official page URL when the detail is version-sensitive.

For code or configuration changes, implement them and then report changed paths plus the observed verification. Avoid dumping the whole documentation catalog when one page answers the request.
