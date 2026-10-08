---
name: risk-stratification-indices
description: >
  Reasoning skill for clinical risk stratification index selection and interpretation. Use when
  the user asks about LACE scores, Charlson Comorbidity Index, Elixhauser Index, readmission
  risk scoring, comorbidity weighting, SDOH Z-codes, Area Deprivation Index, or population
  health stratification methods.
usage: Use when selecting, calculating, or interpreting clinical risk stratification indices or incorporating SDOH factors.
version: 1.0.0
tags: [skill, category:reasoning, risk-stratification, comorbidity, hcls]
triggers:
  - LACE score
  - Charlson
  - Elixhauser
  - risk stratification
  - SDOH Z-codes
  - ADI
  - readmission risk
  - comorbidity index
  - risk score
  - population health stratification
---

# Risk Stratification Indices Reasoning

## Overview

Guide selection and interpretation of clinical risk stratification indices (LACE, Charlson, Elixhauser) and SDOH factors (Z-codes, ADI) for population health management. Based on validated scoring systems from peer-reviewed literature.

## Usage

- Activate when selecting a risk stratification index for a specific use case (readmission, mortality, utilization)
- Activate when interpreting LACE, Charlson, or Elixhauser scores
- Activate when incorporating SDOH factors (Z-codes, ADI) into population health stratification

## Core Concepts

## Response Format

Apply scoring logic internally. Present the recommended index with justification, scoring interpretation, and risk tier. Do not narrate the full scoring calculation unless asked.

## 1. Choosing a Risk Stratification Method

```
What is the use case?
├── 30-day readmission prediction
│   └── Use LACE index (designed for readmission)
├── Long-term mortality risk adjustment
│   └── Use Charlson Comorbidity Index
├── Hospital resource utilization / cost prediction
│   └── Use Elixhauser Comorbidity Index
├── Medicare risk adjustment (payment)
│   └── Use CMS-HCC (Hierarchical Condition Categories)
└── Population health stratification
    └── Combine clinical risk (Charlson/Elixhauser) + SDOH factors
```

## 2. LACE Index (Readmission Risk)

| Component | Scoring | Range |
|-----------|---------|-------|
| **L** — Length of stay | 1d=1, 2d=2, 3d=3, 4–6d=4, 7–13d=5, ≥14d=7 | 0–7 |
| **A** — Acuity of admission | Emergent=3, Urgent=2, Elective=0 | 0–3 |
| **C** — Comorbidity (Charlson) | 0=0, 1=1, 2=2, 3=3, ≥4=5 | 0–5 |
| **E** — ED visits (prior 6 months) | 0=0, 1=1, 2=2, 3=3, ≥4=4 | 0–4 |
| **Total** | Sum of L+A+C+E | 0–19 |

**Risk tiers:** Low (0–4), Moderate (5–9), High (10+)

## 3. Charlson Comorbidity Index

17 conditions with integer weights:

- **Weight 1:** MI, CHF, PVD, CVD, dementia, COPD, connective tissue disease, peptic ulcer, mild liver disease, uncomplicated diabetes
- **Weight 2:** complicated diabetes, hemiplegia, renal disease, non-metastatic cancer
- **Weight 3:** moderate/severe liver disease
- **Weight 6:** metastatic tumor, AIDS/HIV

Total score = sum of all applicable weights.

## 4. Elixhauser Comorbidity Index

| Attribute | Charlson | Elixhauser |
|-----------|----------|------------|
| Conditions | 17 | 31 |
| Weighting | Fixed integer | Varies by model (van Walraven common) |
| Scope | Mortality prediction | Mortality + resource use |
| Mental health | Limited (dementia only) | Depression, psychoses, substance use |
| Best for | Long-term mortality | Hospital utilization, readmission |

## 5. SDOH Risk Factors

### ICD-10 Z-Codes for SDOH

Key ranges: Z55 (education/literacy), Z56 (employment), Z57 (occupational exposure), Z59 (housing/economic — Z59.0 homelessness, Z59.41 food insecurity), Z60 (social environment), Z62 (upbringing/abuse), Z63 (family circumstances), Z65 (psychosocial/legal).

### Area Deprivation Index (ADI)

| ADI Percentile | Risk Level | Implication |
|---------------|------------|-------------|
| 1–25 | Low deprivation | Standard outreach sufficient |
| 26–50 | Moderate | Enhanced reminder systems |
| 51–75 | High | Care coordination, transportation assistance |
| 76–100 | Very high | Intensive outreach, community health workers |

### Incorporating SDOH into Stratification

Weight members higher when:
1. Any SDOH Z-code documented in claims
2. High ADI score (≥51st percentile)
3. Dual-eligible status (Medicare + Medicaid)
4. Language barrier (non-English preferred)
5. No PCP visit in 12 months (care disengagement)

## Common Mistakes

- **Wrong:** Using Charlson for readmission prediction → **Right:** Use LACE (purpose-built for 30-day readmission)
- **Wrong:** Using Elixhauser for long-term mortality → **Right:** Use Charlson (validated for mortality prediction)
- **Wrong:** Ignoring SDOH factors in population stratification → **Right:** Combine clinical index + SDOH for actionable tiers
- **Wrong:** Applying same outreach to all risk tiers → **Right:** Tailor interventions by barrier type (transportation, literacy, engagement)
- **Wrong:** Using ADI alone without clinical risk → **Right:** ADI indicates access barriers; combine with clinical severity for full picture
- **Wrong:** Treating all Z-codes as equivalent risk signals → **Right:** Weight by relevance to the specific outcome (e.g., Z59.0 homelessness is higher barrier than Z56 employment)

## When to Escalate

- When risk scores drive reimbursement or payment decisions (requires validated, audited implementation)
- When stratification results will determine resource allocation across populations
- When combining indices in novel ways not validated in literature
