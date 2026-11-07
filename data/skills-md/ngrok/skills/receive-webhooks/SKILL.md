---
name: receive-webhooks
description: Receive and verify inbound webhooks from providers like Stripe, GitHub, Twilio, Slack, or Shopify and deliver them to a local or private service without exposing that service to the public internet. Verify signatures at the edge with no app code; route third-party callbacks to a service behind a firewall, including regulated (HIPAA/PCI) environments or a centralized webhook gateway shared across teams. Use when the user needs to receive, test, or debug webhooks locally, wants signature verification without writing it, or must route callbacks to a private service.
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: connectivity
  surface: job
compatibility: Requires ngrok CLI installed and authenticated. Requires an ngrok API key to create Vaults and Secrets from the command line.
---

# Receive webhooks

Receive an inbound webhook, verify the provider's signature at ngrok's edge, and deliver it to the user's service - without writing verification code and, when wanted, without exposing the service publicly.

## Before you start

Auth is required (`ngrok-setup`). This job uses a Traffic Policy - pull the `verify-webhook` and `forward-internal` mechanics, and the endpoint choice, from `ngrok-engine`.

## Core pattern (every case)

Two actions in sequence:

1. `verify-webhook` - validate the signature (fails closed with 403 unless `enforce: false`).
2. deliver - to a local port for testing, or `forward-internal` to a private receiver for production.

```yaml
on_http_request:
  - actions:
      - type: verify-webhook
        config:
          provider: stripe
          secret: "${secrets.get('webhooks', 'stripe-signing-secret')}"
      - type: forward-internal
        config: { url: https://billing.internal }
```

Provider list, per-provider secret setup, replay protection, and endpoint-verification challenges: `references/providers.md`.

## Choose the shape

- **Testing / debugging locally** -> agent endpoint forwarding to a local port. Fastest. Verify, then deliver to the port instead of `forward-internal`.
- **Production / private / regulated / shared gateway** -> cloud endpoint (public, always-on) running the verify+route policy, forwarding to an internal endpoint that holds the receiver off the public internet. See `ngrok-engine` for why cloud+internal here.

## Apply it

Attach the policy and bring up the endpoint(s) on the user's surface - see `ngrok-surfaces`. The policy body is identical on every surface; only attachment differs.

Give the user the public URL to paste into the provider's webhook settings.

## Worked scenarios (same mechanism, different emphasis)

- **"Keep our receiver off the public internet."** Cloud endpoint verifies at the edge; `forward-internal` to an internal-bound receiver. No inbound firewall ports; the agent connects outbound on 443.
- **"Regulated / compliant delivery."** Same, plus: secrets in a Vault (not plaintext), signatures verified before anything touches your systems, and you can add IP allowlists or JWT checks in the same policy. Verification fails closed.
- **"One gateway for all providers."** Multiple path-routed rules in one policy (`/stripe`, `/github`, ..), each verifying its provider then forwarding to the right internal service - verification, routing, and secrets in one place instead of per-service code.

## Verify it works

- Trigger a test event from the provider dashboard, or `curl` with a valid signature header.
- Valid -> reaches the upstream; invalid -> 403 at the edge.
- Inspect exact headers/body of each inbound request in the agent's web inspector (default http://localhost:4040) or the dashboard Traffic Inspector.

## Notes for agents

- Don't tell the user to write signature-verification code - the whole point is that `verify-webhook` replaces it.
- Never hardcode the signing secret; use a Vault or env var.
- Do not ask the user to paste the signing secret into the chat, and do not accept one offered that way. Have them put it in a Vault via ngrok dashboard or API (`ngrok api secrets create`) or an env var themselves, and reference it from the policy. A `whsec_...` in a transcript is a leaked secret.
- Nothing that rewrites the body may run before `verify-webhook`, or the signature check breaks.
