---
name: helipod
description: Use when the user mentions Helipod (helipod.io) or wants to work with their Helipod cloud account (containers, VPS, domains, email, AI gateway) from the agent. Explains keys, safety rules for paid and destructive actions, and which Helipod skill or tool fits the task.
---

# Helipod

Helipod is a cloud platform in Indonesia: containers (deploy apps from Git, images or Dockerfiles), VPS, domain registration and DNS, email sending, and an AI gateway. Everything is billed from a prepaid wallet in Rupiah (IDR).

## Access

- **MCP tools** (preferred): if tools like `list_projects`, `create_service`, `list_vps_plans` are available, use them.
- **Without MCP**: call the HTTP API with `Authorization: Bearer $HELIPOD_API_KEY`.
  - VPS, Container, Domain APIs: `https://api.helipod.io/api` (`/containers/...`, `/vps/...`, `/domains/...`)
  - Email API: `https://mail.helipod.io/api/email` with `$HELIPOD_EMAIL_API_KEY` (a separate email key)
  - AI gateway: `https://ai.helipod.io/v1` with a `hel_ai_...` key (OpenAI and Anthropic compatible)
- Keys are created in the dashboard: Project → Settings → API keys. A key is limited to the products and project chosen there; `403 SCOPE_NOT_ALLOWED` means the key lacks that product, `404` on an id means it is outside the key's reach.
- Every response is `{ "success": true, "data": ... }` or `{ "success": false, "error": "...", "code": "..." }`.

## Rules (always)

1. **Money**: before anything that costs money (create/deploy/scale a service, create/renew/upgrade a VPS, register/renew/transfer a domain, deploy a template), get the price first (`dryRun: true` on container calls, `list_vps_plans` / `get_vps_renewal_options`, `domain_prices`), tell the user the amount in IDR, and wait for a clear yes.
2. **Destructive**: before deleting a service/volume, terminating/reinstalling a VPS, rolling back a snapshot or replacing DNS records, say exactly what will be lost and wait for a clear yes.
3. **Background work**: deploys and VPS actions are asynchronous. Poll (`get_deployment`, `get_vps`) every few seconds until they settle; on a failed deploy read `get_deployment_logs` and explain the cause.
4. **Secrets**: never print passwords, API keys or secret variable values unless the user asks. Store app secrets as secret variables, never in code.
5. Use an `idempotencyKey` when retrying a create or deploy, so nothing happens twice.

## Which skill

| Task | Skill |
|---|---|
| Deploy an app or database, env vars, domains, scaling, logs | `helipod-deploy` |
| Servers with root access | `helipod-vps` |
| Buy a domain, DNS, point a domain at an app | `helipod-domains` |
| Send email from an app | `helipod-email` |
| Use AI models in an app through Helipod | `helipod-ai-gateway` |

Docs: https://docs.helipod.io
