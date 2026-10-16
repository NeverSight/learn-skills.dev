---
name: helipod-domains
description: Search, price, register, transfer and renew domains on Helipod (including .id), manage DNS records and nameservers, and point a domain at a Helipod app or VPS. Use when the user wants to buy a domain or change DNS.
---

# Helipod domains

Follow the `helipod` skill rules. Domains belong to the account: the key must be a **whole-account** key with the Domain API (`403 ACCOUNT_KEY_REQUIRED` otherwise).

## Buy a domain

1. `search_domain` for the name the user wants (suggest alternatives or other extensions if taken).
2. `domain_prices` for the extension: registration price (IDR, VAT included) and `whois_protection` per year.
3. `check_registrant`: owner details must be complete once (done in the dashboard). If incomplete, send the user to the dashboard Domains page.
4. Tell the user the total and get a clear yes, then `register_domain` (1 year; `whoisProtection: true` if they want privacy).
5. Premium names are not sold online (`PREMIUM_NOT_SUPPORTED`).

Transfer in: `transfer_domain` with the auth code from the old registrar (1 year added, priced like a transfer). Renew: `renew_domain`.

## DNS

- `list_dns_records` first. `set_dns_records` **replaces all records**: always send the full list including records to keep.
- Point at a Helipod app: add the domain to the service (`add_service_domain`, `kind: "custom"`), then a record from its `dns` field: subdomain `CNAME www → cname.helipod.app`, root domain `A @ → <IP given in dns.value>`.
- Point at a VPS: `A` record to the server's `publicIp`.
- Email: add the records shown by `add_email_domain` / `list_email_domains` exactly as given.
- External DNS provider: `set_nameservers` (then records here stop applying).

Records usually take effect within minutes; certificates for custom domains are issued automatically once DNS points at Helipod.
