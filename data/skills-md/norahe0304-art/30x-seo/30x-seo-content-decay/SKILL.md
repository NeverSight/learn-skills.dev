---
name: 30x-seo-content-decay
description: >
  Detect content decay - old content losing rankings/traffic that needs refresh.
  Identifies pages published >6 months ago with declining performance.
  Outputs refresh priority list with specific update recommendations.
metadata:
  version: 1.0.0
  category: content
  dependencies: [WebFetch]
allowed-tools:
  - WebFetch
  - Read
---

# Content Decay Detection

> Find declining old content that needs refresh

## What is Content Decay

Content "rots" over time:
- Information becomes outdated (2023 data is stale in 2026)
- Competitors publish better content
- Search intent changes
- Google algorithm updates

**Result**: Rankings drop → Traffic drops → Revenue drops

---

## Detection Criteria

| Metric | Threshold | Description |
|--------|-----------|-------------|
| **Publication Date** | >6 months | New content doesn't count as decay |
| **Traffic Change** | Down >20% | Compared to 3 months ago |
| **Ranking Change** | Down >5 positions | Primary keyword |
| **CTR Change** | Down >15% | Title may need updating |

**Trigger Refresh**: Meeting any 2 criteria = needs refresh

---

## Workflow

### Method A: With GSC Data

```
User provides GSC export (CSV)
↓
Analyze each URL:
- Impression trends
- Click trends
- Average position trends
- CTR trends
↓
Identify decaying content
↓
Output refresh priority list
```

### Method B: Without GSC Data

```
User provides URL list
↓
Check each page:
- Publication date / Last updated date
- Content timeliness signals (years, "latest", etc.)
- Competitor SERP analysis (your content vs Top 10)
↓
Identify potentially decaying content
↓
Output recommendation list
```

---

## Output Format

```markdown
# Content Decay Report

## High Priority Refresh (High Traffic Impact)

| Page | Published | Traffic Change | Rank Change | Issue | Recommendation |
|------|-----------|----------------|-------------|-------|----------------|
| /blog/best-crm-2024 | 2024-03 | -45% | -8 positions | Year outdated | Update to 2026 version |
| /guide/remote-work | 2023-11 | -30% | -5 positions | Tool recommendations outdated | Update tool list |

## Medium Priority Refresh

| Page | Published | Issue | Recommendation |
|------|-----------|-------|----------------|
| ... | ... | ... | ... |

## Refresh Recommendations

### /blog/best-crm-2024

**Problem Diagnosis**:
- Title contains "2024", outdated
- Pricing info may be inaccurate
- Missing 2025-2026 new features

**Refresh Checklist**:
- [ ] Update title to "Best CRM 2026"
- [ ] Verify all prices
- [ ] Add new tools (X, Y, Z)
- [ ] Update screenshots
- [ ] Check all external links are valid
- [ ] Update dateModified in Schema

**Estimated Impact**: Recover ~40% traffic
```

---

## Refresh Strategies

### Light Refresh (Quick Update)

**When**: Minor information outdated

- Update years
- Update prices/data
- Fix dead links
- Update dateModified

### Medium Refresh (Content Update)

**When**: Content partially outdated

- Rewrite outdated sections
- Add new information
- Update images/screenshots
- Add new H2 sections

### Heavy Refresh (Content Rewrite)

**When**: Content significantly outdated or intent changed

- Re-analyze SERP intent
- Rewrite most content
- May need new content-brief
- Keep URL (preserve 301 historical equity)

---

## Usage

```bash
# With GSC data
/seo content-decay --gsc [csv-file]

# Without GSC, provide URL list
/seo content-decay --urls [url-list]

# Analyze entire site (crawl sitemap)
/seo content-decay https://example.com
```

---

## Related Skills

| Upstream | This Skill | Downstream |
|----------|------------|------------|
| GSC data | **30x-seo-content-decay** | 30x-seo-content-brief |
| sitemap | ↓ Identify decay | 30x-seo-content-writer |
| | | (refresh content) |

---

## Best Practices

1. **Regular checks**: Run decay detection quarterly
2. **Prioritize high-value pages**: Refresh high traffic/conversion pages first
3. **Keep URLs**: Refresh rather than recreate, preserve historical equity
4. **Update dateModified**: Tell Google content has been updated
5. **Internal link check**: Check if internal links need updating after refresh

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
