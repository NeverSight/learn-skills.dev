---
name: software-forge
description: Use when starting a new project, adding a major feature to an existing system, or when unsure which skills to run and in what order. Supports macOS, iOS, web, full-stack, voice agent, and edge/IoT+ML projects.
---

# Project Orchestrator

## Overview
Universal project lifecycle skill. Classifies your project type, builds a phase plan, then walks through each phase sequentially — invoking existing skills where they exist and running inline design phases where they don't.

**The rule:** No project uses all phases. The router selects 7–18 phases based on what you're actually building.

**Announce at start:** "I'm using the orchestrate skill to guide this project through its lifecycle."

## When to Use
- Starting a new project from scratch (greenfield)
- Adding a major feature that changes architecture, data flow, or integrations
- Unsure which skills to invoke and in what order
- Starting work on a project type you haven't classified before

**When NOT to use:**
- Small bug fixes, typos, minor UI tweaks — just do the work
- Pure research or exploration — use Explore agent directly
- Single-file changes with clear requirements — use TDD directly
- You already know exactly which single skill applies (e.g., just need `/security-audit`)

## Mode Selection

Before doing anything else, ask ONE question:

> **How would you like to work?**
>
> **(A) Build** — Full-speed design and implementation. No teaching pauses.
> **(B) Learn** — Same build quality, plus I teach you software engineering concepts at every decision point. Tracks your growth across projects.

If the user selects **(B) Learn**, invoke the `engineering-mentor` skill using the Skill tool. Engineering Mentor wraps this orchestrator with an adaptive teaching layer — it handles everything from here. **Stop executing this skill** after invoking engineering-mentor.

If the user selects **(A) Build** or gives no preference, continue with Phase 0 below.

## How It Works
1. **Classify** — Ask what you're building, determine project type
2. **Route** — Select the phases that apply
3. **Read** — Load each phase file on demand before executing it
4. **Execute** — Walk through each phase sequentially
5. **Handoff** — Each phase produces a doc artifact; later phases build on earlier ones

All artifacts are saved to `docs/plans/`. If resuming mid-project, check which docs already exist to determine current phase.

---
## Phase 0: Project Classification
Ask ONE question: **"What are you building?"**

| Type | Indicators | Phase Count |
|------|-----------|-------------|
| **macOS App** | Desktop UI, SwiftUI, AppKit, menu bar app | 7–8 phases |
| **iOS Mobile App** | iPhone/iPad, SwiftUI, UIKit, App Store | 9–14 phases |
| **Web Frontend** | React, Vue, static site, no backend | 8–9 phases |
| **Full-Stack Web** | Frontend + database + API + auth | 14–15 phases |
| **Voice Agent** | LiveKit, telephony, STT/TTS, conversational AI | 13 phases |
| **Edge/IoT + ML** | Hardware devices, computer vision, ML pipeline, fleet management | 15–18 phases |

**Sub-classification questions (if needed):**
- Mobile/Web: "Does it have a backend?" — if yes, add full-stack phases
- Any type: "Does it integrate with external services?" — if yes, add resilience phase
- Any type: "Will this be deployed to cloud infrastructure you manage?" — if yes, add infrastructure phase
- Any type: "Is this a new project or adding to an existing system?" — if existing, add system assessment phase
- Any type with UI: "Does your project have state transitions, loading sequences, or interactions that would benefit from motion design?" — if yes, add motion design phase

### Route Table
| Phase | macOS | iOS | Web FE | Full-Stack | Voice | Edge/IoT+ML |
|-------|:-----:|:---:|:------:|:----------:|:-----:|:-----------:|
| 0.5 System Assessment | o | o | o | o | o | o |
| 1. Brainstorm | **x** | **x** | **x** | **x** | **x** | **x** |
| 2. Domain Model | | o | | **x** | **x** | **x** |
| 3. System Design + Security | | o | | **x** | **x** | **x** |
| 4. Resilience | | o | | **x** | **x** | **x** |
| 5. ML Pipeline | | | | | | **x** |
| 6. Edge Architecture | | | | | | **x** |
| 7. API Specification | | o | | **x** | **x** | **x** |
| 8. Voice Prompt Design | | | | | **x** | |
| 9. Infrastructure | | | | o | o | **x** |
| 10. UI Design | **x** | **x** | **x** | **x** | | o |
| 11. UX Design | **x** | **x** | **x** | **x** | | o |
| 12. Motion Design | o | o | o | o | | |
| 13. Cost Analysis & Risk | **x** | **x** | **x** | **x** | **x** | **x** |
| 14. Writing Plans | **x** | **x** | **x** | **x** | **x** | **x** |
| ⟳ COMPACT | **x** | **x** | **x** | **x** | **x** | **x** |
| 15. Implementation | **x** | **x** | **x** | **x** | **x** | **x** |
| ⟳ COMPACT | **x** | **x** | **x** | **x** | **x** | **x** |
| 16. Security Validation | | o | | **x** | **x** | **x** |
| 17. Observability | | | | **x** | **x** | **x** |
| 18. ML Validation | | | | | | **x** |
| 19. Polish & Review | **x** | **x** | **x** | **x** | **x** | **x** |
| 20. Retrospective | **x** | **x** | **x** | **x** | **x** | **x** |

**x** = always applies | **o** = conditional (based on sub-classification) | blank = skip

### Compile Your Phase Plan
After classification, **explicitly list the active phases** for this project before proceeding:
1. Review the route table for your project type
2. For each "o" phase, check the sub-classification answers to determine if it's active
3. Write out the numbered list of active phases (e.g., "Active phases: 0.5, 1, 2, 3, 4, 7, 10, 11, 13, 14, 15, 16, 18")
4. Present the phase plan to the user for confirmation before starting

This prevents accidentally skipping or running wrong phases.

---
## Phase Execution
<HARD-GATE>
BEFORE executing any phase, you MUST use the Read tool to read
the corresponding phase file from ./phases/.

This is not optional. This is not negotiable. You cannot execute
a phase from memory. You cannot summarize. You cannot skip.

When entering Phase N:
1. Read ./phases/phase-XX-name.md using the Read tool
2. Follow its instructions exactly
3. Produce the deliverable it specifies
3b. Append a Decision Log entry to the design doc on disk
    capturing: what was decided, what was rejected, why,
    and any user corrections or teaching moments.
4. Move to the next active phase in your compiled plan

If you catch yourself thinking "I know what this phase does" —
STOP. Read the file. Skills evolve. Your memory is stale.
</HARD-GATE>

## Context Compaction

Context compaction keeps the conversation window lean for implementation and validation phases. During design and planning (Phases 1–14), let the context grow naturally — the agent makes better decisions with the full chain of reasoning visible.

### Compaction Points

**After Phase 14 (Writing Plans), before Phase 15 (Implementation):**
All design decisions and task breakdowns are now saved to `docs/plans/`. Summarize key decisions, constraints, and tech choices into a compact handoff block, then let the natural context compression drop the verbose design conversation.

**After Phase 15 (Implementation), before Phase 16 (Security Validation):**
Implementation details (code discussions, debugging, refactoring) are no longer needed. The code is on disk. Summarize what was built and any deviations from the plan.

### Compaction Protocol

At each compaction point:

1. **Verify artifacts are on disk.** Check that `docs/plans/` contains the expected deliverables from completed phases. If anything is missing, write it before compacting.
2. **Produce a compact summary** of the key decisions carried forward — architecture choices, tech stack, constraints, trade-offs, and anything the next phase needs to know.
3. **After compaction, the next phase MUST re-read its inputs from disk.** Phase 15 reads the plan. Validation phases (16–18) read the relevant design docs for what they're validating.

### Why Only Two Compaction Points

- **Design phases (1–14) need full context.** Each phase builds on the previous. Compacting mid-design forces re-reading and loses nuance — rejected alternatives, trade-off discussions, and "why not" reasoning.
- **Implementation (15) needs the plan, not the design conversation.** The plan captures everything implementation needs.
- **Validation phases (16–18) need design docs + code, not the implementation conversation.** They read code from the filesystem and reference design docs on disk.

---

## Phase File Mapping
| Phase | File |
|-------|------|
| 0.5 | `./phases/phase-00.5-system-assessment.md` |
| 1 | `./phases/phase-01-brainstorming.md` |
| 2 | `./phases/phase-02-domain-modeling.md` |
| 3 | `./phases/phase-03-system-design.md` |
| 4 | `./phases/phase-04-resilience.md` |
| 5 | `./phases/phase-05-ml-pipeline.md` |
| 6 | `./phases/phase-06-edge-architecture.md` |
| 7 | `./phases/phase-07-api-specification.md` |
| 8 | `./phases/phase-08-voice-prompt.md` |
| 9 | `./phases/phase-09-infrastructure.md` |
| 10 | `./phases/phase-10-ui-design.md` |
| 11 | `./phases/phase-11-ux-design.md` |
| 12 | `./phases/phase-12-motion-design.md` |
| 13 | `./phases/phase-13-cost-analysis.md` |
| 14 | `./phases/phase-14-writing-plans.md` |
| 15 | `./phases/phase-15-implementation.md` |
| 16 | `./phases/phase-16-security-validation.md` |
| 17 | `./phases/phase-17-observability.md` |
| 18 | `./phases/phase-18-ml-validation.md` |
| 19 | `./phases/phase-19-polish-review.md` |
| 20 | `./phases/phase-20-retrospective.md` |

---
## Resumption Protocol
If starting a new session mid-project:
1. Check `docs/plans/` for existing artifacts
2. Read each doc to understand decisions already made
3. Determine which phase produced the last artifact
4. Resume from the next phase
5. If `docs/plans/.mentor-checkpoint.json` exists, read it.
   If mode is "learn", invoke engineering-mentor with the
   stored state instead of continuing in Build mode.
6. If the design doc contains `### Decision Log` sections,
   read them to understand prior reasoning before continuing.

**Artifact -> Phase mapping:**
| Artifact | Phase Completed |
|----------|----------------|
| System Assessment section | Phase 0.5 (Existing System Assessment) |
| `*-design.md` | Phase 1 (Brainstorming) |
| Domain Model section in design doc | Phase 2 |
| `*-system-design.md` | Phase 3 (DDIA) |
| Resilience section in system design | Phase 4 |
| `*-ml-pipeline.md` | Phase 5 |
| Edge Architecture section | Phase 6 |
| API Specification section/doc | Phase 7 |
| Voice prompt doc | Phase 8 |
| Infrastructure section | Phase 9 |
| UI Design section in design doc | Phase 10 |
| UX Design section in design doc | Phase 11 |
| Motion Design section in design doc | Phase 12 |
| Cost & Risk section in design doc | Phase 13 (Cost Analysis) |
| `*-plan.md` | Phase 14 (Writing Plans) |
| Code exists + tests pass | Phase 15 (Implementation) |
| Security audit report | Phase 16 |
| Observability section | Phase 17 |
| ML validation report | Phase 18 |
| Review findings addressed | Phase 19 |
| Retrospective section in design doc | Phase 20 |

---
## Anti-Patterns
| Mistake | Fix |
|---------|-----|
| Skipping to implementation | Always start at Phase 0, even if "you know what you're building" |
| Running all phases for a simple macOS app | Trust the router — it selects only applicable phases |
| Treating security as Phase 16 only | Security-by-design is in Phase 3; Phase 16 validates it was implemented |
| Designing the ML pipeline after building the API | Phases are sequential — ML decisions affect API shape |
| Writing plans without a domain model | Plans based on a vague domain produce vague tasks |
| Skipping resilience for "internal" services | Internal services fail too — especially at 3am |
| Averaging latency instead of using percentiles | p50 hides tail latency; use p95/p99 |
| Adding features to an existing system without mapping it first | Run Phase 0.5 — understand what exists before designing what's new |
| Treating accessibility as a Phase 19 afterthought | Accessibility-by-design in Phase 3 catches issues that are expensive to retrofit |
| Ignoring cloud costs until the bill arrives | Phase 13 (Cost Analysis) exists for this — unit economics matter |
| Skipping the phase file read | Always read the phase file, even if you think you remember it |
| Designing UI before knowing the API shape | UI/UX/Motion phases come after API spec for a reason |

---
## Book References
| Phase | Book | Author |
|-------|------|--------|
| 2. Domain Modeling | *Domain-Driven Design* | Eric Evans |
| 3. System Design | *Designing Data-Intensive Applications* | Martin Kleppmann |
| 4. Resilience | *Release It!* | Michael Nygard |
| 5. ML Pipeline | *Designing Machine Learning Systems* | Chip Huyen |
| 9. Infrastructure | *Infrastructure as Code* | Kief Morris |
| 10. UI Design | *Refactoring UI* | Wathan & Schoger |
| 10. UI Design | *Every Layout* | Andy Bell & Heydon Pickering |
| 10. UI Design | *Design Systems* | Alla Kholmatova |
| 11. UX Design | *Don't Make Me Think* | Steve Krug |
| 11. UX Design | *About Face* | Alan Cooper |
| 11. UX Design | *Inclusive Design Patterns* | Heydon Pickering |
| 12. Motion Design | *The Illusion of Life* | Frank Thomas & Ollie Johnston |
| 12. Motion Design | *Animation at Work* | Rachel Nabors |
| 12. Motion Design | *Designing Interface Animation* | Val Head |
| 14. Testing Strategy | *Growing Object-Oriented Software, Guided by Tests* | Freeman & Pryce |
| 17. Observability | *Observability Engineering* | Charity Majors |
| 18. ML Validation | *Reliable Machine Learning* | Cathy Chen et al. |
