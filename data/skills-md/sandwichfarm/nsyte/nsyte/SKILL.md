---
name: nsyte
description: Deploy and manage censorship-resistant static websites on the Nostr network using nsyte CLI. Covers installation, project setup, configuration, authentication (NIP-46 bunkers), deployment to Blossom servers, CI/CD automation, and troubleshooting. Use when the user mentions nsyte, nsite, Nostr site hosting, Blossom uploads, or decentralized web publishing.
license: MIT
metadata:
  author: sandwichfarm
  version: "0.22.0"
  repository: https://github.com/sandwichfarm/nsyte
---

# nsyte — Decentralized Static Site Deployment

nsyte is a Deno-based CLI that publishes static websites to the Nostr network using Blossom servers for file storage. Sites are content-addressed (SHA-256), censorship-resistant, and discoverable via Nostr relays.

**Key concepts:** For Nostr/Blossom domain knowledge (relays, pubkeys, nsec, NIP-46, events), see [references/nostr-concepts.md](references/nostr-concepts.md).

---

## Installation

### Check if installed

```bash
nsyte --version
```

If this prints a version string, skip to [Project Setup](#project-setup).

### Linux / macOS (recommended — no Deno required)

```bash
curl -fsSL https://nsyte.run/get/install.sh | bash
```

Installs to `/usr/local/bin/nsyte`. Use `sudo` if that directory is not writable.

### Linux / macOS (alternative — requires Deno 2.x)

```bash
deno install -A -f -g -n nsyte jsr:@nsyte/cli
```

### Windows

Download the latest binary from `https://github.com/sandwichfarm/nsyte/releases`, place in `%USERPROFILE%\bin\`, and add that directory to PATH.

### Troubleshooting installation

- **Command not found:** Add `/usr/local/bin` to PATH in `~/.bashrc` or `~/.zshrc` and reload.
- **Permission denied:** Use `sudo` for the curl install, or install to a user-writable location.
- **Deno version too old:** Run `deno upgrade` or use the binary install instead.

---

## Project Setup

```bash
cd /path/to/your/project
nsyte init
```

Interactive prompts ask for:
1. **Auth method** — generate new key, enter existing nsec/hex key, or connect NIP-46 bunker
2. **Relay URLs** — one or more `wss://` relay WebSocket URLs
3. **Blossom server URLs** — one or more `https://` Blossom server URLs

On success, creates `.nsite/config.json`. See [Configuration](#configuration) for the schema.

---

## Configuration

Config file: `.nsite/config.json`

For the full JSON Schema, see [assets/config.schema.json](assets/config.schema.json).

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `relays` | `string[]` | Nostr relay URLs (`wss://`), unique items |
| `servers` | `string[]` | Blossom server URLs (`https://`), unique items |

### Authentication

| Field | Type | Description |
|-------|------|-------------|
| `bunkerPubkey` | `string` | 64-char hex pubkey for NIP-46 bunker. Pattern: `^[0-9a-fA-F]{64}$`. **Always set via `nsyte bunker use`, never manually.** |

### Site identity

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `string \| null` | `null` | `null`/empty = root site (kind 15128). Non-empty = named site (kind 35128) |
| `title` | `string` | — | Site title for manifest event |
| `description` | `string` | — | Site description for manifest event |
| `fallback` | `string` | — | 404 fallback HTML path (e.g., `/index.html` for SPAs) |

### Publishing flags (root sites only — `id` must be null/empty)

| Field | Type | Description |
|-------|------|-------------|
| `publishProfile` | `boolean` | Publish kind 0 profile metadata. Requires non-empty `profile` object |
| `publishRelayList` | `boolean` | Publish kind 10002 relay list |
| `publishServerList` | `boolean` | Publish kind 10063 Blossom server list |
| `publishAppHandler` | `boolean` | Publish NIP-89 handler. Requires `appHandler` with `kinds` |

### Optional objects

| Field | Type | Description |
|-------|------|-------------|
| `profile` | `object` | Nostr profile: `name`, `display_name`, `about`, `picture`, `banner`, `website`, `nip05`, `lud16`, `lud06` |
| `appHandler` | `object` | NIP-89 config: `kinds` (required), `id`, `name`, `description`, `icon`, `platforms` |
| `gatewayHostnames` | `string[]` | Gateway hostnames (default: `["nsite.lol"]`) |

### Example configs

**Minimal (root site):**
```json
{
  "relays": ["wss://relay.damus.io", "wss://nos.lol"],
  "servers": ["https://cdn.hzrd149.com"]
}
```

**Named site (blog):**
```json
{
  "relays": ["wss://relay.damus.io"],
  "servers": ["https://cdn.hzrd149.com"],
  "id": "blog",
  "title": "My Blog",
  "description": "A blog about decentralized applications"
}
```

**With profile publishing:**
```json
{
  "relays": ["wss://relay.damus.io", "wss://nos.lol"],
  "servers": ["https://cdn.hzrd149.com"],
  "publishProfile": true,
  "publishRelayList": true,
  "publishServerList": true,
  "profile": {
    "name": "Alice",
    "display_name": "Alice",
    "about": "Decentralization enthusiast",
    "picture": "https://example.com/avatar.jpg",
    "nip05": "alice@example.com",
    "lud16": "alice@getalby.com"
  }
}
```

**With NIP-89 app handler:**
```json
{
  "relays": ["wss://relay.damus.io"],
  "servers": ["https://cdn.hzrd149.com"],
  "publishAppHandler": true,
  "appHandler": {
    "kinds": [1, 30023],
    "name": "My Nostr Viewer",
    "description": "A viewer for notes and articles",
    "icon": "https://example.com/logo.png"
  }
}
```

### Interactive config editor

```bash
nsyte config
```

Requires an interactive terminal. Keys: `↑`/`↓` navigate, `Enter` edit, `s` save, `r` reset, `q` quit.

For non-interactive contexts, edit `.nsite/config.json` directly and validate:

```bash
nsyte validate
```

---

## Authentication

### NIP-46 Bunker (recommended)

#### Connect via QR code

```bash
nsyte bunker connect
```

Choose "Scan QR Code", enter a relay URL, scan with signer app (Amber, nsec.app), approve.

#### Connect via bunker URL

```bash
nsyte bunker connect 'bunker://pubkey?relay=wss://relay.example.com&secret=xxx'
```

**CRITICAL:** Always single-quote the URL — `?` and `&` are shell metacharacters.

#### Link bunker to project

```bash
nsyte bunker use [pubkey]
```

Sets `bunkerPubkey` in config and stores nbunksec in OS keychain. **Never manually edit `bunkerPubkey`.**

#### Bunker management commands

| Command | Purpose |
|---------|---------|
| `nsyte bunker connect` | Connect interactively (QR or URL) |
| `nsyte bunker connect '<url>'` | Connect via bunker URL |
| `nsyte bunker import nbunksec1...` | Import existing nbunksec |
| `nsyte bunker export [pubkey]` | Export stored bunker as nbunksec |
| `nsyte bunker list` | List stored bunkers |
| `nsyte bunker use [pubkey]` | Set project to use a bunker |
| `nsyte bunker remove [pubkey]` | Remove a bunker from storage |
| `nsyte bunker migrate [pubkeys...]` | Rebuild keychain index |

### Secrets storage

nsyte auto-selects the best backend:
1. **macOS:** Keychain
2. **Linux:** Secret Service (fallback: encrypted file)
3. **Windows:** Credential Manager (fallback: encrypted file)

Override with `NSYTE_FORCE_ENCRYPTED_STORAGE=true`.

---

## Deployment

### Basic deploy

```bash
nsyte deploy ./dist
```

### Auth resolution order

1. **`--sec` flag** (highest priority):
   ```bash
   nsyte deploy ./dist --sec "nsec1..."
   nsyte deploy ./dist --sec "${NBUNK_SECRET}"
   ```
   Auto-detects format: `nsec1...`, `nbunksec1...`, `bunker://...`, or 64-char hex.

2. **Stored bunker** from `.nsite/config.json` `bunkerPubkey` + OS keychain.

3. If neither available, nsyte exits with an error.

### Common flags

| Flag | Purpose |
|------|---------|
| `--sec <value>` | Provide signing key/credential |
| `--force` | Re-upload all files (skip diff) |
| `--fallback=/index.html` | SPA fallback for 404s |
| `--non-interactive` | CI mode — no prompts, fail fast |

### Interpreting output

- **Full success:** `{N} files uploaded successfully ({size})` — all files to all servers
- **Partial success:** `{uploaded}/{total} files uploaded` — some servers failed
- **Total failure:** `Failed to upload any files` — check relay/server/auth errors

Gateway URL printed after deploy: `https://{npub}.nsite.lol/`

---

## CI/CD

### Step 1: Generate CI credential (one-time, on dev machine)

```bash
nsyte ci
# or with bunker URL:
nsyte ci 'bunker://pubkey?relay=wss://relay.example.com&secret=xxx'
```

The `nbunksec1...` string is printed once and never stored. Copy it immediately and save as a CI secret.

### Step 2: Deploy in pipeline

```bash
nsyte deploy ./dist --non-interactive --sec "${NBUNK_SECRET}"
```

**CRITICAL:** Use `--sec` (not `--nbunksec`).

### GitHub Actions example

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: denoland/setup-deno@v1
      - run: nsyte deploy ./dist --non-interactive --sec "${{ secrets.NBUNK_SECRET }}"
```

### CI checklist

- [ ] `.nsite/config.json` committed or provided as artifact
- [ ] `NBUNK_SECRET` secret set to `nbunksec1...` string
- [ ] `--non-interactive` flag present
- [ ] Optionally run `nsyte validate` before deploy

---

## Other Commands

| Command | Purpose |
|---------|---------|
| `nsyte ls` | List published files |
| `nsyte browse` | Interactive TUI file browser with relay/server propagation tracking |
| `nsyte download <dir>` | Download published files |
| `nsyte serve -d <dir>` | Local dev server |
| `nsyte run` | Start resolver server with npub subdomains |
| `nsyte debug <npub>` | Debug nsite setup (relays, servers, integrity) |
| `nsyte validate` | Validate config (exit 0 = valid, 1 = invalid) |
| `nsyte purge` | Remove published files from relays/servers |
| `nsyte sites` | List available sites (root + named) |

---

## Troubleshooting

### Auth errors

- **"No valid signing method":** Provide `--sec` or configure bunker via `nsyte bunker use`.
- **"No stored credential":** `bunkerPubkey` set in config but keychain entry missing. Fix: `nsyte bunker use [pubkey]`.
- **Bunker URL rejected:** Shell ate metacharacters. Use single quotes: `'bunker://...'`.

### Deploy errors

- **Relay issues:** Check `relays` array in config has valid `wss://` URLs. Try `--use-fallback-relays`.
- **Blossom server rejection:** Check `servers` array. Try adding a different server via `nsyte config`.
- **Config missing:** Run `nsyte init` first.

### Config errors

- **"Config editor requires interactive terminal":** Edit JSON directly + `nsyte validate`.
- **Validation fails:** Common causes: malformed URLs, `publishAppHandler: true` without `appHandler.kinds`, `publish*` on named site.
- **bunkerPubkey format:** Must be 64 hex chars, not npub. Always use `nsyte bunker use`.
