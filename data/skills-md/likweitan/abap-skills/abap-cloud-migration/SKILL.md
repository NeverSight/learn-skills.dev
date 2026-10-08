---
name: abap-cloud-migration
description: Help with migrating classic ABAP custom code toward higher clean core levels (Level A/B/C/D) including custom code adaptation, identifying released and classic API replacements, generating wrapper classes for non-released objects, ATC clean core and Cloud Readiness checks, changelog for SAP objects, handling incompatible language constructs, and step-by-step remediation workflows. Use when users ask about migrating to ABAP Cloud, custom code migration, cloud readiness, clean core level remediation, eliminating Level D, reducing Level C, non-released API replacement, wrapper pattern, ATC clean core checks, code adaptation, classic to cloud migration, or clean core compliance. Triggers include "migrate to ABAP Cloud", "cloud readiness check", "clean core level", "eliminate Level D", "reduce Level C", "non-released API", "replace with released API", "custom code adaptation", "wrapper for non-released", "ATC clean core", "clean core migration", "changelog for SAP objects", or "ABAP Cloud compatibility".
---

# ABAP Cloud Migration & Clean Core Level Remediation

Guide for systematically raising the **clean core level** of classic ABAP custom code — eliminating Level D, minimizing Level C, and moving toward Level A (ABAP Cloud).

> **Terminology note**: the former 3-tier extensibility model is superseded by the clean core **level concept** (A, B, C, D). Migration is no longer "get everything to Tier 1" — it is "eliminate Level D, minimize Level C, accept stable Level B, target Level A for new work". See the `abap-cloud` skill for the level definitions.

## Workflow

1. **Assess current state**: run ATC clean core checks on existing code
2. **Classify findings by level**: priority 1 → Level D, priority 2 → Level C, priority 3 → Level B
3. **Prioritize remediation**: Level D first (must fix), then Level C (minimize), then Level B (monitor)
4. **Choose a transformation option**: retire · renovate side-by-side · renovate on-stack · adapt
5. **Implement replacements**: released APIs, classic APIs, or wrappers with a single ATC exemption
6. **Validate**: re-run ATC checks, verify no priority 1/2 findings remain, test functionality

## Migration Assessment

### Running ATC clean core checks

1. In ADT: right-click package → **Run As** → **ABAP Test Cockpit**
2. Use check variant `ABAP_CLEAN_CORE_DEVELOPMENT` (SAP-delivered) or build a variant from `ABAP_CLOUD_DEVELOPMENT_DEFAULT` including:
   - `SYCM_USAGE_OF_APIS` — released/classic API classification, SQL on SAP tables, SAP form routines
   - `SYCM_ALLOWED_ENH_TECHNOLOGY` — enhancement technology compliance
   - `CI_SEARCH_CUST_MODIFICATIONS` — modifications
   - `CI_CRITICAL_STATEMENTS` — critical statements
   - `SLIN_SEC` — Code Vulnerability Analyzer (additionally recommended)
3. Use `ABAP_CLOUD_READINESS` to verify ABAP Cloud rules before switching an object's language version
4. Review findings in the ATC Results view

> If `SYCM_USAGE_OF_APIS` or `SYCM_ALLOWED_ENH_TECHNOLOGY` are unavailable, implement **SAP Note 3565942**.

### ATC findings mapped to clean core levels

| ATC priority             | Level | Finding                                                                          | Action                                             |
| ------------------------ | ----- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Priority 1 (Error)**   | **D** | Object is modified                                                               | Remove modification; use a BAdI instead            |
|                          |       | Enhancement technology is not allowed                                            | Delete enhancement; use a BAdI                     |
|                          |       | Implicit or explicit enhancement (source code plug-in)                           | Delete enhancement; use a BAdI                     |
|                          |       | Direct **write** access to SAP database tables                                   | Use released or classic APIs                       |
|                          |       | Call of form routines in SAP program                                             | Use released or classic APIs                       |
|                          |       | Usage of SAP object classified as `noAPI`                                         | Use released or classic APIs; check successor info |
|                          |       | Usage of critical ABAP statements                                                | Use released or classic APIs                       |
| **Priority 2 (Warning)** | **C** | Direct **read** access to SAP database table/view                                | Use released CDS view or classic API               |
|                          |       | Usage of SAP object not classified as classic API (internal) and not released    | Use released or classic APIs                       |
| **Priority 3 (Info)**    | **B** | Usage of deprecated APIs                                                         | Use the successor                                  |
|                          |       | Usage of classic APIs                                                            | — acceptable, no action required                   |

Configure ATC transport settings so **priority 1 and 2 findings block transport release**.

### Remediation priority

1. **Level D — eliminate entirely**
   - No modifications → use BAdIs
   - No implicit or explicit enhancements → use BAdIs
   - No direct write access to SAP DB tables → released or classic APIs
   - No not-recommended (`noAPI`) APIs → released or classic APIs
   - Remove critical ABAP statements → released or classic APIs
   - Do not call form routines within SAP programs → released or classic APIs

2. **Level C — minimize as much as possible**
   - No direct read access to SAP tables → released or classic CDS views
   - Replace SAP internal APIs with released or classic APIs
   - If internal APIs are still needed, explore the **changelog for SAP objects** for incompatible changes
   - Wrap remaining internal objects and create a single fine-grained ATC exemption

3. **Level B — monitor**
   - Adopt successors for deprecated API findings
   - Monitor when SAP releases an equivalent API, then migrate to Level A
   - Do not rewrite stable classic code without a business reason

4. **Level A — sustain**
   - Enforce with `S_ABPLNGVS` authorization and separate software components

## Transformation Options for Legacy Code

| Option                               | When to apply                                                              | Typical tasks                                                                                                                     |
| ------------------------------------ | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Retire unused code**               | ~60% of custom code in a typical ERP is not used productively              | Collect usage data with `SUSG`/`SCMON` · analyze in Custom Code Migration app · remove/backup unused code · use the clone finder  |
| **Renovate & innovate side-by-side** | Loosely coupled extensions better served on SAP Business AI Platform       | Analyze dependencies in Custom Code Migration app · transfer code to BTP · adapt via ATC quick fixes                              |
| **Renovate & innovate on-stack**     | Tightly coupled extensions/modifications worth reimplementing in ABAP Cloud | Analyze complexity for TCO drivers · make code ABAP Cloud compliant · replace non-released objects with released APIs · use only released extension points |
| **Adapt**                            | None of the above is feasible — minimum viable action                      | Adapt via readiness ATC checks, Simplification Database, ADT quick fixes (up to ~60% automation) · SQL Monitor · CDS/AMDP pushdown |

> Recommendation: leave behind as much legacy code as possible **during** the conversion — cleaning up afterwards costs significantly more.

## Changelog for SAP Objects (Level C risk mitigation)

Custom code using internal SAP objects is not upgrade-stable by definition. Internal objects can change during an upgrade, a feature pack import, or even an SAP Note import.

Incompatible changes include:
- Deletion of objects (e.g., function modules)
- Renaming or deletion of function module parameters
- Incompatible changes to parameter types
- Renaming or deletion of methods in SAP classes
- Removal of fields from CDS views

Covered object types: `FUNC`, `CLAS`, `INTF`, `STOB`, `BDEF`.

**How to use it:**
1. Download the Simplification Database file from the SAP Software Download Center (SAP Support Portal)
2. Import it via transaction `SYCM`
3. Run the changelog ATC check during development, or before the system upgrade like other simplification item checks
4. Refactor affected usages toward released or classic APIs

Objects in the changelog are **not** automatically demoted to Level D — continued usage may be allowed depending on the change's scope and criticality.

## Common API Replacements

### Database Access

| Classic Pattern           | ABAP Cloud Replacement        |
| ------------------------- | ----------------------------- |
| `SELECT FROM mara`        | `SELECT FROM i_product`       |
| `SELECT FROM bkpf / bseg` | `SELECT FROM i_journalentry`  |
| `SELECT FROM vbak / vbap` | `SELECT FROM i_salesorder`    |
| `SELECT FROM ekko / ekpo` | `SELECT FROM i_purchaseorder` |
| `SELECT FROM kna1`        | `SELECT FROM i_customer`      |
| `SELECT FROM lfa1`        | `SELECT FROM i_supplier`      |
| `SELECT FROM t001`        | `SELECT FROM i_companycode`   |
| Direct table access       | Use `I_*` released CDS views  |

### Function Modules → Released Classes

| Classic FM                              | Released Replacement                                 |
| --------------------------------------- | ---------------------------------------------------- |
| `GUID_CREATE`                           | `cl_system_uuid=>create_uuid_x16_static( )`          |
| `CONVERSION_EXIT_ALPHA_INPUT`           | `cl_abap_format=>alpha_input( )`                     |
| `CONVERSION_EXIT_ALPHA_OUTPUT`          | `cl_abap_format=>alpha_output( )`                    |
| `POPUP_TO_CONFIRM`                      | Not available — use Fiori UI                         |
| `NUMBER_GET_NEXT`                       | `cl_numberrange_runtime=>number_get( )`              |
| `BAPI_TRANSACTION_COMMIT`               | Handled by RAP framework (no explicit commit)        |
| `SO_NEW_DOCUMENT_ATT_SEND_API1`         | `cl_bcs_mail_message` (send emails)                  |
| `READ_TEXT` / `SAVE_TEXT`               | Not released — wrap or use custom persistence        |
| `JOB_OPEN` / `JOB_CLOSE` / `JOB_SUBMIT` | `cl_apj_rt_api` (Application Jobs)                   |
| `ENQUEUE_*` / `DEQUEUE_*`               | RAP draft / managed locking or `CL_ABAP_LOCK_OBJECT` |

### Language Constructs

| Incompatible Construct                   | Cloud-Compatible Alternative                   |
| ---------------------------------------- | ---------------------------------------------- |
| `CALL TRANSACTION`                       | Not available — use API or RAP                 |
| `SUBMIT ... AND RETURN`                  | Not available — use Application Jobs           |
| `WRITE` / `SKIP` / `ULINE` (list output) | Not available — use Fiori UI for output        |
| `CALL SCREEN` / `CALL SELECTION-SCREEN`  | Not available — use Fiori/UI5                  |
| `MESSAGE ... RAISING`                    | `RAISE EXCEPTION TYPE ...`                     |
| `CALL FUNCTION ... IN UPDATE TASK`       | RAP saver class / managed save                 |
| `EXEC SQL` (Native SQL)                  | ABAP SQL or AMDP                               |
| `GENERATE SUBROUTINE POOL`               | Not available — use strategy/factory pattern   |
| `DESCRIBE FIELD ... TYPE`                | RTTI: `cl_abap_typedescr=>describe_by_data( )` |
| `GET/SET PARAMETER ID`                   | Not available — use method parameters          |

## Wrapper Pattern

When no released API exists, create a wrapper class in a **classic ABAP** software component and release it for **ABAP Cloud (Level A)** consumption.

**Wrapper level classification:**
- Wrapping a **classic API** (Level B object) → the wrapper is **Level B**
- Wrapping an **internal object** (Level C object) → the wrapper is **Level C**
- Wrapping a **not-recommended (`noAPI`) object** → **Level D**, do not build it

Wrapping also collapses N ATC findings into 1, so a single fine-grained exemption covers the usage. This is SAP's recommended practice for working with internal SAP objects.

### Step 1: Create Wrapper Interface (classic ABAP, released for Cloud)

```abap
"Released for use in ABAP Cloud (C1 contract)
INTERFACE zif_text_handler
  PUBLIC.
  METHODS read_text
    IMPORTING iv_id          TYPE thead-tdid
              iv_name        TYPE thead-tdname
              iv_object      TYPE thead-tdobject
              iv_language    TYPE sy-langu DEFAULT sy-langu
    RETURNING VALUE(rt_text) TYPE tline_tab
    RAISING   zcx_text_error.

  METHODS save_text
    IMPORTING iv_id       TYPE thead-tdid
              iv_name     TYPE thead-tdname
              iv_object   TYPE thead-tdobject
              iv_language TYPE sy-langu DEFAULT sy-langu
              it_text     TYPE tline_tab
    RAISING   zcx_text_error.
ENDINTERFACE.
```

### Step 2: Create Wrapper Class (classic ABAP, released for Cloud)

```abap
"Implementation uses non-released FMs internally
"Released for use in ABAP Cloud (C1 contract)
CLASS zcl_text_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_text_handler.
ENDCLASS.

CLASS zcl_text_handler IMPLEMENTATION.
  METHOD zif_text_handler~read_text.
    "Uses non-released FM internally — acceptable inside the wrapper
    CALL FUNCTION 'READ_TEXT'
      EXPORTING
        id       = iv_id
        name     = iv_name
        object   = iv_object
        language = iv_language
      TABLES
        lines    = rt_text
      EXCEPTIONS
        OTHERS   = 1.
    IF sy-subrc <> 0.
      RAISE EXCEPTION TYPE zcx_text_error.
    ENDIF.
  ENDMETHOD.

  METHOD zif_text_handler~save_text.
    DATA ls_header TYPE thead.
    ls_header-tdid     = iv_id.
    ls_header-tdname   = iv_name.
    ls_header-tdobject = iv_object.
    ls_header-tdspras  = iv_language.

    CALL FUNCTION 'SAVE_TEXT'
      EXPORTING header = ls_header
      TABLES    lines  = it_text
      EXCEPTIONS OTHERS = 1.
    IF sy-subrc <> 0.
      RAISE EXCEPTION TYPE zcx_text_error.
    ENDIF.
  ENDMETHOD.
ENDCLASS.
```

### Step 3: Release the Wrapper

In ADT, open the wrapper class properties:

1. Go to **API State** tab
2. Add **Use System-Internally (C1)** contract
3. Set visibility to **Use in ABAP Cloud**

### Step 4: Use in ABAP Cloud (Level A) Code

```abap
"ABAP Cloud code — uses released wrapper
DATA(lo_text) = NEW zcl_text_handler( ).
DATA(lt_text) = lo_text->zif_text_handler~read_text(
  iv_id     = 'ST'
  iv_name   = lv_doc_name
  iv_object = 'VBBK' ).
```

### Step 5: Handle authorizations and exemptions

- Classic APIs often check **non-released authorization objects**, which cannot be used in ABAP Cloud. PFCG roles may mix released and non-released authorization objects.
- Provide `SU22` data for the wrapper when releasing it, and create `SU22` variants for each designated usage so roles can be maintained.
- Create a **single fine-grained ATC exemption** on the wrapper's internal usage rather than one per call site.
- **Retire the wrapper** once SAP releases the API — replace it and move the code to the ABAP Cloud software component.

### Wrapper guidance by object type

- **CDS views**: create a custom CDS view on top of the non-released SAP CDS view and release it. Association targets and value help views may also need wrappers. If no SAP CDS view exists at all, wrap the database table.
- **Classes / interfaces**: wrap the non-released FM or class. Do **not** copy non-released data types (data elements, structures, table types) used in the signature — wrap them via `TYPES` declarations in the wrapper's public section, so only the wrapper needs releasing.

## Migration Strategy by Object Type

### Reports / Programs

```
Classic Report → Application Job class + CDS view + Fiori app
1. Extract data logic → CDS view entities
2. Extract business logic → ABAP Cloud class
3. Create Application Job catalog entry (CL_APJ_DT_CREATE_CONTENT)
4. Schedule via Fiori app "Application Jobs"
```

### Dynpro Transactions

```
Dynpro Transaction → RAP BO + Fiori Elements app
1. Identify CRUD operations → RAP behavior definition
2. Map screen fields → CDS view entity
3. Create service definition/binding
4. Generate Fiori Elements app
```

### BAPIs

```
BAPI → RAP BO with custom actions
1. Map BAPI parameters → CDS abstract entities
2. Implement as RAP actions or factory actions
3. Expose via OData service binding
```

### RFC Function Modules

```
RFC FM → Released API class or RAP service
1. If simple logic → Released ABAP class (Level A)
2. If CRUD → RAP BO with service binding (Level A)
3. If complex → Wrapper class in classic ABAP (Level B or C)
```

## Finding Released and Classic Replacements

### In ADT

1. **Released Object Search**: `Ctrl+Shift+A` → Filter by "Released" APIs
2. **API State Filter**: In Project Explorer, filter by C1 release state
3. **ABAP Element Info**: Hover over a non-released object → see successor suggestion if available

### Using the Released Objects App

Fiori app **Released Objects** (`F5865`):

- Search by classic object name
- Filter by release state (C1, C2)
- View successor information

### Using the Cloudification Repository

Determine an object's clean core level and successor:

- **Classic APIs (Level B)**: `objectClassifications_SAP.json` — viewer at https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json
- **Not recommended (Level D)**: filter the viewer for `state` = `noAPI`
- **Internal with successor (Level C)**: flagged `internalAPI`
- Anything unclassified and not released defaults to **Level C**

### Programmatic Check

```abap
"Check if an object is released for ABAP Cloud (Level A)
SELECT SINGLE *
  FROM i_apistateofrepositoryobject
  WHERE ObjectType     = 'CLAS'
    AND ObjectName     = 'CL_NUMBERRANGE_RUNTIME'
    AND ReleaseState   = 'RELEASED'
  INTO @DATA(ls_state).
```

## Step-by-Step Remediation Checklist

1. [ ] Run ATC clean core checks (`ABAP_CLEAN_CORE_DEVELOPMENT`) on the package/objects
2. [ ] Export findings and group by ATC priority → clean core level (P1=D, P2=C, P3=B)
3. [ ] **Eliminate all Level D findings** (priority 1):
   - [ ] Remove modifications → use released or classic BAdIs
   - [ ] Remove implicit/explicit enhancements → use BAdIs
   - [ ] Remove direct write access to SAP tables → released or classic APIs
   - [ ] Replace `noAPI` object usage → check successor information
   - [ ] Remove critical ABAP statements
   - [ ] Remove calls to SAP form routines
4. [ ] **Minimize Level C findings** (priority 2):
   - [ ] Replace direct read access to SAP tables → released or classic CDS views
   - [ ] Replace SAP internal APIs → released or classic APIs
   - [ ] For unavoidable internal usage: wrap + single ATC exemption
   - [ ] Import the changelog for SAP objects via `SYCM` and check for incompatible changes
5. [ ] **Review Level B findings** (priority 3):
   - [ ] Adopt successors for deprecated APIs
   - [ ] Leave stable classic API usage as-is
6. [ ] For each non-released API without a replacement:
   - [ ] Create a wrapper in the classic ABAP component and release it for ABAP Cloud
   - [ ] Provide `SU22` data and variants for the wrapper
7. [ ] For each incompatible language construct: refactor to a cloud-compatible alternative
8. [ ] For Dynpro/ALV/list-based UIs: plan the Fiori replacement (separate project)
9. [ ] Move migrated objects to the ABAP for Cloud Development software component
10. [ ] Run `ABAP_CLOUD_READINESS` before switching an object's language version
11. [ ] Re-run ATC checks — no priority 1 or 2 findings should remain
12. [ ] Configure ATC transport settings to block release on priority 1 and 2 findings
13. [ ] Execute regression tests

## Output Format

When helping with migration topics, structure responses as:

```markdown
## Migration Guidance

### Current Code Analysis

- Current clean core level: [A / B / C / D] (lowest level used)
- Level D findings (must fix): [list]
- Level C findings (minimize): [list]
- Level B findings (monitor): [list]
- Incompatible constructs: [list]
- Estimated effort: [low / medium / high]

### Remediation Strategy

[Ordered by level: D first, then C, then B]
[For each finding: original → replacement with code, target level]

### Wrapper Requirements

[Objects needing wrappers, with the resulting wrapper level (B or C)]

### Target State

- Achievable clean core level: [A / B]
- Residual exemptions required: [list with justification]
```

## References

- Clean Core Extensibility Whitepaper — the authoritative source for the level concept
- Extend SAP S/4HANA in the cloud and on premise with ABAP based extensions (Version 2.3, August 2025)
- Custom Code Migration Guide: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/custom-code-migration
- ABAP Cloud API Release Info: https://help.sap.com/docs/abap-cloud/abap-rap/released-abap-objects
- Cloudification Repository: https://github.com/SAP/abap-atc-cr-cv-s4hc
- Wrapper Pattern: https://github.com/SAP-samples/abap-cheat-sheets/blob/main/19_ABAP_Cloud.md
- ATC Cloud Readiness: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/checking-abap-cloud-readiness
- SAP Note 3565942 — clean core ATC checks
- SAP Note 3578329 — classic technology classification

## Detailed Reference

- **Remediation checklist**: Read `references/migration-checklist.md` for the full level-based remediation checklist, effort estimation, and rollback planning

## Related Skills

- **abap-cloud**: Use for clean core level definitions, development models, and wrapper classification
- **atc-cloudification**: Use for configuring ATC clean core checks and level governance
- **released-abap-classes**: Use for finding Level A released API replacements
- **badi-enhancement**: Use for replacing modifications and enhancements with BAdIs
- **abap-sql-amdp**: Use for modernizing ABAP SQL and AMDP during migration
