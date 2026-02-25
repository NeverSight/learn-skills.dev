---
name: article-extractor
description: Extracts and organizes MQL5 articles and documentation. Use when researching MQL5 features, MetaTrader API documentation, Python MT5 integration, or algorithmic trading resources.
allowed-tools: Read, Bash, Grep, Glob
---

# MQL5 Article Extractor

Extract technical trading articles from mql5.com for training data collection. **Scope limited to mql5.com domain only.**

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
2. Quantity limit (for testing)
3. Output location preference

---

## Reference Documentation

For detailed information, see:

- [Extraction Modes](./references/extraction-modes.md) - Single, batch, auto-discovery, official docs modes
- [Data Sources](./references/data-sources.md) - User collections and official documentation
- [Troubleshooting](./references/troubleshooting.md) - Common issues and solutions
- [Examples](./references/examples.md) - Usage examples and patterns
