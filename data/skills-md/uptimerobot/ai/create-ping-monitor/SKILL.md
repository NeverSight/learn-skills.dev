---
name: create-ping-monitor
description: Create a PING monitor that sends ICMP echo requests to a hostname or IP and alerts on packet loss / timeout.
tags: [monitoring, ping, icmp, create, uptimerobot]
---

# Create a PING monitor

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Use when the user wants basic network reachability for a host. PING does not care about HTTP status or content — it just checks whether the host responds to ICMP within the timeout.

**Tool:** `create-monitor`
**Required params:** `friendlyName`, `type: "PING"`, `url` (hostname or IP, **no scheme**).

## Minimal call

```json
{
  "friendlyName": "Office gateway",
  "type": "PING",
  "url": "gw.example.com"
}
```

IP addresses work too:

```json
{
  "friendlyName": "VPN endpoint",
  "type": "PING",
  "url": "203.0.113.42"
}
```

## Common optional params

- `interval`, `timeout`, `responseTimeThreshold`, `assignedAlertContacts`, `tagNames`, `maintenanceWindowsIds` — same as HTTP.
- `config.ipVersion` — force `IPv4` or `IPv6`. Defaults to auto.

## Example with IPv6

```json
{
  "friendlyName": "Public DNS v6",
  "type": "PING",
  "url": "2001:4860:4860::8888",
  "config": { "ipVersion": "IPv6" },
  "interval": 120
}
```

## Common mistakes

- Passing `https://host.example.com` — PING requires a bare hostname or IP. Strip the scheme and path.
- Expecting content or status code checks — PING cannot do those. Use HTTP / KEYWORD / API instead.
- Hostname must resolve publicly. Internal-only hostnames will always be down; use a reachable public name or a public IP.
- Some networks block ICMP. If the host is actually up but ICMP is filtered, consider a `PORT` monitor on a known open TCP port instead.

## After creation

Call `get-monitor-details` to confirm.

## Related

- `create-port-monitor` — when ICMP is blocked but a TCP port is open.
- `create-http-monitor` — when the user has an HTTP(S) URL, not a bare host.
