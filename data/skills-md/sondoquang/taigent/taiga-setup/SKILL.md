---
name: taiga-setup
description: "Taiga setup check for the taiga-* skills: the taigent CLI, the user's Taiga login, the Taiga MCP server. Use when setting up or installing the Taiga skills on a machine or in a project, or when a taiga-* skill finds one of them missing."
allowed-tools: mcp__taiga__listProjects
---

# Taiga setup

Check the three things the `taiga-*` skills stand on, in order, and put the fix for every failing one in front of the user. Credentials stay with the user: you never ask for, type, print or write a password or token, and you never run `taigent login` yourself (it refuses without a terminal, and a password typed through you would end up in the transcript).

| Check | Needed by |
|---|---|
| 1. `taigent` CLI | every `taiga-*` skill (the MCP server runs through it too) |
| 2. Taiga login | the same |
| 3. Taiga MCP server `taiga` | `taiga-status-report`, `taiga-plan-backlog`, `taiga-bootstrap-project` |

## 1. taigent CLI

Run from the project root: `node --version`, then `npx --no -- taigent --help`. `--no` restricts npx to an installed `taigent`, so it never fetches the unrelated npm package of that name.

Passes when Node is v24 or later and the second command prints taigent's usage. The **taigent root**, holding the docs the skills cite (`docs/cli.md`, `docs/taiga/conventions.md`), is then the project root when its `package.json` `name` is `taigent`, else `node_modules/taigent/`.

Fix, by where the user works:

- **A clone of the taigent repository** (`github.com/sondoquang/taigent`): `npm install` in the clone.
- **Another project**: `npm install -D github:sondoquang/taigent` at the project root (creates `package.json` when there is none). npm builds the CLI on install; it needs read access to the repository. Append `#<tag>` to pin a release.

## 2. Taiga login

Run from the project root: `npx --no -- taigent whoami`.

- **Prints `User: …`**: passes. Its `Credentials:` line says what taigent uses: the stored login, or `TAIGA_*` variables from the environment or `.env`, which take precedence.
- **`not logged in to Taiga`**: the user runs, **in their own terminal window** (not through you, not with Claude Code's `!`), from the project root:

  ```
  npx taigent login
  ```

  It asks for the Taiga API URL (e.g. `https://taiga.example.com/api/v1`; a bare host gets `/api/v1`), the username or email, and the password (not shown). It keeps a refresh token in the OS credential store (Windows Credential Manager, macOS Keychain, Linux Secret Service), never the password. When the instance admin created an Application for taigent in Django admin (`/admin/` → Applications) and gave its id, `npx taigent login --application <id>` stores a non-expiring application token instead.
- **`expired or was revoked`**: the refresh token went unused for its lifetime (8 days by default); the user runs `npx taigent login` again.
- **`cannot use the …` credential store**: unlock it. On a machine without one (headless Linux, CI), set `TAIGENT_CREDENTIAL_STORE=file` (a 0600 JSON file in the config directory), or set `TAIGA_API_URL`, `TAIGA_USERNAME` and `TAIGA_PASSWORD` (or `TAIGA_TOKEN`) in the environment or in a git-ignored `.env`.
- **`TAIGA_API_URL is …, but the stored login is for …`**: unset that `TAIGA_API_URL` (often in `.env`), or log in to that instance.

When `.env` holds `TAIGA_PASSWORD`, run `git check-ignore -q .env` (exit 0: ignored); if it is not ignored, the fix is a `.env` line in `.gitignore` before anything is committed. Once the user has logged in, suggest deleting `TAIGA_PASSWORD` from `.env` and from their environment.

## 3. Taiga MCP server

Call the Taiga MCP tool `listProjects`. The skills expect the server under the name `taiga`; your agent prefixes its tools with that name (Claude Code: `mcp__taiga__listProjects`).

- **Projects listed**: passes.
- **Error from the tool**: fix check 2 first; the server acts as the same login.
- **No such tool**: in Codex, register the server (below). In Claude Code, run `claude mcp get taiga` and fix by its result:

| `claude mcp get taiga` | Fix |
|---|---|
| `No MCP server named "taiga"` | Register the server, below |
| `Pending approval` | The user restarts Claude Code and accepts the `taiga` server when asked |
| `Rejected` (`disabledMcpjsonServers`) | The user runs `claude mcp reset-project-choices`, restarts Claude Code and accepts `taiga` |
| `Failed to connect` | Run `npx --no -- taigent mcp` in a terminal: its error says what is missing (usually check 1 or 2). Ctrl+C ends it |
| `Connected` | The server was added after this session started: restart Claude Code |

An older entry that starts `npx -y taiga-mcp-server@…` with `TAIGA_*` values is replaced by the one below. When it was added with `claude mcp add -s user`, its password sits in `~/.claude.json`: the user runs `claude mcp remove -s user taiga`.

### Registering the server: Claude Code

**Default: `.mcp.json` at the project root.** It holds no secret, so it can be committed; each user accepts the project server once, when Claude Code asks at startup. Show the user this entry; once they agree, merge it into `.mcp.json`, keeping the file's other entries.

```json
{
  "mcpServers": {
    "taiga": {
      "command": "node",
      "args": ["node_modules/taigent/bin/taigent.js", "mcp"]
    }
  }
}
```

**Just for this user, no approval step**: `claude mcp add -s local taiga -- node node_modules/taigent/bin/taigent.js mcp`, run by the user from the project root (`-s local` runs it in the project directory; a `-s user` entry would not find `node_modules`). Then `claude mcp get taiga` shows `Connected`.

### Registering the server: Codex

`.codex/config.toml` at the project root, read once the project is trusted. Codex passes a stdio server only a few variables; `env_vars` forwards the ones taigent may need when the user sets them.

```toml
[mcp_servers.taiga]
command = "node"
args = ["node_modules/taigent/bin/taigent.js", "mcp"]
env_vars = ["TAIGA_API_URL", "TAIGA_USERNAME", "TAIGA_PASSWORD", "TAIGA_TOKEN", "TAIGENT_CONFIG_DIR", "TAIGENT_CREDENTIAL_STORE", "XDG_CONFIG_HOME", "DBUS_SESSION_BUS_ADDRESS"]
required = true
```

`taigent mcp` runs the `taiga-mcp-server` version pinned in taigent's `package.json` (1.9.20): the skills' tool notes and the banned-tool list of `docs/taiga/conventions.md` §10 are written against it.

## Installing the skills into another project

When the user asks for it: `npx skills add sondoquang/taigent` at the project root installs the nine Taigent skills (every `taiga-*` and `ask-taigent`) for the agents it detects, into `.agents/skills/` (Codex) and `.claude/skills/` (Claude Code); `npx skills update` refreshes them. It installs neither the CLI nor the MCP server: run the checks above.

## Report

One line per check: `ok`, or what failed and its fix. Done when every check passed, or every failing check has its fix in front of the user. When a fix takes effect only after a restart (a new MCP entry, newly copied skills), say so: agents load MCP servers and skills when they start. A new login needs no restart.
