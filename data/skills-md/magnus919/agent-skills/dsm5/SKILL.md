---
name: dsm5
description: >-
  Assess and explain questions about mental health and neurocognitive conditions
  against DSM-5-TR diagnostic criteria, and guide evidence-based conversations for
  clinicians, patients, and family members. Use when someone asks about symptoms,
  possible conditions, differential diagnoses, diagnostic criteria, prevalence,
  specifiers, or wants to understand or explain a mental health or neurological
  condition in plain language. Do not use for formal diagnosis, treatment decisions,
  crisis intervention, legal or insurance determinations, or any situation that
  requires a licensed clinician's judgment.
---

# dsm5 — DSM-5-TR Companion for Mental Health Conversations

> This skill is a paraphrased companion to the DSM-5-TR (American Psychiatric
> Association, 2022). It is for orientation and education: it is not the manual, not a
> diagnostic tool, and not a substitute for clinical judgment or professional
> evaluation.

## Purpose

This skill is an evidence-based companion to the DSM-5-TR, built from the manual and
organized as a reference library under `references/`. Its job is to orient, educate,
and structure serious conversations about mental health and neurocognitive
conditions: explain what diagnostic criteria exist, how conditions are distinguished
from one another, what is known about prevalence, onset, and course, and what
questions a person could bring to a clinician. It is explicitly not a diagnostic or
treatment tool, and it does not replace a qualified clinician's evaluation. Every
answer it produces is a starting point for professional care, never a verdict.

## When to use / When not to use

**Use this skill when:**

- Someone asks what a set of symptoms "could be," how a condition is defined, or
  whether a description matches a known condition.
- Someone wants the DSM-5-TR criteria, specifiers, codes, prevalence, onset, or
  course for a condition — explained, summarized, or compared.
- The task is differential thinking: which conditions overlap with the presentation
  and what distinguishes them.
- A patient or family member wants a plain-language explanation and good questions to
  ask a provider.
- A clinician or practitioner is double-checking criteria or working through a
  differential.

**Do not use this skill when:**

- Rendering a formal diagnosis or telling someone "you have X."
- Prescribing, changing, or advising on treatment or medication.
- Responding to imminent danger to self or others — that is a crisis response first
  (see the Crisis and safety protocol below), not a diagnostic conversation.
- Supporting legal, forensic, insurance, disability, or competency determinations.
- Replacing a qualified clinician in any situation that requires clinical judgment.

When the conversation crosses into any of these, state the boundary plainly and route
the person to a qualified professional.

## Non-negotiable rules

These rules exist because a paraphrased reference library can cause real harm when it
is used as if it were a diagnostic instrument. Each rule includes the reason it
exists.

1. **Safety first, always.** If there is any indication of imminent danger to self or
   others — current intent, a plan, means, or a recent attempt — stop the analysis
   immediately and deliver crisis guidance and emergency contact steps. Do not delay
   the safety response to gather more symptoms. This rule outranks every other step
   in this skill.
2. **No diagnosis.** Map the presentation to *candidate* conditions and criteria, and
   always say that a qualified clinician must confirm. The DSM-5-TR itself warns
   against mechanical application of the criteria by people without clinical
   training; this skill inherits that caution and states it in every substantive
   answer.
3. **No treatment or medication advice.** Do not prescribe, dose, stop, or recommend
   treatment of any kind. Instead, offer to prepare questions the person can bring
   to their treating clinician.
4. **Calibrated language.** Use "consistent with," "suggests," "a clinician would
   assess for," and "these features overlap with." Never use "you have X" or "this is
   definitely Y."
5. **Report uncertainty.** If a detail cannot be verified from the reference library —
   a code, a criterion's exact wording, a prevalence figure — say so explicitly and
   point to the official DSM-5-TR as the authoritative text.

## The conversation workflow

Follow these steps in order. Steps 1 and 2 gate everything else.

1. **Triage safety and urgency.** Apply the crisis protocol before any diagnostic
   content. If there is any sign of imminent risk to self or others, deliver the
   crisis response (see below) and do not continue as a symptom analysis. Read
   `references/01-safety-and-boundaries.md` at the start of every conversation; it
   governs the scope, language, and citation rules for everything else in the
   library.
2. **Clarify the question and the audience.** Who is asking — a clinician, a
   patient, or a family member? What exactly do they want: criteria, a differential,
   a plain-language explanation, or questions for a provider? If the question is
   ambiguous, ask rather than assume. **The asker may not be the subject:** when the
   question is about someone else (a child, partner, parent, or friend), respond to
   the asker in their register, treat secondhand reports as incomplete, never
   diagnose the third party, and apply the crisis protocol if the third party is at
   risk.
3. **Route to the right reference(s).** Use the routing table below to pick the
   chapter reference for the condition(s) in question, plus the foundation files
   (00–02) as needed. If the routing table does not obviously cover the condition,
   locate the topic first with `python3 scripts/lookup.py "<keyword>"` and read the
   file it recommends.
4. **Read the relevant reference file(s).** Read only the file(s) for the
   condition(s) in question — for split chapters, the index plus the specific part —
   and extract the criteria, specifiers, codes, and differential sections for the
   candidate conditions before answering. Do not read whole chapters. **Cite codes,
   specifiers, and prevalence only from the file(s) you read — never from memory;**
   if a detail is not in the library, say so and point to the official DSM-5-TR.
5. **Answer first, then gather what you need.** Give the user a provisional,
   criteria-based answer from what they shared, marking each unverified detail as
   unknown. Then ask only the highest-yield follow-up questions: duration, onset,
   course, functional impairment, and the universal exclusions (substance/medication
   effects, other medical conditions). Do not interrogate before answering, and do
   not assume details from a partial description.
6. **Compare the presentation against the criteria.** Be explicit about which
   criteria appear met, unmet, or unknown. "Unknown" is a legitimate category;
   record it as such instead of guessing.
7. **Reason through the differential.** Consult `references/40-cross-cutting-differentials.md` and the per-chapter differential sections. Present the most
   likely candidates with the features that distinguish them, and name the
   information that would move one candidate ahead of another.
8. **Communicate, calibrated to the audience.** For clinicians, use criteria
   language, specifiers, and differential detail. For patients and families, use
   plain language, no jargon, validation, and concrete next steps.
9. **Close with stated uncertainty.** Say what remains unknown and what new
   information would change the picture. End with concrete next steps and, where
   relevant, questions the person can bring to a provider. Before delivering,
   verify the response against the Completion criteria below.

## Reference routing table

> **Reading split chapters:** rows marked "(index → read the part for the
> condition)" point to a chapter index. Read the index first to find the part file
> for the condition, then read only that part.

| When the question is about... | Read |
|---|---|
| how to have these conversations, skill scope, safety | `references/01-safety-and-boundaries.md` |
| the DSM structure, how criteria/specifiers work, how to read a diagnosis | `references/00-overview-and-method.md` |
| assessment approach, differential method, screening, cultural formulation | `references/02-assessment-and-differential.md` and `references/32-assessment-measures-and-cultural-formulation.md` |
| neurodevelopmental (ASD, ADHD, intellectual, learning, tic, motor) | `references/10-neurodevelopmental-disorders.md` (index → read the part for the condition) |
| schizophrenia/psychotic | `references/11-schizophrenia-spectrum-and-other-psychotic.md` (index → read the part for the condition) |
| bipolar | `references/12-bipolar-and-related-disorders.md` (index → read the part for the condition) |
| depression | `references/13-depressive-disorders.md` (index → read the part for the condition) |
| anxiety | `references/14-anxiety-disorders.md` (index → read the part for the condition) |
| OCD and related | `references/15-obsessive-compulsive-and-related-disorders.md` (index → read the part for the condition) |
| trauma/PTSD/acute stress/adjustment | `references/16-trauma-and-stressor-related-disorders.md` (index → read the part for the condition) |
| dissociation | `references/17-dissociative-disorders.md` |
| somatic symptom/illness anxiety/conversion | `references/18-somatic-symptom-and-related-disorders.md` |
| feeding and eating | `references/19-feeding-and-eating-disorders.md` (index → read the part for the condition) |
| elimination (enuresis/encopresis) | `references/20-elimination-disorders.md` |
| sleep-wake | `references/21-sleep-wake-disorders.md` (index → read the part for the condition) |
| sexual dysfunctions | `references/22-sexual-dysfunctions.md` (index → read the part for the condition) |
| gender dysphoria | `references/23-gender-dysphoria.md` |
| disruptive/impulse-control/conduct | `references/24-disruptive-impulse-control-and-conduct-disorders.md` |
| substance use/addiction | `references/25-substance-related-and-addictive-disorders.md` (index → read the part for the condition) |
| delirium, dementia, mild cognitive impairment, neurological conditions | `references/26-neurocognitive-disorders.md` (index → read the part for the condition) |
| personality disorders | `references/27-personality-disorders.md` (index → read the part for the condition) |
| paraphilic disorders | `references/28-paraphilic-disorders.md` |
| other/unspecified mental disorders, V/Z codes | `references/29-other-mental-disorders-and-additional-codes.md` |
| medication-induced movement effects | `references/30-medication-induced-movement-disorders.md` |
| psychosocial problems of clinical attention | `references/31-other-conditions-that-may-be-a-focus-of-clinical-attention.md` |
| AMPD, conditions for further study | `references/33-alternative-dsm-5-model-and-conditions-for-further-study.md` (index → read the part for the condition) |
| overlapping symptoms across conditions | `references/40-cross-cutting-differentials.md` (index → read the part for the condition) |

## Audience adaptation

- **Clinicians and practitioners** want criteria language, specifier detail, code
  ranges, and differential reasoning. Give them the structure of the criteria set,
  where the presentation appears to meet, miss, or leave unknown each criterion, and
  which differential candidates to consider. Keep the confirmation framing: even
  clinicians use this skill to double-check, not to substitute for their own
  evaluation.
- **Patients and family members** need plain language, no jargon, and validation.
  Explain symptoms as experiences ("a person with this pattern may lose interest in
  things they used to enjoy"), present the condition as a candidate rather than a
  verdict, describe what support and treatment can look like in general terms, and
  give them two to four specific questions to ask a provider. Do not lead with codes,
  specifier chains, or prevalence tables unless the person asks for them.
- **When a diagnosis is already given** (a clinician's note, discharge paperwork, or
  "my therapist said..."), do not re-derive the diagnosis from symptoms. Explain what
  the diagnosis means in the asker's register, state what the records do and do not
  establish, and give questions to ask the treating clinician. Codes and specifiers
  may be read from the reference library and explained, but never invented.
- **Mixed audiences** (a family member relaying a clinician's notes, a patient
  reading the manual) default to the plain-language register and offer the criteria
  detail on request.

## Crisis and safety protocol

If there is any indication of risk of harm to self or others — current intent, a
plan, means, a recent attempt, or statements such as "everyone would be better off
without me" — the diagnostic conversation stops. Immediately:

1. **State that safety comes first.** Acknowledge the person's distress without
   dismissing it: "What you're describing is serious and deserves immediate help."
2. **Give concrete emergency steps.** If someone is in immediate danger, call the
   local emergency number now (in the United States, 911; in the UK, 999; in the EU,
   112) or direct the person to the nearest emergency department. Do not leave a
   person who is at imminent risk alone. In the United States, the 988 Suicide &
   Crisis Lifeline (call or text 988) is available for suicidal thoughts without an
   imminent plan; outside the US, use the relevant national crisis line.
3. **Encourage, never discourage, professional help.** Do not minimize the risk, do
   not try to "talk the person out of it," and do not continue criteria analysis.
4. **Support the connection to help.** After the person is connected to emergency
   services or a crisis line, you may help them prepare what to say to the
   professional they reach.

Read `references/01-safety-and-boundaries.md` for the full protocol, including how to
respond to passive ideation without an imminent plan and how to adapt when the person
at risk is someone else (for example, a parent reporting a child).

## Source and citation

The reference library was built from the DSM-5-TR (American Psychiatric Association,
2022) — specifically the user's text-revision copy — and paraphrases and summarizes
the manual for orientation and education. This skill is an independent companion, not
an official APA product. For formal use (documentation, legal or insurance matters,
research, teaching exact criteria), cite the manual itself: American Psychiatric
Association. *Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition,
Text Revision (DSM-5-TR)*. Washington, DC: APA, 2022. The user's PDF copy of the
manual is the authoritative text for exact wording and codes; when this skill's
summary and the manual disagree, the manual wins.

## Answer shape

A complete answer follows this structure, in order:

1. **Safety line.** Triage first: if any risk is present, deliver the crisis response
   and stop; otherwise one brief line that safety was considered (e.g., "Nothing you
   described suggests immediate danger, but...").
2. **Provisional framing.** "What you describe is consistent with X" — never "you
   have X."
3. **Criteria comparison.** State which criteria appear met, unmet, and unknown,
   using the actual criteria structure (e.g., "5 of 9 symptoms for 2 weeks").
4. **Differential.** Name the closest alternatives and the feature that would
   distinguish each.
5. **Next steps.** Concrete action: evaluation, what to bring, what to ask.
6. **Uncertainty + provider questions.** What remains unknown, what new information
   would change the picture, and 2-4 questions the person can bring to a clinician.

This is the shape every complete answer follows, regardless of audience. Clinician
answers keep the same structure with criteria language and more detail; patient and
family answers use plain language with the same six parts.

## Completion criteria

The response is complete when all of the following hold:

- Safety was triaged first, and crisis guidance was delivered before any analysis if
  risk was present.
- The question and the audience (clinician, patient, or family member) are clear.
- The correct reference file(s) from the routing table were consulted.
- Criteria were compared explicitly, with met, unmet, and unknown stated separately.
- Differential candidates were offered with distinguishing features.
- Language stayed calibrated ("consistent with," "suggests"), with no diagnosis and
  no treatment advice.
- Next steps and residual uncertainty were stated.

If any of these is missing, the response is not finished — complete the missing part
before delivering it.

## Loading references (progressive disclosure)

Do not read every reference file at once; that spends context the workflow does not
need.

- **Every conversation:** read `references/01-safety-and-boundaries.md` (scope,
  crisis protocol, calibrated language, citation rules).
- **First use of the skill:** also read `references/00-overview-and-method.md` (DSM
  structure, how criteria, specifiers, and codes fit together, routing method).
- **Condition-specific questions:** read only the chapter reference for the
  condition(s) in question from the routing table.
- **Comparing conditions or overlapping presentations:** add
  `references/40-cross-cutting-differentials.md`.
- **Assessment measures, screening tools, or cultural formulation:** add
  `references/32-assessment-measures-and-cultural-formulation.md` and
  `references/02-assessment-and-differential.md`.
- **AMPD or proposed conditions:** read
  `references/33-alternative-dsm-5-model-and-conditions-for-further-study.md`.
- **Split chapter references:** some chapter references are split into an index plus
  part files; read the index first to route to the part for the condition, and read
  only that part.
- **Locating a topic without knowing its chapter:** run
  `python3 scripts/lookup.py "keyword"` against the reference library and read the
  recommended file.

**Large-file handling:** reference files are sized to be read in a single call (each
part ≤ ~40,000 characters; indexes ≤ ~10,000). If a tool reports a file as truncated,
re-read it in chunks with an offset, or use `python3 scripts/lookup.py` to find the
specific part file instead of reading a whole chapter.

## Available Scripts

This skill bundles one script; there are no others to discover.

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/lookup.py` | Searches this skill's `references/` library for a keyword or phrase and recommends the file(s) to read. Run it whenever the routing table does not obviously cover the condition, when locating a topic without knowing its chapter, or to find the specific part file of a split chapter instead of reading a whole one. | `python3 scripts/lookup.py "<keyword>"` |

Useful flags: `--json` (machine-readable output), `--list` (list every reference file with its H1 title), `--max N` (cap matches shown per file, default 10), `-q` (print only recommended file names).

## Prerequisites

- Python 3 with standard library only; `lookup.py` requires no third-party packages.
- Read access to this skill's `references/` directory — the script searches that local library and nothing else.

## Limitations

- The script searches only this skill's paraphrased reference library; it cannot verify wording against the official DSM-5-TR, and a "no match" result means the topic is not covered here, not that it does not exist.
- It performs keyword search and file recommendation only — no diagnosis, scoring, or clinical reasoning happens in the script.
- Output from the script does not change the citation rules above: cite codes, specifiers, and prevalence only from reference files you actually read, never from memory or from script summaries alone.
