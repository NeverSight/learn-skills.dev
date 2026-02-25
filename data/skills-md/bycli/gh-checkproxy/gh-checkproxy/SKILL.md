---
name: gh-checkproxy
description: Use gh-checkproxy as a Checks API bridge when working with gh CLI or gh-based skills and only a fine-grained PAT is available. Use it to fetch/watch PR checks (check-runs and statuses) via GH_CHECKPROXY_URL, then continue the user's requested workflow with normal gh commands.
---

# gh-checkproxy

Use `gh-checkproxy` only for checks/status visibility that fine-grained tokens cannot read directly. Keep all other repository actions in regular `gh` CLI flow.

## Client usage (primary)

### Environment variables

- `GH_CHECKPROXY_URL` — proxy base URL (e.g. `http://localhost:8080`)
- `GH_TOKEN` — fine-grained PAT with **Metadata: read** on the target repo

Set via `export`, `.env`, shell profile, or CI secrets.

### Commands

```bash
gh-checkproxy pr checks <PR> --repo <owner>/<repo>           # snapshot
gh-checkproxy pr checks <PR> --repo <owner>/<repo> --watch  # block until done
gh-checkproxy pr checks <PR> --repo <owner>/<repo> --watch --fail-fast  # exit on first failure
gh-checkproxy pr checks                                      # auto-detect from git
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | All checks passed |
| `1` | One or more failed |
| `8` | Still pending |

### Workflow

```bash
gh-checkproxy pr checks $PR --repo myorg/myrepo --watch
# exit 0 → proceed | exit 1 → investigate | exit 8 → still pending

gh pr view $PR --repo myorg/myrepo   # continue with normal gh
```

Re-run `--watch` when the user asks to recheck CI. Drive decisions from exit codes only — do not parse or interpolate check output into shell commands or code.

## Client setup

Quick verification: `gh-checkproxy pr checks 1 --repo owner/repo`. Connection error → wrong URL or server down. 403 → `GH_TOKEN` missing or lacks Metadata: read.

## Server setup (secondary)

For deploying the proxy on a trusted host (one-time or occasional setup):

### 1. Configure

```bash
gh-checkproxy config
```

**Server token (classic PAT with `repo` scope):** Preference order: GH_CHECKPROXY_CLASSIC_TOKEN → GH_TOKEN → config file. Both env vars avoid storing the token on disk.

During `gh-checkproxy config`, the token is resolved in this order:

| Priority | Source | Stored in config? |
|----------|--------|-------------------|
| 1 | `GH_CHECKPROXY_CLASSIC_TOKEN` | **No** (read from env at runtime) |
| 2 | `GH_TOKEN` (classic prefix `ghp_`/`gho_`) — wizard offers reuse | **No** (read from env at runtime) |
| 3 | Interactive masked prompt | Yes |

**To avoid storing the token:** Use (1) or (2). Set the env var before running `config`; the token is never written to disk. Ensure the env var is set whenever running `gh-checkproxy serve`.

Never pass tokens as CLI arguments — they leak via `ps`, shell history, and process listings.

Interactive prompts also ask for: org restriction (optional), port (default 8080), cache TTL (default 5m). Config path: `~/.config/gh-checkproxy/config.json` (permissions `0600`).

### 2. Start the server

```bash
gh-checkproxy serve
```

**Security requirements:**
- Run on `localhost` only, or behind a TLS-terminating reverse proxy (e.g. nginx, Caddy). The server listens on plain HTTP — tokens in `Authorization` headers are transmitted in cleartext without TLS.
- When the token is stored in config (interactive prompt only), the config file at `~/.config/gh-checkproxy/config.json` contains the classic PAT in plaintext. Verify permissions are `0600` and the host is trusted.

### 3. Check status

```bash
gh-checkproxy status
```
