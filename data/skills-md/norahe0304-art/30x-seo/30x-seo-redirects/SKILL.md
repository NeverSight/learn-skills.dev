---
name: 30x-seo-redirects
description: >
  Redirect chain audit and analysis. Detects redirect loops, long chains,
  mixed protocols, and orphaned redirects. Use when user says "redirect audit",
  "301 redirect", "redirect chain", "redirect loop", or "migration redirects".
allowed-tools:
  - WebFetch
  - Read
---

# Redirect Audit

## What This Skill Does

Analyzes website redirects to find problems that hurt SEO and user experience.

## Why Redirects Matter

- **Every redirect = delay**: 301 redirects add 100-500ms latency
- **Chains lose link equity**: Google follows max ~5 hops, then stops
- **Wrong type = lost ranking**: 302 (temporary) doesn't pass full link juice
- **Loops = crawl waste**: Googlebot hits loop, gives up, page not indexed

## Check Categories

### 1. Redirect Chains
A redirect pointing to another redirect, pointing to another...

```
BAD:  /old → /old-2 → /old-3 → /final  (3 hops, slow, loses equity)
GOOD: /old → /final                     (1 hop, fast, full equity)
```

**Rule**: Maximum 1 redirect hop. More than 1 = fix immediately.

### 2. Redirect Loops
Page A redirects to B, B redirects back to A. Infinite loop.

```
BAD:  /page-a → /page-b → /page-a  (loop!)
```

**Detection**: Follow redirects up to 10 hops. If same URL appears twice = loop.

### 3. Redirect Type Audit

| Type | When to Use | SEO Impact |
|------|-------------|------------|
| 301 | Permanent move | Passes ~95% link equity |
| 302 | Temporary (A/B test, maintenance) | Passes less equity, can cause issues if permanent |
| 307 | Temporary (preserves HTTP method) | Same as 302 |
| 308 | Permanent (preserves HTTP method) | Same as 301 |
| Meta refresh | NEVER for SEO | Bad UX, slow, not recommended |
| JavaScript redirect | Avoid if possible | Googlebot may not follow |

**Rule**: Permanent moves must use 301 or 308. Using 302 for permanent = error.

### 4. Protocol Issues

```
BAD:  https://site.com → http://site.com  (downgrade, security warning)
BAD:  http → https → http                 (mixed, confusing)
GOOD: http://site.com → https://site.com  (upgrade, correct)
```

### 5. Domain Consistency

```
BAD:  www.site.com → site.com → www.site.com  (inconsistent)
GOOD: Pick ONE (www or non-www) and redirect all others to it
```

### 6. Trailing Slash Consistency

```
BAD:  /page → /page/ → /page  (loop risk)
GOOD: Pick ONE pattern (/page or /page/) and redirect all others
```

### 7. Post-Migration Orphans
After site migration/redesign:
- Old URLs that redirect to 404 or homepage (should go to equivalent new page)
- Important pages with no redirect (losing all link equity)

### 8. Soft 404s via Redirect
Redirecting deleted pages to homepage = soft 404 penalty risk.

```
BAD:  /deleted-product → /  (Google sees this as soft 404)
GOOD: /deleted-product → 410 Gone (or related category page)
```

## How to Run Audit

### Method 1: Crawl-based (recommended)
Use squirrel audit or similar crawler to:
1. Crawl entire site
2. Follow all internal links
3. Record redirect chains

### Method 2: Log-based (for large sites)
Analyze server access logs for:
- All 301/302 responses
- Most-hit redirect URLs
- External referrers hitting redirects

### Method 3: URL list
If you have a list of old URLs (from migration):
1. Check each URL
2. Record final destination
3. Flag chains, loops, 404s

## Output Format

### Redirect Health Score: XX/100

### Critical Issues (Fix Immediately)
| Issue Type | Count | Example |
|------------|-------|---------|
| Redirect loops | X | /a → /b → /a |
| 5+ hop chains | X | /old → ... → /new |
| HTTPS downgrade | X | https → http |

### High Priority (Fix This Week)
| Issue Type | Count | Example |
|------------|-------|---------|
| 3-4 hop chains | X | /old → /mid → /new |
| 302 used for permanent | X | /old-page 302→ /new-page |
| Soft 404 redirects | X | /deleted → / |

### Medium Priority (Fix This Month)
| Issue Type | Count | Example |
|------------|-------|---------|
| 2 hop chains | X | /old → /mid → /new |
| Inconsistent trailing slash | X | /page and /page/ both exist |

### Redirect Map
Top 20 most-accessed redirects and their chains:
| Source URL | Hops | Final Destination | Type | Monthly Hits |
|------------|------|-------------------|------|--------------|

### Recommendations
1. [Specific fix instructions based on findings]

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
