---
name: drug-repurposing
description: Reason about drug repurposing strategies in HCLS — choosing between target-based and phenotype-based approaches, evaluating mechanism-of-action overlap, querying drug-gene interaction databases, assessing clinical translatability, and ranking candidates by evidence strength. Use when the user asks to repurpose a drug, find approved drugs for a new indication, evaluate a repurposing candidate, query DGIdb or OpenTargets, assess drug-target interactions, design a repurposing study, rank repurposing evidence, or evaluate translatability of a candidate. Triggers include "drug repurposing", "repurpose", "repositioning", "new indication", "off-label use", "target-based repurposing", "phenotype-based repurposing", "CMap", "L1000", "DGIdb", "OpenTargets", "DrugBank", "ChEMBL", "mechanism of action overlap", "drug-gene interaction", "translatability", "existing safety data", "repurposing evidence hierarchy".
usage: Invoke when evaluating drug repurposing strategies, ranking candidates, or designing repurposing studies.
version: 1.0.0
tags: [skill, category:reasoning, drug-repurposing, drug-discovery, pharmacology, hcls]
---

# Drug Repurposing

## Overview

This skill teaches the agent how to *reason* about drug repurposing — identifying approved or clinical-stage compounds that may treat a new indication. Repurposing succeeds when three conditions align: (1) a credible **mechanistic link** between the drug and the new disease, (2) sufficient **evidence strength** from orthogonal sources, and (3) a realistic **translatability path** given existing safety, PK, formulation, and IP data.

Use this skill to evaluate proposals, rank candidates, spot weak evidence, and guide the user toward a defensible repurposing strategy *before* committing to wet-lab or clinical work.

## Usage

Invoke this skill when the user:

- Has a disease target and wants to find approved drugs that modulate it.
- Has a disease transcriptomic signature and wants to find drugs with opposing profiles.
- Asks how to query DGIdb, OpenTargets, ChEMBL, or DrugBank for repurposing candidates.
- Claims a drug "should work" for a new indication based on a single data source.
- Wants to rank multiple repurposing candidates by evidence strength.
- Asks whether a repurposing candidate is translatable to clinical trials.
- Needs to design a repurposing study or write a repurposing rationale.

The agent should respond by:

1. **Classifying the approach** — target-based or phenotype-based (or hybrid).
2. **Auditing the evidence** — what databases were queried, what evidence types support the candidate.
3. **Applying the evidence hierarchy** — genetic > clinical observation > in vitro > computational.
4. **Assessing translatability** — safety profile, PK, dose feasibility, formulation, patent status.
5. **Identifying gaps** — what evidence is missing and what experiments would fill them.

## Response Format

- Lead with the direct recommendation or classification (≤3 sentences)
- Structure as: recommendation → justification (citing specific criteria/thresholds) → caveats
- Use tables for comparisons; bullet points for criteria lists
- Omit background the user already knows — they asked the question
- Target: 200-400 words unless the user requests exhaustive detail
The decision trees and frameworks in this skill are for internal reasoning only. Apply them to reach your conclusion, but do not reproduce them in your response. Present only the final recommendation with supporting evidence.


## Core Concepts

### 1. Two Fundamental Approaches

Every repurposing effort starts from one of two directions. The choice determines the databases, methods, and evidence types involved.

| Approach | Starting point | Method | Key databases | Strength | Limitation |
|---|---|---|---|---|---|
| **Target-based** | Known disease target (gene/protein) | Find approved drugs that bind or modulate the target | DGIdb, ChEMBL, DrugBank, OpenTargets | Mechanistically interpretable; leverages structural biology | Assumes the target is causal and druggable |
| **Phenotype-based** | Disease molecular signature (transcriptomic, proteomic) | Find drugs whose signature opposes the disease signature | CMap (Connectivity Map), LINCS L1000 | Agnostic to mechanism; can discover unexpected connections | Signatures are noisy; opposing expression ≠ therapeutic effect |

#### Decision tree: which approach?

```
Start
│
├── Do you have a validated disease target (gene/protein)?
│     ├── Yes → Target-based approach.
│     │         Query DGIdb, ChEMBL, DrugBank for drugs hitting this target.
│     │         Cross-reference with OpenTargets for target-disease association strength.
│     └── No  → Continue.
│
├── Do you have a disease molecular signature (e.g., differentially expressed genes)?
│     ├── Yes → Phenotype-based approach.
│     │         Query CMap/L1000 for drugs with negatively correlated signatures.
│     │         Validate top hits against known biology.
│     └── No  → Continue.
│
├── Do you have both a target and a signature?
│     ├── Yes → Hybrid: run both approaches independently, then intersect.
│     │         Candidates appearing in both lists have stronger support.
│     └── No  → Insufficient starting data. Gather target evidence or generate
│               disease signatures before attempting repurposing.
```

### 2. Key Databases and What They Provide

Query multiple databases — no single source is sufficient.

| Database | Content | Use for |
|---|---|---|
| **OpenTargets** | Target-disease association scores (genetics, literature, pathways) | Validating target relevance; scoring association strength |
| **DGIdb** | Drug-gene interactions from 30+ sources | Finding approved drugs that interact with a target gene |
| **ChEMBL** | Bioactivity data (IC50, Ki, EC50) | Quantitative binding/activity evidence; SAR context |
| **DrugBank** | Drug targets, PK, indications, interactions | Drug metadata, safety profiles, formulations |
| **CMap / LINCS L1000** | Expression signatures of ~20,000 compounds | Phenotype-based repurposing; signature reversal |
| **TTD** | Targets, drugs, clinical trial status | Cross-referencing target validation and development stage |
| **STITCH** | Chemical-protein interaction network | Network-level drug-target-disease relationships |

#### Rules for database queries

1. **Always query at least two independent databases.** A hit in DGIdb alone is insufficient; cross-reference with ChEMBL bioactivity data.
2. **Check interaction type.** DGIdb reports inhibitors, activators, binders, and more. An "inhibitor" hit is useless if the disease requires target activation.
3. **Check activity values.** A ChEMBL IC50 of 50 µM is not a drug-like interaction. Require IC50/Ki < 1 µM for serious consideration, < 100 nM for high confidence.
4. **Check the cell line / assay context.** Activity in a biochemical assay does not guarantee cellular activity. Prefer cell-based assay data when available.
5. **For CMap queries, require connectivity score < -90 (strong negative correlation).** Scores between -50 and -90 are suggestive but not actionable alone.

### 3. Evidence Hierarchy for Repurposing Candidates

Not all evidence is equal. Rank candidates by the strongest evidence type supporting them.

| Tier | Evidence type | Description | Weight |
|---|---|---|---|
| **1 (strongest)** | Genetic association via Mendelian randomization (MR) | Genetic variants that proxy drug action associate with disease risk; mimics a natural RCT | Highest — causal inference without confounding |
| **2** | Clinical observation | Case reports, retrospective cohorts, or claims data showing the drug affects the new indication in humans | High — real-world human evidence, but confounded |
| **3** | In vitro / in vivo experimental | Cell-based assays, animal models showing efficacy in the disease context | Moderate — mechanism confirmed but translation uncertain |
| **4 (weakest)** | Computational prediction | Signature matching, network proximity, docking scores, AI predictions | Lowest — hypothesis-generating only; requires experimental validation |

#### Rules for applying the hierarchy

1. **A candidate supported only by Tier 4 evidence is a hypothesis, not a repurposing candidate.** Do not recommend it for clinical development without experimental validation.
2. **Tier 1 evidence (MR) is the gold standard for target validation.** If a genetic instrument for the drug's target associates with the disease, the causal chain is strong. Always check for MR studies in OpenTargets or MR-Base.
3. **Tier 2 evidence must be scrutinized for confounding.** Patients taking drug X who have better outcomes may differ systematically from those not taking it (indication bias, healthy-user bias). Require adjustment for confounders or emulated target trial design.
4. **Tier 3 evidence must include the right disease model.** Showing that a drug kills cancer cells in vitro is not evidence for repurposing in Alzheimer's. The model must recapitulate the target disease biology.
5. **Require at least two tiers of evidence for a credible candidate.** The ideal candidate has Tier 1 (genetic) + Tier 3 (experimental) + Tier 2 (clinical observation). A single tier, regardless of strength, is insufficient.

#### Decision tree: is the evidence sufficient?

```
Start
│
├── Is there Mendelian randomization evidence (Tier 1)?
│     ├── Yes → Strong foundation. Proceed to translatability assessment.
│     │         Still seek Tier 3 confirmation (mechanism in disease model).
│     └── No  → Continue.
│
├── Is there clinical observation evidence (Tier 2)?
│     ├── Yes → Promising, but check for confounding.
│     │         Was the analysis adjusted? Was it an emulated target trial?
│     │         Seek Tier 3 confirmation.
│     └── No  → Continue.
│
├── Is there experimental evidence (Tier 3)?
│     ├── Yes → Mechanistically supported.
│     │         Is the model relevant to the target disease?
│     │         Seek Tier 1 or Tier 2 to strengthen the case.
│     └── No  → Continue.
│
├── Is there only computational evidence (Tier 4)?
│     └── Hypothesis only. Do not recommend for clinical development.
│         Design experiments to generate Tier 3 evidence first.
│
└── No evidence at all?
      └── Not a repurposing candidate. Return to target/disease validation.
```

### 4. Mechanism-of-Action Overlap Evaluation

When a drug is proposed for a new indication, the agent must evaluate whether the drug's mechanism is relevant to the new disease.

**Steps:**

1. **Identify the drug's primary and secondary targets.** Use DrugBank for primary targets and ChEMBL for off-target activity (IC50 < 10 µM).
2. **Map targets to disease pathways.** Use OpenTargets or KEGG/Reactome to check whether any drug target participates in disease-relevant pathways.
3. **Assess directionality.** If the disease requires pathway inhibition, the drug must be an inhibitor (not an activator) of the relevant target. Mismatched directionality is a disqualifying finding.
4. **Check for polypharmacology.** Some repurposing candidates work through secondary targets, not their primary indication target. This is valid but requires explicit evidence for the secondary target's role in the new disease.
5. **Evaluate selectivity.** A drug that hits 50 kinases at 1 µM may modulate the target of interest, but also causes toxicity through off-target effects. Check selectivity panels in ChEMBL.

| MOA evaluation criterion | Pass | Fail |
|---|---|---|
| Drug target participates in disease pathway | Target in top 3 disease pathways (OpenTargets) | No pathway overlap |
| Directionality matches | Drug inhibits overactive target / activates deficient target | Drug action opposes therapeutic need |
| Activity at therapeutic concentrations | IC50/Ki < Cmax at approved dose | IC50 >> Cmax (cannot achieve target engagement) |
| Selectivity acceptable | < 10 off-targets at therapeutic concentration | Broad off-target activity likely to cause toxicity |

### 5. Clinical Translatability Assessment

A mechanistically sound candidate may still fail if it cannot be practically developed. Evaluate these dimensions:

| Dimension | Favorable | Unfavorable |
|---|---|---|
| **Safety profile** | Approved drug with well-characterized AE profile; AEs acceptable for new indication severity | Narrow therapeutic index; serious AEs disproportionate to new indication |
| **Pharmacokinetics** | Drug reaches target tissue at therapeutic concentrations; known human PK | Poor bioavailability in target tissue; no human PK data for relevant route |
| **Dose feasibility** | Therapeutic effect achievable at or below approved dose | Required dose far exceeds approved dose (new toxicity territory) |
| **Formulation** | Existing formulation suitable for new indication (e.g., oral for chronic disease) | Requires new formulation (e.g., intrathecal for CNS disease; IV for outpatient) |
| **Patent / exclusivity** | Generic available or patent allows new-indication development | Active composition-of-matter patent blocks development; no method-of-use patent opportunity |
| **Regulatory path** | 505(b)(2) pathway available; existing safety data reduces trial burden | No regulatory shortcut; full NDA-equivalent development required |

#### Rules for translatability

1. **Check Cmax vs IC50.** If the IC50 for the new target exceeds the Cmax achievable at the approved dose, the drug cannot engage the target without dose escalation — which introduces unknown safety risks.
2. **Assess tissue distribution.** A drug with excellent plasma PK but no CNS penetration cannot be repurposed for a brain disease without reformulation.
3. **Evaluate indication severity mismatch.** Repurposing an immunosuppressant (with infection risk) for mild allergic rhinitis is a translatability failure — the risk-benefit ratio does not support it.
4. **Check patent landscape early.** A composition-of-matter patent held by another company may block development regardless of scientific merit. Method-of-use patents for the new indication may still be available.
5. **Prefer drugs with existing generic formulations.** Lower development cost, faster path to market, and no IP barriers.

### 6. Ranking Multiple Candidates

When multiple drugs emerge from database queries, rank them systematically.

**Scoring framework (assign 0–3 per dimension):**

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Evidence tier | Tier 4 only | Tier 3 only | Two tiers (e.g., 3+4) | Tier 1 or Tier 2 + Tier 3 |
| MOA relevance | No pathway overlap | Pathway overlap, wrong directionality | Correct directionality, weak activity | Correct directionality, strong activity (IC50 < Cmax) |
| Safety profile | Narrow TI, serious AEs | Moderate AEs | Well-tolerated, minor AEs | Excellent safety record for target population |
| PK/dose feasibility | IC50 >> Cmax | IC50 ~ 2–5× Cmax | IC50 ≤ Cmax at approved dose | IC50 << Cmax; wide therapeutic window |
| Regulatory/IP path | Blocked by patent; full NDA | Uncertain IP; standard pathway | 505(b)(2) possible; some existing data | Generic available; extensive safety database |

**Total score interpretation:**
- **12–15:** Strong candidate — prioritize for experimental validation.
- **8–11:** Moderate candidate — worth pursuing if resources allow; address gaps.
- **4–7:** Weak candidate — significant barriers; deprioritize unless unique rationale.
- **0–3:** Not viable — do not pursue.

### 7. Study Design for Repurposing Validation

Once a candidate is selected, the validation path depends on available evidence.

```
Start
│
├── Tier 1 (MR) + Tier 3 (experimental) evidence available?
│     └── Proceed to clinical validation.
│         Design: Phase II proof-of-concept trial (randomized, controlled).
│         Endpoint: disease-specific primary endpoint.
│         Leverage existing safety data to shorten Phase I or skip it (505(b)(2)).
│
├── Tier 3 (experimental) evidence only?
│     └── Strengthen with additional preclinical work.
│         - Confirm efficacy in second disease model.
│         - Demonstrate target engagement at achievable concentrations.
│         - Then proceed to clinical validation.
│
├── Tier 2 (clinical observation) only?
│     └── Formalize with retrospective study.
│         - Emulated target trial design on EHR/claims data.
│         - Adjust for confounders (propensity score, IV if available).
│         - If positive, proceed to prospective trial.
│
└── Tier 4 (computational) only?
      └── Generate experimental evidence first.
          - In vitro assay in disease-relevant cell line.
          - Confirm target engagement.
          - Do not proceed to clinical work on computational evidence alone.
```

### 8. Mendelian Randomization for Target Validation

MR provides the strongest non-trial evidence for repurposing by using genetic variants as instruments for drug action. The logic: if a genetic variant that mimics the drug's effect on the target also associates with the disease, the target is causally implicated.

**MR quality checklist:**

| Criterion | Requirement | Red flag |
|---|---|---|
| Instrument strength | F-statistic > 10 per SNP | F < 10 indicates weak instruments; results biased toward confounded observational estimate |
| Relevance | SNPs must associate with the target gene's expression or protein level (cis-pQTL or cis-eQTL) | Trans-pQTLs may act through intermediaries; less specific |
| Independence | No linkage disequilibrium between instruments | Correlated SNPs inflate apparent strength |
| Exclusion restriction | SNPs affect disease only through the target | Horizontal pleiotropy violates the core assumption |
| Pleiotropy tests | MR-Egger intercept non-significant; weighted median and MR-PRESSO consistent with IVW | Significant MR-Egger intercept = pleiotropy present |
| Replication | Consistent across ancestries and biobanks | Single-ancestry MR may reflect population-specific LD patterns |

**Interpreting MR results for repurposing:**

- MR estimates the *direction* and *approximate magnitude* of the effect of lifelong target modulation. A drug given for months will have a smaller effect than the MR estimate suggests.
- A protective MR association (e.g., genetically proxied target inhibition reduces disease risk) supports repurposing an inhibitor of that target.
- A harmful MR association (e.g., genetically proxied target inhibition increases disease risk) is a strong contraindication — do not repurpose.
- Null MR results do not disprove the target; they may reflect insufficient power, wrong tissue, or non-linear effects.

### 9. Practical Database Query Workflow

A systematic repurposing screen follows this order:

```
Step 1: Define the target or disease signature
│
├── Target-based: Identify gene symbol, UniProt ID, Ensembl ID.
│
└── Phenotype-based: Generate or obtain disease DEG list
    (log2FC > 1, FDR < 0.05 from case-control transcriptomics).

Step 2: Query primary databases
│
├── Target-based:
│     ├── OpenTargets → target-disease association score (require > 0.5).
│     ├── DGIdb → list of drugs with known interactions for the target.
│     └── ChEMBL → bioactivity data (IC50, Ki) for each drug-target pair.
│
└── Phenotype-based:
      └── CMap/LINCS L1000 → query disease signature → rank drugs by
          negative connectivity score (require < -90).

Step 3: Cross-reference and filter
│
├── For each candidate drug:
│     ├── DrugBank → current indications, safety profile, PK parameters.
│     ├── ClinicalTrials.gov → prior trials for this drug + new indication.
│     └── ChEMBL → confirm activity at achievable concentrations (IC50 < Cmax).
│
└── Remove candidates with:
      ├── IC50 > 10× Cmax (cannot achieve target engagement).
      ├── Prior Phase II/III failure for the same indication.
      ├── Unacceptable safety profile for indication severity.
      └── Blocked IP (active composition-of-matter patent, no generic).

Step 4: Rank surviving candidates
│
└── Apply the scoring framework (Section 6) across all dimensions.
    Prioritize candidates scoring ≥ 12/15.

Step 5: Validate top candidates
│
└── Follow the study design decision tree (Section 7).
```

### 10. Network Pharmacology Considerations

Network-based approaches complement direct target queries by considering the drug's effect in the context of protein-protein interaction (PPI) networks and disease modules.

**When network pharmacology adds value:**

- The disease is polygenic with no single dominant target.
- The drug has polypharmacology (multiple targets) and you want to assess aggregate effect.
- You want to identify synergistic repurposing combinations.

**When network pharmacology is insufficient:**

- As the sole evidence for a repurposing candidate (Tier 4 only).
- When the PPI network is incomplete for the tissue of interest.
- When the disease module is poorly defined (few known disease genes).

**Key metrics:**

| Metric | Interpretation | Threshold |
|---|---|---|
| Network proximity (z-score) | How close drug targets are to disease genes in PPI network | z < -2 (significantly closer than random) |
| Overlap coefficient | Fraction of drug targets that are disease genes | > 0 required; > 0.1 is notable |
| Separation score (SAB) | Topological separation between drug and disease modules | SAB < 0 indicates overlap |

**Rules:**

1. Network proximity is hypothesis-generating. A z-score < -2 justifies further investigation, not clinical development.
2. Always use tissue-specific PPI networks when available. Generic interactomes include interactions irrelevant to the disease tissue.
3. Validate network predictions with at least one orthogonal method (database query, MR, or experimental assay) before advancing.
4. Report the network used (BioGRID, STRING, IntAct) and the confidence threshold for edges. Low-confidence edges inflate proximity artificially.

## When NOT to Use This Skill

- Making go/no-go decisions on clinical candidates (needs medicinal chemistry review)
- Evaluating candidates where IP/patent landscape is the primary constraint

## When to Escalate to a Human Expert

- Before investing in clinical trials based on repurposing rationale
- When mechanism-of-action overlap requires structural biology confirmation

## Common Mistakes

- **Wrong:** Treating a negative CMap connectivity score as proof of therapeutic efficacy
  **Right:** Treat CMap results as hypothesis-generating (Tier 4 evidence) and validate with experimental or clinical data
  **Why:** Cell line transcriptomic signatures do not recapitulate in vivo disease biology — opposing expression does not equal therapeutic effect

- **Wrong:** Using a DGIdb "interacts with" hit without checking whether the drug inhibits or activates the target
  **Right:** Always verify interaction directionality (inhibitor vs activator) and confirm it matches the therapeutic need
  **Why:** An inhibitor of a target that needs activation will worsen the disease

- **Wrong:** Treating any ChEMBL binding hit as evidence of therapeutic activity
  **Right:** Always compare IC50/Ki to Cmax at the approved dose — require IC50 < Cmax for serious consideration
  **Why:** A drug may bind a target at concentrations far above what is achievable in vivo, making the interaction clinically irrelevant

- **Wrong:** Basing a repurposing decision on a single database query
  **Right:** Cross-reference at least two independent databases (e.g., DGIdb + ChEMBL, or OpenTargets + DrugBank)
  **Why:** Each database has biases and gaps — DGIdb may miss recent data, ChEMBL lacks clinical context, DrugBank has limited disease associations

- **Wrong:** Proposing a drug with serious side effects for a mild condition based on mechanistic support alone
  **Right:** Evaluate the risk-benefit ratio relative to indication severity before advancing any candidate
  **Why:** The risk-benefit test fails regardless of mechanistic support when side effects are disproportionate to the condition

- **Wrong:** Investing effort in a scientifically sound candidate without checking patent status
  **Right:** Check patent landscape early — look for composition-of-matter blocks and method-of-use opportunities
  **Why:** IP barriers can prevent development regardless of scientific merit, wasting time and resources

- **Wrong:** Assuming the approved dose will achieve target engagement for the new indication
  **Right:** Check PK/PD modeling for the new target — the required exposure may differ from the original indication
  **Why:** The approved dose was optimized for the original target; the new target may require different concentrations

- **Wrong:** Presenting network proximity (drug-target-disease PPI distance) as validation evidence
  **Right:** Treat network-based predictions as Tier 4 (hypothesis-generating) and require experimental confirmation
  **Why:** Computational network proximity is insufficient for clinical development decisions

- **Wrong:** Proposing a drug for a tissue it cannot reach (e.g., non-BBB-penetrant drug for a CNS disease)
  **Right:** Verify tissue-specific distribution — confirm the drug reaches the disease-relevant tissue at therapeutic concentrations
  **Why:** A validated target in the disease tissue is irrelevant if the drug cannot access that tissue

- **Wrong:** Advancing a repurposing candidate without searching ClinicalTrials.gov for prior attempts
  **Right:** Always check for prior failed trials for the same drug-indication pair before investing resources
  **Why:** A Phase II failure for the same indication is a strong negative signal unless the failure was due to trial design rather than efficacy

- **Wrong:** Citing a single underpowered Mendelian randomization study as definitive Tier 1 evidence
  **Right:** Require valid instruments (F-statistic > 10), no horizontal pleiotropy (MR-Egger intercept), and replication across ancestries
  **Why:** A single underpowered MR study without sensitivity analyses does not meet the Tier 1 evidence standard


