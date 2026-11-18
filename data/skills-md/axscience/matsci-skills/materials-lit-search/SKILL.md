---
name: materials-lit-search
description: Formulating effective literature search queries for materials science questions, and synthesizing/citing search results responsibly. Requires an actual search tool (web search, an API, or similar) to be available to the agent; it cannot substitute for one. Same discipline as the sibling neuro-skills repo's literature-search skill, adapted for materials-specific search conventions.
license: MIT
allowed-tools: Read WebSearch WebFetch
compatibility: Assumes access to a search tool (Web of Science/Scopus API, Google Scholar, or general web search) — this skill provides no search capability itself.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-lit-search
---

# Materials Science Literature Search

## Overview

This skill is knowledge about *how* to search and synthesize materials-science literature well — it
is not itself a search capability. An agent following this skill still needs an actual tool (web
search, a database API call) to execute against; without one, the best this skill can offer is
documentation, not results.

## When to use this skill

Activate when the request involves:
- Literature search, prior work, related studies, has this material/property been reported before
- "What does the literature say about X," "find papers on...," "has this synthesis route been tried"

## Core usage

### Query formulation

```
Weak query:  "good battery cathode material"
Better:      "high capacity cathode material lithium ion battery cycling stability"
Best (using materials-specific terminology and property qualifiers):
             ("cathode material" OR "positive electrode") AND "Li-ion battery"
             AND ("capacity retention" OR "cycling stability") AND ("layered oxide" OR "NMC")
```

Specific composition notation, phase names, and property terminology (not lay paraphrases) retrieve
substantially more relevant results — materials science literature searches benefit especially from
including both a material's common name and its formula/composition notation, since papers vary in
which they emphasize.

### A systematic search checklist, not a single query

- **Terminology**: both common names and formal composition/structure notation (e.g. "NMC811" and
  "LiNi0.8Mn0.1Co0.1O2")
- **Study type**: distinguish computational (DFT-predicted) from experimental (synthesized and
  measured) results explicitly — a materials-science literature search that doesn't separate these
  can conflate a predicted-but-unsynthesized candidate with a validated result
- **Recency**: materials databases and reported "best" properties for a given application (e.g.
  battery capacity records) change quickly; check whether a cited value is still representative of
  the current state of the art

### Synthesis discipline

- State what search was actually performed (terms, database, date range) so a reader can assess
  coverage.
- Distinguish a computational prediction from an experimentally validated result — this distinction
  matters more in materials science than in many fields, since a large fraction of the
  high-throughput screening literature reports predicted-but-unsynthesized candidates.
- Note contradictory findings (e.g. conflicting reported values for the same material's property,
  common when measurement conditions differ) rather than citing only the most favorable value found.

## Validation & Pitfalls

- **A literature search is only as good as the search tool's actual coverage and the agent's actual
  ability to invoke it** — if the executing agent has no real search/API access, its output is
  recalled/memorized training data dressed as a search result, not a current search, and should never
  be presented as if a search was actually performed when it wasn't.
- **Citation fabrication is a known failure mode for language models operating without real
  retrieval** — a plausible-sounding author/year/journal citation is not evidence it's real; any
  citation this skill (or any skill in this repo) produces should be verifiable against an actual
  source.
- **Reported material properties in the literature vary with measurement/synthesis conditions that
  aren't always stated prominently** (sample purity, measurement temperature, processing history) —
  a single literature-reported value should be treated as one data point under specific conditions,
  not a universal material constant, especially for structure-sensitive properties (mechanical
  strength, ionic conductivity) that vary substantially with microstructure.
- **Predicted (computational screening) results significantly outnumber experimentally validated
  ones in current materials discovery literature** — a search that doesn't distinguish these risks
  presenting an unsynthesized computational prediction with the same confidence as a validated
  experimental result.
