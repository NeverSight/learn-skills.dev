---
name: claude-code-proxy-patterns
description: Claude Code OAuth proxy patterns and anti-patterns for multi-provider model routing. TRIGGERS - proxy Claude Code, OAuth token Keychain, route Haiku to MiniMax, ANTHROPIC_BASE_URL, model routing proxy, claude-code-proxy, proxy-toggle, multi-provider setup, anthropic-beta oauth, proxy auth failure, go proxy, failover proxy, launchd proxy, proxy failover
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

<!-- # SSoT-OK: version references are documentation of binary analysis findings, not package versions -->

# Claude Code Proxy Patterns

Multi-provider proxy that routes Claude Code model tiers to different backends. Haiku to MiniMax (cost/speed), Sonnet/Opus to Anthropic (native OAuth passthrough). Includes Go binary proxy with launchd auto-restart and failover wrapper for resilience.

**Scope**: Local reverse proxy for Claude Code with OAuth subscription (Max plan). Routes based on model name in request body.

**Reference implementations**:

- Go proxy binary: `/usr/local/bin/claude-proxy` (port 8082)

---

## When to Use This Skill

- Building or debugging a Claude Code multi-provider proxy
- Setting up `ANTHROPIC_BASE_URL` with OAuth subscription mode
- Integrating Anthropic-compatible providers (MiniMax, etc.)
- Diagnosing "OAuth not supported" or auth failures through a proxy
- Understanding how Claude Code stores and transmits OAuth tokens

**Do NOT use for**: Claude API key-only setups (no proxy needed), MCP server development, Claude Code hooks (operate at tool level, not API level), or corporate HTTPS proxy traversal.

---

## Architecture

```
Claude Code (OAuth/Max subscription)
    |
    |  ANTHROPIC_BASE_URL=http://127.0.0.1:8082 (Go proxy)
    |  (unset ANTHROPIC_API_KEY to avoid auth conflict)
    v
+----------------------------------+
| Go proxy (:8082)                 |
| launchd managed, auto-restart   |
+----------------------------------+
    |
    | model =
    | claude-haiku-
    | 4-5-20251001
    v
+-----------+
| MiniMax   |
| M2.5      |
| highspeed |
+-----------+
```

**Port Configuration**:

- `:8082` - Go proxy (entry point, launchd-managed, auto-restart)

The Go proxy uses `cenkalti/backoff/v4` for built-in retry logic.

The proxy reads the `model` field from each `/v1/messages` request body. If it matches the configured Haiku model ID, the request goes to MiniMax. Everything else falls through to real Anthropic with OAuth passthrough.

---

## Working Patterns

### WP-01: Keychain OAuth Token Reading

Read OAuth tokens from macOS Keychain where Claude Code stores them.

**Service**: `"Claude Code-credentials"` (note the space before the hyphen)
**Account**: Current username via `getpass.getuser()`

```python
import subprocess, json, getpass

result = subprocess.run(
    ["security", "find-generic-password",
     "-s", "Claude Code-credentials",
     "-a", getpass.getuser(), "-w"],
    capture_output=True, text=True, timeout=5, check=False,
)
if result.returncode == 0:
    data = json.loads(result.stdout.strip())
    oauth = data.get("claudeAiOauth")
```

See [references/oauth-internals.md](./references/oauth-internals.md) for the full deep dive.

### WP-02: Token JSON Structure

The Keychain stores a JSON envelope with the `claudeAiOauth` key.

```json
{
  "claudeAiOauth": {
    "accessToken": "eyJhbG...",
    "refreshToken": "rt_...",
    "expiresAt": 1740268800000,
    "subscriptionType": "claude_pro_2025"
  }
}
```

**Note**: `expiresAt` is in **milliseconds** (Unix epoch _ 1000). Compare with `time.time() _ 1000` or divide by 1000 for seconds.

### WP-03: OAuth Beta Header

The `anthropic-beta: oauth-2025-04-20` header is **required** for OAuth token authentication. Without it, Anthropic rejects the Bearer token.

**Critical**: APPEND to existing beta headers, do not replace them.

```python
# proxy.py:304-308
existing_beta = original_headers.get("anthropic-beta", "")
beta_parts = [b.strip() for b in existing_beta.split(",") if b.strip()] if existing_beta else []
if "oauth-2025-04-20" not in beta_parts:
    beta_parts.append("oauth-2025-04-20")
target_headers["anthropic-beta"] = ",".join(beta_parts)
```

### WP-04: ANTHROPIC_API_KEY=proxy-managed

Setting `ANTHROPIC_BASE_URL` alone is insufficient in OAuth mode. Claude Code must also see `ANTHROPIC_API_KEY` set to switch from OAuth-only mode to API-key mode, which then honors `ANTHROPIC_BASE_URL`.

```bash
# In .zshenv (managed by proxy-toggle)
export ANTHROPIC_BASE_URL="http://127.0.0.1:8082"
export ANTHROPIC_API_KEY="proxy-managed"
```

The value `"proxy-managed"` is a dummy sentinel. The proxy intercepts it (line 324) and never forwards it to providers.

### WP-05: OAuth Token Cache with TTL

Avoid repeated Keychain subprocess calls by caching the token for 5 minutes.

```python
# proxy.py:117-118
_oauth_cache: dict = {"token": None, "expires_at": 0.0, "fetched_at": 0.0}
_OAUTH_CACHE_TTL = 300  # Re-read from Keychain every 5 minutes
```

Cache invalidation triggers:

- TTL expired (5 minutes since last fetch)
- Token's `expiresAt` has passed
- Proxy restart

### WP-06: Auth Priority Chain

The proxy tries multiple auth sources in order for Anthropic-bound requests.

```
1. REAL_ANTHROPIC_API_KEY env var   -> x-api-key header (explicit config)
2. Keychain OAuth token             -> Authorization: Bearer + anthropic-beta
3. ~/.claude/.credentials.json      -> Authorization: Bearer (plaintext fallback)
4. Forward client Authorization     -> Pass through whatever Claude Code sent
5. No auth                          -> Will 401 (expected)
```

See `proxy.py:293-314` for the implementation.

### WP-07: count_tokens Endpoint Auth

The `/v1/messages/count_tokens` endpoint needs the same auth as `/v1/messages`. Claude Code calls this for preflight token counting. Missing auth here causes silent failures. Returns 501 for non-Anthropic providers (MiniMax doesn't support it).

### WP-08: Anthropic-Compatible Provider URLs

Third-party providers that support the Anthropic `/v1/messages` API format.

| Provider               | Base URL                           | Notes                                             |
| ---------------------- | ---------------------------------- | ------------------------------------------------- |
| MiniMax M2.5-highspeed | `https://api.minimax.io/anthropic` | Returns `base_resp` field, extra `thinking` block |

See [references/provider-compatibility.md](./references/provider-compatibility.md) for the full matrix.

### WP-09: Concurrency Semaphore

Per-provider rate limiting prevents overwhelming third-party APIs. No semaphore for Anthropic (they handle their own rate limiting).

```python
# proxy.py:207-209
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
haiku_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
opus_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
sonnet_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
```

### WP-10: proxy-toggle Enable/Disable

The `proxy-toggle` script manages `.zshenv` entries and a flag file atomically.

```bash
~/.claude/bin/proxy-toggle enable    # Adds env vars, creates flag file, checks health
~/.claude/bin/proxy-toggle disable   # Removes env vars, removes flag file
~/.claude/bin/proxy-toggle status    # Shows routing flag, proxy process, .zshenv state
```

**Important**: Claude Code must be restarted after toggling because `ANTHROPIC_BASE_URL` is read at startup.

### WP-11: Health Endpoint

The `/health` endpoint returns provider configuration state for monitoring.

```bash
curl -s http://127.0.0.1:8082/health | jq .
```

### WP-12: Go Proxy with Retry

Go proxy with built-in retry using `cenkalti/backoff/v4` (exponential backoff: 500ms -> 1s -> 2s, max 5s elapsed).

```go
import "github.com/cenkalti/backoff/v4"

backoffConfig := backoff.NewExponentialBackOff(
    backoff.WithInitialInterval(500 * time.Millisecond),
    backoff.WithMultiplier(2),
    backoff.WithMaxInterval(2 * time.Second),
    backoff.WithMaxElapsedTime(5 * time.Second),
)
err := backoff.Retry(operation, backoffConfig)
```

**Location**: `/usr/local/bin/claude-proxy` | **Environment**: `ANTHROPIC_BASE_URL=http://127.0.0.1:8082` in `.zshenv`

### WP-13: Launchd Service Configuration

The Go proxy runs as a macOS launchd daemon for auto-restart on crash and boot persistence.

**Plist**: `/Library/LaunchDaemons/com.terryli.claude-proxy.plist`

Full plist configuration, commands, verification checklist, and debugging: [references/launchd-configuration.md](./references/launchd-configuration.md)

### WP-14: OAuth Token Auto-Refresh

Background goroutine refreshes OAuth tokens every 30 minutes, 5 minutes before expiry. Falls back to Keychain if API refresh fails.

Full implementation and refresh logic: [references/oauth-auto-refresh.md](./references/oauth-auto-refresh.md)

---

## Anti-Patterns Summary

Full details with code examples: [references/anti-patterns.md](./references/anti-patterns.md)

| ID     | Severity | Gotcha                                                 | Fix                                                                    |
| ------ | -------- | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| CCP-01 | HIGH     | ANTHROPIC_BASE_URL alone without ANTHROPIC_API_KEY     | Set `ANTHROPIC_API_KEY=proxy-managed`                                  |
| CCP-02 | HIGH     | Missing `anthropic-beta: oauth-2025-04-20` header      | Append to existing beta headers                                        |
| CCP-03 | MEDIUM   | Using `/api/oauth/claude_cli/create_api_key` endpoint  | Requires `org:create_api_key` scope (users only have `user:inference`) |
| CCP-04 | HIGH     | Lowercase keychain service `"claude-code-credentials"` | Actual name has space: `"Claude Code-credentials"`                     |
| CCP-05 | MEDIUM   | Reading `~/.claude/.credentials.json` as primary       | Keychain is SSoT; credential file is stale fallback                    |
| CCP-06 | HIGH     | Hardcoding OAuth tokens                                | Tokens expire; read dynamically with cache                             |
| CCP-07 | HIGH     | Using `gh auth token` in proxy/hooks                   | Causes process storms (recursive spawning)                             |
| CCP-08 | HIGH     | ANTHROPIC_API_KEY set in env while having OAuth token  | Auth conflict warning in Claude Code; unset it                         |
| CCP-09 | MEDIUM   | cache_control param sent to MiniMax                    | MiniMax doesn't support it; remove from allowedParams                  |
| CCP-10 | MEDIUM   | Setting ANTHROPIC_API_KEY to real key while proxy runs | Proxy forwards it to all providers, leaking key                        |
| CCP-11 | MEDIUM   | Not handling `/v1/messages/count_tokens`               | Causes auth failures on preflight requests                             |
| CCP-12 | LOW      | Running proxy on 0.0.0.0                               | Bind to 127.0.0.1 for security                                         |

---

## TodoWrite Task Templates

Setup, provider addition, diagnostics, and disable templates: [references/task-templates.md](./references/task-templates.md)

---

## Reference Implementation

The working production deployment (Go proxy is primary):

| File                                                    | Purpose                          |
| ------------------------------------------------------- | -------------------------------- |
| `/usr/local/bin/claude-proxy`                           | Go proxy binary (~960 lines)     |
| `~/.claude/tools/claude-code-proxy-go/main.go`          | Go proxy source                  |
| `~/.claude/tools/claude-code-proxy-go/oauth_refresh.go` | OAuth auto-refresh (80 lines)    |
| `~/.claude/tools/claude-code-proxy-go/.env`             | Provider config (chmod 600)      |
| `/Library/LaunchDaemons/com.terryli.claude-proxy.plist` | launchd config                   |
| `~/.zshenv`                                             | Environment (ANTHROPIC_BASE_URL) |

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Anti-patterns table matches [references/anti-patterns.md](./references/anti-patterns.md)
2. [ ] Working patterns verified against proxy.py source
3. [ ] No hardcoded OAuth tokens in examples
4. [ ] Beta header version current (`oauth-2025-04-20`)
5. [ ] All internal links use relative paths (`./references/...`)
6. [ ] Link validator passes
7. [ ] Skill validator passes
8. [ ] Append changes to [references/evolution-log.md](./references/evolution-log.md)

---

## Troubleshooting

| Issue                                  | Cause                                          | Solution                                         |
| -------------------------------------- | ---------------------------------------------- | ------------------------------------------------ |
| Claude Code ignores ANTHROPIC_BASE_URL | Missing ANTHROPIC_API_KEY (CCP-01)             | Set `ANTHROPIC_API_KEY=proxy-managed` in .zshenv |
| 401 Unauthorized from Anthropic        | Missing anthropic-beta header (CCP-02)         | Ensure proxy appends `oauth-2025-04-20`          |
| Keychain read returns empty            | Wrong service name (CCP-04)                    | Use `"Claude Code-credentials"` (with space)     |
| Proxy forwards real API key            | ANTHROPIC_API_KEY set to real key (CCP-10)     | Use `proxy-managed` sentinel value               |
| count_tokens auth failure              | Missing endpoint handler (CCP-11)              | Proxy must handle `/v1/messages/count_tokens`    |
| Proxy accessible from network          | Bound to 0.0.0.0 (CCP-12)                      | Bind to 127.0.0.1 only                           |
| Process storms on enable               | gh auth token in hooks (CCP-07)                | Never call gh CLI from hooks/credential helpers  |
| MiniMax returns wrong model name       | MiniMax quirk                                  | Cosmetic only; Claude Code handles it            |
| Token expired after 5 min              | Cache TTL (WP-05)                              | Normal behavior; proxy re-reads from Keychain    |
| Auth conflict warning in Claude Code   | ANTHROPIC_API_KEY set (CCP-08)                 | Unset ANTHROPIC_API_KEY in .zshenv               |
| cache_control.ephemeral.scope error    | MiniMax doesn't support cache_control (CCP-09) | Remove cache_control from allowedParams          |
