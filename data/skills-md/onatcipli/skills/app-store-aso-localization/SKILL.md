---
name: app-store-aso-localization
description: >
  App Store Optimization and metadata localization for iOS/macOS apps. Use this
  skill when working with App Store metadata for any of these tasks:
  (1) Analyzing current app metadata health (character usage, missing localizations),
  (2) Keyword research and optimization across locales,
  (3) Translating and localizing metadata to 38+ languages,
  (4) Implementing cross-localization strategies to maximize keyword coverage,
  (5) Bulk updating metadata via App Store Connect API,
  (6) Competitor ASO analysis and keyword gap identification,
  (7) Generating optimized titles, subtitles, keywords, and descriptions,
  (8) Auditing metadata for ASO best practices compliance.
---

# App Store ASO & Localization

Optimize your App Store metadata and localize across 38 languages using ASO best
practices and the App Store Connect API.

## Metadata Field Reference

| Field | Limit | Indexed | Level | Notes |
|-------|-------|---------|-------|-------|
| **App Name** | 30 chars | Yes (highest) | App | Brand + primary keyword |
| **Subtitle** | 30 chars | Yes (medium) | App | USP + secondary keywords |
| **Keywords** | 100 chars | Yes (iOS only) | Version | Comma-separated, no spaces |
| **Promotional Text** | 170 chars | No | Version | Can update without review |
| **Description** | 4,000 chars | No (iOS) | Version | Conversion-focused |
| **What's New** | 4,000 chars | No | Version | Release notes |

**Important:** iOS App Store does NOT index the description for search. Focus
keywords in Title → Subtitle → Keywords field only.

## API Access

| Tier | Auth | Endpoints | Use Case |
|------|------|-----------|----------|
| **Public** | None | iTunes Search/Lookup | Competitor research |
| **Private** | JWT | App Store Connect API | Manage your metadata |

For authentication setup, see [api-endpoints.md](references/api-endpoints.md).

---

## Workflow 1 — Analyze Current Metadata

Audit your app's metadata for optimization opportunities.

### Step 1: Fetch Current Localizations

```
GET /v1/apps/{appId}/appInfos
GET /v1/appInfos/{appInfoId}/appInfoLocalizations
GET /v1/appStoreVersions/{versionId}/appStoreVersionLocalizations
```

### Step 2: Check Character Usage

For each locale, calculate usage percentage:

```python
fields = {
    "name": {"limit": 30, "value": localization.name},
    "subtitle": {"limit": 30, "value": localization.subtitle},
    "keywords": {"limit": 100, "value": localization.keywords},
    "promotionalText": {"limit": 170, "value": localization.promotionalText},
    "description": {"limit": 4000, "value": localization.description}
}

for field, data in fields.items():
    usage = len(data["value"]) / data["limit"] * 100
    if usage < 90:
        flag_underutilized(field, usage)
```

### Step 3: Identify Missing Localizations

Compare active localizations against recommended markets:

```
Priority markets: en-US, en-GB, de-DE, fr-FR, ja, zh-Hans, zh-Hant,
                  ko, es-ES, es-MX, pt-BR, it, nl, ru, tr, ar
```

### Step 4: Check for ASO Violations

- Duplicate keywords across Title/Subtitle/Keywords
- Stop words in keywords field ("the", "and", "app", "a", "an")
- Spaces after commas in keywords
- Keywords repeated across locales (wasteful)

### Step 5: Generate Health Report

```markdown
## Metadata Health Report — {App Name}

### Overview
- Active localizations: 12/38
- Character utilization: 78% average
- ASO violations: 3 found

### Character Usage by Locale

| Locale | Name | Subtitle | Keywords | Status |
|--------|------|----------|----------|--------|
| en-US  | 28/30 (93%) | 25/30 (83%) | 98/100 (98%) | Good |
| de-DE  | 22/30 (73%) | 18/30 (60%) | 72/100 (72%) | Underutilized |
| ja     | 15/30 (50%) | 12/30 (40%) | 45/100 (45%) | Poor |

### Missing High-Value Localizations
- zh-Hans (China) — 2nd largest App Store
- ko (Korea) — High spending market
- pt-BR (Brazil) — Growing market

### ASO Violations Found
1. ❌ Keyword "photo" appears in both Title and Keywords (en-US)
2. ❌ Stop word "app" in keywords field (en-GB)
3. ❌ Space after comma in keywords (de-DE)

### Recommendations
1. Add Chinese (Simplified) localization — potential +15% downloads
2. Expand German keywords to use full 100 characters
3. Remove duplicate keywords to add more unique terms
```

---

## Workflow 2 — Keyword Research & Optimization

Research and optimize keywords for maximum discoverability.

### Step 1: Seed Keyword Collection

Gather initial keywords from:

1. **Your metadata** — Current title, subtitle, keywords
2. **Competitor metadata** — Via iTunes Lookup API
3. **Review mining** — Common words in user reviews
4. **Category analysis** — Top apps in your category

```
GET https://itunes.apple.com/lookup?id={competitor_id}&country={cc}
```

### Step 2: Keyword Analysis

For each keyword, evaluate:

| Metric | Description | Source |
|--------|-------------|--------|
| **Search Volume** | How often users search this term | ASO tools / estimation |
| **Difficulty** | Competition level (0-100) | Top 10 app ratings |
| **Relevance** | How well it describes your app | Manual assessment |
| **Current Rank** | Your position for this keyword | Track over time |

### Step 3: Keyword Scoring

```python
def score_keyword(volume, difficulty, relevance):
    """
    Higher score = better keyword opportunity
    Volume: 1-100, Difficulty: 1-100, Relevance: 1-10
    """
    opportunity = volume * (1 - difficulty/100)
    score = opportunity * relevance
    return score
```

### Step 4: Generate Optimized Keyword Set

Rules for the 100-character keywords field:

1. **No duplicates** — Words in Title/Subtitle are already indexed
2. **No spaces** — Use commas only: `keyword1,keyword2,keyword3`
3. **No stop words** — Remove "the", "and", "a", "an", "app"
4. **Single words** — Break phrases into individual tokens
5. **Prioritize** — Highest-scoring keywords first

```markdown
## Optimized Keywords — {App Name} (en-US)

### Title (30 chars)
"PhotoEdit Pro - Picture Editor"
Keywords captured: photoedit, pro, picture, editor

### Subtitle (30 chars)
"Filters, Collage & Retouch"
Keywords captured: filters, collage, retouch

### Keywords Field (100 chars)
"camera,enhance,crop,adjust,brightness,contrast,saturation,blur,sharpen,resize,rotate,frame,effects"
Characters used: 97/100

### Total Unique Keywords: 17
```

See [keyword-strategies.md](references/keyword-strategies.md) for advanced techniques.

---

## Workflow 3 — Localize Metadata

Translate and adapt metadata for international markets.

### Step 1: Select Target Locales

Prioritize by market opportunity:

| Tier | Locales | Rationale |
|------|---------|-----------|
| **Tier 1** | en-US, en-GB, de-DE, ja, zh-Hans | Largest markets |
| **Tier 2** | fr-FR, ko, es-ES, pt-BR, it | High growth |
| **Tier 3** | nl, ru, tr, ar, zh-Hant, sv | Market expansion |
| **Tier 4** | All remaining | Full coverage |

### Step 2: Translate Content

For each field, translate while respecting limits:

```python
def translate_field(text, source_lang, target_lang, char_limit):
    """
    Translate text and ensure it fits within character limit.
    """
    translated = ai_translate(text, source_lang, target_lang)

    if len(translated) > char_limit:
        # Shorten while preserving meaning
        translated = ai_shorten(translated, char_limit)

    return translated
```

### Step 3: Localize Keywords (Don't Just Translate!)

Keywords require **localization**, not just translation:

```markdown
Example: "photo editor" app

❌ Wrong (direct translation):
- German: "fotobearbeitung" (literal translation)

✅ Right (localized):
- German: "bildbearbeitung,fotos,bilder,bearbeiten,filter"
  (terms Germans actually search for)
```

Research local search behavior:
1. Check competitor keywords in that locale
2. Use local App Store search suggestions
3. Consider local spelling variations

### Step 4: Apply Translations

```
PATCH /v1/appInfoLocalizations/{localizationId}
{
  "data": {
    "type": "appInfoLocalizations",
    "id": "{localizationId}",
    "attributes": {
      "name": "Localized App Name",
      "subtitle": "Localized Subtitle"
    }
  }
}

PATCH /v1/appStoreVersionLocalizations/{localizationId}
{
  "data": {
    "type": "appStoreVersionLocalizations",
    "id": "{localizationId}",
    "attributes": {
      "keywords": "localized,keywords,here",
      "description": "Localized description...",
      "promotionalText": "Localized promo text"
    }
  }
}
```

### Step 5: Verify Translations

After applying:
1. Check character counts are within limits
2. Verify no encoding issues
3. Confirm keywords don't duplicate title/subtitle
4. Review for cultural appropriateness

---

## Workflow 4 — Cross-Localization Strategy

Apple indexes keywords from MULTIPLE locales per storefront. Use this to
effectively **double your keyword coverage**.

### Cross-Localization Map

| Storefront | Primary Locale | Secondary Locale(s) |
|------------|---------------|---------------------|
| USA | en-US | es-MX |
| UK | en-GB | en-US |
| Canada | en-CA | fr-CA, en-US |
| Australia | en-AU | en-US |
| Germany | de-DE | en-US |
| France | fr-FR | en-US |
| Japan | ja | en-US |
| Brazil | pt-BR | en-US |
| Mexico | es-MX | en-US |
| Spain | es-ES | en-US |
| China | zh-Hans | en-US |
| Taiwan | zh-Hant | en-US |

### Strategy Implementation

For the US App Store (indexes en-US + es-MX):

```markdown
## US Market — Cross-Localization

### en-US Keywords (100 chars)
"photo,editor,camera,filter,retouch,enhance,crop,adjust,collage"

### es-MX Keywords (100 chars) — ALSO indexed in US!
"fotos,editar,imagen,efectos,marcos,belleza,retrato,selfie,blur"

### Result: 18 unique keywords indexed for US users
(vs 9 if only using en-US)
```

### Rules for Cross-Localization

1. **No overlap** — Don't repeat keywords between paired locales
2. **Relevance first** — Both sets must be relevant to your app
3. **Language appropriate** — es-MX keywords work because US has Spanish speakers
4. **Monitor performance** — Track which locale's keywords perform better

### Generate Cross-Localization Plan

```markdown
## Cross-Localization Plan — {App Name}

### Target: US App Store
Primary: en-US | Secondary: es-MX

| en-US Keywords | es-MX Keywords |
|----------------|----------------|
| photo | fotos |
| editor | editar |
| camera | cámara |
| filter | filtros |
| enhance | mejorar |
| collage | collage ❌ (duplicate, remove) |
| retouch | retocar |
| beauty | belleza |
| portrait | retrato |

**Recommendation:** Replace "collage" in es-MX with unique term like "marcos"
```

See [locale-reference.md](references/locale-reference.md) for complete cross-indexing map.

---

## Workflow 5 — Bulk Update via API

Apply metadata changes programmatically.

### Prerequisites

- App Store Connect API key (Admin or App Manager role)
- JWT token generation
- App ID and version ID

### Step 1: Get Current Version

```
GET /v1/apps/{appId}/appStoreVersions?filter[appStoreState]=READY_FOR_SALE,PREPARE_FOR_SUBMISSION
```

### Step 2: List Existing Localizations

```
GET /v1/appStoreVersions/{versionId}/appStoreVersionLocalizations
```

### Step 3: Create Missing Localizations

```
POST /v1/appStoreVersionLocalizations
{
  "data": {
    "type": "appStoreVersionLocalizations",
    "attributes": {
      "locale": "de-DE",
      "keywords": "keywords,here",
      "description": "German description...",
      "promotionalText": "German promo",
      "whatsNew": "What's new in German"
    },
    "relationships": {
      "appStoreVersion": {
        "data": {
          "type": "appStoreVersions",
          "id": "{versionId}"
        }
      }
    }
  }
}
```

### Step 4: Update Existing Localizations

```
PATCH /v1/appStoreVersionLocalizations/{localizationId}
{
  "data": {
    "type": "appStoreVersionLocalizations",
    "id": "{localizationId}",
    "attributes": {
      "keywords": "updated,keywords",
      "description": "Updated description..."
    }
  }
}
```

### Step 5: Update App Info Localizations (Name/Subtitle)

```
PATCH /v1/appInfoLocalizations/{localizationId}
{
  "data": {
    "type": "appInfoLocalizations",
    "id": "{localizationId}",
    "attributes": {
      "name": "New App Name",
      "subtitle": "New Subtitle"
    }
  }
}
```

### Batch Update Script

```python
async def bulk_update_localizations(app_id, updates):
    """
    updates = {
        "de-DE": {"keywords": "...", "description": "..."},
        "fr-FR": {"keywords": "...", "description": "..."},
    }
    """
    version_id = await get_current_version(app_id)
    localizations = await get_localizations(version_id)

    for locale, changes in updates.items():
        loc_id = find_localization_id(localizations, locale)

        if loc_id:
            await patch_localization(loc_id, changes)
        else:
            await create_localization(version_id, locale, changes)

        # Rate limiting
        await asyncio.sleep(0.5)

    return {"updated": len(updates)}
```

---

## Workflow 6 — Competitor ASO Analysis

Analyze competitor metadata to identify opportunities.

### Step 1: Identify Competitors

```
GET https://itunes.apple.com/search?term={category}&media=software&limit=25
```

Or specify competitor app IDs directly.

### Step 2: Fetch Competitor Metadata

For each competitor, across key locales:

```python
locales = ["us", "gb", "de", "fr", "jp", "br"]

for competitor_id in competitors:
    for locale in locales:
        data = fetch_itunes_lookup(competitor_id, locale)
        store_metadata(competitor_id, locale, data)
```

### Step 3: Extract Keywords

From competitor metadata, extract likely keywords:

```python
def extract_keywords(app_data):
    keywords = set()

    # From title (remove brand name)
    title_words = app_data["trackName"].lower().split()
    keywords.update(title_words)

    # From description (top frequency words)
    desc_words = extract_top_words(app_data["description"], n=20)
    keywords.update(desc_words)

    # Filter stop words
    keywords = filter_stop_words(keywords)

    return keywords
```

### Step 4: Gap Analysis

```python
def find_keyword_gaps(your_keywords, competitor_keywords):
    """Find keywords competitors use that you don't."""
    gaps = competitor_keywords - your_keywords
    return sorted(gaps, key=lambda k: estimate_value(k), reverse=True)
```

### Step 5: Generate Competitive Report

```markdown
## Competitor ASO Analysis — {Category}

### Competitors Analyzed
1. Competitor A (id: 123456) — 4.8★, 50K ratings
2. Competitor B (id: 789012) — 4.6★, 30K ratings
3. Competitor C (id: 345678) — 4.5★, 25K ratings

### Keyword Coverage Comparison

| Keyword | You | Comp A | Comp B | Comp C | Opportunity |
|---------|-----|--------|--------|--------|-------------|
| photo editor | ✓ | ✓ | ✓ | ✓ | Low (saturated) |
| ai enhance | ✗ | ✓ | ✓ | ✗ | High |
| background remove | ✗ | ✓ | ✓ | ✓ | High |
| collage maker | ✓ | ✗ | ✓ | ✓ | Covered |
| beauty camera | ✗ | ✓ | ✗ | ✓ | Medium |

### Keyword Gaps (High Opportunity)
1. "ai enhance" — Used by 2/3 competitors, you're missing
2. "background remove" — Used by 3/3 competitors
3. "portrait mode" — Growing trend, 2/3 competitors

### Title/Subtitle Patterns
- 3/3 competitors include "Photo" in title
- 2/3 use "Pro" or "Plus" suffix
- All include primary feature in subtitle

### Recommendations
1. Add "ai enhance" to keywords — high competitor usage
2. Consider "background" variations in title/subtitle
3. Test "Pro" suffix for premium positioning
```

---

## Quick Reference — API Endpoints

| Task | Method | Endpoint |
|------|--------|----------|
| List app infos | GET | `/v1/apps/{id}/appInfos` |
| List app info localizations | GET | `/v1/appInfos/{id}/appInfoLocalizations` |
| Update app info localization | PATCH | `/v1/appInfoLocalizations/{id}` |
| List version localizations | GET | `/v1/appStoreVersions/{id}/appStoreVersionLocalizations` |
| Create version localization | POST | `/v1/appStoreVersionLocalizations` |
| Update version localization | PATCH | `/v1/appStoreVersionLocalizations/{id}` |
| Delete version localization | DELETE | `/v1/appStoreVersionLocalizations/{id}` |
| iTunes lookup | GET | `itunes.apple.com/lookup?id={id}&country={cc}` |
| iTunes search | GET | `itunes.apple.com/search?term={q}&media=software` |

---

## ASO Checklist

Before submitting metadata updates:

- [ ] All character limits respected
- [ ] No duplicate keywords across Title/Subtitle/Keywords
- [ ] No stop words in keywords field
- [ ] Keywords comma-separated without spaces
- [ ] Cross-localization strategy applied
- [ ] High-value markets localized
- [ ] Keywords localized (not just translated)
- [ ] No competitor brand names in keywords
- [ ] Description is conversion-optimized
- [ ] Promotional text ready (can update anytime)

---

## Reference Files

| File | Purpose |
|------|---------|
| [aso-best-practices.md](references/aso-best-practices.md) | Character limits, rules, optimization tips |
| [locale-reference.md](references/locale-reference.md) | All 38 locales with cross-indexing map |
| [api-endpoints.md](references/api-endpoints.md) | App Store Connect API details |
| [keyword-strategies.md](references/keyword-strategies.md) | Advanced keyword research techniques |
