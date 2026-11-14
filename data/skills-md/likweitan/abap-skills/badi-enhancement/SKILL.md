---
name: badi-enhancement
description: Help with BAdI (Business Add-In) development, the ABAP enhancement framework, and the clean core level classification of enhancement techniques. Covers new BAdIs, fallback classes, filter-based BAdIs, enhancement spots, enhancement implementations, key user extensibility, classic BAdIs, allowed vs. non-allowed enhancement technologies, and replacing modifications and implicit enhancements. Use when users ask about BAdI, BAdIs, Business Add-In, enhancement spot, enhancement implementation, enhancement framework, BAdI filter, BAdI fallback, BAdI definition, BAdI implementation, key user extensibility, custom logic injection, enhancement point, implicit enhancement, explicit enhancement, allowed enhancement technologies, user exit, customer exit, modification, or extending SAP standard code. Triggers include "create a BAdI", "implement a BAdI", "enhancement spot", "find a BAdI", "BAdI filter", "fallback class", "key user extensibility", "extend standard", "enhancement framework", "replace modification", "implicit enhancement", or "which level is this enhancement".
---

# BAdI & Enhancement Framework

Guide for using BAdIs (Business Add-Ins) and the ABAP enhancement framework to extend SAP standard functionality, with clean core **level** classification for each technique.

> BAdIs are the **only** recommended enhancement technology under the clean core level concept. The ATC check `SYCM_ALLOWED_ENH_TECHNOLOGY` reports `ENHO` enhancements built on any other technology as a **priority 1 (Level D)** finding.

## Workflow

1. **Determine the user's goal**:
   - Finding an existing BAdI to implement
   - Creating a custom BAdI definition
   - Implementing a BAdI
   - Replacing a modification or implicit enhancement with a BAdI
   - Understanding classic vs. new enhancement framework
   - Using key user extensibility
   - Classifying an enhancement's clean core level

2. **Identify the framework**:
   - New BAdI framework (preferred, ABAP Cloud compatible)
   - Classic BAdI framework (legacy, `SE18`/`SE19`)
   - Enhancement spots and implementations
   - Key user extensibility (no-code)

3. **Classify the clean core level** using the table below

4. **Guide implementation** toward the highest applicable level

## Clean Core Level by Enhancement Technique

| Technique                             | Level | Guidance                                                                                              |
| ------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------- |
| **Key user extensibility**            | **A** | Start here for tightly coupled extensions — custom fields, custom logic, custom CDS views             |
| **Released BAdI**                     | **A** | Preferred code-based extension point                                                                  |
| **Released extension include**        | **A** | Preferred technique for custom fields on DB tables and CDS views                                      |
| **Released extension point / RAP BO** | **A** | Use for extending RAP-based SAP Fiori apps                                                            |
| **CDS extends / metadata extensions** | **A/B** | Extend SAP CDS views rather than modifying them                                                     |
| **Non-released BAdI**                 | **B** | Good choice for classic extensions even when not released for cloud development. Monitor for release  |
| **User exits** (VOFM, `SAPMV45A`)     | **B** | Predefined SAP coding parts are stable and typically survive upgrades. Technically a modification     |
| **Customer exits** (SMOD/CMOD)        | **B** | Predecessor of BAdIs. Use only where no BAdI exists — likely to be replaced in future releases        |
| **Non-released extension include**    | **B** | Acceptable; monitor when a released extension include becomes available                               |
| **DDIC appends** (CI / EEW includes)  | **B** | Append fields via customer includes or extension includes                                             |
| **Domain value appends, search help appends/exits** | **B** | Acceptable classic extension techniques                                               |
| **OData service redefinition**        | **B** | Redefine rather than modify                                                                           |
| **Classic append on DB table**        | **C** | Monitor when an extension include becomes available and adapt accordingly                             |
| **Explicit enhancement spots**        | **B/D** | Exceptional cases only, to include a custom BAdI. **Do not** place extension code directly in the spot |
| **Implicit enhancement spots**        | **D** | Similar to a modification — **do not use**                                                            |
| **Source code plug-ins**              | **D** | ATC priority 1 finding — delete and use a BAdI                                                        |
| **SAP-internal-flagged BAdI**         | **D** | Exceptional cases only                                                                                |
| **Modifications**                     | **D** | Avoid completely. If unavoidable, use the modification assistant and govern via ATC                   |

**General rule**: no modifications to SAP objects. Where a modification exists, check whether a released or classic BAdI can replace it.

### ATC governance

| ATC check                        | Technical name                 | Reports                                                                          |
| -------------------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
| Allowed enhancement technologies | `SYCM_ALLOWED_ENH_TECHNOLOGY`  | `ENHO` enhancements on non-allowed technology — only BAdIs are recommended       |
| Search customer modifications    | `CI_SEARCH_CUST_MODIFICATIONS` | Modified objects (one finding per object); checks ABAP Cloud object type support |

Both produce **priority 1 (error)** findings, corresponding to Level D. Implement **SAP Note 3565942** if these checks are unavailable.

## BAdI Framework Overview

### New vs. Classic BAdIs

| Aspect               | New BAdI Framework              | Classic BAdI Framework |
| -------------------- | ------------------------------- | ---------------------- |
| **Transactions**     | ADT or `SE18`/`SE19`            | `SE18`/`SE19`          |
| **Enhancement Spot** | Required container              | Not applicable         |
| **Multiple Use**     | Always multiple-use             | Configurable           |
| **Filter**           | Filter types supported          | Filter values          |
| **Fallback Class**   | Supported                       | Not available          |
| **ABAP Cloud**       | Supported (released BAdIs only) | Not available          |
| **Clean core level** | A if released, else B           | B (or D if SAP-internal-flagged) |
| **Recommendation**   | Use for all new development     | Maintain existing only |

## Creating a Custom BAdI

### Step 1: Create Enhancement Spot

```
ADT: New → Other ABAP Repository Object → Enhancements → Enhancement Spot
Name: Z_ENH_SPOT_TRAVEL
```

### Step 2: Define the BAdI Interface

```abap
INTERFACE zif_badi_travel_validate
  PUBLIC.
  METHODS validate
    IMPORTING
      is_travel       TYPE zstravel
    CHANGING
      ct_messages     TYPE bapiret2_t
    RAISING
      cx_badi_not_implemented.
ENDINTERFACE.
```

### Step 3: Define the BAdI in Enhancement Spot

In the enhancement spot, add a BAdI definition:

| Property           | Value                                 |
| ------------------ | ------------------------------------- |
| **BAdI Name**      | `ZBADI_TRAVEL_VALIDATE`               |
| **Interface**      | `ZIF_BADI_TRAVEL_VALIDATE`            |
| **Multiple Use**   | Yes (allows multiple implementations) |
| **Fallback Class** | `ZCL_BADI_TRAVEL_FALLBACK` (optional) |

### Step 4: Create Fallback Class (Optional)

```abap
CLASS zcl_badi_travel_fallback DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_travel_validate.
ENDCLASS.

CLASS zcl_badi_travel_fallback IMPLEMENTATION.
  METHOD zif_badi_travel_validate~validate.
    "Default behavior when no implementation is active
  ENDMETHOD.
ENDCLASS.
```

### Step 5: Call the BAdI in Your Code

```abap
"Get BAdI handle
DATA lo_badi TYPE REF TO zif_badi_travel_validate.

GET BADI lo_badi.

"Call BAdI — loops through all active implementations
CALL BADI lo_badi->validate
  EXPORTING is_travel   = ls_travel
  CHANGING  ct_messages = lt_messages.
```

### With Filters

```abap
"Define BAdI with filter
"In Enhancement Spot: add filter type COUNTRY (type LAND1)

"Get BAdI with filter
GET BADI lo_badi
  FILTERS country = ls_travel-country.

CALL BADI lo_badi->validate
  EXPORTING is_travel   = ls_travel
  CHANGING  ct_messages = lt_messages.
```

## Implementing an Existing BAdI

### Step 1: Find the BAdI

Methods to find a BAdI:

- **ADT search**: Search for BAdI name or enhancement spot
- **Transaction `SE18`**: Browse BAdI definitions
- **Breakpoint on `GET BADI`**: Set breakpoint at `CL_BADI_INTERNAL_FACTORY=>GET_BADI` to find BAdIs called during a process
- **Documentation**: Check SAP documentation or community for BAdI names

### Step 2: Create Enhancement Implementation

```
ADT: New → Other ABAP Repository Object → Enhancements → Enhancement Implementation
Name: Z_ENH_IMPL_TRAVEL_CHECK
Enhancement Spot: Z_ENH_SPOT_TRAVEL (or SAP's spot)
```

### Step 3: Create BAdI Implementation Class

```abap
CLASS zcl_badi_impl_travel_check DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES zif_badi_travel_validate.
ENDCLASS.

CLASS zcl_badi_impl_travel_check IMPLEMENTATION.
  METHOD zif_badi_travel_validate~validate.
    "Custom validation logic
    IF is_travel-begin_date < cl_abap_context_info=>get_system_date( ).
      APPEND VALUE #(
        type       = 'E'
        id         = 'Z_TRAVEL'
        number     = '001'
        message_v1 = 'Travel begin date must be in the future'
      ) TO ct_messages.
    ENDIF.
  ENDMETHOD.
ENDCLASS.
```

## BAdIs in ABAP Cloud / RAP

In ABAP for Cloud Development, BAdIs follow a specific pattern:

### Released BAdIs — Level A

- Only SAP-released BAdIs can be implemented in ABAP Cloud
- Search for released BAdIs in ADT: `api:badi`
- Common in RAP scenarios for extending standard RAP BOs
- Verify release state programmatically:

```abap
SELECT SINGLE *
  FROM i_apistateofrepositoryobject
  WHERE ObjectType   = 'SXSD'          "BAdI definition
    AND ObjectName   = 'MY_BADI'
    AND ReleaseState = 'RELEASED'
  INTO @DATA(ls_state).
```

### RAP BAdI Pattern

```abap
"BAdI for extending SAP Fiori apps / RAP BOs
"Implement the released BAdI interface
CLASS zcl_my_rap_badi DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_some_released_badi.
ENDCLASS.

CLASS zcl_my_rap_badi IMPLEMENTATION.
  METHOD if_some_released_badi~some_method.
    "Custom logic
  ENDMETHOD.
ENDCLASS.
```

### Dynamic BAdI Calls

```abap
"Dynamic GET BADI with BAdI name in variable
DATA lo_badi TYPE REF TO cl_badi_base.
DATA(lv_badi_name) = 'ZBADI_MY_BADI'.

GET BADI lo_badi TYPE (lv_badi_name).

"Dynamic CALL BADI with method name in variable
CALL BADI lo_badi->('VALIDATE')
  EXPORTING is_data = ls_data.
```

## Enhancement Spots and Implementations

Beyond BAdIs, the enhancement framework supports the techniques below. **Note the clean core level of each** — most are Level D and must be avoided.

### Explicit Enhancement Points — Level B/D

SAP defines explicit points in standard code where custom logic can be inserted. These were mainly created to enable industry-specific adaptations.

**Guidance**: use only in exceptional cases, and only to include a custom-defined BAdI into the SAP core. Do **not** place extension code directly in the enhancement spot.

```abap
"In SAP standard code:
ENHANCEMENT-POINT z_enh_point SPOTS z_enh_spot.

"In your enhancement implementation:
ENHANCEMENT z_my_enhancement.
  "Preferred: delegate to a custom BAdI rather than inlining logic
  DATA lo_badi TYPE REF TO zif_badi_my_logic.
  GET BADI lo_badi.
  CALL BADI lo_badi->process CHANGING cs_data = ls_data.
ENDENHANCEMENT.
```

### Explicit Enhancement Sections — Level B/D

```abap
"SAP code with replaceable section:
ENHANCEMENT-SECTION z_section SPOTS z_enh_spot.
  "Default code (can be replaced)
  lv_result = lv_a + lv_b.
END-ENHANCEMENT-SECTION.

"Your replacement:
ENHANCEMENT z_my_section_impl.
  "Custom replacement code
  lv_result = lv_a * lv_b.
ENDENHANCEMENT.
```

### Implicit Enhancements — Level D, do not use

Implicit enhancement points (at the start/end of methods, forms, programs) are technically equivalent to modifications. `SYCM_ALLOWED_ENH_TECHNOLOGY` reports them as **priority 1 (error)** findings.

**Remediation**: delete the enhancement implementation and use a released or classic BAdI instead.

### Modifications — Level D, avoid completely

If a modification cannot be prevented:
- Use the **modification assistant** so post-upgrade adjustment stays manageable
- Govern via the `CI_SEARCH_CUST_MODIFICATIONS` ATC check
- Reset modifications from SAP Notes once the correction is part of the core

**Remediation**: check whether a released or classic BAdI can replace the modification.

### User Exits and Customer Exits — Level B

- **User exits** (VOFM, `SAPMV45A`): predefined SAP coding parts (form routines, includes) in an SAP namespace. Stable and typically survive upgrades, though technically treated as modifications. Monitor whether a released BAdI can replace them.
- **Customer exits** (SMOD/CMOD): the predecessor technology to BAdIs. Usable in exceptional cases where no BAdI exists yet; most will be replaced in upcoming releases.

## Structural Extension Techniques

Beyond business logic, these techniques extend SAP data structures and services:

### DDIC — Level A/B/C

- **Released extension includes** (EEW) → **Level A**, preferred
- **Customer includes** (CI includes) on non-released structures/tables → **Level B**
- **Classic appends** on DB tables → **Level C**; monitor for a released extension include
- Domain value appends, search help appends, search help exits → **Level B**

### CDS — Level A/B

- Use **CDS extends** rather than modifying SAP CDS views
- Use **CDS metadata extensions** for UI annotation changes

### OData — Level B

- Use **redefinition** of OData services rather than modification

## Key User Extensibility — Level A

No-code/low-code extension capabilities available via SAP Fiori. This is the **starting point** for tightly coupled extensions.

| Capability                    | Description                                 |
| ----------------------------- | ------------------------------------------- |
| **Custom Fields**             | Add fields to standard business objects     |
| **Custom Logic**              | Add validation/determination logic via BRF+ |
| **Custom CDS Views**          | Create simple analytical views              |
| **Custom Business Objects**   | Create simple transactional objects         |
| **Custom Analytical Queries** | Build queries on existing CDS views         |

**Finding extension points**: use the extension registry (transaction `SEEA` / the extension point registry) to find every extension point registered in the system.

When a requirement is too complex for key user extensibility, move to **developer extensibility** (ABAP Cloud) — still Level A.

## Replacing Level D Enhancements

| Existing Level D technique                  | Replacement                                                             |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| Modification                                | Released BAdI → classic BAdI → key user extensibility                   |
| Implicit enhancement                        | Released BAdI → classic BAdI                                            |
| Explicit enhancement with inline code       | Move the code into a custom BAdI called from the enhancement            |
| Source code plug-in                         | Released or classic BAdI                                                |
| SAP-internal-flagged BAdI implementation    | Find an alternative released or classic extension point                 |
| SAP Note manual correction                  | Reset the modification once the correction ships in the core            |

**Remediation workflow:**
1. Run `SYCM_ALLOWED_ENH_TECHNOLOGY` and `CI_SEARCH_CUST_MODIFICATIONS`
2. For each priority 1 finding, search for a released BAdI (`api:badi` in ADT)
3. If no released BAdI exists, search for a classic BAdI (Level B)
4. If neither exists, consider key user extensibility or a custom BAdI in an explicit enhancement spot
5. Delete the Level D implementation and migrate the logic
6. Re-run ATC to confirm the finding is resolved

## Best Practices

1. **BAdIs are the only recommended enhancement technology** — everything else is Level B at best
2. **Prefer released BAdIs (Level A)** over non-released BAdIs (Level B)
3. **Prefer new BAdI framework** over classic BAdIs
4. **Never use implicit enhancements or modifications** (Level D)
5. **Start with key user extensibility (Level A)** for tightly coupled extensions
6. **Use filters** to scope implementations to specific contexts
7. **Implement fallback classes** for default behavior
8. **Keep implementations focused** — one concern per implementation
9. **Document the BAdI** with clear interface documentation
10. **Test implementations** independently using ABAP Unit
11. **In ABAP Cloud**, only implement released BAdIs
12. **Govern with ATC** — block transport release on priority 1 and 2 findings

## Output Format

When helping with BAdI/enhancement topics, structure responses as:

```markdown
## BAdI / Enhancement Guidance

### Framework

- Type: [New BAdI / Classic BAdI / Enhancement Spot / Key User]
- Clean core level: [A / B / C / D]
- Context: [ABAP Cloud / Classic ABAP]

### Implementation

[Step-by-step with code examples]

### Expected ATC Findings

- [Check name, priority, and level, if any]

### Testing

[How to verify the enhancement works]
```

## References

- Clean Core Extensibility Whitepaper — clean core level concept
- Extend SAP S/4HANA in the cloud and on premise with ABAP based extensions (Version 2.3, August 2025)
- BAdI Cheat Sheet: https://github.com/SAP-samples/abap-cheat-sheets/blob/main/35_BAdIs.md
- Enhancement Framework: https://help.sap.com/docs/abap-cloud/abap-development-tools-user-guide/enhancement
- Key User Extensibility: https://help.sap.com/docs/sap-s4hana-cloud/extensibility
- SAP Note 3565942 — delivers `SYCM_ALLOWED_ENH_TECHNOLOGY`

## Detailed Reference

- **BAdI patterns**: Read `references/badi-patterns.md` for implementation patterns, filters, fallback classes, and testing

## Related Skills

- **abap-cloud**: Use for clean core level definitions and which BAdIs are released
- **abap-cloud-migration**: Use for replacing Level D modifications and enhancements
- **atc-cloudification**: Use for configuring `SYCM_ALLOWED_ENH_TECHNOLOGY` governance
- **rap**: Use for implementing released RAP BAdIs for SAP Fiori apps
- **authorization-iam**: Use for setting up authorizations for enhanced functionality
