---
name: snap-o-network-inspector
description: Inspect Android network captures and intercept HTTP calls with the Snap-O CLI for a selected device/socket. Use for request/response details, websocket events, API response overrides, mock responses, or delays with Python route handlers.
---

# Snap-O Network Tool

Use this skill to inspect network traffic or override API responses in an Android app.

## CLI Path

Use the Network CLI bundled with the Snap-O plugin:

```bash
SNAPO_BIN=/path/to/snap-o/skills/snap-o-network-inspector/scripts/snapo-network
```

Resolve `scripts/snapo-network` relative to the directory containing this `SKILL.md`; do not assume the current working directory. The script requires Python 3 and Android Platform Tools; no Python packages, compiler toolchain, or macOS application are required.

The script resolves `adb` from `PATH`, `ANDROID_SDK_ROOT`, or `ANDROID_HOME`. Use `--adb <path>` or `SNAPO_ADB` to select a specific ADB executable or wrapper. Wrappers selecting a remote ADB server must tunnel Snap-O forwards back to localhost; otherwise, pass both `--adb-host` and `--adb-port`.

Listings use ADB process and package information without contacting the app. JSON rows contain `pid`, `processName`, and `packageName`; unresolved identity fields are `null`. Friendly app labels and icons are not loaded.

## Current Command Surface

- `snapo-network list`: lists available Snap-O Network Tool servers.
- `snapo-network requests`: emits CDP network events for a server.
- `snapo-network show`: shows full details for a request id, including headers and bodies.
- `snapo-network intercept <file.py>`: runs [Python route handlers](references/interception.md) to edit or mock HTTP responses; requires Snap-O OkHttp interception support in the app.

Useful global selectors:

- `-s`, `--serial`: use a specific device serial.
- `-d`: use the single connected USB device.
- `-e`: use the single connected emulator.
- `--adb`: use a specific ADB executable or wrapper.
- `--adb-host`, `--adb-port`: connect directly to an explicit remote ADB server; otherwise the configured ADB command selects its endpoint.

## Inspection Flow

1. List available servers.

```bash
"$SNAPO_BIN" list --json
```

For a remote ADB endpoint, append `--adb-host <host> --adb-port <port>` to `list`, `requests`, `show`, or `intercept`; the script uses the ADB server directly. Otherwise, its localhost forward is removed automatically when the command exits.

Use `--no-app-info` to skip package and process lookup.

2. Pick a target serial and socket. If multiple devices or sockets are available, select them explicitly.

3. Pull captured events.

```bash
"$SNAPO_BIN" requests -s <serial> -n <socket_name> --filter '<url-filter>' --no-stream --json
```

`--filter` uses the same case-insensitive URL syntax as the Network Tool search bar. Separate terms must all match, a term prefixed with `-` is excluded, and quotes or backslashes can escape whitespace.

`snapo-network requests` replaces request `Authorization` and `Cookie` values and response `Set-Cookie` values with `[REDACTED]`.

4. Inspect one request deeply when full request or response details are required.

```bash
"$SNAPO_BIN" show -s <serial> -n <socket_name> -r <request_id> --json
```

This output can contain URL query values and request or response bodies.

5. Re-check command help if output differs.

```bash
"$SNAPO_BIN" --help
"$SNAPO_BIN" list --help
"$SNAPO_BIN" requests --help
"$SNAPO_BIN" show --help
"$SNAPO_BIN" intercept --help
```

## Output Notes

- `--json` emits NDJSON, so process it line by line.
- `snapo-network requests` emits Chrome DevTools Protocol-style records with top-level `method` and `params` fields.
- Use `--no-stream` for a one-shot buffered snapshot.
- `snapo-network intercept` writes runner logs to stderr and does not accept `--json`, `--filter`, or `--no-stream`.
- Network protocol 4 uses a tool-owned `/network/protocol` version check, HTTP history and body reads, and SSE for live events. Interception registers routes with a POST that returns its own SSE connection. The CLI requires an updated Android Network library.
