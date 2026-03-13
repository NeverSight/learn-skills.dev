---
name: paystack-apple-pay
description: >-
  Paystack Apple Pay API — register and manage domains for Apple Pay integration.
  Register top-level domains or subdomains, list registered domains, and unregister
  domains. Use this skill whenever enabling Apple Pay on your website, registering
  domains for Apple Pay checkout, managing Apple Pay domain whitelisting, or
  troubleshooting Apple Pay domain verification issues. Also use when you see
  references to /apple-pay/domain endpoint or Apple Pay registration.
---

# Paystack Apple Pay

The Apple Pay API lets you register your domains for Apple Pay integration.

> Depends on: **paystack-setup** for the `paystackRequest` helper.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/apple-pay/domain` | Register a domain |
| GET | `/apple-pay/domain` | List registered domains |
| DELETE | `/apple-pay/domain` | Unregister a domain |

> **Note**: Only one domain or subdomain can be registered per request.

## Register Domain

```typescript
await paystackRequest("/apple-pay/domain", {
  method: "POST",
  body: JSON.stringify({ domainName: "example.com" }),
});
// { status: true, message: "Domain successfully registered on Apple Pay" }

// Register a subdomain too
await paystackRequest("/apple-pay/domain", {
  method: "POST",
  body: JSON.stringify({ domainName: "pay.example.com" }),
});
```

## List Registered Domains

```typescript
const domains = await paystackRequest<{
  domainNames: string[];
}>("/apple-pay/domain");
// domains.data.domainNames → ["example.com", "pay.example.com"]
```

## Unregister Domain

```typescript
await paystackRequest("/apple-pay/domain", {
  method: "DELETE",
  body: JSON.stringify({ domainName: "example.com" }),
});
```
