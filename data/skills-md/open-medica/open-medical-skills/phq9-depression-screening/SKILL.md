---
name: phq9-depression-screening
description: >
  Validated Patient Health Questionnaire-9 (PHQ-9) for depression screening
  and severity assessment. Automatic scoring and interpretation with suicide
  risk flagging.
---

# PHQ-9 Depression Screening Tool

## Overview

The PHQ-9 (Patient Health Questionnaire-9) is the gold standard self-report instrument for depression screening and severity monitoring in clinical practice. This skill implements the complete PHQ-9 with automated scoring, DSM-5 criteria cross-referencing, suicide risk flagging on Item 9, and evidence-based treatment recommendations calibrated to severity level.

## Clinical Context

Major depressive disorder affects approximately 8% of adults in the United States in any given year and is the leading cause of disability worldwide. The USPSTF recommends screening all adults for depression in clinical practices with adequate systems for diagnosis, treatment, and follow-up (Grade B recommendation). The PHQ-9 has a sensitivity of 88% and specificity of 88% for major depression at a cutoff score of 10 (Manea et al., CMAJ 2012).

## Features

- **Full PHQ-9 Scoring:** Nine items scored 0-3, total range 0-27, with five severity levels (none/minimal, mild, moderate, moderately severe, severe)
- **PHQ-2 Ultra-Brief Screen:** Two-item initial screen; score >= 3 triggers full PHQ-9
- **DSM-5 Criteria Mapping:** Each item maps to a specific DSM-5 criterion for major depressive episode; algorithmic check for probable MDD (>= 5 symptoms including at least one core symptom)
- **Item 9 Suicide Risk Flagging:** ANY positive response on Item 9 generates an immediate safety protocol with structured assessment guidance, crisis resources, and documentation requirements
- **Treatment Recommendations:** Severity-tiered recommendations from watchful waiting (mild) through combined psychotherapy + pharmacotherapy (severe), aligned with APA Practice Guidelines
- **Longitudinal Treatment Monitoring:** Track PHQ-9 scores over time to assess treatment response (>= 50% reduction) and remission (score < 5)

## Safety Classification: CAUTION

The PHQ-9 is a screening tool and does not establish a diagnosis. Item 9 screens for suicidal ideation and requires immediate clinical follow-up regardless of the total score. All patients endorsing suicidal thoughts must receive a comprehensive safety assessment.

## References

- Kroenke K, et al. "The PHQ-9: Validity of a Brief Depression Severity Measure." *J Gen Intern Med*. 2001;16(9):606-613.
- Manea L, et al. "Optimal Cut-off Score for Diagnosing Depression with the PHQ-9." *CMAJ*. 2012;184(3):E191-E196.
- USPSTF. "Screening for Depression in Adults." *JAMA*. 2016;315(4):380-387.
- Lowe B, et al. "Monitoring Depression Treatment Outcomes with the PHQ-9." *Med Care*. 2004;42(12):1194-1201.
