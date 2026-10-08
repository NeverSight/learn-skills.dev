---
name: risk-adjustment-strategy
description: >
  Reasoning skill for CMS-HCC risk adjustment strategy and methodology. Use when the user asks
  about CMS-HCC model versions V24 or V28, blended transition methodology, ICD-10-to-HCC
  mapping logic, disease interaction hierarchies, RAF score methodology, risk adjustment factor
  calculation, coding gap identification, audit-defensible documentation, HCC recapture strategy,
  prospective vs retrospective risk adjustment, or Medicare Advantage risk scoring. Triggers
  include "CMS-HCC", "V24", "V28", "blended transition", "HCC mapping", "disease hierarchy",
  "RAF score", "risk adjustment", "coding gap", "HCC recapture", "chart review", "audit
  defensible", "risk score methodology", "Medicare Advantage risk", "capitation revenue",
  "hierarchical condition category".
usage: Invoke when reasoning about CMS-HCC risk adjustment strategy, model version selection, coding gap identification, or audit-defensible documentation requirements.
version: 1.0.0
tags: [skill, category:reasoning, risk-adjustment, hcc, hcls]
---

# Risk Adjustment Strategy — Reasoning Skill

## Overview

Guide the agent through CMS-HCC risk adjustment methodology, model version differences,
hierarchy resolution, coding gap identification, and audit-defensible documentation
requirements. This skill encodes regulatory and actuarial knowledge for risk adjustment
programs, primarily Medicare Advantage (Part C).

## Usage

- Reason about CMS-HCC model versions (V24/V28), blended transition, and hierarchy resolution
- Identify coding gaps and design audit-defensible recapture strategies

## Core Concepts

---

## Response Format

- Lead with the direct recommendation or classification (≤3 sentences)
- Structure as: recommendation → justification (citing specific criteria/thresholds) → caveats
- Use tables for comparisons; bullet points for criteria lists
- Omit background the user already knows — they asked the question
- Target: 200-400 words unless the user requests exhaustive detail
The decision trees and frameworks in this skill are for internal reasoning only. Apply them to reach your conclusion, but do not reproduce them in your response. Present only the final recommendation with supporting evidence.


## 1. CMS-HCC Model Overview

### What Is Risk Adjustment?

CMS pays Medicare Advantage (MA) plans a capitated amount per member per month. The payment
is adjusted based on the member's health status, measured by diagnoses submitted on claims.
Sicker members generate higher payments (higher RAF scores). The CMS-HCC model translates
ICD-10-CM diagnosis codes into Hierarchical Condition Categories (HCCs) and calculates a
Risk Adjustment Factor (RAF) score.

### RAF Score Formula

```
RAF = demographic_coefficient
    + SUM(hcc_coefficients for all active HCCs after hierarchy resolution)
    + SUM(disease_interaction_terms)
    + coding_intensity_adjustment (negative, applied by CMS)
```

### Model Versions

| Attribute | V24 (Legacy) | V28 (Current) |
|---|---|---|
| Number of HCCs | 86 | 115 |
| Payment year | Through 2023 (blended 2024–2025) | 2026+ (full weight) |
| Key additions | — | Substance use disorders, social determinants proxies, expanded mental health |
| Key removals | — | Some lower-severity HCCs consolidated |
| Coefficient source | 2015–2016 FFS data | 2017–2018 FFS data |
| Coding intensity adj. | -5.90% (2024) | Built into coefficients |

### Blended Transition Schedule (2024–2025)

| Payment Year | V24 Weight | V28 Weight |
|---|---|---|
| 2024 | 67% | 33% |
| 2025 | 33% | 67% |
| 2026+ | 0% | 100% |

**Implication**: During the transition, BOTH models must be run and blended. A diagnosis that
maps to an HCC in V24 but not V28 (or vice versa) has partial payment impact.

---

## 2. ICD-10-to-HCC Mapping

### Mapping Pipeline

```
ICD-10-CM code
  → CMS crosswalk → Condition Category (CC)
    → Hierarchy resolution → HCC (only highest-severity CC in each hierarchy retained)
      → Coefficient lookup → RAF contribution
```

### Mapping Rules

1. **Only specific ICD-10 codes map to CCs**. Many ICD-10 codes have no CC mapping and
   contribute nothing to the RAF score.
2. **Multiple ICD-10 codes can map to the same CC**. Any one qualifying code is sufficient.
3. **CCs are grouped into hierarchies**. Within each hierarchy, only the highest-severity CC
   is retained as an HCC.
4. **Diagnoses must be from face-to-face encounters** with acceptable provider types
   (physician, NP, PA, etc.). Lab-only or radiology-only encounters do NOT qualify.
5. **Diagnoses must be submitted annually**. HCCs do not carry forward year-to-year
   (except for certain conditions in the ESRD model).

### Example Hierarchy: Diabetes

| CC | Description | Hierarchy Position | V24 Coefficient (Community, Non-Dual, Aged) |
|---|---|---|---|
| 17 | Diabetes with Acute Complications | Highest | 0.368 |
| 18 | Diabetes with Chronic Complications | ↓ | 0.368 |
| 19 | Diabetes without Complication | Lowest | 0.118 |

**Rule**: If a member has both CC 17 and CC 19, only CC 17 (HCC 17) is retained. CC 19 is
"hierarchied off."

### Common Hierarchies to Know

| Hierarchy Group | CCs (V24, highest → lowest) | Clinical Area |
|---|---|---|
| Diabetes | 17 → 18 → 19 | Endocrine |
| Heart Failure | 85 → 86 → 87 | Cardiovascular |
| COPD | 111 → 112 | Pulmonary |
| Renal | 136 → 137 → 138 | Nephrology |
| Cancer | 8 → 9 → 10 → 11 → 12 | Oncology |
| Vascular | 107 → 108 | Cardiovascular |

---

## 3. Disease Interaction Terms

### What Are Interactions?

CMS recognizes that certain combinations of HCCs have a greater-than-additive cost impact.
Interaction terms add additional RAF points when specific HCC pairs (or groups) co-occur.

### Key Interaction Terms (V24)

| Interaction | HCCs Required | Additional Coefficient |
|---|---|---|
| Diabetes + CHF | HCC 17/18 + HCC 85/86 | +0.154 |
| CHF + COPD | HCC 85/86 + HCC 111/112 | +0.175 |
| CHF + Renal | HCC 85/86 + HCC 136/137/138 | +0.154 |
| Diabetes + CHF + COPD | HCC 17/18 + HCC 85/86 + HCC 111/112 | +0.047 (additional) |
| Cancer + Immune | HCC 8/9/10/11/12 + HCC 47 | +0.190 |

**Rule**: Interaction terms are ONLY applied if the component HCCs survive hierarchy
resolution. If a higher-severity CC in the same hierarchy replaces a component, re-check
whether the interaction still qualifies.

---

## 4. Coding Gap Identification

### What Is a Coding Gap?

A coding gap exists when clinical evidence suggests a condition is present, but no qualifying
ICD-10 code has been submitted on a face-to-face claim in the current payment year.

### Identification Methods

#### 4a. Rx Proxy Analysis

| Medication (Rx) | Suspected Condition | Target HCC (V24) |
|---|---|---|
| Metformin, glipizide, insulin | Diabetes mellitus | HCC 19 (or 17/18 with complications) |
| Statins (atorvastatin, rosuvastatin) | Hyperlipidemia | No HCC (but may indicate vascular disease) |
| Lisinopril, losartan | Hypertension | No HCC (but may indicate CHF, renal disease) |
| Furosemide, spironolactone | Heart failure | HCC 85/86/87 |
| Albuterol, fluticasone/salmeterol | COPD or asthma | HCC 111/112 |
| Donepezil, memantine | Dementia | HCC 51/52 |
| Warfarin, apixaban | Atrial fibrillation or DVT/PE | HCC 96 or 107/108 |
| Methotrexate, adalimumab | Rheumatoid arthritis | HCC 40 |

**Rule**: Rx proxies identify SUSPECTED gaps. They are NOT sufficient for coding — a provider
must document and code the condition on a qualifying encounter.

#### 4b. Lab Proxy Analysis

| Lab Result | Suspected Condition | Target HCC |
|---|---|---|
| HbA1c ≥ 6.5% | Diabetes mellitus | HCC 19+ |
| eGFR < 60 mL/min | Chronic kidney disease | HCC 136/137/138 |
| BNP > 100 pg/mL | Heart failure | HCC 85/86/87 |
| TSH > 10 mIU/L | Hypothyroidism | No HCC |
| BMI ≥ 40 | Morbid obesity | HCC 22 |

#### 4c. Historical Diagnosis Analysis

Conditions documented in the prior year but not yet recaptured in the current year.

**Decision tree for gap prioritization**:
```
Is the condition chronic (expected to persist year-over-year)?
 ├─ YES
 │   ├─ Was it documented in the prior year?
 │   │   ├─ YES → High-priority recapture gap
 │   │   └─ NO → New gap identified by Rx/lab proxy
 │   └─ Does it map to an HCC?
 │       ├─ YES → Revenue-impacting gap → prioritize
 │       └─ NO → Clinical gap only → lower priority for risk adjustment
 └─ NO (acute condition)
     └─ Do NOT assume recapture; only code if currently active
```

---

## 5. Audit-Defensible Documentation

### CMS Audit Requirements (RADV)

CMS conducts Risk Adjustment Data Validation (RADV) audits to verify that submitted diagnoses
are supported by medical record documentation.

### Documentation Must Support

1. **The specific ICD-10 code submitted** — not just the general condition category.
2. **Face-to-face encounter** with an acceptable provider type.
3. **Assessment, monitoring, evaluation, or treatment** of the condition during the encounter.
4. **Date of service** matching the claim.
5. **Provider signature** (or authenticated electronic signature).

### Documentation Decision Tree

```
Does the medical record contain:
 ├─ A face-to-face encounter note? → If NO, diagnosis is NOT audit-defensible
 ├─ Provider signature/authentication? → If NO, not defensible
 ├─ The condition listed in the assessment/plan? → If NO, not defensible
 ├─ Evidence of evaluation or management of the condition?
 │   (e.g., medication review, test ordering, counseling)
 │   → If NO, not defensible (listing alone is insufficient)
 └─ Specificity matching the ICD-10 code?
     (e.g., "diabetes with nephropathy" for E11.21, not just "diabetes")
     → If NO, code must be downgraded to the supported specificity level
```

### Common Documentation Failures

| Failure | Example | Risk |
|---|---|---|
| Problem list only | Diabetes on problem list but not addressed in note | HCC deleted on audit |
| Cloned notes | Identical assessment across multiple visits | All HCCs at risk |
| Unspecified codes | E11.9 (diabetes unspecified) when complications exist | Missed higher HCC |
| Missing laterality | I63.511 vs I63.512 (stroke, right vs left) | Code rejected |
| Resolved conditions | "History of cancer" coded as active cancer | HCC deleted + penalty |
| Missing provider type | Diagnosis from lab-only encounter | Does not qualify |

---

## 6. Recapture Strategy

### Annual Recapture Workflow

1. **Identify prior-year HCCs**: Pull all HCCs from the prior payment year.
2. **Check current-year claims**: Which HCCs have already been recaptured?
3. **Flag gaps**: Prior-year HCCs not yet recaptured = recapture opportunities.
4. **Prioritize by RAF impact**: Sort gaps by coefficient value (highest first).
5. **Schedule encounters**: Coordinate with care management to ensure face-to-face visits
   address open gaps.
6. **Validate documentation**: After encounter, verify the note supports the specific ICD-10 code.

### Recapture Prioritization Matrix

| Priority | Criteria | Action |
|---|---|---|
| Critical | HCC coefficient > 0.3 AND chronic condition | Schedule dedicated visit or ensure addressed at next visit |
| High | HCC coefficient 0.15–0.3 AND chronic | Address at next scheduled visit |
| Medium | HCC coefficient < 0.15 AND chronic | Address opportunistically |
| Low | Acute condition from prior year | Do NOT recapture unless condition is still active |

### Timing Considerations

| Quarter | Strategy |
|---|---|
| Q1 (Jan–Mar) | Begin recapture for highest-value HCCs; schedule annual wellness visits |
| Q2 (Apr–Jun) | Mid-year gap report; target members with no visits yet |
| Q3 (Jul–Sep) | Escalate outreach for members with open high-value gaps |
| Q4 (Oct–Dec) | Final sweep; focus on members with scheduled visits remaining |

---

## 7. Model Selection During Transition

### Decision Framework for 2024–2025

```
Which model version should I optimize for?
 ├─ Payment year 2024?
 │   └─ Run BOTH V24 and V28. Weight: 67% V24 + 33% V28.
 │       Focus on V24 HCCs (higher weight) but do not ignore V28-only HCCs.
 ├─ Payment year 2025?
 │   └─ Run BOTH. Weight: 33% V24 + 67% V28.
 │       Shift focus to V28 HCCs.
 └─ Payment year 2026+?
     └─ V28 only.
```

### HCCs That Changed Between V24 and V28

| Change Type | Example | Impact |
|---|---|---|
| Removed in V28 | Some lower-severity CCs consolidated | Lost revenue if only V28 applies |
| New in V28 | Substance use disorders, expanded mental health | New revenue opportunity |
| Coefficient changed | Diabetes coefficients recalibrated | May increase or decrease RAF |
| Hierarchy restructured | Some hierarchies split or merged | Different CC may survive hierarchy |

**Rule**: During the transition, a diagnosis that maps to an HCC in V24 but NOT V28 still
has partial value (67% in 2024, 33% in 2025). Do not ignore these diagnoses.

---

## When NOT to Use This Skill

- Submitting RAF scores to CMS (needs certified risk adjustment coder)
- When chart review findings contradict claims-based HCC assignments
- Individual member clinical documentation (needs provider engagement)

## When to Escalate to a Human Expert

- When audit identifies systematic upcoding patterns requiring compliance review
- Before extrapolating risk scores to populations outside the model's training data
- When V24/V28 transition creates >5% revenue impact requiring actuarial review

## 8. Common Mistakes

1. **Wrong:** Coding diagnoses directly from Rx claims without a face-to-face encounter
   **Right:** Use Rx data to identify suspected gaps, then document the condition via a qualifying face-to-face encounter
   **Why:** Rx claims are proxies, not diagnosis sources — CMS requires face-to-face documentation for risk adjustment

2. **Wrong:** Recapturing conditions that have resolved (e.g., coding "history of cancer" as active cancer)
   **Right:** Only code conditions that are currently active and being evaluated, monitored, or treated
   **Why:** "History of" is not an active diagnosis; submitting resolved conditions as active is audit-indefensible and may constitute fraud

3. **Wrong:** Calculating RAF scores without applying hierarchy resolution
   **Right:** Always resolve hierarchies (retain only the highest-severity CC in each group) before summing coefficients
   **Why:** Counting superseded CCs overstates the RAF score and produces incorrect revenue projections

4. **Wrong:** Optimizing coding strategy for V24 only during the 2025 payment year
   **Right:** Run both V24 and V28 models with appropriate blend weights (33% V24 / 67% V28 in 2025)
   **Why:** V28 carries 67% weight in 2025; ignoring it means missing the majority of payment impact

5. **Wrong:** Submitting diagnoses from lab-only or radiology-only encounters
   **Right:** Ensure every submitted diagnosis comes from a face-to-face encounter with a qualifying provider type (MD, DO, NP, PA)
   **Why:** Lab-only encounters do not qualify for risk adjustment under CMS rules — these diagnoses will be deleted on RADV audit

6. **Wrong:** Cloning documentation across multiple visits with identical assessment text
   **Right:** Ensure each encounter note reflects the specific visit with unique clinical details and current status
   **Why:** Cloned notes put all associated HCCs at risk during audit — CMS may delete every HCC from cloned documentation

7. **Wrong:** Submitting unspecified ICD-10 codes when clinical documentation supports higher specificity
   **Right:** Code to the highest specificity level supported by the documentation (e.g., E11.21 instead of E11.9)
   **Why:** Unspecified codes may map to a lower-value HCC or no HCC at all, leaving revenue on the table

---

## 9. Reporting Checklist

Every risk adjustment analysis MUST report:

1. **Model version(s)**: V24, V28, or blended (with weights).
2. **Population**: Medicare Advantage, Medicaid, ACA marketplace.
3. **Payment year**: Determines which model version and coefficients apply.
4. **Hierarchy resolution**: Confirm hierarchies were applied before RAF calculation.
5. **Interaction terms**: List which interactions were evaluated and applied.
6. **Coding gap methodology**: Rx proxy, lab proxy, historical, or chart review.
7. **Audit readiness**: Documentation validation status for submitted HCCs.
8. **Coding intensity adjustment**: Applied by CMS; note the current percentage.

---

## 10. Glossary

| Term | Definition |
|---|---|
| CC | Condition Category — intermediate grouping of ICD-10 codes |
| HCC | Hierarchical Condition Category — CC that survives hierarchy resolution |
| RAF | Risk Adjustment Factor — numeric score representing expected cost |
| RADV | Risk Adjustment Data Validation — CMS audit program |
| MA | Medicare Advantage — Part C managed care plans |
| FFS | Fee-for-Service — traditional Medicare payment model |
| ESRD | End-Stage Renal Disease — separate CMS-HCC model |
| AWV | Annual Wellness Visit — key encounter for HCC recapture |
| NPI | National Provider Identifier |
| PY | Payment Year — the calendar year for which RAF scores are calculated |
