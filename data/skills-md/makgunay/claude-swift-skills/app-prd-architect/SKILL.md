---
name: app-prd-architect
description: "Guided app discovery, PRD generation, and architectural design for native macOS/iOS applications. Takes the user from a rough app idea through an interactive exploration of features, user experience, and design vision, then produces three deliverables: (1) a comprehensive PRD with functional requirements, user stories, and success metrics, (2) a technical architecture document with data models, system diagrams, and component design, (3) a feature list for non-technical stakeholders. Use when user says things like 'I have an app idea', 'help me plan an app', 'write a PRD', 'design the architecture for', 'what should my app do', 'help me think through features', or 'I want to build an app that...'. Also use when user has an existing PRD draft and wants to expand, validate, or restructure it. Guides through iterative discovery before producing documents — never jumps straight to writing."
---

# App PRD & Architecture Generator

## Overview

Transform a rough app idea into production-ready planning documents through structured discovery. Act as a product team: product manager, UX designer, and systems architect collaborating with the user.

**Core principle:** Never write the PRD until discovery is complete. The quality of the documents depends entirely on the quality of the conversation that precedes them.

## Workflow

```
Phase 1: DISCOVERY → Phase 2: FEATURE DESIGN → Phase 3: IDEA EXPANSION → Phase 4: DOCUMENTS
    ↑                    ↑                          ↑                         ↑
    └────────────────────┴──────────────────────────┴─────────────────────────┘
                         (Iterate freely between phases)
```

**Quick start routing:**
- "I have an idea for an app" → Phase 1 (full discovery)
- "Here's my draft PRD, help me improve it" → Read draft → Phase 2 (fill gaps) → Phase 4
- "I need an architecture doc for this PRD" → Read PRD → Phase 4 (architecture only)
- "Help me think through features for X" → Brief Phase 1 → Phase 2 (deep dive)

## Phase 1: Discovery

### Approach
Ask questions conversationally — 2-3 at a time maximum. Adapt depth to user's clarity level. If the user already knows what they want, don't slow them down.

### 1.1 Foundation (Always start here)
- What does this app do in one sentence?
- Who is the primary user? (Be specific — "developers" is too broad, "indie iOS developers who use multiple AI assistants daily" is good)
- What problem does it solve? What's the current workaround?
- What platform(s)? macOS, iOS, both? What's the minimum OS version?

### 1.2 User Context
- Walk me through a typical use session — from opening the app to closing it
- What triggers the user to reach for this app? (Notification? Keyboard shortcut? Habit?)
- How frequently will they use it? (Multiple times daily, weekly, occasionally?)
- What other apps will they have open alongside it?

### 1.3 Competitive Landscape
- What do people use today instead? (Even if it's "nothing" or "copy-paste from Notes")
- Name 2-3 apps (any domain) whose UX you admire. What specifically?
- What's the one thing you want this app to do better than any alternative?

### 1.4 Scope & Constraints
- Solo developer or team? What's the realistic timeline?
- Distribution: App Store, direct, or both?
- Monetization: Free, paid upfront, freemium, subscription?
- What's explicitly NOT in v1.0?

### 1.5 Design Sensibility
- Describe the personality of this app in 3 words
- Minimal and hidden, or feature-rich and visible?
- Reference any apps whose visual design resonates

### Discovery Output
Synthesize into a **Product Brief** (present to user for confirmation before proceeding):

```markdown
# Product Brief: [App Name]

## One-Liner
[What it does in one sentence]

## Target User
[Specific persona with context]

## Core Problem
[The pain point and current workaround]

## Key Differentiator
[The one thing this does better than alternatives]

## Platform & Constraints
- Platform: [macOS/iOS/both]
- Distribution: [App Store/direct/both]
- Monetization: [model]
- Timeline: [realistic estimate]
- Non-goals: [explicit exclusions]
```

Confirm the brief with the user before moving to Phase 2.

## Phase 2: Feature Design

### 2.1 Core Feature Identification

Work through features systematically. For each feature:

1. **User story**: "As a [user], I want to [action] so that [benefit]"
2. **Happy path**: What happens when everything works?
3. **Edge cases**: What happens when things go wrong or get weird?
4. **States**: Empty state, loading, populated, error, disabled
5. **Priority**: Must-have (v1.0), Should-have (v1.1), Nice-to-have (v2.0)

### 2.2 Interaction Model

Define the core interaction patterns:
- **Entry point**: How does the user invoke the app? (Dock, menu bar, hotkey, widget?)
- **Primary flow**: What's the 3-step happy path? (Invoke → Search/Select → Action)
- **Navigation structure**: Flat, tabbed, sidebar + detail, single-window?
- **Keyboard-first or mouse-first?** What are the essential shortcuts?

### 2.3 Data Model Sketch

For each core entity:
- What properties does it have?
- What are the relationships between entities?
- What needs to persist vs. what's ephemeral?
- Does it sync? (iCloud, server, export/import only?)

### 2.4 Settings & Configuration

- What can the user customize?
- What are the sensible defaults?
- Where do settings live? (Menu bar, preferences window, inline?)

Present features as a structured table for user review:

```markdown
| Feature | Priority | User Story | Complexity |
|---------|----------|------------|------------|
| [Name]  | Must     | As a...    | Low/Med/Hi |
```

## Phase 3: Idea Expansion

Before finalizing, dedicate one exchange to exploring what the user hasn't thought of:

### 3.1 "What If" Exploration
- What would make this feel magical rather than merely functional?
- If you had unlimited time, what would v3.0 look like? (Then: which v3.0 ideas should we design for now even if we don't build them yet?)
- Is there a workflow this app could automate that users currently do manually?

### 3.2 Defensive Thinking
- What's the most likely reason a user would stop using this after a week?
- What happens when the user has 10x more data than expected?
- What accessibility considerations matter? (VoiceOver, keyboard navigation, Reduce Motion)

### 3.3 Platform Opportunities
- Can this integrate with Siri/Shortcuts?
- Would a widget or menu bar presence add value?
- Does it benefit from Handoff / Universal Clipboard / Continuity?

Flag new ideas to the user — don't silently add them to the PRD.

## Phase 4: Document Production

Produce deliverables as actual files (.md for text, .docx for formal documents). See `references/prd-template.md` and `references/architecture-template.md` for complete templates.

### Document A: Product Requirements Document (PRD)

**Audience:** Engineering team, technical stakeholders
**Format:** Markdown (.md)

Sections:
1. Executive Summary
2. Problem Statement (with market context)
3. Goals & Success Metrics (quantifiable)
4. Non-Goals (explicit scope boundaries)
5. User Personas (with jobs-to-be-done)
6. User Stories with Acceptance Criteria
7. Functional Requirements (complete feature spec)
8. Non-Functional Requirements (performance, accessibility, security, privacy)
9. UI/UX Specifications (key screens, states, transitions)
10. Data Model
11. Error Handling Specification
12. Dependencies & Risks
13. Implementation Phases with Milestones
14. Open Questions & Decisions Log
15. Glossary

### Document B: Technical Architecture

**Audience:** Engineering team
**Format:** Markdown (.md)

Sections:
1. Architecture Overview (with diagram description)
2. Technology Stack (with justification for each choice)
3. System Components & Responsibilities
4. Data Layer (models, persistence, sync strategy)
5. Concurrency Model (actor isolation, background work)
6. UI Layer (view hierarchy, navigation, state management)
7. Integration Points (system services, permissions, APIs)
8. Security & Privacy Architecture
9. Performance Budget (launch time, memory, storage)
10. Testing Strategy
11. Build & Distribution Pipeline
12. Migration & Upgrade Path

### Document C: Feature List (Non-Technical)

**Audience:** Non-technical stakeholders, marketing, investors
**Format:** Markdown (.md)

Sections:
1. One-Sentence Product Description
2. Problem / Solution Framing (no jargon)
3. Core Features with User-Benefit Framing ("You can..." not "The system...")
4. Feature Categorization (Core / Power User / Future)
5. Competitive Differentiation
6. Target User Description

## Quality Checklist

Before delivering documents, verify:

- [ ] Every feature in the PRD maps to a user story
- [ ] Every user story has acceptance criteria
- [ ] Non-goals are explicit — not just "whatever we didn't mention"
- [ ] Data model supports all described features
- [ ] Architecture addresses concurrency, persistence, and sync
- [ ] Performance budgets are stated (launch time, memory)
- [ ] Error states are defined for every user-facing feature
- [ ] Accessibility requirements are specified
- [ ] v1.0 scope is achievable within stated timeline
- [ ] Open questions are captured with owners/deadlines

## Key Principles

1. **Discover before designing** — Never write the PRD first
2. **Challenge assumptions** — If the user says "simple CRUD app," ask what makes it worth building
3. **Name the non-goals** — Scope is defined as much by what's excluded as included
4. **Design for the edges** — Happy paths are easy; edge cases reveal the real product
5. **Think in versions** — v1.0 ships, v2.0 expands, v3.0 transforms
6. **Stay concrete** — "Fast" isn't a requirement; "< 200ms cold launch" is
7. **Respect the timeline** — A perfect PRD for a product that never ships helps no one
