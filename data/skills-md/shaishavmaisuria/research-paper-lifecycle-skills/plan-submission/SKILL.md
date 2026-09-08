---
name: plan-submission
description: Builds a backwards submission timeline from a conference deadline - days remaining (AoE-aware), abstract-registration offsets, author-list freeze, OpenReview/CMT/EasyChair/HotCRP/PCS account lead times and per-system steps, supplementary-material and code size limits, reciprocal-reviewing duties, and a dual-submission audit. Use when the user wants to plan a submission, asks how long until a deadline, mentions abstract registration, submission checklist, deadline countdown, "what do I need before the NeurIPS/ICML/CHI deadline", or asks what happens after submitting (rebuttal window, notification, camera-ready). Phase-aware - produces pre-submission, under-review, and camera-ready plans from venues/ profiles and flags overdue steps.
---

# Plan Submission

Turn "the deadline is in N weeks" into a dated, phase-aware milestone plan.
Works backwards from the paper deadline (or forwards through rebuttal and
camera-ready if the deadline already passed), anchored to a
`venues/conferences/<venue>-<year>.yml` profile. Companion skills:
`parse-cfp` (creates the profile), `preflight-check` (the T-3d desk-reject
lint), `write-rebuttal`, `prepare-camera-ready`.

## When to use

- "Plan my SIGSPATIAL submission" / "what do I need to do before the deadline?"
- "How many days until the NeurIPS deadline?" (AoE confusion included)
- "When do I have to register the abstract?" / "when does the rebuttal start?"
- The user just picked a venue (via `select-venue`) and asks "what now?"

## Inputs

- A venue + year (and ideally a track). The profile must exist at
  `venues/conferences/<venue>-<year>.yml`; if it does not, run `parse-cfp`
  first — never plan from remembered dates.
- Today's date, and any user-specific constraints (vacations, co-author
  availability, experiments still running).
- `CONTACT_EMAIL` env var if the live re-verification fetch is used.

## Process

1. **Resolve the venue profile.** Locate
   `venues/conferences/<venue>-<year>.yml`. Missing or from a previous
   cycle → route through `parse-cfp` to create/refresh it before planning.
   Check the profile's `verified:` block — if `confidence` is not
   `verified-live` or `verified.date` is old, treat every date as suspect.

2. **Re-verify the critical dates against the live CFP.** Mandatory before
   the user relies on the plan. Run:

   ```
   python3 scripts/fetch_page.py "<cfp_url from the profile>"
   ```

   Confirm the abstract deadline, paper deadline, and timezone on the live
   page (deadlines slip mid-cycle — extensions are common, but so are
   silent corrections). On mismatch, update the profile first. If the page
   is JS-rendered or down, say so and mark the plan "dates unverified".

3. **Build the timeline.** Run:

   ```
   python3 scripts/build_timeline.py venues/conferences/<venue>-<year>.yml \
       --track "<track>" --today YYYY-MM-DD
   ```

   The script is offline and deterministic: it detects the current phase
   (pre-submission / under-review / camera-ready), computes days remaining
   for every profile deadline, and emits dated milestones with standard
   backwards offsets (T-21d dual-submission audit and reciprocal-reviewing
   check, T-14d system accounts, T-10d author-list freeze, abstract
   registration at its real date, T-5d supplementary, T-3d preflight, T-2d
   draft upload, T-1d final upload). `--camera-ready YYYY-MM-DD` supplies a
   deadline the profile lists as null. `--format json` for machine use.

4. **Customize the milestones** using
   [references/milestone-playbook.md](references/milestone-playbook.md):
   what each milestone actually requires, why the offset is what it is,
   supplementary/code size limits, reciprocal-reviewing mechanics, and the
   AoE math. Adjust offsets for the user's constraints (e.g. co-author on
   leave at T-10d → freeze the author list earlier). Never move a HARD
   deadline; only prep milestones are adjustable.

5. **Add per-system steps** from
   [references/submission-systems.md](references/submission-systems.md) for
   the profile's `review.submission_system` — account lead times (OpenReview
   profile moderation can take ~2 weeks), what the submission form demands,
   conflict-of-interest entry, and each system's signature gotcha (HotCRP's
   "ready for review" checkbox, PCS metadata lock, EasyChair co-author email
   typos, CMT COI lists).

6. **Run the dual-submission audit interactively.** Quote the profile's
   `review.dual_submission` policy verbatim, then ask the user to inventory
   every overlapping manuscript by ANY co-author that is under review or
   planned elsewhere (including workshop versions and arXiv plans). Flag
   conflicts against the quoted policy; when the policy is ambiguous, say
   so and point at the CFP — do not adjudicate.

7. **Present the plan**: phase, key-dates table with days remaining,
   milestone table (OVERDUE items first, called out explicitly), per-system
   steps, policy gates, and the re-verify warning. If the paper deadline
   has already passed, do NOT pretend otherwise — plan the next phase and
   say plainly which deadlines are gone.

## Output

A dated submission plan in Markdown: current phase, key dates with
days-remaining (timezone noted), backwards milestone schedule with status
(in Nd / TODAY / OVERDUE / PASSED), submission-system checklist, policy
gates (dual submission, LLM policy, reciprocal reviewing), and the closing
notice: *"Dates from `<profile>` (verified `<date>`). Re-verified against
`<cfp_url>` on `<today>`. Deadlines change mid-cycle — check the CFP again
before each milestone."*

## Guardrails

- Never invent a date. A `null` in the profile stays unknown in the plan,
  with an instruction on where to find it — a guessed deadline is worse
  than none.
- Always state the timezone next to every deadline. AoE is common, not
  universal (SIGSPATIAL uses Pacific Time); a wrong assumption costs a day.
- Never submit, register, create accounts, or click anything in any
  submission system on the user's behalf. The plan tells the user what to
  do; the user does it.
- Past deadlines are reported as passed, never silently dropped or
  rescheduled.
- One page per fetch-script invocation; cache stays under `.cache/`
  (gitignored); never commit fetched CFP text.

## Bundled files

- [references/milestone-playbook.md](references/milestone-playbook.md) —
  what every milestone requires, default offsets and their rationale,
  supplementary/code limits, reciprocal reviewing, dual-submission audit,
  AoE math.
- [references/submission-systems.md](references/submission-systems.md) —
  per-system walkthroughs: OpenReview, CMT, EasyChair, HotCRP, PCS.
- `scripts/build_timeline.py` — deterministic phase-aware timeline builder
  (run it; do not compute date arithmetic by hand).
- `scripts/fetch_page.py` — polite single-page fetcher for live CFP
  re-verification (vendored from `parse-cfp` so this skill is
  self-contained).
- `scripts/venue_profile.py` — shared profile loader (YAML-subset parser +
  family merge), vendored for self-containment.
