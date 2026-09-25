---
name: learning-objectives
description: Writing learning objectives using Bloom's Taxonomy, for L&D teams. Use this skill whenever an instructional designer, trainer, or course developer has a vague learning objective — like "employees understand the sales process", "participants know the key rules", or "learners are aware of the risks" — and needs to turn it into something specific, observable, and testable using Bloom's Taxonomy and the ABCD model (Audience, Behavior, Condition, Degree). Trigger when someone asks "how do I write a good learning objective", "is this a good learning objective", "what should participants be able to do by the end", "Bloom's Taxonomy", "SMART learning objectives", or wants to check, rewrite, or derive learning objectives for a course, module, or program. Also trigger proactively whenever a course or module is being scoped (right after needs analysis or didactic reduction) and learning objectives haven't been defined yet — objectives are the bridge to assessment design and microlearning design, and skipping this step produces weak quizzes and unfocused modules.
---

# Writing Learning Objectives with Bloom's Taxonomy

**The problem**: "Employees understand the sales process" sounds like a learning objective, but nobody can tell whether it's been achieved. "Understand", "know", and "be familiar with" describe states inside someone's head — they can't be observed, tested, or designed around. Without a measurable objective, `assessment-design` has nothing to write questions against and `microlearning-design` has nothing to structure scenes around.

This skill turns vague topics or objectives into precise, testable ones — the bridge between *what to teach* (`needs-analysis`, `didactic-reduction`) and *how to build it* (`assessment-design`, `microlearning-design`).

## Step 1 — Understand the situation

Ask the user. If some answers are already clear from context, fill them in and ask only what's missing.

1. **What's the topic or skill?** Push for specificity — not "the sales process" but "handling objections in an initial phone call with a new customer".
2. **Who is the learner?** Role, experience level, what they currently know or do.
3. **What do they have already?** A vague objective to fix, a raw topic with no objective yet, or a course outline with several modules that all need objectives.
4. **What's the performance context?** What should the learner do differently on the job after this — concretely, in a real situation?
5. **What's this for?** A single objective check, a full set for a course/program, or prep work before assessment or microlearning design.

## Step 2 — Bloom's Taxonomy as a diagnostic tool

Bloom's levels aren't a checklist to climb — they're a way to match the verb to what the job actually requires. Most workplace training needs at least **Apply**; "Remember" and "Understand" objectives are usually only valid as a *prerequisite step* inside a larger objective, not the destination.

| Level | What it means | Verbs to use | Verbs to avoid here |
|---|---|---|---|
| **Remember** | Recall facts, terms, sequences | list, recall, name, state | know, be familiar with |
| **Understand** | Explain or reorganize in own words | explain, summarize, classify, compare | understand, grasp |
| **Apply** | Use knowledge in a new, concrete situation | apply, perform, solve, demonstrate | "implement" (alone, without context) |
| **Analyze** | Break a situation into parts, spot patterns | analyze, differentiate, diagnose, contrast | "take into account" (too vague) |
| **Evaluate** | Make and justify a judgment | evaluate, justify, prioritize, critique | "raise awareness of" |
| **Create** | Produce something new from parts | design, develop, compose, construct | "be creative" |

If the topic came from `needs-analysis` or `didactic-reduction`, the performance goal identified there usually already implies the right Bloom level — check it against this table rather than picking one in isolation.

## Step 3 — Sharpen with the ABCD model

Each objective should specify:

- **A — Audience**: who, specifically (not "participants" if a more precise role is known)
- **B — Behavior**: the observable verb from Step 2 — what the learner visibly *does*
- **C — Condition**: under what circumstances, with what tools, with or without support
- **D — Degree**: how well — the standard or criterion that counts as "achieved"

**Worked example:**

> Original: *"Sales reps understand the sales process."*
>
> Diagnosis: "understand" isn't observable, "sales reps" isn't specific, no condition, no degree, and it bundles four sub-skills (the four phases) into one objective.
>
> Rewrite (Apply level): *"By the end of the module, field sales reps (A) can correctly apply the four phases of the company's sales process (B) in a simulated first call with a new customer (C), asking at least one relevant needs-assessment question in each phase (D)."*
>
> Supporting prerequisite (Remember level): *"Sales reps can name the four phases of the sales process in the correct order."*

Not every objective needs all four letters spelled out explicitly in the final wording — but if the user can't answer one of A/B/C/D when asked, that's the part of the objective that's still too vague.

## Step 4 — Diagnose and rewrite

Run the user's input through these red flags. Most weak objectives trip more than one.

| Red flag | What it looks like | Fix |
|---|---|---|
| Unmeasurable verb | "understand", "know", "be familiar with", "be aware of" | Replace with the observable verb from Step 2 that matches what the job actually requires |
| Bundled objective | "Participants understand X, can do Y, and know Z" | Split into separate objectives, each with one verb and one outcome |
| Trainer-centered, not learner-centered | "This course covers...", "Module 3 addresses..." | Rewrite from the learner's side: "By the end of the module, participants can..." |
| Activity instead of outcome | "Participants watch a video", "Participants take part in a discussion" | Ask: what capability results from this activity? The objective describes that capability, not the activity itself |
| Bloom level mismatched to the job | Compliance training stuck at "Remember" when the job requires recognizing and acting on a real situation (Apply/Analyze) | Re-check against the performance context from Step 1 |

## Step 5 — Produce the output

```
LEARNING OBJECTIVE ANALYSIS: [Topic/Module]

STARTING POINT
Original objective / topic: [what the user brought]
Issues identified: [which red flags from Step 4 apply]

REVISED LEARNING OBJECTIVES

1. [Objective written in ABCD format]
   Bloom level: [Remember / Understand / Apply / Analyze / Evaluate / Create]
   Assessment note: [which question format from `assessment-design` fits — e.g. "Apply → scenario-based question"]
   Microlearning note: [which kind of scene/exercise from `microlearning-design` fits — e.g. "Apply → practice scene with a decision point"]

2. [further objective, if applicable]
   ...

OBJECTIVE HIERARCHY (if there are multiple objectives)
[Which objectives are prerequisites for others? In what order should they appear in the course?]

NEXT STEP
→ These objectives are ready for `assessment-design` (test questions) and/or `microlearning-design` (module structure).
```

If the user provided a course outline with multiple modules, run Steps 2–4 per module, then use the hierarchy section to show how the modules' objectives build on each other across the program — not just within one module.

## Step 6 — Prompt to take away

```
LEARNING OBJECTIVE PROMPT

Role: You are an experienced instructional designer specializing in Bloom's Taxonomy and the ABCD model.
Topic: [specific topic]
Audience: [role, experience level]
Performance context: After the training, learners should be able to [concrete on-the-job situation/behavior].

Task: Write [N] learning objective(s) at [Bloom level(s)] using the ABCD model
(Audience, Behavior, Condition, Degree).

Avoid: "understand", "know", "be familiar with", "be aware of", and other
non-observable verbs. Don't bundle multiple capabilities into one objective.

Output:
- Each objective as a complete sentence in ABCD format
- Bloom level per objective
- If there are multiple objectives: order/dependencies between them

[PASTE YOUR SOURCE TEXT / RAW TOPIC DESCRIPTION HERE]
```
