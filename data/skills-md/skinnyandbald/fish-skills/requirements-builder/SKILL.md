---
name: requirements-builder
description: "Progressively gather requirements through automated codebase discovery and yes/no questions, then generate a comprehensive requirements spec. Use when starting a new feature, planning a build, or when you need structured requirements before implementation."
---

# Requirements Builder

Intelligent requirements gathering system that discovers codebase context, asks structured yes/no questions, and generates comprehensive requirements documentation.

Based on [claude-code-requirements-builder](https://github.com/rizethereum/claude-code-requirements-builder).

## Arguments

`$ARGUMENTS` — description of the feature or requirement to gather (e.g., "add user profile photo upload")

## Setup

Ensure the `requirements/` directory exists in the project root:
```
mkdir -p requirements
touch requirements/.current-requirement
```

## Workflow Overview

```
Phase 1: Initial Setup & Codebase Analysis
    → Create timestamped folder, analyze codebase structure
Phase 2: Context Discovery Questions (5 yes/no questions)
    → Ask about problem space, workflows, integrations
Phase 3: Targeted Context Gathering (autonomous)
    → Deep-dive into relevant code, patterns, similar features
Phase 4: Expert Requirements Questions (5 yes/no questions)
    → Ask like a senior dev who knows the codebase
Phase 5: Requirements Documentation
    → Generate comprehensive spec with acceptance criteria
```

---

## Phase 1: Initial Setup & Codebase Analysis

1. Create timestamp-based folder: `requirements/YYYY-MM-DD-HHMM-[slug]`
2. Extract slug from `$ARGUMENTS` (e.g., "add user profile" → "user-profile")
3. Create initial files:
   - `00-initial-request.md` with the user's request
   - `metadata.json` with status tracking
4. Read and update `requirements/.current-requirement` with folder name
5. Analyze the codebase to understand overall structure:
   - Get high-level architecture overview
   - Identify main components and services
   - Understand technology stack
   - Note patterns and conventions

## Phase 2: Context Discovery Questions

6. Generate the five most important yes/no questions to understand the problem space:
   - Questions informed by codebase structure
   - Questions about user interactions and workflows
   - Questions about similar features users currently use
   - Questions about data/content being worked with
   - Questions about external integrations or third-party services
   - Questions about performance or scale expectations
   - Write all questions to `01-discovery-questions.md` with smart defaults
   - Begin asking questions one at a time proposing the question with a smart default option
   - Only after all questions are asked, record answers in `02-discovery-answers.md` as received and update `metadata.json`. Not before.

### Discovery Question Format:
```
## Q1: Will users interact with this feature through a visual interface?
**Default if unknown:** Yes (most features have some UI component)

## Q2: Does this feature need to work on mobile devices?
**Default if unknown:** Yes (mobile-first is standard practice)
```

## Phase 3: Targeted Context Gathering (Autonomous)

7. After all discovery questions answered:
   - Search for specific files based on discovery answers
   - Read relevant code in batch
   - Deep dive into similar features and patterns
   - Analyze specific implementation details
   - Use WebSearch and/or context7 for best practices or library documentation
   - Document findings in `03-context-findings.md` including:
     - Specific files that need modification
     - Exact patterns to follow
     - Similar features analyzed in detail
     - Technical constraints and considerations
     - Integration points identified

## Phase 4: Expert Requirements Questions

8. Now ask questions like a senior developer who knows the codebase:
   - Write the top 5 most pressing unanswered detailed yes/no questions to `04-detail-questions.md`
   - Questions should be as if you were speaking to the product manager who knows nothing of the code
   - These questions are meant to clarify expected system behavior now that you have a deep understanding of the code
   - Include smart defaults based on codebase patterns
   - Ask questions one at a time
   - Only after all questions are asked, record answers in `05-detail-answers.md` as received

### Expert Question Format:
```
## Q7: Should we extend the existing UserService at services/UserService.ts?
**Default if unknown:** Yes (maintains architectural consistency)

## Q8: Will this require new database migrations in db/migrations/?
**Default if unknown:** No (based on similar features not requiring schema changes)
```

## Phase 5: Requirements Documentation

9. Generate comprehensive requirements spec in `06-requirements-spec.md`:
   - Problem statement and solution overview
   - Functional requirements based on all answers
   - Technical requirements with specific file paths
   - Implementation hints and patterns to follow
   - Acceptance criteria
   - Assumptions for any unanswered questions

---

## Important Rules

- ONLY yes/no questions with smart defaults
- ONE question at a time
- Write ALL questions to file BEFORE asking any
- Stay focused on requirements (no implementation)
- Use actual file paths and component names in detail phase
- Document WHY each default makes sense

## Phase Transitions

- After each phase, announce: "Phase complete. Starting [next phase]..."
- Save all work before moving to next phase

---

## Sub-Commands

### /requirements-status
Show current requirement gathering progress and continue from last unanswered question.

1. Read `requirements/.current-requirement`
2. If no active requirement, suggest starting one
3. If active: show formatted status, load question files, continue from last unanswered question

### /requirements-current
Display detailed information about the active requirement (view-only, doesn't continue gathering).

Shows: initial request, codebase overview, all questions/answers, context findings, current phase, next steps.

### /requirements-list
Display all requirements with their status and summaries, sorted by active first, then complete, then incomplete.

### /requirements-end
Finalize the current requirement gathering session. Options:
1. **Generate spec** with current information (defaults for unanswered)
2. **Mark as incomplete** for later
3. **Cancel and delete**

### /requirements-remind
Quick correction when deviating from requirements gathering rules. Auto-detects:
- Open-ended questions asked → rephrase as yes/no
- Multiple questions asked → ask one at a time
- Implementation started → redirect to requirements
- No default provided → add a default

---

## File Structure

Each requirement creates this folder structure:
```
requirements/
  .current-requirement          # Active requirement folder name
  YYYY-MM-DD-HHMM-[slug]/
    00-initial-request.md       # Original user request
    01-discovery-questions.md   # Context discovery questions
    02-discovery-answers.md     # User's answers
    03-context-findings.md      # AI's codebase analysis
    04-detail-questions.md      # Expert requirements questions
    05-detail-answers.md        # User's detailed answers
    06-requirements-spec.md     # Final requirements document
    metadata.json               # Status tracking
```

## Metadata Structure

```json
{
  "id": "feature-slug",
  "started": "ISO-8601-timestamp",
  "lastUpdated": "ISO-8601-timestamp",
  "status": "active",
  "phase": "discovery|context|detail|complete",
  "progress": {
    "discovery": { "answered": 0, "total": 5 },
    "detail": { "answered": 0, "total": 0 }
  },
  "contextFiles": ["paths/of/files/analyzed"],
  "relatedFeatures": ["similar features found"]
}
```

## Final Spec Format

```markdown
# Requirements Specification: [Name]

Generated: [timestamp]
Status: [Complete with X assumptions / Partial]

## Overview
[Problem statement and solution summary]

## Detailed Requirements

### Functional Requirements
[Based on answered questions]

### Technical Requirements
- Affected files: [list with paths]
- New components: [if any]
- Database changes: [if any]

### Assumptions
[List any defaults used for unanswered questions]

### Implementation Notes
[Specific guidance for implementation]

### Acceptance Criteria
[Testable criteria for completion]
```
