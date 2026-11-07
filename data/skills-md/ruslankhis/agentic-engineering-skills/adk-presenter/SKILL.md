---
name: adk-presenter
description: >-
  Prepare the presentation that wins the next decision on a Google ADK agent
  project, from its recorded evidence: a slide outline with an action title
  and an evidence citation per slide, the spoken narrative, the questions to
  expect and a one-page decision memo. Use at a phase boundary that needs
  someone's decision (proof-of-concept approval, a production decision, a
  final results review) or for a public case study, in business and technical
  versions. Also writes the go-live rollout pack (user guide, training,
  messages, AI disclosure, adoption metrics, hypercare exit) and the monthly
  value report to the sponsor (outcome against baseline, cost per outcome, a
  stop, continue or scale call). Do not activate to change the application,
  run evaluations or audit results (adk-agent-evaluation), to choose the use
  case (adk-discovery), to design the system or write a proposal
  (adk-system-designer), or for governance papers (adk-governance-pack).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-cutting"
  sources-reviewed: "2026-10-15"
  verified-against: "not applicable: writes presentations from recorded evidence; runs no ADK code"
  version: "2026.10.28"
---

# ADK presenter

Turn what the project has recorded into the material a decision-maker needs:
one outline per audience with the evidence beside every claim, what to say,
what they will ask, and the one page they keep. The deliverable is documents
under `docs/presentations/<topic>/`; the skill changes no code and runs no
evaluation. A number the record does not hold does not go on a slide: the
slide says "not yet measured" and names the goal that would measure it, or
the agent asks the user for the source. Arithmetic on recorded numbers is
allowed when both inputs and the operation are on the slide and the voice is
*we estimate* ("$142 over 312 sessions, about $0.46 a session, build-time
spend included"). A projection that multiplies a recorded per-unit figure by
a stated volume assumption (a pilot queue scaled to four queues) is allowed
when the assumption is on the slide in the same voice; stacking two
assumptions is not.

## Read the record, then settle the stage and the audience

Read the record first, in this order, and note the path of every figure you
will use: the discovery brief (`docs/discovery/<topic>.md`: baseline,
hypothesis chain, counter-metric, stakeholders and decision dates), the
design (`docs/architecture/<topic>.md`: profile, contracts, decisions,
deferred controls, open decisions), the plan (`docs/plans/<topic>.md`: goals,
the schedule check's hours, evidence lines per contract, cut line, risks,
acceptance cases marked not run, the build each result came from, and the
measurement records `M1`, `M2` and incident records `I1`, `I2` that a pilot
or production run adds, each with value, baseline, window, sample, method,
owner and build), tickets and their Evidence sections, and any evaluation
report, cost record or incident log the plan links, and the governance
pack (`docs/governance/<topic>/`) when one exists: its system card for
limits and oversight, its classification memo and open counsel questions
for the risk slide. When a later report
contradicts the plan's calendar or a recorded figure, ask which is right and
record the change in the plan's change table before drafting; when the
record lacks a measurement record for a figure the user reports, write it
into the plan as `M<n>` first, labelled with its source, so the slide cites
a record. Where the project keeps these under other
names, use those. Write down what the record does not contain (no baseline,
cases not run, cost not measured, no build tag on a result, no demo) before
drafting; those gaps become slides, not omissions.

If the engineer keeps a practice profile, read
[practice profile](references/practice-profile.md) for the org's audience and
presentation style; numbers still come only from the record. Its past AI
attempts can frame the story ("the last chatbot was stopped for accuracy;
this measures accuracy first"), never as a figure on a slide.

Then settle three things in one line each, asking only for what the request
and the record do not say:

- **Stage:** `poc-approval` (before the build), `production-approval` (the
  proof-of-concept review that decides on production), `final-results`
  (after production), or `case-study` (public, after measured results and
  approvals), or `value-report` (monthly after launch: one page for the
  sponsor, not a deck; read [value report](references/value-report.md),
  write it from the [template](assets/value-report-template.md) and check
  it with `scripts/check_value_report.py`; the audience is the sponsor,
  there are no minutes, and the storyline, deck and rehearsal sections
  below do not apply). A proof of concept with only a demo and no measurement is
  presented as an approval case with hypotheses, not as results.
- **Audience:** `business` (funds, extends, builds, stops; reads the summary,
  the result against criteria, cost, risk, the ask), `technical` (hosts,
  depends on, is paged for; reads the design, contracts, evaluation report
  and runbook; an external IT firm that will host it counts, and gets a
  shorter outline centred on what it inherits), or `public` for a case
  study. When both are needed, write
  two outlines from the same evidence; never one deck for both.
- **Minutes, decider and date:** the speaking time, the one person who
  decides, and when; the brief's decision calendar and the plan's waits
  usually hold them. Default: fifteen minutes for business, thirty for
  technical.

## Write the storyline before the slides

Read [storyline](references/storyline.md). Write the four lines (situation,
complication, question, answer) from the record, then the ghost deck: the
ordered action titles with the `Covers:` tag and the evidence each needs,
following the outline for the stage and audience in
[stage outlines](references/stage-outlines.md). Read the titles as a
paragraph; when they do not carry the argument from situation to answer to
ask on their own, fix the titles before writing a body. Every ask is two or
three real options with the recommended one marked, the decider and the
date. Every deck has a value slide against the baseline, a cost slide (before a
pilot: the hours and the spend ceiling; after one: per conversation and per
month, actuals apart from estimates) and a risk slide with a control and an
owner per risk, because those are the three reasons agent projects get
cancelled.

## Draft in the deck format

Write the outline in the [deck format](assets/deck-format.md): front matter
with stage, audience, minutes, sources and the decision sentence; slides
separated by `---`; each with `## <action title>`, `Covers:`, `Evidence:`
and `Notes:` written as speech from [the speech reference](references/speech.md):
bottom line first, today and after in alternation, one real case on the
story spine, three reasons, what did not work and the answer, options and
the decider, and the stage skeleton's timings. The three voices stay apart
in titles and notes: *we measured*, *we estimate*, *we hypothesise*; on a slide that
mixes them, each bullet opens with its voice word and the `Evidence:` line
lists each source. State the build the demo shows and the build the numbers
cover, or that there is no demo. Put vanity counts (conversations, messages)
and the answers to expected questions in appendix slides tagged `questions`
or `appendix`; they do not count against the minutes. For a technical audience, link the
design, the contracts table, the evaluation report and the runbook by path
and quote the figures; qualifiers go in the title. Read
[audiences and questions](references/audiences-and-questions.md) for the
notes pattern and the question bank; answer each question from the record in
an appendix slide or with "not measured" and the goal that would measure it.

For a case study, read [case study](references/case-study.md) first: it adds
the approval trail per sentence, Google's approved attribution phrases and
the submission pack, and uses the [case-study template](assets/case-study-template.md);
the prose is the deliverable, linted with `check_deck.py --prose`, and a
companion deck is written only when the user wants a meeting version.

## Check, then pre-wire and rehearse

Run the deck check from the project root with any Python 3.9 or later,
resolving `SKILL_DIR` to this skill's directory:

```bash
python3 "$SKILL_DIR/scripts/check_deck.py" --deck docs/presentations/<topic>/<stage>-<audience>.md
```

Exit 0 means every slide cites evidence or says why not and the stage's
coverage is complete; fix every error and read every warning, including the
spoken-time estimate it makes from the notes. The outline is not ready until
the check passes. Then run the premortem ("this presentation failed to get
the decision; why?") and put each answer's evidence in an appendix slide;
write the pre-wiring table and the premortem answers to
`pre-wiring-<stage>.md` in the same folder; and give the user the rehearsal checklist and the question
protocol from the speech reference, with two runs out loud, one before a
colleague who plays the decider and interrupts (once per project; later
stages point back to it).

Write the [decision memo](assets/decision-memo-template.md) to
`decision-memo-<stage>.md` in the same folder as the one-page pre-read, and
after the meeting record the decision, owners and next checkpoint in it and
in the plan (the decision date is the calendar wait the next phase depends
on), together with the estimate the decision rested on (hours, spend, cost
per unit), so the next review measures against a number that lives in the
plan, not in an old deck. When the presentation is a plan goal or a ticket,
fill its Evidence section: the outline paths, the check result, the
briefings held, and after the meeting the decision.

The outline is the stage's deliverable; render slides only when the user
asks for them. Then, when the host offers a slide-building tool or skill,
build the slides from the outline by [slide craft](references/slide-craft.md):
the action title as the headline, one visual with its caption, at most two
call-outs, charts from recorded data with the baseline drawn, `Notes:` as
speaker notes, `Evidence:` kept out of the audience's view, and two
renderings (projected and leave-behind); otherwise hand the outline and that
reference's checklist to whoever owns the company template.

## Rollout pack at go-live

When the request is the rollout pack, a user guide, training, launch
messages, AI disclosure text or adoption measures, read the record as above
(the stage and audience lines do not apply), then read
[rollout and adoption](references/rollout-and-adoption.md) instead of the
storyline and deck references, and write from the
[rollout pack template](assets/rollout-pack-template.md) to
`docs/rollout/<topic>/rollout-pack.md`. Every statement of what the agent
will or will not do cites the contract that enforces it, any claim of how
well it works cites a measurement record, and "report a problem" writes the
feedback record that `adk-agent-observability` defines. Check it with
`python3 "$SKILL_DIR/scripts/check_rollout.py" --pack <path> --design <design path>`;
the pack is not ready until the check passes. Finish with where the pack is,
the check's result, the assumptions and gaps table's open items with who
settles each, and the prompt for the next goal (often the operations
handover).

## Finish

End with where the files are, the check's result, the gaps the record left
and how each is shown on a slide, the decision sentence, and the prompt for
the next step: the plan's next goal after the decision, or
`/adk-presenter` for the other audience. When the evidence does not support
the decision the user wants to ask for, say so before the deck does.
With a practice profile, offer its harvest ([practice profile](references/practice-profile.md), step 5).

Independent community project; not affiliated with or endorsed by Google.
