---
name: training-design
last_reviewed: 2026-09-06
group: Teaching and planning
description: >-
  Design enterprise training: needs analysis, curriculum structure, blended delivery and
  evaluation. Use when developing corporate workshops, course modules, or adult learning.
---

# training-design

## Core Philosophy
Corporate and enterprise training programs fail when they are treated as performative "edutainment": subjecting employees to 4-hour slide presentations where participants passively nod, eat catered lunches, fill out a polite survey, and immediately return to their desks without changing a single work behavior. Professional training design is an exercise in **behavioral and systems engineering**: applying the **ADDIE model** and **Kirkpatrick's Four Levels of Evaluation** to translate business performance bottlenecks into measurable learning objectives, experiential practice simulations, and quantifiable business ROI.

---

## 4-Step Enterprise Training Architecture

### Step 1: Training Needs Analysis (TNA) & Gap Math
1. **The Performance Gap Formula**:
   $$\text{Performance Gap} = \text{Target Operational Standard} - \text{Current Metric}$$
   - *Example*: Production outages caused by unauthorized database schema migrations are at 4/month; target standard is 0/month.
2. **Is Training the Right Solution? (Mager & Pipe Model)**:
   - Ask: *"Could the employees perform the task if their lives depended on it?"*
   - If YES $\to$ The problem is not a skill deficiency; it is an incentive, tooling, or cultural bottleneck (do NOT build training).
   - If NO $\to$ Build targeted training.

### Step 2: Curriculum Architecture (ADDIE Framework)
1. **Analysis**: Profile learner technical baselines, constraints, and operational context.
2. **Design**: Establish Bloom-aligned terminal learning objectives (TLOs):
   - *Formula*: *"Given [Condition], the learner will [Measurable Action] according to [Performance Standard]."*
3. **Development**: Build 80% hands-on experiential lab exercises and 20% framing lecture.
4. **Implementation**: Deliver via blended delivery (asynchronous pre-work sandbox + synchronous live workshop).
5. **Evaluation**: Measure behavioral change and business impact.

### Step 3: Kirkpatrick's 4 Levels of Training Evaluation
1. **Level 1: Reaction (Smile Sheets)**:
   - Did learners find the training relevant and engaging? (Target: $\ge 85\%$ positive sentiment).
2. **Level 2: Learning (Knowledge Acquisition)**:
   - Did learners acquire the knowledge/skills? Measured via pre-test vs post-test diagnostic assessments.
3. **Level 3: Behavior (Application on the Job)**:
   - Are employees applying the new skill in their daily workflow 30-60 days post-training? (Audited via peer review and telemetry).
4. **Level 4: Results (Business ROI)**:
   $$\text{Training ROI} = \frac{\text{Net Financial Benefits} - \text{Total Training Costs}}{\text{Total Training Costs}} \times 100$$
   - Reductions in production incident downtime, support ticket volume, or customer churn.

### Step 4: Blended Delivery & Simulation Labs
1. **The 70-20-10 Learning Framework**:
   - 10% Formal Coursework (Live conceptual lectures).
   - 20% Social Learning (Peer code reviews, group debugging sessions).
   - 70% Experiential Learning (Live sandbox environment breaks and real-world disaster simulations).

---

## Deliverable Format: Enterprise Training Curriculum Blueprint

```markdown
# Training Blueprint: Production Cloud Incident Triage & Reliability Engineering
- **Target Audience**: 120 Backend Software Engineers
- **Business Target**: Reduce Mean Time to Resolution (MTTR) for Tier 1 incidents from 45 min to 15 min.

### Modular Curriculum Schedule:

| Module | Delivery Mode | Duration | Learning Objective & Hands-On Deliverable |
|---|---|---|---|
| **Module 1: Telemetry & Tracing** | Async Sandbox | 2 Hours | Instrument an un-traced microservice with OpenTelemetry distributed trace spans. |
| **Module 2: Chaos Engineering** | Synchronous Lab | 4 Hours | Given an active simulated memory leak and network partition, diagnose root cause within 15 minutes using Grafana/Prometheus. |
| **Module 3: Runbook Automation** | Synchronous Lab | 3 Hours | Write and execute an automated rollback runbook that resolves a split-brain Redis cluster without human data loss. |
| **Module 4: Post-Mortem Facilitation** | Peer Workshop | 2 Hours | Author a blameless post-mortem for a simulated Sev-1 incident adhering to company SLA standards. |

### Evaluation Architecture:
- **Level 2**: Mandatory sandbox qualification exam (Must score $\ge 85\%$ on incident resolution).
- **Level 3**: 60-day telemetry audit of incident triage logs.
- **Level 4**: Track company MTTR across Q3 and Q4.
```

---

## Worked Example: Slashing Phishing Susceptibility via Behavioral Simulation

- **Problem**: A Fortune 500 company suffered a 28% failure rate on enterprise phishing simulation tests despite mandating a yearly 45-minute slide-based compliance video.
- **Intervention**:
  1. Scrapped the generic 45-minute annual video.
  2. Implemented the ADDIE model: deployed simulated, context-specific phishing emails directly to employee inboxes.
  3. Clicking a simulated link immediately routed the employee to a 2-minute micro-training highlighting the exact specific visual tells (spoofed domain, urgent emotional tone) in the email they had just clicked.
- **Outcome**: Phishing susceptibility plummeted from 28% to 1.8% within 90 days.

---

## Verification Checklist

- [ ] Training Needs Analysis confirms the bottleneck is a genuine skill deficiency, not tooling or incentives.
- [ ] Learning objectives formulated with observable, measurable behavioral verbs.
- [ ] Minimum 70% of synchronous time dedicated to hands-on simulated exercises.
- [ ] Evaluation strategy covers Kirkpatrick Levels 2, 3, and 4 (not just smile sheets).
- [ ] Pre-work and post-training reinforcement workflows established.

---

## Anti-Patterns

- **Death by PowerPoint**: Lecturing adults for 6 hours straight without providing hands-on exercises or active participation.
- **Stopping at Level 1 Evaluation**: Measuring training success solely by whether participants liked the instructor and lunch on the post-course survey.
- **Training as a Band-Aid for Bad Systems**: Mandating training for employees because software tooling is confusing, broken, or misconfigured.
