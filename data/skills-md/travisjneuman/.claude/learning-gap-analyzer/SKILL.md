---
name: learning-gap-analyzer
description: Map understanding, identify knowledge gaps, and build targeted learning plans with spaced repetition. Use when assessing knowledge levels, designing study plans, or optimizing learning paths.
---

# Learning Gap Analyzer

Frameworks for diagnosing knowledge gaps, creating targeted remediation plans, and designing effective learning strategies using evidence-based techniques.

## Knowledge Mapping

### Self-Assessment Matrix

```
KNOWLEDGE MAP: [Subject/Domain]

Topic                    | Awareness | Understanding | Application | Mastery
                         | (1)       | (2)           | (3)         | (4)
-------------------------|-----------|---------------|-------------|--------
[Subtopic 1]             | [ ]       | [ ]           | [ ]         | [ ]
[Subtopic 2]             | [ ]       | [ ]           | [ ]         | [ ]
[Subtopic 3]             | [ ]       | [ ]           | [ ]         | [ ]
[Subtopic 4]             | [ ]       | [ ]           | [ ]         | [ ]
[Subtopic 5]             | [ ]       | [ ]           | [ ]         | [ ]

LEVELS:
  1 - Awareness:     I've heard of it, can recognize the term
  2 - Understanding: I can explain the concept in my own words
  3 - Application:   I can use it to solve problems independently
  4 - Mastery:       I can teach it, adapt it, and combine with other concepts

SCORING GUIDE:
  Mark your honest current level for each topic.
  Gaps = Topics where your level is below the target level.
  Priority = High target importance + large gap size.
```

### Concept Dependency Map

```
PREREQUISITE CHAIN: [Domain]

Build knowledge in this order (each level requires prior levels):

Level 1 (Foundations):
  □ [Concept A] → Required for everything else
  □ [Concept B] → Required for everything else

Level 2 (Core):
  □ [Concept C] ← Requires: A
  □ [Concept D] ← Requires: A, B
  □ [Concept E] ← Requires: B

Level 3 (Intermediate):
  □ [Concept F] ← Requires: C, D
  □ [Concept G] ← Requires: D, E

Level 4 (Advanced):
  □ [Concept H] ← Requires: F, G
  □ [Concept I] ← Requires: G

DIAGNOSTIC APPROACH:
  1. Test understanding at Level 3+
  2. If gaps found, trace back to prerequisites
  3. Start remediation at the earliest gap in the chain
  4. Don't skip ahead — build foundations first
```

## Gap Identification Methods

### Diagnostic Assessment Design

```
DIAGNOSTIC ASSESSMENT TEMPLATE:

PURPOSE: Identify specific knowledge gaps before starting learning plan

STRUCTURE:
  Section 1: Foundational concepts (5 questions)
    - If <60% correct: Start at Level 1
    - Tests: Definitions, basic recall, simple recognition

  Section 2: Core understanding (5 questions)
    - If <60% correct: Start at Level 2
    - Tests: Explanation, comparison, basic application

  Section 3: Application (5 questions)
    - If <60% correct: Start at Level 3
    - Tests: Problem-solving, scenario analysis, transfer

  Section 4: Advanced (5 questions)
    - If <60% correct: Start at Level 4
    - Tests: Synthesis, evaluation, novel situations

QUESTION TYPES:
  - Explain in your own words: [concept]
  - Given [scenario], what would happen if [variable changed]?
  - Compare and contrast: [concept A] vs [concept B]
  - Solve: [problem requiring application]
  - What's wrong with this: [flawed example]
```

### The Feynman Technique for Gap Detection

```
FEYNMAN TECHNIQUE:

STEP 1: Choose a concept you think you understand
STEP 2: Explain it as if teaching a 12-year-old
  - Use simple language
  - No jargon
  - Include examples

STEP 3: Identify where you get stuck
  - Where do you reach for jargon?
  - Where does your explanation get vague?
  - Where can't you provide a clear example?

  → THESE ARE YOUR GAPS

STEP 4: Go back to source material
  - Study specifically the areas where you struggled
  - Don't re-read everything — target the gaps

STEP 5: Simplify and retry
  - Re-explain using analogies
  - If you can explain it simply, you understand it
  - If you can't, repeat steps 3-4

TRACKING FORMAT:
  Concept: _______________
  Explanation attempt: [Your explanation]
  Stuck points: [Where it broke down]
  Gap identified: [What you need to learn]
  Source to study: [Specific chapter, video, article]
  Re-explanation: [After studying]
  Confidence: [ ] Low  [ ] Medium  [ ] High
```

## Learning Plan Design

### Targeted Remediation Plan

```
LEARNING PLAN: [Goal]

CURRENT STATE: [Assessment results summary]
TARGET STATE: [Desired competency level]
TIMELINE: [Weeks/months]
WEEKLY TIME BUDGET: [Hours]

PHASE 1: FOUNDATIONS (Weeks 1-N)
  Gap: [Specific knowledge gap]
  Resources:
    - [Resource 1] — Estimated time: [X hours]
    - [Resource 2] — Estimated time: [X hours]
  Practice:
    - [Exercise or application activity]
  Milestone: [How you'll know you've closed this gap]

PHASE 2: CORE SKILLS (Weeks N-M)
  Gap: [Specific knowledge gap]
  Resources:
    - [Resource 1] — Estimated time: [X hours]
    - [Resource 2] — Estimated time: [X hours]
  Practice:
    - [Exercise or application activity]
  Milestone: [How you'll know you've closed this gap]

PHASE 3: APPLICATION (Weeks M-P)
  Gap: [Specific knowledge gap]
  Resources:
    - [Resource 1] — Estimated time: [X hours]
  Practice:
    - [Project or real-world application]
  Milestone: [Demonstrable competency]

WEEKLY SCHEDULE:
  Day       | Activity                    | Duration
  Monday    | New material (reading/video) | 1 hour
  Tuesday   | Practice problems            | 45 min
  Wednesday | Spaced review (flashcards)   | 30 min
  Thursday  | New material                 | 1 hour
  Friday    | Application project          | 1 hour
  Weekend   | Weekly review + assessment   | 30 min
```

## Spaced Repetition System

### Optimal Review Schedule

```
SPACED REPETITION INTERVALS:

First learning:     Day 0
First review:       Day 1   (24 hours later)
Second review:      Day 3   (2 days after first review)
Third review:       Day 7   (4 days after second review)
Fourth review:      Day 14  (7 days after third review)
Fifth review:       Day 30  (16 days after fourth review)
Sixth review:       Day 60  (30 days after fifth review)
Maintenance:        Every 90 days thereafter

ADJUSTMENT RULES:
  If you recalled easily:     Move to next interval
  If you recalled with effort: Repeat at current interval
  If you failed to recall:    Reset to Day 1 interval

CARD DESIGN PRINCIPLES:
  - One concept per card (atomic)
  - Question on front, answer on back
  - Include context/example on back
  - Use images where possible
  - Avoid yes/no questions — require recall
```

### Active Recall Techniques

| Technique | How It Works | Best For | Effort Level |
|-----------|-------------|----------|-------------|
| **Flashcards** | Question → attempt recall → check | Facts, definitions, formulas | Low-Medium |
| **Practice problems** | Solve without looking at solution | Application, procedures | Medium |
| **Free recall** | Close book, write everything you know | Comprehensive review | Medium-High |
| **Interleaving** | Mix topics in practice (don't block) | Discrimination, transfer | Medium |
| **Elaborative interrogation** | Ask "why?" and "how?" for each fact | Deep understanding | Medium |
| **Self-testing** | Create and take your own quizzes | All types of knowledge | Medium |
| **Teaching others** | Explain concept to someone else | Deep mastery verification | High |

## Progress Tracking

### Weekly Progress Template

```
WEEKLY LEARNING REVIEW

Week: ___ of ___
Date: __________

HOURS INVESTED:
  Planned: ___ hours
  Actual: ___ hours

TOPICS COVERED:
  □ [Topic 1] — Confidence: [ ] Low [ ] Med [ ] High
  □ [Topic 2] — Confidence: [ ] Low [ ] Med [ ] High
  □ [Topic 3] — Confidence: [ ] Low [ ] Med [ ] High

ASSESSMENT RESULTS:
  Quiz/test score: ___/___
  Practice problem accuracy: ___%
  Concepts recalled via free recall: ___/___

WHAT WENT WELL:
  - [Insight or breakthrough]

WHAT WAS DIFFICULT:
  - [Struggle point]
  - Gap identified: [Specific concept]

ADJUSTMENTS FOR NEXT WEEK:
  - [Change to plan based on this week's learning]

SPACED REVIEW DUE:
  □ [Topic from Week N-1] — Review due: [Date]
  □ [Topic from Week N-3] — Review due: [Date]
```

### Mastery Criteria

| Level | Evidence Required | Assessment Method |
|-------|------------------|-------------------|
| **Awareness** | Can define term and recognize it in context | Multiple choice, matching |
| **Understanding** | Can explain concept in own words with examples | Short answer, Feynman test |
| **Application** | Can solve novel problems using the concept | Practice problems, case studies |
| **Mastery** | Can teach others and combine with other concepts | Teaching exercise, project |

## Learning Science Principles

### Evidence-Based Strategies

```
HIGH-IMPACT LEARNING STRATEGIES:

1. RETRIEVAL PRACTICE (Effect: +0.7 SD)
   Don't just re-read — test yourself
   Implementation: Flashcards, practice quizzes, free recall

2. SPACED PRACTICE (Effect: +0.6 SD)
   Distribute learning over time, don't cram
   Implementation: Review schedule, interleaved practice

3. ELABORATION (Effect: +0.5 SD)
   Connect new info to existing knowledge
   Implementation: "How does this relate to...?" questions

4. INTERLEAVING (Effect: +0.4 SD)
   Mix different topics/problem types in practice
   Implementation: Shuffle practice problems from multiple chapters

5. CONCRETE EXAMPLES (Effect: +0.4 SD)
   Connect abstract concepts to specific instances
   Implementation: Generate 2-3 real examples for each concept

6. DUAL CODING (Effect: +0.3 SD)
   Combine verbal and visual representations
   Implementation: Draw diagrams, create concept maps

LOW-IMPACT STRATEGIES (AVOID):
  ✗ Re-reading (passive, creates illusion of learning)
  ✗ Highlighting (passive, doesn't require processing)
  ✗ Summarizing without retrieval (only slightly better)
  ✗ Massed practice / cramming (poor long-term retention)
```

## See Also

- [Course Material Creator](../course-material-creator/SKILL.md)
- [Career Path Planner](../career-path-planner/SKILL.md)
- [Literature Review Planner](../literature-review-planner/SKILL.md)
