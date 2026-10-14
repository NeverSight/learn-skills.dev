---
name: domains
description: Hostinger Domains API for domain portfolio management, availability checks, forwarding, WHOIS profiles, nameservers, domain lock, privacy protection, and domain access verifications. Use when registering domains, checking availability, managing DNS delegation, configuring redirects, handling WHOIS contact information, or checking domain verification status.
last_updated: "2026-06-12"
doc_source: https://developers.hostinger.com
---

# Hostinger Domains

The Domains API provides full domain lifecycle management — from checking availability and purchasing to configuring nameservers, forwarding, WHOIS profiles, domain locks, and privacy protection.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Common Patterns](#common-patterns)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Core Concepts

### Domain Portfolio

Your domain portfolio contains all domains registered under your Hostinger account. Each domain has configuration for nameservers, WHOIS contacts, lock status, and privacy protection.

### Domain Availability

Before purchasing, check if a domain name is available across one or more TLDs. The API also supports alternative domain suggestions.

### Domain Forwarding

Redirect a domain to another URL using 301 (permanent) or 302 (temporary) redirects.

### WHOIS Profiles

Contact information associated with domain registrations. Each TLD may require specific WHOIS details. Profiles can be reused across multiple domains.

### Domain Lock

Prevents unauthorized domain transfers. Must be disabled before transferring a domain to another registrar.

### Privacy Protection

Hides the domain owner's personal information from public WHOIS databases.

### Domain Access Verification

Some operations require proof that you control a domain. The Domain Access Verifier returns the pending and completed verifications for a set of domains, so you can check verification status before relying on a domain.

> **Note:** This endpoint lives under a different base path — `/api/v2/direct/verifications/active` — not `/api/domains/v1/`.

## Common Patterns

### Check Domain Availability

```bash
curl -X POST "https://developers.hostinger.com/api/domains/v1/availability" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "myawesomesite",
    "tlds": ["com", "net", "org"],
    "with_alternatives": true
  }'
```

**Python SDK:**

```python
from hostinger_api import Hostinger

client = Hostinger(api_token="YOUR_API_TOKEN")
result = client.domains.availability.check(
    domain="myawesomesite",
    tlds=["com", "net", "org"],
    with_alternatives=True
)
```

**TypeScript SDK:**

```typescript
import { Hostinger } from "hostinger-api-sdk";

const client = new Hostinger({ apiToken: "YOUR_API_TOKEN" });

const result = await client.domains.availability.check({
  domain: "myawesomesite",
  tlds: ["com", "net", "org"],
  withAlternatives: true,
});
```

**PHP SDK:**

```php
use Hostinger\Api\HostingerApi;

$client = new HostingerApi('YOUR_API_TOKEN');

$result = $client->domains->availability->check([
    'domain' => 'myawesomesite',
    'tlds' => ['com', 'net', 'org'],
    'with_alternatives' => true,
]);
```

> **Note:** Rate limited to 10 requests per minute. TLDs should be without leading dot (e.g., `com` not `.com`). For alternatives, provide only one TLD.

### Purchase a Domain

```bash
curl -X POST "https://developers.hostinger.com/api/domains/v1/portfolio" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "my-new-domain.com",
    "item_id": "hostingercom-domain-com-usd-1y",
    "payment_method_id": 1327362,
    "domain_contacts": {
      "owner_id": 741288,
      "admin_id": 741288,
      "billing_id": 741288,
      "tech_id": 741288
    }
  }'
```

> Get `item_id` from the billing catalog. If no payment method is provided, your default is used. If no WHOIS info is provided, default contact information for that TLD is used.

### List and View Domains

```bash
# List all domains
curl -X GET "https://developers.hostinger.com/api/domains/v1/portfolio" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Get domain details
curl -X GET "https://developers.hostinger.com/api/domains/v1/portfolio/example.com" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"
```

### Configure Nameservers

```bash
curl -X PUT "https://developers.hostinger.com/api/domains/v1/portfolio/example.com/nameservers" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ns1": "ns1.custom-dns.com",
    "ns2": "ns2.custom-dns.com"
  }'
```

### Domain Forwarding

```bash
# Create forwarding (301 permanent redirect)
curl -X POST "https://developers.hostinger.com/api/domains/v1/forwarding" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "old-domain.com",
    "redirect_type": "301",
    "redirect_url": "https://new-domain.com"
  }'

# Get forwarding config
curl -X GET "https://developers.hostinger.com/api/domains/v1/forwarding/old-domain.com" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Delete forwarding
curl -X DELETE "https://developers.hostinger.com/api/domains/v1/forwarding/old-domain.com" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"
```

### Domain Lock & Privacy Protection

```bash
# Enable domain lock (prevent transfers)
curl -X PUT "https://developers.hostinger.com/api/domains/v1/portfolio/example.com/domain-lock" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Disable domain lock (before transfer)
curl -X DELETE "https://developers.hostinger.com/api/domains/v1/portfolio/example.com/domain-lock" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Enable privacy protection
curl -X PUT "https://developers.hostinger.com/api/domains/v1/portfolio/example.com/privacy-protection" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Disable privacy protection
curl -X DELETE "https://developers.hostinger.com/api/domains/v1/portfolio/example.com/privacy-protection" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"
```

### WHOIS Profile Management

```bash
# List WHOIS profiles (optionally filter by TLD)
curl -X GET "https://developers.hostinger.com/api/domains/v1/whois?tld=com" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Create a WHOIS profile
curl -X POST "https://developers.hostinger.com/api/domains/v1/whois" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tld": "com",
    "entity_type": "individual",
    "country": "US",
    "whois_details": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "+1.5551234567",
      "address": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001"
    }
  }'

# Check which domains use a WHOIS profile
curl -X GET "https://developers.hostinger.com/api/domains/v1/whois/741288/usage" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"

# Delete a WHOIS profile
curl -X DELETE "https://developers.hostinger.com/api/domains/v1/whois/741288" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN"
```

### Check Domain Verifications

```bash
# Get pending and completed verifications for one or more domains
curl -X GET "https://developers.hostinger.com/api/v2/direct/verifications/active" \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "domains": ["example.com", "example.net"] }'
```

## API Reference

### Availability

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/domains/v1/availability` | Check domain availability (rate limit: 10/min) |

### Portfolio

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/domains/v1/portfolio` | List all domains |
| `POST` | `/api/domains/v1/portfolio` | Purchase a new domain |
| `GET` | `/api/domains/v1/portfolio/{domain}` | Get domain details |
| `PUT` | `/api/domains/v1/portfolio/{domain}/nameservers` | Update nameservers |
| `PUT` | `/api/domains/v1/portfolio/{domain}/domain-lock` | Enable domain lock |
| `DELETE` | `/api/domains/v1/portfolio/{domain}/domain-lock` | Disable domain lock |
| `PUT` | `/api/domains/v1/portfolio/{domain}/privacy-protection` | Enable privacy protection |
| `DELETE` | `/api/domains/v1/portfolio/{domain}/privacy-protection` | Disable privacy protection |

### Forwarding

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/domains/v1/forwarding` | Create domain forwarding |
| `GET` | `/api/domains/v1/forwarding/{domain}` | Get forwarding config |
| `DELETE` | `/api/domains/v1/forwarding/{domain}` | Delete forwarding |

### WHOIS

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/domains/v1/whois` | List WHOIS profiles |
| `POST` | `/api/domains/v1/whois` | Create WHOIS profile |
| `GET` | `/api/domains/v1/whois/{whoisId}` | Get WHOIS profile |
| `DELETE` | `/api/domains/v1/whois/{whoisId}` | Delete WHOIS profile |
| `GET` | `/api/domains/v1/whois/{whoisId}/usage` | Get profile usage |

### Verifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v2/direct/verifications/active` | Get pending and completed domain verifications (body: `domains` string array) |

## Best Practices

### Registration
- Always check availability before attempting to purchase
- Ensure WHOIS profile exists for the target TLD before registering
- Some TLDs require `additional_details` — check requirements per TLD
- Keep domain lock enabled to prevent unauthorized transfers

### Security
- Enable **privacy protection** to hide personal information from public WHOIS
- Enable **domain lock** on all production domains
- Only disable domain lock immediately before an intended transfer

### Nameservers
- Improper nameserver configuration makes the domain unresolvable
- Always have at least 2 nameservers configured
- Verify nameservers are responding before switching

### Forwarding
- Use `301` (permanent) for SEO-preserving redirects
- Use `302` (temporary) for short-term redirects
- Remove forwarding before pointing the domain to hosting

## Troubleshooting

### Domain Not Resolving After Nameserver Change
- Nameserver changes can take up to 48 hours to propagate
- Verify new nameservers are configured correctly: `dig NS example.com`
- Check that DNS records exist on the new nameserver

### Domain Purchase Failed
- Check registration status in [hPanel](https://hpanel.hostinger.com/)
- Verify WHOIS profile is complete for the target TLD
- Ensure payment method has sufficient funds

### Domain Lock Cannot Be Disabled
- Some TLDs have registrar-imposed lock periods after registration
- Contact support if the lock state doesn't change

### WHOIS Profile Deletion Fails
- Profile may be in use by active domains
- Check usage with the `/whois/{whoisId}/usage` endpoint first

## See Also

The following deep-dive guide is available in this skill directory:

- `transfer-guide.md` — Domain purchase workflow, nameserver configuration, transfer procedures, WHOIS management, and bulk operations (TypeScript/PHP examples)

## References

- [Hostinger API Documentation](https://developers.hostinger.com)
- [Hostinger API Changelog](https://github.com/hostinger/api/blob/main/CHANGELOG.md)
- [Python SDK](https://github.com/hostinger/api-python-sdk)
- [TypeScript SDK](https://github.com/hostinger/api-typescript-sdk)
- [PHP SDK](https://github.com/hostinger/api-php-sdk)
- [CLI Tool](https://github.com/hostinger/api-cli)
