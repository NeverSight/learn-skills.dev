---
name: mitm-find-referer
description: Find Referer header leakage vulnerabilities. Use when user asks about URL leakage, third-party data exposure, or sensitive data in headers.
---

# Find Referer Header Leakage

Analyze the mitmproxy dump (log.txt) for Referer leakage for: $ARGUMENTS

> **Requires**: `log.txt` in the current directory. If it's missing, capture traffic first:
> ```bash
> mitmdump --set flow_detail=3 2>&1 | tee log.txt
> ```

## What to Look For

### 1. Sensitive Data in URLs
- Tokens in URL being leaked via Referer
- Session IDs in query parameters
- User IDs, order IDs in path
- Payment transaction IDs

### 2. Third-Party Requests
- External scripts receiving internal URLs
- CDN requests with sensitive referers
- Social widgets getting page URLs
- External images/fonts leaking URLs

### 3. Analytics Leakage
- Google Analytics receiving sensitive URLs
- Third-party analytics with full page paths
- Marketing pixels with transaction data

### 4. Payment Page Leaks
- Payment IDs leaked to external sites
- Transaction URLs sent to verification badges
- "Verified by Visa" logos receiving payment URLs

## Vulnerable Patterns

- External link clicks from sensitive pages
- Third-party widgets on payment pages
- Analytics on authenticated pages
- Social sharing from transaction pages

## Output Format

For each finding:
- **External Domain**: Who receives the data
- **Leaked Data**: What sensitive info is exposed
- **Source Page**: Where the leak originates
- **Severity**: Based on data sensitivity
- **Fix**:
  - Add `Referrer-Policy: no-referrer` header
  - Use `rel="noreferrer"` on links
  - Remove sensitive data from URLs
  - Use POST instead of GET for sensitive data
