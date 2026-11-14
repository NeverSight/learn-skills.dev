---
name: atc-cloudification
description: Configure ATC clean core and Cloud Readiness checks using the SAP Cloudification Repository, and map ATC findings to clean core levels (A, B, C, D). Use when users ask about ATC check variants for cloud readiness, clean core compliance, clean core levels, released/classic/internal/noAPI object classification, cloudification repository setup, objectReleaseInfo or objectClassifications JSON files, ATC exemptions, changelog for SAP objects, SAP Cloud ERP or SAP Cloud ERP Private API validation, or migrating custom code to ABAP Cloud. Triggers include "configure ATC cloud readiness", "set up clean core check", "cloudification repository URL", "released APIs check", "which level is this ATC finding", "ATC priority 1 clean core", "ATC exemption", "changelog for SAP objects", or "which JSON file for my S/4HANA version".
---

# ATC Clean Core & Cloudification Repository Checks

Configure ABAP Test Cockpit (ATC) clean core checks against the SAP Cloudification Repository, and map findings to **clean core levels** (A, B, C, D) for governance and remediation planning.

> The clean core level concept supersedes the former 3-tier extensibility model. ATC is the governance tool that makes levels measurable: priority 1 → Level D, priority 2 → Level C, priority 3 → Level B, no finding → Level A.

## Overview

The [SAP Cloudification Repository](https://github.com/SAP/abap-atc-cr-cv-s4hc) contains the release state and clean core classification of SAP objects. Its JSON files serve as ATC check content, enabling customers and partners to analyse custom code across all ECC and S/4HANA releases.

## Quick Reference

Read `references/quick-reference.md` for:

- JSON file URLs for each target product and version
- ATC check variant configuration steps
- Available JSON files and their purpose
- SAP Notes required for setup

## Configuration by Target Product

### SAP Cloud ERP

1. Activate in your ATC check variant: **"Cloud Readiness"** → **Usage of Released APIs (Cloudification Repository)**
2. In the check attributes, enter the URL:
   ```
   https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfoLatest.json
   ```

### SAP Cloud ERP Private

1. Activate in your ATC check variant: **"Clean Core"** → **Usage of Released APIs (Cloudification Repository)**
2. In the check attributes, enter the URL for your version:
   - **Latest version**: `https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectReleaseInfo_PCELatest.json`
   - **Specific release**: Replace `PCELatest` with the version, e.g. `PCE2025_0` for Release 2025 FPS00

### New Clean Core Check (Note 3565942)

For the newer ATC checks **"Usage of APIs"** and **"Allowed Enhancement Technologies"**, use:

```
https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/objectClassifications_SAP.json
```

## Clean Core Levels and Object Classification

Extensions are classified into clean core **levels** (A–D) based on the SAP objects they consume. An extension takes the **lowest** level of any object it uses.

> The clean core level concept supersedes the former 3-tier extensibility model.

| Clean Core Level | SAP object qualifier                                          | Meaning                                                                                          | ATC finding              |
| ---------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------ |
| **Level A**      | `[Released]` remote API, local API, extension point           | Governed by a formal **stability contract**. Target state for all new development.               | No finding               |
| **Level B**      | `[Classic]` SAP API, SAP extension point                      | SAP-nominated classic APIs and frameworks. No stability contract, but proven upgrade-stable.     | Priority 3 (information) |
| **Level C**      | `[Internal]` SAP object                                       | The **default** for any object not otherwise classified. Not released, not documented, not supported. | Priority 2 (warning)  |
| **Level D**      | `[Not recommended]` SAP object, extension point or technology | Explicitly unfit for customer use. Highest risk and technical debt.                              | Priority 1 (error)       |

**Clean core status**: Level A = clean core · Levels B and C = conditional clean core · Level D = not clean core.

### Key rules

- **Level A** (Released): use for all new development. Discover via SAP Business Accelerator Hub, Cloudification Repository, or ADT.
- **Level B** (Classic API): acceptable for classic ABAP development where no released API exists. Wrappers around classic APIs are Level B and can be released for ABAP Cloud consumption. Do not force rewrites of stable classic code.
- **Level C** (Internal): minimize. Wrap remaining usages and create a single ATC exemption. Use the **changelog for SAP objects** to detect upcoming incompatible changes.
- **Level D** (Not recommended): **eliminate immediately**. Includes `noAPI` objects, modifications, implicit/explicit enhancements, direct table writes, form routine calls, and critical ABAP statements.
- **Deprecated**: still Level A/B, but adopt the successor API.

### JSON files and states

- `objectReleaseInfo*.json` — release state of SAP objects: `released`, `deprecated`, `notToBeReleased`, `notReleased`
- `objectClassifications_SAP.json` — clean core classification: `classicAPI` (Level B), `noAPI` (Level D), `internalAPI` (Level C with a released successor available)
- Labels: `remote-enabled` (RFC-enabled), `transactional-consistent` (usable inside RAP-based applications)

Classified object types: `FUNC` (function modules), `CLAS` (classes), `INTF` (interfaces), `STOB` (CDS views), `BDEF` (BO interfaces).

DDIC objects (data elements, structures, table types) are **not** classified and are not checked when used as data types. Only SQL access to SAP tables is checked.

## ATC Clean Core Checks

Configure a single **global check variant** used during development and on transport release. Set ATC transport settings so **priority 1 and 2 findings block release**.

| Check                                | Category                 | Technical name                  | Purpose                                                                                     |
| ------------------------------------ | ------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------- |
| **Usage of APIs**                    | Clean core               | `SYCM_USAGE_OF_APIS`            | Released/classic API classification, SQL on SAP tables and views, calls to SAP form routines |
| **Allowed enhancement technologies** | Clean core               | `SYCM_ALLOWED_ENH_TECHNOLOGY`   | Reports `ENHO` enhancements on non-allowed technology. Only BAdIs are recommended.           |
| **Search customer modifications**    | Clean core               | `CI_SEARCH_CUST_MODIFICATIONS`  | Finds modified objects (one finding per object); checks ABAP Cloud object type support       |
| **Critical statements**              | Clean core               | `CI_CRITICAL_STATEMENTS`        | Statements critical for security or program stability (kernel calls, `EXEC SQL`, …)          |
| **Code Vulnerability Analyzer**      | Additionally recommended | `SLIN_SEC`                      | Security vulnerabilities                                                                     |

> If **Usage of APIs** or **Allowed Enhancement Technologies** is missing, implement **SAP Note 3565942**.

### Check variant templates

- `ABAP_CLEAN_CORE_DEVELOPMENT` — SAP-delivered predefined variant for initial setup
- `ABAP_CLOUD_DEVELOPMENT_DEFAULT` — template to enrich with the checks above
- `ABAP_CLOUD_READINESS` — verify ABAP Cloud rules before switching an object's language version

### Central ATC system

Set up a central ATC system for the whole landscape:
- Public cloud solution on **SAP BTP** — SAP's recommended option
- Or installed in the private cloud / on-premise landscape

### ATC findings mapped to levels

| ATC priority             | Level | Finding                                                                          | Recommended action                                 |
| ------------------------ | ----- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Priority 1 (Error)**   | **D** | Object is modified                                                               | Remove modification; use a BAdI instead            |
|                          |       | Enhancement technology is not allowed                                            | Delete enhancement implementation; use a BAdI      |
|                          |       | Implicit or explicit enhancement (source code plug-in)                           | Delete enhancement implementation; use a BAdI      |
|                          |       | Direct **write** access to SAP database tables                                   | Use released or classic APIs                       |
|                          |       | Call of form routines in SAP program                                             | Use released or classic APIs                       |
|                          |       | Usage of SAP object classified as `noAPI`                                         | Use released or classic APIs; use successor info   |
|                          |       | Usage of critical ABAP statements                                                | Use released or classic APIs                       |
| **Priority 2 (Warning)** | **C** | Direct **read** access to SAP database table/view                                | Use released CDS view or classic API               |
|                          |       | Usage of SAP object not classified as classic API (internal) and not released    | Use released or classic APIs                       |
| **Priority 3 (Info)**    | **B** | Usage of deprecated APIs                                                         | Use the successor instead                          |
|                          |       | Usage of classic APIs                                                            | — acceptable, no action required                   |

### Critical statements covered

`CI_CRITICAL_STATEMENTS` reports: kernel function calls · system-calls · editor calls · `EXEC SQL` · database hints · generation of reports and Dynpros · read/insert report · read/insert Dynpro · import/export nametab.

## Exemption Strategy

- Focus exemptions on **priority 1 (Error)** and **priority 2 (Warning)** findings
- **Do not** exempt priority 3 (Info) findings such as classic API usage
- Use **fine-granular, finding-level** exemptions for clean core findings — best governance
- Use an **ATC baseline** only for legacy code you will not change, to hide a large set of findings
- **Preferred practice**: wrap the SAP object and consume the wrapper. N findings collapse to 1, so one exemption suffices
- Monitor adoption via the **ATC exemption browser**

## Changelog for SAP Objects (Level C mitigation)

Internal SAP objects can change during an upgrade, feature pack import, or even an SAP Note import. The changelog proactively lists objects with **incompatible changes** in upcoming releases.

Incompatible changes include: deletion of objects · renaming or deletion of function module parameters · incompatible parameter type changes · renaming or deletion of methods in SAP classes · removal of fields from CDS views.

Covered object types: `FUNC`, `CLAS`, `INTF`, `STOB`, `BDEF`.

**Setup:**
1. Download the Simplification Database file from the SAP Software Download Center (SAP Support Portal)
2. Import via transaction `SYCM`
3. Run the changelog ATC check during development, or before the upgrade like other simplification item checks

Objects in the changelog are **not** automatically demoted to Level D — continued usage may be allowed depending on the change's criticality. Use findings to drive refactoring toward released or classic APIs.

## Workflow

1. **Determine the target product**: SAP Cloud ERP or SAP Cloud ERP Private
2. **Identify the correct JSON file** using the quick reference
3. **Verify prerequisites**: implement SAP Note 3565942 (clean core checks) and review SAP Note 3578329 (classic technology classification)
4. **Set up a central ATC system** (SAP BTP recommended)
5. **Configure one global check variant** with the clean core checks and JSON URL
6. **Configure transport settings** so priority 1 and 2 findings block transport release
7. **Import the changelog for SAP objects** via `SYCM` for Level C risk assessment
8. **Run ATC checks** on custom code
9. **Map findings to levels** (P1→D, P2→C, P3→B) and determine the current overall level
10. **Plan remediation**: eliminate Level D, minimize Level C, monitor Level B, target Level A
11. **Govern residual usage** with fine-grained exemptions on wrappers

## Output Format

When helping with ATC clean core topics, structure responses as:

```markdown
## ATC Clean Core Guidance

### Configuration

- Target product: [SAP Cloud ERP / SAP Cloud ERP Private]
- JSON file: [URL]
- Check variant: [name and included checks]

### Finding Classification

| ATC finding | Priority | Clean core level | Action |
|-------------|----------|------------------|--------|
| ... | ... | ... | ... |

### Remediation Plan

[Ordered: Level D first, then C, then B]

### Exemption Recommendations

[Which findings justify an exemption and why]
```

## Cloudification API Viewer

Use the online viewers to browse object classifications interactively:

- **SAP Cloud ERP** (release info): https://sap.github.io/abap-atc-cr-cv-s4hc/
- **SAP Cloud ERP Private** (release info): https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectReleaseInfo_PCELatest.json
- **Clean core classification** (classic APIs / `noAPI` / `internalAPI`): https://sap.github.io/abap-atc-cr-cv-s4hc/?version=objectClassifications_SAP.json

Filter by `state`:
- `classicAPI` → Level B candidates
- `internalAPI` → Level C with a released successor available
- `noAPI` → Level D, must be replaced

## References

- Clean Core Extensibility Whitepaper — clean core level concept
- Extend SAP S/4HANA in the cloud and on premise with ABAP based extensions (Version 2.3, August 2025)
- Cloudification Repository: https://github.com/SAP/abap-atc-cr-cv-s4hc
- SAP Note 3565942 — delivers `SYCM_USAGE_OF_APIS` and `SYCM_ALLOWED_ENH_TECHNOLOGY`
- SAP Note 3578329 — classification of classic technologies, reuse services and frameworks

## Related Skills

- **abap-cloud**: Use for clean core level definitions, development models, and wrapper classification
- **abap-cloud-migration**: Use for level-based remediation guidance after running ATC checks
- **released-abap-classes**: Use for finding Level A released API replacements identified by ATC
- **badi-enhancement**: Use for replacing Level D modifications and enhancements with BAdIs
