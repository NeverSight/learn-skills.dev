---
name: solvapay
description: >
  Integrate SolvaPay into any project -- SDK integration for Next.js, React, Express,
  and MCP servers; provider account onboarding; and hosted website checkout. Use this
  skill whenever the user mentions SolvaPay, payments, billing, monetization, pricing,
  subscriptions, paywalls, checkout, products, plans, customer portal, usage tracking,
  webhooks, or any payment-related setup, even if they don't explicitly say 'SolvaPay'.
---

# SolvaPay

Route user intent to the right domain guide and provide shared context.

## Quick Start

1. Identify the primary user intent from request keywords.
2. If intent is ambiguous, ask one disambiguation question.
3. Read the matching domain guide:
   - [sdk-integration/guide.md](sdk-integration/guide.md) -- SDK paywall, checkout, usage, webhooks
   - [website-checkout/guide.md](website-checkout/guide.md) -- hosted checkout for web apps
   - [provider-onboarding/guide.md](provider-onboarding/guide.md) -- account setup through go-live
4. Follow the domain guide to completion.

## Documentation Sources

Use this retrieval order for all domains:

1. SolvaPay Docs MCP server (preferred): https://docs.solvapay.com/mcp
2. Docs index fallback: https://docs.solvapay.com/llms.txt
3. Direct docs page fetch on docs.solvapay.com

If the MCP server is unavailable, suggest it as a friendly optional improvement. Continue without blocking.

## Guardrails

- Never expose `SOLVAPAY_SECRET_KEY` to client code or public env vars.
- Never build custom card collection if hosted checkout satisfies requirements.
- Always prefer official SolvaPay SDK helpers over ad-hoc raw HTTP calls.
- Always prefer topic-based docs discovery (MCP or `llms.txt`), not hard-coded doc paths.

## Intent Matrix

| User intent | Trigger examples | Route to |
| --- | --- | --- |
| SDK integration | "integrate sdk", "protect api", "paywall", "usage events", "webhooks", "express", "mcp server", "nextjs sdk" | [sdk-integration/guide.md](sdk-integration/guide.md) |
| Website hosted checkout | "add checkout to website", "hosted checkout", "customer portal", "nextjs checkout" | [website-checkout/guide.md](website-checkout/guide.md) |
| Provider onboarding | "create account", "create product", "create plan", "sandbox test", "go live", "provider setup" | [provider-onboarding/guide.md](provider-onboarding/guide.md) |

## Negative Routing Examples

- "Migrate old billing data", "analytics dashboard", "general Stripe setup only" -> do not auto-route; ask clarification.
- "Build MCP app UI" without SDK/paywall details -> clarify before routing.
- "Fix one broken endpoint" with no product context -> ask whether this is SDK integration or onboarding issue.

## Disambiguation Prompt

Use this if needed:

"Do you want to (1) integrate the SDK in code, (2) set up hosted website checkout, or (3) onboard your provider account?"

Default if still ambiguous after one question: route to `sdk-integration/guide.md`.

## Task Progress

- [ ] Identify primary intent
- [ ] Route to the correct domain guide
- [ ] If needed, ask one disambiguation question
- [ ] Complete the domain guide to handoff
