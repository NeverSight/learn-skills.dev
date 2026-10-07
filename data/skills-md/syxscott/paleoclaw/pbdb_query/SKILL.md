---
name: pbdb_query
description: "Query the Paleobiology Database (PBDB) for fossil occurrences, taxonomy, and geological data. Use when: finding fossil records, checking taxonomic classifications, geographic distributions, time ranges. NOT for: non-paleontological data, modern species distributions."
homepage: https://github.com/syxscott/PaleoClaw
metadata:
  {
    "paleoclaw":
      {
        "emoji": "🦕",
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
            {
              "id": "apt",
              "kind": "apt",
              "package": "curl",
              "bins": ["curl"],
              "label": "Install curl (apt)",
            },
          ],
      },
  }
---

# PBDB Query Skill

Query the Paleobiology Database for fossil and geological data.

## When to Use

✅ **USE this skill when:**

- "Find fossil occurrences of [taxon]"
- "What is the time range of [genus]?"
- "Geographic distribution of [species]"
- "List species in [family/order]"
- "What fossils are found in [formation]?"
- Taxonomic classification lookup

## When NOT to Use

❌ **DON'T use this skill when:**

- Modern species data → use NCBI/GBIF
- Non-biological geological data → use geology databases
- Molecular/genetic data → use GenBank
- Unpublished or private collections

## API Endpoints

Base URL: `https://paleobiodb.org/data1.2/`

### Taxon Query

```bash
# Basic taxon search
curl -s "https://paleobiodb.org/data1.2/taxa/list.json?name=Tyrannosaurus&rank=genus" | jq '.'

# Get taxon info with classification
curl -s "https://paleobiodb.org/data1.2/taxa/list.json?name=Tyrannosaurus&rank=genus&show=class" | jq '.'
```

### Occurrence Query

```bash
# Fossil occurrences for a taxon
curl -s "https://paleobiodb.org/data1.2/occs/list.json?taxon=Tyrannosaurus&limit=10" | jq '.records[] | {taxon: .taxon_name, lat: .lat, lng: .lng, age: .max_ma, formation: .formation}'

# Occurrences by location
curl -s "https://paleobiodb.org/data1.2/occs/list.json?lat=45.0&lng=-110.0&dist=100&limit=20" | jq '.'
```

### Time Range Query

```bash
# Get first and last appearance
curl -s "https://paleobiodb.org/data1.2/taxa/list.json?name=Tyrannosaurus&rank=genus&show=firstlast" | jq '.'
```

### Classification Lookup

```bash
# Full taxonomic hierarchy
curl -s "https://paleobiodb.org/data1.2/taxa/list.json?name=Tyrannosaurus&rank=genus&show=class" | jq '.records[0] | {name: .name, rank: .rank, parent: .parent_name, class: .class, order: .order, family: .family}'
```

### Formation Query

```bash
# Fossils in specific formation
curl -s "https://paleobiodb.org/data1.2/occs/list.json?formation=Yixian&limit=10" | jq '.records[] | {taxon: .taxon_name, age: .max_ma}'
```

## Response Format

### Taxon Query Result

```
**Taxon**: [Name]
**Rank**: [genus/species/family/etc.]
**Classification**:
  - Kingdom: Animalia
  - Phylum: Chordata
  - Class: [Class]
  - Order: [Order]
  - Family: [Family]
  - Genus: [Genus]

**Time Range**: [Start] - [End] Ma
**First Appearance**: [Period/Epoch]
**Last Appearance**: [Period/Epoch]
```

### Occurrence Result

```
**Fossil Occurrences** for [Taxon]:

1. **Location**: [Country/Region]
   Coordinates: [lat, lng]
   Age: [Ma]
   Formation: [Formation name]
   Taxon: [Species/Genus]
   Reference: [Collection ID]

[Continue for N occurrences...]
```

## Example Queries

### Tyrannosaurus Query

```bash
# Get full taxon info
curl -s "https://paleobiodb.org/data1.2/taxa/list.json?name=Tyrannosaurus&rank=genus&show=class,firstlast" | jq -r '
  .records[0] |
  "**Taxon**: \(.name)\n**Rank**: \(.rank)\n**Time Range**: \(.firstapp) - \(.lastapp) Ma\n**Classification**: \(.class) > \(.order) > \(.family)"
'
```

### Triceratops Occurrences

```bash
curl -s "https://paleobiodb.org/data1.2/occs/list.json?taxon=Triceratops&limit=5" | jq -r '
  .records[] |
  "**Location**: \(.country // "Unknown")\nAge: \(.max_ma) Ma\nFormation: \(.formation // "Unknown")\nTaxon: \(.taxon_name)\n"
'
```

### Yixian Formation Fossils

```bash
curl -s "https://paleobiodb.org/data1.2/occs/list.json?formation=Yixian&limit=10" | jq -r '
  .records[] |
  "- \(.taxon_name) (~\(.max_ma) Ma)"
'
```

## Scientific Integrity Rules

⚠️ **CRITICAL**:

- NEVER fabricate fossil occurrences or taxa
- If PBDB returns no records: "No verified fossil occurrences found in PBDB for [query]."
- Always report age ranges in Ma (Mega-annum)
- Distinguish between identified and tentative classifications
- Note when data is incomplete or uncertain
- PBDB is community-curated; verify critical data

## Time Scale Reference

- Cambrian: 541-485 Ma
- Ordovician: 485-444 Ma
- Silurian: 444-419 Ma
- Devonian: 419-359 Ma
- Carboniferous: 359-299 Ma
- Permian: 299-252 Ma
- Triassic: 252-201 Ma
- Jurassic: 201-145 Ma
- Cretaceous: 145-66 Ma
- Paleogene: 66-23 Ma
- Neogene: 23-2.6 Ma
- Quaternary: 2.6 Ma-present

## Notes

- PBDB is free and open access
- No API key required
- Rate limit: ~100 requests/minute
- Data quality varies by taxon group
- Cite PBDB in publications: https://paleobiodb.org/#/cite
