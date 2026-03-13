---
name: google-ads-editor
description: Insert campaigns, ad groups, keywords, and RSA ads directly into Google Ads Editor's local SQLite database. Bypass CSV import workflow.
group: marketing
---

# Google Ads Editor Database Skill

Insert campaigns directly into Google Ads Editor's local SQLite database without CSV import.

## Database Location

```
~/Library/Application Support/Google/Google-AdWords-Editor/724/ape_4295165693.db
```

**Note:** The account ID (`4295165693`) may vary. Find the correct one:
```bash
ls ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_*.db
```

## Key Tables

| Table | Purpose | Parent Relationship |
|-------|---------|---------------------|
| Campaign | Campaigns | None |
| AdGroup | Ad groups | parentId = 2^33 + Campaign.localId |
| Keyword | Keywords | parentId = 2^34 + AdGroup.localId |
| ResponsiveSearchAd | RSA ads | parentId = 2^34 + AdGroup.localId |

## ID Encoding Formula

```python
# Campaign → AdGroup relationship
adgroup_parent_id = (2**33) + campaign_local_id  # 8589934592 + local_id

# AdGroup → Keyword/RSA relationship
keyword_parent_id = (2**34) + adgroup_local_id   # 17179869184 + local_id
```

## Field Value Reference

### Status Values
- `0` = Paused
- `1` = Enabled

### State Values
- `0` = Synced from server
- `1` = New/pending upload

### Keyword Match Types (criterionType)
- `0` = Broad match
- `1` = Phrase match
- `2` = Exact match

### Money Values
All monetary values in **micros** (1 dollar = 1,000,000 micros):
```python
def dollars_to_micros(dollars: float) -> int:
    return int(dollars * 1_000_000)

# Examples:
# $2.00 = 2000000
# $0.50 = 500000
```

### Bidding Strategy Types
- `1` = Manual CPC
- `9` = Target CPA
- `12` = Maximize Conversions

### Campaign Types
- `0` = Search
- `2` = Display
- `3` = Shopping

## URL Blob Encoding

finalUrls field uses a custom blob format:

```python
import struct

def encode_urls_blob(urls: list[str]) -> bytes:
    """Encode URLs list to Google Ads Editor blob format."""
    if not urls:
        return b'\x00\x00\x00\x00'

    result = struct.pack('<I', len(urls))  # URL count (little-endian uint32)

    for url in urls:
        url_bytes = url.encode('utf-16-le')
        char_count = len(url)
        result += struct.pack('<I', char_count)  # Character count
        result += url_bytes

    return result
```

## Quick Insert Examples

### Insert Campaign
```sql
INSERT INTO Campaign (localId, state, name, status, campaignType, biddingStrategyType)
VALUES (
    (SELECT COALESCE(MAX(localId), 0) + 1 FROM Campaign),
    1,  -- state: new
    'My Campaign',
    1,  -- status: enabled
    0,  -- campaignType: search
    1   -- biddingStrategyType: manual CPC
);
```

### Insert Ad Group
```sql
-- First get the campaign localId
INSERT INTO AdGroup (localId, parentId, state, name, status, maxCpc)
VALUES (
    (SELECT COALESCE(MAX(localId), 0) + 1 FROM AdGroup),
    8589934592 + [CAMPAIGN_LOCAL_ID],  -- parentId encoding
    1,  -- state: new
    'My Ad Group',
    1,  -- status: enabled
    2000000  -- maxCpc: $2.00
);
```

### Insert Keyword
```sql
INSERT INTO Keyword (localId, parentId, state, text, criterionType, status, maxCpc, finalUrls)
VALUES (
    (SELECT COALESCE(MAX(localId), 0) + 1 FROM Keyword),
    17179869184 + [ADGROUP_LOCAL_ID],  -- parentId encoding
    1,  -- state: new
    'my keyword',
    2,  -- criterionType: exact match
    1,  -- status: enabled
    2000000,  -- maxCpc: $2.00
    X'...'  -- encoded URL blob
);
```

## Python Helper Script

Full script available at:
```
/Users/avysotsky/Projects/vood/vibe-business/scripts/google_ads_db_insert.py
```

### Usage

```bash
# Close Google Ads Editor first!
python3 /Users/avysotsky/Projects/vood/vibe-business/scripts/google_ads_db_insert.py
```

### Import and Use Programmatically

```python
from scripts.google_ads_db_insert import GoogleAdsDBInserter, dollars_to_micros

with GoogleAdsDBInserter() as db:
    # Create campaign
    campaign_id = db.insert_campaign(
        name="My Campaign",
        status=1,
        campaign_type=0,
        bidding_strategy_type=1,
    )

    # Create ad group
    ag_id = db.insert_ad_group(
        campaign_local_id=campaign_id,
        name="My Ad Group",
        max_cpc=2.00,  # dollars
    )

    # Add keyword
    db.insert_keyword(
        ad_group_local_id=ag_id,
        text="my keyword",
        criterion_type=2,  # exact
        max_cpc=2.00,
        final_url="https://example.com?utm_source=google",
    )

    # Add RSA
    db.insert_responsive_search_ad(
        ad_group_local_id=ag_id,
        headlines=["Headline 1", "Headline 2", ...],  # up to 15
        descriptions=["Description 1", ...],  # up to 4
        final_url="https://example.com",
        path1="path1",
        path2="path2",
    )
```

## Important Notes

1. **Close Google Ads Editor** before running database inserts
2. **Backup the database** before making changes:
   ```bash
   cp ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db \
      ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db.backup
   ```
3. After inserting, open Google Ads Editor - new items appear with "pending" state
4. Click "Post" to upload changes to Google Ads

## Viewing Database

```bash
# List all campaigns
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db \
  "SELECT localId, name, status FROM Campaign"

# List all ad groups
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db \
  "SELECT localId, name, status, maxCpc FROM AdGroup"

# List all keywords
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db \
  "SELECT localId, text, criterionType, maxCpc FROM Keyword LIMIT 20"
```

## Schema Reference

Full schema can be viewed with:
```bash
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db ".schema Campaign"
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db ".schema AdGroup"
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db ".schema Keyword"
sqlite3 ~/Library/Application\ Support/Google/Google-AdWords-Editor/724/ape_4295165693.db ".schema ResponsiveSearchAd"
```
