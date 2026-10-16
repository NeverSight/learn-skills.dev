---
name: install-dexsql
description: Install a prebuilt DexSQL binary and connect it to the user's local MCP client. Use when asked to install, set up, or update DexSQL MCP; also accepts a user-provided local DexSQL executable.
license: MIT
---

# Install DexSQL MCP

Finish with a working local DexSQL MCP connection, using the user's chosen version
and client. DexSQL is closed source: install a prebuilt executable, not a source
build. The server runs as `dexsql mcp` over stdio and needs no JVM, GUI, or Python
runtime. This skill is installation guidance; installing the skill alone does
not install the executable or register an MCP server.

## Choose the executable

- Detect the host OS and architecture, the requested MCP client, and any existing
  DexSQL executable or configuration. Infer the current local client when clear;
  ask only if the destination client or scope is genuinely ambiguous.
- Prefer a compatible existing executable unless the user requested an update.
  A user-supplied local executable is also supported. Check `--version` and
  `mcp --help` before configuring it.
- Otherwise inspect the actual assets at
  `https://api.github.com/repos/LSPosed/dexsql-release/releases/latest`, or
  `https://api.github.com/repos/LSPosed/dexsql-release/releases/tags/<tag>` for a
  requested version. The human-facing release list is
  `https://github.com/LSPosed/dexsql-release/releases`.
- Select the CLI executable or archive for the detected OS/architecture. Do not
  substitute a WASM bundle, source archive, or another project's binary.
  Use the API's actual `browser_download_url`; do not invent asset names.
- The v0.1.0 assets are standalone executables, with these platform mappings:
  - Windows x64 (`x86_64` / `amd64`): `dexsql-windows-amd64.exe`.
  - Linux x64 (`x86_64` / `amd64`): `dexsql-linux-amd64`.
  - Linux ARM64 (`arm64` / `aarch64`): `dexsql-linux-arm64`.
  - macOS 13+ on Apple silicon (`arm64` / `aarch64`): `dexsql-darwin-arm64`.
  Recheck the selected release's assets; this list is not a version pin or a
  complete list of platforms that future releases may support.
- If the repository is inaccessible, no release exists, or there is no matching
  binary, explain the concrete issue and accept a local executable or an official
  release URL from the user. Do not claim installation succeeded or try to build
  the closed-source engine.

## Install locally

Download to a temporary directory. When the release asset API provides a
`digest` of the form `sha256:<hex>`, compare it with the downloaded file's SHA-256
before running or installing it. A published checksum file is another supported
source. Stop on a mismatch. If neither is available, report the computed hash as
a local fingerprint, not a verified upstream checksum. Standalone executables
need no extraction; extract archives only into the temporary directory, keeping
entries within it.

Place the executable and its accompanying license/notices in a versioned,
user-writable directory, such as `%LOCALAPPDATA%/DexSQL/<version>/` on Windows or
`~/.local/share/dexsql/<version>/` on macOS/Linux. Use its absolute path in MCP
configuration, so no administrator privileges or shell PATH edits are needed.
Normalize the installed filename to `dexsql.exe` on Windows or `dexsql` on
macOS/Linux. For bare binaries, also keep `LICENSE` and `LICENSE-AUXILIARY`
beside the executable. Prefer assets from the same release,
using their API-provided URLs and digests. If `LICENSE` or `LICENSE-AUXILIARY`
is not an asset, fetch
`https://raw.githubusercontent.com/LSPosed/dexsql-release/<tag>/<filename>` using
the selected release's actual `tag_name`, not the default branch.
`LICENSE` is required; retain `LICENSE-AUXILIARY` whenever that version provides
it. Third-party notices are compressed inside the executable; no separate
notice download is needed. When a readable copy is requested, run
`dexsql extract licenses --output THIRD_PARTY_NOTICES` with the installed
executable to export complete UTF-8 text offline. The command refuses to
overwrite existing files. Preserve supplied notices and access to embedded notices.
On macOS/Linux, ensure the executable bit is set. Preserve an existing install
until the new executable passes verification. Do not disable OS security checks
to force an incompatible or blocked binary to run.

## Connect the requested client

Inspect the relevant existing configuration and preserve unrelated servers and
settings. For a new connection, add a server named `dexsql`. For an update,
change only that server's executable path unless the user requested other changes;
retain custom arguments, environment settings, and timeouts. Back up a config
file before editing it. An already-correct entry needs no rewrite.

For **Codex**, prefer its CLI for a new entry:

```sh
codex mcp add dexsql -- /absolute/path/to/dexsql mcp
codex mcp get dexsql --json
```

Quote the executable path as required by the user's shell. If Codex CLI is not
available, merge this table into the chosen Codex config file:

```toml
[mcp_servers.dexsql]
command = "/absolute/path/to/dexsql"
args = ["mcp"]
```

For clients using **`mcpServers` JSON**, merge this entry into their documented
configuration location, or use their MCP settings UI:

```json
{
  "mcpServers": {
    "dexsql": {
      "command": "/absolute/path/to/dexsql",
      "args": ["mcp"]
    }
  }
}
```

Use proper JSON/TOML escaping for Windows paths. Do not assume every client uses
the same config path or schema. Do not install another AI client merely to finish
this task. This is a local stdio server; no network listener or API key is needed.

## Verify and hand off

Run `--version`, then verify an MCP initialize handshake and `tools/list` through
the client when available, or a temporary stdio MCP probe. The tool list must
include `open_dataset`, `query`, and `decode`. Close the probe afterward. Config
registration alone is not a successful connection test.

If the client needs a restart or new chat before discovering the server, state
that separately from the verified executable/protocol status. Do not claim the
current chat is connected until its tools are available. Analyze an APK only if
the user asked; installation does not require opening their files.

Report the installed version, executable path, config location, verification
result, and any remaining client reload step. A useful first prompt is:
"Open this APK with DexSQL, find methods referencing this string, and show their
callers and Smali."
