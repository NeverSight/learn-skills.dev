---
name: attack-surface-recon
description: Map an organization's external attack surface — domains, subdomains, exposed services, leaked credentials, and brand abuse. Use at the start of assessments or for continuous monitoring.
---

# Attack Surface Recon

Build a complete external attack-surface picture from public sources.

## 1. Root Domain Discovery

- Start from known brands/domains; expand via certificate transparency (crt.sh), ASN lookups, WHOIS reverse lookups, acquisition history
- Identify cloud ranges: enumerate owned netblocks (bgp.he.net, ipinfo)

## 2. Subdomain Enumeration

- Passive sources: CT logs, DNS datasets (SecurityTrails-style), web archives
- Active: DNS bruteforce, permutation generation (alterations of known hosts: `-dev`, `-staging`, `-old`)
- Resolve; probe HTTP(S) for live services; fingerprint technologies (httpx/wappalyzer)

## 3. Exposed Services

- Port scan in-scope IPs (top ports minimum, full range on high-value hosts)
- Flag: exposed admin panels, databases (3306/5432/27017), RDP/SMB, Redis/Memcached, Kubernetes API, VPN portals, file shares
- Takeover checks: dangling CNAMEs pointing at deprecated cloud services

## 4. Credential and Code Leaks

- Breach data for corporate domains (report presence; never view more than proof)
- Public code search (GitHub/gists) for org domains, tokens, internal hostnames in commits
- Exposed storage: open S3 buckets/azure blobs matching org naming patterns

## 5. People and Brand

- Employee enumeration via LinkedIn for phishing-simulation scoping (policy permitting)
- Lookalike domains registered recently (typosquats), abuse of brand in app stores

## Rules

- Passive sources preferred; active scanning only within authorization
- Found leaked credentials: report immediately, do not log in with them

## Output

Ranked asset inventory: exposed services by risk, credential leak notifications, takeover-prone records, and monitoring recommendations.
