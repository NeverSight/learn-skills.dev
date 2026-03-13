---
name: hk-open-data
description: Use when working with Hong Kong Open Data API (DATA.GOV.HK), fetching datasets, filtering data, querying historical archives, finding nearest facilities, or building applications that consume HK government open data
---

# Hong Kong Open Data API

**Official Documentation:** https://data.gov.hk/en/help/api-spec

## Overview

DATA.GOV.HK provides multiple APIs for accessing government open data. All APIs use GMT+8 timezone.

**API Types:**
1. **CKAN API** - Dataset discovery and metadata
2. **Data Filtering API** - Query and filter dataset resources
3. **Historical Archive API** - Access historical versions
4. **Nearest Facilities API** - Location-based queries

## Language Endpoints

All CKAN APIs have language-specific endpoints:

| Language | Endpoint Pattern |
|----------|-------------------|
| English | `https://data.gov.hk/en-data/api/3/action/...` |
| Traditional Chinese | `https://data.gov.hk/tc-data/api/3/action/...` |
| Simplified Chinese | `https://data.gov.hk/sc-data/api/3/action/...` |

**CRITICAL:** Always choose the correct language endpoint for your users.

## CKAN API (Dataset Discovery)

### List All Datasets

```python
import requests

# Get all dataset IDs (English)
response = requests.get("https://data.gov.hk/en-data/api/3/action/package_list")
datasets = response.json()["result"]
```

**Parameters:** `limit` (int, optional), `offset` (int, optional)

```python
# Get first 10 datasets with pagination
response = requests.get(
    "https://data.gov.hk/en-data/api/3/action/package_list",
    params={"limit": 10, "offset": 0}
)
```

### Get Dataset Metadata

```python
# Get details of a specific dataset
dataset_id = "hk-td-tis_2-traffic-snapshot-images"
response = requests.get(
    "https://data.gov.hk/en-data/api/3/action/package_show",
    params={"id": dataset_id}
)
metadata = response.json()["result"]
resources = metadata["resources"]  # List of data files/URLs
```

### List Data Categories

```python
response = requests.get("https://data.gov.hk/en-data/api/3/action/group_list")
categories = response.json()["result"]
# Returns: ["city-management", "transport", "health", ...]
```

### Get Datasets by Category

```python
category_id = "transport"  # Use category ID from group_list
response = requests.get(
    "https://data.gov.hk/en-data/api/3/action/group_show",
    params={"id": category_id}
)
datasets = response.json()["result"]["packages"]
```

**Category IDs:** `city-management`, `climate-and-weather`, `commerce-and-industry`, `social-welfare`, `development`, `education`, `legislature`, `employment-and-labour`, `environment`, `finance`, `food`, `health`, `housing`, `law-and-security`, `population`, `recreation-and-culture`, `information-technology-and-broadcasting`, `tourism`, `transport`, `miscellaneous`

## Data Filtering API

**CRITICAL:** Use **v2** endpoint, not v1.

**Endpoint:** `https://api.data.gov.hk/v2/filter`

**Method:** GET with URL-encoded JSON query parameter

### Query Structure

**Columns are 1-indexed** (not 0-indexed).

```python
import requests
import urllib.parse
import json

query = {
    "resource": "http://www.cr.gov.hk/datagovhk/psi/ml_licensees.csv",
    "section": 1,  # Required if dataset has sections (default: 1)
    "format": "json",  # Options: csv (default), json, xml
    "filters": [
        [1, "eq", ["3983"]],        # Column 1 equals "3983"
        [2, "nct", ["2021"]],       # Column 2 does not contain "2021"
        [3, "gt", ["100"]]          # Column 3 greater than 100
    ],
    "sorts": [
        [4, "asc"],   # Sort column 4 ascending
        [7, "desc"]   # Then column 7 descending
    ]
}

# URL encode the JSON query
url = f"https://api.data.gov.hk/v2/filter?q={urllib.parse.quote(json.dumps(query))}"
response = requests.get(url)
data = response.json()
```

### Filter Operators

**Text Only:**
- `eq` - equals (1 operand)
- `ne` - not equals (1 operand)
- `in` - is in (2+ operands)
- `ni` - is not in (2+ operands)
- `ct` - contains (1 operand)
- `nct` - does not contain (1 operand)
- `bw` - begins with (1 operand)
- `nbw` - does not begin with (1 operand)
- `ew` - ends with (1 operand)
- `new` - does not end with (1 operand)

**Number Only:**
- `lt` - less than (1 operand)
- `le` - less than or equal (1 operand)
- `gt` - greater than (1 operand)
- `ge` - greater than or equal (1 operand)
- `bt` - between (2 operands)

**Example - Multiple Values with "in":**

```python
query = {
    "resource": "...",
    "filters": [
        [2, "in", ["Kowloon", "Hong Kong Island", "New Territories"]]
    ]
}
```

**Example - Range with "bt":**

```python
query = {
    "resource": "...",
    "filters": [
        [5, "bt", ["100", "500"]]  # Column 5 between 100 and 500
    ]
}
```

**CRITICAL:** Always include `"section": 1` if the dataset has multiple sections. Check the dataset page or metadata to confirm.

## Historical Archive API

**Endpoint:** `https://app.data.gov.hk/v1/historical-archive/...`

**Note:** Latest historical data is from **yesterday** (not today).

### List Historical Files

```python
response = requests.get(
    "https://app.data.gov.hk/v1/historical-archive/list-files",
    params={
        "start": "20230101",  # YYYYMMDD
        "end": "20231231",    # YYYYMMDD
        "category": "climate-and-weather",  # Optional
        "provider": "hk-hko",  # Optional
        "format": "csv",  # Optional: file extension
        "search": "temperature",  # Optional: keyword
        "order": "url",  # Optional: dataset-en, dataset-tc, resource-en, etc.
        "skip": 0  # Optional: pagination offset
    }
)
files = response.json()["result"]
```

### List File Versions

```python
response = requests.get(
    "https://app.data.gov.hk/v1/historical-archive/list-file-versions",
    params={
        "url": "http://www.cr.gov.hk/datagovhk/psi/ml_licensees.csv",
        "start": "20230101",
        "end": "20231231"
    }
)
versions = response.json()["result"]
# Note: Maximum 10,000 results returned
```

### Download Historical File

```python
response = requests.get(
    "https://app.data.gov.hk/v1/historical-archive/get-file",
    params={
        "url": "http://www.cr.gov.hk/datagovhk/psi/ml_licensees.csv",
        "time": "202301011230"  # YYYYMMDDHHmm
    }
)
# Response: 302 redirect to file download
# Follow redirect to get file content
```

### Download Schema or Data Dictionary

```python
# Schema
response = requests.get(
    "https://app.data.gov.hk/v1/historical-archive/get-schema",
    params={
        "url": "DATASET_URL",  # Dataset URL, not resource URL
        "date": "20230101"
    }
)

# Data Dictionary
response = requests.get(
    "https://app.data.gov.hk/v1/historical-archive/get-data-dictionary",
    params={
        "url": "DATASET_URL",
        "date": "20230101"
    }
)
```

## Nearest Facilities API

**Endpoint:** `https://api.data.gov.hk/v1/nearest-schools`

```python
response = requests.get(
    "https://api.data.gov.hk/v1/nearest-schools",
    params={
        "lat": 22.2812,  # WGS84 latitude
        "long": 114.1659,  # WGS84 longitude
        "max": 5  # Max results (optional, default: all, limit: 100)
    }
)
schools = response.json()["results"]
# Results ordered by distance ascending
```

**Related Dataset:** School Location and Information

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using v1 Filtering API | Use `https://api.data.gov.hk/v2/filter` |
| 0-indexed columns | Columns are **1-indexed** |
| Missing `section` parameter | If dataset has sections, always include `"section": 1` |
| Wrong language endpoint | Use `en-data` for English, `tc-data` for Traditional Chinese, `sc-data` for Simplified Chinese |
| Quering today's historical data | Historical data available starting from **yesterday** |
| Not following redirects | Historical file download returns **302 redirect** - follow it |
| String values for all filter operands | Convert numbers to strings: `"100"` not `100` |
| Forgetting URL encoding | Always `urllib.parse.quote(json.dumps(query))` |
| Exceeding 10,000 result limit | Historical File Version API limits to 10,000 results |

## Workflow: Getting Started

1. **Discover datasets** using CKAN `package_list` or `group_show`
2. **Get metadata** using `package_show` to find resource URLs
3. **Query data** using v2 Filtering API with proper filters and sections
4. **For historical data** use Historical Archive APIs

## Error Handling

```python
# Filtering API returns HTTP 200 with JSON
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    # Error details in JSON
    error = response.json()
    print(error.get("error", {}).get("message", "Unknown error"))

# Historical Archive API
# 200 - Success
# 302 - Redirect (for file downloads)
# 400 - Syntax error (check required parameters)
# 404 - File not available (for historical versions)
```

## Provider IDs (Common)

| Provider ID | Name |
|--------------|------|
| `hk-dpo` | Digital Policy Office |
| `hk-hko` | Hong Kong Observatory |
| `hk-td` | Transport Department |
| `hk-fehd` | Food and Environmental Hygiene Department |
| `mtr` | MTR Corporation Limited |
| `hospital` | Hospital Authority |

**Full provider list:** 90+ providers available in API documentation.

## Quick Reference

| Task | API | Endpoint |
|------|-----|-----------|
| List all datasets | CKAN | `/api/3/action/package_list` |
| Get dataset metadata | CKAN | `/api/3/action/package_show?id=...` |
| List categories | CKAN | `/api/3/action/group_list` |
| Get datasets by category | CKAN | `/api/3/action/group_show?id=...` |
| Filter/query data | Filtering | `https://api.data.gov.hk/v2/filter?q=...` |
| List historical files | Archive | `/v1/historical-archive/list-files?...` |
| Get file versions | Archive | `/v1/historical-archive/list-file-versions?...` |
| Download historical file | Archive | `/v1/historical-archive/get-file?...` |
| Find nearest schools | Facilities | `/v1/nearest-schools?lat=...&long=...` |

## Real-World Example: Traffic Data

```python
import requests
import urllib.parse
import json

# Step 1: Discover traffic datasets
response = requests.get(
    "https://data.gov.hk/en-data/api/3/action/group_show",
    params={"id": "transport"}
)
datasets = response.json()["result"]["packages"]

# Step 2: Get specific dataset metadata
dataset_id = "hk-td-tis_2-traffic-snapshot-images"
response = requests.get(
    "https://data.gov.hk/en-data/api/3/action/package_show",
    params={"id": dataset_id}
)
resources = response.json()["result"]["resources"]
resource_url = resources[0]["url"]

# Step 3: Filter the data
query = {
    "resource": resource_url,
    "section": 1,
    "format": "json",
    "filters": [
        [1, "eq", ["HIGHWAY"]],
        [5, "gt", ["2024-01-01"]]
    ],
    "sorts": [[3, "desc"]]
}

url = f"https://api.data.gov.hk/v2/filter?q={urllib.parse.quote(json.dumps(query))}"
response = requests.get(url)
traffic_data = response.json()
```