---
name: stratigraphy_lookup
description: "Query stratigraphic and geological formation data (formation name, age, period, epoch, location). Use when: identifying rock formations, checking geological ages, correlating strata, finding formation fossils."
homepage: https://github.com/syxscott/PaleoClaw
metadata:
  {
    "paleoclaw":
      {
        "emoji": "🪨",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl (brew)",
            },
          ],
      },
  }
---

# Stratigraphy Lookup Skill

Query geological formation and stratigraphic data.

## When to Use

✅ **USE this skill when:**

- "What age is [formation name]?"
- "Find formations from [period/epoch]"
- "What fossils are in [formation]?"
- "Where is [formation] located?"
- Correlating stratigraphic units
- Checking formation time ranges

## When NOT to Use

❌ **DON'T use this skill when:**

- Modern sediment data → use geological surveys
- Unpublished/local stratigraphic names
- Highly specialized regional stratigraphy
- Non-geological dating

## Data Sources

**Primary**: Paleobiology Database (PBDB)
**Secondary**: Macrostrat, Geolex (via API when available)

## Commands

### Formation Query

```bash
# Query formation by name
curl -s "https://paleobiodb.org/data1.2/occs/list.json?formation=Yixian&limit=5" | jq '
  .records[0] | {
    formation: .formation,
    age: .max_ma,
    period: .period,
    country: .country
  }
'
```

### Fossils in Formation

```bash
# List taxa from a formation
curl -s "https://paleobiodb.org/data1.2/occs/list.json?formation=Hell+Creek&limit=20" | jq '
  [.records[].taxon_name] | unique | .[]
'
```

### Formation by Age

```bash
# Find formations from specific time period
curl -s "https://paleobiodb.org/data1.2/occs/list.json?min_ma=145&max_ma=66&limit=10" | jq '
  [.records[].formation] | unique | .[]
'
```

### Geographic Query

```bash
# Formations in a country
curl -s "https://paleobiodb.org/data1.2/occs/list.json?country=China&limit=10" | jq '
  [.records[].formation] | unique | .[]
'
```

## Response Format

```
**Stratigraphic Information**

**Formation**: [Formation name]
**Age**: [XX] Ma ([Period]/[Epoch])
**Location**: [Country/Region]
**Lithology**: [Rock type, if available]

**Associated Fossils**:
- [Taxon 1]
- [Taxon 2]
- [Taxon N]

**Stratigraphic Context**:
- Underlies: [Overlying formation]
- Overlies: [Underlying formation]
- Correlates with: [Equivalent formations]
```

## Geological Time Scale Reference

```
Eon: Phanerozoic
├─ Era: Cenozoic
│  ├─ Period: Quaternary (2.6 Ma - present)
│  │  ├─ Epoch: Holocene (0.0117 Ma - present)
│  │  └─ Epoch: Pleistocene (2.6 - 0.0117 Ma)
│  ├─ Period: Neogene (23 - 2.6 Ma)
│  └─ Period: Paleogene (66 - 23 Ma)
├─ Era: Mesozoic
│  ├─ Period: Cretaceous (145 - 66 Ma)
│  │  ├─ Epoch: Late Cretaceous (100 - 66 Ma)
│  │  └─ Epoch: Early Cretaceous (145 - 100 Ma)
│  ├─ Period: Jurassic (201 - 145 Ma)
│  │  ├─ Epoch: Late Jurassic (163 - 145 Ma)
│  │  ├─ Epoch: Middle Jurassic (174 - 163 Ma)
│  │  └─ Epoch: Early Jurassic (201 - 174 Ma)
│  └─ Period: Triassic (252 - 201 Ma)
└─ Era: Paleozoic (541 - 252 Ma)
```

## Scientific Integrity Rules

⚠️ **CRITICAL**:

- NEVER fabricate formation names or ages
- If formation not found: "No verified stratigraphic data found for [formation]."
- Report age ranges with uncertainty
- Note regional naming variations
- Distinguish formal vs informal formation names
- Some formations span multiple time periods

## Notes

- Formation names may vary by region
- Radiometric dating updates ages periodically
- Some formations have poor fossil records
- Cross-reference with geological surveys for precise work
