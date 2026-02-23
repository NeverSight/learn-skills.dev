---
name: q-educator
description: Course content development skill. Produces lecture outlines, demo outlines, student emails, assignment prompts, and per-group feedback using an interview-driven, projects-first teaching philosophy with domain-specific analogies. Use when developing or iterating on university course materials.
---

# Q-Educator

Q-Educator encodes a teaching philosophy and facilitation workflow for graduate-level, projects-first courses. It produces course materials through an interview-driven process that prioritizes student judgment, transparent reasoning, and domain-specific analogies.

## When to Use

Use this skill when the instructor needs to develop lecture outlines for a new or existing course week, create demo outlines for live project pipeline walkthroughs, draft follow-up emails to students after class sessions, design assignment prompts with scaffolded sections, write per-group feedback documents on student submissions, or iterate on any of the above based on instructor direction.

## Teaching Philosophy

The following six principles govern all content produced by this skill.

### 1. Projects-First, Not Lectures-First

Students learn by executing full analytical workflows, not by absorbing lectures. Class time prioritizes short concept modules, structured labs, and guided interpretation over extended instructor monologues.

### 2. Judgment Over Polish

The goal is not polished AI output. The goal is developing students' scholarly judgment: what to analyze, which visualization tells the story, whether a finding overclaims. Tools handle mechanics. Students handle reasoning.

### 3. Instructor as Methodological Arbiter

The instructor does not transmit content. The instructor provides exemplars, detailed guidance, and diagnostic feedback that shape students' analytical judgment while preserving student ownership of the work.

### 4. Repeat-Exposure Transfer

Students encounter the same analytic logic (cleaning, operationalization, analysis, interpretation, ethics) across multiple projects in different substantive domains. This reinforces transfer rather than rote learning.

### 5. Transparent Reasoning Over Correct Answers

Students must justify analytical choices, acknowledge tradeoffs and limitations, and avoid overclaiming. Documenting decisions (why this method, why this scope, what was tried and rejected) matters more than arriving at "the right answer."

### 6. Domain-Specific Analogies

All analogies must come from the course's subject domain. For a sport course, use sport analogies. For a business course, use business analogies. Generic tech metaphors should never appear when a richer domain-native analogy exists.

## Interview-Driven Planning

Before drafting any content, always conduct an interview with the instructor. Do not assume goals, constraints, or tone. Ask first, then draft.

The interview should proceed through six questions in this order. First, ask what the goal is for this week or module: what should students walk away knowing or being able to do? Second, ask what happened last time: what worked, what did not, and what feedback came from students. Third, ask about the class structure: total time, how to split it between lecture, demo, and hands-on work, and any hard stops. Fourth, ask about the dataset or project context: which data are students working with this week. Fifth, ask about specific constraints: topics to avoid, things to emphasize, pacing concerns, and deliverables. Sixth, ask about tone: conversational, formal, urgent, or encouraging.

Only after the interview is complete should content generation begin.

## Content Development Pipeline

The standard pipeline for a single class session produces three deliverables, always in this order:

```
1. Lecture Outline  ->  2. Demo Outline  ->  3. Follow-Up Email
         ^                                         |
         +------------ Iterative Refinement -------+
```

After each deliverable, pause for instructor review. Iterate until approved before moving to the next.

## Deliverable 1: Lecture Outline

### Structure

```markdown
# Week [N] Lecture Outline: [Topic]
**[Course Code] | [Date]**

---

## Pre-Class Note
> [Context for instructor: what happened last week, student readiness assumptions]

---

## Part 1: [Concept Block] (~[time] min)

### [Analogy or Scenario Title]
> "[Vivid scenario or analogy in the instructor's voice, always domain-specific]"

### [Framework / Comparison Table]
| [Without Tool/Concept] | [With Tool/Concept]   |
| ---------------------- | --------------------- |
| [Concrete comparison]  | [Concrete comparison] |

Key Insight:
> "[One-sentence takeaway]"

### Q&A Pause (~3 min)
- "[Discussion prompt tied to students' own experience]"

---
[Repeat for each concept block]

## Demo Preview (~5 min)
> "[Transition previewing the demo and what to watch for]"
```

### Design Rules

Every section must end with a Q&A pause. Never go more than 15 minutes without one. All analogies must be domain-specific, drawn from the course's subject area. Key insights should fit in one sentence; if they cannot, they are not clear enough. Comparison tables are required to show "without" versus "with" for every new concept. The instructor's spoken voice should be evident throughout; write as the instructor would speak, not as a textbook reads.

## Deliverable 2: Demo Outline

### Structure

```markdown
# Week [N] Demo Outline: [Title]
**[Course Code] | [Date]**

---

## Overview
| Segment                 | Time        | What Students See            |
| ----------------------- | ----------- | ---------------------------- |
| Demo (instructor-led)   | ~[time] min | Full pipeline: [step list]   |
| Student Experimentation | ~[time] min | Hands-on with their own data |

**Dataset:** [Name]
**Tool:** [Name]

---

## Step [N]: [Step Title] (~[time] min)

### What to Say
> "[Framing statement in instructor's voice]"

### What to Show
1. [Concrete action]
2. [Exact prompt or command to demo]
3. [Walk through output]

### Key Teaching Moment
> "[Domain-specific analogy connecting the tool action to the scholarly skill]"

### Quick Check (~1 min)
- "[Brief question to gauge understanding]"

---
[Repeat for each pipeline step]

## Student Experimentation (~[time] min)

### Suggested Prompts to Try
1. [Starter prompt]
2. [Starter prompt]

### Instructor Role During Experimentation
- Rotate through groups
- Ask: "What did the tool give you? What would you change? Why?"
- Reinforce: "Your judgment matters."
```

### Design Rules

Always start with plan mode so the project is scoped before execution begins. Each step should include exactly one Key Teaching Moment that connects the tool action to the scholarly judgment being developed. Show exact prompts so students can replicate what they see. Student experimentation time is non-negotiable; always protect it. The standard pipeline order is: Plan, Research Questions, Literature, Analyze, Visualize, Interpret, Draft, Present. Presentation is always the last step.

## Deliverable 3: Follow-Up Email

### Style Rules

The email must be written in conversational paragraph form with no headers, no bullet lists, and no numbered lists. It should read as the instructor would speak: warm, direct, and encouraging. The structure, rendered entirely in flowing paragraphs, should open with a recap of what was covered, summarize the pipeline or concepts in plain language, state the deliverable and next steps, weave starter prompts or resources into the prose rather than listing them, include logistical reminders such as breaks and deadlines, and close with encouragement and the instructor's sign-off.

## Deliverable 4: Assignment Prompt

### Structure

```markdown
# [Assignment Title]
**Course:** [Code and Title]
**Due:** [Date and time]
**Submission:** [Method, file naming, CC instructions]

---

## 1. Research Questions and Significance
For each RQ: The Question, The Context, Why It Matters

## 2. Dataset Selection and Justification
Which data, why, which specific files

## 3. Preliminary Variable Operationalization
| Construct | Operational Definition | Data Source / Indicator |
| --------- | ---------------------- | ----------------------- |

## 4. Proposed Analyses
| Analysis Type | Description | RQ Addressed |
| ------------- | ----------- | ------------ |

## 5. Limitations and Potential Issues
At least 2-3, honest self-assessment

## 6. Ethical Considerations
Privacy, harm, bias, with specific sub-prompts for each

## 7. Group Role Assignments
| Role | Member | Primary Responsibilities |
| ---- | ------ | ------------------------ |

## 8. Data Visualization Plan
Goal, description, design rationale, verification methods, brief interpretation

## 9. AI-Assisted Work Documentation
Tools used, verification methods (code explanation, output validation,
iterative refinement counts), learning reflection

## Submission Checklist
- [ ] Checkboxes for each section completed
```

### Design Rules

Assignment prompts are planning documents, not final reports. Expectations are for reasonable preliminary thinking, not polished answers. Every section must include explicit sub-prompts so students never wonder what to write. Tables should be used for structured responses such as operationalization, analyses, and roles. AI documentation is mandatory: students must record which tools they used, how they verified outputs, and how many iterations they needed. Submission logistics must be explicit, including file naming conventions, email instructions, CC requirements, and deadlines.

## Deliverable 5: Per-Group Feedback

### Structure

```markdown
# Week [N] Feedback: [Group Name]
**Reviewer:** [Name]
**Date:** [Date]

---

## Overall Assessment
[2-3 sentence summary: what is strong, what needs work]

---

## [N]. [Section Title, mirrors assignment structure]

### Strengths
- [Specific, concrete positives]

### Area for Improvement: [Named Issue]
The Issue:
- [Clear articulation of the gap]

Suggestions for Revision:
- Option A: [Concrete suggestion]
- Option B: [Alternative approach]
- Option C: [Hybrid if applicable]

### Next Steps
- [Actionable items with specifics]

---
[Repeat for each section of the assignment]

## Summary: Moving Forward

During Class:
- [What to do in today's session]

Questions to Bring to Consultation:
- [Specific questions to discuss with the instructor]

This Week:
- [Immediate action items]

Next Week:
- [Upcoming deliverables and priorities]

---
Overall: [One-sentence encouragement and direction]
```

### Design Rules

Feedback should mirror the assignment structure so that every section the student submitted receives a corresponding feedback section. Lead with strengths before improvements. Name each issue explicitly, such as "Area for Improvement: RQ-Context Alignment," rather than offering vague criticism. Provide multiple options for revision so students have choices rather than commands. Next steps should include a concrete timeline distinguishing between "during class," "this week," and "next week." When suggesting additions to operationalization or analysis tables, use the same table format the assignment uses. Close with encouragement that acknowledges strengths and provides clear direction.

## Workflow Summary

```
+----------------------------------------------------------+
|                    Q-EDUCATOR PIPELINE                    |
|                                                          |
|  +-----------+                                           |
|  | INTERVIEW | <- Always start here                     |
|  | Instructor|                                           |
|  +-----+-----+                                           |
|        |                                                 |
|        v                                                 |
|  +----------+  +----------+  +----------+               |
|  | Lecture   |->| Demo     |->| Email    |               |
|  | Outline   |  | Outline  |  |          |               |
|  +----------+  +----------+  +----------+               |
|        |                                                 |
|        v                                                 |
|  +----------+  +----------+                              |
|  |Assignment|->| Feedback |                              |
|  | Prompt   |  | Per Group|                              |
|  +----------+  +----------+                              |
|                                                          |
|  Each step: Draft -> Instructor Review -> Iterate -> Next|
+----------------------------------------------------------+
```

## Key Phrases

These phrases capture the teaching philosophy and should appear naturally in generated content where appropriate.

"Skills replace repetition, not judgment." This phrase reinforces that tools automate the mechanical, not the scholarly.

"Your taste matters most." This phrase reminds students that selecting, curating, and judging outputs is the core skill.

"The AI handles the how. You handle the why." This phrase draws the line between tool execution and scholarly reasoning.

"Iterate, do not accept." This phrase establishes that first drafts from any source, AI or otherwise, are starting points.

"First drafts from AI are starting points. Your critical eye is what makes it research." This phrase connects iteration to the scholarly standard.

"Plan, execute, review, revise. That cycle is the process." This phrase names the workflow students should internalize across every project.

## Reference Files

- references/lecture_example.md: Example lecture outline with domain-specific analogies
- references/demo_example.md: Example demo outline with pipeline walkthrough
- references/email_example.md: Example follow-up email in conversational style
- references/assignment_example.md: Example assignment prompt with full scaffold
- references/feedback_example.md: Example per-group feedback document
