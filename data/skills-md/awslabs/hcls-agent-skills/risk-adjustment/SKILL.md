---
name: risk-adjustment
description: >
  Pipeline skill for CMS-HCC risk adjustment calculation and coding gap identification. Use
  when the user asks to apply the ICD-10-to-HCC crosswalk, calculate RAF scores, resolve
  disease hierarchies programmatically, identify coding gaps from Rx or lab proxies, project
  member-level risk scores, build a risk adjustment data pipeline, compute HCC coefficients,
  run hierarchy resolution code, or generate member risk score reports. Triggers include
  "calculate RAF score", "ICD-10 to HCC crosswalk", "hierarchy resolution code", "coding
  gap detection", "Rx proxy gap", "lab proxy gap", "risk score projection", "HCC pipeline",
  "member risk report", "risk adjustment Python", "risk adjustment SQL", "RAF calculation
  code", "CMS-HCC pipeline".
usage: Invoke to generate executable Python and SQL code for ICD-10-to-HCC mapping, hierarchy resolution, RAF score calculation, and coding gap identification.
version: 1.0.0
validated_against:
  date: 2025-01-15
  packages: {hcc-tools: "1.0", pandas: "2.2"}
tags: [skill, category:pipeline, risk-adjustment, hcc, hcls]
---

# Risk Adjustment — Pipeline Skill

## Overview

Provide deterministic, copy-paste-ready Python and SQL code for CMS-HCC risk adjustment:
ICD-10-to-HCC crosswalk, hierarchy resolution, RAF score calculation, and coding gap
identification from Rx/lab proxies.

## Usage

- Apply ICD-10-to-HCC crosswalk and resolve disease hierarchies programmatically
- Calculate member-level RAF scores and identify coding gaps from Rx/lab proxies

## Core Concepts

---


## Response Format

- Lead with the command or code the user needs — explain after
- Structure as: confirm inputs → working code → key parameters explained → gotchas
- One complete working example per task; do not show every alternative
- Keep code comments minimal and functional (what, not why-it-exists)
- Target: 50-100 lines of code with brief surrounding explanation

## 1. ICD-10-to-HCC Crosswalk

### Python

```python
import pandas as pd


def load_crosswalk(filepath: str) -> pd.DataFrame:
    """Load CMS ICD-10-to-CC crosswalk. Expected columns: [icd10, cc]."""
    xwalk = pd.read_csv(filepath, dtype=str)
    xwalk.columns = [c.strip().lower() for c in xwalk.columns]
    xwalk["icd10"] = xwalk["icd10"].str.replace(".", "", regex=False).str.upper()
    xwalk["cc"] = xwalk["cc"].astype(int)
    return xwalk


def map_diagnoses_to_ccs(dx_df: pd.DataFrame, xwalk: pd.DataFrame) -> pd.DataFrame:
    """Map member diagnoses to Condition Categories.

    Args:
        dx_df: [member_id, icd10, service_date, provider_type].
        xwalk: [icd10, cc].
    Returns:
        Deduplicated [member_id, icd10, cc].
    """
    dx = dx_df.copy()
    dx["icd10"] = dx["icd10"].str.replace(".", "", regex=False).str.upper()
    qualifying = {"MD", "DO", "NP", "PA", "CNS"}
    dx = dx[dx["provider_type"].str.upper().isin(qualifying)]
    mapped = dx.merge(xwalk, on="icd10", how="inner")
    return mapped.drop_duplicates(subset=["member_id", "cc"])
```

### SQL

```sql
SELECT DISTINCT d.member_id, d.icd10, x.cc
FROM diagnoses d
JOIN icd10_cc_crosswalk x ON REPLACE(d.icd10, '.', '') = x.icd10
WHERE d.provider_type IN ('MD','DO','NP','PA','CNS')
  AND d.service_date BETWEEN '2025-01-01' AND '2025-12-31';
```

---

## 2. Hierarchy Resolution

### Python

```python
import pandas as pd
from collections import defaultdict

# V24 hierarchies: {higher_cc: [lower_ccs_it_supersedes]}
V24_HIERARCHIES = {
    17: [18, 19], 18: [19],           # Diabetes
    85: [86, 87], 86: [87],           # Heart failure
    111: [112],                        # COPD > asthma
    136: [137, 138], 137: [138],      # Renal
    8: [9,10,11,12], 9: [10,11,12], 10: [11,12], 11: [12],  # Cancer
    107: [108],                        # Vascular
    27: [28, 29], 28: [29],           # Liver
    51: [52],                          # Dementia
    82: [83, 84], 83: [84],           # Hemiplegia
}


def resolve_hierarchies(member_ccs: pd.DataFrame,
                        hierarchies: dict = None) -> pd.DataFrame:
    """Remove lower CCs when higher CC in same hierarchy is present.

    Args:
        member_ccs: [member_id, cc].
        hierarchies: {higher_cc: [lower_ccs]}. Defaults to V24.
    Returns:
        [member_id, hcc] with only surviving CCs.
    """
    if hierarchies is None:
        hierarchies = V24_HIERARCHIES

    superseded_by = defaultdict(set)
    for higher, lowers in hierarchies.items():
        for lower in lowers:
            superseded_by[lower].add(higher)

    results = []
    for mid, grp in member_ccs.groupby("member_id"):
        cc_set = set(grp["cc"])
        for cc in cc_set:
            if not superseded_by.get(cc, set()).intersection(cc_set):
                results.append({"member_id": mid, "hcc": cc})
    return pd.DataFrame(results)
```

### SQL

```sql
WITH hierarchy_rules AS (
    SELECT 17 AS hi, 18 AS lo UNION ALL SELECT 17,19 UNION ALL SELECT 18,19 UNION ALL
    SELECT 85,86 UNION ALL SELECT 85,87 UNION ALL SELECT 86,87 UNION ALL
    SELECT 111,112 UNION ALL SELECT 136,137 UNION ALL SELECT 136,138 UNION ALL SELECT 137,138
),
superseded AS (
    SELECT mc.member_id, mc.cc
    FROM member_ccs mc
    JOIN hierarchy_rules h ON mc.cc = h.lo
    JOIN member_ccs mc2 ON mc.member_id = mc2.member_id AND mc2.cc = h.hi
)
SELECT mc.member_id, mc.cc AS hcc
FROM member_ccs mc
LEFT JOIN superseded s ON mc.member_id = s.member_id AND mc.cc = s.cc
WHERE s.cc IS NULL;
```

---

## 3. RAF Score Calculation

```python
import pandas as pd

# V24 Community Non-Dual Aged (example subset)
DEMO_COEFF = {
    ("M","65-69"): 0.395, ("M","70-74"): 0.487, ("M","75-79"): 0.596,
    ("M","80-84"): 0.728, ("M","85-89"): 0.896, ("M","90-94"): 1.003, ("M","95+"): 1.073,
    ("F","65-69"): 0.339, ("F","70-74"): 0.421, ("F","75-79"): 0.532,
    ("F","80-84"): 0.668, ("F","85-89"): 0.854, ("F","90-94"): 0.979, ("F","95+"): 1.055,
}

HCC_COEFF = {
    8: 2.484, 9: 0.975, 10: 0.690, 17: 0.368, 18: 0.368, 19: 0.118,
    47: 0.545, 51: 0.437, 52: 0.294, 85: 0.441, 86: 0.335, 87: 0.237,
    96: 0.296, 111: 0.335, 112: 0.199, 136: 0.288, 137: 0.237, 138: 0.237,
}

INTERACTIONS = {
    frozenset(["diabetes","chf"]): 0.154,
    frozenset(["chf","copd"]): 0.175,
    frozenset(["chf","renal"]): 0.154,
    frozenset(["diabetes","chf","copd"]): 0.047,
}

HCC_GROUP = {
    17: "diabetes", 18: "diabetes", 85: "chf", 86: "chf",
    111: "copd", 112: "copd", 136: "renal", 137: "renal", 138: "renal",
}


def calculate_raf(demographics: pd.DataFrame, member_hccs: pd.DataFrame) -> pd.DataFrame:
    """Calculate RAF scores. demographics: [member_id, sex, age_group]. member_hccs: [member_id, hcc]."""
    hcc_map = member_hccs.groupby("member_id")["hcc"].apply(set).to_dict()
    rows = []
    for _, r in demographics.iterrows():
        mid, hccs = r["member_id"], hcc_map.get(r["member_id"], set())
        demo = DEMO_COEFF.get((r["sex"], r["age_group"]), 0.0)
        hcc_score = sum(HCC_COEFF.get(h, 0.0) for h in hccs)
        groups = {HCC_GROUP[h] for h in hccs if h in HCC_GROUP}
        interact = sum(v for k, v in INTERACTIONS.items() if k.issubset(groups))
        rows.append({"member_id": mid, "demo": round(demo, 3), "hcc_score": round(hcc_score, 3),
                      "interaction": round(interact, 3), "total_raf": round(demo + hcc_score + interact, 3),
                      "hcc_count": len(hccs), "hccs": sorted(hccs)})
    return pd.DataFrame(rows).sort_values("total_raf", ascending=False)
```

### SQL

```sql
WITH hcc_scores AS (
    SELECT mh.member_id, SUM(c.coefficient) AS hcc_score, COUNT(*) AS hcc_count
    FROM member_hccs mh
    JOIN hcc_coefficients c ON mh.hcc = c.hcc
    WHERE c.model_version = 'V24' AND c.segment = 'CNA'
    GROUP BY mh.member_id
),
demo_scores AS (
    SELECT md.member_id, dc.coefficient AS demo_score
    FROM member_demographics md
    JOIN demographic_coefficients dc ON md.sex = dc.sex AND md.age_group = dc.age_group
    WHERE dc.model_version = 'V24' AND dc.segment = 'CNA'
)
SELECT d.member_id, d.demo_score, COALESCE(h.hcc_score, 0) AS hcc_score,
       ROUND(d.demo_score + COALESCE(h.hcc_score, 0), 3) AS total_raf
FROM demo_scores d LEFT JOIN hcc_scores h ON d.member_id = h.member_id
ORDER BY total_raf DESC;
```

---

## 4. Coding Gap Identification

### 4a. Rx Proxy Gaps

```python
import pandas as pd

RX_MAP = {
    "metformin":      {"condition": "diabetes",       "icd_pfx": "E11", "hccs": [17,18,19]},
    "glipizide":      {"condition": "diabetes",       "icd_pfx": "E11", "hccs": [17,18,19]},
    "insulin":        {"condition": "diabetes",       "icd_pfx": "E11", "hccs": [17,18,19]},
    "furosemide":     {"condition": "heart_failure",  "icd_pfx": "I50", "hccs": [85,86,87]},
    "spironolactone": {"condition": "heart_failure",  "icd_pfx": "I50", "hccs": [85,86,87]},
    "albuterol":      {"condition": "copd_asthma",    "icd_pfx": "J44", "hccs": [111,112]},
    "donepezil":      {"condition": "dementia",       "icd_pfx": "F03", "hccs": [51,52]},
    "memantine":      {"condition": "dementia",       "icd_pfx": "F03", "hccs": [51,52]},
}


def identify_rx_gaps(rx_df: pd.DataFrame, dx_df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Members with Rx evidence but no matching diagnosis in payment year."""
    rx_yr = rx_df[rx_df["fill_date"].dt.year == year]
    dx_yr = dx_df[dx_df["service_date"].dt.year == year].copy()
    dx_yr["pfx"] = dx_yr["icd10"].str[:3]

    gaps = []
    for drug, m in RX_MAP.items():
        with_rx = set(rx_yr[rx_yr["drug_name"].str.lower().str.contains(drug, na=False)]["member_id"])
        with_dx = set(dx_yr[dx_yr["pfx"] == m["icd_pfx"]]["member_id"])
        for mid in with_rx - with_dx:
            gaps.append({"member_id": mid, "condition": m["condition"],
                         "evidence": drug, "target_hccs": m["hccs"], "gap_type": "rx_proxy"})
    return pd.DataFrame(gaps).drop_duplicates(subset=["member_id", "condition"])
```

### 4b. Lab Proxy Gaps

```python
import pandas as pd

LAB_MAP = {
    "HbA1c": {"thresh": 6.5, "op": ">=", "condition": "diabetes",       "icd_pfx": "E11", "hccs": [17,18,19]},
    "eGFR":  {"thresh": 60,  "op": "<",  "condition": "ckd",            "icd_pfx": "N18", "hccs": [136,137,138]},
    "BNP":   {"thresh": 100, "op": ">=", "condition": "heart_failure",  "icd_pfx": "I50", "hccs": [85,86,87]},
    "BMI":   {"thresh": 40,  "op": ">=", "condition": "morbid_obesity", "icd_pfx": "E66", "hccs": [22]},
}


def identify_lab_gaps(labs: pd.DataFrame, dx_df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Members with abnormal labs but no matching diagnosis."""
    labs_yr = labs[labs["result_date"].dt.year == year]
    dx_yr = dx_df[dx_df["service_date"].dt.year == year].copy()
    dx_yr["pfx"] = dx_yr["icd10"].str[:3]

    gaps = []
    for test, m in LAB_MAP.items():
        t = labs_yr[labs_yr["test_name"].str.upper() == test.upper()].copy()
        t["val"] = pd.to_numeric(t["result_value"], errors="coerce")
        abn = t[t["val"] >= m["thresh"]] if m["op"] == ">=" else t[t["val"] < m["thresh"]]
        with_dx = set(dx_yr[dx_yr["pfx"] == m["icd_pfx"]]["member_id"])
        for mid in set(abn["member_id"]) - with_dx:
            gaps.append({"member_id": mid, "condition": m["condition"],
                         "evidence": test, "target_hccs": m["hccs"], "gap_type": "lab_proxy"})
    return pd.DataFrame(gaps).drop_duplicates(subset=["member_id", "condition"])
```

### SQL — Rx Gap Detection

```sql
WITH rx_diabetes AS (
    SELECT DISTINCT member_id FROM rx_claims
    WHERE LOWER(drug_name) IN ('metformin','glipizide','insulin glargine','insulin lispro')
      AND fill_date BETWEEN '2025-01-01' AND '2025-12-31'
),
dx_diabetes AS (
    SELECT DISTINCT member_id FROM diagnoses
    WHERE icd10 LIKE 'E11%' AND service_date BETWEEN '2025-01-01' AND '2025-12-31'
      AND provider_type IN ('MD','DO','NP','PA')
)
SELECT r.member_id, 'diabetes' AS condition, 'rx_proxy' AS gap_type
FROM rx_diabetes r LEFT JOIN dx_diabetes d ON r.member_id = d.member_id
WHERE d.member_id IS NULL;
```

---

## 5. End-to-End Pipeline

```python
def project_risk_scores(dx_df, xwalk_df, demo_df, hierarchies=None):
    """Full pipeline: crosswalk → hierarchy → RAF → summary."""
    ccs = map_diagnoses_to_ccs(dx_df, xwalk_df)
    hccs = resolve_hierarchies(ccs, hierarchies)
    scores = calculate_raf(demo_df, hccs)
    print(f"Members: {len(scores)}, Mean RAF: {scores['total_raf'].mean():.3f}, "
          f"Median: {scores['total_raf'].median():.3f}")
    return scores
```

---

## 6. Parameter Reference

| Function | Key Parameter | Default | Guidance |
|---|---|---|---|
| `load_crosswalk` | CMS file | Annual release | Verify payment year match |
| `resolve_hierarchies` | `hierarchies` | V24 | Use V28 for PY 2026+; both during transition |
| `calculate_raf` | Coefficient tables | V24 CNA | Match to population segment |
| `identify_rx_gaps` | `year` | Current | Gaps are year-specific |
| `identify_lab_gaps` | Lab thresholds | Clinical standards | Adjust per guidelines |

---

## Common Mistakes

- **Wrong:** Applying the ICD-10-to-HCC crosswalk without stripping periods from ICD-10 codes
  **Right:** Normalize codes with `str.replace(".", "").upper()` before joining to the crosswalk
  **Why:** CMS crosswalk files use unformatted codes (e.g., `E119` not `E11.9`); mismatches silently drop valid mappings

- **Wrong:** Summing all CC coefficients without running hierarchy resolution first
  **Right:** Always call `resolve_hierarchies()` to retain only the highest-severity CC per hierarchy group before scoring
  **Why:** Counting superseded CCs inflates RAF scores and produces incorrect revenue projections

- **Wrong:** Using V24 hierarchies and coefficients for payment year 2026+
  **Right:** Use V28 tables for PY 2026+; use blended weights (33% V24 / 67% V28) for PY 2025
  **Why:** CMS transitions to V28 full-weight in 2026; stale coefficients produce materially wrong scores

- **Wrong:** Including diagnoses from any provider type in the crosswalk mapping
  **Right:** Filter to qualifying provider types (MD, DO, NP, PA, CNS) before mapping
  **Why:** CMS only accepts diagnoses from face-to-face encounters with eligible providers for risk adjustment

- **Wrong:** Treating Rx proxy gaps as confirmed diagnoses and coding them directly
  **Right:** Use Rx/lab proxies to identify suspected gaps that require provider documentation on a qualifying encounter
  **Why:** Proxies are screening signals, not diagnosis sources — submitting without documentation fails RADV audit

- **Wrong:** Running `identify_lab_gaps` without converting `result_value` to numeric first
  **Right:** Cast with `pd.to_numeric(errors="coerce")` and handle NaN before threshold comparison
  **Why:** Lab values often contain text qualifiers (">100", "see note"); string comparison produces wrong results
