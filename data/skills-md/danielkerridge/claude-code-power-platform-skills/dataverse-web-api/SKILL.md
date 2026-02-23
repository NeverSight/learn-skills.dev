---
name: dataverse-web-api
description: >
  Use when programmatically creating, modifying, or querying Dataverse schema and metadata
  via the Web API (OData v4.0). Covers table/column/relationship definitions, solution ALM,
  form and view XML construction, app module composition, global option sets, business rules,
  Custom API registration, and publishing. Triggers on: "dataverse api", "dataverse metadata",
  "entitydefinitions", "web api schema", "create dataverse table", "create dataverse column",
  "fetchxml", "formxml", "layoutxml", "dataverse solution", "dataverse relationship",
  "odata dataverse", "metadata api", "publish customizations", "dataverse alm",
  "grid control", "editable grid", "business rule", "rich text", "auto-number",
  "file column", "image column", "pcf control", "security role", "column security",
  "environment variable", "custom api", "data migration", "solution import".
license: MIT
compatibility: "Dataverse Web API v9.2, OData v4.0, OAuth 2.0"
metadata:
  author: custom
  version: "1.0.0"
  platform: "Microsoft Power Platform / Dataverse"
  api-version: "v9.2"
---

# Dataverse Web API Metadata Skill

You are an expert in the Microsoft Dataverse Web API, specifically the metadata and schema
management capabilities exposed via the OData v4.0 RESTful endpoint. You help developers
programmatically architect Dataverse environments — treating application structure as code.

## CRITICAL RULES -- Read These First

1. **Always use the `MSCRM.SolutionUniqueName` header** when creating components.
   Creating tables, columns, or relationships without this header adds them to the
   Default Solution (Active layer), which is an ALM anti-pattern. Read `resources/solutions-alm.md`.

2. **The API is polymorphic.** Column (Attribute) creation payloads MUST include the
   correct `@odata.type` (e.g., `Microsoft.Dynamics.CRM.StringAttributeMetadata`).
   Omitting or using the wrong type causes 400 errors. Read `resources/columns-attributes.md`.

3. **Every table needs a Primary Name attribute.** When creating a table via
   `POST /EntityDefinitions`, the `Attributes` array MUST contain exactly one
   `StringAttributeMetadata` with `IsPrimaryName: true`. Read `resources/tables-entities.md`.

4. **Publishing is required.** Creating forms, views, or sitemap changes leaves them in
   draft state. Call the `PublishXml` action to make changes visible. Read `resources/publishing-ops.md`.

5. **FormXml and LayoutXml must stay in sync with FetchXml.** Every attribute in a view's
   `layoutxml` MUST appear in its `fetchxml`. Mismatches cause runtime errors.
   Read `resources/views-queries.md`.

6. **Base URL pattern:** `https://{org}.api.crm.dynamics.com/api/data/v9.2/`

7. **Required headers for all requests:**
   - `Authorization: Bearer {token}` (OAuth 2.0)
   - `Content-Type: application/json; charset=utf-8`
   - `OData-Version: 4.0`
   - `OData-MaxVersion: 4.0`

8. **Windows: Always use PowerShell .ps1 scripts** for API calls. Bash mangles OData `$` params
   (`$filter`, `$select`). Write `.ps1` files and run with `powershell -ExecutionPolicy Bypass -File`.

9. **Never create placeholder columns.** If a field needs computation, use formula columns
   (`FormulaDefinition`), plugins, or code-based updates. Never create empty columns
   "to be configured later in Maker Portal." Read `resources/best-practices.md`.

10. **Never use `pac auth token`** — this command does not exist. Use Azure CLI instead:
    `az account get-access-token --resource "https://[org].crm6.dynamics.com/" --tenant "[tenant-id]" --query accessToken -o tsv`

11. **Some Dataverse design decisions are PERMANENT** and cannot be changed after creation
    (data types, table logical names, ownership type). Read `resources/dataverse-design-rules.md`
    before designing tables.

## Quick Reference: Key Endpoints

| Operation | Method | Endpoint |
|---|---|---|
| Create table | POST | `/EntityDefinitions` |
| Create column | POST | `/EntityDefinitions(LogicalName='{table}')/Attributes` |
| Create 1:N relationship | POST | `/RelationshipDefinitions` |
| Create N:N relationship | POST | `/RelationshipDefinitions` |
| Create global option set | POST | `/GlobalOptionSetDefinitions` |
| Create form | POST | `/systemforms` |
| Create view | POST | `/savedqueries` |
| Create solution | POST | `/solutions` |
| Create publisher | POST | `/publishers` |
| Create app module | POST | `/appmodules` |
| Create sitemap | POST | `/sitemaps` |
| Add component to solution | Action | `AddSolutionComponent` |
| Add component to app | Action | `AddAppComponents` |
| Publish changes | Action | `PublishXml` |
| Validate app | Function | `ValidateApp` |
| Create business rule | POST | `/workflows` (Category=2) |
| Create environment variable | POST | `/environmentvariabledefinitions` |
| Create custom API | POST | `/customapis` |

## Workflow: Building a Dataverse Schema from Scratch

### Step 1 -- Create Publisher and Solution

Every project starts with a Publisher (defines prefix) and a Solution (groups components).
Read `resources/solutions-alm.md` for full payloads and patterns.

```http
POST /publishers
{
  "friendlyname": "Contoso Corp",
  "uniquename": "contoso",
  "customizationprefix": "cnt",
  "customizationoptionvalueprefix": 10000
}
```

```http
POST /solutions
{
  "uniquename": "ContosoHRModule",
  "friendlyname": "Contoso HR Module",
  "version": "1.0.0.0",
  "publisherid@odata.bind": "/publishers({publisher-guid})"
}
```

### Step 2 -- Create Tables

Include the `MSCRM.SolutionUniqueName` header. The Primary Name attribute is inline.
Read `resources/tables-entities.md` for all properties and table types.

```http
POST /EntityDefinitions
MSCRM.SolutionUniqueName: ContosoHRModule

{
  "SchemaName": "cnt_Project",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "Label": "Project", "LanguageCode": 1033 }] },
  "DisplayCollectionName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "Label": "Projects", "LanguageCode": 1033 }] },
  "OwnershipType": "UserOwned",
  "HasNotes": true,
  "HasActivities": true,
  "Attributes": [{
    "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
    "SchemaName": "cnt_ProjectName",
    "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{ "Label": "Project Name", "LanguageCode": 1033 }] },
    "IsPrimaryName": true,
    "MaxLength": 200,
    "RequiredLevel": { "Value": "ApplicationRequired" }
  }]
}
```

### Step 3 -- Add Columns

Read `resources/columns-attributes.md` for all 12+ column types with exact payloads.

### Step 4 -- Define Relationships

Read `resources/relationships.md` for 1:N and N:N patterns with cascade configuration.

### Step 5 -- Create Views

Read `resources/views-queries.md` for FetchXML + LayoutXML construction.

### Step 6 -- Create Forms

Read `resources/forms-ui.md` for FormXml schema and programmatic form generation.

### Step 7 -- Build the App Module

Read `resources/app-modules.md` for app composition, sitemap, and validation.

### Step 8 -- Publish

```http
POST /PublishXml
{
  "ParameterXml": "<importexportxml><entities><entity>cnt_project</entity></entities></importexportxml>"
}
```

Read `resources/publishing-ops.md` for selective vs full publishing and ValidateApp.

## When Debugging API Calls

1. Check `@odata.type` is correct for the payload type
2. Verify `MSCRM.SolutionUniqueName` header is present
3. Ensure `SchemaName` includes the publisher prefix (e.g., `cnt_`)
4. Confirm `IsPrimaryName` attribute exists when creating tables
5. Check that `fetchxml` and `layoutxml` columns match for views
6. Remember to call `PublishXml` after form/view/sitemap changes
7. Use `$metadata` endpoint to inspect the current schema: `GET /api/data/v9.2/$metadata`

## Resource Files

- `resources/solutions-alm.md` -- Publishers, solutions, component management, ALM patterns
- `resources/tables-entities.md` -- Table creation, types, behavioral properties
- `resources/columns-attributes.md` -- All column types with exact payloads
- `resources/relationships.md` -- 1:N, N:N relationships, cascade config, eligibility checks
- `resources/views-queries.md` -- FetchXML, LayoutXML, view types, savedquery creation
- `resources/forms-ui.md` -- FormXml schema, form types, programmatic form construction
- `resources/app-modules.md` -- App modules, sitemaps, AddAppComponents, ValidateApp
- `resources/publishing-ops.md` -- PublishXml, Custom APIs, business rules, workflow
- `resources/best-practices.md` -- No placeholder columns, idempotent scripts, token management, naming
- `resources/formula-columns.md` -- Formula column creation, supported types/functions, limitations
- `resources/parallelization.md` -- Schema creation dependency graph, agent team strategies
- `resources/grid-controls.md` -- Grid types: Power Apps Grid Control, Editable Grid, nested grids, Kanban alternatives
- `resources/advanced-column-types.md` -- Rich text, address, file, image, auto-number, multi-select, currency details
- `resources/business-rules.md` -- Business rules via API, XAML patterns, decision guide vs JS vs plugins
- `resources/security-model.md` -- Security roles, column security, app-level security, sharing, BPF security
- `resources/environment-variables.md` -- Environment variable types, default/current values, usage patterns
- `resources/dataverse-design-rules.md` -- Permanent design decisions, import gotchas, performance optimization
- `resources/custom-apis.md` -- Custom API creation, binding types, function vs action, testing
- `resources/testing-monitoring.md` -- Monitor tool, Application Insights, PAD testing, Solution Checker, testing decision matrix
