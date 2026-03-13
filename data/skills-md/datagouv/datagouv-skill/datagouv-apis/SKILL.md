---
name: datagouv-apis
description: Interact with data.gouv.fr APIs — Main API (datasets, orgs, users, resources, reuses, discussions), Metrics API (usage/stats by model), Tabular API (query CSV rows by resource ID). Use when working with data.gouv.fr data, catalog, or platform features.
---

# data.gouv.fr APIs — Consolidated Reference

Three APIs: **Main** (catalog), **Metrics** (usage), **Tabular** (CSV rows). Prefer the data.gouv.fr MCP server tools when configured; endpoints below apply with or without MCP.

---

## 1. Main API

**Base URL:** `https://www.data.gouv.fr/api/1/` | Demo: `https://demo.data.gouv.fr/api/1/`

**Auth:** Read public. Write (POST/PUT/PATCH/DELETE): header `X-API-KEY`. Permissions = web (org member to edit org datasets). `private: true` for drafts. **IDs:** technical id or slug; prefer technical id. **Content:** JSON; file uploads: `multipart/form-data`. **Optional:** `X-Fields` to limit returned fields.

**Response:** Paginated lists: `data`, `page`, `page_size`, `total`, `next_page`, `previous_page`. Errors: 400, 401, 403, 404, 410, 423, 500, 502. Body: `{"message":"..."}`. Rate limits: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

### Datasets
| Method | Path |
|--------|------|
| GET | `/datasets/` — q, page, page_size, sort, organization, owner, tag, license, format, geozone, granularity, temporal_coverage, schema, topic, archived, deleted, private |
| POST | `/datasets/` — title, description, frequency, last_update, organization/owner, license, tags, private |
| GET/PUT/DELETE | `/datasets/{id}/` |
| GET | `/datasets/{id}/resources/` |
| POST | `/datasets/{id}/resources/` — create |
| PUT | `/datasets/{id}/resources/` — reorder (body: array) |
| GET/PUT/DELETE | `/datasets/{id}/resources/{rid}/` |
| POST | `/datasets/{id}/resources/{rid}/upload/` or `/datasets/{id}/upload/` |
| POST/DELETE | `/datasets/{id}/badges/`, `/datasets/{id}/badges/{badge_kind}/` |
| POST/DELETE | `/datasets/{id}/featured/` |
| GET/POST/DELETE | `/datasets/{id}/followers/` |
| GET | `/datasets/{id}/rdf`, `/datasets/{id}/rdf.{_format}` |
| GET/POST/... | `/datasets/community_resources/`, `.../{community}/`, `.../upload/` |
| GET | `/datasets/badges/`, `frequencies/`, `licenses/`, `resource_types/`, `extensions/`, `schemas/` |
| GET | `/datasets/suggest/`, `suggest/formats/`, `suggest/mime/` — q, size |
| GET | `/datasets/r/{id}` — redirect to latest resource |
| GET | `/datasets/recent.atom` |

### Organizations
| Method | Path |
|--------|------|
| GET/POST | `/organizations/` |
| GET/PUT/DELETE | `/organizations/{id}/` |
| POST/PUT/DELETE | `/organizations/{id}/member/{user}/` — role: admin|editor |
| GET/POST | `/organizations/{id}/membership/`, `.../accept/{id}/`, `.../refuse/{id}/` |
| GET | `/organizations/{id}/datasets/`, `reuses/`, `discussions/`, `contacts/`, `contacts/suggest/` |
| GET | `/organizations/{id}/datasets.csv`, `dataservices.csv`, `datasets-resources.csv`, `discussions.csv` |
| GET | `/organizations/{id}/catalog`, `catalog.{_format}` |
| GET/POST/DELETE | `/organizations/badges/`, `{id}/badges/`, `{id}/badges/{badge_kind}/` |
| POST/PUT | `/organizations/{id}/logo/` |
| GET | `/organizations/roles/`, `suggest/` |
| GET/POST/DELETE | `/organizations/{id}/followers/` |

### Users
| Method | Path |
|--------|------|
| GET/POST | `/users/` |
| GET/PUT/DELETE | `/users/{id}/` |
| POST | `/users/{id}/avatar/` |
| GET | `/users/{id}/contacts/` |
| GET | `/users/roles/`, `suggest/` |
| GET/POST/DELETE | `/users/{id}/followers/` |

### Me (authenticated)
| Method | Path |
|--------|------|
| GET/PUT/DELETE | `/me/` |
| DELETE/POST | `/me/apikey/` |
| POST | `/me/avatar/` |
| GET | `/me/datasets/`, `reuses/`, `metrics/`, `org_datasets/`, `org_reuses/`, `org_community_resources/`, `org_discussions/` |

### Reuses
| Method | Path |
|--------|------|
| GET/POST | `/reuses/` — q, organization, owner, tag, topic, type, dataset, featured |
| GET/PUT/DELETE | `/reuses/{id}/` |
| POST | `/reuses/{id}/datasets/`, `dataservices/` |
| GET/POST/DELETE | `/reuses/badges/`, `{id}/badges/`, `{id}/featured/` |
| POST | `/reuses/{id}/image/` |
| GET | `/reuses/topics/`, `types/`, `suggest/` |
| GET/POST/DELETE | `/reuses/{id}/followers/` |
| GET | `/reuses/recent.atom` |

### Dataservices (external APIs)
| Method | Path |
|--------|------|
| GET/POST | `/dataservices/` — GET: q, page, page_size, organization, owner, topic, tag, access_type, featured, dataset, sort |
| GET/PATCH/DELETE | `/dataservices/{id}/` — GET returns `base_api_url`, `machine_documentation_url` (OpenAPI/Swagger spec), title, description, organization, license, etc. |
| POST | `/dataservices/{id}/datasets/` — body: [{id}] |
| DELETE | `/dataservices/{id}/datasets/{dataset}/` |
| POST/DELETE | `/dataservices/{id}/featured/` |
| GET | `/dataservices/{id}/rdf`, `rdf.{_format}` |
| GET/POST/DELETE | `/dataservices/{id}/followers/` |
| GET | `/dataservices/recent.atom` |

**To use a dataservice:** (1) Search `/dataservices/?q=term` to find it. (2) GET `/dataservices/{id}/` to get `machine_documentation_url` and `base_api_url`. (3) Fetch `machine_documentation_url` to get OpenAPI spec with endpoints/params. (4) Make calls to `base_api_url` per spec.

### Contacts, Harvest, Discussions, Notifications
| Method | Path |
|--------|------|
| POST | `/contacts/` — name, email, role |
| GET | `/contacts/roles/` |
| GET/PUT/DELETE | `/contacts/{id}/` |
| GET/POST | `/harvest/sources/` |
| GET/PUT/DELETE | `/harvest/source/{id}/` |
| GET | `/harvest/source/{id}/jobs/`, `harvest/job/{ident}/` |
| POST | `/harvest/source/{id}/run/` |
| POST/DELETE | `/harvest/source/{id}/schedule/` |
| GET/POST | `/harvest/source/{id}/preview/`, `harvest/source/preview/` |
| POST | `/harvest/source/{id}/validate/` |
| GET | `/harvest/backends/` |
| GET/POST/PUT/DELETE | `/discussions/`, `discussions/{id}/` |
| POST | `/discussions/{id}/` — comment, close (body) |
| PUT/DELETE | `/discussions/{id}/comments/{idx}/` |
| DELETE | `/discussions/{id}/comments/{idx}/spam/`, `discussions/{id}/spam/` |
| GET | `/notifications/` |
| POST | `/notifications/{id}/read/` |

### Posts, Pages, Reports, Transfer, Activity, Site, Spatial, Tags
| Method | Path |
|--------|------|
| GET/POST | `/posts/` — name, content, body_type, kind, datasets, reuses |
| GET/PUT/DELETE | `/posts/{id}/` |
| POST/PUT | `/posts/{id}/image/` |
| POST/DELETE | `/posts/{id}/publish/` |
| GET | `/posts/recent.atom` |
| GET/POST | `/pages/` |
| GET/PUT | `/pages/{id}/` |
| GET/POST | `/reports/` — reason (explicit_content|illegal_content|others|personal_data|security|spam), subject, message |
| GET | `/reports/reasons/` |
| GET/PATCH | `/reports/{id}/` |
| GET/POST | `/transfer/`, `transfer/{id}/` — subject, recipient, comment; response: accept\|refuse |
| GET | `/activity/` — user, organization, related_to |
| GET/PATCH | `/site/` |
| GET | `/site/catalog`, `catalog.{_format}`, `context.jsonld`, `data.{_format}` |
| GET | `/site/datasets.csv`, `dataservices.csv`, `reuses.csv`, `organizations.csv`, `resources.csv`, `harvests.csv`, `tags.csv` |
| GET | `/access_type/reason_categories/` |
| GET | `/avatars/{identifier}/{size}/` |
| GET | `/spatial/granularities/`, `levels/`, `coverage/{level}/`, `zone/{id}/`, `zone/{id}/datasets/`, `zones/{ids}/`, `zones/suggest/` |
| GET | `/tags/suggest/` |
| GET | `/spam/` |
| GET | `/proconnect/auth`, `login/`, `logout`, `logout_oauth` |
| GET/POST | `/workers/jobs/` |
| GET/PUT/DELETE | `/workers/jobs/{id}/` |
| GET | `/workers/jobs/schedulables/`, `workers/tasks/{id}/` |

---

## 2. Metrics API

**Base URL:** `https://metric-api.data.gouv.fr` | Swagger: https://metric-api.data.gouv.fr/api/doc

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/{model}/data/` | Paginated metrics (JSON). Params: page, page_size, column__sort, column__exact, column__contains, column__less, column__greater |
| GET | `/api/{model}/data/csv/` | Same as CSV stream (no pagination) |
| GET | `/health/` | Health check |

`{model}` = table name (e.g. site, organization, dataset). See Swagger for models and columns.

---

## 3. Tabular API

**Base URL:** `https://tabular-api.data.gouv.fr` | Swagger: https://tabular-api.data.gouv.fr/api/doc | Per-resource: `GET /api/resources/{rid}/swagger/`

`{rid}` = resource UUID from main API (dataset's resources).

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/resources/{rid}/` | Metadata, links to profile/data/swagger |
| GET | `/api/resources/{rid}/profile/` | Column types, formats, stats, indexes |
| GET | `/api/resources/{rid}/swagger/` | OpenAPI for data endpoint (columns, operators) |
| GET | `/api/aggregation-exceptions/` | Resource UUIDs allowed for aggregation |
| GET | `/api/resources/{rid}/data/` | Filter, sort, paginate (page, page_size max 50) |
| GET | `/api/resources/{rid}/data/csv/` | Stream CSV |
| GET | `/api/resources/{rid}/data/json/` | Stream JSON |
| GET | `/health/` | Health check |

**Data params:** `columns=col1,col2` | Filter: `column__exact`, `__differs`, `__isnull`, `__isnotnull`, `__contains`, `__notcontains`, `__in`, `__notin`, `__less`, `__greater`, `__strictly_less`, `__strictly_greater` | Sort: `column__sort=asc|desc` | Aggregation (allowed resources, indexed cols): `column__groupby`, `__count`, `__avg`, `__min`, `__max`, `__sum`. JSON columns: only isnull/isnotnull.

---

## Quick Examples

```python
# Main API — search datasets
requests.get("https://www.data.gouv.fr/api/1/datasets/", params={"q": "transport", "page_size": 20}).json()

# Metrics API
requests.get("https://metric-api.data.gouv.fr/api/dataset/data/", params={"page": 1}).json()

# Tabular API — resource data
requests.get(f"https://tabular-api.data.gouv.fr/api/resources/{resource_id}/data/", params={"page": 1, "page_size": 20}).json()
```

**Python client:** https://github.com/etalab/datagouv-client-python  
**Main API Swagger:** https://www.data.gouv.fr/api/1/swagger.json  
**Guides:** https://guides.data.gouv.fr/guide-data.gouv.fr/readme-1/reference/
