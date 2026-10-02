---
name: find-medical-specialist
description: Find and compare medical specialists in a requested area and time horizon using Zocdoc and the two strongest local hospitals for that specialty. Screen credentials, insurance and availability, evaluate written patient reviews, and maintain one ranked CSV. Use for provider research, not diagnosis or treatment advice.
---

# Find a medical specialist

Deliver one ranked CSV and a concise, sourced explanation of who survived clinical-review screening and why. Match the layout described in [references/csv-schema.md](references/csv-schema.md). Reuse an existing candidate CSV when supplied; do not leave competing final versions.

## Inputs and defaults

Require four inputs:

- **Specialty:** the type of specialist.
- **Area:** city, boroughs, region or a clearly bounded radius.
- **Time horizon:** a duration from today or an explicit appointment deadline.
- **Insurance:** carrier and exact plan/product name, or an explicit self-pay/uninsured search.

Infer these from the request/context when clear. Ask for missing required inputs together. Use the user's local date/timezone; resolve the horizon to an inclusive cutoff and state the exact search area and date range before research.

Optional inputs: symptoms or condition focus, adult/pediatric patient, sex-related care eligibility, appointment time, in-person/video preference, credentials, named hospitals, review thresholds and deeper-review batch size. Carry forward explicit preferences in the same session. Do not put a particular user's insurance or health information into this reusable skill.

If omitted, proceed with clearly stated assumptions: adult outpatient care, new-patient in-person visits, appointments strictly after 12:00 pm, and physician credentials MD or DO. Adapt credentials to the specialty explicitly requested (for example DDS/DMD for dentistry); do not substitute an NP/PA or a different profession without permission. Do not require sex information unless needed for an obvious eligibility restriction. Insurance is required before completing network screening. Reuse a clearly supplied plan from this session; otherwise ask for the carrier and exact plan/product together with any other missing required inputs. A carrier name alone is not an exact plan; request the missing plan detail while continuing independent hospital/provider discovery. An explicit self-pay/uninsured instruction satisfies this input, with network screening marked Not applicable. Do not invent plan details or request an insurance card/member ID for public provider research.

## Choose the two hospitals

Use current web research to identify the two strongest hospital systems for the requested specialty that have relevant outpatient specialists inside the area. Start with specialty-specific rankings or outcome evidence from a credible independent source and verify the actual department and locations on official hospital websites.

Hospital reputation overall is insufficient. Match the specialty, adult/pediatric context and any supplied condition focus. Distinguish nationally ranked specialties from local reputation and distinguish independent ranking evidence from a hospital's own marketing. Rankings may assess inpatient care rather than the outpatient doctor; use them to select sources, not to score individual physicians.

Explain the two choices briefly with links, evidence dates and uncertainty. Treat a named hospital as an override when requested. Use separate systems rather than two campuses of the same system where possible. If the region lacks two relevant hospitals, use the available hospital and the strongest relevant academic/specialty center; disclose the substitution. For specialties/geographies Zocdoc does not cover, report that source gap and continue with the other sources.

## First pass: collect and screen

Search **Zocdoc + both hospital physician directories**. Use specialty/condition terms and the whole requested area. Do not inherit an accidentally zoomed map or a narrower appointment-date filter from an attached tab. Check pagination and multiple physician office locations. Collect relevant unique physicians from accessible result pages, deduplicating by full name, specialty, NPI when available and affiliations. Combine sources on one row. An outside office does not disqualify a physician who also has an eligible office.

Screen in this order:

1. Verify identity, relevant specialty and acceptable credentials on official profiles.
2. Check obvious patient eligibility. For an adult patient, exclude profiles explicitly pediatric-only. If a male patient is specified, reject only an obvious women-only practice; female physician gender or expertise in women's health is not itself an exclusion. Do not deep-dive eligibility when the profile is clear.
3. Verify at least one location inside the area.
4. Check the supplied exact plan on the physician/location's booking page or official insurer/provider source. Distinguish **confirmed in-network**, **closest listed plan / exact network unverified**, **carrier only**, **unknown**, and **confirmed out-of-network**. Carrier acceptance and hospital participation do not establish this physician's exact network. Keep plausible but unverified matches conditional; exclude confirmed out-of-network unless the user allows alternatives.
5. Check new-patient availability through the inclusive cutoff at the eligible office. Record the earliest appointment strictly after noon separately from the earliest appointment at any time, with the local timezone. Keep unknown or phone-only availability conditional; do not turn uncertainty into an exclusion. Record proven failures to meet the deadline/time preference separately from unknown availability. Do not use generic FAQ claims as evidence of a real slot.
6. Default Zocdoc threshold: **4.6 or higher when a rating exists**. Hospital-directory candidates without a matching Zocdoc profile or without ratings remain eligible; leave absent data blank and explain. Do not invent matching profiles from similar names.
7. For credential-eligible and insurance-plausible candidates, inspect the matching **Google** physician/location listing. Default threshold: **at least 4.5 when there are more than 10 ratings**. Smaller samples or no reviews do not automatically exclude; flag uncertainty. Do not assign a group practice's rating to an individual physician without attribution.
8. Collect **Healthgrades and WebMD** ratings, counts and profile links when available for every retained first-pass candidate. Use another established written-review source, such as Vitals, if a source is absent or adds useful clinical evidence. Add corresponding columns when actually used. No extra star threshold applies to these sources unless specified.

For each fact preserve a direct source link and checked date. Distinguish rating count from number of written comments. Zero means a verified empty review profile; blank means unknown, not collected or no matching profile. Search-result snippets and cached pages can be useful but must be labeled when they are the only accessible evidence.

Keep one row per candidate. Include first-pass survivors and candidates explicitly reviewed then excluded, so decisions remain auditable. Keep other first-pass exclusions in working records unless the user wants the entire exclusion inventory. Never describe an incomplete source search as exhaustive: record accessible pages, coverage and concrete gaps.

## Rank, then read actual comments

First create a provisional order using ratings and sample sizes across platforms. Discount very small samples, avoid treating hundreds of star-only ratings as hundreds of informative comments, and give less weight to institution-hosted ratings than independent written accounts. Do not use an opaque star average as the final clinical judgment.

By default perform a deeper pass on **eight** strong candidates: at least two from each discovery source when viable, plus the next two strongest candidates by review evidence. Deduplicate across affiliations. If fewer candidates exist, review the available pool. If a source cannot supply its share, disclose the gap and fill from the others. Do not restore an obviously ineligible physician merely to fill a quota. When the user requests a follow-up batch, take the next unreviewed ranked candidates, respecting any specified source split; revisits do not count as new independent evidence.

Read actual written comments from the first few review pages, including recent and lowest-rated views when available. Read more when medical concerns appear, the sample is small enough to finish, or the initial pages are too generic. Expand truncated comments. For institution profiles with manageable comment counts, read all published comments.

Prioritize:

- **Clinical concerns:** dismissal of symptoms, refusal to listen, poor diagnostic explanation/workup, claimed missed diagnosis, problematic treatment changes, failure to discuss results or follow up, extreme disrespect directed at the patient.
- **Clinical positives:** careful history/record review, thoughtful evaluation, clear reasoning, shared treatment decisions, symptom validation, appropriate referrals, useful follow-up and longitudinal disease management.
- **Lower weight:** punctuality, long waits, billing, scheduling and office demeanor. An administrative problem becomes clinically important when the account describes lost results, interrupted treatment or failure to obtain medical follow-up.

Separate what the reviewer reports from what can be verified. A patient alleging misdiagnosis is not proof of misdiagnosis or malpractice. Repeated testing or a disputed treatment choice alone does not establish poor care. Do not let a single anecdote automatically outweigh a broad, specific positive record; consider seriousness, specificity, recency, independence and counterevidence. A conservative exclusion based on one serious account must explicitly say it is isolated and unverified.

Count apparent cross-platform duplicates once. Star-only low ratings have an unknown cause. Keep the doctor's behavior separate from staff behavior when the comment distinguishes them. Do not treat absent reviews as evidence of good or bad care.

For every deeper-pass candidate record the platforms, number of written comments read, date range/key complaint dates, recurring clinical positives, clinical concerns, counterevidence, decision and limitations. If review access requires login or verification, use accessible evidence and disclose the gap; do not claim unread pages were vetted.

## Final ranking and deliverables

Use written clinical evidence as the principal basis for deeper-pass ranking. Order the strongest reviewed survivors first. Preserve a lower-confidence tier for reviewed candidates with too little written evidence; completing a source check does not justify promoting a doctor with no comments above candidates with useful evidence. First-pass-only candidates retain provisional ranks based on rating/count evidence and are explicitly marked **First pass only**.

Rank active candidates with unique consecutive integers. Use **N/A** for excluded candidates retained for audit. Keep first-pass screening status separate from review judgment in Notes. A review-only rank never overrides known insurance, geography or appointment failures. When the user explicitly requests review-only comparison of previously filtered candidates, include them with the original practical exclusion visible.

Update the same CSV on each follow-up. Keep **Ranking first and Notes last**. Notes must identify **Second pass completed**, **First pass only**, or **Second pass: source check; insufficient written evidence**, along with rationale and coverage limits. Include sourced years of experience for the current top five if available: label the definition consistently (approximately years since medical/professional degree, including training) rather than conflating it with years of independent specialty practice. Update top-five experience when ranks change; leave unknown values blank.

Use the CSV schema reference when writing. Apply an available spreadsheet skill for artifact authoring and an available browser skill for UI research when those tools are needed. Keep intermediate evidence in work/ and only one final candidate CSV in outputs/. Preserve existing source data and prior decisions unless new evidence justifies a documented change.

Validate that names are deduplicated, source links match identities, ranks are consecutive, exclusions use N/A, unknowns are not zero-filled, the cutoff/timezone are correct, and prior fields survive updates. Verify the saved CSV parses with the declared column order. Finish with a link to the CSV, brief hospital-selection rationale, retained/excluded candidates and the clinical reasons, common positives, and any meaningful coverage limits. Do not book appointments or contact offices as part of this research skill.
