---
name: supplement-drug-interactions
description: >
  First supplement-drug interaction safety tool for AI agents. Evidence-based
  supplement safety intelligence with 805 FDA FAERS adverse event signals and
  CYP450 pathway analysis.
---

# Supplement-Drug Interaction Safety

The first supplement-drug interaction safety tool purpose-built for AI agents. Provides evidence-based supplement safety intelligence covering 805 FDA FAERS adverse event signals and comprehensive CYP450 enzyme pathway analysis for herbal products, vitamins, and dietary supplements that are frequently omitted from standard drug interaction databases.

## Quick Install

```bash
npx skills add Open-Medica/open-medical-skills --skill supplement-drug-interactions
```

## What It Does

- **FDA FAERS signal integration**: Cross-references 805 curated adverse event signals from the FDA Adverse Event Reporting System specifically cataloging supplement-related safety reports
- **CYP450 pathway mapping**: Identifies which cytochrome P450 enzymes (CYP3A4, CYP2D6, CYP1A2, CYP2C9, CYP2C19) each supplement induces or inhibits, and flags medications processed through the same pathways
- **Pharmacokinetic interaction grading**: Classifies supplement-drug interactions by mechanism (absorption interference, enzyme induction/inhibition, protein binding displacement, pharmacodynamic synergy/antagonism)
- **Common supplement coverage**: Includes St. John's Wort, ginkgo biloba, garlic extract, turmeric/curcumin, fish oil, ginseng, echinacea, valerian, kava, milk thistle, and hundreds more
- **Patient-facing summaries**: Generates plain-language explanations suitable for patient counseling alongside technical pharmacologic detail for clinicians

## Clinical Use Cases

- **Integrative medicine consultations**: A patient taking warfarin wants to add turmeric and fish oil supplements. The skill identifies curcumin's antiplatelet effects and omega-3 fatty acid interference with coagulation, quantifying the combined bleeding risk
- **Pre-surgical supplement hold list**: Before elective surgery, the skill generates a list of supplements the patient should discontinue and the recommended washout period for each (e.g., ginkgo 36 hours, garlic 7 days, fish oil 7 days)
- **Oncology regimen screening**: Cancer patients frequently use herbal supplements alongside chemotherapy. The skill flags St. John's Wort as a potent CYP3A4 inducer that can reduce irinotecan and imatinib plasma levels by 40-50%
- **Mental health medication safety**: Identifies serotonergic supplements (5-HTP, SAMe, tryptophan) that carry serotonin syndrome risk when combined with SSRIs, SNRIs, or MAOIs

## Safety & Evidence

- **Safety Classification:** Safe — The skill provides informational alerts and does not modify prescriptions or treatment plans. Supplement interaction data is sourced from regulatory databases and peer-reviewed pharmacology literature.
- **Evidence Level:** High — Built on FDA FAERS signal data, Natural Medicines Comprehensive Database interaction ratings, and published CYP450 metabolism studies. Interaction grading is conservative, erring toward flagging potential issues.

## Example Usage

**Single supplement check:**
```
Check interactions between St. John's Wort and oral contraceptives
```
> **Result:** Significant interaction. St. John's Wort is a potent CYP3A4 inducer that can reduce ethinyl estradiol and progestin plasma concentrations by 40-60%, leading to contraceptive failure. Documented in multiple case reports of unplanned pregnancies. Recommendation: use alternative contraception or discontinue St. John's Wort.

**Multi-supplement screening:**
```
Patient takes: metoprolol 50mg BID, lisinopril 10mg daily
Supplements: CoQ10 200mg, magnesium glycinate 400mg, hawthorn berry extract
Screen for interactions.
```
> **Result:** (1) CoQ10 — no significant interaction with either medication; may provide additive cardioprotective benefit. (2) Magnesium — monitor: high-dose magnesium may enhance the hypotensive effect of lisinopril; advise spacing doses. (3) Hawthorn berry — Caution: additive bradycardia and hypotension risk with metoprolol; monitor heart rate and blood pressure closely.

## Technical Details

- **Category:** Pharmacy
- **Author:** OMS Contributors
- **License:** MIT
- **Version:** 1.0.0
- **Specialty:** Pharmacy, Integrative Medicine

## References

- FDA Adverse Event Reporting System (FAERS) Public Dashboard — supplement-related reports
- Natural Medicines Comprehensive Database (Therapeutic Research Center), interaction monographs
- Tsai HH, et al. "A review of potential harmful interactions between anticoagulant/antiplatelet agents and Chinese herbal medicines." *PLoS One*. 2013;8(5):e64255.
- Gurley BJ, et al. "Clinical assessment of CYP2D6-mediated herb-drug interactions in humans." *Clin Pharmacol Ther*. 2008;83(1):61-69.
- Posadzki P, Watson L, Ernst E. "Herb-drug interactions: an overview of systematic reviews." *Br J Clin Pharmacol*. 2013;75(3):603-618.

---

*This skill is part of [Open Medical Skills](https://github.com/Open-Medica/open-medical-skills), a curated marketplace of medical AI skills maintained by physicians for physicians and the healthcare industry.*
