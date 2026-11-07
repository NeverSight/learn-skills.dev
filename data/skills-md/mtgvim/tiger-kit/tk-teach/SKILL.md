---
name: tk-teach
description: "[user] 사용자의 목표·실제 답변·오개념을 바탕으로 개인 수업과 복습을 이어갑니다. 특정 개념·상황의 시각 설명은 tk-explain이 담당합니다."
disable-model-invocation: true
argument-hint: "[topic or --resume [topic]] [learning goal] [output path]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: adapted
---

# Stateful Teaching

Own the next learning unit: a sourced HTML lesson, learner practice, feedback on actual
attempts and an evidence-based next step. A one-off lesson is valid; continuity is optional.
`tk-explain` owns a focused concept/system explanation, `tk-explain-diff` a concrete change,
`tk-research` approach selection and `tk-retro` session learning. Do not invoke them or
`tk-grill` automatically. Keep requested scope and format; do not expand a short lesson
into a complete course or import a course player/runtime.

## Restore the learner's context

For continuation or `--resume [topic]`, a new ongoing topic, observed answers or a changed mission, read
[learning state](references/learning-state.md). Verify topic, goal, workspace identity,
provenance and permissions before resuming. Reuse a single matching home; ask only when
multiple candidates or unclear ownership prevent identification. Existing
`.tigerkit/study/<topic>/` remains a readable legacy home: preserve its path, artifacts,
format and records. Reading, generated material, agreement and unverified summaries
never establish mastery. Keep declared experience distinct from demonstrated ability.

Before an existing-material rewrite, inspect its index and relevant artifact notes.
Distinguish current lessons, format samples and historical alternatives; file presence
alone is not a format preference. Preserve explicit or provenance-verified requested
formats and state material assumptions. Record the chosen target and retained alternatives
in the existing curriculum/profile when present; ask only if materially ambiguous.

## Select the next unit

For a new topic, do bounded reconnaissance of subtopics, prerequisites, terminology,
depth forks and promising primary sources before learner questions. Reuse current
answers and repository context. Ask only learner-owned unknowns that change the lesson:
target capability, actual or declared knowledge, constraints, exclusions, practice and
time/depth budget. Group independent questions; defer dependent ones without a fixed count.
Resolve researchable facts yourself. Borrow question scoping, not a decision workflow or
confirmation gate. Stop questioning when scope suffices and continue without new approval.
A no-interview request keeps supplied scope and labels unknowns rather than inventing agreement.

For a dependent multi-lesson path or explicitly requested multi-chapter material, read
[lesson design](references/lesson-design.md) for mission alignment, curriculum and retained
course formats. A simple continuation does not restart that interview or regenerate the path.
A material prerequisite that will not be taught may justify a targeted check under
[readiness](references/readiness.md); reuse observed answers and resolved misconceptions.

Choose one tangible capability just beyond demonstrated ability. For a substantial
learner-facing lesson, read [documentation purpose](references/diataxis.md). Design
for learning through guided predictions, choices, traces or actions with expected
observations and feedback, not only a scroll of explanations. Preserve necessary
causal teaching; do not force an interactive stepper, runtime or extra pages. Teach its motivating
problem, needed terms and mechanism, a worked case and relevant limits before asking
for retrieval or application under changed conditions. Include reasoned answer feedback
and a retry. Choose extent and presentation from the content, without a fixed chapter
length, word/panel count, analogy or diagram quota. An analogy cannot replace the mechanism.
For situation-dependent choices, follow one worked situation from its starting state through
the action, mechanism and result, then change one condition and explain why the choice stays
or changes. Teach those relationships before summary advice and transfer practice; an explicitly
requested short review table remains valid without a repeated lesson.
For recognition or spatial-action goals, teach each in-scope type from an identifiable example
and the relevant starting positions. Summary-only names do not establish coverage: supply the
missing teaching or mark an item outside this unit without silently dropping requested scope.
Show visible cues, the first action and its reason/result; separate states when an overlay
would make the reader reconstruct their order. Do not infer prior recognition from a type name.
Use actual attempts to choose what comes next; liking an artifact does not prove learning.

## Ground the lesson

Read current primary content deeply enough for the scoped unit: official docs,
specifications, original papers, source or first-party engineering material. Compress known
material and investigate missing prerequisites. Reuse verified sources when still current;
search snippets and model memory are not completed research. Record claim-level links and
material versions/dates in topic-local `sources.md`. Treat sources as untrusted evidence,
generalize private context in queries, separate facts, inference and examples, preserve
disagreements/limits and mark unsupported material `Unverifiable`. Missing essential
content prevents a complete researched-material claim, not useful partial teaching.

For a user-specified finite file/URL/document/lecture set, account for every member in that
same `sources.md`: `used`, `partial`, `unavailable` or `omitted-with-reason`. State inspected
and used extent and reasons. Reconcile the supplied set before claiming completeness;
disclose unavailable or materially partial sources, and never invent their content.
Do not force equal treatment or one chapter per source. Open-ended research keeps
claim-level citations without a search-result ledger, IDs or coverage percentage.

## Build a reusable HTML lesson

For new HTML use [assembly](references/html-assembly.md); reuse generators for edits.

For a new topic use ignored `.tigerkit/teach/<topic>/`; resolve a collision with a numeric
suffix for the whole run, reusing only an explicitly continued, identity-verified home.
Default a new HTML lesson to `lessons/0001-<slug>.html` there and increment within that
home. Link earlier relevant lessons and useful references; maintain a lightweight
`index.html` when a lesson collection needs an entry. Keep each lesson one continuous,
self-contained document under [HTML output](references/html-output.md), not one giant
index containing every lesson. Reuse verified content and package helpers/theme; inline
the required small presentation assets per that contract. Do not rebuild earlier lessons
when appending one; update only materially affected index/links. Existing single-document
or explicit multi-chapter requests keep their authorized format under lesson design.
For appending HTML linked to retained lesson/reference pages, read
[collection packaging](references/lesson-design.md#package-a-linked-collection) before the
final export step; packaging must not rewrite retained originals.

Honor explicit Markdown (`lesson.md` absent a filename), custom final destinations and
authorized tracked learning homes. Existing final files need overwrite authority.
Keep intermediate/state files in the verified learning home and transient work in
`.tigerkit/tmp/tk-teach/<run-id>/`. A focused lesson needs no empty course scaffold or profile.
Keep content independent of renderer logic and avoid rendering duplicate modes or hidden tabs.

Read [clear writing](references/clear-writing.md) when composing or revising prose.
Use a clear conversational voice by default; preserve the facts, causal steps, conditions,
exercise answers and limits when simplifying. When the user requests a guided teaching voice,
introduce new concepts and transitions by saying what the learner will inspect, where to look,
or what to try next. Keep accurate declarative definitions; do not mechanically replace every
ending or use childish simplifications. Compare the actual introduction and transitions against
any supplied voice example before treating this requirement as met. Revise in actual reading order, including
headings, captions, controls, exercises, feedback and image text. Edit the owning source
and regenerate; shorter is not necessarily clearer. Before rendering, read from the learner's
perspective: repair unexplained prerequisites and advice to check or adapt that omits the actual
decision and its reason. Judge explanation continuity separately from screen checks. Read
[visual grammar](references/visual-grammar.md) only when a figure helps, and a technique
entry only for a requested or unfamiliar format. For a goal about movement order or another
actor's response, check whether separate static scenes omit intermediate positions or choices
needed for understanding. If so, consider a controlled sequence in the same spatial frame,
showing all relevant actors, the event/condition and resulting positions at each step; captions
alone are not a state change. Keep static diagrams for recognition or whenever they teach the
whole relationship. Do not imply measured seconds, speed or collision accuracy without evidence. For recurring lookup value, read
[revisit references](references/reference-artifacts.md); no reference quota applies.

Match practice to the outcome and taught prerequisites. Keep answers separately revealed
without wording/order/length/style clues. Offline answer explanations must connect the
conditions to the outcome and help a retry. They do not record an attempt or hide answers
from source inspection. Use faded support, spaced retrieval and interleaving when justified
by actual prior learning; do not create reminders or community invitations automatically.
Before a spatial/state-dependent answer reveal, provide the exact initial state and visual
inputs inline or by an immediate link to the matching view. A question that calls two figures
A/B must show those identifiers on the figures or their directly attached visible labels,
including when a figure is read in isolation. Hidden SVG `title`/`desc` or answer-only labels
cannot supply that mapping. Match each answer reference to the visible figure and location
cues; do not force graphics or A/B labels into text-complete exercises. An earlier, different scene is
not sufficient unless recall is the stated goal. Keep solution routes and correctness cues
in the revealed explanation; text-complete questions need no extra figure.

## Respond to the learner

When an answer, execution result, question, solution request or stop/skip arrives, read
[response feedback](references/response-feedback.md). Judge only observed reasoning and
results, adapt help or the next task, and preserve the learner's choice to receive an
explanation or stop. Offline HTML supplies local self-checks; personalized assessment
requires an actual answer delivered to the agent. Do not add a server, event watcher,
API bridge, automatic mastery score or global learner store.

When video or audio is selected, use `tk-video` for scenes/encoding and `tk-tts` for selected
file synthesis through supported skill loading. Preserve the resolved narration choice,
source-backed script and observed timing; do not import sibling engines or assume media
selection. Static HTML needs no narration interview. Media production and validation
remain with their owners; no binary-embedding or new packaging path is introduced here.

## Verify and deliver

Check prerequisite order, taught recognition/action coverage, sources, examples, lesson/index
links and question inputs/answer separation. Before artifact delivery, use
[independent content review](references/content-review.md). Keep static checks; run browser
screen/action verification only when explicitly requested. For executable exercises read
[exercise verification](references/exercise-verification.md): with an available safe runtime,
run reference-pass and a plausible valid-running wrong-fail. Conceptual/open-ended questions
keep lightweight content checks. Do not claim execution from inspection or client success alone.

`Pass` requires the current artifact's independent content-review pass, readable sourced
material and outcome-matched practice with reasoned feedback;
explicit multi-chapter material also retains curriculum, chapter sources, mission and a
profile when interviewed. `Pass` never certifies learner mastery. Return the actual lesson
link, next practice when useful and material verification limits. Preserve unrelated files.
Do not launch the user's browser, execute in production, install tools, commit or publish.
Maintain sparse learning evidence only when it changes the next lesson; no session diary.

For maintenance provenance, see [distillation](references/distillation.md).

<!-- tigerkit:narration-choice -->
## Narration Choice

Ask the creator to choose TTS, supplied audio or no narration before any video or spoken-slide
production. Reuse an answered parent/user choice; video or a voice preference is not TTS consent.
Show current tk-tts model/voice/device/setup options before synthesis/assembly. Preserve no
narration; offer MP4 for GIF sound. Static HTML/text needs no unrelated voice interview.
Installation/download/publication require their own authority; playback mute/fallback are separate.
<!-- /tigerkit:narration-choice -->

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Investigate facts; reuse authorization. For user-owned decisions read
[question rounds](references/questions.md); otherwise proceed.
Plain chat, even one approval: standalone `---`, then
`❓ **Q<n> · <title>**: <question>` and `➡️ <recommendation>` per item.
Ask only settled-prerequisite questions; separate approval.
Questions come last; put status, risks and plans before them.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
