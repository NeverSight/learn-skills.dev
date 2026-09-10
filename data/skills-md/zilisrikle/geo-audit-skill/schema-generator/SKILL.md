---
name: schema-generator
description: Generate JSON-LD structured data markup for any website. Supports HowTo, FAQPage, Article, BlogPosting, Organization, WebSite, BreadcrumbList, Product, LocalBusiness, and MedicalWebPage types.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch
context: fork
---

# Schema Generator Skill

You generate production-ready JSON-LD structured data for any website to maximize AI engine comprehension and rich result eligibility.

## Input

The user may provide:
- A URL to generate schema for
- A content file path to generate schema for
- A schema type to generate (e.g., "HowTo for onboarding guide")
- "site-wide" to generate Organization + WebSite + BreadcrumbList

If a `brand.md` exists in the project root, read it for publisher details (name, url, logo). Otherwise, infer from the target page.

## Schema Selection Logic

| Page Type | Schema Types to Generate |
|-----------|------------------------|
| Step-by-step guide / tutorial | HowTo + FAQPage + BreadcrumbList |
| Blog post / article | BlogPosting + FAQPage + BreadcrumbList |
| Long-form research article | Article + FAQPage + BreadcrumbList |
| Category / collection page | CollectionPage + ItemList + BreadcrumbList |
| Homepage | WebSite + Organization |
| About / company page | AboutPage + Organization |
| Product page | Product + FAQPage + BreadcrumbList |
| Local business | LocalBusiness + FAQPage |
| Health / medical content | MedicalWebPage + FAQPage + BreadcrumbList |

## Generation Process

### Step 1: Run Schema Check

```bash
python3 scripts/check-schema.py <url>
```

Review the output: what schema types are already present, what's missing, what's incomplete. Use this as the baseline — only generate what's needed.

### Step 2: Analyze Content

Read the page/content and identify:
- Primary topic and @type
- All steps (for HowTo)
- All Q&A pairs (for FAQ)
- Key entities and relationships
- Dates (published, modified)
- Authors and citations

### Step 3: Generate JSON-LD

Produce each schema block as a separate `<script>` tag:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "...",
  ...
}
</script>
```

### Step 4: Validate

```bash
# Validate JSON syntax
echo '<json-ld-content>' | python3 -m json.tool > /dev/null && echo "VALID" || echo "INVALID"
```

### Step 5: Cross-Reference

Ensure consistency:
- Organization name matches across all blocks
- URLs are absolute and correct
- Dates are in ISO 8601 format (YYYY-MM-DD)
- No placeholder text remaining

## Output

For each page, produce:
1. All applicable JSON-LD blocks
2. Implementation notes (where to place in HTML `<head>`)
3. Rich result eligibility assessment
4. Validation status

Save to `schema/[page-slug]-schema.json`.
