---
name: recon-security
description: Guide authorized external penetration testing from recon through validation and scoped exploitation using free and open-source tools. Use for domain/IP attack surface mapping, subdomain discovery, nmap/httpx/nuclei/ffuf workflows, web app testing, SIP/NAS checks, Burp/ZAP validation, PoC documentation, and pentest reporting without commercial APIs.
---

# Recon Security

This skill guides an agent through an **authorized external pentest workflow**: recon, normalization, active discovery, web and infrastructure checks, validation, scoped exploitation (when RoE allows), and reporting. Use only free/open-source tools unless the user explicitly opts into commercial services outside this skill.

Do not assume permission. Gate every active, invasive, or state-changing step on Pass 0. This skill is model-guided only: propose commands and workflows; the user or agent runs them when scope and mode allow. No bundled scripts ship with this skill.

## Engagement lifecycle

```text
Pass 0 Scope/RoE → Pass 1 Passive → Pass 2 Normalize → Pass 3 Active
    → Pass 4 Web + infra → Pass 5 Triage → Pass 6 Validation
    → Pass 7 Scoped exploitation (if approved) → Pass 8 Report
```

## Mental model

- **Recon** maps what is exposed.
- **Validation** proves what matters with minimal reproducible evidence.
- **Exploitation** demonstrates impact only within written RoE — not unrestricted attack.

Prefer conservative, reproducible checks. One confirmed finding beats dozens of scanner lines.

## Pass 0: scope and authorization

Establish before any active work:

- In-scope domains, subdomains, IPs, ASNs, apps, and environments (prod vs staging).
- Out-of-scope assets and forbidden techniques (brute force, DoS, data dump, lateral movement).
- Written authorization or explicit ownership.
- Scan intensity: passive only, light active, standard, or deep.
- Whether exploitation and credential testing are allowed.
- Evidence directory (`PROJECT_DIR`, default `~/Projects/pentest-engagement`). See `references/environment-setup.md`.
- Deliverable: command plan only, executed tests, or full report.

If authorization is unclear, stop at passive planning and ask.

## Pass 1: passive recon

Build inventory from public sources only:

- DNS, WHOIS/RDAP, RIPEstat/BGPView, certificate transparency (`crt.sh`, `subfinder`, `amass -passive`, `assetfinder`).
- Historical URLs (`gau`, `waybackurls`, Common Crawl, public `urlscan.io`).
- Search dorks and public code references (no secret copying).

Use example commands from `references/environment-setup.md` and `references/tools.md` when the user wants executable steps.

## Pass 2: normalize targets

Produce working lists under `targets/`:

- `domains.txt`, `in_scope_domains.txt`, `resolved_hosts.txt`, `web_targets.txt`, `ips.txt`
- `needs-scope-confirmation.txt` for uncertain assets

Deduplicate; drop unrelated CT names and out-of-scope SaaS unless approved.

## Pass 3: active recon

Requires Pass 0 approval. Rate-limit all probes.

- `dnsx`, `httpx`, `nmap` (top ports first), optional `naabu` / rate-limited `masscan`
- `wafw00f`, `testssl.sh` or `sslyze`, `nuclei` (open templates; triage as leads)

Propose rate-limited active commands; save raw output under `evidence/active/`.

## Pass 4: web app and infrastructure checks

### Web applications

- Fingerprint headers, cookies, security headers, technologies.
- Misconfigurations: `.git`, `.env`, backups, `phpinfo`, directory listing, `robots.txt`.
- Content/parameter discovery: `ffuf`, `feroxbuster`, `arjun`, `katana`, `hakrawler`.
- Light automated probes; `sqlmap` detection-only by default; `dalfox` for reflected XSS leads.
- Manual proxy review: OWASP ZAP or Burp Suite Community.

Walk through fingerprinting, misconfiguration checks, and light probes for each priority URL.

### Infrastructure (when in scope)

Telecom, storage, and file services often appear on external pentests:

- **SIP/VoIP**: UDP/TCP 5060/5061, `nmap --script=sip-methods`, OPTIONS probes. No call setup unless authorized.
- **NAS/file exposure**: ports 445, 139, 548, 873, 2049, 5000/5001, 8080; `smbclient -N -L`, `showmount -e`. Document share permissions, not customer file contents.

Save SIP/NAS results under `evidence/infra/`.

## Pass 5: triage and evidence

Classify every item:

| Class | Meaning |
|-------|---------|
| Confirmed finding | Reproduced with clear evidence and impact |
| Likely finding | Strong signal; needs Pass 6 |
| Lead | Interesting; not yet tested |
| False positive / OOS | Drop from report |

Build a prioritized queue for validation. Store under `evidence/triage/`. Never paste secrets or bulk PII into reports.

## Pass 6: validation

Turn leads into confirmed findings. Read `references/validation.md`.

- Import `web_targets.txt` into Burp or ZAP; map auth and roles.
- Manually confirm nuclei/ffuf/sqlmap signals.
- Two-account testing for IDOR/BOLA; pair with `authz-security` when code is available.
- Infrastructure: focused port/service re-checks; SIP/NAS proof without data theft.

PoC bar: numbered steps, request/response or screenshot, impact, fix.

## Pass 7: scoped exploitation

Only when Pass 0 explicitly allows exploitation. Read `references/exploitation-roe.md`.

- Minimum proof of impact (one row, one harmless upload, one auth bypass with test accounts).
- No `--dump`, persistence, lateral movement, or destructive actions unless contract permits.
- Remove test artifacts when cleanup is required.
- Stop and escalate if scope, production risk, or legal boundaries are unclear.

## Pass 8: reporting

Use `references/report-template.md`. Include:

- Executive summary and scope
- Methodology by phase (passive, active, validation, exploitation if run)
- Findings by severity with reproduction and remediation
- Leads and limitations
- Remediation roadmap (immediate / short / long term)

## Severity scale

- **P0**: Sensitive data exposure, unauthenticated admin/control, confirmed critical exploit path.
- **P1**: High-impact issue with limited preconditions; confirmed injection or authz break without mass extraction.
- **P2**: Medium exposure or hardening gap without confirmed exploit chain.
- **P3**: Informational, hygiene, or scan limitations.

## Output format

```
[P1] exposed-admin-panel on https://admin.example.com
  Evidence: httpx + manual browser review; headers in evidence/webapp/.
  Impact: Public admin surface increases credential and exploit risk.
  Fix: Restrict by VPN/IdP, enforce MFA, monitor access.
```

## Reference files

- `references/tools.md` — approved tools and commercial exclusions
- `references/checklist.md` — full engagement checklist
- `references/environment-setup.md` — macOS setup and directory layout
- `references/validation.md` — manual validation and PoC bar
- `references/exploitation-roe.md` — allowed/prohibited exploitation boundaries
- `references/report-template.md` — final deliverable structure

## What this skill won't do

- Require Shodan, Censys, DeHashed, IntelX, or Burp Pro.
- Treat scanner output as confirmed without Pass 6.
- Run exploitation, dumping, persistence, or lateral movement without explicit RoE approval.
- Bypass authorization or test out-of-scope assets.
