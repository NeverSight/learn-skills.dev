---
name: spaceship-domains
description: Manages domains via the Spaceship registrar API — registers domains, configures DNS records, manages contacts and WHOIS privacy, transfers domains, sets up nameservers, and sells domains on SellerHub. Use when asked to "manage domains", "register a domain", "configure DNS", "add DNS records", "set up nameservers", "check domain availability", "transfer a domain", "sell a domain", "set up email DNS", "manage WHOIS privacy", or any Spaceship domain registrar operation. Requires the Spaceship MCP server to be configured.
---

# Spaceship Domain Management

Manages domains through 48 Spaceship MCP tools across 9 categories: domain lookup, domain info, domain settings, domain lifecycle, DNS management, DNS record creation, contacts & privacy, personal nameservers, and SellerHub marketplace.

## When to Use

- Managing domains registered at Spaceship (DNS, settings, contacts, privacy)
- Registering, renewing, transferring, or restoring domains via Spaceship
- Configuring DNS records for domains using Spaceship nameservers
- Setting up email (Google Workspace, Microsoft 365) on Spaceship-managed domains
- Listing domains for sale on Spaceship SellerHub
- Checking domain availability and pricing through Spaceship
- Setting up vanity/glue nameservers for Spaceship domains

## When NOT to Use

- Domains managed at other registrars (Cloudflare, GoDaddy, Namecheap, etc.)
- DNS hosted outside Spaceship (e.g. Cloudflare DNS, Route 53, Google Cloud DNS)
- General DNS troubleshooting unrelated to Spaceship
- Web hosting or server configuration
- SSL certificate management (use CAA records for authorization only)
- Email server setup beyond DNS records

## Tool Loading

All Spaceship tools are deferred. Load them before use:

```
ToolSearch: "+spaceship <keyword>"
```

Examples: `+spaceship dns`, `+spaceship domain`, `+spaceship contact`, `+spaceship sellerhub`.

## Tool Categories

| Category | Tools | Key Operations |
|----------|-------|----------------|
| Domain Lookup | `check_domain_availability` | Check availability + pricing for 1–20 domains |
| Domain Info | `list_domains`, `get_domain` | List/inspect domains in account |
| Domain Settings | `set_auto_renew`, `set_transfer_lock`, `update_nameservers`, `get_auth_code` | Configure domain settings |
| Domain Lifecycle | `register_domain`, `renew_domain`, `restore_domain`, `transfer_domain`, `get_transfer_status`, `get_async_operation` | Registration, renewal, transfer (all async + financial) |
| DNS Management | `list_dns_records`, `save_dns_records`, `delete_dns_records`, `check_dns_alignment` | Bulk DNS operations |
| DNS Creators | `create_a_record`, `create_aaaa_record`, `create_cname_record`, `create_mx_record`, `create_txt_record`, `create_srv_record`, `create_ns_record`, `create_alias_record`, `create_caa_record`, `create_https_record`, `create_ptr_record`, `create_svcb_record`, `create_tlsa_record` | Create individual DNS records by type |
| Contacts & Privacy | `save_contact`, `get_contact`, `save_contact_attributes`, `get_contact_attributes`, `update_domain_contacts`, `set_privacy_level`, `set_email_protection` | Contact profiles, WHOIS privacy |
| Personal NS | `list_personal_nameservers`, `get_personal_nameserver`, `update_personal_nameserver`, `delete_personal_nameserver` | Vanity nameservers (glue records) |
| SellerHub | `list_sellerhub_domains`, `create_sellerhub_domain`, `get_sellerhub_domain`, `update_sellerhub_domain`, `delete_sellerhub_domain`, `create_checkout_link`, `get_verification_records` | Domain marketplace |

## References

- [API Reference](references/api-reference.md) — complete parameter specs for all 48 tools
- [Gotchas](references/gotchas.md) — common pitfalls, edge cases, and correct usage patterns
- [Patterns](references/patterns.md) — DNS recipes for Google Workspace, Microsoft 365, Vercel, Netlify, and more

## Common Workflows

### Check & Register a Domain

```
1. check_domain_availability({ domains: ["example.com"] })
   → Returns availability + pricing
2. save_contact({ firstName, lastName, email, address1, city, country, phone })
   → Returns { contactId }
3. register_domain({ domain: "example.com", contacts: { registrant: contactId } })
   → Returns { operationId } (async, financial — confirm with user first)
4. get_async_operation({ operationId })
   → Poll until status is "completed"
5. set_privacy_level({ domain, level: "high", userConsent: true })
6. set_transfer_lock({ domain, locked: true })
```

### Configure DNS for a Website

```
1. list_dns_records({ domain: "example.com" })
   → See existing records
2. create_a_record({ domain, name: "@", address: "93.184.216.34" })
3. create_cname_record({ domain, name: "www", cname: "example.com" })
4. check_dns_alignment({ domain, expectedRecords: [...] })
   → Verify all records are correct
```

For email, CDN, and hosting provider DNS patterns, see [references/patterns.md](references/patterns.md).

### Transfer a Domain to Spaceship

```
1. save_contact({ ... })
   → Create contact profile first
2. transfer_domain({ domain, authCode: "EPP-CODE", contacts: { registrant: contactId } })
   → Returns { operationId } (async, financial — confirm with user first)
3. get_transfer_status({ domain })
   → Check transfer progress
4. get_async_operation({ operationId })
   → Poll until complete
```

### Sell a Domain on SellerHub

```
1. create_sellerhub_domain({ domain, binPrice: { amount: "5000", currency: "USD" }, binPriceEnabled: true })
2. get_verification_records()
   → Get DNS verification records (account-level)
3. create_txt_record({ domain, name, value })
   → Add the verification TXT record
4. create_checkout_link({ domain, type: "buyNow" })
   → Returns shareable purchase URL
```

## Key Gotchas

- **Async + financial**: `register_domain`, `renew_domain`, `restore_domain`, `transfer_domain` return `{ operationId }` — always confirm with user before executing, then poll with `get_async_operation`
- **DNS creators replace**: Each `create_*_record` replaces ALL existing records with the same name+type
- **Privacy requires consent**: `set_privacy_level` needs `{ userConsent: true }` — mandatory
- **Rate limits**: 5 requests per 300 seconds per domain for write endpoints

For the full list with examples, see [references/gotchas.md](references/gotchas.md).

## Instructions

1. **Identify the action** from the user's request
2. **Load required tools** via `ToolSearch` with `+spaceship <keyword>`
3. **Confirm destructive/financial operations** before executing (register, renew, restore, transfer, delete DNS)
4. **Follow the appropriate workflow** above, or check [references/patterns.md](references/patterns.md) for service-specific DNS recipes
5. **Poll async operations** for lifecycle operations
6. **Report results** clearly — show domain status, DNS records, pricing, or operation results in readable format

If `$ARGUMENTS` is provided, interpret it as the domain name or action to perform.
