---
name: article-extractor
description: Extract MQL5 articles and documentation. TRIGGERS - MQL5 articles, MetaTrader docs, mql5.com resources.
allowed-tools: Read, Bash, Grep, Glob
---

# MQL5 Article Extractor

Extract technical trading articles from mql5.com for training data collection. **Scope limited to mql5.com domain only.**

## When to Use This Skill

Use this skill when:

- Extracting articles from mql5.com for reference or training data
- Downloading MQL5 documentation and tutorials
- Collecting trading articles from specific MQL5 users
- Building a corpus of MQL5 programming examples

## Scope Boundaries

**VALID requests:**

- "Extract this mql5.com article: <https://www.mql5.com/en/articles/19625>"
- "Get all articles from MQL5 user 29210372"
- "Download trading articles from mql5.com"
- "Extract 5 MQL5 articles for testing"

**OUT OF SCOPE:**

- "Extract from yahoo.com" - NOT SUPPORTED (mql5.com only)
- "Scrape news from reuters" - NOT SUPPORTED (mql5.com only)
- "Get stock data from Bloomberg" - NOT SUPPORTED (mql5.com only)

If user requests non-mql5.com extraction, respond: "This skill extracts articles from mql5.com ONLY. For other sites, use different tools."

## Repository Location

Working directory: `$HOME/eon/mql5` (adjust path for your environment)

Always execute commands from this directory:

```bash
cd "$HOME/eon/mql5"
```

## Valid Input Types

### 1. Article URL (Most Specific)

**Format**: `https://www.mql5.com/en/articles/[ID]`
**Example**: `https://www.mql5.com/en/articles/19625`
**Action**: Extract single article

### 2. User ID (Numeric or Username)

**Format**: Numeric (e.g., `29210372`) or username (e.g., `jslopes`)
**Source**: From mql5.com profile URL
**Action**: Auto-discover and extract all user's articles

### 3. URL List File

**Format**: Text file with one URL per line
**Action**: Batch process multiple articles

### 4. Vague Request

If user says "extract mql5 articles" without specifics, prompt for:

1. Article URL OR User ID
1. Quantity limit (for testing)
1. Output location preference

---

## Reference Documentation

For detailed information, see:

- [Extraction Modes](./references/extraction-modes.md) - Single, batch, auto-discovery, official docs modes
- [Data Sources](./references/data-sources.md) - User collections and official documentation
- [Troubleshooting](./references/troubleshooting.md) - Common issues and solutions
- [Examples](./references/examples.md) - Usage examples and patterns

---

## Troubleshooting

| Issue                  | Cause                         | Solution                                          |
| ---------------------- | ----------------------------- | ------------------------------------------------- |
| Non-mql5.com URL       | Skill only supports mql5.com  | Use other tools for non-mql5.com sites            |
| Article not found      | Invalid article ID or removed | Verify URL exists by visiting in browser          |
| User ID not recognized | Wrong user ID format          | Use numeric ID from profile URL or exact username |
| Empty extraction       | Rate limiting or site change  | Wait and retry, check for site structure changes  |
| Permission denied      | Working directory mismatch    | Run from $HOME/eon/mql5 directory                 |
| Batch too large        | Too many articles requested   | Limit batch size, use URL list file               |
| Missing dependencies   | Required tools not installed  | Install curl, jq for extraction                   |
| Output encoding issues | Unicode in article content    | Ensure UTF-8 output handling                      |
