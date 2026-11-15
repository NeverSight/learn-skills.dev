---
name: website-security-audit
description: Comprehensive 5-Phase & 10-Layer defensive website vulnerability scanner, OWASP Top 10 DAST/SAST auditor, security headers checker, and client-side bundle/API inspector for user-owned websites and web applications (inspired by Pentest-Tools Website Scanner & OWASP ZAP).
---

# Website Security Audit & 10-Layer Web Infrastructure Scanner

## Overview
This skill provides a standardized, automated methodology for performing defensive security audits, OWASP Top 10 vulnerability assessments, and full-stack architecture inspections on websites and web applications owned by the user. It combines **Pentest-Tools Website Scanner** DAST/SAST workflows (Light Passive Scan vs. Deep Active Scan, Spidering, Technology Fingerprinting, and Authenticated Testing) with our **5-Phase Defensive Audit** and **10-Layer Web Stack Reference**.

---

## 1. Scan Modes & Diagnostic Questions (Pentest-Tools Scanner Methodology)

When auditing a target URL or web repository, support three execution modes (defaulting to **Deep Full-Stack Audit** unless specified):
1. **Light Scan (Passive & Non-Intrusive):**
   - Inspects HTTP response headers, DNS/SSL/TLS posture, server banners, cookie security flags (`HttpOnly`, `Secure`, `SameSite`), technology fingerprinting, and client-side JS bundle secret leaks without sending active fuzzing payloads.
2. **Deep Scan (Active OWASP Top 10 Assessment):**
   - Performs automated crawling/spidering to discover hidden routes, forms, API endpoints, and query parameters.
   - Evaluates **OWASP Top 10** risks: SQL Injection (SQLi), Cross-Site Scripting (Reflected/Stored/DOM XSS), OS Command Injection, Local/Remote File Inclusion (LFI/RFI), SSRF, Broken Access Control (IDOR/BOLA), and Outdated JS Libraries / CVE exposure.
3. **Authenticated Scan (Session / Cookie / Bearer Token):**
   - Audits protected dashboards, multi-tenant isolation (Supabase/Postgres RLS), state-changing POST/PUT/DELETE endpoints, and payment webhooks behind login boundaries.

### Smart Diagnostic Questions (When User Asks "How Should I Audit My Website?")
If the user asks what to check or how to prompt, offer or automatically verify these core questions:
- *Are HTTP security headers (`HSTS`, enforced `CSP`, `X-Frame-Options`, `X-Content-Type-Options`, strict `CORS`) properly blocking XSS and clickjacking?*
- *Are any private keys (`SUPABASE_SERVICE_ROLE_KEY`, `sk_live_*`, database URLs, internal `.env` variables) bundled into client-side Webpack/Vite/Next.js chunks?*
- *If `anon_key` or Firebase config is public, is Row-Level Security (RLS) strictly enforced on every table (`auth.uid() = user_id`)?*
- *Are public `/api/*`, GraphQL, and authentication endpoints protected against brute-force, credential stuffing, and denial-of-wallet attacks via rate limiting?*
- *Do Stripe/Paddle/LemonSqueezy webhook handlers verify cryptographic HMAC signatures before granting user entitlements?*

---

## 2. Automated 5-Phase Defensive Audit Pipeline

### Phase 1: HTTP Security Headers & Transport Security
Inspect response headers using `curl.exe -I -s -L https://<target-domain>/` or REA MCP `inspect_web_page`:
1. **Strict-Transport-Security (HSTS):** Must include `max-age=31536000; includeSubDomains; preload`.
2. **Content-Security-Policy (CSP):**
   - Flag if CSP is only in `Content-Security-Policy-Report-Only` (non-blocking) instead of enforced `Content-Security-Policy`.
   - Flag dangerous directives: `'unsafe-inline'`, `'unsafe-eval'`, or overly broad wildcards (`*`). Recommend cryptographic nonces (`nonce-<base64>`).
3. **Cross-Origin Resource Sharing (CORS):** Flag `Access-Control-Allow-Origin: *` or reflected `Origin` with `Access-Control-Allow-Credentials: true` on authenticated routes.
4. **Clickjacking & MIME Defense:** Verify `X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`) and `X-Content-Type-Options: nosniff`.
5. **Referrer & Permissions:** Verify `Referrer-Policy: strict-origin-when-cross-origin` and restrictive `Permissions-Policy`.

### Phase 2: Frontend Bundle & Secret Leakage Inspection
Use REA MCP (`analyze_web_bundle`, `recover_javascript_sources`, `export_web_scripts`) or automated Python/Node inspection to scan all HTML and `.js` chunks:
```python
import urllib.request, re

url = "https://<target-domain>/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")

high_risk_patterns = {
    "Supabase Service Role Key": r"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+",
    "Private API Key / Secret": r"(?:sk_live_|secret_key|private_key|api_secret)\w+",
    "Database URL with Credentials": r"postgres://\w+:[^@]+@[\w\.-]+",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
}
api_routes = set(re.findall(r'["\'](/api/[\w\-/]+)["\']', html))
```
- **Safe to expose:** `NEXT_PUBLIC_*`, Supabase `anon_key` (only when RLS is enabled), Clerk publishable key (`pk_live_*`).
- **Critical Leaks:** Supabase `service_role_key`, Stripe `sk_live_*` / webhook secrets (`whsec_*`), database credentials, `.env` / `.git/HEAD` exposure.

### Phase 3: Auth & Database Access Controls (RLS Verification)
1. **Row Level Security (RLS):** Confirm all Supabase/PostgreSQL tables have `ENABLE ROW LEVEL SECURITY` and policies restricting access by `auth.uid() = user_id`.
2. **Session & JWT Security:** Verify short-lived access tokens, `HttpOnly; Secure; SameSite=Lax/Strict` cookies, and server-side session revocation.

### Phase 4: API Endpoint, GraphQL & Route Hardening
1. **Authentication & Authorization (BOLA/IDOR):** Verify unauthenticated requests to private `/api/*` routes return `401`/`403` and users cannot access other tenants' IDs.
2. **Rate Limiting & Schema Validation:** Ensure login, OTP, AI generation, and checkout endpoints enforce rate limits (Upstash Redis / Cloudflare WAF) and strict schema validation (Zod / Pydantic).
3. **GraphQL Introspection:** Check if production GraphQL endpoints leave full schema introspection and unbounded query depth open.

### Phase 5: Webhook & Payment Security
1. **Webhook Signature Verification:** Verify HMAC signatures (`stripe.webhooks.constructEvent`, Paddle signature verification) using the raw request body before fulfilling orders.
2. **Idempotency:** Verify duplicate event IDs are deduplicated in the database.

---

## 3. Complete 10-Layer Website Infrastructure & Tooling Matrix

When performing deep web architecture recovery, reconnaissance, or security scanning, leverage this 10-layer ecosystem:

1. **DNS, Domains & SSL/TLS Infrastructure:**
   - Diagnostics: `dig`, `nslookup`, `whois`, `traceroute`, `nmap`, `Shodan`, `Censys`, `DNSChecker`, `MXToolbox`.
   - TLS/Crypto: `openssl s_client`, `Certbot` / Let's Encrypt, Cloudflare SSL/TLS cipher grading.
2. **Web Servers, Reverse Proxies & Load Balancers:**
   - Servers & Proxies: Nginx, Apache, Caddy, Microsoft IIS, OpenLiteSpeed, HAProxy, Envoy Proxy, Traefik, AWS ALB/ELB, Cloudflare CDN.
3. **Web Hosting, Cloud Infrastructures & PaaS:**
   - Cloud & PaaS: AWS, GCP, Azure, Vercel, Netlify, Render, Railway, Fly.io, Cloudflare Pages, DigitalOcean, Hetzner, cPanel/Plesk.
4. **Containers, Orchestration & CI/CD:**
   - Runtime & Pipelines: Docker, Podman, LXC, Kubernetes (K8s), Helm, GitHub Actions, GitLab CI/CD, Jenkins, ArgoCD.
5. **Databases, Caches & Vector Stores:**
   - SQL/NoSQL/Vector: PostgreSQL, MySQL/MariaDB, SQLite, MongoDB, DynamoDB, Firestore, Redis, Kafka, Elasticsearch, Pinecone, Milvus, Chroma.
6. **Frontend, Backend Frameworks & CMS:**
   - Frontend: React, Next.js, Vue, Nuxt, Svelte, Tailwind CSS.
   - Backend: Node.js (Express, NestJS, Fastify), Python (Django, FastAPI, Flask), PHP (Laravel), Go (Gin, Fiber), Java (Spring Boot), Ruby on Rails.
   - CMS: WordPress, Strapi, Ghost, Drupal, Shopify, Magento.
7. **API Architecture, Testing & Documentation:**
   - Protocols & Specs: REST, GraphQL, gRPC, WebSockets, Webhooks, SOAP, OpenAPI / Swagger, Postman, Insomnia, Bruno, Hoppscotch.
8. **Web Traffic Inspection & Network Debugging:**
   - Intercepting Proxies: Burp Suite, OWASP ZAP, Caido, Charles Proxy, Proxyman, `mitmproxy`, HTTP Toolkit, Wireshark, `tcpdump`.
9. **Web Security Scanners, Fuzzers & WAFs:**
   - Discovery & Scanning: `Nuclei`, `ffuf`, `Gobuster`, `Feroxbuster`, `Dirsearch`, `SQLmap`, `Nikto`, `WPScan`, `Amass`, `Sublist3r`.
   - WAFs: Cloudflare WAF, ModSecurity, AWS WAF.
10. **Client-Side Web Reverse Engineering & Scraping:**
    - Inspection & Automation: REA MCP (`analyze_web_bundle`, `inspect_web_page`, `observe_web_session`), Chrome DevTools, `de4js`, `Retire.js`, Microsoft Playwright MCP, Puppeteer, Bright Data MCP, Hyperbrowser MCP, `Wappalyzer`.

---

## 4. Deliverable Format
Always structure the output report with:
1. **Executive Summary & Risk Score**
2. **Critical & High Priority Findings** (with exact proof/headers/lines)
3. **Medium & Low Priority Hardening**
4. **Verified Strengths**
5. **Copy-Paste Remediation Code Snippets** (`next.config.js`, `middleware.ts`, SQL RLS policies, Nginx/Cloudflare rules).
