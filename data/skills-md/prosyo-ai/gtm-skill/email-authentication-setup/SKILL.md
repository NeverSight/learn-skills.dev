---
name: email-authentication-setup
description: "Use this skill when you need to set up or fix SPF, DKIM and DMARC for a sending domain: \"set up SPF DKIM DMARC\", \"my DMARC is failing\", \"write my SPF record\", \"meet bulk sender requirements\". Inventories every service that sends as the domain, writes the exact DNS records, explains alignment, plans a safe DMARC rollout from monitoring to enforcement, and gives the checks that confirm everything passes."
license: MIT
metadata:
  title: SPF, DKIM and DMARC setup
  category: deliverability
  tags: "RevOps, Founders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "spf dkim dmarc setup, how to set up dmarc, spf record generator, claude email authentication skill, bulk sender requirements"
  inputs: "Domain, Services that send email as the domain, Current DNS records"
  outputs: "Sender inventory, Exact DNS records, DMARC rollout plan, Verification checklist"
---

Use this when a domain sends email and authentication is missing, broken or failing alignment. Without all three records passing, major mailbox providers junk or reject bulk and cold mail.

## Inputs

- The domain.
- Every service that sends email as that domain: mailbox provider, marketing platform, CRM, support desk, billing, product notifications.
- Current DNS records, if any.

## The play

### 1. Inventory senders
List every service and how it sends: does it send "as" your domain, and does it support custom DKIM? Missing a sender here is how a DMARC rollout ends up blocking invoices.

### 2. SPF
One TXT record on the domain listing every service, ending in `~all` (soft fail) or `-all` (hard fail).

```
v=spf1 include:<mail provider> include:<marketing service> ~all
```

Rules: exactly one SPF record per domain; 10 DNS lookups or fewer (each `include` counts, and nested includes count too). Over 10 lookups causes a permanent error and SPF fails for everyone. Use subdomains for high-volume services to stay under the limit.

### 3. DKIM
Turn on signing in each service and publish the key it gives you (usually a CNAME or TXT at `<selector>._domainkey.<domain>`). Then confirm signing is actually enabled; a published key with signing off is a common silent failure.

### 4. DMARC
Start in monitoring mode and tighten over weeks:

| Stage | Record | When to move on |
| --- | --- | --- |
| Monitor | `v=DMARC1; p=none; rua=mailto:<reports address you own>` | 2-4 weeks of reports show all legitimate senders passing |
| Quarantine | `p=quarantine; pct=25` then 50, 100 | No legitimate mail failing |
| Reject | `p=reject` | Optional, for maximum protection |

Read [references/dns-records.md](references/dns-records.md) for record examples, alignment explained and how to read aggregate reports.

### 5. Verify
Send test emails to a mailbox you control and check the headers: `spf=pass`, `dkim=pass`, `dmarc=pass`, with the From domain aligned.

## What good looks like

- Every legitimate sender passes DMARC before the policy moves past `p=none`.
- SPF stays under 10 lookups with room to add a service.
- DMARC reports go to an address the user owns and someone actually reads them.
- The common mistake is publishing `p=reject` on day one and silently blocking the billing system's emails.

## Rules

- MUST inventory all senders before changing SPF or DMARC.
- MUST start DMARC at `p=none`.
- MUST send DMARC reports only to addresses or services the user controls.
- NEVER publish a second SPF record; merge into one.
- NEVER change DNS without the user's explicit approval.

## Example prompts

- "Write SPF, DKIM and DMARC for acme.com. We send from our mailbox provider, a marketing platform and a support desk."
- "Our DMARC report shows failures from an IP we don't recognise. What is it?"
- "We're over the SPF lookup limit. Fix it."
