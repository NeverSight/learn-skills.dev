---
name: learning-roadmap
last_reviewed: 2026-09-06
group: Learning
description: >-
  Build the roadmap: skill tree, milestone checkpoints, ordered reading with difficulty ratings,
  and time estimates. Use when planning structured skill acquisition from beginner to mastery.
---

# learning-roadmap

## Core Philosophy
Learning a complex skill—whether it is distributed systems engineering, corporate finance, or machine learning—without a structured roadmap is like sailing across an ocean without a compass. Learners fall into the "tutorial purgatory" trap: endlessly following video courses, copying code, and feeling productive while remaining utterly incapable of independent problem-solving. A professional learning roadmap operates as a **Directed Acyclic Graph (DAG)** of competencies: decomposing domains into prerequisites, establishing measurable milestone projects, curating battle-tested primary literature, and pacing progression from Novice to Autonomous Practitioner.

---

## 4-Step Learning Roadmap Architecture

### Step 1: Competency Mapping & Prerequisite DAGs
1. **The Dreyfus Model Progression**:
   - **Novice**: Rule-based execution; zero context awareness.
   - **Advanced Beginner**: Recognizes recurring situational patterns.
   - **Competent**: Solves novel problems independently using conceptual frameworks.
   - **Proficient**: Intuitive grasp of edge cases and trade-offs.
   - **Expert**: Authoring new patterns, tools, or theory.
2. **Prerequisite Graph Dependency**:
   - Ensure foundational competencies are mastered before dependent abstractions are introduced (e.g. *Memory pointers & CPU cache lines* $\to$ *Concurreny & Locks* $\to$ *Lock-free queues*).

### Step 2: Tiered Curriculum & Primary Source Curation
1. **The 3-Tier Source Hierarchy**:
   - **Tier 1 (Foundational Texts)**: Canonical textbooks and seminal whitepapers (e.g. Tanenbaum, Hennessy & Patterson, Knuth).
   - **Tier 2 (Official References & Standards)**: Language specifications, official RFCs, production documentation.
   - **Tier 3 (Applied Practice)**: Open-source codebases, interactive sandboxes, production teardowns.
2. **Eliminating Low-Signal Noise**:
   - Ban generic 40-hour video bootcamps that hold the student's hand through copy-paste exercises.

### Step 3: Milestone Gate Projects (Proof of Competence)
1. **The "No-Tutorial" Project Rule**:
   - At each milestone gate, the learner must build a non-trivial project from scratch with zero boilerplate or video tutorials.
2. **The Defense Gate**:
   - A milestone is only passed when the project is tested, documented, and capable of handling edge cases.

### Step 4: Time Estimation & Pacing Models
1. **Deliberate Practice Hours Calculation**:
   $$T_{\text{mastery}} = \sum_{i=1}^{N} (\text{Theory Hours}_i \times 1.0 + \text{Build Hours}_i \times 2.5)$$
   - Allocate 70% of total learning time to hands-on building and debugging, and 30% to reading.

---

## Deliverable Format: 6-Month Systems Programming (Rust) Roadmap

```markdown
# Roadmap: Zero to Production Rust Systems Engineer

## Phase 1: Systems Foundations & Memory Model (Weeks 1-6)
- **Core Competencies**: Stack vs Heap, CPU Cache Locality, Pointer Arithmetic, OS Syscalls.
- **Reading / Resources**:
  - *The Rust Programming Language* (Klabnik & Nichols) — Chapters 1-10.
  - *Computer Systems: A Programmer's Perspective* (Bryant & O'Hallaron) — Ch 1-3.
- **Milestone Project 1**:
  - Build a custom CLI memory visualizer that parses `/proc/$PID/maps` on Linux and prints mapped virtual memory segments.

## Phase 2: Ownership, Lifetimes & Concurrency (Weeks 7-14)
- **Core Competencies**: Affine Type System, Borrow Checker, Unsafe Rust, Mutex/RwLock, Atomics.
- **Reading / Resources**:
  - *Rust for Rustaceans* (Jon Gjengset) — Chapters 1-5.
  - *The Rustonomicon* (Selected chapters on Unsafe & Invariants).
- **Milestone Project 2**:
  - Implement a thread-safe, lock-free MPSC (Multi-Producer Single-Consumer) bounded ring-buffer queue from scratch using atomic operations (`std::sync::atomic`).

## Phase 3: Network Systems & Asynchronous I/O (Weeks 15-24)
- **Core Competencies**: Epoll / Kqueue, Tokio Async Runtime, Reactor Pattern, Zero-Copy Parsing.
- **Reading / Resources**:
  - *Programming WebAssembly with Rust* or Tokio official architecture guides.
  - RFC 793 (TCP Specification fundamentals).
- **Milestone Project 3 (Capstone)**:
  - Build a mini Redis-compatible in-memory caching server supporting `GET`, `SET`, `EXPIRE`, and concurrent client connections, benchmarking $\ge 80,000\text{ QPS}$ under `redis-benchmark`.
```

---

## Worked Example: Accelerating a Junior Backend Developer into Distributed Systems

- **Problem**: A junior developer wanted to learn distributed systems but was jumping randomly between Kubernetes tutorials, Kafka documentation, and YouTube videos, retaining nothing.
- **Intervention**:
  1. Structured a 16-week rigorous curriculum focused on the MIT 6.824 Distributed Systems syllabus.
  2. Anchored the roadmap around 3 seminal papers (Google GFS, Raft Consensus, Amazon Dynamo).
  3. Established 4 hard programming milestones implemented in Go: Lab 1 (MapReduce), Lab 2 (Raft Leader Election & Log Replication), Lab 3 (Fault-Tolerant KV Store).
- **Outcome**: The developer successfully implemented a passing Raft consensus cluster and transitioned into a Senior Infrastructure Engineer role within 9 months.

---

## Verification Checklist

- [ ] Learning goals decomposed into a clear prerequisite dependency tree (DAG).
- [ ] Resources prioritized by authoritative canonical texts and primary documentation.
- [ ] 70/30 split enforced between hands-on project building and passive reading.
- [ ] Every milestone concludes with an independently built, unguided artifact.
- [ ] Realistic time budgets allocated based on weekly available study hours.

---

## Anti-Patterns

- **Tutorial Hell**: Watching 200 hours of video courses without writing a single line of original code or building an unguided project.
- **Skipping Prerequisites**: Trying to learn deep learning transformers before understanding linear algebra and multivariate calculus.
- **Unbounded Scope**: Declaring "I want to learn AI" without defining specific bounded outcomes (e.g. "Deploy fine-tuned LoRA weights for customer support triage").
