---
name: whop-app-integration
description: End-to-end implementation guide for adding Whop licensing to apps with a secure backend, activation flow, and webhook synchronization. Use when tasks involve Whop checkout setup, membership/license activation, validate_license integration, webhook signature verification, revocation handling, device-binding policies, or periodic license checks in Node.js, Python, iOS, or macOS apps.
---

# Whop App Integration

## Overview

Implement Whop licensing using a backend-first architecture, then connect app activation UX, periodic revalidation, and webhook-driven entitlement sync.

## Required Architecture

- Keep Whop API keys only on backend services.
- Route requests as `app -> backend -> Whop API`.
- Process Whop webhooks on backend and persist entitlement state locally.
- Reject client-only designs that send `Authorization: Bearer` Whop keys from app code.

## Workflow

1. Define entitlement policy before coding
- Choose plan model: subscription or perpetual.
- Define device policy: one device, up to N devices, or manual transfer.
- Define offline grace policy and revocation timing.
- Persist these as explicit backend config.

2. Configure Whop assets
- Configure product and plans; confirm each `purchase_url`.
- Create API key with minimum scopes required by the chosen endpoints.
- Configure webhook endpoint and secret.
- Enable at least: `membership.activated`, `membership.deactivated`, `membership.cancel_at_period_end_changed`.

3. Implement backend contract
- Implement `POST /api/license/activate` that receives license input and `hwid`, then calls Whop license validation.
- Implement `POST /api/webhooks/whop` and verify signature before processing payload.
- Store entitlements keyed by Whop membership id and user id.
- Make webhook handling idempotent.

4. Implement app activation
- Build input UI for license key and loading/error states.
- Send activation requests only to backend endpoints.
- Store only activation status, timestamps, and non-secret metadata in app storage.
- Present user-safe messages for invalid license, conflict, and connectivity failures.

5. Implement periodic validation
- Revalidate on launch and on time interval (for example every 24h).
- Reuse the same metadata strategy used during activation.
- If offline, apply a bounded grace window before disabling paid access.

6. Implement cancellation and revocation sync
- Revoke local entitlement on `membership.deactivated`.
- Update renewal state on cancel-at-period-end changes.
- Treat webhook events as source of truth for passive status changes.

7. Complete release checks
- Test activation success, mismatch, and not-found cases.
- Test webhook signature pass/fail handling.
- Test transfer/reset behavior if supported by product policy.
- Test offline grace expiration behavior.

## Implementation Rules

- Read `references/implementation-playbook.md` for endpoint matrix, payloads, and error mappings.
- Read `references/platform-recipes.md` for Node, Python, and Swift implementation recipes.
- Use `scripts/verify_whop_webhook.py` to test signature verification with captured payloads.
- Prefer current official Whop docs when endpoint versions differ from existing code.
- Keep structured logs with request id, membership id, event type, HTTP status, and API error body.

## Output Requirements

When using this skill in a task:

1. Deliver backend route(s), webhook handler(s), and app activation flow updates.
2. Add or update automated tests for activation, webhook verification, and revocation.
3. Document security-sensitive implementation choices in changed files.
4. Return a checklist that separates completed items from pending items.
