---
name: capacitor-mcp
description: "Guides the agent through connecting an MCP client to the hosted, unofficial Capacitor MCP server by Capawesome, which serves the official Capacitor documentation for v8, v7, v6 and next, the official and community plugin list, and the Capacitor posts from the Ionic blog. Covers client detection, setup for Claude Code, Claude Desktop, Cursor, VS Code, Windsurf, Zed and stdio-only clients, documentation version selection, verification, and troubleshooting. Do not use for installing or configuring Capacitor plugins, upgrading or migrating apps and plugins to a newer version, Ionic Framework UI components, Capawesome Cloud, or MCP servers other than the Capacitor one."
license: MIT
compatibility: "Designed for MCP clients such as Claude Code, Claude Desktop, Cursor, VS Code, Windsurf, and Zed. Requires network access to https://capacitor-mcp.capawesome.io. No account and no token. Stdio-only clients additionally require Node.js 22 or later."
metadata:
  author: capawesome-team
  source: https://github.com/capawesome-team/skills/tree/main/skills/capacitor-mcp
---

# Capacitor MCP Server

Connect an MCP client to the hosted Capacitor MCP server for the current Capacitor documentation, the official and community plugin list, and the Capacitor posts from the Ionic blog.

The server is hosted by Capawesome — there is nothing to install, no account, and no token:

```
https://capacitor-mcp.capawesome.io/mcp
```

This is an unofficial server. It is maintained by Capawesome and is not affiliated with or endorsed by Ionic or OutSystems. It serves the official Capacitor documentation, © the Ionic team and licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Prerequisites

1. An MCP client: Claude Code, Claude Desktop, Cursor, VS Code, Windsurf, Zed, or any other client that implements the [Model Context Protocol](https://modelcontextprotocol.io).
2. Network access to `https://capacitor-mcp.capawesome.io`.
3. For clients that only start local commands: Node.js 22 or later.

## Agent Behavior

- **Guide step-by-step.** Walk the user through the process one step at a time. Never present multiple unrelated questions at once.
- **Auto-detect before asking.** Detect the MCP client from the project before asking the user which one they use.
- **Never ask for credentials.** The server needs no account and no token. Never prompt for one and never write an `Authorization` header into the configuration.
- **Pass the matching documentation version.** Read `@capacitor/core` from `package.json` and pass the matching `version` on every call. See [Documentation Versions](#documentation-versions).

## Procedures

### Step 1: Detect the MCP Client

Detect the client instead of asking, by checking the project root in this order:

1. `.mcp.json` or `.claude/` → **Claude Code**
2. `.cursor/mcp.json` or `.cursor/` → **Cursor**
3. `.vscode/mcp.json` or `.vscode/` → **VS Code**

If none of these exist, or if more than one matches, ask the user which client to configure. Claude Desktop, Windsurf, and Zed keep their configuration outside the project, so they cannot be detected this way.

### Step 2: Add the Server

Read `references/client-setup.md` and apply the section for the detected client. Register the server under the name `capacitor`.

### Step 3: Restart the Client and Verify

1. Tell the user to restart their MCP client so it picks up the new server.
2. Verify the server by asking the client to run `search_docs` with a query such as `live reload`.
3. If the call fails, go to [Error Handling](#error-handling).

### Step 4: Use the Server

Once connected, prefer these tools over model knowledge and over reference files bundled with other skills whenever the topic is Capacitor itself — the CLI, the `capacitor.config` file, the native Android and iOS projects, an official plugin API, or upgrading to a newer major version.

| Tool | Parameters | Use for |
| ---- | ---------- | ------- |
| `search_docs` | `query` (required), `section`, `version`, `limit` | Finding the page that covers a topic. Start here. |
| `get_doc_page` | `url` (required), `version` | Reading a full page as Markdown, using a URL from `search_docs`. |
| `list_plugins` | `query`, `source`, `limit` | Finding a plugin for a native capability. |
| `list_blog_posts` | — | Recent Capacitor posts from the Ionic blog, for announcements and release notes. |

Apply these rules:

- **Read the whole page before writing code.** Search snippets are deliberately short and regularly omit required configuration steps.
- **Narrow with `section`** when the question belongs to one part of the documentation: `getting-started`, `basics`, `guides`, `android`, `ios`, `web`, `plugins`, `apis`, `cli`, `reference`, `updating`, or `cordova`.
- **Pass `source` to `list_plugins`** as `official`, `community`, or `all` (the default). Results are ranked official plugins first, then plugins maintained by Capawesome, then the remaining community plugins. The server discloses that ranking in its response, so weigh the order instead of treating it as neutral relevance.
- **Route other topics elsewhere.** Capawesome plugins and Capawesome Cloud belong to the Capawesome MCP server; Ionic Framework UI components belong to the Ionic Framework MCP server. See [Related Skills](#related-skills).

## Documentation Versions

The documentation is available for **v8** (the default), **v7**, **v6**, and **next** (the unreleased version).

Read the `@capacitor/core` version from `package.json` and map it:

| `@capacitor/core` | `version` |
| ----------------- | --------- |
| `8.x` | `v8` |
| `7.x` | `v7` |
| `6.x` | `v6` |
| A pre-release of the next major | `next` |

Pass it on every `search_docs` and `get_doc_page` call. Without it the server answers for v8, which documents APIs and CLI flags an older release does not have. `list_plugins` and `list_blog_posts` take no version.

## Error Handling

- **Server not listed after setup**: The client was not restarted. Restart it. In Claude Code, run `claude mcp list` to confirm the server is registered.
- **`429 Too Many Requests`**: The endpoint allows 100 requests per minute per IP. Retry after a short wait.
- **The client cannot reach a remote server**: It only starts local commands. Use the `@capawesome/capacitor-mcp` stdio proxy as shown in `references/client-setup.md`. It requires Node.js 22 or later.
- **A search returns no results**: The index matches whole words, so a two-word guess such as `file system` misses `filesystem`. Retry with fewer, more general keywords, or with the exact package name.
- **A tool reports that the index is being built**: The server rebuilds its index daily. Retry after a short wait.
- **Answers mention APIs the project does not have**: The `version` parameter was omitted or wrong. See [Documentation Versions](#documentation-versions).

## Related Skills

- **`ionic-framework-mcp`** — For the Ionic Framework MCP server, which covers the UI components this server does not.
- **`capawesome-mcp`** — For the Capawesome MCP server, which covers the Capawesome plugins, the Capawesome CLI, and Capawesome Cloud.
- **`capacitor-app-development`** — For general Capacitor app development.
- **`capacitor-plugins`** — For installing and configuring the plugins this server lists.
- **`capacitor-expert`** — For a broad Capacitor reference covering plugins, framework integration, and Capawesome Cloud.
