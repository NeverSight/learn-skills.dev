---
name: mcp-z-cli
description: Use @mcp-z/cli to discover and call MCP tools, prompts, and resources from a terminal using a project's .mcp.json. Load for mcp-z or z commands, CLI-based MCP access, or on-demand capability discovery. Application code using @mcp-z/client belongs to the client skill.
---

# @mcp-z/cli

Use a project's existing MCP configuration from a shell-capable agent, without writing a connection script. When the project selects CLI access, keep its calls on that route rather than substituting native agent MCP tools.

## Run and locate configuration

Requires Node.js 20 or newer. For one-shot use:

```sh
npx -y @mcp-z/cli inspect --servers SERVER --tools
```

Alternatively, install with `npm install -g @mcp-z/cli` and use `mcp-z` or its alias `z`. The examples below use `mcp-z`; the remaining arguments are identical with either executable or the npx prefix. `SERVER` and `TOOL` are placeholders for discovered names, not built-in aliases.

With no `--config`, commands find the nearest `.mcp.json` from the current working directory upward, through the home directory inclusive. Outside the home directory tree, lookup checks only the current directory. Run from the intended project or its subdirectory; a nearer config takes precedence over a parent's. Configured child processes start with the config directory as their working directory.

Let that lookup select the project's ordinary `.mcp.json`; examples omit `--config` for this reason. Use `--config` when the task selects another configuration or needs an exact path: a bare filename such as `.mcp.staging.json` searches upward; `./.mcp.staging.json` or an absolute path selects that exact file. Server names are keys under `mcpServers`. Inspect the relevant entry without exposing its credentials.

## Discover as the task requires

Start with the task's existing evidence, such as a document link in local project notes, and load enough context to resolve the next uncertainty. Configuration membership alone does not make a server relevant. When the server is known, inspect it directly. When the capability is unfamiliar, search likely servers first and expand when the results are insufficient. For example, finding an unfamiliar spreadsheet operation starts with a short candidate list:

```sh
mcp-z search "spreadsheet" --servers sheets --types tool --limit 5
```

Here `sheets` is an illustrative configured server name. After choosing a candidate, inspect its server's schema, saving and selecting locally when the server exposes many tools. The [schema extraction example](resources/output-and-arguments.md#save-schemas-without-loading-every-schema-into-context) shows that path. A small server's schema output can simply be read directly:

```sh
mcp-z inspect --servers SERVER --tools --json
```

Discovery returns live server-owned names and schemas; use those rather than guessing parameters from a tool's name. Search is unnecessary when the desired tool and its applicable schema are already known. A schema does not need fetching again for every call. Search results may be limited or incomplete if a server failed to connect, particularly in JSON mode where connection warnings are suppressed. Inspect the expected server before concluding a capability is absent.

Readable output is the default. Search descriptions are shortened; ordinary inspect output does not include full input schemas. Use `inspect --tools --json` for complete schemas, or `--verbose` for readable parameter details. JSON is useful for parsing and saving results, but is not inherently smaller. Request bounded data where the tool supports it; for large responses, save the full output and inspect relevant portions locally. Small results may be cheaper to read whole. Preserve errors, continuation tokens, and evidence of completeness when filtering.

## Call and check the result

```sh
mcp-z call-tool SERVER TOOL '{"argument":"value"}' --json
```

Replace the illustrative JSON with the tool's actual input object; use `'{}'` when it needs no arguments. These inline examples use POSIX shell quoting. JSON must reach the CLI as one argument; shell-specific alternatives are in [saved output and argument handling](resources/output-and-arguments.md).

Discovery does not authorize a write. Tool calls stay within the user's requested action. Check command failure and the returned data: successful application payloads can still report per-item failures. `call-tool --json` prints the parsed tool result rather than a guaranteed raw MCP envelope. After an uncertain write outcome, read the target before retrying because the write may already have succeeded.

## Task examples

These are independent examples, not a reading sequence. Their descriptions identify when they are relevant; the main workflow may already provide everything needed. A prompt/resource reference becomes useful when that capability is part of the task, not to establish that an ordinary tool call does not need it.

- For a real provider read or an authorized bounded update, use [read and update a spreadsheet](resources/provider-operations.md). It also explains operation-triggered OAuth for MCP-Z Google and Microsoft servers.
- For large results, schema extraction, or shell argument handling, use [saved output and argument handling](resources/output-and-arguments.md).
- When a discovered prompt or resource fits the task, use [prompts and resources](resources/prompts-and-resources.md).
- When working without a config, attaching to HTTP servers, or diagnosing protocol negotiation, use [connection options](resources/connections.md).

Use `mcp-z --help` or `mcp-z COMMAND --help` for the installed command's options. Capability discovery through the CLI avoids preloading every schema into model context; it does not imply that every configured server process is started lazily.
