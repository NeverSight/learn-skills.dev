---
name: lev-design
description: |
  [WHAT] UX-first design workflow from problem framing to wireframes
  [HOW] 7-step agentic pipeline with parallel research and framework-driven analysis
  [WHEN] Use when starting new features, redesigns, or product discovery requiring structured UX thinking
  [WHY] Design is late-stage compression - must understand users, jobs, tasks, and structure before drawing rectangles

  Triggers: "design", "ux", "wireframe", "user flow", "screen", "interface", "prototype"
skill_type: workflow
category: process-design

lifecycle_integration:
  stage: crystallizing
  input_artifact: idea.md | report.md
  output_artifact: wireframe.v1.json + SYNTHESIS.md

required_skills:
  - lev-research         # Prior art + industry research
  - lev-find            # `lev get` backend for codebase pattern discovery
  - interview           # Framework-powered questioning

related_skills:
  - design-to-bd        # Creates BD tasks from design
  - lev-cdo             # Complex design decisions
  - sidequest           # Routes by complexity

protocol_handlers:
  - lev://design?mode={auto|full|step}
  - /ux
  - /ux full

plankton: false
---

# lev-design - UX-First Design Pipeline

## Lev Concept

**What is this?**
A 7-step agentic workflow that transforms product ideas into validated wireframes. Each step uses specialized frameworks and produces machine-readable artifacts.

**Why does it exist?**
Design is a late-stage compression step. UX teams don't start with screens - they start by understanding problems, jobs, tasks, and information architecture. This skill encodes that process.

**When to use it:**
- Starting a new feature
- Redesigning existing flows
- Product discovery
- Mobile/desktop app design
- Dashboard/admin UI design

**When NOT to use it:**
- Simple bug fixes → Just fix it
- Copy changes → Direct edit
- Already have wireframes → Skip to implementation

---

## The 7 Steps

```
User Request
    ↓
[1. Problem Framing]     ← First Principles, Constraints
    ↓
[2. Jobs to Be Done]     ← JTBD, MBTI User Types
    ↓
[3. Task Decomposition]  ← State Machines, Failure Modes
    ↓
[4. Information Arch]    ← DDD, Entity-Relationship
    ↓
[5. Interaction Models]  ← FSM, Accessibility
    ↓
[6. Component Intent]    ← Atomic Design, I/O Contracts
    ↓
[7. Wireframes]          ← Gestalt, Cognitive Load
    ↓
Design Artifacts + SYNTHESIS.md
```

---

## CLI Usage

```bash
# Auto mode - runs all 7 steps without stopping
/ux "Design the onboarding flow for OpenClaw iOS app"

# Interactive mode - asks questions at each step
/ux full "Design the settings screen"

# Jump to specific step (with prior context)
/ux step 4 --context ./ux-2026-02-01/

# Compare wireframes to current implementation
/ux compare ./ux-2026-02-01/ ./apps/ios/Sources/
```

---

## Team Structure

Each step spawns:

**3 Research Agents (Parallel):**
- Codebase patterns (Explore)
- Documentation/decisions (Explore)
- Industry best practices (general-purpose + web)

**3 Skill Phases (Sequential):**
- Framework Application
- Artifact Generation
- Validation

---

## Artifacts Produced

```
./ux-{date}/
├─ problem_spec.yaml      # Step 1
├─ jobs.graph.json        # Step 2
├─ task_graph.json        # Step 3
├─ ia_schema.json         # Step 4
├─ interaction_fsm.json   # Step 5
├─ component_intents.yaml # Step 6
├─ wireframe.v1.json      # Step 7
├─ SYNTHESIS.md           # Human summary
└─ COMPARISON.md          # vs current (if exists)
```

---

## Framework Reference

| Step | Primary Frameworks |
|------|-------------------|
| 1. Problem | First Principles, Theory of Constraints, Cynefin |
| 2. JTBD | Jobs to Be Done, MBTI User Types, Extreme Users |
| 3. Tasks | Systems Thinking, State Machines, Failure Mode Analysis |
| 4. IA | Domain-Driven Design, Object-Action Matrix, Card Sorting |
| 5. Interaction | State Machines, Reactive Design, WCAG Accessibility |
| 6. Components | Atomic Design, Composition over Inheritance, SOLID |
| 7. Wireframes | Gestalt Principles, Cognitive Load Theory, Mobile-First |

---

## Integration with Lev Ecosystem

**Before design:**
- `lev get` - Gather existing patterns
- `lev-research` - Industry research

**After design:**
- `design-to-bd` - Create epics/tasks
- `sidequest` - Route implementation by complexity
- `lev-builder` - POC → Production

**During design:**
- `lev-cdo` - Complex architectural decisions
- `interview` - Framework-powered brainstorming

---

## Expand/Collapse Behavior

**Auto-expand when:**
- Unresolved questions remain
- Validation found conflicts
- Complexity > 7
- User requested "full" mode

**Auto-collapse when:**
- High confidence answers
- Clean validation
- Complexity < 4
- User requested "auto" mode

---

## Pivot Detection

Stop and prompt if:
- Fundamental assumption invalidated
- Requirements conflict discovered
- Technical blocker found
- Better alternative revealed by research

---

## Example Usage

```
> /ux "Design chat interface for OpenClaw iOS"

🔍 Phase 0: Prior Art Check
├─ Found: ChatView.swift, MessageBubble.swift
├─ Found: Previous chat redesign epic (clawd-chat-v2)
└─ Research: ChatGPT, Claude, Gemini UI patterns

📋 Step 1: Problem Framing
├─ Problem: Users need fast, intuitive AI chat on mobile
├─ Constraints: iOS 17+, offline-first, accessibility
└─ Success: <2s response display, 95% task completion

👤 Step 2: JTBD
├─ Job 1: "When I need quick answers, I want to ask naturally"
├─ Job 2: "When context matters, I want to share screenshots"
└─ User types: INTJ (power user), ESFP (casual)

... [Steps 3-7] ...

✅ Complete: ./ux-2026-02-01/
├─ 7 artifacts generated
├─ SYNTHESIS.md ready for review
└─ Comparison: 12 differences from current ChatView
```

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-design, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
