---
name: cnv-acmg-classifier
description: >-
  Classify structural variants / copy-number variants (deletions and
  duplications) using the ClinGen / ACMG 2019 (Riggs et al. 2020) point
  framework and return a five-tier classification with a per-section evidence
  trail. Germline CNV interpretation, not SNV/indel.
license: MIT
metadata:
  version: "0.1.0"
  author: ClawBio Contributors
  domain: clinical-genomics
  tags:
    - cnv
    - structural-variant
    - acmg
    - clingen
    - dosage-sensitivity
  inputs:
    - name: input_file
      type: file
      format:
        - vcf
        - csv
        - tsv
      description: CNV/SV calls (VCF with SVTYPE/END, or a CSV/TSV with cnv_id,chrom,start,end,type)
      required: true
    - name: dosage_map
      type: file
      format:
        - csv
      description: Optional dosage-sensitivity map (chrom,start,end,name,hi_score,ts_score,benign)
      required: false
    - name: gene_model
      type: file
      format:
        - csv
      description: Optional protein-coding gene model (chrom,start,end,gene) for gene counting
      required: false
  outputs:
    - name: report
      type: file
      format:
        - md
      description: Per-CNV classification report with evidence codes and tier counts
    - name: result
      type: file
      format:
        - json
      description: Machine-readable classifications with section-by-section evidence
  dependencies:
    python: ">=3.10"
    packages:
  demo_data:
    - path: demo_cnv_calls.csv
      description: Seven synthetic CNVs spanning all five ACMG tiers
    - path: data/curated_dosage_map.csv
      description: Curated demonstration dosage-sensitivity map
    - path: data/curated_gene_model.csv
      description: Curated demonstration gene model (incl. a 40-gene cluster)
  endpoints:
    cli: python skills/cnv-acmg-classifier/cnv_acmg_classifier.py --input {input_file} --output {output_dir}
  openclaw:
    requires:
      bins:
        - python3
    always: false
    emoji: "🦖"
    homepage: https://github.com/ClawBio/ClawBio
    os:
      - darwin
      - linux
    install:
    trigger_keywords:
      - CNV classification
      - copy number variant ACMG
      - structural variant interpretation
      - ClinGen dosage sensitivity
      - deletion duplication pathogenic
---

# 🦖 CNV ACMG Classifier

You are **CNV ACMG Classifier**, a specialised ClawBio agent for clinical genomics. Your role is to classify copy-number variants (deletions and duplications) using the ClinGen/ACMG 2019 point framework and return a transparent, five-tier verdict.

## Trigger

**Fire this skill when the user says any of:**
- "classify this CNV" / "classify this copy-number variant"
- "is this deletion / duplication pathogenic?"
- "ACMG classification for a structural variant / CNV"
- "ClinGen dosage sensitivity scoring"
- "score my CNV / SV calls" (deletions or duplications)
- "interpret the CNVs / SVs from my sarek / CNV-caller output"

**Do NOT fire when:**
- The user wants SNV/indel ACMG classification → route to `clinical-variant-reporter`.
- The user wants to *call* CNVs/SVs from reads → route to `nfcore-sarek-wrapper`.
- The user wants generic VCF annotation of small variants → route to `variant-annotation` / `vcf-annotator`.

**Design notes:** The disambiguator is "copy-number / structural" (whole-gene dosage) versus single-nucleotide ACMG. If the variant is a DEL/DUP spanning genes, it belongs here.

## Why This Exists

- **Without it**: Analysts hand-score CNVs against the 19-category ClinGen rubric in a spreadsheet — slow, error-prone, inconsistent between reviewers.
- **With it**: Deterministic, reproducible point scoring with a full evidence trail in seconds.
- **Why ClawBio**: Points and thresholds trace to the published ClinGen/ACMG standard, not to a model's guess. The agent never invents dosage sensitivity.

## Core Capabilities

1. **Section 1–3 auto-scoring**: genomic content, dosage-sensitive overlap, and gene-count tiers computed from coordinates + dosage map + gene model.
2. **Section 4–5 curator inputs**: case/literature evidence and inheritance are taken from the input (never fabricated).
3. **Five-tier verdict**: Pathogenic / Likely pathogenic / VUS / Likely benign / Benign with the official thresholds.

## Scope

**One skill, one task.** This skill classifies germline CNV/SV dosage effects and nothing else. It does not call variants, annotate SNVs, or predict phenotypes.

## Input Formats

| Format | Extension | Required Fields | Example |
|--------|-----------|-----------------|---------|
| Table | `.csv` / `.tsv` | cnv_id, chrom, start, end, type (+ optional inheritance, case_evidence_points) | `demo_cnv_calls.csv` |
| VCF | `.vcf` / `.vcf.gz` | CHROM, POS, INFO SVTYPE + END | sarek/Manta/CNVnator output |

Optional reference files: `--dosage-map` columns `chrom,start,end,name,hi_score,ts_score,benign,element_type` (`element_type` is `gene` or `region`) plus, for gene entries, `strand` and `cds_start,cds_end` (used to derive the 2C/2D breakpoint geometry; if omitted the whole gene is treated as coding); `--gene-model` columns `chrom,start,end,gene`. Partial-overlap sub-calls are computed from coordinates — there is no free-text loss-of-function flag.

## Workflow

1. **Validate**: Check input columns (or VCF SVTYPE/END); normalise type to loss/gain.
2. **Process**: For each CNV apply Section 1 (content), Section 2 (dosage/benign overlap), Section 3 (gene count), Section 4 (case evidence), Section 5 (inheritance).
3. **Generate**: Sum points, round to 2 dp, map to the five-tier classification.
4. **Report**: Write `report.md`, `result.json`, `tables/cnv_classifications.csv`, and a reproducibility bundle.

**Freedom level:** Scoring is prescriptive — points and thresholds are fixed by the standard. The agent may compose the narrative summary but must never alter a score or tier.

## CLI Reference

```bash
# Standard usage (bring your own dosage map + gene model for real work)
python skills/cnv-acmg-classifier/cnv_acmg_classifier.py \
  --input cnvs.vcf --dosage-map clingen_dosage.csv --gene-model gencode_genes.csv \
  --output cnv_report

# Demo mode (synthetic data, no user files needed)
python skills/cnv-acmg-classifier/cnv_acmg_classifier.py --demo --output /tmp/cnv_demo

# Via ClawBio runner
python clawbio.py run cnv-acmg --demo
```

## Demo

```bash
python clawbio.py run cnv-acmg --demo
```

Expected output: a report classifying 7 synthetic CNVs covering all five ACMG tiers (2 Pathogenic, 2 Likely pathogenic, 1 VUS, 1 Likely benign, 1 Benign).

## Algorithm / Methodology

ClinGen/ACMG copy-number point framework (Riggs et al. 2020):

The five sections are **additive** — every applicable section contributes points and the total is their sum (there is no early stop on 2A or 2F). Consequently a complete 2A deletion inherited from an unaffected parent scores 1.00 + (−0.30) = 0.70 = VUS, and a de novo 2A gain scores 1.00 + 0.45 = 1.45 = Pathogenic — matching the ClinGen worked examples.

1. **Section 1 — content**: 1A (contains protein-coding/functional element) = 0.00; 1B (no functional content) = −0.60 (nothing further to score).
2. **Section 2 — dosage**: 2A complete overlap of an established (score 3) HI region/gene (loss) or TS region/gene (gain) = +1.00; 2F complete containment in an established benign region = −1.00. Partial overlaps of an established HI **gene** are derived from **breakpoint geometry** (gene strand + coding boundaries), not a free-text flag: 2C-1 (+0.90) 5′ end deleted with coding sequence involved; 2C-2 (0.00) 5′ end, 5′UTR only; 2D-4 (+0.90) 3′ end deleted with coding exon(s) involved; 2D-1 (0.00) 3′ end, 3′UTR only; 2E intragenic (+0.90 if coding involved, else 0.00). Region-level partial overlaps and all gain partials = 2B (0.00, uncertain).
3. **Section 3 — gene number** (per the ClinGen note, omitted **only when a _complete_ established call — 2A or 2F — is made**; a 0-scoring partial such as 2B/2C-2/2D-1 still earns it, so a deletion that merely clips an established region but spans many genes is scored on size): loss → 0–24 (0.00) / 25–34 (+0.45) / ≥35 (+0.90); gain → 0–34 (0.00) / 35–49 (+0.45) / ≥50 (+0.90).
4. **Section 4 — case/literature**: analyst-supplied aggregate points, clamped to ±0.90, always summed.
5. **Section 5 — inheritance**: de novo (both parents tested) = +0.45; inherited from an unaffected parent = −0.30; always summed.

**Key thresholds** (source: ClinGen/ACMG 2019, Riggs 2020) — symmetric about zero:
- Pathogenic ≥ +0.99; Likely pathogenic +0.90 to +0.98; VUS −0.89 to +0.89; Likely benign −0.90 to −0.98; Benign ≤ −0.99.
- "Established" dosage sensitivity = ClinGen score 3 (sufficient evidence).

## Example Queries

- "Classify the deletions in this VCF with ACMG."
- "Is a duplication spanning the 22q11.2 region pathogenic?"
- "Score these CNV calls against ClinGen dosage sensitivity."

## Example Output

```markdown
| CNV | Region | Type | Genes | Score | Classification | Evidence |
|---|---|---|---:|---:|---|---|
| CNV_P_TP53del | chr17:7,660,000-7,695,000 | loss | 1 | 1.00 | Pathogenic | 1A, 2A |
| CNV_LP_TP53partial | chr17:7,680,000-7,700,000 | loss | 1 | 0.90 | Likely pathogenic | 1A, 2C-1, 3A |
| CNV_B_benign | chr1:152,030,000-152,070,000 | loss | 1 | -1.00 | Benign | 1A, 2F |
| CNV_VUS_inh | chr2:50,120,000-50,180,000 | loss | 1 | -0.30 | Variant of uncertain significance | 1A, 3A, 5B |
| CNV_LB_caseev | chr2:50,120,000-50,180,000 | loss | 1 | -0.95 | Likely benign | 1A, 3A, 4, 5B |
| CNV_P_dup22q | chr22:18,800,000-21,600,000 | gain | 3 | 1.45 | Pathogenic | 1A, 2A, 5A |
| CNV_LP_genedense | chr19:51,990,000-52,410,000 | loss | 40 | 0.90 | Likely pathogenic | 1A, 3C |
```

## Output Structure

```
output_directory/
├── report.md                       # Primary markdown report
├── result.json                     # Machine-readable classifications + evidence
├── tables/
│   └── cnv_classifications.csv      # One row per CNV with evidence codes
└── reproducibility/
    ├── commands.sh                  # Exact command to reproduce
    ├── environment.yml              # Conda env snapshot (conda-forge, nodefaults)
    └── checksums.sha256             # SHA-256 of every output artifact
```

## Dependencies

**Required**: Python ≥ 3.10 standard library only (no third-party packages).

**Optional**: a real ClinGen dosage map and a Gencode/RefSeq gene model for production scoring (the bundled curated files are for demonstration).

## Gotchas

- **The model will want to treat the bundled dosage/gene files as authoritative for real cases. Do not.** They are a small curated demonstration subset. For clinical work, pass `--dosage-map` (full ClinGen Dosage Sensitivity Map) and `--gene-model` (Gencode/RefSeq). Why: a missing dosage gene silently downgrades a true Pathogenic CNV.
- **The model will want to auto-mine Section 4/5 evidence. Do not.** Case-level and inheritance evidence cannot be derived from coordinates; they must come from the input columns. The skill leaves them at 0 / unknown when absent and says so.
- **2C-1 (+0.90) is derived from breakpoint geometry, not a flag.** A partial deletion earns +0.90 only when geometry shows the 5′ end of an established HI gene is removed with coding sequence involved (or 3′ coding exons, or an intragenic coding deletion). A 5′UTR-only clip is 2C-2 (0.00) and a region-level partial is 2B (0.00). This avoids the over-call of crediting any coordinate overlap.
- **Scoring is additive — there is no terminal section.** All applicable sections sum (Riggs 2020). A complete 2A deletion inherited from an unaffected parent is 1.00 + (−0.30) = 0.70 = VUS; a de novo 2A gain is 1.45 = Pathogenic. The model must not "lock in" a Pathogenic call at 2A and drop Sections 4/5.
- **Section 3 gene-count is omitted only on a _complete_ established call (2A / 2F).** A 0-scoring partial (2B / 2C-2 / 2D-1) still earns gene-count, so a deletion that merely clips an established region but spans ≥35 genes is scored Likely pathogenic rather than forced to VUS.
- **Coordinates must share a genome build with the dosage map and gene model (GRCh38 by default).** Mixing GRCh37 calls with GRCh38 references produces silently wrong overlaps. Lift over first.
- **CN-notation on sex chromosomes is ambiguous.** `CN1` on chrX/chrY is the normal hemizygous male state, so the skill refuses to auto-call it a loss and asks for an explicit DEL/DUP. `CN0`→loss and `CN3+`→gain are unambiguous.
- **Gains are scored conservatively**: a partial overlap of a triplosensitive element is not given positive points without breakpoint evidence, by design.

## Safety

- **Local-first**: No data upload; all processing is on-machine, stdlib-only, no network.
- **Disclaimer**: Every report includes the ClawBio medical disclaimer.
- **Audit trail**: A reproducibility bundle records the exact command.
- **No hallucinated science**: All points and thresholds trace to the ClinGen/ACMG 2019 standard; the agent must not invent dosage sensitivity.

## Agent Boundary

The agent (LLM) dispatches the skill and explains the verdict. The skill (Python) executes the scoring. The agent must NOT override points, thresholds, or tiers, nor assert dosage sensitivity not present in the dosage map.

## Integration with Bio Orchestrator

**Trigger conditions**: the orchestrator routes here when input is a CNV/SV call set (DEL/DUP) and the user asks for ACMG/ClinGen classification.

**Chaining partners**:
- `nfcore-sarek-wrapper`: SV/CNV VCFs from Sarek feed directly into this skill.
- `clinical-variant-reporter`: SNV/indel sibling; pair the two for a complete germline report.
- `profile-report`: structured `result.json` can roll up into a unified profile.

## Maintenance

- **Review cadence**: Re-evaluate when ClinGen releases a new Dosage Sensitivity Map or when ACMG updates the CNV standard.
- **Staleness signals**: ClinGen score reassignments; a new build of the gene model; ACMG threshold revisions.
- **Deprecation**: If superseded by an official ClinGen API wrapper, archive to `skills/_deprecated/` with a pointer.

## Citations

- [Riggs ER et al., Genet Med 2020 (ClinGen/ACMG technical standards for CNV interpretation)](https://pubmed.ncbi.nlm.nih.gov/31690835/); the point framework and thresholds.
- [ClinGen Dosage Sensitivity Map](https://dosage.clinicalgenome.org/); established haploinsufficiency / triplosensitivity calls.

## Self-Audit (SKILL.md Conformance Checklist)

| Check | Status |
|-------|--------|
| YAML `name` present, matches folder | PASS |
| YAML `version` semver | PASS |
| YAML `author` present | PASS |
| YAML `description` one line, specific | PASS |
| YAML `inputs` with format and required flag | PASS |
| YAML `outputs` with format | PASS |
| YAML `trigger_keywords` ≥ 3 | PASS (5) |
| Section `## Trigger` fire / do-not-fire lists | PASS |
| Section `## Scope` one-skill-one-task | PASS |
| Section `## Workflow` numbered steps | PASS |
| Section `## Example Output` rendered sample | PASS |
| Section `## Gotchas` ≥ 3 entries | PASS (6) |
| Section `## Safety` disclaimer referenced | PASS |
| Section `## Agent Boundary` present | PASS |
| Demo data file present | PASS |
| `tests/` directory with ≥ 1 test | PASS (24 tests) |
| SKILL.md under 500 lines | PASS |
| `agentskills validate` (strictyaml spec) | PASS |
