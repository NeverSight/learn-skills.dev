---
name: seo
description: Governs Technical SEO, Google Helpful Content (E-E-A-T) compliance, organic search ranking, and human-grade anti-AI content writing for public web applications.
---

# SEO & Humanized Content Engineering Skill

Activate this skill when creating or editing public-facing web pages, marketing copy, blog posts, landing pages, metadata, sitemaps, robots configurations, or structured data (JSON-LD).

> **Operational Directive:** *Deliver zero-slop, high-information-gain content that satisfies user search intent, strictly complies with Google's Helpful Content and E-E-A-T guidelines, and eliminates predictable AI writing patterns.*

---

## 1. Relevance Gate: Public vs Private Routes

* **Public Pages (Marketing, Blog, Docs, Landing Pages, Public Profiles):** SEO is active. Generate clean metadata, OpenGraph tags, sitemaps, structured JSON-LD schemas, and human-grade, high-ranking content.
* **Private Authenticated Areas (Admin Panels, User Dashboards, Billing Settings):** Do NOT inject heavy SEO infrastructure, sitemaps, or structured schemas. Ensure `<meta name="robots" content="noindex, nofollow" />` is set.

---

## 2. Core Technical SEO Checklist

1. **Title & Meta Description:**
   - `<title>`: Unique per page, 50–60 characters max, format: `[Page Title] | [Brand Name]`.
   - `<meta name="description">`: Engaging summary, 140–160 characters max. Include primary search intent without keyword stuffing.
2. **Heading Hierarchy:**
   - Exactly one `<h1>` per indexable page representing the primary topic and search intent.
   - Follow logical sequential order: `<h1>` -> `<h2>` -> `<h3>` (never skip levels for styling).
3. **Canonical URLs:**
   - Explicit `<link rel="canonical" href="https://example.com/canonical-path" />` on every public page.
4. **Social Sharing Metadata (Open Graph & Twitter Cards):**
   - `og:title`, `og:description`, `og:image` (1200x630px recommended), `og:url`, `og:type`.
   - `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image`.

---

## 3. Structured Data Schema (JSON-LD)

For articles, software tools, or organizations, provide valid JSON-LD schemas:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Tailor",
  "operatingSystem": "All",
  "applicationCategory": "DeveloperApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

---

## 4. Sitemaps & Robots Configuration

* Maintain an automatically generated `sitemap.xml` listing all indexable canonical URLs.
* Provide a clean `robots.txt` referencing the sitemap and disallowing private endpoints (`/api/`, `/admin/`, `/dashboard/`).

---

## 5. Google Helpful Content & E-E-A-T Invariants

Every piece of written web content must strictly align with Google's Search Essentials, March 2024 Core Update (anti-scaled-content-abuse), and E-E-A-T Quality Rater Guidelines:

1. **Experience (First-Hand Evidence):**
   - Ground arguments in tangible real-world evidence: specific metrics, terminal output, actual benchmark numbers, real trade-offs, or concrete code snippets.
   - Never write speculative summaries without empirical backing.
2. **Expertise (Domain Depth):**
   - Use precise technical terminology correctly; do not simplify to the point of factual dilution.
   - Address edge cases, real friction points, and constraints rather than painting an idealized picture.
3. **Authoritativeness & Information Gain:**
   - **Google Information Gain Patent Requirement:** Content must provide *new* value beyond existing SERP results. Never rehash what the top 5 Google results say. Include original insights, counter-intuitive findings, or proprietary workflow comparisons.
   - Cite authoritative primary documentation or verified sources.
4. **Trustworthiness (Accuracy & Transparency):**
   - State limitations upfront. If a tool or solution fails in specific environments (e.g. Windows symlink quirks, node ESM resolution), state it plainly.

---

## 6. Anti-AI / Anti-ChatGPT Editorial Directives (De-LLM Filter)

LLM-generated text defaults to recognizable, low-perplexity, low-burstiness patterns that trigger spam filters and cause bounce rates. Strictly enforce the following rules:

### A. The Banned Vocabulary & Cliché Blacklist
**NEVER use the following AI hallmark words and phrases:**
* *Banned verbs/adjectives:* "delve", "tapestry", "beacon", "testament", "multifaceted", "plethora", "pivotal", "fostering", "harnessing", "unwavering", "demystify", "embark", "realm", "crucial", "paramount", "game-changer", "transformative".
* *Banned throat-clearing openings:* "In today's fast-paced digital world...", "In the ever-evolving landscape of...", "Have you ever wondered...", "In this comprehensive guide, we will explore...".
* *Banned summary conclusions:* "In conclusion...", "To wrap it up...", "As we look ahead...", "Ultimately, the choice depends on your specific needs...".

### B. Syntactic Burstiness (Sentence Rhythm)
* **Vary sentence length aggressively.** Combine punchy fragments or short sentences (3–6 words) with medium sentences (10–14 words) and occasional complex compound sentences (20–28 words).
* Avoid the classic LLM monotonic cadence where every sentence is approximately 16–18 words.

### C. Bottom Line Up Front (BLUF) / Inverted Pyramid
* Deliver the direct answer or core solution within the first two sentences.
* Never force readers to wade through background history or definitions before answering the query intent.

### D. Asymmetrical, Organic Layouts (Anti-Symmetric Listicle)
* Reject the predictable LLM bullet format: `**[Bold Title]:** [Verb] [Uniform 15-word explanation]`.
* Mix paragraphs, code snippets, comparison tables, and short checklists. Some bullet points should be three words; others should be two full sentences.

### E. Active Voice & Definite Opinions
* Avoid passive hedging ("It can be argued that...", "Some developers prefer...").
* Take clear, defensible engineering stances based on verified performance and empirical reality.

---

## 7. Pre-Publish Content Quality Gate

Before approving any public content or page copy, verify:
* [ ] Does the page answer the search intent in the first 50 words?
* [ ] Does the copy contain zero blacklisted AI words (`delve`, `tapestry`, `landscape`, `testament`, etc.)?
* [ ] Is there measurable information gain (benchmarks, original code, distinct perspective) not found in competing SERP articles?
* [ ] Is heading hierarchy strictly sequential (`h1` -> `h2` -> `h3`)?
* [ ] Are title tag (50–60 chars) and meta description (140–160 chars) uniquely configured?
