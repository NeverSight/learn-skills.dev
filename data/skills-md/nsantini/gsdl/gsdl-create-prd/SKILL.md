---
name: gsdl-create-prd
description: Generate a Product Requirements Document (PRD) from a seed file or user input. Use when the user wants to create a PRD, document requirements, formalize a feature spec, or turn an idea into a structured requirements document.
disable-model-invocation: true
---

# Create PRD

Generates a detailed Product Requirements Document (PRD) in Markdown format, based on a project's seed file and user input. The PRD is designed to be clear, actionable, and suitable for a junior developer to understand and implement.

## Prerequisites

Before creating a PRD, verify:

1. **Project exists**: The project should have its own folder at `.planning/[project-name]/`
2. **Tasks folder exists**: Ensure `.planning/[project-name]/tasks/` directory exists (create if missing)
3. **Seed file exists**: Check for `.planning/[project-name]/seed.md` containing the initial idea or concept

If the project structure doesn't exist, create it first following the project-setup conventions.

## Process

### Step 1: Read the Seed File from Disk

Read `.planning/[project-name]/seed.md` **directly from disk** — do **not** rely on any in-context version. The user may have edited the file after the project setup phase. Always use the on-disk content as the source of truth.

Use the file to understand:
- The initial problem or opportunity
- Rough feature ideas or concepts
- Inspiration or reference links
- Questions or uncertainties
- Any initial thoughts that inform the PRD

### Step 2: Ask Clarifying Questions

**IMPORTANT**: Do not skip this step. Ask questions to gather sufficient detail before generating the PRD.

Adapt questions based on the seed file content. Common areas to explore:

| Area | Example Questions |
|------|-------------------|
| **Problem/Goal** | "What problem does this feature solve for the user?" / "What is the main goal?" |
| **Target User** | "Who is the primary user of this feature?" |
| **Core Functionality** | "What are the key actions a user should be able to perform?" |
| **User Stories** | "Can you provide user stories? (As a [user], I want to [action] so that [benefit])" |
| **Acceptance Criteria** | "How will we know when this is successfully implemented?" |
| **Scope/Boundaries** | "What should this feature *not* do (non-goals)?" |
| **Data Requirements** | "What data does this feature need to display or manipulate?" |
| **Design/UI** | "Are there mockups or UI guidelines to follow?" |
| **Edge Cases** | "What edge cases or error conditions should we consider?" |

Focus on understanding the "what" and "why" — the developer will figure out the "how."

### Step 3: Generate the PRD

Based on the seed file and user's answers, generate a PRD with this structure:

```markdown
# [Feature Name] - Product Requirements Document

## 1. Introduction/Overview
Briefly describe the feature and the problem it solves. State the goal.

## 2. Goals
List specific, measurable objectives for this feature.
- Goal 1
- Goal 2

## 3. User Stories
Detail user narratives describing feature usage and benefits.
- As a [type of user], I want to [action] so that [benefit]

## 4. Functional Requirements
List specific functionalities the feature must have. Use clear, concise language.
1. The system must allow users to...
2. The system must validate...
3. The system must display...

## 5. Non-Goals (Out of Scope)
Clearly state what this feature will NOT include.
- Will not support...
- Future consideration: ...

## 6. Design Considerations (Optional)
Link to mockups, describe UI/UX requirements, or mention relevant components/styles.

## 7. Technical Considerations (Optional)
Mention known technical constraints, dependencies, or suggestions.
- Should integrate with...
- Consider using...

## 8. Success Metrics
How will success be measured?
- Metric 1: ...
- Metric 2: ...

## 9. Open Questions
List remaining questions or areas needing clarification.
- [ ] Question 1
- [ ] Question 2
```

### Step 4: Save the PRD

1. Generate filename: `prd-[feature-name].md` (kebab-case)
2. Save to: `.planning/[project-name]/tasks/prd-[feature-name].md`
3. Confirm creation with the user, showing the file path

## Target Audience

The PRD reader is a **junior developer**. Requirements should be:
- Explicit and unambiguous
- Free of unexplained jargon
- Detailed enough to understand the feature's purpose and core logic

## Important Rules

1. **Do NOT start implementing** after creating the PRD
2. **Always ask clarifying questions** based on the seed file before generating
3. **Iterate on the PRD** based on user feedback

## Edge Cases

### No Seed File
- Ask the user to describe their idea
- Optionally create a seed.md first to capture raw thoughts
- Proceed with questions as if seed content was provided verbally

### Vague Requirements
- Ask more specific questions
- Suggest concrete options for the user to react to
- Break down broad concepts into smaller, specific features

### Multiple Features
- Suggest creating separate PRDs for each major feature
- Or create one PRD with clearly separated sections per feature

### Existing PRD
- If a PRD already exists for the feature, ask if user wants to:
  - Update the existing PRD
  - Create a new version (e.g., `prd-feature-name-v2.md`)
  - Replace the existing one

## Output

- **Format:** Markdown (`.md`)
- **Location:** `.planning/[project-name]/tasks/`
- **Filename:** `prd-[feature-name].md`
- **Example:** `.planning/my-project/tasks/prd-user-authentication.md`
