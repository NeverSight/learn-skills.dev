---
name: steve2
description: The ultimate autonomous dev pipeline. Combines wavybaby (CoVe verification, skill discovery, MCP tooling) + GSD (roadmaps, phases, plans, discovery, state tracking) + Ralph (autonomous loop with circuit breakers). Generates a PRD, equips itself with the best tools, bootstraps a full GSD .planning/ structure, then runs Ralph to autonomously execute each plan with CoVe-verified code until the milestone is complete.
disable-model-invocation: false
user-invocable: true
argument-hint: "[project description or path]"
---

# Steve — wavybaby + GSD + Ralph Autonomous Execution

Combines three systems:
- **wavybaby**: Self-equipping toolchain (CoVe verification, skill discovery via skills.sh, MCP server setup, project config)
- **GSD**: Structured project management (`.planning/`, roadmaps, phases, plans, discovery, verification, state tracking)
- **Ralph**: Autonomous while-true loop (circuit breakers, dual-condition exit, session persistence, rate limiting)

**IMPORTANT — Context Management**: Steve offloads heavy phases to subagents via the Task tool to avoid hitting the 20MB API request limit. Phase instructions live in template files at `~/.claude/skills/steve/templates/`. The main conversation stays lean — it orchestrates, collects brief summaries, and handles user interaction only.

---

## EXECUTION FLOW

### Step 1: Parallel Kickoff

Do these TWO things simultaneously in a single message with parallel tool calls:

**A) Spawn Phase 0 subagent (Equip):**
```
Use the Task tool with subagent_type: "general-purpose", mode: "bypassPermissions"
Prompt: "Read the template at ~/.claude/skills/steve/templates/phase0-equip.md, then execute all steps for this project: [user's $ARGUMENTS]. Working directory: [current working directory]."
Run in background: true
```

**B) Begin Phase 1 (PRD Q&A) in the main conversation** — see the PRD Generation section below.

### Step 2: PRD Completion

After all Q&A rounds are done:
1. Write the PRD to `.planning/specs/PRD.md` (create `.planning/specs/` if needed)
2. Ask user for approval: "PRD generated at `.planning/specs/PRD.md`. Ready to proceed, or want changes?"
3. **CRITICAL — Context Consolidation**: After PRD approval, summarize your understanding in exactly this format and use ONLY this summary for all subsequent phases:
   ```
   PRD approved. Summary:
   - Project: [name and type]
   - Stack: [languages, frameworks, key deps]
   - Key entities: [core data objects]
   - MVP scope: [2-3 bullet summary]
   - Phases needed: [estimated count and names]
   ```
   Do NOT reference the Q&A history or PRD contents again. The file is on disk for subagents to read.

### Step 3: Collect Phase 0 Result

Check on the Phase 0 background subagent. Capture its brief equip summary (~3 lines). If it failed, inform the user and offer to retry or skip.

### Step 4: Spawn Phase 2+3 Subagent (GSD Bootstrap + Plans)

```
Use the Task tool with subagent_type: "general-purpose", mode: "bypassPermissions"
Prompt: "Read the template at ~/.claude/skills/steve/templates/phase2-bootstrap.md, then execute all steps.
PRD location: .planning/specs/PRD.md
Stack: [from Phase 0 equip summary]
Has existing code: [yes/no]
Working directory: [current working directory]"
```

Wait for completion. Capture the brief summary (~3 lines).

### Step 5: Spawn Phase 4 Subagent (Loop Config)

```
Use the Task tool with subagent_type: "general-purpose", mode: "bypassPermissions"
Prompt: "Read the template at ~/.claude/skills/steve/templates/phase4-loop.md, then execute all steps.
Project name: [name]
Stack: [type]
Skills installed: [from Phase 0 summary]
MCPs configured: [from Phase 0 summary]
Working directory: [current working directory]"
```

Wait for completion. Capture the brief summary (~2 lines).

### Step 6: Print Final Status + Launch Ralph

Print the complete status report:

```
Steve setup complete.

EQUIPPED:
  Skills:         [from Phase 0 summary]
  MCP servers:    [from Phase 0 summary]
  Config:         settings.local.json

PROJECT:
  PRD:            .planning/specs/PRD.md
  Project:        .planning/PROJECT.md
  Roadmap:        .planning/ROADMAP.md
  State:          .planning/STATE.md
  Phase 1 Plans:  .planning/phases/01-*/

LOOP:
  Config:         .ralphrc
  Prompt:         .ralph/PROMPT.md
  Build/test:     .ralph/AGENT.md

To run:
  ralph --monitor      # Recommended: loop + dashboard in tmux
  ralph                # Loop only
```

Then launch: `ralph --monitor`

---

## PHASE 1: PRD GENERATION (runs in main context)

### Deep-dive questioning (MANDATORY)

Before writing the PRD, conduct a thorough interview. Ask questions in **multiple rounds** using AskUserQuestion. Do NOT rush — the PRD quality depends on how well you understand the project. Keep asking until you have a clear picture.

**Round 1: Vision & Users**
- "What problem does this solve? What's the pain point today?"
- "Who are the primary users? Describe 2-3 distinct personas."
- "What does success look like? How will you know this is working?"
- "Are there existing products/competitors? What do they get wrong?"

**Round 2: Core Experience**
- "Walk me through the ideal user journey from first open to daily use."
- "What are the 3 features that MUST exist for this to be useful? What's the single most important one?"
- "What should the user feel when using this? (fast, calm, powerful, fun, simple)"
- "Are there any workflows that need to feel instant vs. ones that can load?"

**Round 3: Technical & Platform**
- "What's the target platform? (iOS, Android, both, web, desktop, CLI)"
- "Any existing backend, database, auth system, or APIs to integrate with?"
- "Do you have preferences on stack/framework, or should I recommend?"
- "Does this need real-time features? (live updates, collaboration, notifications)"
- "Offline support needed? What should work without internet?"
- "Any third-party services? (payments, maps, analytics, AI/ML, messaging)"

**Round 4: Data & Business Logic**
- "What are the core entities/objects in this system? (users, posts, orders, etc.)"
- "What are the key relationships between them?"
- "Are there different user roles or permission levels?"
- "Any complex business rules? (pricing tiers, approval workflows, calculations)"
- "What data is sensitive? (PII, financial, health)"

**Round 5: Scope & Constraints**
- "What's MVP vs. nice-to-have vs. definitely-not-now?"
- "Any hard deadlines or constraints?"
- "Any design preferences? (dark mode, brand colors, reference apps)"
- "Accessibility? Internationalization? Compliance? (GDPR, HIPAA, SOC2, PCI)"

**Round 6: Edge Cases & Polish**
- "What happens when something goes wrong? (no internet, server error, invalid input)"
- "What empty states exist? (new user, no data, no search results)"
- "What notifications/emails/alerts should the system send?"
- "Onboarding flow? Admin/backoffice needs?"

You do NOT need to ask every question. Skip irrelevant ones. But ask across at least 4 of 6 rounds. If the user's description is vague, ask more. If detailed, focus on gaps.

After each round, acknowledge what you learned and explain what you still need before asking the next round. Stop when you have enough for a comprehensive PRD.

### Generate `.planning/specs/PRD.md`

Write a complete PRD with ALL sections:

```markdown
# PRD: [Project Name]

## 1. Overview
One paragraph: what this does and why.

## 2. Target Users
| User Type | Description | Primary Need |
|-----------|-------------|--------------|

## 3. User Stories

### Epic: [Feature Area]
- **US-001**: As a [user], I want to [action] so that [benefit]
  - Acceptance Criteria:
    - [ ] [Specific, testable criterion]

(Continue for all epics/stories)

## 4. Technical Requirements

### Stack
| Layer | Technology | Rationale |

### Architecture
- Key architectural decisions, data flow, API structure

### Data Model
| Entity | Key Fields | Relationships |

### API Endpoints
| Method | Path | Purpose | Auth |

## 5. Screens & Navigation

### Screen Map
(Tree diagram of all screens/routes)

### Screen Descriptions
| Screen | Purpose | Key Components |

## 6. Non-Functional Requirements
- Performance, security, accessibility, offline support

## 7. MVP Scope
### In Scope (MVP)
### Out of Scope (Post-MVP)

## 8. Success Metrics
| Metric | Target | How Measured |

## 9. Open Questions
```

---

## HOW THE LOOP EXECUTES GSD

### Per-Iteration Flow

```
Loop iteration N:
  1. Read .planning/STATE.md
  2. Identify: Phase X, Plan Y
  3. If DISCOVERY.md missing -> research phase (use Context7) -> write DISCOVERY.md -> done
  4. If plans not generated -> generate plans from DISCOVERY + PRD -> done
  5. Read .planning/phases/{X}-{name}/{XX}-{YY}-PLAN.md
  6. Execute all tasks in plan
     - Non-trivial code -> CoVe 4-stage verification
     - Library usage -> Context7 doc lookup
  7. Run verification checks
  8. Write {XX}-{YY}-SUMMARY.md
  9. Update STATE.md (plan Y+1, metrics)
  10. If last plan in phase -> update ROADMAP.md, advance to Phase X+1
  11. If last phase -> verification gate -> EXIT_SIGNAL: true
  12. Output RALPH_STATUS block
```

### Circuit Breaker (from Ralph)

| Trigger | Result |
|---------|--------|
| 3 loops no file changes | OPEN (halted) |
| 5 loops same error | OPEN (halted) |
| 2 loops no progress in STATE.md | HALF_OPEN (monitoring) |
| Progress resumes | CLOSED (recovered) |

### Exit Detection (Dual-Condition Gate)

Ralph only stops when BOTH:
1. `completion_indicators >= 2` (from RALPH_STATUS blocks)
2. `EXIT_SIGNAL: true` (all phases complete, verification gate passed)

---

## COMPARISON

| Feature | Spidey | GSD only | Steve |
|---------|--------|----------|-------|
| Auto-equip (skills, MCP, config) | No | No | Yes (wavybaby) |
| PRD generation | Yes | No | Yes |
| Structured phases | No (flat checklist) | Yes | Yes |
| Discovery/research docs | No | Yes | Yes |
| Atomic plans with verification | No | Yes | Yes |
| CoVe code verification | No | No | Yes (wavybaby/rnv) |
| Context7 doc lookups | No | No | Yes (wavybaby) |
| State tracking | Basic | Detailed | Detailed |
| Autonomous execution | Yes (Ralph loop) | No (manual) | Yes (Ralph loop) |
| Circuit breakers | Yes | No | Yes |
| Session persistence | Ralph session | STATE.md | Both |
| Just-in-time planning | No (all upfront) | Yes | Yes |
| SUMMARY.md audit trail | No | Yes | Yes |
| Codebase documentation | No | Yes | Yes |
| Progress metrics/velocity | Basic | Detailed | Detailed |

---

Now setting up Steve for: **$ARGUMENTS**
