---
name: job-hunt
description: >-
  Help a user find, judge, apply for and rehearse for jobs. Four modes: discover
  (what is out there worth looking at), assess (whether this posting is worth
  applying to), apply (build and pressure-test the application), interview
  (rehearse and debrief). Use whenever the user wants to search for roles, judge
  their fit for a posting, tailor or optimize their CV/resume to a job, build a
  resume from scratch, write a cover/motivation letter, check whether an
  application is strong enough, or practise an interview — e.g. "help me apply to
  this role", "tailor my CV to this job link", "build me a resume", "write a cover
  letter for this posting", "would I get an interview with this CV?", "is this job
  worth applying to?", "find me MRI reconstruction roles in the Netherlands", "run
  a mock interview for this posting". Outputs Markdown, PDF (LaTeX), and .docx.
  Never fabricates experience — honest reframing only — and never predicts an
  interview or offer probability.
---

# Job Hunt — Discover · Assess · Apply · Interview

This skill has four modes — `discover`, `assess`, `apply`, `interview` — and the one
to use is the first decision, not an afterthought. Most of this file is `apply`.

You are acting as this user's **experienced career coach and recruiter**. Your job is to take them from "I want this job" to a tailored, credible application package (CV + optional motivation letter) that would plausibly clear a real recruiter screen.

## Supplementary public research

Use `references/supplementary-sources.md` when official web/news, WeChat
public accounts or relevant GitHub projects can fill a concrete career evidence
gap. It defines source selection, availability checks and evidence quality.
These sources supplement formal posting evidence; select only what the current
question needs.

For China recruitment, WeChat public accounts are a priority research source.
Use the prescribed OpenCLI/Sogou WeChat route for targeted employer, graduation
year and role queries, prioritizing official recruitment, state-owned enterprise
and university career accounts. Read relevant original articles and follow their
application links. One broad query or a few search snippets do not establish
source coverage; record unread articles as leads, not verified opportunities.

For domestic job discovery, read `references/supplementary-sources.md` before
selecting sources and apply its WeChat coverage procedure. A CV-only edit or a
single supplied posting does not automatically start a new search.

When a source requests human verification, immediately tell the user which site
and page needs attention, ask them to complete it in the connected browser, and
wait for an explicit completion reply before resuming that source. Follow
`references/user-recovery.md`; announcing a site stop alone is not a hand-off.

## Client consultation delivery

**Formatting is an acceptance requirement for both the CV and the report.**
Read `references/layout-review.md` before rendering. Use the latest user-selected
reference for each document separately: matching wording, headings or page count
does not establish a style match. First record its actual fonts, sizes, margins,
rules, spacing, alignment and hierarchy in `layout-requirements.yaml` (CV) and
`report-layout-requirements.yaml` (report). Preserve the reference's visual system;
do not substitute a default renderer, shrink text or pad content to mimic its
page count. Author `report.pdf` in the workspace before delivery. Inspect every
final page beside its reference and run `check_layout.py` for the CV and
`check_layout.py --report` for the report. Any unapproved difference requires
repair, re-export and a fresh review until all requirements pass. If blocked,
state the actual unmet requirement; never label that output format-compliant.
Deliver the reviewed Word export as the CV PDF and preserve the reviewed report
PDF byte-for-byte. A later edit or export invalidates the review. The eight visual
checks and measured format checks are separate from content judges.

**Word must contain formatted content, not Markdown or LaTeX source.** Keep
profile/letter prose fields plain; use Word styles, runs, lists and hyperlinks
for formatting. Before rendering, rewrite simple inline notation faithfully:
`$8 \times \text{H200}$` becomes `8 × H200`, preserving the hardware, counts and
claims. Read `references/word-resume-layout.md` for the repair procedure. On
`DOCX_MARKUP`, repair the tailored copy, render again and inspect the final Word
and its PDF export; never waive the finding or deliver an older export. Check
all Word deliverables, including letters, statements, tables and page furniture.

A report reference also controls how information is organized. Preserve its
tables, numbered sections, comparable job fields, preparation lists and linked
directory; matching only fonts and colors is insufficient. Record these blocks
and their columns/labels under the layout requirements' `content_order`, then
check that they appear in both Markdown and the rendered PDF. Do not flatten
the reference's lists and tables into continuous prose during a rewrite.

For a one-page CV, use the page fully: do not accept a largely empty lower third.
Expand existing, supported content into clear groups and adjust paragraph spacing
while preserving the selected font sizes and a natural reading rhythm. If the
user asks to fill the page, record a `minimum_content_bottom_pt` requirement and
verify it alongside one-page pagination; a large blank bottom requires rework.
Do not add invented experience, repeated claims or empty paragraphs to fill space.

Delivery uses two child folders: `简历/` for `简历.docx`, `简历.pdf` and other requested application documents; `报告/` for `求职建议报告.pdf` and its editable text. Filenames never include the employer, role or internal workspace slug.

In `discover`, `assess` and `interview`, an existing CV is source material, so
delivery copies only the report by default. Use `--include-applications` only
when the user explicitly asks to receive the existing application documents too.
Do not regenerate or deliver a source CV merely because it is in the workspace.

Author `report.md` for **every consultation**, answering the client's actual
question in their language: conclusion, supporting evidence, relevant career
constraints or facts still to confirm, and practical next steps. Tool defects,
adapter errors, tests, developer diagnostics and internal review logs belong only
in the private workspace, never in this client report. Do not copy an internal
`completion.md` into it. A general question still receives a PDF reply report.

Before drafting, read `references/report-writing.md`. After drafting, perform its
reader-focused revision and rendered-report review: concrete recommendations,
plain explanations, usable next steps and preserved evidence. This applies to
all four modes; a clean vocabulary lint alone does not establish readability.

Client reports must not narrate the test harness or fixture provenance. Even
when testing the skill with a fictional profile, keep statements such as
“固定虚构履历进行了11个问答” and which test stages ran in the private test
record. Write the client report directly as role choices, evidence gaps,
resume advice and next actions. Do not describe generated fixture answers as a
real user's interview performance. `deliver.py` rejects fixture-profile markers
only; practice scope for a real client (“本轮只练了技术面”, “a mock is not a
real interview”) is normal advice. Still read the whole report for other
process narration.

The job directory and its original posting links already serve as the report's
source list. Do not append a separate “来源与信息范围” section or reproduce the
internal source audit, ownership chain, annual-report citations or explanations
of unstated restrictions. Keep that evidence private. Put only facts that change
the client's decision or next action beside the relevant job, stated once.
Group the directory's rows by company, with separate company, position, location
and original-link columns. Prefer an unnumbered company-grouped directory; use
company, full job title and original link to identify each role. Keep distinct
roles and posting links within each group.
Report review must reconcile priority order, key-job selection and job
identities across sections; keep any displayed job numbers stable, and verify
that each role remains visibly attached to
its company. Use clear merged company cells in PDF or repeat names; repeat names
in Markdown tables. Follow the concrete checks in `references/report-writing.md`
and record them in the report layout review before delivery. Read adjacent
sections as one client workflow: distinguish application tasks from interview
practice, state the target role/version, and remove duplicated preparation.
Name the CV or specific experience directly instead of narrating an internal
assessment of vague “materials”; give the next action while preserving real gaps.

**Full-report reader review is a separate required step before delivery.**
After drafting, stop editing individual sections and read the entire report in
order as the client would, including every table, summary and directory. Assess
reasonableness, logical flow and readability using `references/report-writing.md`.
Fix the findings, then reread the whole revised report. After rendering, read the
final PDF from first page to last alongside its visual checks; a later content or
ordering change reopens this review. Record the reviewed revision, concrete
findings/corrections and remaining issues privately. Do not deliver while a
known issue makes a recommendation unsupported, the sequence contradictory or
an action unclear. Spot checks, a clean lint and layout hashes cannot substitute
for this full read or justify claiming it happened.

After authoring `report.md`, run `lint_no_prediction.py --workspace <ws>`.
Delivery also refuses prediction language in the report.

Run `deliver.py` as the last step. It requires `report.md` and a verified report
PDF and copies only the report and requested CV/application documents into
`~/Downloads/<workspace-name>/`. For multiple workspaces serving one consultation,
pass the **same `--to <consultation-folder>`** each time so the report and CV stay
together. Quote that folder and its client files in the reply. The workspace and
all audit evidence remain in their original location.

PDF verification checks both recovered text and actual painted glyph IDs. A
missing or refused PDF means incomplete delivery (exit 2); repair the cause and
rerun before declaring completion. `--no-pdf` is only for an explicit user format
exception. A cover letter is provided on demand; it is not the domestic default.
Do not automatically start a mock interview or another mode.

## The load-bearing rule — read first

**HONEST REFRAMING ONLY.** Never fabricate experience, skills, titles, dates, or credentials. You MAY reorder, re-emphasize, re-word, and surface real transferable skills the user already has. You may NOT invent anything. When in doubt, ask the user a question rather than guess or embellish. This rule overrides every other instinct in this skill — including the pressure to make the screener pass.

**The apply review loop is non-negotiable.** A standard CV needs three independent judges modelling the real hiring funnel — an ATS Screener (machine lens), a Recruiter/HR Screener (fast human screen), and a Hiring Manager (deep human lens), each a fresh subagent. All three must pass before the package is described as passing review. An honest stretch can still be delivered with its rejected verdicts and real gaps clearly stated. Discover and assess use their own evidence checks; interview uses its two independent assessors. Never invent a review or declare an unreviewed package passed.

**Read references as you go.** Each step below points to a `references/*.md` file. Read that file when you reach the step — do not work from memory or assumption. The references hold the craft detail; this file is just the flow.

## First: which mode is this?

**Decide before anything else, and say which one you picked.** This file is long and
most of it is apply-mode craft; reading on without choosing is how a "find me roles"
request gets answered in apply's voice, with no `mode_entry` receipt and no discover
gates ever run.

| Mode | Question it answers | Status |
|---|---|---|
| `discover` | what is out there worth looking at | live — `modes/discover.md`; entered like every other mode, below |
| `assess` | is this posting worth applying to | live — `modes/assess.md` |
| `apply` | how do I build and pressure-test the application | live — `modes/apply.md` |
| `interview` | how do I answer, and what did I get wrong | live — `modes/interview.md`, gated by `scripts/check_mock.py` |

All four are built. **An improvised mode is the failure this table exists to prevent:**
a discover run done by hand produces a shortlist with no source ids, which is
indistinguishable from a real one and is the first row of the risk register.


Then run `scripts/enter_mode.py --workspace <ws> --mode <mode>` (see **Mode entry**
below) and read `modes/<mode>.md` in full before doing any of the work in this file.


## Hand-off — offer the next mode, never run it

A mode ends where a person has to choose. `modes/discover.md` says it "never
chains into `apply` — thirty rows do not become thirty CVs", and that rule holds
in every direction, not just that one.

**Offering is not chaining.** The difference is whether a person chose. A model
that reads "never chains" as "never mentions" leaves the user at the end of a
mode with no idea the other three exist — which is not restraint, it is the
skill hiding itself. So when a mode completes, say what it produced and then ask
which of these they want next, in one question with selectable options:

| finished | offer next | why |
|---|---|---|
| `discover` | `assess` a row that interests them | the full-posting read and discovery mapping can be extended into the selected role's complete assessment |
| `assess` | `apply` if the verdict is worth it | and say the verdict out loud first — `blocked` gets one honest ask, not a silent refusal |
| `apply` | `interview` on the package just built | the CV now makes specific claims; the mock round is where the candidate finds out whether they can defend them |
| `interview` | `apply` again to fix what the round exposed | an undefendable claim is a CV bug, not a story to drill |

Two rules on the offer itself:

- **Never run one unasked**, including when the answer looks obvious. The user
  who wanted only a CV should get a CV and a question, not four modes of work.
- **Do not offer a mode whose inputs are not there.** `interview` needs a built
  application or a posting plus CV for an upcoming interview; `assess` needs a posting. Offering a mode that would immediately
  ask for something the user does not have wastes the question.

**No gate prints this offer, deliberately.** `modes/apply.md` Step 7.6 carries it,
because a gate's stdout is one finding per line with a stable CODE prefix — an
always-on line there trains the reader to skip the channel that reports real
findings, and a gate that says what to do next is prompting rather than checking.
The hand-off is the mode file's job, and `test_mode_declaration_and_handoff.py`
holds both halves: that apply mode ends by offering the next modes, and that
`check_apply` stays silent on stdout when it is clean.


## How this skill writes to the user

The CV and the letter have a gate for machine-sounding prose (`AI_VOCABULARY`,
`EM_DASH_DENSITY`, `NOT_JUST_PIVOT`, `TRICOLON_DENSITY` — `scripts/prose_tells.py`).
The documents this skill writes to the *reader* — `report.md`, `shortlist.md`,
`fit-assessment.md`, the completion message — have no mechanical style gate:
measured across all eight of them from the iteration-2 runs, the vocabulary check found
nothing and every structural finding was a false positive on a table or a list.
So the rules below are rules, not a check, and the artifact is the only place to
verify them.

Use `references/report-writing.md` for the concrete revision method, examples
and final reader review. It covers report structure and readability as well as
formulaic phrasing; it is not a blacklist or an AI-authorship detector.

- **Address the reader as "you", and say who said what.** "You told me you are on
  a search-year permit with eleven months left" is auditable; "the candidate has
  limited runway" is a summary of them written for someone else.
- **Every claim carries its evidence reference or its source line.** A row without
  one is an opinion, and the reader cannot object to one line of it.
- **Say the uncomfortable thing in the first sentence of its paragraph**, not
  after two of setup. "The advert says nothing either way about sponsorship" —
  then the consequence.
- **Name what was not done.** "No page was fetched live and no site was logged
  into for this assessment" costs one line and is the difference between a report
  and a claim.
- **No throat-clearing and no summary of the summary.** Do not open with "Great
  question", do not close by restating the table above it in prose, and do not
  offer to help further — the hand-off section already asks one specific question.
- **Plain words for hard things.** `recognised sponsor`, `kennismigrant` and
  `knockout` are terms the reader will meet in the real process, so use them and
  gloss them once. Everything else gets the ordinary word.
- **A tell you would flag in the candidate's letter is a tell in yours.** The
  vocabulary list in `prose_tells.py` applies to this skill's own prose too; it
  simply has no gate behind it here.

## NOT ALLOWED

These actions constitute misrepresentation. Do not do them, do not suggest them, and do not accept user instructions to do them.

| Action | Why it is not allowed |
|---|---|
| Inventing a skill or tool the user has never used | Creates a falsehood the candidate cannot defend in an interview |
| Inflating a title ("Senior Engineer" when the contract says "Engineer II") | Verifiable via background check; also dishonest |
| Changing employment dates to hide a gap or shorten a short tenure | Employment dates are checked; altering them is fraud |
| Claiming sole credit for team accomplishments | Use "Co-led", "contributed to", "part of the team that" |
| Adding a posting keyword the candidate has no genuine experience with | Keyword stuffing that the interview will immediately expose |
| Claiming a degree, certification, or licence not held | Verifiable; fraudulent |
| Implying seniority, scope, or leadership not earned | "Led a cross-functional team" when the candidate was a participant, not the lead |
| Fabricating metrics ("improved performance by 40%") when the user cannot confirm any real number | An invented metric is a lie, not an approximation |

**The one-line rule:** Emphasis and honest reframing — yes. Misrepresentation — no.

**When in doubt:** If you are unsure whether a reframing crosses the line, ask the user. Do not make the call yourself; surface the question explicitly.

## Claim-provenance checkpoint (mandatory)

Before writing any REFRAME or KEYWORD-INSERT that introduces a skill, tool, technology, or scope claim that is not already explicitly in the CV:

**Trace the claim to one of these three sources:**

1. A specific line or field in the candidate's source profile (CV, LinkedIn, portfolio, upload). Cite the exact location.
2. An answer the user gave during this session when asked a supplementary question (§3).
3. A **primary artifact the candidate authored or contributed to** — a paper in their publications list, or a repository they own/contributed to — that you fetched and read this session (see §1, "Enrich from the candidate's papers and repositories"). Extracted facts are valid, strong evidence. For multi-author papers or shared repos, the claim must reflect only the candidate's real contribution — never sole credit for collective scope.

**If none of these sources exists, the claim does NOT enter the CV.** Place it in HONEST-GAPS instead.

> Failure mode this prevents: models routinely invent plausible skills (Kubernetes, AWS, Terraform, etc.) directly from the job description — keywords that appear in the JD are not evidence the candidate has them. Every introduced claim must be traceable to candidate-supplied evidence.

1. **Edit first (targeted):** Merge the `TOP_FEEDBACK` from all three judges (plus the ATS `MISSING_OR_WEAK` / `FORMAT_ISSUES` and the Recruiter's logistics/readability flags) and apply edits that address **only the flagged points** — do not re-tailor sections the judges didn't fault. Apply to `<workspace>/tailored-profile.yaml` (and `<workspace>/letter.yaml` if present). Ask the user any `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE` from the Recruiter or Hiring Manager — honestly, never inviting fabrication. **A keyword the ATS screener flags as missing goes into the CV ONLY if the candidate genuinely has it** (the claim-provenance checkpoint still applies); otherwise it stays in HONEST-GAPS. **Re-run the claim-provenance checkpoint on every edit made this round before re-rendering** — any term added to satisfy an ATS REJECT must cite its source (a profile line or a user answer this session). The correct response to an ATS gap you cannot honestly close is to let the loop fail at round 3 and report it — *never* to insert an ungrounded keyword. A coverage gate failing because the candidate genuinely lacks must-haves is a true result, not a problem to engineer around.

## Equivalence test

**Equivalence test — claim true equivalences at full strength (don't under-sell).** Honest ≠ timid. Before hedging an adjacency into "familiar with…", ask: is the candidate's real experience *functionally equivalent* to the requirement, just named differently? — e.g. "REST API design" vs. "building HTTP services"; "Postgres" vs. "relational databases"; one major cloud vs. another for a cloud-agnostic skill; "deep learning" vs. "neural networks". **If yes, claim it at full strength using the posting's term** — that is honest reframing, not a stretch. Reserve hedged "familiar with…" language for genuine *partials* (a real gap in depth/recency/exact-match). Weakening a true equivalence into a `partial` costs the interview with no honesty benefit — it is its own failure mode.

## Hard disqualifiers are a wall

If the failed requirement is a `[disqualifier]` (work authorization/visa, a legally required licence or clearance, a hard on-site/location requirement, language fluency, a regulated experience floor — see `job-posting-extraction.md`), it is **not** a HONEST-GAP to mitigate with framing. No reframing closes a legal barrier. Instead: **tell the user plainly and let them decide** — "This role requires X, which you don't currently meet; applying anyway is your call, but be aware it's likely an automatic screen-out." Never spend a cover-letter "mitigation" pretending a hard barrier is a soft framing problem. (A disqualifier the candidate *does* meet just needs to be made visible — e.g. a one-line work-authorization note — which the recruiter judge will otherwise flag.)

Some must-haves are **non-negotiable barriers** the candidate cannot close by tailoring or learning: **work authorization / visa** for the country, a **legally required license or security clearance**, a **hard on-site/location** requirement, **language fluency**, or a **regulated experience floor**. Tag these `[disqualifier]` (distinct from an ordinary must-have like "Kubernetes", which is recoverable).

Surface `[disqualifier]` items **first** in the §4 confirmation and ask the user directly: *"These look non-negotiable — do you meet them? If not, this may not be worth a full application."* This protects the user's time on day one (the recruiter judge would otherwise only catch a logistics wall after a whole package is built), and it keeps a genuine legal barrier from being mis-handled downstream as a soft "framing" gap (see `gap-analysis.md §3`).

## Quantification ladder

If a bullet says "improved system performance" and the user can supply the actual numbers, update the bullet. When exact numbers are unavailable, use this fallback ladder in order — stop at the most specific level the user can honestly confirm:

| Level | Form | Example |
|---|---|---|
| 1 — Exact number | `X%`, `$X`, `Xms` | "Reduced latency by 38%" |
| 2 — Honest range | "X–Y%" | "Cut processing time by 20–30%" |
| 3 — Scope / scale | "~N users", "Xk records" | "Serving ~200k monthly users" |
| 4 — Before → after | qualitative direction | "Reduced review cycle from days to hours" |
| 5 — Team / org size as proxy | headcount or org scale | "Across a 40-person engineering org" |

Never invent a precise figure. Level 5 is a last resort — a vague but honest scale claim is better than silence, but only barely. Push back up the ladder if the user can recall more.

> ✓ Allowed: honest quantification is better than vague language, and honest approximation is better than silence.

**Not every role is quantified in numbers — match the evidence to the profession.** This ladder is built for measurable-output work (engineering, sales, ops, growth) where a percentage or a dollar figure is the natural currency. Much of the labour market is not like that, and forcing a metric onto it reads as inauthentic or tips into fabrication. For **care (nursing, social work), education, creative/design, legal, public-sector, hospitality, and skilled trades**, the strongest *honest* evidence is usually qualitative and concrete rather than a number: scope and responsibility ("ran a 32-bed ward's night shift solo"), caseload/volume ("managed a 60-client caseload"), outcomes and recognition ("led the unit to its first 'Outstanding' CQC rating"), named results ("won the Henderson appeal"), credentials, inspection/audit ratings, repeat clients, or a portfolio. A specific qualitative statement beats a bolted-on percentage — do **not** manufacture a soft metric ("improved morale by 30%") to satisfy a numbers reflex; that violates the NOT-ALLOWED rules below. Use the number when it's real and natural to the role; otherwise reach for concrete scope, outcome, or credential.

**Recency matters.** A must-have evidenced only by **stale** experience — used heavily 5+ years ago with nothing since (e.g. "Python 2012–2017, nothing after") — is `partial`, not `strong`: it satisfies the keyword but reads as rusty to a human. Flag it, and if the candidate has any recent touch (a side project, a course, a current-role mention), surface that to restore currency. Do not invent recent use.

## Prioritization under the length limit (LEAD-WITH)

Coverage is necessary, not sufficient — **placement is the other half.** A CV that covers every keyword but buries its best evidence on page two loses the 6–10-second skim to a 70%-coverage CV that leads with its strongest, on-target work. After building AMPLIFY, rank its items by *signal to this role* (not by recency) and decide what lands in the scarce **top third of page one** — the summary plus the first role's first two bullets, which *is* the screen. State explicitly:

- **Summary opening line** — the single most role-relevant identity + the candidate's real standout signal (their marquee employer/lab, rare relevant skill, shipped-at-scale product, or top-venue publication). This is the first thing read; make it specific, not boilerplate.
- **First bullet of the most recent relevant role** — the strongest quantified, on-target achievement.
- **What gets cut or compressed** to make room (per `cv-craft.md §5`): off-target bullets, stale roles, generic skills. Name the cuts; do not silently keep everything and let the page overflow.

This is honest-only: prioritization reorders and trims *real* content — it never invents a standout signal the candidate lacks. If the Hiring Manager review later reports a buried `STANDOUT_SIGNAL`, surfacing it here is the fix.

## Post-tailoring AI-uniformity check

After completing all REFRAME and KEYWORD-INSERT edits, review the **full CV** for mechanical uniformity before presenting it to the user:

1. **Verb variety:** Are the same stock verbs ("spearheaded", "leveraged", "drove", "utilized") repeated across multiple bullets or roles? Replace repetitive openers with alternatives from the action-verb bank in `cv-craft.md §3`.
2. **Sentence structure variety:** Do bullets follow an identical grammatical template (verb → noun phrase → result → percentage)? Vary the structure — some bullets can lead with the outcome, some with the scope, some with the action.
3. **Voice and specificity:** Does the CV read as one person's work history, or as a generic template filled in with different nouns? Each role should have at least one detail that is unmistakably that candidate's experience.
4. **Prose quality:** Flawless-but-voiceless prose signals AI generation to experienced recruiters. Preserve natural sentence rhythms even when the grammar is corrected.
5. **The 2026 vocabulary:** `spearheaded`, `pivotal`, `intricate`, `showcasing`, `delve`, `realm`, `robust`, `cutting-edge`, `seamless`, "a valuable asset". `lint_cv.py` reports these as `AI_VOCABULARY` over the whole document, and `check_letter.py` adds the structural tells on a letter (`EM_DASH_DENSITY`, `NOT_JUST_PIVOT`, `TRICOLON_DENSITY`).

If the uniformity check fails on any dimension, make targeted repairs before delivering the final CV.

The lint is the floor, not the check. It sees the word `pivotal`; it cannot see that three roles were written to the same template. A clean `lint_cv` run is not evidence the CV reads as a person's — dimensions 1–4 above are the part no gate measures, and `references/gap-analysis.md` carries them in full.

## FIT SNAPSHOT — show before tailoring (baseline) and after (delta)

A lone coverage count misleads: a CV can cover most must-haves while the candidate is under-leveled or off-domain (both kill the application), or miss several and still be a strong apply on a perfect responsibility + seniority match. So show the user a small **fit snapshot** — still no fake precision, every line evidence-backed:

```
FIT SNAPSHOT — [Role Title] at [Company]

Must-have coverage:  X of N strongly evidenced (Y partial, Z missing)

| Must-have requirement | In CV? | Evidence |
|---|---|---|
| [Requirement 1] | Yes / Partial / No | CV-nnn |
| … | … | … |

Responsibility match: M of K core responsibilities demonstrated (from the §1 responsibility-evidence pass)
Seniority fit:        step_up / lateral / step_down / unclear — [one line]
Domain fit:           same-domain / adjacent / cross-over — [one line]

APPLY VERDICT: strong_apply / worth_applying / stretch / likely_screen_out / blocked — [one honest sentence why]
```

Run it before tailoring (baseline) and after (so the user sees the delta). The apply verdict is the north-star question — it tells the user whether this is worth their time, not just whether the words matched.

**This snapshot and the advice block below are the same judgement in two places, so they must not disagree.** The snapshot is apply mode's before/after view; the advice block is the shape every mode uses to state fit. Both carry the same five verdicts from `scripts/vocab.py` — `blocked` included, because a legal barrier is not a weak `likely_screen_out` — and `insufficient_evidence` replaces the whole thing rather than appearing as a sixth level. Both carry the required disclaimer verbatim.

**REQUIRED disclaimer to include every time:**

> ⚠️ This is a count of evidence, not a forecast of the outcome. Every must-have is
> printed with the evidence reference behind it, so the denominator can be audited row
> by row and you can object to one line rather than to the whole number. `strongly
> evidenced` counts `strong` only — `partial` and `gap` are never merged into a covered
> number, because merging them needs a weight for a partial match and any weight would
> be invented. This is not a prediction about a screening system: keyword stuffing
> (adding terms not backed by real experience) backfires at interview and with
> sophisticated ATS, and no count here estimates an interview or hiring outcome.
> Whether to apply is your call.

**Computation & labels (avoid two conflicting numbers):** the **"strongly evidenced" count** = must-haves where CV evidence is `strong` (count `partial` and `missing` separately; do not merge them into one "covered" number). **Evidence that is only `dated` counts as `partial`, never `strong`** — stale experience satisfies the keyword and reads as rusty to a human (`gap-analysis.md`, "Recency matters"). That clause is not decoration: `count_coverage.py` applies the same downgrade mechanically, and a snapshot that counts a stale-but-strong must-have as evidenced disagrees with it on the same rows. **When a `fit-assessment.yaml` exists, run `count_coverage.py` and use its numbers rather than counting again by hand** — two paths are tolerable only while they give one answer. This is *not* the same as the ATS screener's coverage formula (which gives partials half-weight: `(present + 0.5·partial)/total`) — label them distinctly ("evidenced must-haves" here vs. "ATS coverage %" from Judge 1) so the user never sees two unreconciled percentages. Be honest about `partial`: a keyword in the Skills list with no supporting bullet is partial, not strong.

## Personal-data safety interlock (apply before rendering — this is a hard rule, not a style preference)

The conventions above are not symmetric in *risk*. Adding a photo/DOB in the EU is a neutral style choice; adding one to a **US/Canada/UK/Ireland/Australia/NZ** application is a genuine problem — many employers there route such CVs straight to rejection because considering that data exposes them to discrimination-law liability. Because a returning user's master profile may have been built for an EU/Asia target (and may legitimately carry a photo, DOB, nationality, or marital status), you must not let those fields bleed into a Cluster-1 application.

So, when `meta.target_market` is a **Cluster-1** country (US, CA, UK, IE, AU, NZ) **or** the conservative default: **strip photo, date of birth, age, marital status, and nationality from the tailored profile even if they are present in the master**, and tell the user you did and why ("US employers can't consider these — including them only hurts you"). Never *add* them for a Cluster-1 target. The one deliberate exception is a Japanese *rirekisho* (`references/rirekisho.md`), which is a different document type with its own form — its photo/DOB belong only on that form and must **never** be reused for any non-Japan target. When in genuine doubt about a market, follow the conservative default and omit them.

**Where personal data and a photo live (for markets that expect them).** When the target market *does* expect them — much of continental Europe (DE, FR, traditional NL/IT/ES sectors) and East Asia (China, Korea, Japan-Western-CV) — put them in `contact.personal` (a dict, e.g. `{date_of_birth: "1992-05-01", nationality: "...", hometown: "...", marital_status: "..."}`) and set `meta.photo` to an image path. The renderer shows the personal block in the header and a passport-style photo above the name (LaTeX/PDF and .docx; Markdown embeds the path). **The renderer enforces the interlock as defense-in-depth**: for a Cluster-1 `meta.target_market` it ignores `contact.personal` and `meta.photo` entirely, so a mis-tailored profile physically cannot leak protected data onto a US/UK CV. Collect these fields honestly from the user — never invent a DOB, nationality, or photo.

## Posting-fetch integrity

Garbage in, garbage out: extracting from a page that isn't actually the posting produces fabricated requirements that then drive the whole application. So validate the source first.

- **A `200 OK` is not proof you have the posting.** LinkedIn, Workday, Greenhouse, Indeed, and most portals return a success status for a **login wall, cookie/consent banner, bot check, or search page**. If the fetched text has no responsibilities and no requirements, is dominated by "sign in" / "create account" / cookie text, or is suspiciously short, you did **not** get the posting.
- **When the fetch is thin or wrong, do not extract — ask the user to paste the full posting text.** Inventing must-haves off a login wall is worse than asking.
- **Terminal case:** if the posting genuinely can't be obtained (dead link, nothing to paste), stop and say so. Never proceed on guessed requirements.

If the user already provided complete posting text, validate that text and proceed
to extraction. Otherwise follow this retrieval order.

**Step 1 — Try to fetch the URL.**

Use `WebFetch` on the provided URL. Examine the returned text:
- Does it identify the specific role and employer and contain substantive duties and requirements?
- Is the description complete rather than a search card, truncated excerpt or access wall?

If yes, proceed to extraction.

**Step 2 — Detect a blocked or unusable page.**

The following platforms frequently return login walls, empty shells, or JavaScript-rendered content that is not usable as text:
- LinkedIn job postings (most return a login prompt or a thin snippet)
- Workday embeds (e.g. `company.wd5.myworkdayjobs.com`) — often return near-empty HTML
- Greenhouse iframes loaded inside a company's own site
- Lever postings embedded in iframes
- Taleo and iCIMS portals

Word count is a warning signal, not a minimum: concise postings and languages
without spaces can still carry complete requirements. A sign-in link beside a
readable description is not a login wall. If the description is actually missing
or truncated, **do not guess**. Use an available reader under
`references/network-recovery.md`, or ask for the full text when access requires
the user's participation.

**Step 3 — Ask the user to paste the full text.**

Say exactly this (adjust as needed):

> The job posting at [URL] is behind a login wall / returned too little text to extract reliably. Please paste the full posting text here and I'll extract the structured schema from it.

Wait for the pasted text. Then extract.

## Extraction field table

| Field | Type | How to populate |
|---|---|---|
| `role_title` | string | The exact title as written in the posting (e.g. "Senior Data Engineer", "Machine Learning Engineer II"). |
| `company` | string | The exact public employer name as the posting writes it. `check_letter.py` verifies the letter's recipient against it, and the application workspace directory is named from it. |
| `seniority` | enum: `intern / junior / mid / senior / lead` | Infer from title words, years-of-experience stated, and scope of responsibilities. See §2 for implicit seniority signals. |
| `location` | string | The posting's own location text, verbatim and as one string (e.g. "Amsterdam, hybrid", "Remote — EU"). NOT a `{city, country, arrangement}` mapping: no script reads a structured location, and the two shapes travelling between modes is what let assess and apply write mutually incompatible `posting.yaml` files for the same posting. |
| `must_haves[]` | list of strings | Hard requirements the posting marks as required, essential, must-have, or minimum. Include degrees/certs if stated as required (not just "preferred"). See §2 for phrasing heuristics. |
| `nice_to_haves[]` | list of strings | Skills/experience the posting marks as preferred, bonus, a plus, nice to have, or "we'd love". Include items in a separate "Preferred Qualifications" section. |
| `responsibilities[]` | list of strings | Day-to-day duties — what the person will actually do. Drawn from "What you'll do" / "Responsibilities" / "Day in the life" sections. Use the posting's own phrasing. |
| `keywords[]` | list of strings | **Exact ATS terms** to mirror in the CV and cover letter: tool names, language names, frameworks, methodologies, certifications, domain-specific jargon. Extract casing exactly (e.g. "PyTorch", "CI/CD", "REST APIs", "Agile/Scrum"). |
| `company_values_tone` | string | Culture signals + voice. Note: formal vs. casual writing style, mission language ("we believe", "our north star"), DEI statements, pace signals ("fast-moving", "startup within a larger company"), team descriptors ("collaborative", "autonomous"). This shapes the cover letter's register. |
| `red_flags` | list of strings | Signals of a problematic role. See the full list of red-flag patterns in §2. |
| `salary_range` | string or null | The stated pay range, if the posting gives one (e.g. "€65k–80k"); else `null`. Many EU/US postings now state a range. |
| `application_type` | enum: `cv / structured` | `structured` when the employer asks for a supporting statement, criterion-by-criterion evidence, a competency response or a structured application form. Essential / Desirable headings or a framework name alone do not establish that requirement. Otherwise `cv`; preserve any explicitly requested CV alongside structured materials. Follow `references/structured-applications.md`. |

**The `posting.yaml` field list, and it is exactly these twelve names in this order:**

```
role_title, company, seniority, location, must_haves, nice_to_haves,
responsibilities, keywords, company_values_tone, red_flags, salary_range,
application_type
```

`company` is the exact public employer name — `check_letter.py` hard-fails with `NO_COMPANY_IN_POSTING` without it, so a posting extracted without it breaks every downstream apply run. `location` is a **scalar string**, the posting's own location text, not a `{city, country, arrangement}` mapping. There is no `language` field: the CV's language follows the market and lives in `meta.language` on the profile. The old `SKILL.md:71` table silently dropped `salary_range` and `application_type`, and `application_type: structured` is the only signal routing to the supporting-statement branch — that condensation defect already shipped once.

## Structured applications

The CV judges (ATS / Recruiter / Hiring Manager) are calibrated to a free CV and an ATS pipeline — they don't model a criterion-scored form. So for a structured application, review the **supporting statement** against the framework instead: **every Essential criterion has a clearly-labelled, evidenced STAR paragraph; each statement is within any stated word limit; no criterion is unaddressed; claims are provenance-checked; unmet Essentials are surfaced honestly.** Report that criterion-coverage to the user (e.g. "8/8 Essential, 3/5 Desirable evidenced") in place of an ATS coverage %. If a CV is also required, run the normal judge loop on the CV as a secondary check.

## Localized salutations

**`salutation`** — Follows `recipient.name`:

| Situation | Salutation |
|---|---|
| Named contact (person's name confirmed) | `Dear [First name] [Last name],` or `Dear [First name],` (use first name if the company tone is casual; full name if formal) |
| Name only guessed / inferred (uncertain) | Use `Dear Hiring Team,` — a generic but professional salutation is not penalised; a wrong name is worse than a generic one |
| Team/department, no named contact | `Dear [Team Name] Hiring Team,` or `Dear Hiring Team,` |
| Academic / highly formal context | `Dear Dr. [Last name],` |
| Do not use | `To Whom It May Concern,` — outdated; `Dear Sir/Madam,` — outdated and gendered; never fabricate a name |

**Localized salutations (non-English letters):** when the letter is written in the market's local language, use that language's standard salutation — not a literal translation of "Dear". For an unnamed recipient: German `Sehr geehrte Damen und Herren,`; French/Belgian `Madame, Monsieur,`; Spanish `Estimados señores:`; Italian `Gentile Responsabile delle Assunzioni,`; Dutch `Geachte heer/mevrouw,`. For a named recipient, use the formal gendered form (e.g. German `Sehr geehrte Frau [Last],` / `Sehr geehrter Herr [Last],`). Match the salutation's language to the letter's language; never mix.

## Letter body constraints

| **Word count** | 250–350 words optimal for the body (the `body` paragraphs in `letter.yaml`). **400 words is the hard ceiling** — do not cut genuine value just to hit 350, but nothing beyond 400. Stays comfortably on one page when rendered. |

**`body`** — A YAML list. Each element is one paragraph as a single string. No Markdown formatting inside the strings (no `**bold**`, no bullet points) — render_letter.py outputs plain text per paragraph. Keep each paragraph to 4–7 sentences maximum.

**`closing`** — Choose from: `"Sincerely,"` (universal, formal), `"Kind regards,"` (warm professional), `"Best regards,"` (slightly more casual). Match the register. The sender's name is appended automatically by render_letter.py.

## Rirekisho honesty

The rirekisho asks for **personal data** a Western CV omits — date of birth, age, sometimes gender, address, and a photo. These are **provided by the candidate, never invented or inferred.** Ask the user for them; do not guess a birth date, fabricate an address, or assume a gender.

- **Gender (性別):** modern Japanese practice increasingly **omits** gender (the 2021 JIS-style template dropped the field). Include it only if the user chooses to. Default: omit unless asked.
- **Photo:** a 36–40mm × 24–30mm headshot. If the user supplies an image path (`jp.photo_path`), it is embedded; otherwise the form shows a labelled placeholder box.
- **学歴・職歴 dates and entries** are derived from the candidate's real `education`/`experience` — same honest-reframing rules as the Western CV.

`age` is conventionally written as 満○歳. The skill (which knows today's date) computes it from `date_of_birth`; the renderer only prints what it is given (it does not compute dates).

## The review loop

**Dispatch all three in parallel** — as fresh independent **Agent** subagents in a **single message (three tool calls at once)** each round, so they run concurrently. They share no state, so parallel dispatch is both faster and avoids ordering bias; never run one, read its verdict, then run the next. Each has **no other context**, so paste everything it needs:

**The mechanism is replaceable; the isolation is not.** On a host with no subagent tool, dispatch concurrent fresh invocations of that host's own CLI (for example, `codex exec`) using `agents/*.md`. A judge that watched the tailoring is not a second opinion. If no fresh context is available, preserve the draft and report that independent review is incomplete. Self-review may find obvious defects, but it cannot produce judge verdicts, review receipts or a claimed review PASS. Resume with isolated judges when available. See `references/portability.md`.

- *ATS Screener:* the **full text** of `agents/ats-screener.md` + the structured posting + the tailored CV Markdown (`<workspace>/cv.md`) + the **CV language**. (No letter — ATS doesn't parse letters.)
- *Recruiter / HR Screener:* the **full text** of `agents/recruiter-screener.md` + the structured posting (`<workspace>/posting.yaml`) + the tailored CV Markdown (`<workspace>/cv.md`) + the motivation letter (`<workspace>/letter.md`) if produced, else `No letter provided.` + the **target market & CV language**.
- *Hiring Manager:* the **full text** of `agents/hiring-manager.md` + the structured posting + the tailored CV Markdown (`<workspace>/cv.md`) + the motivation letter if produced, else `No letter provided.` + the **target market & CV language** (e.g. "Germany / German") so it calibrates conventions and reads the CV in the right language.

**Parsing each verdict (apply exactly, to all three):**

1. In each judge's response, find the last line beginning with `VERDICT:` followed by `PASS` or `REJECT` (case-insensitive). If absent or ambiguous (anything other than exactly `PASS`/`REJECT`), treat that judge as `REJECT` and re-dispatch it.
2. ATS Screener: also read `COVERAGE`, `NON_KEYWORD_REQUIREMENTS`, `MISSING_OR_WEAK`, and `FORMAT_ISSUES`. Verify every original must-have is either keyword-scoped or explicitly retained for human/by-start review. A high keyword count does not clear an unresolved qualification, and an absent values slogan is not a reason to add ungrounded self-praise.
3. Recruiter / HR Screener: also read `SCORES`, `SCREEN_NOTE`, `TOP_FEEDBACK`, and `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE`. The recruiter's questions are often **logistics** (work authorization, relocation) — surface them to the user.
4. Hiring Manager: also read `SCORES`, `LEVELING`, `STANDOUT_SIGNAL`, `TOP_FEEDBACK`, and `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE` (a single `  - none` bullet means no questions). `LEVELING` and `STANDOUT_SIGNAL` are advisory — they do not change the verdict, but relay them to the user and act on them when tailoring (e.g. lead the summary with a buried standout signal; address an under-leveled read).

**Combined verdict: PASS only if ALL THREE judges return `PASS`.** If any is `REJECT`, the round is a `REJECT`.

**If `REJECT` — per-round sequence (order is mandatory):**

1. **Edit first (targeted):** Merge the `TOP_FEEDBACK` from all three judges (plus the ATS `MISSING_OR_WEAK` / `FORMAT_ISSUES` and the Recruiter's logistics/readability flags) and apply edits that address **only the flagged points** — do not re-tailor sections the judges didn't fault. Apply to `<workspace>/tailored-profile.yaml` (and `<workspace>/letter.yaml` if present). Ask the user any `SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE` from the Recruiter or Hiring Manager — honestly, never inviting fabrication. **A keyword the ATS screener flags as missing goes into the CV ONLY if the candidate genuinely has it** (the claim-provenance checkpoint still applies); otherwise it stays in HONEST-GAPS. **Re-run the claim-provenance checkpoint on every edit made this round before re-rendering** — any term added to satisfy an ATS REJECT must cite its source (a profile line or a user answer this session). The correct response to an ATS gap you cannot honestly close is to let the loop fail at round 3 and report it — *never* to insert an ungrounded keyword. A coverage gate failing because the candidate genuinely lacks must-haves is a true result, not a problem to engineer around.
2. **Re-render second:** Re-render ONLY the affected outputs from the just-edited YAML (never re-send stale rendered files).
3. **Re-judge third:** Dispatch all three fresh judges with the newly rendered files. Never re-dispatch with the old rendered version.

## Judge lanes

**Three independent judges** must **all** return `PASS` before the package is interview-ready. They model the real hiring funnel — **ATS → Recruiter/HR → Hiring Manager** — and fail in *different* directions, so the CV must be **machine-findable, recruiter-skimmable & eligible, and genuinely strong** to clear all three:

The three lenses are deliberately distinct: ATS = literal findability, Recruiter = fast/broad/logistics, Hiring Manager = deep technical fit. Some overlap is expected; each owns its lane (the agent files state the boundaries).

1. `must_have_fit >= 3` (the candidate plausibly belongs in the pile — a real human would not bin this on sight). You are the *broad* filter: a deliberate, honestly-positioned stretch applicant (career-changer, re-entry, someone genuinely a notch junior) should clear *your* gate at a 3; it is the **Hiring Manager** who owns the strict `>= 4` deep cut. Reserve a `must_have_fit` of 1–2 for a CV that is genuinely off-target or missing the core of the role, not for one that is a legitimate stretch. Rejecting every stretch here would defeat the skill's whole purpose — those are the candidates it most exists to help.

- **Catch over-tailoring tells.** A Skills section that mirrors the posting's keyword list near-verbatim with no supporting evidence in any bullet is coverage-gaming, not strength — treat unsupported keyword density as an `evidence`/`credibility` concern and name the specific skills that appear with zero supporting context. The ATS screener (Judge 1) rewards literal keyword presence and structurally cannot catch stuffing; you are the only backstop.

## Honest-gap early stop

**Honest-gap early-stop (don't grind a loop you cannot win honestly).** After any round, diagnose *why* a judge still rejects before spending another round:
- If the **only** remaining cause is must-haves the candidate **genuinely lacks** — terms the claim-provenance checkpoint forbids you to add — then no honest edit can move that number. Looping again would only pressure you toward the one thing the skill forbids (inserting an ungrounded keyword). **Stop now**, even before round 3, and report it as an honest gap, not a failure of the package. This is the *expected* outcome for a genuine stretch application, and it is a true result — surface it, don't engineer around it.
- Keep iterating only while the rejects are about things you *can* honestly fix: ordering, emphasis, surfacing a buried real qualification, readability, missing logistics notes, a real keyword the candidate has but the CV omitted.

## Poorly built vs honest stretch

**Loop until ALL THREE pass, the honest-gap early-stop fires, or 3 rounds** (early-exit the instant all three pass — don't run extra rounds). If not all passed, **STOP** and report honestly — but **distinguish the two very different reasons a package can end un-passed**, because they mean opposite things for the user:
- **Poorly built** — a judge rejects over something fixable that tailoring should have caught (weak ordering, vague bullets, an unaddressed logistic, a real-but-hidden qualification). This is a tailoring miss to own and, budget permitting, fix.
- **Honest stretch** — the package is as strong as it can truthfully be, and the only thing keeping a `>= 4` deep-fit gate from passing is that the candidate is genuinely a notch off the role (the Step 3 apply verdict was "stretch"/"worth applying"). This is **not** a defective application: it is a well-built application for a reach role, and the user may well still submit it. Say so plainly — "this is a strong submission for a stretch; the gap is real and the honest framing is X" — rather than reporting a bare "failed review."

In both cases give the final per-judge verdicts, the ATS coverage % (or `n/a`), the remaining honest gaps, and concrete next steps (skills to gain, certifications, better-fitting roles). **Never fake a pass.**

## Immutability + workspace

Resolve the store with `scripts/paths.py` first. Paths below illustrate the default;
when `JOBHUNT_PROFILES_ROOT` is set, use `paths.PROFILES_ROOT` for profile and
resume lookups and report the actual saved paths. A missing store is normal on
first use; `save_profile.py` creates it when a profile is saved.

**Resume an in-progress application first.** Before anything else, check `~/.claude/job-profiles/*/applications/` for a workspace that matches this target (by company/role) and already contains a `posting.yaml` and/or `tailored-profile.yaml`. If one exists, a prior run was interrupted — show the user what's already there and offer to **resume from where it stopped** (e.g. posting already extracted → jump to gap analysis or tailoring) rather than rebuilding from Step 0. Only start fresh if they prefer it or no matching workspace exists.

**Check for existing profiles next.** Before building or parsing, check `~/.claude/job-profiles/` for any saved master profiles. If one or more exist, offer to reuse one (retargeting it for this new application) instead of rebuilding from scratch. A returning user can confirm a name and you jump straight to Step 2. New users with no saved profiles proceed to build/parse below.

**Reusing a master carries their experience forward, never their target.** `meta.target_market`, `meta.language` and any `contact.personal` in that file describe the application it was last built for. Re-ask the region and language (Step 0, question 2) before tailoring, and re-confirm any personal field the new market's cluster would treat differently — the master is the source of truth about the candidate, not about where they are applying.

**Offer to save the master** to `~/.claude/job-profiles/<name>/profile.yaml` so it's reusable across applications. This master profile is the source of truth and is **NEVER mutated by tailoring** — tailoring always works on a copy (Step 4).

**One candidate has one CV per language, and saving a new one never overwrites another language's.** A Chinese CV is a different document from an English one — different conventions, length rules and personal-data expectations — not a translation of it, so a user who supplies both has two masters: `profile.yaml` and `profile.<lang>.yaml` beside it. **Save through `python3 scripts/save_profile.py --name <name> --profile <file>`, never by writing the path yourself.** It resolves the slot by reading each existing master's own `meta.language` rather than trusting a filename, so a second English CV goes back into the legacy `profile.yaml` instead of becoming a duplicate; it backs up what it replaces; and it refuses a profile with no `meta.language`, because the unsuffixed slot is where a legacy English master usually lives and dropping an untagged CV there is the overwrite this is here to prevent. On the read side the same rule runs backwards: tailor from the master whose language matches the CV language chosen in Step 0, and say which file you took as the base. Reaching for the English master to build a Chinese CV throws away the one the user wrote for exactly that purpose.

**Application workspace.** All per-application files live under:

```
~/.claude/job-profiles/<name>/applications/<company>-<role>-<YYYY-MM-DD>/
```

This workspace contains: `tailored-profile.yaml`, `letter.yaml` (if any), `posting.yaml`, and the rendered outputs (`cv.md`, `cv.docx`, `cv.pdf`, `letter.*`). The master profile at `~/.claude/job-profiles/<name>/profile.yaml` is **NEVER** mutated.

- Write the tailored copy to `<workspace>/tailored-profile.yaml`. **Never edit the master.**

## Fast path

**Fast path (reduce friction for the common case).** When the user already hands you a parseable CV *and* a clear posting (URL or pasted text) and is not building from scratch, do not gate every step with its own round-trip. Do the work, then present the parsed profile, the extracted requirements, and the tailoring plan **together in one message**, and proceed unless the user objects or corrects something. Still run every step and the non-negotiable three-judge review loop — this only collapses the *confirmation* round-trips, never the analysis or the judges. Reserve the full step-by-step interview for when information is genuinely missing (building a CV from scratch, an unreachable posting, or ambiguous requirements).

## Enrich from the candidate's papers and repositories — fetch before you ask

When the profile names a **paper** (title, DOI, arXiv ID, venue) or links a **repository** (GitHub/GitLab project the candidate owns or contributed to), that artifact is primary evidence of the candidate's real work. **Fetch and read it to extract concrete, truthful detail — do not make the user retype what a tool can read.**

- **How:** use `WebFetch`/`WebSearch` for a paper (abstract, method, headline results, the candidate's listed authorship position); for a repo, fetch the README / project page (and `gh` CLI if available) for what it does, the tech stack, scale signals (stars, downloads, dataset size), and the candidate's specific contribution.
- **What to extract:** the kind of detail that makes a bullet specific and credible — what was built, the techniques/tools actually used, quantified results, and scope. This turns a thin line ("worked on a segmentation model") into an evidenced one ("lightweight SAM variant trained on a single GPU in ~1 day; published in MELBA") — all sourced from the candidate's own artifact, not invented.
- **Honesty (critical):** the artifact being in the candidate's profile is their assertion of authorship — extract only **their** real contribution. For a multi-author paper or a shared repo, attribute honestly (co-author, contributor) and never claim sole credit for collective scope. Pull facts about the work; do not borrow a co-author's part as the candidate's own.
- **Restricted access is the only reason to ask the user.** If the paper is paywalled, the repo is private, or the fetch is blocked, *then* ask the user for the specific facts you need (method, your contribution, the numbers) — phrased honestly, never as an invitation to embellish. Fetching first, asking second.

## Interview brief

For each **REFRAMED** or **AMPLIFIED** claim on the final CV, list:
- the **claim as written** on the CV,
- the **real source fact** it traces to (from the provenance checkpoint), and
- a one-line **"be ready to explain…"** prompt.

> Example
> - CV says: *"Built and maintained CI/CD pipelines, cutting deploy time 40%."*
>   Source: you wrote automated deployment scripts at Role B; the 40% is your confirmed number.
>   Be ready to: walk through what the scripts did end-to-end, which tool, and how you measured the 40%.

The point is not to coach a story — it's to make sure every word on the page is something the candidate can stand behind truthfully and specifically. If a candidate *can't* comfortably explain a claim, that's a signal the reframing went too far — soften it back.

- **Honest only.** This brief never invents a story; it points each CV claim back to a true source and prepares a truthful answer. If a claim has no defensible source, the fix is to change the CV, not to coach a cover story.
- **Keep it thin.** This is a defense brief generated from data you already hold — not a mock-interview module. A page or less.
- **Flag the over-reach signal.** If preparing the brief surfaces a claim the candidate cannot truthfully defend, treat it as a tailoring error and walk the claim back on the CV.

## Before the first mode on a new machine

```bash
python3 scripts/doctor.py            # what works, what does not, what each costs
python3 scripts/doctor.py --install  # installs the missing PYTHON packages only
```

Before running it, read [references/agent-setup.md](references/agent-setup.md) and
prepare a usable Python environment if needed. The agent runs it once for a new
user and resolves required missing capabilities. It reports capabilities rather than binary names —
the PDF check renders a PDF, because looking for `xelatex` alone once called this
machine broken while `tectonic` was installed and every PDF rendered fine.

**The cheap half of it runs on its own, every mode entry.** `enter_mode.py` calls
`doctor.fast_capabilities()` — imports and `which`, no rendering, milliseconds —
records the result in the `mode_entry` line and prints
`NOTICE_MISSING_CAPABILITIES` on stderr when something is absent. That exists
because this script spent its first week named here and in none of the four mode
files, so no run ever invoked it: a new user learned their machine could not
render a PDF when a PDF failed to appear. A capability that does not enter the
scaffolding is a capability nobody uses.

The fast check is sound about what is MISSING and silent about what works — no
pandoc on PATH means no template-based CV PDF; bundled report PDFs still work.
Pandoc plus an engine can both be
present and still fail. Confirming a capability stays with `doctor.py`, which
renders one. A warning may only fire when it is sure, or it becomes the line
everyone filters out.

Nothing here blocks a run: a machine with no LaTeX engine still produces Markdown
and .docx, and one with no `opencli` can still do assess, apply and interview from
a pasted posting. What the report buys is saying WHICH capability is missing
before the user hits it, instead of discovering it when a PDF does not appear.

**The agent owns first-run setup.** Follow [references/agent-setup.md](references/agent-setup.md)
when a required capability is missing: install the necessary dependencies,
run `scripts/setup_dependencies.py` (add `--discovery` for Node/OpenCLI),
use the bundled AnySearch client and CDP reader, and verify daily-browser
CDP access. Never use browser extensions. Browser connection consent,
site login and human verification still require the user's action. Reuse working tools and continue the
original task after setup. `doctor.py --install` covers Python packages only;
use `scripts/run_tool.py` to invoke the prepared runtime. No additional skill is required.

## Mode entry

On entering a mode, run:

```bash
python3 scripts/enter_mode.py --workspace <ws> --mode <mode> \
    --because "<why this mode, in one line, from what the user asked>"
```

then read `modes/<mode>.md` in full. The entry writes the mode file's content hash to
`journal.jsonl`; `check_apply.py` fails if it is absent or stale.

**Create `<ws>` yourself first** (`mkdir -p`). `enter_mode.py` refuses a workspace that
does not exist rather than creating one, for the same reason every gate refuses: one
mistyped `--workspace` would leave a directory holding a single `mode_entry` line, and
the "resume an in-progress application" lookup finds a workspace **by name** — so it
would offer to continue from an empty shell.

## The advice block, and the disclaimer that is not optional

Whenever this skill states how good a fit a posting is, it states it in exactly this
shape — counted facts, then one word, then the disclaimer. **The block follows the
user's language, not the market's**, so both shapes are here; `scripts/count_coverage.py`
emits them with `--lang zh` and `--lang en` and is the only path that produces the counts.

    必备条件有充分证据：   X 项，共 N 项   （部分符合 P，存在缺口 G，无证据 U）
    核心职责已证实：     M 项，共 K 项
    职级匹配：           <上跳 | 平级 | 下沉 | 不明>
    可补缺口所需投入：   <当天 | 一晚 | 数日 | 补不上>
    投递建议：           <强烈建议投 | 值得投 | 可以冲刺 | 大概率被筛掉 | 硬性阻断>

    must-haves strongly evidenced:   X of N   (partial P, gap G, no evidence U)
    core responsibilities demonstrated: M of K
    level match:                     <step_up | lateral | step_down | unclear>
    effort to close the gaps:        <quick | evening | multi_day | not_closable>
    apply verdict:                   <strong_apply | worth_applying | stretch |
                                      likely_screen_out | blocked>

**Immediately under the block, ship the matching disclaimer unchanged.** Counts and
required report text support zh, en, ja, ko and es. Read
[report-localization.md](references/report-localization.md) for Japanese, Korean or
Spanish headings, disclaimers, notices and discover disclosure templates. The gate
checks the language's explicit anchor; a free paraphrase may still fail as `NO_DISCLAIMER`.

> ⚠️ 以上是对证据的清点，不是对结果的预判。每一项都连同它的证据引用一起印出，分母可以逐条审计；
> 本 skill 不给出面试或录用的可能性估计，也不给 0–100 分。要不要投，由你决定。

> ⚠️ This is a count of evidence, not a forecast of the outcome. Every item is printed
> with its evidence reference so the denominator can be audited row by row. This skill
> states no interview or hiring outcome estimate and no 0–100 score. Whether to apply
> is your call.

Every item inside N and K is printed with its evidence reference, so the denominator
is auditable. `强证据` counts only `strong`; `partial` and `gap` are never folded into
a "covered" number; evidence that is only `dated` counts as `partial`, never `strong`.
When the input cannot support a conclusion at all, the whole block is replaced by
`证据不足—不出结论` and the reason — that is a refusal, not a sixth level, and it is
never softened into `可以冲刺`.

## Words this skill does not put in its output

No percentages of fit. No self-invented scales (`7/10`, `B+`, "score: 82"). No
probability language at all: `概率`, `chance`, `odds`, `likely to be hired`,
`likely to be interviewed`, `strong candidate`, `would pass`. There is no data
behind any of them — "interview probability 45–65%" is a number someone made up,
and a weighted total is the same fabrication with arithmetic on top. The advice is
one word from the five, and the counts beside it are counts of evidence.

**The one exception, and its shape.** When the employer has published its own rubric
— a UK Civil Service Success Profiles level named in the advert, an NHS values
framework, a university person specification — this skill may walk the candidate
through **that** scale, in the employer's own wording, with the source named, framed
as "what the panel is asked to look at". Quoting the employer's scale is reporting.
Using it as a conclusion is fabrication. Never assert a score on it.

## The grounding contract

```
  Original source             Referenced claim              Check
  posting-source.txt --> JD-001…JD-080 --> requirement row --> check_evidence_refs.py
  cv.md / profile    --> CV-001…CV-080 --> requirement row --> resolves or is dropped

  profile.yaml field       --|
  answer in this session   --|--> claims.yaml --> each REFRAME / KEYWORD-INSERT
  candidate artifact read  --|                                |
                                                             v
                                                      check_claims.py

  Human-authored commit --> market-conventions/<key>.yaml
                                       |
                            allowlisted IDs; verbatim text
                            no model paraphrase
                                       v
                               check_conventions.py
```

1. **Evidence blocks tie the analysis to the source text.** The model may only cite
   blocks that exist; a reference that will not resolve is **dropped, not fatal**. An
   empty evidence list is not an error — rejecting it would punish the honest shape,
   and a *fabricated* reference lands in that same empty array and passes anyway.
   Carry the honest boundary into the skill's own output:
   **this is a floor on credibility, not a proof — it guarantees a claim points at
   something that really exists, not that the claim follows from it.**
2. **Claim provenance ties the output to source facts.** Three permitted sources,
   and there is no fourth. `claims.yaml` is the first thing that makes it a diffable
   artifact instead of a habit.
3. **Market tables tie down the one class of claim with no citable source.** In this
   whole skill exactly one kind of statement cannot be traced to text the user gave
   us: what this market screens for that the posting does not say. So it is written
   by a person, dated, with its source kind, whitelisted by id, and **rendered
   verbatim** — the model may not strengthen "usually" into "must", may not attach a
   number to it, and may not invent a row.

**Restate the fence next to the field that tempts the violation.** A rule at the top
of fifty instructions is not where the model is standing when it writes the dangerous
field. The no-fabrication rule is restated in exactly three places: the KEYWORD-INSERT
step, mock-interview question generation (a question premise the CV does not support is
a fabrication the candidate then repeats back), and the shortlist's `why_matched` field.

## Gates

| Gate | Script | Fires on |
|---|---|---|
| Personal data | `scripts/check_personal_data.py` | protected fields on a Cluster-1 target, or an unrecognised market. The renderer WITHHOLDS them for both — an unrecognised market is the conservative default, not a pass — and says so on stderr; markets are matched by ISO code, English name, endonym (`Nederland`, `España`, `한국`, `Việt Nam`) and CJK name |
| Rendering refusals | `scripts/render_cv.py` | right-to-left text (Arabic, Hebrew, Syriac, Thaana, N'Ko): the LaTeX template has no `bidi`, so a PDF would come out reversed and unshaped at exit 0. The PDF and the `.tex` are both refused as `UNSUPPORTED_SCRIPT` — a **tolerated** failure, so Markdown and .docx still ship and the exit code is unchanged. Paper is `letterpaper` for a US/CA target and `a4paper` otherwise; `meta.paper` overrides for the other Letter-using countries |
| Claim provenance | `scripts/check_claims.py` | a term with no source (skills, certifications, titles, orgs, degrees, institutions, project roles, publications, awards, volunteer, board); a status qualifier dropped off a real credential — in every language this skill writes CVs in, so `(in Bearbeitung)`, `(nog niet afgerond)`, `（修了見込み）`, `(재학중)` and `（在读）` count exactly as `(in progress)` and `B1` do; a mutated master profile |
| Verdict parsing | `scripts/parse_verdicts.py` | anything that is not exactly PASS/REJECT; a non-unanimous round |
| Render freshness | `scripts/check_render_freshness.py` | a judge that read a file the disk no longer has |
| CV lint | `scripts/lint_cv.py` | clichés, weak openers, over-long bullets, repeated verbs; the 2026 AI vocabulary from `scripts/prose_tells.py` (`AI_VOCABULARY`). The cliché and vocabulary scans run over the WHOLE document, not only the bullets — the summary is the line a recruiter reads first, and it used to be the one line nothing checked. Headings and the contact line are skipped, so an employer called "Robust Systems" is not reported as a cliché. A CV is exempt from the structural checks: a skills line reads "Python, C++, MATLAB" and would fire the tricolon check on every correct CV |
| Letter | `scripts/check_letter.py` | machine-prose tells over the whole body — the 2026 AI vocabulary (`AI_VOCABULARY`), em-dash density (`EM_DASH_DENSITY`), the "not just X, but Y" pivot (`NOT_JUST_PIVOT`) and tricolon density (`TRICOLON_DENSITY`), all from `scripts/prose_tells.py`, whose thresholds are calibrated against real letters including this skill's own; markdown in a body string, length, duplicated name, wrong company/role; a missing salutation or sign-off in a language this skill has no sourced default for (`NO_SALUTATION` / `NO_CLOSING`) — the renderer no longer prints an English one onto a non-English letter, so the gate is what stops it shipping with none. The 250–350 band is an ENGLISH word count, so a CJK-dominant letter is reported (`NOTICE_CJK_LENGTH_UNSCORED`, stderr) rather than scored — this skill has no sourced length convention for one, and the one-page constraint behind the band is measured directly by `check_pages` on the rendered PDF |
| Page count and PDF text | `scripts/check_pages.py` | a PDF longer than the market's table allows; a letter over one page; an unreadable PDF; a PDF whose text is missing `meta.name` or an `experience[].org`, or whose text cannot be read at all (`UNVERIFIED_PDF_TEXT` — not a pass); a start date in a calendar it cannot read (`START_DATE_UNREAD` — years of experience is then *unknown*, not zero, and the permissive budget is used rather than the strictest) |
| Template layout review | `scripts/check_layout.py` | missing/stale requirements, reference or final-file fingerprints; measured font, size, color, paper or margin mismatches; a PDF replaced after Word export; uninspected pages or unresolved differences. `--report` reviews the report separately and requires the current `report.md` prose, in order and as whole lines, in `report.pdf`, with table cells present (`REPORT_PDF_TEXT_MISMATCH`). Measurements supplement the eight actual visual comparisons; failures require repair and re-review. See `references/layout-review.md`. |
| Word limits | `scripts/check_word_limits.py` | a supporting-statement criterion over its stated limit, empty, or with no limit recorded; and the machine-prose tells from `scripts/prose_tells.py`, measured per criterion so the finding names which answer to rewrite. This is the artifact that is actually MARKED — the three CV judges are routed away from a structured application by design — and it had no reader for its prose at all |
| Apply completion | `scripts/check_apply.py` | a missing receipt; a receipt that does not match its own `receipt_hash`, i.e. hand-written or edited rather than produced by a gate (`RECEIPT_UNVERIFIED`); a gate that only ran its `--record` setup (`NOT_VERIFIED`); ANY gate left failing, named or not; an unclassified stop; a missing brief. `RECEIPT_UNVERIFIED` and `MODE_FILE_MISSING` are checked by every composer — apply, assess, discover and interview — not just this one |
| Mock interview | `scripts/check_mock.py` | an invented tag or band; a tag with no quote, or a quote that is not in the transcript; a pass emitting the other pass's tags; a scraped question with no id, no date, or the wrong country; an answer-bank entry with no source; a collapsed claim with no walk-back; an unsourced fact neither promoted nor walked back |
| Evidence blocks | `scripts/evidence_blocks.py` | the posting and CV cut into addressable `JD-nnn` / `CV-nnn`; the only chunker |
| Evidence refs | `scripts/check_evidence_refs.py` | refs that resolve to no block; block ids left in reader-facing prose |
| Prediction lint | `scripts/lint_no_prediction.py` | percentages (incl. fullwidth `％` and 「百分之七十」), `n/m` scores, scores worn as a NOUN rather than a symbol (`匹配度 85 分`, `overall score: 85`, `rated 8.5`, `4.5 stars`, `confidence: 0.85`, `grade: B+`, `Bewertung 8`, `점수 85점`), and prediction vocabulary in every language it writes in — EN + ZH (「成功率」「入围率」「七成」…) plus DE/NL/FR/ES/IT/JA/KO (`Chancen`, `kans`, `probabilité`, `可能性が高い`, `확률`) in the **judgement-facing** artifacts: `fit-assessment.md`, `shortlist.md`, `cheatsheet.md`, `mock/answer-guide.md`, `mock/assessment-*.md`. Numbers the round actually CAPTURED are exempt, but only from a file an `adapter_call` record names or an intact `browser_call` snapshot — a raw file nobody journaled is not a capture, it is a note the model wrote itself. Deliberately NOT the CV or letter — there a number is a measured past achievement, which the Quantification ladder above requires, not a claim about the future |
| Contradictions | `scripts/consistency.py` | verdict vs effort, loose knockouts, gaps with no action, work-authorization conflicts — reports, never repairs |
| Coverage counts | `scripts/count_coverage.py` | the only count-producing path **wherever a `fit-assessment.yaml` exists** — assess mode, and apply mode resumed from one. Apply mode without an assessment has no file for it to read and hand-counts its FIT SNAPSHOT instead; that is a second path, so it must apply the identical rule (below), and it is why the rule is written out in both places rather than trusted to memory. The card renders in **zh, en, ja, ko or es** using the same counts; pair it with the required text in [report-localization.md](references/report-localization.md). Other languages embed an English or Chinese card and required labels. Missing judgements, evidence and disclaimers remain failures in every supported language |
| Market tables | `scripts/check_conventions.py` | digits/percent in prose, source provenance, protected traits, duplicate ids, expired `review_by` (CI-hard) |
| Assess | `scripts/check_assessment.py` | composes the six above and requires their receipts; disclaimer, disqualifier section, the 「那该怎么办」 half, verbatim conventions, stale-review banner; a top-level `level_direction` or `effort` the card prints but nobody assessed, and a work-authorization token spelled outside its set |
| Migration losslessness (CI only) | `scripts/check_skill_lossless.py` | a baseline line that exists nowhere in this tree |
| Adapter classification | `scripts/check_opencli_result.py` | *(wrapper, not a gate)* a non-zero exit, a login wall, a platform stop-signal, or an empty identity field |
| First-run environment | `scripts/doctor.py` | *(precondition, not a gate)* every capability the skill needs, checked by USING it — the PDF check renders a PDF, because an earlier `command -v xelatex` check called a working machine broken while tectonic was installed. `--install` installs the Python packages; the agent prepares required tools and daily-browser CDP via `references/agent-setup.md` |
| Saving a master | `scripts/save_profile.py` | *(guarded write, not a gate)* one master per language; a new language never overwrites another, a repeat language is backed up first, and a profile with no `meta.language` is refused |
| Delivery | `scripts/deliver.py` | *(hand-off, not a gate)* requires a client `report.md` and verified report PDF; puts requested client documents together in `~/Downloads/<workspace-name>/` (or shared `--to` folder) and prints the path. Exits 0 or 2, never 1. `DELIVER_DEST_UNWRITABLE` is macOS TCC refusing `~/Downloads` mid-session — say so and offer `--to`, never leave the artifacts undelivered |
| Read-only | `scripts/check_no_write.py` | a journaled command whose published `access:` is `write`, or whose access cannot be resolved at all |
| Discovery profile snapshot | `scripts/snapshot_profile.py` | *(guarded helper, not a gate)* freezes `candidate-profile.yaml` for one search round and refuses to replace it with a changed master, so later CV edits cannot silently rewrite matching evidence |
| Candidate match | `scripts/check_candidate_match.py` | a high verdict or default recommendation that lacks a complete row-specific detail, a frozen-profile evidence pointer, a valid requirement mapping, or its localized reader-facing summary; a card promoted without detail; a core gap hidden by optional preferences; a stale ordering or more detail mappings than `brief.max_match_reviews` permits; `detail_unmapped` verifies a full read without counting as a CV mapping |
| Shortlist | `scripts/check_shortlist.py` | a row whose `source_id` or `raw_text` is in no raw capture, whose `id` is not `<site>-<source_id>`, or whose direct posting URL is empty, malformed, or not returned by its source; a candidate missing that clickable URL in `shortlist.md`; a duplicated or over-counted source report; "no results" with no adapter that exited 0; a missing disclosure block or the wrong provisional stamp for card-only versus detail-reviewed output; a detail fetch outside the top three; an uncapped brief, or a run that exceeded the caps the brief declares; a posting URL rendered in `shortlist.md` that is in no `shortlist.yaml` row; a row whose company or salary contradicts its own capture; a missing or stale mode entry. Warns (does not fail) when a row's location names a country outside `brief.markets` |

**No mode may claim success while `journal.jsonl` lacks a receipt for its gates.** A skipped script produces no output, and no output is exactly what a clean run looks like. `scripts/check_skill_lossless.py` is the one exception and is marked as such: it is a repo-level CI check with no workspace and no receipt, so requiring one would be requiring evidence that cannot exist.

<!-- BEGIN discover-inserts (plan 3) -->
## Discovery: the read-only surface

### OpenCLI-first fallback for discovery

Apply the fixed source-to-tool routes in [supplementary-sources.md](references/supplementary-sources.md):
WeChat (Sogou WeChat), Xiaohongshu, Douyin and Toutiao use OpenCLI. Do not
reconsider that tool choice. AnySearch search uses its HTTP API.

Begin every discovery round with OpenCLI's offline CDP routing and read-adapter
capability checks in `scripts/doctor.py`. Use OpenCLI only after its actual
website adapter is verified to use CDP. Never use browser extensions, even when
already installed or reported connected. A generic OpenCLI health result is not
proof of CDP routing. Only when the checks diagnose a missing CLI, disconnected
CDP connection, or unsupported CDP extraction, follow [the one-way browser
fallback](references/browser-fallback.md) with an available built-in CDP route.
If that fallback is unavailable too, disclose the gap; do not switch back to
OpenCLI for the same round. Keep browser evidence and gate receipts; a site
refusal is not a fallback reason and stops reads across both tools. Neither
backend submits applications.
Both OpenCLI and its fallback use the customer's daily browser unless they
explicitly request a separate one; follow [daily-browser routing](references/daily-browser.md).
Use [network recovery](references/network-recovery.md) for a generic
transport failure that has not yet established a fallback reason.


### opencli: the four command pairs this skill actually uses

| site | search | detail | login state (2026-08-09) | identity field |
|---|---|---|---|---|
| `51job` | `opencli 51job search "<kw>" --area <city> --page 1 --limit 20 --window background -f json` | `opencli 51job detail <jobId>` | no auth adapter | `title` |
| `indeed` | `opencli indeed search "<kw>" --location "<loc>" --fromage 7 --start 0 --limit 15 --window background -f json` | `opencli indeed job <id>` | no auth adapter | `title` — **measured EMPTY**, recover via detail. **US site only**, see below |
| `linkedin` | `opencli linkedin search "<kw>" --location "<loc>" --date-posted week --start 0 --limit 10 --window background -f json` | `opencli linkedin job-detail <job-url>` | logged in (cookie session) | `title` |
| `boss` | `opencli boss search "<kw>" --city <城市> --page 1 --limit 15 --window background -f json` | `opencli boss detail <security_id>` | logged in (cookie session) | `name`, **not** `title` |

**`indeed` serves the US site, and `--location` is resolved against a US
gazetteer.** A non-US place name does not fail — it silently returns US rows:
`--location "London"` came back with every row in Columbus, Ohio (London, OH is
25 miles away), exit 0, `classification: ok`, and `--location "Manchester, United
Kingdom"` returned California and New York (measured 2026-08-16; the adapter's own
`opencli indeed --help` describes it as "rendered DOM via browser session, US
site"). So for a `uk`/`nl`/`de` market this ADAPTER is the wrong tool — but that
is not a reason to stop at `linkedin` alone, which needs a login. Indeed's own
country site (`nl.indeed.com`, `de.indeed.com`, `uk.indeed.com`) is read through
the diagnosed browser route; the region table in `modes/discover.md` carries it,
along with the bot-block to expect there. If you use the adapter anyway, read
every returned `location` before it becomes a row. This is a third shape of risk-register row 2: not
found-nothing and not all-adapters-failed, but **adapter-succeeded-and-searched-
the-wrong-country**, where every receipt is green and the honest conclusion
("there are no London backend roles") is the wrong one. `check_shortlist.py`
answers only the row half of this, as the warning `WARN_ROW_OUTSIDE_BRIEF_MARKET`;
nothing can report the empty half, which is why it is written here instead.

Always `-f json`. Always `--window background`.
And **always branch on the exit code before you read stdout**:
a login wall gives exit 1, EMPTY stdout and a YAML error body on stderr even under
`-f json`, so `JSON.parse(stdout || '[]')` turns a 403 into a zero-result success.
Never run a command whose published `access:` is `write` —
`check_no_write.py` reads that field out of the tool itself.

### When a platform says stop, stop

A platform limit is any refusal the platform itself put up: a risk-control or
captcha body, a rate-limit, or a refusal on a site `opencli auth status` says you
are logged into. When one appears, stop automatic reads and offer the user a
recovery hand-off before ending the search. Follow
[the pause-and-resume workflow](references/user-recovery.md): explain the actual
login, verification or rate-limit obstacle and wait for explicit confirmation.
“Done, continue” after that prompt requests one new bounded round with the same
source/backend and a link to the old workspace; never erase the stopped journal.
While paused, preserve already retrieved rows and offer partial results. The
following rules govern the stopped round; use its degraded output when recovery
is declined/unavailable, not as a silent substitute for waiting:

1. **Stop that site for that round.**
2. Do not retry.
3. Do not change parameters and retry — a smaller `--limit`, a different city or a
   fresh `--window` is still a retry.
4. Do not route around it — no other adapter, no public mirror, no logged-in
   session standing in for a logged-out one.
5. Emit the **direction-level degraded output** instead: 3-5 target directions, no `rows:`,
   so it cannot claim a posting exists.
6. Fill in the disclosure table, whose answers ship pre-filled as localized "no" precisely
   so that concealing a retry has to be an active overwrite rather than an
   omission. Six lines, one language — `modes/discover.md` gives the block in both.

The per-platform trigger strings are data and live in
`references/risk-control-signals.yaml`; **this rule is not data and does not live
in a reference file**, because the moment it needs to be applied is the moment
nobody is going to go and look it up.

**READ `references/source-policy.md` before the first live retrieval of any run**
— before the first `opencli` adapter call — and again before agreeing to page
further, to fetch more detail pages, or to work while the user is away. It is the
ONE source standard: what is green, what is yellow-with-caps, and what is never
done whatever the user asks. Its two round caps are enforced rather than
suggested: `brief.yaml` must carry `max_rows_per_round` and `max_pages_per_site`,
and `check_shortlist.py` fails the run with `CAP_MISSING` or `CAP_ABOVE_CEILING`.

**READ `references/discovery-sources.md` when you are in discover mode and
about to call an adapter other than the four in the table above** (upwork,
nowcoder, maimai, or any site added later). It carries that
adapter's flags, its measured login state, its identity field and its detail
command — and `shortlist.yaml`'s `sources:` entry cannot be filled in without
them, so `check_shortlist.py` fails the run with `SOURCE_REPORT_MISSING` if you
skipped it.
<!-- END discover-inserts (plan 3) -->

## Mock interview — the anti-coaching line

### Rehearse retrieval, never rehearse content

A mock interview may help the candidate FIND, ORDER, and COMPRESS a true story they
already lived. It may not help them ACQUIRE one. The test is where the fact came from:

- If a detail traces to the profile, to the provenance map in `interview-brief.md`, or to
  something the candidate told you earlier in this session — helping them say it better is
  preparation.
- If a detail first appears in YOUR mouth — a number, a tool, a scope, a motive, a
  result — it is fabrication, however plausible, and it stays fabrication after the candidate
  agrees with it.

**Four hard rules.**

1. **Never write an answer for the candidate.** You may name what is missing ("your answer
   never said what changed as a result"). You may not supply the missing part. Naming a gap
   is feedback; filling it is ghostwriting a lie.

2. **A leading question is a fabrication vector.** "So you'd say you owned the migration?"
   hands the candidate an over-claim they will repeat in the real room and will not be able
   to defend. Ask "who owned the migration?" — open, and let the answer be whatever it is.
   This applies to your interview questions too: never build a question on a premise the CV
   does not support ("when you led that team of twelve").

3. **An undefendable claim is a CV bug, not a story to drill.** If the candidate cannot
   truthfully support a CV claim under ONE follow-up, that is a tailoring error. Log it to
   the walk-back list and change the CV. This is `references/interview-prep.md`'s over-reach
   rule — the mock interview is the stage where it actually fires, because the three CV
   judges only read the page and the page does not stammer.

4. **Never rehearse a gap into a non-gap.** For an HONEST-GAP the only preparation is the
   truthful framing already chosen in the tailoring plan. Do not produce a smoother version
   that implies experience the candidate lacks. "I haven't done X" must survive rehearsal
   intact; only the sentence around it may improve.

**The tripwire.** Any figure, tool, employer, title, or scope that appears in the
candidate's answer and is in NEITHER the profile, NOR `interview-brief.md`, NOR an earlier
answer this session, is tagged `UNSOURCED-FACT` (or `OVER-CLAIM` if it exceeds a recorded
source fact) and the candidate is asked where it came from BEFORE it may enter the answer
bank. Usually the answer is "it's true, it's just not on my CV" — that is a real finding and
it should probably go on the CV. Sometimes it is drift under pressure. Either way it gets
resolved, never silently kept: an answer-bank entry containing an unsourced fact is worse
than no answer bank, because the candidate will say it out loud in the real interview
believing you vetted it.

### Mock-interview session mechanics

- **Information isolation.** The interviewer is inline and sees everything. The first
  assessment pass sees the transcript, `posting.yaml` and `cv.md` — **the first assessment
  pass does not see `interview-brief.md` or `claims.yaml`**, so it cannot credit the
  candidate for a source fact they never said out loud. The second pass sees the transcript,
  `claims.yaml` and `interview-brief.md` but not the rubric, and emits only
  `UNSOURCED-FACT` / `OVER-CLAIM` / `CONTRADICTED`. Feeding the two passes different inputs
  is what turns the honesty tripwire from an intention into a mechanism.
- **One round per dispatch.** Assess, write the artifacts, stop. Round n+1 carries an
  open-loops summary, never the full transcript.
- **Flush the transcript after every answer**, not at the end of the round. A crashed
  session then loses one answer instead of a round, and the assessors read a file rather
  than this conversation.
- **Bands, not scores.** `not_present` / `asserted` / `instanced` / `held_under_probe`, plus
  the non-band flag `contradicted`. They are unnumbered so they cannot be averaged, and
  `held_under_probe` is the ceiling on purpose: a higher band would require knowing what
  this employer expects at this level, and this skill does not.
- **The interviewer and both assessors may not emit** a score, grade, percentage or invented
  "X out of Y"; a probability, likelihood or odds; "you would pass / fail / they would hire
  you"; "strong candidate" / "weak candidate" / "hire" / "no-hire"; any comparison to other
  candidates; any claim about what the interviewer thought or would conclude; or a rating on
  a scale the employer did not publish. **The one exception**: where the employer publishes
  its own rubric, you may walk the candidate through that published scale in the employer's
  own wording, attributed, as a checklist of what the panel is told to look for. Quoting an
  employer's scale is reporting; applying it as a verdict is fabrication.

## Self-check — run through this before reporting the package as done

- [ ] Drafting or revising a client report? Read `references/report-writing.md`,
      complete the separate full-report reader review: read every section/table,
      assess reasonableness, logic and readability, fix and reread the entire
      revision, then read the final PDF. Record concrete findings privately;
      preserve every posting's city/link and inspect navigation and typography.
- [ ] Domestic job discovery? Reconcile the WeChat source plan with captured
      queries, original articles and recruitment conditions; identify unread or
      inaccessible leads. A successful search command is not completed research.
- [ ] Following a report example? Compare its applicable tables, columns,
      numbered jobs, field labels, preparation lists and directory with both the
      final Markdown and PDF. Recheck every explicit user correction; do not
      accept a font/color match while the information structure is missing.
- [ ] Client delivery? Read the entire report without the private test notes:
      it must give career decisions and actions, with no fixture or test-process
      narration. For a requested full-page CV, check the final Word-export PDF's
      page count, measured content bottom and natural spacing before delivery.

- [ ] On a site refusal, follow `references/user-recovery.md`: explain the reason,
      preserve partial results, wait for explicit user confirmation before a new
      linked round; do not clear the stopped journal.

- [ ] Daily-browser CDP and parallel sources: follow `references/daily-browser.md`;
      verify the selected profile, isolate tabs and share site budgets.
- [ ] Browser capture: read `references/browser-fallback.md` and record each
      actual snapshot with `scripts/record_browser_capture.py` before another read.
      Use `browser_page` evidence and stop across tools after a site refusal.
      Navigation requires a journal-derived budget and a catalog selector for
      every stage; final-page rows alone cannot establish round compliance.

Read-when:
- [ ] Reviewing a Word or PDF CV? Follow `references/layout-review.md` and compare every rendered page with the supplied template and the user's later changes.
- [ ] Page unavailable? Follow `references/network-recovery.md`: classify first,
      use bounded retries, and inspect relevant VPN/split-routing evidence.
- [ ] Diagnosed OpenCLI adapter incompatibility? Read `references/opencli-compat.md`;
      `scripts/opencli_compat.py` checks optional, reversible local patches.
      Browser fallback does not require patching; a site refusal still stops reads.
- [ ] Running on a host that is not Claude Code — codex, another agent, or as a
      subagent without `AskUserQuestion`? Read `references/portability.md`.
- [ ] Not a software/research/engineering role? Read `references/role-families.md`.
- [ ] Employment gap >6 months, career switch, re-entry, over/under-levelled, thin
      experience, executive, military transition or international credentials?
      Read `references/candidate-situations.md`.
- [ ] Essential/Desirable criteria, behaviours or a scored supporting statement?
      Read `references/structured-applications.md` — it REPLACES the CV judge loop.
- [ ] Writing a letter? Read `references/motivation-letter.md` (skip gate first).
- [ ] Japan + traditional/domestic employer? Read `references/rirekisho.md`.
- [ ] Building or reordering the CV? `references/cv-craft.md`.
- [ ] Rendering a Word CV? Follow `references/word-resume-layout.md` and inspect the exported pages.
- [ ] Doing gap analysis or tailoring? `references/gap-analysis.md`.
- [ ] Extracting a posting? `references/job-posting-extraction.md`.
- [ ] Writing the brief? `references/interview-prep.md`.
- [ ] In apply mode? `modes/apply.md`, loaded on entry, not on demand.
- [ ] In interview mode? `modes/interview.md`, loaded on entry, not on demand — and
      `references/interview-shapes.md` in full before the first question.
- [ ] In discover mode? `modes/discover.md`, loaded on entry, not on demand.
- [ ] Matching a discovered role to a CV? Read `references/candidate-matching.md`,
      then run `scripts/snapshot_profile.py` once to freeze
      `candidate-profile.yaml` before mapping any detail.
- [ ] About to make the first live retrieval of a run, or asked to page further,
      fetch more detail pages, or work while the user is away?
      `references/source-policy.md`.
- [ ] About to call an adapter other than the four in SKILL.md's table?
      `references/discovery-sources.md`.
- [ ] An adapter call exited non-zero? `references/risk-control-signals.yaml`
      carries the stop-signal patterns `scripts/check_opencli_result.py` matches.

Dispatched:
- [ ] `agents/ats-screener.md`, `agents/recruiter-screener.md` and
      `agents/hiring-manager.md` were each pasted IN FULL into their own judge.
- [ ] `agents/mock-assessor-transcript.md` and `agents/mock-assessor-provenance.md` were
      each pasted IN FULL into their own assessor, with **different** input packs.

Ran, with a receipt in `journal.jsonl` — `scripts/check_apply.py` requires each of these
unconditionally:
- [ ] `scripts/check_personal_data.py`
- [ ] `scripts/check_claims.py` — the VERIFYING run. The `--record` run at mode entry
      fingerprints the master and checks nothing; its receipt says `baseline_recorded`
      and `check_apply` reports it as `NOT_VERIFIED`, not as a pass.
- [ ] `scripts/check_render_freshness.py` — recorded before dispatch AND verified after.
      Same rule: the dispatch record is `baseline_recorded`, the verifying run is the
      one that counts, and re-recording for the next round does not carry the last one.
- [ ] `scripts/parse_verdicts.py` — its receipt reports on the PARSE. A cleanly parsed
      round is `recorded` whatever the three judges said; `fail` means a judge returned
      no usable `VERDICT:` line and must be re-dispatched.
- [ ] `scripts/lint_cv.py`

Required too, but only when the artifact they read is on disk — `check_apply` keys each
one on the file, so "it did not apply" is never guesswork:
- [ ] `scripts/check_letter.py` (when `letter.yaml` exists)
- [ ] `scripts/check_layout.py` (when `cv.docx` or `cv.pdf` exists; inspect all pages against the supplied template first)
- [ ] `scripts/check_pages.py` (when `cv.pdf` AND `tailored-profile.yaml` exist — both
      are its inputs, and a `could_not_run` receipt does not satisfy it)
- [ ] `scripts/check_word_limits.py` (when `supporting-statement.md` exists, or
      `posting.yaml` says `application_type: structured` and the statement is missing)

Ran, with a receipt — but `scripts/check_apply.py` does NOT require these, so skipping
one is silent and only this line reports it:
- [ ] `scripts/check_apply.py` — the composer itself; it cannot require its own receipt.
- [ ] `scripts/check_mock.py` (once per mock-interview round — interview mode, not apply)

`check_apply` also fails on ANY gate in this workspace's journal whose latest receipt
says `fail`, named on the lists above or not — a receipt from another mode excepted.
Enumerating gates does not keep up with the gates: `check_pages` and `check_word_limits`
were both off the required list, so either could run, print `CV_TOO_LONG` / `OVER_LIMIT`,
and have `check_apply` write its own `pass` three lines below it in the same file.

Ran, leaving a `mode_entry` record rather than a gate receipt:
- [ ] `scripts/enter_mode.py` — and its recorded hash still matches `modes/apply.md`.

Ran, leaving nothing in the journal (they render; they do not judge):
- [ ] `scripts/render_cv.py`, plus `scripts/render_letter.py` /
      `scripts/render_rirekisho.py` if applicable.
- [ ] `scripts/deliver.py` — the LAST step of every mode. A workspace under
      `~/.claude/job-profiles/` is where the skill works, not where a person
      looks, and a path pasted into a chat message is gone once it scrolls.
- [ ] `references/supplementary-sources.md` — career source selection, WeChat articles and source quality.
- [ ] `scripts/pdf_glyphs.py` — shared painted-glyph validation used by page checks and delivery.
- [ ] `scripts/layout_requirements.py` — imported measurement checks used by `check_layout.py`; verify reference-derived requirements for CV and report.
- [ ] `scripts/doctor.py` — once per machine, before the first mode. Reports
      capabilities by using them; `--install` covers the Python packages only. Follow
      `references/agent-setup.md` to install required tools and prepare daily-browser CDP.
- [ ] `scripts/setup_dependencies.py` — prepare the private runtime when required;
      `scripts/run_tool.py` invokes it without depending on global executables.
- [ ] `scripts/browser_cdp.mjs` — diagnosed fallback reads only; import the capture
      through `scripts/record_browser_capture.py` before the next same-site read.
- [ ] `scripts/save_profile.py` — every master save goes through it. One CV per
      language, and a new language never overwrites another's file.

In CI, not in a workspace (no receipt exists for these, by design):
- [ ] `scripts/check_skill_lossless.py` — only when this skill's own files changed.

Ran, with a receipt in `journal.jsonl` — the discover gates. `scripts/check_apply.py`
does not require these; a discover run is not reportable without them:
- [ ] `scripts/check_no_write.py` (discover)
- [ ] `scripts/check_candidate_match.py` (discover; after the profile snapshot and before the shortlist)
- [ ] `scripts/check_shortlist.py` (discover); final `scripts/deliver.py` must check
      complete descriptions for all retained postings across collection rounds,
      or captured access failures with visible reasons. Cards are allowed in an
      explicitly requested preliminary report, not a completed consultation.
- [ ] `scripts/check_search_coverage.py` (complete discover/collection delivery):
      register planned sources and directions before retrieval; close every
      planned pair and observed lead with evidence. Round limits, target counts
      and `shortfall` do not mean completion. Delivery rechecks current evidence.
      See `references/search-coverage.md` for the multi-round manifest and schema.

Ran, leaving an `adapter_call` record rather than a gate receipt:
- [ ] `scripts/check_opencli_result.py` — once per adapter invocation. It is a
      wrapper, not a gate: it exits 0 (classified) or 2 (could not classify), never 1,
      so there is no receipt to look for and no pass/fail to read into the exit code.

Every line above says what evidence it leaves, and the headings differ for a
reason: a checklist that promises a receipt where none can exist teaches its reader
that one of its lines is decorative, and the reader cannot tell which one.

In assess mode:
- [ ] Assessing a posting? `modes/assess.md`, entered with `scripts/enter_mode.py`.
- [ ] Writing a Japanese, Korean or Spanish discover/assess report?
      `references/report-localization.md` for native headings, counts and disclosures.
- [ ] Rendering a market convention card? `references/market-conventions/README.md` is the
      rule for what may be in one; the tables are `references/market-conventions/cn.yaml`,
      `references/market-conventions/nl.yaml`, `references/market-conventions/de.yaml`,
      `references/market-conventions/uk.yaml`, `references/market-conventions/us.yaml`.
- [ ] Ran `scripts/evidence_blocks.py`, `scripts/count_coverage.py`,
      `scripts/consistency.py`, `scripts/check_evidence_refs.py`,
      `scripts/lint_no_prediction.py` and `scripts/check_assessment.py`, and quoted
      `check_assessment`'s receipt? `scripts/check_conventions.py` runs in CI over all five
      tables.

Told the user:
- [ ] All three verdicts and the ATS coverage line, verbatim, each round.
- [ ] The FIT SNAPSHOT with its required disclaimer, before and after.
- [ ] Which market and language the CV was calibrated for.
- [ ] Any remaining honest gaps, and — if the loop ended un-passed — whether this is
      POORLY BUILT or an HONEST STRETCH.
- [ ] The consultation folder and its client report/CV files; keep internal files private.
- [ ] **The delivered files** `deliver.py` printed — in one `~/Downloads/<workspace-name>/` folder, including the report PDF.
      That is the one the user can actually open; the workspace path is for an audit.
- [ ] In discover: before delivering a complete report, read the full description
      of every retained posting. Search-card summaries serve internal triage and
      do not satisfy this requirement. If access genuinely fails, retain a failure
      capture, explain the reason in the report and mark the posting unresolved;
      never count it as detail-reviewed. Show the Sources and read quality table,
      the trigger reason and each posting's actual read status. Full detail review
      is still distinct from a complete application assessment; use the matching
      disclosure from `modes/discover.md` and `references/report-localization.md`.
      **Write the output in the user's language.** Keep one language per document.

CV typography: English uses Times New Roman and Chinese uses SimSun (宋体),
including names and headings, unless the user explicitly requests otherwise.
For reports, follow `references/word-resume-layout.md`: an explicitly selected
font/template wins; otherwise the portable renderer may use its embedded fonts.
Verify embedded PDF fonts, not only DOCX settings. Preserve template font sizes
and aim for a well-filled page; any added gap before a section heading is at
most one blank line. Never invent content or shrink fonts just to fill a page.
