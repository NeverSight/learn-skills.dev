---
name: abap-cloud
description: Help with ABAP Cloud development and the clean core level concept (Levels A, B, C, D) including ABAP Cloud vs. classic ABAP development models, ABAP Cloud language version restrictions, wrapper patterns for non-released APIs, released/classic/internal/not-recommended object classification, and clean core principles. Use when users ask about ABAP Cloud, ABAP for Cloud Development, clean core, clean core levels, Level A B C D, classic API, internal object, not recommended object, noAPI, wrapper pattern, released APIs, stability contract, language version, restricted ABAP, embedded Steampunk, developer extensibility, key user extensibility, changelog for SAP objects, or ABAP Cloud readiness. Triggers include "ABAP Cloud restrictions", "clean core", "clean core level", "which level is my extension", "Level A extension", "classic API", "wrapper class", "released API alternative", "ABAP language version", "Steampunk", or "extensibility model".
---

# ABAP Cloud & the Clean Core Level Concept

Guide for developing with the ABAP Cloud programming model, classifying extensions using the clean core **level concept** (A–D), and applying clean core principles.

> **Terminology note**: SAP has evolved the former **3-tier extensibility model** into the **clean core level concept**. The 3-tier model (Tier 1/2/3) is superseded — use Levels A, B, C, D instead. Current product naming: **SAP Cloud ERP** (public), **SAP Cloud ERP Private** (formerly S/4HANA Cloud Private Edition), **SAP Business AI Platform** (includes SAP BTP capabilities), **SAP Build** (pro-code and low-code tooling, includes ABAP Cloud).

## Workflow

1. **Determine the user's context**:
   - Understanding ABAP Cloud concepts and restrictions
   - Classifying an extension into a clean core level
   - Choosing between ABAP Cloud development and classic ABAP development
   - Wrapping non-released APIs for use in ABAP Cloud
   - Identifying released or classic API alternatives

2. **Classify the extension by clean core level**:
   - Level A: only released APIs and extension points (stability contract)
   - Level B: classic APIs and classic frameworks (nominated, no stability contract)
   - Level C: SAP internal objects (conditionally clean with changelog)
   - Level D: not-recommended objects and patterns (must be remediated)

3. **Apply the lowest-level rule**: an extension is classified by the **lowest** level it uses. A Level A extension that calls one internal object is a **Level C** extension.

4. **Guide implementation** toward the highest applicable level (Level A first).

## Clean Core Level Concept

SAP classifies extensions into four levels, similar to energy labels. Level A is the target state reflecting the "SAP Business AI Platform first" strategy; Level D must be remediated.

| Level       | Name                            | SAP objects qualifier                                          | Upgrade stability                                 | ATC behavior                 |
| ----------- | ------------------------------- | -------------------------------------------------------------- | ------------------------------------------------- | ---------------------------- |
| **Level A** | Extend with SAP Build           | `[Released]` SAP remote APIs, local APIs, extension points     | Guaranteed by **stability contract**              | No finding                   |
| **Level B** | Leverage classic APIs           | `[Classic]` SAP APIs and extension points                      | Nominated by SAP experts, no formal contract      | Priority 3 (information)     |
| **Level C** | Access internal objects         | `[Internal]` SAP objects (the default for unclassified objects) | Not upgrade-stable; mitigate via changelog        | Priority 2 (warning)         |
| **Level D** | Not recommended                 | `[Not recommended]` SAP objects, extension points, techniques  | High risk, significant technical debt             | Priority 1 (error)           |

**Clean core status**: Level A = clean core · Levels B and C = conditional clean core · Level D = not clean core.

### Level A — Extend with SAP Build and Joule Studio

Only publicly released interfaces and extension points with a **stability contract**.

- **On-stack**: ABAP Cloud development model inside SAP Cloud ERP Private, using released local APIs (released CDS views, released BO interfaces, released extension points), plus key user extensibility
- **Side-by-side**: SAP Business AI Platform using ABAP Cloud, CAP, or low-code/no-code tools (SAP Build, Joule Studio) consuming released remote APIs
- Discover released objects in the **SAP Business Accelerator Hub**, the **Cloudification Repository**, or directly in ADT
- Note: Level A coverage does not span the full functional scope of SAP Cloud ERP Private, and full coverage is not planned

```abap
"Level A: ABAP Cloud class using only released APIs
CLASS zcl_my_extension DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_oo_adt_classrun.
ENDCLASS.

CLASS zcl_my_extension IMPLEMENTATION.
  METHOD if_oo_adt_classrun~main.
    "Released CDS view — no direct table access
    SELECT FROM I_BusinessPartner
      FIELDS BusinessPartner, BusinessPartnerName
      INTO TABLE @DATA(partners)
      UP TO 10 ROWS.
    out->write( partners ).
  ENDMETHOD.
ENDCLASS.
```

### Level B — Leverage classic APIs

Well-established, documented, SAP-nominated **classic APIs** and classic frameworks. No formal stability contract, but a long history of reliable use and SAP internal quality assurance.

- Typical examples: `BAPI_*` function modules, `CL_GUI_ALV_GRID`, non-released BAdIs, user/customer exits, SAP GUI and ALV frameworks
- Custom objects in ABAP language version **Standard ABAP** are Level B, provided they reference only released or classic objects
- Wrappers around classic APIs that enable consumption from Level A code are Level B
- Identify classic APIs in `objectClassifications_SAP.json` (Cloudification Repository) and **SAP Note 3578329** for framework classification
- Recommended software component for classic ABAP development: `HOME`

### Level C — Access internal objects

SAP **internal** objects that are technically accessible but not released, not nominated, not documented, and not supported for customer use. This is the **default** classification for any SAP object not otherwise classified.

- Typical examples: direct calls to internal function modules/classes, **read** access to SAP database tables
- Mitigation: the **changelog for SAP objects** identifies internal objects targeted for incompatible changes in upcoming releases, enabling proactive refactoring before upgrades
- SAP may reclassify internal objects as classic (→ Level B) or not recommended (→ Level D)
- Objects with a released successor are flagged `internalAPI` in the Cloudification Repository

### Level D — Not recommended

Highest risk, highest technical debt. **Remediate immediately.**

- SAP objects classified `noAPI` in the Cloudification Repository (e.g., `RFC_READ_TABLE`)
- Modifications to SAP objects (including SAP Notes applied with manual corrections)
- Implicit and explicit enhancements (source code plug-ins)
- Direct **write** access to SAP database tables
- Calling form routines inside SAP programs
- Critical ABAP statements (kernel calls, system calls, editor calls, `EXEC SQL`, DB hints, report/Dynpro generation, nametab import/export)
- Implementation of BAdIs flagged as SAP-internal

## Development Models

Two coexisting on-stack development models in SAP Cloud ERP Private:

| Aspect             | ABAP Cloud development                                          | Classic ABAP development                                    |
| ------------------ | --------------------------------------------------------------- | ----------------------------------------------------------- |
| **Clean core**     | Level A                                                         | Level B (or C/D if internal/not-recommended objects used)   |
| **Language version** | ABAP for Cloud Development                                     | Standard ABAP                                               |
| **Default choice** | Yes — for all new ABAP-based extensions                         | Only where no released API exists or UI is classic          |
| **Leading model**  | RAP                                                             | Classic frameworks (SAP GUI, ALV, Web Dynpro, SEGW, BOPF)   |
| **Enforcement**    | Syntax check + runtime check                                    | ABAP test cockpit (ATC) governance                          |
| **Software component** | Component with language version ABAP for Cloud Development  | `HOME` or existing classic component                        |
| **IDE**            | ADT (mandatory)                                                 | ADT or SAP GUI                                              |
| **Developer role** | `SAP_BC_ABAP_DEVELOPER_5` template                              | Standard developer role                                     |

### Access rules

**ABAP Cloud objects** may access only:
- Custom objects inside the same software component
- Released SAP objects (released APIs)
- Custom objects released for ABAP Cloud development (released custom APIs) from a classic software component

**Classic ABAP objects** should access only:
- Custom objects inside their own software component
- Released SAP APIs **and** classic SAP APIs
- Custom objects in classic and ABAP Cloud software components

### Enforcing the model via authorization

Authorization object `S_ABPLNGVS` controls whether a developer may create objects in Standard ABAP or only in ABAP for Cloud Development. Use it to create a dedicated ABAP Cloud developer role.

## Key Restrictions in ABAP for Cloud Development

- Only released SAP APIs (C1 contract) can be used
- No direct database table access for SAP tables (use released CDS views)
- No classic dynpro, selection screens, or SAP GUI-dependent statements
- No `CALL TRANSACTION`, `SUBMIT`, `AUTHORITY-CHECK` (use `CL_ABAP_AUTHORIZATION`)
- No classic BAdIs or user exits (only released BAdIs)
- No `EXEC SQL` or native SQL (use ABAP SQL or AMDP)
- No non-released function modules
- No `INCLUDE` programs
- No `WRITE` or classic list output
- Use `if_oo_adt_classrun` for console output

## Wrapper Pattern

When a required API is not released, build a wrapper in a **classic ABAP** software component and release it for ABAP Cloud development. The consuming ABAP Cloud code stays clean; the wrapper localizes the level violation to a single place.

**Wrapper level classification** (from the whitepaper):
- Wrapper around a **classic API** (Level B object) → the wrapper is **Level B**
- Wrapper around an **internal object** (Level C object) → the wrapper is **Level C**
- Wrapper around a **not-recommended object** → **Level D**, do not build it

```abap
"Classic ABAP software component: wrapper class released for ABAP Cloud
"Wrapping BAPI_PO_CREATE1 (a classic API) → Level B
CLASS zcl_wrapper_material DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_material_reader.
    "Release with C1 contract in ADT → API State tab
ENDCLASS.

CLASS zcl_wrapper_material IMPLEMENTATION.
  METHOD zif_material_reader~get_material.
    "Access non-released API internally
    SELECT SINGLE * FROM mara
      WHERE matnr = @iv_matnr
      INTO @DATA(ls_mara).
    "Map to released structure
    rs_material = VALUE #(
      matnr = ls_mara-matnr
      mtart = ls_mara-mtart
      matkl = ls_mara-matkl ).
  ENDMETHOD.
ENDCLASS.
```

### Wrapper guidance

- **CDS views**: create a custom CDS view on top of the non-released SAP CDS view and release it. Association targets and value help views may need wrappers too. If no SAP CDS view exists, wrap the database table.
- **Classes/interfaces**: wrap the non-released FM or class. Do **not** copy non-released data types — wrap them via `TYPES` declarations in the wrapper's public section so only the wrapper needs releasing.
- **Authorizations**: classic APIs often check non-released authorization objects, which cannot be used in ABAP Cloud. PFCG roles can mix released and non-released authorization objects. Provide `SU22` data for the wrapper when releasing it and create `SU22` variants per designated usage.
- **ATC exemptions**: wrapping reduces N findings to 1 — create a single fine-grained exemption on the wrapper instead of one per usage. This is SAP's recommended practice for internal objects.
- **Retire wrappers**: once SAP releases the API, replace the wrapper and move the code to ABAP Cloud.

### Wrapper via RFC Proxy (side-by-side to on-stack)

```abap
"Side-by-side consumer calls a released RFC wrapper
DATA(lo_dest) = cl_rfc_destination_provider=>create_by_comm_arrangement(
  comm_scenario  = 'Z_MY_COMM_SCENARIO'
  service_id     = 'Z_MY_OUTBOUND_SRV' ).

CALL FUNCTION 'Z_WRAPPER_FM'
  DESTINATION lo_dest->get_destination_name( )
  EXPORTING iv_param = lv_value
  IMPORTING ev_result = lv_result.
```

## Object Classification Discovery

| Method                          | Description                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| **Cloudification Repository**   | `objectClassifications_SAP.json` — classic APIs, noAPI, internalAPI classifications  |
| **Cloudification API Viewer**   | Browse at https://sap.github.io/abap-atc-cr-cv-s4hc/                                 |
| **SAP Business Accelerator Hub** | Released remote and local APIs with stability contracts                             |
| **ADT: Released Object Search** | Search with `api:` prefix (e.g., `api:cl_*`), or Project Explorer → Released Objects |
| **ATC clean core checks**       | `SYCM_USAGE_OF_APIS`, `SYCM_ALLOWED_ENH_TECHNOLOGY`, `CI_SEARCH_CUST_MODIFICATIONS`  |
| **SAP Note 3578329**            | Classification of classic technologies, reuse services, application frameworks       |
| **SAP Note 3565942**            | Delivers the `Usage of APIs` and `Allowed Enhancement Technologies` ATC checks        |
| **released-abap-classes skill** | Common released classes for ABAP Cloud                                               |
| **XCO Library**                 | `XCO_CP_*` classes provide cloud-ready alternatives                                  |

Classic API classifications are provided for these object types: function modules (`FUNC`), classes (`CLAS`), interfaces (`INTF`), CDS views (`STOB`), BO interfaces (`BDEF`). DDIC objects used as data types are not classified or checked; only SQL access to SAP tables is checked.

## Common Non-Released → Released Replacements

| Non-released (Level C/D)    | Released alternative (Level A)                    |
| --------------------------- | ------------------------------------------------- |
| `AUTHORITY-CHECK`           | `CL_ABAP_AUTHORIZATION=>check_authorization()`    |
| `sy-uname`                  | `cl_abap_context_info=>get_user_technical_name()` |
| `sy-datum` / `sy-uzeit`     | `cl_abap_context_info=>get_system_date/time()`    |
| `cl_gui_frontend_services`  | Not available — use Fiori UI instead              |
| `CALL TRANSACTION`          | RAP action or Fiori navigation                    |
| `SUBMIT ... AND RETURN`     | Background job via `CL_APJ_RT_API`                |
| Direct SAP table `SELECT`   | Released CDS view (`I_*` views)                   |
| `CONVERSION_EXIT_*`         | `CL_ABAP_CONV_CODEPAGE`, domain fixed values      |
| `BAPI_*` function modules   | Released APIs or RAP BO consumption (else Level B)|
| `RFC_READ_TABLE` (noAPI)    | Released CDS view or released remote API          |
| Classic `MESSAGE` statement | RAP messages via `REPORTED`                       |

## Use Case → Level Mapping

| Category            | Use case                                                        | Level                        |
| ------------------- | --------------------------------------------------------------- | ---------------------------- |
| Extensions          | Custom field via **released** extension include                 | A                            |
| Extensions          | Implementation of a **released** SAP BAdI                       | A                            |
| Extensions          | Custom field via **non-released** extension include             | B                            |
| Extensions          | Custom field on DB table via classic append                     | C                            |
| Extensions          | Implementation of user/customer exit (e.g., `SAPMV45A`)         | B                            |
| Extensions          | Implementation of a **non-released** SAP BAdI                   | B                            |
| Extensions          | Implementation of a BAdI flagged **SAP-internal**               | D                            |
| Extensions          | Extension of a RAP-based SAP Fiori app                          | A                            |
| Extensions          | Extension of an SEGW / BOPF / UI5 SAP Fiori app                 | B                            |
| Extensions          | Extension of an SAP GUI transaction                             | B                            |
| Custom applications | Custom RAP-based SAP Fiori app (core scope)                     | A                            |
| Custom applications | Custom SEGW / BOPF / UI5 app                                    | B (prefer RAP)               |
| Custom applications | Legacy UI app (ABAP report with ALV, Web Dynpro)                | B (should be prevented)      |
| Custom applications | `SE54`-based BC UI                                              | B (prefer RAP-based BC app)  |
| Wrapper             | Wrapper class around non-released SAP object (e.g., BAPI)       | B if wrapped object is classic API, else C |
| Wrapper             | Wrapper CDS view for non-released SAP table or CDS view         | B if wrapped object is classic API, else C |
| Modifications       | SAP Note with manual corrections                                | D (reset once in core)       |
| Modifications       | Business-driven modification                                    | D (exceptional cases only)   |

## Key User vs. Developer Extensibility

Both are **Level A** when they use released extension points:

- **Key user extensibility** (no/low code): custom fields, custom logic, custom CDS views, custom business objects, custom analytical queries via Fiori apps. Start here for tightly coupled extensions — use transaction `SEEA` / the extension registry to find registered extension points.
- **Developer extensibility** (ABAP Cloud): use when key user extensibility is too limited. Full lifecycle in ADT with RAP.

## Best Practices

1. **Target Level A** — "SAP Business AI Platform first", ABAP Cloud for on-stack
2. **Classify by the lowest level used** — one internal object makes the whole extension Level C
3. **Eliminate Level D immediately** — modifications, implicit enhancements, table writes, noAPI objects
4. **Minimize Level C** — replace internal objects with released or classic APIs; monitor the changelog for SAP objects
5. **Accept Level B pragmatically** — classic APIs are upgrade-stable in practice; do not force unnecessary rewrites
6. **Wrap, don't scatter** — one wrapper with one ATC exemption beats many direct usages
7. **Govern with ATC** — global check variant, block transport release on priority 1 and 2 findings
8. **Separate software components** — ABAP Cloud component vs. `HOME` for classic

## Output Format

When helping with ABAP Cloud / clean core topics, structure responses as:

```markdown
## ABAP Cloud Guidance

### Context

- Clean core level: [A / B / C / D] (classified by the lowest level used)
- Development model: [ABAP Cloud / Classic ABAP]
- Language version: [ABAP for Cloud Development / Standard ABAP]
- Target platform: [SAP Cloud ERP / SAP Cloud ERP Private / SAP Business AI Platform]

### Recommendation

[Guidance on the approach and how to reach a higher level]

### Code Example

[ABAP code following clean core principles]

### Released API References

- [List of relevant released or classic APIs used]

### Expected ATC Findings

- [Priority and check name, if any]
```

## References

- Clean Core Extensibility Whitepaper (level concept): https://www.sap.com/documents/2023/11/2e6b5b98-957e-001e-9e9e-cbd0b2b1f1e0.html
- Extend SAP S/4HANA with ABAP-based extensions (guide): https://community.sap.com/t5/enterprise-resource-planning-blogs-by-sap/extend-sap-s-4hana-in-the-cloud-and-on-premise-with-abap-based-extensions/ba-p/13500561
- SAP Cloudification Repository: https://github.com/SAP/abap-atc-cr-cv-s4hc
- Cloudification Repository Viewer: https://sap.github.io/abap-atc-cr-cv-s4hc/
- SAP Business Accelerator Hub: https://api.sap.com/
- ABAP Cloud Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets
- Clean Core Guidelines: https://help.sap.com/docs/abap-cloud
- SAP Note 3578329 — classic technology classification
- SAP Note 3565942 — clean core ATC checks

## Detailed Reference

- **Clean core level details**: Read `references/clean-core-levels.md` for a full level-by-level comparison, decision matrix, governance setup, and remediation priorities

## Related Skills

- **abap-cloud-migration**: Use for level-based remediation of existing custom code
- **atc-cloudification**: Use for configuring ATC clean core checks and level governance
- **released-abap-classes**: Use for finding Level A released API alternatives
- **authorization-iam**: Use for authorization in ABAP Cloud and wrapper `SU22` handling
- **badi-enhancement**: Use for level classification of BAdIs and enhancement techniques
