---
name: interview-scheduler
description: Design and coordinate efficient interview processes with optimal panel composition, scheduling logistics, and candidate experience
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Interview Scheduler

> Design efficient interview processes with optimal panel composition, logical scheduling flow, and positive candidate experience.

## When to Use This Skill

- Setting up interview loops
- Coordinating panel schedules
- Designing interview stages
- Optimizing candidate experience
- Creating interview runbooks

## Methodology Foundation

Based on **structured interviewing best practices** and **candidate experience research**, combining:
- Stage-appropriate assessment
- Panel diversity requirements
- Time-to-hire optimization
- Candidate communication

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs interview stages | Final panel selection |
| Suggests panel composition | Scheduling conflicts |
| Creates question banks | Interview format (virtual/onsite) |
| Drafts communications | Offer timing |
| Identifies bottlenecks | Business priorities |

## Instructions

### Step 1: Define Interview Process

**Stage Design:**

| Stage | Purpose | Format | Duration |
|-------|---------|--------|----------|
| Phone Screen | Basic qualification | Remote | 30 min |
| Technical | Skills assessment | Remote/Onsite | 60 min |
| Hiring Manager | Fit and depth | Remote/Onsite | 45 min |
| Team/Culture | Team dynamics | Onsite | 45 min |
| Executive | Final approval | Onsite | 30 min |

**Process Variations:**

| Role Level | Stages | Total Time |
|------------|--------|------------|
| Individual Contributor | 3-4 | 3-4 hours |
| Manager | 4-5 | 5-6 hours |
| Director+ | 5-6 | 6-8 hours |
| Executive | 6+ | 8+ hours |

### Step 2: Panel Composition

**Panel Selection Criteria:**

| Role | Include | Rationale |
|------|---------|-----------|
| Hiring Manager | Always | Final decision authority |
| Direct Reports | If managing | Two-way assessment |
| Cross-functional | Recommended | Collaboration preview |
| Skip Level | Senior roles | Leadership alignment |
| HR/Recruiting | Screen/Final | Process consistency |

**Diversity Requirements:**
- Minimum 2 different perspectives on panel
- Gender diversity when possible
- Tenure diversity (new and experienced)
- Function diversity for cross-team roles

### Step 3: Schedule Optimization

**Scheduling Principles:**
1. Candidate availability first
2. Minimize calendar fragmentation
3. Allow buffer between interviews
4. End with positive impression interview
5. Same-day feedback when possible

**Optimal Day Structure:**

| Time | Interview | Why |
|------|-----------|-----|
| 9:00 | Technical | Fresh candidate, complex assessment |
| 10:30 | Break | Decompression |
| 11:00 | Hiring Manager | Core conversation |
| 12:00 | Lunch | Culture signal, informal |
| 1:00 | Team | Energy after lunch |
| 2:00 | Executive | Final impression |

### Step 4: Communication Templates

**Key Touchpoints:**
1. Interview confirmation
2. Day-before reminder
3. Day-of logistics
4. Post-interview next steps
5. Status updates

### Step 5: Feedback Coordination

**Debrief Structure:**
- Schedule within 24 hours of final interview
- Collect written feedback before meeting
- Structured discussion format
- Clear decision criteria
- Documented outcome

## Examples

### Example 1: Full Interview Loop Design

**Input:**
```
Design interview process for:
- Role: Senior Software Engineer
- Team: 5 engineers, 1 manager
- Timeline: Hire within 3 weeks
- Format: Hybrid (some remote, some onsite)
```

**Output:**
```
## Interview Process: Senior Software Engineer

### Process Overview

| Stage | Format | Duration | Interviewers | Turnaround |
|-------|--------|----------|--------------|------------|
| 1. Recruiter Screen | Phone | 30 min | Recruiter | Same day |
| 2. Technical Screen | Video | 60 min | Engineer | 24 hours |
| 3. Onsite Loop | In-person | 4 hours | Panel | 24 hours |
| 4. Debrief | Internal | 30 min | All | Same day |
| 5. Offer | Call | 15 min | HM + Recruiter | 48 hours |

**Total Timeline:** 10-14 business days

---

### Stage 1: Recruiter Screen

**Format:** Phone/Video call
**Duration:** 30 minutes
**Interviewer:** Recruiter

**Purpose:** Basic qualification, logistics, motivation

**Questions:**
1. Walk me through your background (5 min)
2. Why are you interested in this role? (3 min)
3. What's your ideal next role? (3 min)
4. Salary expectations? (2 min)
5. Timeline and availability? (2 min)
6. Candidate questions (10 min)

**Pass Criteria:**
- [ ] Meets minimum experience (5+ years)
- [ ] Reasonable salary alignment
- [ ] Available within timeline
- [ ] Genuine interest

---

### Stage 2: Technical Screen

**Format:** Video call with code sharing
**Duration:** 60 minutes
**Interviewer:** Senior Engineer (Sarah)

**Purpose:** Technical depth, problem-solving, code quality

**Structure:**
- 5 min: Introductions
- 10 min: Technical background discussion
- 35 min: Coding problem (medium difficulty)
- 10 min: System design discussion
- 5 min: Candidate questions

**Assessment Areas:**
| Area | Weight | Signals |
|------|--------|---------|
| Problem solving | 40% | Approach, communication |
| Code quality | 30% | Clean, tested, efficient |
| Technical depth | 20% | Language mastery, patterns |
| Collaboration | 10% | Receptive to hints, explains well |

**Pass Criteria:** Score 3+ on each area (1-5 scale)

---

### Stage 3: Onsite Loop (4 Hours)

**Panel Composition:**

| Time | Interview | Interviewer | Focus |
|------|-----------|-------------|-------|
| 9:00 | System Design | Tom (Staff Eng) | Architecture thinking |
| 10:00 | Code Review | Lisa (Senior Eng) | Code quality, feedback |
| 11:00 | Hiring Manager | Mike (Eng Manager) | Fit, growth, expectations |
| 12:00 | Lunch | Any team member | Culture, informal |
| 1:00 | Behavioral | Sarah (Senior Eng) | STAR examples |

**Detailed Interview Guides:**

#### System Design (Tom, 9:00-10:00)

**Question:** "Design a real-time notification system for a social media platform"

**Assessment:**
| Criterion | What to Look For |
|-----------|------------------|
| Requirements gathering | Clarifies scale, features |
| High-level design | Components, data flow |
| Deep dive | Storage, queuing, delivery |
| Trade-offs | Articulates decisions |
| Scale | Handles growth scenarios |

#### Code Review (Lisa, 10:00-11:00)

**Exercise:** Review prepared PR with intentional issues

**Assessment:**
| Criterion | What to Look For |
|-----------|------------------|
| Bug detection | Finds logic errors |
| Style feedback | Constructive, specific |
| Security awareness | Identifies vulnerabilities |
| Communication | Kind, actionable feedback |

#### Hiring Manager (Mike, 11:00-12:00)

**Topics:**
1. Career trajectory and goals
2. Management style preferences
3. Conflict resolution examples
4. Growth areas and learning
5. Questions about team/role

#### Behavioral (Sarah, 1:00-2:00)

**STAR Questions:**
1. "Tell me about a time you disagreed with a technical decision"
2. "Describe a project that failed and what you learned"
3. "Give an example of helping a teammate grow"
4. "Tell me about navigating ambiguity"

---

### Stage 4: Debrief

**Timing:** Same day, 4:00 PM
**Attendees:** All interviewers + Recruiter
**Format:** 30-minute structured discussion

**Agenda:**
| Time | Activity |
|------|----------|
| 0-5 | Written feedback review (pre-submitted) |
| 5-20 | Round-robin: Each interviewer shares (3 min each) |
| 20-25 | Discussion of concerns/questions |
| 25-30 | Decision: Strong Yes / Yes / No / Strong No |

**Decision Criteria:**
- Strong Yes from HM required
- No more than 1 "No" vote
- Technical interviewers must be Yes+

---

### Communication Templates

**Interview Confirmation:**
```
Subject: Interview Confirmation - Senior Software Engineer

Hi [Name],

We're excited to have you visit for your onsite interviews!

Date: [Date]
Time: 9:00 AM - 2:00 PM
Location: [Address]

Your schedule:
9:00 - System Design with Tom
10:00 - Code Review with Lisa
11:00 - Hiring Manager with Mike
12:00 - Lunch with the team
1:00 - Behavioral with Sarah

Please bring a laptop and valid ID. Parking validation available.

Reply to confirm or if you have any questions.

Best,
[Recruiter]
```

**Post-Interview Next Steps:**
```
Subject: Thank You & Next Steps

Hi [Name],

Thank you for spending time with our team today!

Our team will be debriefing this afternoon, and you'll hear
from us within 48 hours on next steps.

In the meantime, please don't hesitate to reach out with
any questions.

Best,
[Recruiter]
```
```

### Example 2: Quick Schedule Coordination

**Input:**
```
Need to schedule 4 interviews for tomorrow:
- Candidates: Alice, Bob, Carol
- Interviewers available: Mike (9-12), Sarah (10-2), Tom (11-4)
- Each interview: 45 minutes
```

**Output:**
```
## Optimized Interview Schedule

### Tomorrow's Schedule

| Time | Mike | Sarah | Tom |
|------|------|-------|-----|
| 9:00 | Alice | - | - |
| 10:00 | - | Bob | - |
| 11:00 | Carol | - | Alice |
| 12:00 | - | Carol | Bob |
| 1:00 | - | - | Carol |

### By Candidate

| Candidate | Interview 1 | Interview 2 |
|-----------|-------------|-------------|
| Alice | Mike @ 9:00 | Tom @ 11:00 |
| Bob | Sarah @ 10:00 | Tom @ 12:00 |
| Carol | Mike @ 11:00 | Sarah @ 12:00 |

### Notes

- Alice: 2-hour gap between interviews (offer coffee/workspace)
- Bob: Back-to-back, efficient
- Carol: Back-to-back, efficient

### Calendar Invites Needed

1. Alice + Mike: 9:00-9:45
2. Bob + Sarah: 10:00-10:45
3. Alice + Tom: 11:00-11:45
4. Carol + Mike: 11:00-11:45
5. Bob + Tom: 12:00-12:45
6. Carol + Sarah: 12:00-12:45
7. Carol + Tom: 1:00-1:45
```

## Skill Boundaries

### What This Skill Does Well
- Designing interview stages
- Optimizing panel composition
- Creating schedules
- Drafting communications

### What This Skill Cannot Do
- Access actual calendars
- Send invitations
- Know interviewer preferences
- Make hiring decisions

## Iteration Guide

**Follow-up Prompts:**
- "Create interview questions for [stage]"
- "Draft the candidate rejection email"
- "How should we handle scheduling conflict with [interviewer]?"
- "Design a scorecard for [interview type]"

## References

- Google re:Work Hiring Practices
- Lever Interview Scheduling Guide
- SHRM Interview Best Practices
- Greenhouse Structured Interviewing

## Related Skills

- `resume-screener` - Pre-interview evaluation
- `onboarding-guide` - Post-hire process
- `employee-support` - New hire support

## Skill Metadata

- **Domain**: HR Operations
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 30-60 min per role
- **Prerequisites**: Role requirements, panel availability
