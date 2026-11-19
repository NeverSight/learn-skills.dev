---
name: assessment-design
last_reviewed: 2026-09-06
group: Assessment
description: >-
  Build the assessment: questions across Bloom's levels, answer keys, grading rubrics and
  difficulty calibration. Use when developing grading rubrics, Bloom's taxonomy tests, or
  evaluation.
---

# assessment-design

## Core Philosophy
An assessment is an instrument of measurement, and like any scientific instrument, it must possess both **validity** (measuring what it purports to measure) and **reliability** (producing consistent, reproducible results). Poorly designed exams measure test-taking endurance, trick-question decoding, or rote memorization of trivia rather than genuine conceptual mastery. Professional assessment design aligns with Bloom's Revised Taxonomy, balances cognitive depth across tiers, eliminates distractor ambiguity, and provides calibrated analytic rubrics that ensure two independent graders award the exact same score to the same work.

---

## 4-Step Assessment Design Architecture

### Step 1: Bloom's Revised Taxonomy Cognitive Distribution
1. **The 6 Cognitive Tiers**:
   - **Level 1 (Remember)**: Recall facts, terms, definitions (e.g. *Define polymorphism*).
   - **Level 2 (Understand)**: Explain ideas, translate, summarize (e.g. *Explain why immutability prevents race conditions*).
   - **Level 3 (Apply)**: Use information in new situations (e.g. *Calculate the subnet mask for 50 hosts*).
   - **Level 4 (Analyze)**: Draw connections, distinguish causes, critique (e.g. *Profile two sorting algorithms and explain when QuickSort degrades to $O(n^2)$*).
   - **Level 5 (Evaluate)**: Justify a stand or decision (e.g. *Evaluate whether to use SQL or NoSQL for a financial ledger*).
   - **Level 6 (Create)**: Assemble elements into a new pattern/structure (e.g. *Design a fault-tolerant microservice architecture*).
2. **Balanced Target Blueprint**:
   - Introductory Course: 30% Levels 1-2, 50% Levels 3-4, 20% Levels 5-6.
   - Advanced / Capstone Course: 10% Levels 1-2, 40% Levels 3-4, 50% Levels 5-6.

### Step 2: Multiple-Choice Question (MCQ) Psychometrics
1. **Item Difficulty ($p$-value)**:
   $$p = \frac{\text{Number of Correct Responses}}{\text{Total Test Takers}}$$
   - Calibrated target: $0.40 \le p \le 0.75$. Items with $p > 0.90$ are too easy; $p < 0.25$ indicate defective items or confusing wording.
2. **Discrimination Index ($D$)**:
   $$D = P_{\text{Upper 27\%}} - P_{\text{Lower 27\%}}$$
   - $D \ge 0.40$: Excellent item discrimination.
   - $D < 0.20$: Flawed item; top students missed it at the same rate as bottom students.
3. **Distractor Engineering**:
   - Every incorrect option (distractor) must represent a documented common misconception, not an absurd joke or grammatical misfit.

### Step 3: Analytic vs Holistic Rubric Formulation
1. **Holistic Rubrics**: Single global grade score (1-5). Fast to grade, but low feedback utility and high inter-rater variance.
2. **Analytic Rubrics (The Gold Standard)**:
   - Multi-dimensional grid: Criteria along rows, Performance Levels along columns with explicit, observable behavioral descriptions for each cell.

### Step 4: Difficulty Calibration & Time Audits
1. **The 3x Rule for Exam Duration**:
   $$\text{Allowed Student Exam Time} \ge 3 \times \text{Instructor Completion Time}$$
   - If the professor or author takes 20 minutes to complete the test with flawless accuracy, students require 60 minutes minimum.

---

## Deliverable Format: Analytic Grading Rubric for System Architecture Design

| Criterion (Weight) | Exemplary (4 pts) | Proficient (3 pts) | Developing (2 pts) | Inadequate (1 pt) |
|---|---|---|---|---|
| **Data Consistency & Transactions (25%)** | Correctly implements distributed consensus (e.g. Raft) or two-phase commit with detailed failure rollback mechanisms. | Implements ACID transactions within a single database but overlooks split-brain edge cases. | Mentions consistency loosely; relies on eventual consistency without reconciling read-after-write anomalies. | Ignores concurrent write race conditions entirely; data corruption likely. |
| **Fault Tolerance & Redundancy (25%)** | Multi-region active-passive failover with automated health probes and zero-loss read replica promotion. | Single-region high availability with load-balanced nodes; manual failover recovery. | Single points of failure identified but unresolved; backup strategy vague. | Monolithic architecture with zero redundancy; crashes result in unrecoverable downtime. |
| **Scalability & Bottlenecks (25%)** | Quantifies throughput math ($QPS$, network bandwidth, disk IOPS) and applies sharding/caching appropriately. | Implements caching (Redis) and database read replicas, but does not calculate connection pool limits. | Architecture scales vertically only; no horizontal sharding or partition keys defined. | System fails under load; database performs unbounded full-table scans. |
| **Security & Authorization (25%)** | Zero-trust architecture: mutual TLS, least-privilege IAM roles, encrypted at-rest and in-transit data pipelines. | Standard JWT authentication with HTTPS; basic role-based access control (RBAC). | Passwords stored in plain text or basic SHA-256 without salt; open firewall ingress rules. | Zero authentication or access controls implemented. |

---

## Worked Example: Redesigning a Broken University CS Midterm Question

- **Original Flawed Question**: "Which of the following is true about Java garbage collection? A) It runs every second. B) It frees memory automatically. C) It is written in Python. D) It never causes pauses."
  - *Psychometrics*: $p = 0.98$ (98% got it right, testing trivial recall; $D = 0.04$, zero discrimination).
- **Redesigned Bloom Level 4 Item**:
  - *"An enterprise service experiences 800ms Stop-The-World latency spikes every 15 minutes during peak traffic. Memory graphs show high Young-Generation promotion rates of short-lived objects. Which garbage collector reconfiguration directly mitigates this bottleneck?"*
  - Distractors mapped to real GC flags (`-XX:NewRatio`, `-XX:SurvivorRatio`, G1GC pause time targets).
  - *Result*: $p = 0.58$, $D = 0.48$. Cleanly separated deep systems comprehension from surface memorization.

---

## Verification Checklist

- [ ] Exam blueprint maps questions explicitly across Bloom's Taxonomy levels.
- [ ] MCQ stems are clear, affirmative, and contain the central problem without gratuitous filler.
- [ ] Distractors represent genuine, documented student misconceptions.
- [ ] Analytic rubrics provide distinct, observable performance benchmarks per score level.
- [ ] Total exam time adheres to the $\ge 3\times$ instructor benchmark rule.

---

## Anti-Patterns

- **"All of the Above" / "None of the Above" Options**: Allows students to eliminate options by partial knowledge without true mastery, undermining item discrimination.
- **Negative Stems ("Which of the following is NOT...")**: Increases cognitive reading load rather than testing domain competence.
- **Subjective "I Know It When I See It" Grading**: Grading essay or code submissions without an analytic rubric, causing severe grade inconsistency across students.
