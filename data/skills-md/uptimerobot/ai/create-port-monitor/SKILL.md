---
name: create-port-monitor
description: Create a PORT monitor that opens a TCP connection to a host:port and alerts when the port is not accepting connections.
tags: [monitoring, port, tcp, create, uptimerobot]
---

# Create a PORT monitor

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Use when the user wants to check that a specific TCP port is open on a host — databases, SSH, SMTP, custom services, etc.

**Tool:** `create-monitor`
**Required params:** `friendlyName`, `type: "PORT"`, `url` (host or IP, no scheme), `port` (1–65535).

## Minimal call

```json
{
  "friendlyName": "Postgres primary",
  "type": "PORT",
  "url": "db.example.com",
  "port": 5432
}
```

## Common optional params

- `timeout` — how long to wait for the TCP handshake (1–60s).
- `interval`, `responseTimeThreshold`, `assignedAlertContacts`, `tagNames`, `maintenanceWindowsIds`.
- `config.ipVersion` — `IPv4` or `IPv6`.

## Examples

SMTP over IPv4:

```json
{
  "friendlyName": "Mail relay",
  "type": "PORT",
  "url": "smtp.example.com",
  "port": 25,
  "timeout": 15,
  "interval": 300
}
```

SSH with alert contacts:

```json
{
  "friendlyName": "Bastion SSH",
  "type": "PORT",
  "url": "bastion.example.com",
  "port": 22,
  "assignedAlertContacts": [
    { "alertContactId": "10", "threshold": 0, "recurrence": 0 }
  ],
  "tagNames": ["infra", "security"]
}
```

## Common mistakes

- Passing `https://host:443` as `url`. Split into `url: "host"` and `port: 443`.
- Passing `port` as a string. It must be an integer 1–65535.
- Passing `port` outside the valid range (e.g. 0 or 70000). The server rejects with `-29001`.
- Using PORT for an HTTP health check where you actually want status code / body — prefer `HTTP` or `KEYWORD`.

## After creation

Call `get-monitor-details` to confirm host + port were stored.

## Related

- `create-udp-monitor` — for UDP services (DNS, NTP, QUIC, game servers).
- `create-ping-monitor` — for reachability without a specific port.
