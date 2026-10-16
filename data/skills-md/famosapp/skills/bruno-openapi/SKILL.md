---
name: bruno-openapi
description: |
  Design and maintain OpenAPI 3.1 contracts and Git-friendly Bruno collections:
  human REST docs, bru import openapi, .bru endpoints, auth/scripts/tests,
  codegen, Scalar/Redocly preview, and CI regression.

  Trigger when the user asks for OpenAPI, API contracts, REST documentation,
  Bruno collections, generate bruno, import Postman/curl, Bruno CI, Scalar,
  Redoc, or SDK/app codegen from OpenAPI.

  Keywords: OpenAPI, OAS 3.1, OAS 3.2, Bruno, .bru, collection, operationId,
  $ref, codegen, Spectral, Scalar, Redoc, bru import, OpenCollection,
  envelope, sandbox=developer, sync contract, writeOnly
version: 1.2.0
license: Apache-2.0
metadata:
  author: famosapp
  stack: openapi-3.1, bruno-cli, optional-spectral, optional-sdk-gen, optional-scalar-redocly
  related_skills: team-orch, make-it-clear, database-design
  primary_outputs: openapi.yaml | bruno-collection/ | generated-app | test-report | api-docs
  sources_synthesized: openapi-spec-generation, openapi-to-application-code, bruno-collection-generator, bruno-endpoint-creation, api-test-bruno, production-bruno-openapi-conventions
---

# Bruno + OpenAPI

Contract and collection discipline for HTTP APIs. **Non-negotiables override
framework fashion.** Prefer OpenAPI as the contract **and public REST docs**
SoT; Bruno as the Git-friendly executable twin.

**Announce when activating:** "Using the bruno-openapi skill."

## When to load which reference

| Need | Read |
|------|------|
| Hard bans | [non-negotiable.md](references/non-negotiable.md) |
| Pick a mode | [modes.md](references/modes.md) |
| Write / evolve OpenAPI 3.1 | [openapi-spec.md](references/openapi-spec.md) |
| Human REST docs / portal | [api-docs.md](references/api-docs.md) |
| Path prefixes, envelopes, writeOnly | [openapi-conventions.md](references/openapi-conventions.md) |
| Code-first, lint, SDK tooling | [openapi-tooling.md](references/openapi-tooling.md) |
| Bruno collection layout / generate | [bruno-collections.md](references/bruno-collections.md) |
| Verb gold patterns (CRUD/action/neg) | [bruno-patterns.md](references/bruno-patterns.md) |
| Single .bru auth / body / params | [bruno-requests.md](references/bruno-requests.md) |
| docs / assert / tests rules | [bruno-docs-assert.md](references/bruno-docs-assert.md) |
| `scripts/api.js` helpers + chaining | [bruno-helpers.md](references/bruno-helpers.md) |
| Scripts, test layers (smoke…) | [bruno-scripts-tests.md](references/bruno-scripts-tests.md) |
| Route ↔ Bruno ↔ OAS sync | [sync-contract.md](references/sync-contract.md) |
| Import curl/Postman/etc. | [source-import.md](references/source-import.md) |
| OpenAPI → application code | [codegen.md](references/codegen.md) |
| CI, reports, smoke vs full | [testing-ci.md](references/testing-ci.md) |
| Headless / capture failures | [troubleshooting.md](references/troubleshooting.md) |
| Types / layouts | [types-and-layouts.md](references/types-and-layouts.md) |
| Pitfalls | [gotchas.md](references/gotchas.md) |
| DO / DON'T | [do-dont.md](references/do-dont.md) |
| Recipes | [examples.md](references/examples.md) |
| Review checklist | [review-checklist.md](references/review-checklist.md) |

---

## Core rules

1. **Contract first when shaping a new API** — design-first OpenAPI (or hybrid) before sprawling handlers; code-first only to catch up existing code.
2. **Dual SoT, no drift** — OpenAPI = declarative contract; Bruno = executable mirror. Same PR updates both ([sync-contract.md](references/sync-contract.md)).
3. **Git-friendly Bruno** — plain-text `.bru` + `bruno.json` + `collection.bru` + `scripts/api.js`; secrets only via `vars:secret` / CI.
4. **Envelopes** — document and assert success/pagination/error envelopes; never leak write-only secrets in responses.
5. **`$ref` + operationId + tags** — reuse components; stable ids; tag by domain.
6. **Verb patterns** — CREATE/LIST/GET/UPDATE/DELETE/ACTION/NEGATIVE follow gold templates ([bruno-patterns.md](references/bruno-patterns.md)).
7. **Every `.bru`**: `assert {}` + `tests {}` + `docs {}` ([bruno-docs-assert.md](references/bruno-docs-assert.md)).
8. **Chain via capture** — `api.capture` / `captureFirstItem`; sentinel `vars:pre-request` for path UUIDs.
9. **Auth inherit** — collection Bearer; health + login/refresh override `auth: none`.
10. **Headless** — `bru run --env Local --sandbox=developer` (required for `require()`).
11. **Risk-ordered tests** — smoke → contract → business → negative; P0 fails CI.
12. **Mode by ask** — don’t full-codegen for one request ([modes.md](references/modes.md)).
13. **Human REST docs** — OpenAPI `info`/`tags`/`operations` are the public docs; Bruno `docs {}` + collection README are the executable twin. Same PR, no contradictions ([api-docs.md](references/api-docs.md)).

---

## Non-negotiable

Full: [non-negotiable.md](references/non-negotiable.md).

| Rule | Requirement |
|------|-------------|
| OpenAPI version | Prefer **3.1.x** for new specs; **3.2.0** only when tooling/repo already supports it |
| Human docs | Public ops have summary + description + examples; Bruno `docs {}` aligned; no second path catalog |
| Secrets | Never commit tokens/keys; `writeOnly` credentials omitted from response schemas |
| Sync | Route change ⇒ matching `.bru` + OAS in the **same PR** |
| Envelopes | Success / paginated / error shapes documented and asserted |
| Auth | `securitySchemes` + per-op `security`; Bruno collection auth + inherit |
| Bruno triad | Every request: `assert` + `tests` + `docs` |
| Capture | Prefer shared `scripts/api.js` helpers over ad-hoc `setEnvVar` |
| Path vars | Sentinel in `vars:pre-request` for every URL `{{uuid}}` |
| Sandbox | Headless `require()` needs `--sandbox=developer` |
| Codegen | Validate OAS first; follow target framework conventions |

---

## Gotchas

Summary — [gotchas.md](references/gotchas.md).

- Spec without examples/errors/envelopes; `"string"` placeholders; empty `info.description`.
- `bru import openapi` without `--collection-format=bru` (CLI defaults to OpenCollection YAML).
- Mixing `.bru` and `.yml` requests in one collection.
- Committing tokens; asserting secret fields in responses.
- Missing `--sandbox=developer` → `require is not defined`.
- Undefined `{{uuid}}` without sentinel → Bruno parse errors.
- Delete clobbering a chain UUID still needed downstream.
- Route added without `.bru` / OAS (drift).
- `setEnvVar` spaghetti instead of `api.capture`.
- Full suite on every PR; Postman JSON as eternal SoT.

---

## Types (“Data Types”)

| Kind | Values / shape |
|------|----------------|
| Mode | `openapi_design` · `openapi_from_code` · `bruno_generate` · `bruno_endpoint` · `bruno_test_plan` · `import_sources` · `codegen_app` · `docs_portal` |
| OAS version | `3.1.x` (preferred) · `3.2.0` (when tooling supports) · `3.0.x` (legacy) |
| Approach | `design-first` · `code-first` · `hybrid` |
| Auth | `none` · `bearer` · `basic` · `apikey` · `oauth2` · `inherit` |
| HTTP method | `get` · `post` · `put` · `patch` · `delete` · `head` · `options` |
| Test layer | `smoke` · `contract` · `business` · `negative` |
| Case status | `pass` · `fail` · `skip` |
| Source format | `openapi` · `curl` · `postman` · `insomnia` · `bruno` · `opencollection` · `wsdl` · `zip` |
| Env name | `Local` / `Development` · `Staging` · `Production` |

Details: [types-and-layouts.md](references/types-and-layouts.md).

---

## Layouts (“Tables / Columns”)

### OpenAPI top-level

| Field | Role |
|-------|------|
| `openapi` / `info` / `servers` | Identity + hosts |
| `tags` / `paths` | Operations |
| `components.schemas` | Models |
| `components.parameters` / `responses` / `examples` | Reuse |
| `components.securitySchemes` | Auth |

### Bruno collection layout

```
collection/
├── bruno.json
├── collection.bru          # optional collection auth
├── environments/
│   ├── Local.bru
│   ├── Staging.bru
│   └── Production.bru
├── auth/
│   ├── folder.bru
│   └── login.bru
└── <resource>/
    ├── folder.bru
    ├── list.bru
    ├── get-by-id.bru
    ├── create.bru
    ├── update.bru
    └── delete.bru
```

### .bru section columns

| Block | Purpose |
|-------|---------|
| `meta` | name, type, seq |
| `get`/`post`/… | url, body, auth |
| `auth:*` / `headers` / `query` / `params:*` | request shape |
| `body:json` | payload |
| `script:pre-request` / `script:post-response` | automation |
| `tests` | assertions |
| `docs` | human docs |

### Report row columns

`run_id` · `tool` · `env` · `case_id` · `method` · `path` · `status` · `status_code` · `latency_ms` · `message` · `timestamp`

---

## DO and DON'T

| DO | DON'T |
|----|--------|
| Prefer OAS 3.1 + `$ref` + examples + `info` chapters | Giant inline schemas; vague / empty descriptions |
| `bru import openapi --collection-format=bru` then enrich | Trust CLI stubs; mix `.bru` and `.yml` |
| Declare security + errors | “Happy path only” contracts |
| Bruno envs + `vars:secret` | Hardcoded tokens / prod URLs |
| Collection auth + `auth: inherit` | Copy bearer blocks on every file |
| Smoke on PR; full on main/nightly | Skip assertions; commit secrets |
| Normalize imports → then generate | Hand-edit Postman JSON as SoT |
| Codegen to framework conventions | Invent alien project layout |

Complete: [do-dont.md](references/do-dont.md).

---

## Examples

See [examples.md](references/examples.md):

1. Design-first OpenAPI with envelopes + path-prefix rules
2. CREATE → capture → GET chain
3. LIST + captureFirstItem
4. Negatives error envelope
5. Collection helpers + `--sandbox=developer`
6. Sync audit (routes ↔ .bru ↔ OAS)
7. CI smoke with secrets injected
8. Import / codegen (CLI import then enrich)
9. REST docs portal preview (Scalar / Redocly)

---

## Critical / Recommended / Nits

Full: [review-checklist.md](references/review-checklist.md).

### Critical
Committed secrets; protected ops without security; missing error/envelope docs; route without `.bru`/OAS; tests without status assert; missing sandbox on `require`; codegen from invalid OAS; secret fields in response schemas; public ops with empty descriptions when asked to document the API.

### Recommended
Verb gold patterns; capture helpers; docs triad; path-prefix/server split for health; writeOnly credentials; smoke vs full CI; sentinel UUID vars; permission notes in descriptions; `--collection-format` on CLI import; reporter skip-headers in CI.

### Nits
seq ordering; folder.bru; Spectral style; Meta env snapshot request; `info.contact` / `license.identifier`.

---

## Decision workflow

1. **Deliverable?** Spec · Bruno · docs · import · codegen · CI → [modes.md](references/modes.md).
2. Vague intent → [make-it-clear](../make-it-clear/SKILL.md).
3. Produce/update **OpenAPI** ([openapi-spec.md](references/openapi-spec.md), [openapi-conventions.md](references/openapi-conventions.md), [api-docs.md](references/api-docs.md)).
4. **Bruno** via patterns + helpers ([bruno-patterns.md](references/bruno-patterns.md), [bruno-helpers.md](references/bruno-helpers.md)).
5. Enforce **sync** ([sync-contract.md](references/sync-contract.md)).
6. Wire **CI** + sandbox ([testing-ci.md](references/testing-ci.md)).
7. **Codegen** only when asked ([codegen.md](references/codegen.md)).
8. Run [review-checklist.md](references/review-checklist.md).
