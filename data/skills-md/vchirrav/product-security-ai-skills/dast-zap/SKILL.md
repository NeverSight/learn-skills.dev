---
name: dast-zap
description: Run OWASP ZAP for Dynamic Application Security Testing. Performs baseline, full, or API scans against running web applications to find XSS, SQLi, CSRF, and other runtime vulnerabilities.
---

# DAST Scan with OWASP ZAP

You are a security engineer running Dynamic Application Security Testing (DAST) using **OWASP ZAP** (Zed Attack Proxy).

## When to use

Use this skill when asked to perform a dynamic security scan against a running web application or API.

## Prerequisites

- ZAP installed (Docker recommended: `docker pull zaproxy/zap-stable`)
- Or standalone: download from zaproxy.org
- Target application must be running and accessible

## Instructions

1. **Identify the target** — Confirm the URL of the running application.
2. **Run the scan:**

   **Baseline scan (passive, fast):**
   ```bash
   docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
     zap-baseline.py -t <target-url> -J zap-baseline-results.json
   ```

   **Full scan (active + passive):**
   ```bash
   docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
     zap-full-scan.py -t <target-url> -J zap-full-results.json
   ```

   **API scan (OpenAPI/GraphQL):**
   ```bash
   docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
     zap-api-scan.py -t <openapi-url> -f openapi -J zap-api-results.json
   ```

3. **Parse the results** — Read JSON output and present findings:

```
| # | Risk | Confidence | Alert | URL | CWE | Description | Solution |
|---|------|------------|-------|-----|-----|-------------|----------|
```

4. **Summarize** — Provide:
   - Total alerts by risk level (High/Medium/Low/Informational)
   - Attack vectors found with proof-of-concept details
   - Specific remediation steps

## ZAP Scan Types

| Scan Type | Speed | Coverage | Use Case |
|-----------|-------|----------|----------|
| Baseline | ~2 min | Passive only | CI/CD gates, quick checks |
| Full | 10-60 min | Active + passive | Pre-release security review |
| API | 5-20 min | API-focused | REST/GraphQL endpoint testing |
