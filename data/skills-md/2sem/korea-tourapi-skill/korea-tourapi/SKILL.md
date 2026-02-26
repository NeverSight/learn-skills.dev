---
name: korea-tourapi
description: Expert workflow for Korea Tourism Organization TourAPI. Builds valid requests, validates parameters, handles pagination/errors, and maps responses to app models.
---

# Korea TourAPI Skill

Use this skill when implementing or debugging integrations with Korea Tourism Organization TourAPI 4.0 KorService2.

## Source of Truth

- API family: `KorService2`
- Base URL: `https://apis.data.go.kr/B551011/KorService2`
- Manual version: TourAPI 4.0 Ver 4.3 (2025-05-12)
- Core endpoints covered:
  - `areaCode2`, `categoryCode2`, `areaBasedList2`, `locationBasedList2`
  - `searchKeyword2`, `searchFestival2`, `searchStay2`
  - `detailCommon2`, `detailIntro2`, `detailInfo2`, `detailImage2`
  - `areaBasedSyncList2`, `detailPetTour2`, `ldongCode2`, `lclsSystmCode2`

## When to Use

- Building new list/detail/taxonomy API calls.
- Migrating old TourAPI params to latest Ver 4.3 behavior.
- Troubleshooting request validation errors and no-data cases.
- Designing model mapping for `contentid`, `contenttypeid`, coordinates, image fields.
- Adding sync jobs from `areaBasedSyncList2`.

## Required Request Baseline

For every request, enforce these baseline params first:

1. `serviceKey`
2. `MobileOS` (`IOS`, `AND`, `WEB`, `ETC`)
3. `MobileApp` (service name)
4. `_type=json` (unless XML is explicitly required)

Then add endpoint-specific required params.

## Operating Procedure

1. Identify user intent: list, detail, codes, sync, pet travel.
2. Select endpoint by intent (see `references/quick-reference.md`).
3. Build request with required params and only compatible optional filters.
4. Validate dependency params before call:
   - `sigunguCode` requires `areaCode`
   - `cat2` requires `cat1`
   - `cat3` requires `cat1` and `cat2`
   - `lDongSignguCd` requires `lDongRegnCd`
   - `lclsSystm2` requires `lclsSystm1`
   - `lclsSystm3` requires `lclsSystm1` and `lclsSystm2`
5. For location queries, clamp `radius` to `<= 20000`.
6. Parse `response.header` first:
   - success expected: `resultCode == "0000"`
   - else map to actionable error
7. Parse `response.body.items.item` robustly (single object or array).
8. Return normalized fields and pagination (`pageNo`, `numOfRows`, `totalCount`).
9. If detail flow is needed, chain:
   - `detailCommon2` -> `detailIntro2` -> `detailInfo2` -> `detailImage2`
10. Respect licensing metadata (`cpyrhtDivCd`) in downstream usage.

## Request/Response Validation Feature (Mandatory)

Before implementation guidance, run two explicit checks and report both:

1. Request validation
2. Response validation

### 1) Request validation

- Validate baseline params: `serviceKey`, `MobileOS`, `MobileApp`, `_type`.
- Validate endpoint required params from `references/validation-matrix.md`.
- Validate dependency params (`cat2`/`cat3`, `sigunguCode`, legal-dong, classification-system).
- Validate removed params denylist:
  - `defaultYN`, `firstImageYN`, `areacodeYN`, `catcodeYN`, `addrinfoYN`, `mapinfoYN`, `overviewYN`, `subImageYN`
- If any invalid param exists, block request construction and output a corrected param set.

### 2) Response validation

- Accept success only when `resultCode == "0000"`.
- Validate envelope shape:
  - list/detail endpoints: `response.header`, `response.body`, `response.body.items.item`
  - provider error shape: `resultCode`/`resultMsg` top-level may appear
- Validate pagination fields when present: `pageNo`, `numOfRows`, `totalCount`.
- Validate endpoint-specific minimum fields from `references/validation-matrix.md`.
- If required response fields are missing, return a parsing warning and safe fallback mapping.

## Content Type IDs (Kor)

- 12: Tour spot
- 14: Culture facility
- 15: Festival/performance/event
- 25: Travel course
- 28: Leports
- 32: Stay
- 38: Shopping
- 39: Food

## Response-Safe Parsing Rules

- Parse numeric fields from strings (`contentid`, `mapx`, `mapy`, `dist`) safely.
- Treat missing optional values as null/empty, not errors.
- Keep raw source payload for debugging.
- Keep a strict distinction between:
  - transport errors (HTTP/network)
  - platform errors (`OpenAPI_ServiceResponse`)
  - provider errors (`resultCode` in response header)

## Known 4.3 Notes

- New filters/fields include legal-dong and classification-system values.
- Some older flags were removed from older endpoint revisions.
- `detailCommon2` is simplified compared with prior revisions.

## Hard Guardrails (Prevent Invalid Params)

Never send removed legacy flags to `detailCommon2`:

- `defaultYN`
- `firstImageYN`
- `areacodeYN`
- `catcodeYN`
- `addrinfoYN`
- `mapinfoYN`
- `overviewYN`

If any of the above appears in generated code, remove it before request execution.

`detailCommon2` request should be treated as:

- baseline params: `serviceKey`, `MobileOS`, `MobileApp`, `_type`
- required params: `contentId`
- optional paging only: `numOfRows`, `pageNo`

Also do not use deprecated `subImageYN` on `detailImage2`.

## Output Contract for Agent

When this skill is used, always output:

1. Selected endpoint and reason.
2. Final request URL (redact or mask `serviceKey`).
3. Required/optional params split.
4. Validation checks run.
   - Request validation result (pass/fail + fixes)
   - Response validation result (pass/warn/fail)
5. Pagination handling plan.
6. Error handling mapping.
7. Model mapping notes for app code.

## Local References

- `references/quick-reference.md`
- `references/validation-matrix.md`
- `references/wherewego-mapping.md`
- `docs/FEATURE_PLAN.md`
