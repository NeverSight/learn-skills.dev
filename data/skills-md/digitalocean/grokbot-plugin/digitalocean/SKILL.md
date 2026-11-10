---
name: digitalocean
description: >-
  DigitalOcean product guidance: pick the right service and skill, confirm which
  team is active, and pull current docs before acting. Use when the user says
  "on DigitalOcean", "my DO account", "which DigitalOcean product", or asks
  what to use on DigitalOcean without naming a service.
---
# DigitalOcean root router

Route DigitalOcean work to the right skill and DigitalOcean service. All tools
are reached through the single hosted **DigitalOcean MCP** server
(`mcp.digitalocean.com/mcp`, server key `digitalocean`). Do not call write tools
from this skill.

## Before any infrastructure change

1. Load the **digitalocean-safety** policy (approval tiers and global rules).
1. State which **DigitalOcean team** the OAuth grant targets. If unclear, use
   `account-get-information` (accounts service) once DigitalOcean MCP is connected.
1. Prefer **read-only** calls first to establish current state.

## Choose a skill

| User intent                | Skill                     | DigitalOcean service(s)                      |
| -------------------------- | ------------------------- | -------------------------------------------- |
| Connect, auth, 401/403/429 | digitalocean-connect      | DigitalOcean MCP (connection only)           |
| Cost, balance, invoices    | digitalocean-costs        | digitalocean-droplets, digitalocean-accounts |
| Droplets, VMs, snapshots   | digitalocean-droplets     | digitalocean-droplets                        |
| App Platform, deploy, logs | digitalocean-app-platform | digitalocean-apps, digitalocean-docs         |
| Managed databases          | digitalocean-databases    | digitalocean-databases                       |
| DNS, firewalls, LB, VPC    | digitalocean-networking   | digitalocean-networking                      |
| Uptime, alerts, metrics    | digitalocean-monitoring   | digitalocean-insights                        |
| Incidents, outages, errors | digitalocean-troubleshoot | Multiple (read-first)                        |
| Inventory, cleanup ideas   | digitalocean-inventory    | Multiple (read-first)                        |
| Product/docs questions     | digitalocean (this skill) | digitalocean-docs                            |

The skills above cover the most common products. DigitalOcean MCP reaches
**every** DigitalOcean product (for example Kubernetes, Spaces, Functions,
Container Registry, GenAI). For a product without a dedicated skill, use
`find_tools` to discover the right tool and `invoke_tool` to run it, and still
apply **digitalocean-safety** tiers (unmapped writes are Tier 3 / confirm).

## Docs

For product selection or unfamiliar APIs, search the docs service with
`docs-search` before proposing changes.

## Connecting

One hosted DigitalOcean MCP server fronts every service, so a single OAuth
sign-in covers droplets, apps, accounts, databases, networking, insights, and
docs. Use `find_tools` to discover a tool and `invoke_tool` to run it.

If the **digitalocean** MCP server is disabled or unsigned, hand off to
**digitalocean-connect**.
