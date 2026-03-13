---
name: seo-engine
description: >-
  Expert SEO auditing skill for analyzing URLs, HTML source code, robots.txt, and sitemaps. 
  Evaluates on-page technical requirements, content basics, optimization signals, 
  and spam-policy compliance (cloaking, hidden text, keyword stuffing).
  Trigger phrases: "Run an SEO audit", "Analyze this URL for SEO", "Check my webpage for SEO issues", 
  "Is my robots.txt correct?", "Find cloaking or hidden text on this page".
license: MIT
metadata:
  author: Abderrahmen Gharsallah
  version: "1.1.0"
  category: auditing
  tags: [seo, audit, technical-seo, spam-detection]
---

# SEO Engine

The SEO Engine provides a standardized methodology for performing deterministic SEO audits using pre-defined rules and specialized diagnostic scripts. It handles everything from input preparation (fetching live data) to heuristic analysis of spam policies.

## Use Case
Perform technical SEO audits on websites or local files to ensure compliance with search engine guidelines and identify potential ranking issues.

## Triggering Logic
Use this skill when a user:
- Provides a website URL for analysis.
- Uploads/references HTML, robots.txt, or sitemap files.
- Asks for a "technical SEO check" or "audit".
- Specifically mentions SEO-related concerns like "indexability", "crawlability", or "spam signals".

## When NOT to use
- For general SEO strategy advice (e.g., "how do I rank for 'best laptops'?").
- For off-page SEO (backlink analysis, domain authority).
- For live performance monitoring (use Lighthouse/CWV tools).

---

## Workflow: SEO Audit Pipeline

Follow these steps sequentially. Do not skip validation gates.

### Step 1 — Input Identification & Preparation

1.  **Identify Input:** URL or local files (`@filename.html`).
2.  **Validation Gate (Input Type):** Ensure the input is a valid URL or supported file types (`.html`, `.htm`, `robots.txt`, `.xml`).
3.  **Prepare Live Data (if URL):**
    - `cd scripts/prepare_input/`
    - Run `python fetch_html.py <URL>`
    - Run `python fetch_robots_txt.py <URL>`
    - Run `python fetch_sitemap.py <URL>`
4.  **Validation Gate (File Presence):** Confirm that the fetched files (or provided local files) are readable and non-empty.

### Step 2 — Basic Rule Application (Deterministic)

1.  Scan the `rules/` directory for applicable rules.
2.  Read the YAML frontmatter of each rule to match `inputFields` with your prepared data.
3.  **Execute Checks:** Compare the content of your files against the "Incorrect/Correct" examples in the rule documentation.
4.  **Apply Logic:** Categorize findings into Pass/Fail.

### Step 3 — Specialized Script Execution (Heuristic & Complex)

For complex checks, execute the dedicated Python scripts in the `scripts/` directory:

| Task | Script Path |
|---|---|
| **Cloaking** | `scripts/cloaking_detection/cloaking_detection.py` |
| **Hidden Text** | `scripts/hidden_text_detection/hidden_text_detection.py` |
| **Keyword Stuffing** | `scripts/keyword_stuffing_detection/keyword_stuffing_detection.py` |
| **Sneaky Redirects** | `scripts/sneaky_redirect_detection/sneaky_redirect_detection.py` |
| **Favicon Audit** | `scripts/favicon_dimensions/favicon_dimensions.py` |
| **Experience Diversity**| `scripts/page_experience_diversity/page_experience_diversity.py` |

*Instructions for running each script are found in their respective README.md files.*

### Step 4 — Result Synthesis & Reporting

1.  **Normalize Results:** Translate pass/fail outputs from rules and JSON results from scripts into a unified report.
2.  **Prioritization:** Sort results by "Critical", "High", "Medium", and "Low" priorities.
3.  **Remediation:** For every failure, provide the specific "Actionable Fix" found in the rule documentation or script output.

---

## Example Invocations

### Example 1 — Website URL Audit
**User:** "Analyze https://example.com for SEO issues"
**Action:** Prepare inputs using `fetch_*.py` -> Apply Rules -> Run specialized scripts -> Generate prioritized report.

### Example 2 — Local File Audit
**User:** "Check @index.html and @robots.txt for SEO compliance"
**Action:** Validate files -> Apply matching rules from `rules/` -> Report findings.

### Example 3 — Spam Detection
**User:** "Check if this page is using hidden text or cloaking: @page.html"
**Action:** Run `cloaking_detection.py` and `hidden_text_detection.py` -> Report similarity scores and hidden elements.

---

## Troubleshooting

### Skill Undertriggering
- **Cause:** Vague request like "Check my site".
- **Fix:** Ask the user to provide a specific URL or upload files. Re-trigger with "I will now run an SEO audit on [URL]".

### Preparation Failures
- If `fetch_html.py` fails due to bot detection, advise the user that the site might be blocking headless browsers.
- If `fetch_robots_txt.py` returns 503, immediately flag the `ROBOTS_TXT_NOT_503` rule as Critical Fail.

---

## Trigger Testing Plan

### Should Trigger
- "Run an SEO audit on example.com"
- "Audit this HTML file for technical SEO"
- "Are there any spam policy violations on this page?"
- "Check my sitemap and robots.txt for errors"

### Should NOT Trigger
- "Write a blog post about SEO"
- "What is the keyword volume for 'cat toys'?"
- "How do I get more backlinks?"
