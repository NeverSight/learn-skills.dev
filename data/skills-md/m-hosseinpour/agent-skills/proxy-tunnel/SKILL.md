---
name: proxy-tunnel
description: Use when a page fetch fails because the site is blocked, geo-restricted, or sanctioned in this network (timeouts, connection resets, 403 from the region), or when the user asks to reach a domain through their VLESS/Trojan configs without tunneling the whole system.
---

# Proxy Tunnel

A local HTTP proxy on `127.0.0.1:1080` that sends **only chosen domains** through a
pool of VLESS/Trojan configs and connects everything else directly. Fetch servers are
launched through `proxy-tunnel-exec`, which injects the proxy only while the gateway
is healthy, so no client config carries proxy settings.

```
fetch tool ──► 127.0.0.1:1080 ──► domain listed in domains.txt? ──► tunnel config
                                     └─ no ──────────────────────► direct
```

This keeps normal pages fast and inside the local network path: only the blocked
hostnames borrow the tunnel's bandwidth. **You supply the configs:** the skill ships
no share links. Bring your own `vless://` / `trojan://` links (or an installed
v2rayN), or there is nothing to tunnel through.

## Use it

1. **Check the gateway.** `python3 scripts/tunnel.py status` — if it says `stopped`,
   start it with `up`. One probe of the canary is enough; do not loop.
2. **Fetch through the URL reader.** Whatever tool your harness gives you for reading
   pages (an MCP `web_url_read`, a fetch tool, a browser) must be launched through the
   wrapper — a **one-time edit per MCP server**, described in
   `references/setup.md#wiring-a-fetch-tool`. Once wired, a normal call is all that is
   needed: do not add proxy flags per call, and do not edit the client config to "turn
   the proxy on".
3. **Retry once before diagnosing.** A single `fetch failed` is usually one reset
   from the public config, not a dead tunnel. Call the tool again.
4. **If the domain was never routed**, the first attempt fails because it went
   direct. Run `allow <domain>` and retry. Routing is by domain suffix, so
   `allow x.com` covers `api.x.com`.
5. **If the whole tunnel is down** (`status` shows `canary: FAILED`), run
   `up --refresh` to rotate to another config, then retry.
6. **If the tunnel is healthy but fetches still go direct**, the client was launched
   without the wrapper: run `doctor`; it prints a note when no known client config
   mentions the launcher, and `FAIL` when a known client is only half-wired.

## Commands

| Command | Does |
|---|---|
| `status` | gateway pid/port, canary health, last-good config, pool and domain counts |
| `up [--refresh]` | start the gateway; `--refresh` ignores the last-good config and rescans |
| `serve [--interval N]` | keep the gateway running and rotate dead configs; the systemd service runs this |
| `down` | stop the gateway |
| `allow <domain>...` | route these domains (and subdomains) through the tunnel, hot-reload |
| `disallow <domain>...` | stop routing them |
| `domains` | list routed domains |
| `list` | pool entries in priority order |
| `fetch <url> [--raw]` | fetch through the gateway without any MCP |
| `env` | print raw proxy settings (only for clients that cannot use the launcher) |
| `pause` / `resume` | stop/restart injecting the proxy at launch, without touching any client config |
| `doctor` | check pool, service, launcher, and client wiring in one go |
| `setup [--db PATH] [--group good] [--service]` | fresh machine: get xray, seed the pool, install the launcher (service only with `--service`) |
| `seed [--db PATH] [--group good] [--force]` | rebuild `pool.txt` from a v2rayN database |
| `install-wrapper` / `install-service` | the two `setup` steps, separately |

Run these commands from this skill's directory, or use the absolute path to
`scripts/tunnel.py`. Data lives in the platform config dir
(`~/.config/proxy-tunnel` on Linux, `~/Library/Application Support/proxy-tunnel` on
macOS, `%APPDATA%\proxy-tunnel` on Windows).

First run on a new machine, in order:

```bash
python3 scripts/tunnel.py setup     # downloads xray if no v2rayN/system binary exists
# paste vless:// / trojan:// links into pool.txt if setup could not seed from v2rayN
python3 scripts/tunnel.py up
python3 scripts/tunnel.py doctor
```

Then, once per client, change that client's command to the wrapper — `setup` cannot
edit your agent's config for you:

```
command: proxy-tunnel-exec        # stores no port or proxy; injects at launch
args:    ['--url-reader', <original command and args>]
```

Repeat for every MCP server that fetches pages (a URL reader, Playwright, a browser
tool) with the profile flag that server understands, then restart the agent so the
server relaunches through the wrapper. `references/setup.md#wiring-a-fetch-tool` has the
profile list, the opencode and Claude Code shapes, and the env-variable fallback for
clients whose command cannot be changed. Servers that only talk to a local service (a
search server, for instance) do not need wiring.

v2rayN is optional. When it is installed, `setup` and `seed` reuse its database and its
bundled xray; otherwise the official xray release is downloaded once, checksum-checked,
and kept in the data dir (`bin/xray-<version>/`) for later runs.

## Ground rules

- Add the **smallest** domain that works (`youtube.com`, not `google.com`). A wide
  entry sends unrelated traffic through a shared public config.
- Never edit `gateway.json`: it is generated on every `up` and `allow`.
- Shared public configs reset roughly one request in three. Retry, then rotate; do not
  conclude the site is unreachable from one failure.
- The pool is ordered, and `up` tries from the top, so put preferred configs first in
  `pool.txt`. Manual entries are just share links, one per line.
- If `status` shows the pool empty or exhausted, reseed it (`seed --force`, or
  `seed --db PATH --force`) or ask the user for fresh links.
- Do not route a search tool that only calls a local service through the tunnel (for
  example a local SearXNG): the proxy hop adds latency and a dependency without
  changing results.
- Reddit answers a login/anti-bot wall to these datacenter exits, and Trustpilot or
  Product Hunt answer 403 both ways. Report those as unavailable instead of retrying;
  search snippets are the fallback.

## Setup and wiring (other agents, browser, systemd)

See `references/setup.md` for first-time seeding, wiring the proxy into an MCP server
or Playwright, running the gateway as a user service, and troubleshooting. The examples
there name specific tools (mcp-searxng, opencode, Claude Code) because those were
exercised; any client that starts a command with args and env follows the same pattern.
