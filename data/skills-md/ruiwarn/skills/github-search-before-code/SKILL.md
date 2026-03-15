---
name: github-search-before-code
description: "Proactively search GitHub for reference implementations before writing new code. Use this skill when: (1) User requests implementing completely new functionality, algorithms, or modules that don't exist in the current codebase, (2) User mentions repeated failures with phrases like 'still not working', 'tried many times', 'still has problems', or (3) AI recognizes the need to implement unfamiliar or complex features. The skill helps avoid reinventing the wheel by finding and analyzing existing high-quality implementations, then adapting them to user needs."
---

# GitHub Search Before Code

## Trigger Conditions

**Scenario 1 - New functionality**: New algorithms, protocols, drivers, or complex features not in codebase
**Scenario 2 - Repeated failures**: User says "still not working", "tried many times", "改了很多次了", "还是有问题"

## Workflow

### 1. Infer Domain

Analyze conversation context to extract 1-2 domain keywords:
- Without first identifying the industry background, keyword extraction may lead to results that are completely off-topic.
- Current discussion topic
- Recent code files/functions
- User's project description

If unclear, see [industry-background.md](references/industry-background.md) for domain keyword reference.

### 2. Construct Keywords

Pattern: `"<function> <domain> <tech>"`

Examples:
- C: "harmonic analysis" + "power" → `"harmonic analysis power metering" C`
- Python: "web scraping" → `"web scraping beautifulsoup" Python`
- Shell: "backup automation" → `"incremental backup script" Shell`

**Domain matters**: "Goertzel" → audio ❌, "Goertzel power" → power analysis ✅

### 3. Search GitHub

```bash
python3 scripts/github_search.py repo "<keywords>" [language]
```

**Features**:
- see [search-strategies.md](references/search-strategies.md) for search flow reference.
- Auto-fallback: tries 4 strategies if no results (language → no-lang → simplified → core-word)
- Token support: set `GITHUB_TOKEN` env var for 5000/h quota (vs 60/h)
- Desc truncated to 200 chars to save tokens

### 4. Analyze & Use

**Screen**: Stars > 20, language matches project, updated < 2yr
**Read**: WebFetch README for key info
**Use**: Extract logic, adapt style, add `// Reference: [URL]` (or `# Reference:` for Python/Shell)

**No results**: Try broader keywords or WebSearch

## Commands
Output: `⭐stars | lang | year | desc` (sorted by stars)
