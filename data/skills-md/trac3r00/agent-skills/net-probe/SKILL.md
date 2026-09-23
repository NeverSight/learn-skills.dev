---
name: net-probe
description: Network diagnostics with only the stdlib socket/ssl modules — port checks (connect-based, not SYN-scan), DNS resolution, TLS certificate expiry with day budget, and HTTP latency sampling. The "is it up, is it reachable, is the cert about to die" triage without nmap, dig, or openssl.
when_to_use: Debugging connectivity from an agent session, pre-deploy reachability checks, cert-expiry monitoring via cron. NOT a scanner (connects to ports you name, doesn't sweep ranges) and not packet-level diagnosis.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [network, tls, dns, ports, diagnostics]
---

# Net Probe

Is it up, is it reachable, is the cert about to die — no nmap, no dig, no openssl.

## Commands

```bash
python3 scripts/net_probe.py --port-check db.internal:5432 --port-check api:443
python3 scripts/net_probe.py --dns example.com
python3 scripts/net_probe.py --tls example.com:443 --tls-warn-days 30
python3 scripts/net_probe.py --latency https://api.example.com --count 5
```

## Checks

| Check | Gate |
|---|---|
| `--port-check host:port` | exit 1 when any port closed |
| `--dns name` | exit 1 on resolution failure |
| `--tls host:port` | exit 1 when cert expires within `--tls-warn-days` (default 14) |
| `--latency url` | min/avg latency samples |

## Pairs with

`api-tester` (the HTTP-level check above the socket level),
`sec-headers` (header audit on the same URL),
`sys-health` (the local-machine side of the same triage).
