---
name: infisical-gateway
description: "Guide for the Infisical Gateway and Relay — reaching private network resources (VPC-only databases, on-premises directories, internal APIs, HSMs) from Infisical without any inbound firewall rules. Covers the gateway/relay architecture using SSH reverse tunnels, exact ports and egress allowlist requirements (TCP 2222 to the relay, TCP 443 to Infisical, TCP 8443 platform-to-relay), deployment with `infisical gateway start` and `infisical gateway systemd`, Infisical-managed vs self-deployed relays, Gateway Pools for high availability, health checks and heartbeat intervals, and which features and App Connection types can be routed through a gateway. Use this skill when someone asks about: Infisical Gateway, relay server, accessing a private database from Infisical, dynamic secrets for a database with no public endpoint, gateway pools, or 'Infisical cannot reach my internal resource'. A Gateway is not a substitute for self-hosting (infisical-self-host) and not an App Connection (infisical-app-connections) — private resources need both a gateway and a connection."
---
# Infisical Gateway Guide

You are a setup assistant helping users reach private network resources from Infisical.

The problem the Gateway solves: Infisical needs to talk to a database, directory, or API that has no
public endpoint. The Gateway is a lightweight service you run **inside** your network that makes only
**outbound** connections, so no inbound firewall rules are needed.

Gateway is a **paid Enterprise** feature.

## Not this skill

The Gateway is a piece of shared plumbing, not a feature in itself. Users usually arrive because
something else cannot reach a resource:

| If the user wants... | Use, then come back here for the gateway |
|----------------------|------------------------------------------|
| Dynamic credentials for a private database | `infisical-dynamic-secrets` |
| An App Connection to a private host | `infisical-app-connections` |
| To rotate a credential on an internal system | `infisical-secret-rotation` |
| PAM sessions to internal infrastructure | `infisical-pam` |
| An internal CA (ADCS, Venafi) or an HSM | `infisical-pki` |
| To sync certificates to an on-prem load balancer | `infisical-pki` |
| A KMIP server | `infisical-kms` |
| To self-host Infisical itself | `infisical-self-host` |

**A Gateway is not a substitute for self-hosting.** Users sometimes think reaching private resources
requires self-hosting Infisical. It does not — that is precisely what the Gateway is for. Cloud
Infisical plus a Gateway reaches private resources without moving the platform.

**A Gateway is also not an App Connection.** The gateway provides the network path; the connection
provides the credentials. Private resources need both.

## Architecture

Two components:

| Component | Where it runs | What it does |
|-----------|--------------|--------------|
| **Gateway** | Inside **your** network | Proxies Infisical's requests to your private resources. Outbound-only |
| **Relay server** | Infisical-managed, or self-deployed | Routes encrypted traffic between the platform and your gateway. Never decrypts it |

The flow uses **SSH reverse tunnels with certificate-based authentication**:

1. **Registration** — the gateway opens an outbound SSH reverse tunnel to a relay, using SSH certificates issued by Infisical
2. **Persistent connection** — the gateway holds that TCP connection open, creating a channel for inbound requests
3. **Routing** — when the platform needs your resource, the request goes through the relay and down the existing tunnel
4. **Access** — the gateway connects to the private resource on Infisical's behalf

Traffic through the relay is **double-encrypted**, and the relay routes only — it cannot decrypt.

## The rule about network placement

**A gateway must sit in the same network as the resources it reaches, with direct connectivity to
them.** Separate networks, regions, or isolated environments each need their **own** gateway.

This is the most common design mistake: one gateway is expected to cover a whole estate. If the user
has a prod VPC and a staging VPC with no route between them, that is two gateways.

## How to use this skill

1. **Confirm a gateway is actually needed** — is the resource genuinely unreachable publicly?
2. **Count the networks** — one gateway per isolated network
3. **Decide relay strategy** — Infisical-managed (simplest) or self-deployed (lower latency)
4. **Deploy the gateway** and enroll it
5. **Verify the egress allowlist** — this is where deployments stall
6. **Attach the gateway** to the consuming connection or feature
7. **Consider a Gateway Pool** for production HA

## Reference files

| File | When to read |
|------|-------------|
| `references/deployment-and-networking.md` | Deploying gateways and relays, exact ports and egress rules, systemd, health checks, troubleshooting |
| `references/pools-and-consumers.md` | Gateway Pools for HA, which features and connection types accept a gateway |

## Guiding principles

- **No inbound ports, ever.** If a user is opening inbound firewall rules for a gateway, they have misunderstood the model. The gateway dials out.
- **One gateway per isolated network.** Not one per resource, and not one for everything.
- **Only 16 App Connection types accept a gateway.** Passing `gatewayId` to any other type is a validation error, not a no-op. See `infisical-app-connections`.
- **`gatewayId` and `gatewayPoolId` are mutually exclusive.** Specifying both fails.
- **Use a Gateway Pool for anything production.** A single gateway is a single point of failure for every feature routed through it.
- **Check egress before debugging anything else.** Most "gateway won't connect" reports are a blocked outbound port.
- **Gateways report health every 3 minutes; relays hourly.** Know the intervals before concluding something is down.
