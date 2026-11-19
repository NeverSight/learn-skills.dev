---
name: mentoring
last_reviewed: 2026-09-06
group: Learning
description: >-
  Run a mentoring conversation using Socratic questioning and the GROW model, asking rather than
  telling. Use when structuring 1-on-1 mentorship, goal tracking, or career growth.
---

# mentoring

## Core Philosophy
Mentorship is not an advisory session where a senior person pontificates, tells war stories, and gives unsolicited advice. Telling someone what to do creates passive dependency and robs the mentee of agency and problem-solving growth. True mentorship is an exercise in **Socratic facilitation**: using active listening, incisive inquiry, and structured coaching frameworks like the **GROW Model** to help mentees clarify their own goals, diagnose their own behavioral bottlenecks, and commit to their own action plans.

---

## 4-Step Mentoring Architecture

### Step 1: The GROW Coaching Framework
1. **G — Goal (What do you want to achieve?)**:
   - Anchor on concrete, observable outcomes:
     - *"What does success look like 6 months from now in your engineering leadership role?"*
2. **R — Reality (Where are you right now?)**:
   - Strip emotional rationalization to assess objective facts:
     - *"What have you tried so far? What specific feedback did your team give during the last retro?"*
3. **O — Options (What could you do?)**:
   - Brainstorm divergent pathways without premature judgment:
     - *"If there were zero political risk, what are 3 different ways you could handle this underperforming tech lead?"*
4. **W — Will / Way Forward (What will you do?)**:
   - Lock in explicit, accountable micro-commitments:
     - *"Which of these 3 options will you execute first? By what day and time will that email be sent?"*

### Step 2: Socratic Inquiry & The 80/20 Listening Rule
1. **The 80/20 Rule**:
   - The mentee should be speaking 80% of the time; the mentor 20%.
2. **Open vs Closed Inquiries**:
   - *Closed / Prescriptive*: "Have you tried talking to Sarah?" (Suggests the solution).
   - *Open / Empowering*: "What conversation needs to happen between you and Sarah to unblock this project?"
3. **The Powerful Questioning Hierarchy**:
   - Shift from "Why" (prompts defensiveness and rationalization) to "What" and "How" (prompts reflection and action):
     - *Avoid*: "Why did you miss that deadline?"
     - *Use*: "What friction points emerged during the sprint that contributed to the delay?"

### Step 3: Psychological Safety & The Radical Candor Matrix
1. **Care Personally + Challenge Directly (Kim Scott)**:
   - Provide unvarnished, direct feedback on performance and behavior without attacking personal identity.
2. **Distinguishing Mentoring from Therapy**:
   - Mentoring focuses on professional competence, skill acquisition, career trajectory, and operational effectiveness. Maintain professional boundaries.

### Step 4: Accountability Architecture & Session Cadence
1. **The Bi-Weekly Cadence**:
   - 45-minute structured sessions every 2 weeks.
2. **The Mentee Ownership Protocol**:
   - The mentee is responsible for creating the agenda 24 hours in advance and emailing summary commitments within 24 hours post-session.

---

## Deliverable Format: Mentoring Session Dialogue & Action Plan

```markdown
# Mentoring Session Notes: Engineering Lead Transition
- **Date**: September 6, 2026
- **Mentee**: Alex (Senior SWE $\to$ Tech Lead)
- **Mentor**: Staff Systems Architect

### 1. Goal Check-In
- Alex wants to stop spending 30 hours a week coding so he can focus on architecture and unblocking junior engineers.

### 2. Current Reality Exploration
- *Mentor Question*: "What percentage of pull requests did you personally review this week?"
- *Alex*: "Almost 100%. I don't trust the PRs won't break production."
- *Mentor Reflection*: "So the bottleneck isn't team velocity; it's your personal fear of production incidents."

### 3. Divergent Options Explored
- Option A: Write comprehensive end-to-end integration test suites in CI.
- Option B: Institute a peer-review buddy system among mid-level engineers.
- Option C: Restrict personal reviews to critical architecture services only.

### 4. Committed Way Forward (Will)
- [ ] Alex will delegate PR approvals for Service B to Jordan by Tuesday.
- [ ] Alex will define and document automated CI linting rules by Thursday.
- [ ] Review progress at next session: September 20, 2026.
```

---

## Worked Example: Coaching a Senior Engineer Struggling with Cross-Functional Stakeholders

- **Context**: An exceptional senior infrastructure engineer was consistently passed over for promotion to Staff because product managers and design leads found him combative and dismissive during roadmapping.
- **Intervention**:
  1. Rather than lecturing him on corporate diplomacy, the mentor used Socratic roleplay: *"Assume you are the Product Director with a Q4 revenue target. Walk me through how you perceive this proposal to halt feature development for a 3-month database refactor."*
  2. The engineer experienced a visceral realization of the product team's commercial pressures.
  3. Formulated a communication bridge: packaging technical debt refactors into commercial reliability and SLA metrics.
- **Outcome**: The engineer successfully co-authored the subsequent quarterly roadmap with product leads and achieved promotion to Staff within two review cycles.

---

## Verification Checklist

- [ ] Mentee speaks at least 75-80% of total session time.
- [ ] Session follows the GROW structural framework.
- [ ] Mentor avoids prescribing answers; uses open-ended "What" and "How" questioning.
- [ ] Clear, time-bound action commitments recorded at the conclusion of every session.
- [ ] Mentee owns agenda creation and post-session follow-up documentation.

---

## Anti-Patterns

- **The Unsolicited Lecture**: Spending 40 minutes recounting "How I solved this back in 2018 at my previous company," leaving 5 minutes for the mentee.
- **Prescribing the Solution**: Telling the mentee exactly what email to write or what decision to make, fostering learned helplessness.
- **Vague Venting Sessions**: Allowing sessions to devolve into unstructured gripe sessions about company management without identifying actionable steps.
