---
name: build-with-arcgis-api-for-python
license: Apache-2.0
description: Use when working with ArcGIS API for Python (ArcGIS Python API, Python API for ArcGIS, Esri Python API), the arcgis Python package/library/module, or arcgis-mapping (arcgis.map). Covers scripts/notebooks, setup, authentication, Spatially Enabled DataFrames (SEDF), queries/edits, publishing, portal administration, cloning/dependencies, Web Maps/Web Scenes, analysis, geocoding, routing and arcgis.ai for ArcGIS Online, Enterprise and Location Platform. Not for ArcPy-only tasks or non-Python SDKs.

---

# Build with ArcGIS API for Python

The ArcGIS API for Python (`arcgis`) is a Python library for GIS visualization, analysis, data management and administration. Use it in scripts, notebooks and scheduled jobs to access ArcGIS services and automate spatial and portal workflows.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

### Developer credential items

[Developer credentials](https://developers.arcgis.com/documentation/security-and-authentication/how-to-use-authentication/#1-create-developer-credentials) are portal items for API key or OAuth credentials, not organization-wide sign-in configuration. Creating these items is separate from authenticating a script's user through an existing application registration or session; not every script needs its own credential item.

- For ArcGIS Online credential creation, eligible user types are Creator, Professional and Professional Plus. Also verify the required role privileges for the selected credential type; see the [API key credential prerequisites](https://developers.arcgis.com/documentation/security-and-authentication/api-key-authentication/api-key-credentials/online/#creating-api-key-credentials) and the authentication skill's OAuth credential guidance.
- For ArcGIS Enterprise, check the deployed release against [Developer credentials for ArcGIS Enterprise](https://developers.arcgis.com/documentation/security-and-authentication/developer-credentials/developer-credentials-enterprise/). Supported credential types and privileges vary by version; do not assume the latest documentation applies unchanged.

## Installation and setup

Keep installation and environment setup guidance in this skill, not in topic reference files.

### Agent-completed steps
- Inspect versions, manifests/lockfiles and kernel; reuse package manager and preserve base environments.
- Isolate standalone environments; clone Pro's. Install only missing, compatible dependencies per [installation](https://developers.arcgis.com/python/latest/guide/install-and-set-up/intro/) and [requirements](https://developers.arcgis.com/python/latest/guide/system-requirements/).
- Check `arcgis-mapping`/rendering and geometry/I/O engines as needed; `arcgis` is not ArcPy.
- The `arcgis-mapping` package provides the `arcgis.map` module; import mapping classes with `from arcgis.map import Map, Scene`.

### User-completed configuration
- Confirm privileges/licenses, services and spending limits.
- Supply secrets securely via profiles/storage/environment, never chat, source, logs or notebook output.
- Configure trusted certificates; never disable verification.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `python-api` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

### Version-aware documentation

- When API version compatibility matters, determine the installed `arcgis` package version from the user's active Python environment, if accessible.
- For a known version, use the corresponding documentation at `https://archive.developers.arcgis.com/v<version>/` (for example, `https://archive.developers.arcgis.com/v2.4.3/`), including when following links below or in references.
- If the version is unknown or matching documentation is unavailable, fall back to `https://developers.arcgis.com/python/latest/`.
- When using newer documentation for an older installation, do not assume compatibility. Verify against the installed API when possible; otherwise clearly communicate uncertainty.

## Workflow references

Load only the reference relevant to the task. References marked as outlines are incomplete workflow outlines, not executable instructions. Continue to use the established patterns and validation process below when using them.

| Task | Reference |
| --- | --- |
| Author, edit or visualize Web Maps/Web Scenes with `arcgis.map.Map`/`Scene`; configure layers, renderers, popups, symbols or Field Maps forms | [Mapping with arcgis-mapping](./references/arcgis-mapping.md) |
| Discover item dependencies and plan migration scope | [Item dependency graphs](./references/item-dependency-graph.md) |
| Clone between portals and investigate offline export/import | [Cloning](./references/cloning.md) |
| Analyze images or text, or translate text with `arcgis.ai` | [AI-powered services](./references/ai-powered-services.md) |

## Patterns and guidelines

Match APIs/return types to installed versions and [deprecations](https://developers.arcgis.com/python/latest/guide/deprecation-notices/), not blind upgrades. Load the mapping reference above only for map/scene authoring or visualization tasks; other ArcGIS workflows do not need its mapping-specific APIs.

For new environments, check Esri's current system requirements and release/install documentation, then use the newest ArcGIS API for Python version compatible with the target Python, ArcGIS Pro/Enterprise runtime, and other project constraints. Do not treat a version mentioned in a deprecation example or old project as the current default. In dependency files, avoid an exact pin unless reproducibility or deployment requires one; document and lock a tested version when deterministic installs are needed. Existing projects should retain their declared compatibility constraints unless the user asks to upgrade.

### Choosing an application format
- Match the interface to the user's workflow; do not assume "application" means a browser UI.
- Prefer a command-line script for straightforward utilities, repeatable jobs, and batch processing; use a notebook for interactive exploration.
- If the intended interface is unclear and materially changes the solution, ask a brief clarifying question or state the assumption before implementing.

### Python accounts and sessions
- Account requirements vary by workflow: anonymous `GIS()`/`GIS(portal_url)` can read public data where allowed, and local processing needs no account. Credential-creation requirements do not apply to all API use. Check privileges/sharing and subscription/Enterprise-version limits.
- Preserve auth; if the auth skill is absent, use project patterns and [Python auth](https://developers.arcgis.com/python/latest/guide/working-with-different-authentication-schemes/).
- Verify user OAuth versus app/API-key support. Protect owner-impersonating secrets; test profiles under the unattended identity.
- Use `GIS("home")` in hosted notebooks, `GIS("pro")` for Pro (Pro notebooks also support `home`). Verify portal/identity; reuse connections/refresh and explicit `gis`/geocoder where supported.
- `GIS("home")` and `GIS("pro")` require the corresponding ArcGIS notebook or ArcGIS Pro authentication context and fail without it. For standalone scripts without that context (for example, on macOS), use an explicit portal URL and a supported authentication method.

### SEDF
- Follow [features/SEDF](https://developers.arcgis.com/python/latest/api-reference/arcgis.features.toc.html). ArcGIS registers pandas' `.spatial` and `.geom` accessors when its accessor module is loaded. Explicit imports of `GeoAccessor` and `GeoSeriesAccessor` from `arcgis.features` provide that registration when working directly with pandas.
- Read via `pd.DataFrame.spatial.from_layer` or `layer.query(as_df=True)`; publish with `sdf.spatial.to_featurelayer`, export with `to_featureclass`.
- Establish the spatial reference and units; assigning a spatial reference does not reproject coordinates. `sdf.spatial.project(...)` mutates in place, returning a boolean.
- Check engines/nulls/column sanitization: some Shapely publishing paths turn null integers into zero. Set `to_featureclass` overwrite explicitly (default: `True`).


### Writes and administration
- Check search limits/completeness. Prefer supported `Folder.add`/`Item.sharing` over deprecated `ContentManager.add`/`Item.share`.
- Before jobs/writes, verify target/query with a bounded read. Check schema/domains, geometry and spatial reference, capabilities and affected IDs/count. Preview destructive/broad changes; confirm scope/recovery.
- Distinguish publishing from updating/overwriting; preserve dependencies. Reassign content before user deletion; never expose private data to bypass errors.
- Use `edit_features` for small edits; consider supported `append`/upsert for 250+ inserts/updates (not a hard limit). Check formats/mappings/unique match keys; otherwise batch to service limits. Append does not delete.
- Use actual object-ID fields or supported GlobalIDs. Rollback is per-request, not cross-batch. Inspect per-feature results/read-back; report partial success.
- Retry transient failures with bounded backoff/`Retry-After`; reconcile uncertain writes/jobs by IDs/keys/status first. Fix permission/schema errors instead of retrying.

### Service analysis and routing
- Distinguish local work from service analysis/routing; verify availability, privileges/licenses and data-sharing approval.
- Use supported `estimate=True`; check fees, extent, spatial reference, units, output persistence and routing modes/restrictions/time.
- Resolve jobs/futures and inspect results/errors; submission is not success.

### Geocoding
- Select an approved geocoder; confirm privacy before transmitting addresses.
- Set `geocode(..., for_storage=True)` for storage where required (default: `False`); check privileges/billing. `batch_geocode` has separate requirements, no `for_storage`.
- Respect `MaxBatchSize`/`SuggestedBatchSize`; reconcile IDs, not order. Set search and spatial reference constraints; report unmatched/poor matches.

## Validation process

Validate authorized work only; never write just to test.

- [ ] Interpreter imports `arcgis`, reports version; maps render as needed.
- [ ] Portal/auth/identity are correct.
- [ ] Counts/IDs are complete/unique; schema, nulls, geometry and spatial reference survive I/O.
- [ ] Writes pass results/read-back; jobs succeed.
- [ ] Outputs/sharing/costs are intended; no secrets leak.
- [ ] Report checks/failures/untested paths; fix and revalidate.
