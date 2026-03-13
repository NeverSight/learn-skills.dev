---
name: seo
description: SEO auditing, optimization, and implementation. Use when auditing sites for SEO issues, optimizing content for search, conducting keyword research, implementing technical SEO, or improving organic search performance. For automated crawl-based audits with 230+ rules, use audit-website instead.
metadata:
  version: 1.0.0
---

# SEO — Audit & Optimization

Expert guidance for identifying SEO issues and implementing improvements to boost organic search performance.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions.

Before auditing, understand:

1. **Site Context** — Type (SaaS, e-commerce, blog), primary SEO goal, priority keywords
2. **Current State** — Known issues, organic traffic level, recent changes/migrations
3. **Scope** — Full site or specific pages? Technical + on-page, or one focus area?

---

## Audit Framework

### ⚠️ Schema Markup Detection Limitation

`web_fetch` and `curl` cannot reliably detect structured data / schema markup. Many CMS plugins inject JSON-LD via client-side JavaScript.

**To check for schema markup, use:**
1. **Browser tool** — render page and run: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results

**Never report "no schema found" based solely on `web_fetch` or `curl`.**

### Priority Order
1. **Crawlability & Indexation** — Can Google find and index it?
2. **Technical Foundations** — Is the site fast and functional?
3. **On-Page Optimization** — Is content optimized?
4. **Content Quality** — Does it deserve to rank?
5. **Authority & Links** — Does it have credibility?

---

## Technical SEO

### Crawlability
- **Robots.txt** — Check for unintentional blocks, verify sitemap reference
- **XML Sitemap** — Exists, submitted to Search Console, contains only canonical indexable URLs
- **Site Architecture** — Important pages within 3 clicks, logical hierarchy, no orphan pages
- **Crawl Budget** (large sites) — Parameterized URLs, faceted navigation, infinite scroll

### Indexation
- **Index Status** — `site:domain.com` check, Search Console coverage
- **Issues** — Noindex on important pages, wrong canonicals, redirect chains, soft 404s, duplicates
- **Canonicalization** — Self-referencing canonicals, HTTP→HTTPS, www consistency, trailing slashes

### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s
- **INP** (Interaction to Next Paint): < 200ms
- **CLS** (Cumulative Layout Shift): < 0.1

**Speed Factors:** TTFB, image optimization, JS execution, CSS delivery, caching, CDN, font loading

### Mobile & Security
- Responsive design, tap targets, viewport, no horizontal scroll
- HTTPS everywhere, valid SSL, no mixed content, HSTS

### URL Structure
- Readable, descriptive, keyword-rich, lowercase, hyphen-separated

---

## On-Page SEO

### Title Tags
- Unique per page, primary keyword near beginning, 50-60 chars, compelling
- **Common issues:** Duplicate, truncated, keyword-stuffed, missing

```html
<!-- Good -->
<title>Ultimate Guide to React Hooks - Learn useEffect & useState</title>
```

### Meta Descriptions
- Unique per page, 150-160 chars, includes keyword, clear CTA
- **Common issues:** Duplicate, auto-generated, too long/short

### Heading Structure
- One H1 per page with primary keyword, logical H1→H2→H3 hierarchy
- **Common issues:** Multiple H1s, skipped levels, headings for styling only

### Content Optimization
- Keyword in first 100 words, related terms used naturally
- Sufficient depth/length, answers search intent, better than competitors

### Image Optimization
```html
<img
  src="/images/react-hooks-diagram.webp"
  alt="React Hooks lifecycle diagram showing useState and useEffect"
  width="800" height="600" loading="lazy"
/>
```

### Internal Linking
- Descriptive anchor text, 3-5 internal links per 1000 words
- No orphan pages, no broken links, reasonable link count

### Schema Markup (Structured Data)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Complete Guide to React Hooks",
  "datePublished": "2024-01-15",
  "author": { "@type": "Person", "name": "Jane Developer" }
}
```

**Common types:** Article, Product, FAQ, HowTo, Organization, LocalBusiness, BreadcrumbList

---

## Content Quality

### E-E-A-T Signals
- **Experience** — First-hand experience, original insights/data
- **Expertise** — Author credentials, accurate detailed info
- **Authoritativeness** — Recognized in space, cited by others
- **Trustworthiness** — Transparent, contact info, HTTPS

### Content Depth
- Comprehensive coverage, answers follow-up questions
- Better than top competitors, updated and current

---

## Advanced Strategies

### Topic Clusters & Pillar Pages
```
Pillar: "Complete Guide to React"
  ├── "React Hooks Tutorial"
  ├── "React Context API Guide"
  ├── "React Performance Optimization"
  └── "React Testing Best Practices"
```

### Featured Snippet Optimization
- Question-based content with concise answers
- List-based and table-based content formats

---

## Common Issues by Site Type

| Type | Common Issues |
|------|--------------|
| **SaaS** | Thin product pages, blog not linked to product, missing comparison pages |
| **E-commerce** | Thin category pages, duplicate descriptions, missing product schema |
| **Blog** | Outdated content, keyword cannibalization, no topic clusters |
| **Local** | Inconsistent NAP, missing local schema, no GMB optimization |

---

## SEO Content Checklist

- [ ] Title tag with primary keyword (under 60 chars)
- [ ] Meta description (150-160 chars, compelling)
- [ ] H1 with primary keyword
- [ ] URL slug optimized
- [ ] Images compressed with alt text
- [ ] 3-5 internal links
- [ ] Schema markup implemented
- [ ] Mobile-friendly and responsive
- [ ] Page speed optimized (< 3s)
- [ ] Canonical tag set correctly
- [ ] Open Graph + Twitter Card tags

---

## Output Format

**Executive Summary** — Health assessment, top 3-5 priorities, quick wins

**Per Issue:** Issue → Impact (H/M/L) → Evidence → Fix → Priority

**Action Plan:**
1. Critical fixes (blocking indexation)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

---

## Tools

**Free:** Google Search Console, PageSpeed Insights, Rich Results Test, Bing Webmaster Tools
**Paid:** Screaming Frog, Ahrefs/Semrush, Sitebulb

---

## References

- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid

## Related Skills

- **audit-website**: Automated website auditing with squirrelscan CLI (230+ rules)
- **page-cro**: Optimizing pages for conversion (not just ranking)
