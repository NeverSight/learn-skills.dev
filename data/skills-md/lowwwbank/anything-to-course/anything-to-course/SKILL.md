---
name: anything-to-course
description: Turn any source material — documents, notes, books, articles, transcripts, slides, codebases, or just a topic — into a complete self-study course built on evidence-based learning science (retrieval practice, spaced repetition, interleaving, faded scaffolding, confidence calibration). Use whenever the user wants to create a course, curriculum, tutorial, training program, study guide, workshop, onboarding track, or learning path from existing content or expertise, even if they only say "help me teach X", "make learning materials from this", or "I need to explain this to my team".
license: MIT
metadata:
  author: lowwwbank
  version: "1.0"
---

# Anything to Course

Build courses that change what the learner **can do**, not what they recognize.

The failure mode to avoid: a "content dump" — well-organized explanations followed by a
few recognition quizzes. It reads smoothly, feels clear, and evaporates within a week.
Fluency is not learning. Every design decision in this skill exists to force effortful
retrieval, spaced re-encounters, and transfer to new contexts, because those are the
mechanisms that produce durable capability (see `references/learning-science.md` for the
principles and the research behind them).

## The one rule that governs everything

> The unit of course design is not a topic or a page. It is a **new capability of the
> learner** — something they can do after the course that they could not do before.

Content that does not serve a capability gets cut. A capability without practice is a
promise without a mechanism. A check that doesn't match the capability measures the
wrong thing.

## Workflow

### Step 0 — Intake

Collect the source material and establish context. Ask the user (or infer and state
assumptions explicitly if working autonomously):

1. **Audience** — who is the learner? What do they already know? What jargon is safe?
2. **Target capabilities** — what should the learner be able to DO afterwards?
3. **Scope and time budget** — a 2-hour primer and a 6-week course are different designs.
4. **Delivery format** — markdown for self-study (default), slides, LMS-ready text, etc.
5. **Stakes** — hobby curiosity vs. job-critical skill changes how much retention
   engineering (reviews, checkpoints) the course needs.

If the source material is thin in places, say so and either research the gap or mark it
as an explicit assumption. Never invent facts to fill a chapter.

### Step 1 — Define capabilities, not topics

Convert the material into 3–8 observable capabilities. Each must answer four questions:

1. What will the learner be able to do?
2. In what situation?
3. To what standard?
4. How will we see that it formed?

Weak: *"Understand product metrics."*
Strong: *"Given a product description and a set of metrics, the learner can choose the
primary metric, justify the choice, reject plausible alternatives, and name one risk of
misinterpreting it."*

Weak objectives produce weak courses — you cannot design practice for "understand".

### Step 2 — Map prerequisites and structure

- Build a dependency graph: which capabilities rest on which concepts and procedures.
- Slice into modules and lessons. **One lesson = one coherent capability**, a limited
  set of new concepts, one connected mental model. If a task needs several not-yet-taught
  operations, split the lesson or add stepping stones.
- Order by dependencies, not by the source material's table of contents.
- Plan a short diagnostic at each module start — its job is to choose the right level of
  support, not to grade.

Read `references/course-blueprint.md` before writing any lesson — it defines the
canonical chapter flow this skill follows.

### Step 3 — Prove the format with one sample lesson

Before building the whole course, write ONE representative lesson (pick the most
central capability, not the easiest) and show it to the user with a one-line note:
"this is the format every lesson will follow — happy with the depth, tone, and
practice style?". Why this step exists: it moves the user's first payoff from
"30+ minutes in" to "5 minutes in", and it catches style/depth mismatches when
fixing them costs one lesson, not a whole course. Adjust on feedback, then proceed.
Skip only when the user explicitly asked for a fully autonomous run — and say so.

### Step 4 — Write lessons using the canonical flow

Every lesson follows the attempt-first sequence (full detail and rationale in
`references/course-blueprint.md`):

1. Real problem or question the lesson answers
2. Learner's short attempt or prediction **before** the explanation
3. Clear statement of the principle
4. Fully worked example — showing *why* each step, not just *what*
5. Contrasting example or counterexample
6. Self-explanation prompts
7. Partially completed task
8. Independent task, notes closed
9. Feedback (in a separate answer file — never visible before the attempt)
10. Corrected retry or new variation
11. Exit ticket mixing current and previous lessons

Two writing rules are non-negotiable:

- **First-use rule**: never use a term the target learner doesn't know without defining
  it in plain words at first substantive use. Pattern: *"**Term** — what it is in plain
  words; what distinguishes it from neighbors; why it matters here."* Judge novelty by
  the audience's vocabulary, not the author's.
- **Example → principle**: every story or case ends with the transferable principle and
  at least one contrast (different context, or a look-alike case where the principle
  does NOT apply). One vivid example without contrast teaches surface details.

### Step 5 — Design practice and assessment

Read `references/practice-design.md` for the practice format matrix, question design,
distractor rules, and feedback structure. Core constraints:

- Practice format must match the capability (recall → free recall, not multiple choice;
  tool selection → mixed tasks that don't name the method; judgment → open case with a
  rubric).
- Recall before recognition: the learner formulates an answer from memory first, rates
  confidence, and only then sees options or the answer key.
- Support fades: worked example → completion task → independent task → new context.
- Some tasks must NOT name the method — in real work, problems don't arrive labeled with
  the chapter title.

### Step 6 — Engineer retention

- Schedule spaced reviews: same day → +1 day → +7 days → +21–30 days, scaled to course
  length. Every review requires retrieval, not rereading.
- Each lesson's exit ticket pulls one or two items from earlier lessons.
- Every 2–3 modules: a cumulative checkpoint with interleaved tasks from all previous
  modules, including at least one integration task where the method is not named.
- Emit a `review-schedule.md` so the learner knows when to return and to what.

### Step 7 — Quality gate

Before delivering, audit the whole course against the author checklist in
`references/quality-rubrics.md`. Fix every violation — the checklist items are cheap to
fix at this stage and expensive to discover as a learner. Also verify none of the
anti-patterns (same file) survived: recognition-only quizzes, answers visible before
attempts, terms used before definition, single examples without contrast, practice only
at the end.

### Step 8 — Deliver

Default output structure (adapt if the user asked for a different format):

```
<course-name>/
├── 00-syllabus.md            # capabilities, prerequisites, module map, how to study
├── modules/
│   ├── 01-<module-name>/
│   │   ├── 00-overview.md    # outcomes, why it matters, diagnostic
│   │   ├── 01-<lesson>.md    # lessons per canonical flow
│   │   └── 99-checkpoint.md  # end-of-module mixed practice
│   └── ...
├── answers/                  # feedback + explanations, one file per lesson,
│   └── ...                   # kept separate so answers aren't visible during attempts
└── review-schedule.md        # spaced repetition plan with dates/offsets
```

In `00-syllabus.md`, tell the learner *how* to use the course: attempt before peeking,
rate confidence, follow the review schedule, treat errors as material. Learners default
to rereading — the course must teach them not to.

## Study mode — running a course as the tutor

This skill also RUNS courses, not only writes them. When the user says "help me study
this course", "quiz me", "run my review session", or points at a course produced by this
skill (or any structured material), switch to tutor mode and follow the session protocol
in `references/study-mode.md`: retrieval first, confidence before checking, feedback
after the attempt, calibration log, and the spaced schedule as the source of what's due.
After delivering a new course (Step 8), offer this explicitly: "Want me to run your
first study session now?" — the course only works if somebody studies it.

When the course will be graded by an AI (open cases, variations), embed the guardrails
from `references/practice-design.md` § "AI as coach": give the AI the goal, context,
rubric, and quality-level examples; require it to cite specific fragments of the
learner's answer; and treat its feedback as a hypothesis, not a verdict. AI feedback
without a rubric drifts toward generic praise.

## Scaling to the request

Not every request needs the full apparatus. A "quick 1-hour intro" still gets
capability-first objectives, attempt-before-explanation, and retrieval practice — but
fewer modules, a lighter review schedule, and no cumulative checkpoints. State what was
cut and why. What never gets cut: practice with feedback, and answers hidden until after
the attempt.
