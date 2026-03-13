---
name: stripe-connect
license: MIT
metadata: metadata.json
description: "Implement Stripe Connect for marketplace and platform payments: connected accounts, onboarding, charge flows, payouts, and platform fees. Use when: (1) Building a marketplace with sellers/service providers, (2) Creating a platform that routes payments to third parties, (3) Onboarding connected accounts (Standard, Express, Custom), (4) Implementing direct charges, destination charges, or separate charges and transfers, (5) Managing platform fees and payout schedules, (6) Building OAuth flows for account connection. Triggers on: marketplace, platform, connected account, stripe connect, onboarding, destination charge, direct charge, transfer, platform fee, express account, standard account, custom account."
---

# Stripe Connect

Build marketplace and platform payment flows with connected accounts, flexible charge routing, and automated payouts.

## Priority Rules

| Rule | Impact | File |
|------|--------|------|
| Default to Express accounts | High | `rules/account-choose-express-default.md` |
| Account type is permanent | High | `rules/account-never-change-type.md` |
| Request card_payments + transfers together | High | `rules/account-request-both-capabilities.md` |
| Prefer destination charges | High | `rules/charge-use-destination.md` |
| Use on_behalf_of for statement descriptors | High | `rules/charge-include-on-behalf-of.md` |
| Require on_behalf_of for cross-region | High | `rules/charge-cross-region-on-behalf-of.md` |
| Use source_transaction for SCT | High | `rules/charge-sct-use-source-transaction.md` |
| Reverse transfers on refund | High | `rules/charge-reverse-transfer-on-refund.md` |
| Verify charges_enabled before processing | High | `rules/onboard-check-capabilities.md` |
| Implement refresh_url handler | High | `rules/onboard-handle-refresh.md` |
| Use webhooks to confirm onboarding | High | `rules/onboard-use-connect-webhooks.md` |
| No hosted onboarding in WebViews | High | `rules/onboard-no-webview.md` |
| Validate fee < charge amount | High | `rules/fee-never-exceed-charge.md` |
| Never combine both fee methods | High | `rules/fee-not-both-methods.md` |
| Check payouts_enabled before payouts | High | `rules/payout-verify-enabled.md` |
| Handle payout failures | High | `rules/payout-handle-failures.md` |
| Monitor account.updated events | High | `rules/webhook-listen-account-updated.md` |
| Set up Connect webhook endpoint | High | `rules/webhook-setup-connect-endpoint.md` |
| Handle deauthorization events | High | `rules/webhook-handle-deauthorization.md` |
| Prefer application_fee_amount | Medium | `rules/fee-use-application-fee.md` |
| Refund fees on full refunds | Medium | `rules/fee-refund-with-charge.md` |
| Prefill known info at creation | Medium | `rules/onboard-prefill-known-info.md` |
| Verify instant payout eligibility | Medium | `rules/payout-check-instant-eligibility.md` |
| Use controller properties for new integrations | Medium | `rules/account-use-controller-properties.md` |

## Quick Reference

### Account Type Decision Tree

```
How much onboarding control do you need?
|
+-- Sellers manage their own Stripe dashboard?
|   -> Standard accounts (least platform liability)
|
+-- Platform-branded onboarding, Stripe-hosted dashboard?
|   -> Express accounts (balanced control)
|
+-- Full white-label, platform owns entire UX?
    -> Custom accounts (most control, most responsibility)
```

| Feature | Standard | Express | Custom |
|---------|----------|---------|--------|
| Onboarding | Stripe-hosted | Stripe-hosted (branded) | Platform builds |
| Dashboard | Full Stripe | Express dashboard | None (platform builds) |
| Branding | Stripe | Platform + Stripe | Platform only |
| Liability | Account holder | Shared | Platform |
| Effort | Low | Medium | High |

### Charge Flow Decision Tree

```
Who should the customer see on their statement?
|
+-- The connected account (seller)?
|   -> Direct charges
|      Customer -> Connected Account (platform takes fee)
|
+-- The platform?
|   -> Destination charges
|      Customer -> Platform -> Connected Account
|
+-- Complex splits / delayed routing?
    -> Separate Charges and Transfers
       Customer -> Platform -> Multiple Connected Accounts
```

### Quick Start: Express + Destination Charges

```typescript
// 1. Create Connected Account
const account = await stripe.accounts.create({
  type: 'express',
  country: 'US',
  email: 'seller@example.com',
  capabilities: {
    card_payments: { requested: true },
    transfers: { requested: true },
  },
});

// 2. Generate Onboarding Link
const accountLink = await stripe.accountLinks.create({
  account: account.id,
  refresh_url: 'https://example.com/reauth',
  return_url: 'https://example.com/return',
  type: 'account_onboarding',
});

// 3. Create Payment with Platform Fee
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000,
  currency: 'usd',
  application_fee_amount: 1500,
  transfer_data: {
    destination: 'acct_connected_xxx',
  },
});
```

### Critical Webhooks

| Event | Action |
|-------|--------|
| `account.updated` | Check `charges_enabled`, `payouts_enabled` |
| `account.application.deauthorized` | Handle disconnection |
| `payment_intent.succeeded` | Confirm transfer completed |
| `transfer.created` | Track money movement |
| `payout.paid` / `payout.failed` | Monitor seller payouts |

## Reference Docs

| Reference | Description |
|-----------|-------------|
| `references/account-types.md` | Standard vs Express vs Custom: creation, capabilities, dashboard, liability, migration |
| `references/charge-flows.md` | Direct, destination, SCT: code examples, fund flows, refunds, disputes |
| `references/onboarding.md` | Account Links, embedded onboarding, refresh/return URLs, verification |
| `references/platform-fees.md` | Application fees, transfer amounts, fee calculation, pricing models |
| `references/payouts.md` | Schedules, instant payouts, manual payouts, cross-border, failures |
| `references/oauth.md` | OAuth flow for Standard accounts: authorization, token exchange, deauthorization |
| `references/compliance.md` | KYC requirements, 1099 reporting, identity verification, cross-border |

## How to Use

1. **Choosing an account type**: Start with `rules/account-choose-express-default.md`, then consult `references/account-types.md` for full comparison
2. **Implementing a charge flow**: Start with `rules/charge-use-destination.md`, then consult `references/charge-flows.md` for code examples
3. **Building onboarding**: Check rules prefixed with `onboard-`, then consult `references/onboarding.md` for full flow
4. **Setting up fees**: Check rules prefixed with `fee-`, then consult `references/platform-fees.md` for calculation patterns
5. **Configuring payouts**: Check rules prefixed with `payout-`, then consult `references/payouts.md` for schedules and instant payouts
6. **Webhook integration**: Check rules prefixed with `webhook-`, and set up Connect-specific webhook endpoint
7. **OAuth for Standard accounts**: Consult `references/oauth.md` for full authorization flow
8. **Compliance**: Consult `references/compliance.md` for KYC, tax reporting, and cross-border requirements
