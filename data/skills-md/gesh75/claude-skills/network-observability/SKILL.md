---
name: network-observability
description: Capacity, SLO/SLA, NOC health, telemetry (SNMP, streaming, NetFlow), probes, and error budgets for the network service. Use for dashboards, capacity reviews, "is this WAN healthy", or SLA misses. Not for a single-box CLI debug (netops-mcp).
origin: snm-pack
---

# Network observability

You cannot manage what you do not measure. Prefer **probes + telemetry +
error budget** over a wall of unactionable graphs.

## When to use

- SLO/SLA definition or miss
- Capacity (WAN, internet, DC fabric, wireless, licenses)
- NOC dashboard / health score
- "Is the network the cause?"
- NetFlow / streaming telemetry / SNMP design

## Service SLOs (default starting points)

| Service | SLO (monthly) | Probe |
|---------|---------------|-------|
| Core L3 campus | 99.99% | IP SLA + BGP |
| WAN / SD-WAN site | 99.95% dual-home | both underlays + app |
| Internet egress | 99.95% | dual ISP synthetics |
| Wireless (clinical voice) | 99.9% + MOS | location-aware |
| EHR path (broker→app) | 99.99% | TCP 443 synthetic |
| Guest wifi | 99.5% | best-effort |

Error budget drives change freeze, not feelings. A miss is a Problem
ticket, not a slide.

Capacity math: [reference/capacity.md](reference/capacity.md).

## Telemetry stack

1. **Synthetic probes** on every named service (source of truth for SLO)
2. **Streaming telemetry / SNMP** for devices (interface, optics, CPU, env)
3. **Flow** (NetFlow/IPFIX/sFlow) sampled — never full PCAP on clinical
4. **AAA / NAC / VPN** logs into the SIEM
5. **Config diff** as an event (every unauthorized change is an incident)

If a box cannot stream, SNMP + trap is acceptable; "we'll SSH when it
breaks" is not.

## Health score (NOC)

One number 0–100 per site: probes (40), errors/discards (20), control
plane (20), capacity headroom (10), backup freshness (10). Red < 70.
Do not average a dying OR with a fine cafeteria SSID — score **services**.

## "Is it the network?"

Packet walk (`network-diagrams`) + probe at each hop + the app's own
golden signal. If probes are green and the app is red, say so and stop
taking the blame.

## Output

```text
SERVICE
- SLO · budget remaining · probe

EVIDENCE
- hop / counter / flow (no payloads)

CAPACITY
- 95th · headroom · time-to-70%

ACTIONS
- Problem / Change / buy · owner · due
```

## Reference Files
- [reference/capacity.md](reference/capacity.md)
