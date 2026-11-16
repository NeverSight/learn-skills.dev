---
name: targeted-proxy-access
description: Use when a page fetch fails because the site is blocked, geo-restricted, or sanctioned in this network (timeouts, connection resets, 403 from the region) — whether the fetch came from an MCP server, a browser, or the harness's own built-in page reader; when a domain routed through the tunnel still fails and the gateway, routed domains, or wiring needs checking; or when the user asks to reach a domain through their VLESS/Trojan configs without tunneling the whole system.
---

# Targeted Proxy Access

A local HTTP proxy on `127.0.0.1:1080` that sends **only chosen domains** through a
pool of VLESS/Trojan configs and connects everything else directly. Separately launched
fetchers go through `proxy-tunnel-exec`, which injects the proxy only while the gateway is
healthy; a harness's own in-process reader gets the standard proxy variables in its own
environment instead.

```
fetch tool ──► 127.0.0.1:1080 ──► domain listed in domains.txt? ──► tunnel config
                                     └─ no ──────────────────────► direct
```

This keeps normal pages fast and inside the local network path: only the blocked
hostnames borrow the tunnel's bandwidth. **You supply the configs:** the skill ships
no share links. Bring your own `vless://` / `trojan://` links (or an installed
v2rayN), or there is nothing to tunnel through.

The skill name is `targeted-proxy-access`; the gateway's existing command names,
`PROXY_TUNNEL_*` settings, service, and data directories retain `proxy-tunnel` for
compatibility. If upgrading from the former `skills/proxy-tunnel/` folder, follow
[the rename upgrade steps](references/setup.md#upgrading-after-the-skill-rename)
to refresh installed links and launch paths; existing pool and state files stay put.

## Use it

1. **Check the gateway.** `python3 scripts/tunnel.py status` — if it says `stopped`,
   start it with `up`. One probe of the canary is enough; do not loop.
2. **Point the page reader at the gateway**, once per client, in whichever shape it takes:
   - **A separate process** — an MCP server, a browser, a CLI fetcher — is launched through
     the wrapper: a **one-time edit per server**, described in
     `references/setup.md#wiring-a-fetch-tool`. Servers that only talk to a local service
     need no edit.
   - **The harness's own page reader** runs inside the agent process and cannot be wrapped.
     Give that process the standard `HTTP_PROXY`/`HTTPS_PROXY` and a `NO_PROXY` that keeps
     loopback and direct-only API hosts out — once, in however it gets its environment. See
     [in-process readers](references/setup.md#in-process-readers).
   Once wired, a normal call is all that is needed: do not add proxy flags per call, and do
   not edit the client config to "turn the proxy on".
3. **Retry once before diagnosing.** A single `fetch failed` is usually one reset
   from the public config, not a dead tunnel. Call the tool again.
4. **Locate the failing layer, first match wins:**
   - `status` reports `canary: FAILED` → the whole tunnel is down: `up --refresh`,
     then retry.
   - `python3 scripts/tunnel.py fetch <url>` returns a 2xx page where the client
     tool fails → the client is not using the proxy, or the tunnel is paused: run
     `doctor`, which notes a paused tunnel and flags a client config that never
     mentions the launcher. For a separate server, restart it — one started before the
     config edit keeps running direct — or wire it if its config still carries the
     original command. For the harness's own reader, check the process environment and
     restart that process.
   - Both fail and no listed entry covers the host → the request went direct. When
     the direct path is blocked in this network, `learn <url>` and retry the tool: it
     routes the domain only if the tunnel is what made that URL work, and leaves the
     list alone otherwise. An entry covers subdomains (`x.com` handles `api.x.com`).
     Use `allow <domain>` only when you already know it needs the tunnel. If the retry
     still fails, compare again with `tunnel.py fetch`: an unwired client is a separate
     fault.
   - Both fail and the host is already routed → rotate with `up --refresh`, then
     call the tool again. If that does not help either, the site refuses these exits
     or is down: report it unavailable rather than widening the route.

**The harness's own reader sees more than the gateway.** It reads the page, so it can
spot a block page that a CONNECT proxy cannot. When it fails on a page:

1. `learn <url>` — tries direct, then through the tunnel, and keeps the route only when
   the tunnel is what made the URL work. It reverts and fails if neither route works.
2. Retry the reader once.
3. A 2xx block or consent page is the site's answer, not a route fault: report it and
   leave the list alone. `learn` compares status, not content, so it cannot make that
   call; the reader's content can. It also refuses a 429 or 451 outright: a rate limit
   or a legal block is the site's answer, not a route fault.

## Commands

| Command | Does |
|---|---|
| `status` | gateway pid/port, canary health, last-good config, pool and domain counts |
| `up [--refresh]` | start the gateway; `--refresh` ignores the last-good config and rescans |
| `serve [--interval N]` | keep the gateway running and rotate dead configs; the systemd service runs this |
| `down` | stop the gateway |
| `allow <domain>...` | route these domains (and subdomains) through the tunnel and reload the gateway |
| `disallow <domain>...` | stop routing them and reload the gateway |
| `domains` | list routed domains |
| `list` | pool entries in priority order |
| `fetch <url> [--raw]` | fetch through the gateway without any MCP |
| `learn <url>` | try direct, then the tunnel; route the domain only when only the tunnel works |
| `env` | print raw proxy settings (only for clients that cannot use the launcher) |
| `pause` / `resume` | stop/restart injecting the proxy at launch, without touching any client config |
| `doctor` | check pool, service, launcher, and client wiring in one go |
| `setup [--db PATH] [--group good] [--service]` | fresh machine: get xray, seed the pool, install the launcher (service only with `--service`) |
| `seed [--db PATH] [--group good] [--force]` | rebuild `pool.txt` from a v2rayN database |
| `install-wrapper` / `install-service` | the two `setup` steps, separately |

`allow`, `disallow` and `learn` rewrite entry lines only: whole-line comments and blank
lines in `domains.txt` stay.

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

- **Route only what the tunnel fixes.** Unlisted domains go direct through the
  gateway, so `domains.txt` is a list of exceptions, not a copy of the sites you
  read: a site that already answers direct gains nothing from the hop, and one that
  refuses datacenter addresses keeps refusing. Add the **smallest** domain that
  works (`youtube.com`, not `google.com`); a wide entry sends unrelated traffic
  through a shared public config. A routed entry carries everything that process does
  on the domain — including credentialed requests — through that exit, and a plain
  `http://` page travels in clear through it.
- Never edit `gateway.json`: it is generated on every `up`, `allow`, `disallow` and `learn`.
- Shared public configs reset roughly one request in three. Retry, then rotate; do not
  conclude the site is unreachable from one failure.
- The pool is ordered, and `up` tries from the top, so put preferred configs first in
  `pool.txt`. Manual entries are just share links, one per line.
- If `status` shows the pool empty or exhausted, reseed it (`seed --force`, or
  `seed --db PATH --force`) or ask the user for fresh links.
- Do not route a search tool that only calls a local service through the tunnel (for
  example a local SearXNG): the proxy hop adds latency and a dependency without
  changing results.
- Do not add sites that refuse datacenter exits: Reddit answers a login/anti-bot
  wall, and Trustpilot or Product Hunt answer 403 both ways. Report those as
  unavailable instead of retrying; search snippets are the fallback. The
  [measured table](references/setup.md#sites-these-exits-do-not-unlock) is a snapshot
  from one exit, and your configs leave from somewhere else.

## Setup and wiring (other agents, browser, systemd)

See `references/setup.md` for first-time seeding, wiring the proxy into an MCP server
or Playwright, running the gateway as a user service, and troubleshooting. The examples
there name specific tools (mcp-searxng, opencode, Claude Code) because those were
exercised; any client that starts a command with args and env follows the same pattern.
