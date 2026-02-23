---
name: update-agents-md
description: Update AGENTS.md with new rules to prevent AI misbehavior or add operational guidelines. Use when the user says "update AGENTS.md", "add this rule", "change AI behavior", or "don't do X automatically".
---

# update-agents-md

Update AGENTS.md when AI causes rework, makes unauthorized decisions, or when new operational rules are needed.

## Trigger Examples

- "Update AGENTS.md"
- "Add this rule"
- "Change AI behavior"
- "Don't do X automatically"

## Execution Flow

### 1. Read and Analyze AGENTS.md

- Load current AGENTS.md content
- Understand existing section structure
- Search for related existing rules

### 2. Analyze User Input

**Identify the problem type:**

- AI misbehavior (unauthorized decisions, rework, rule violations)
- Insufficient or ambiguous existing rules
- New operational rule addition

**Determine affected section (koborin-ai specific):**

- Mission
- Repository Layout
- Infrastructure Rules
- Application Rules
- Astro Development Best Practices
- CI/CD Expectations
- Release Process
- Diagram Guidelines
- Documentation Standards
- Code Quality Standards
- Pull Request Checklist

### 3. Determine Best Section and Placement

**Extend existing section (preferred):**

- Similar rules already exist in a section
- Same category

**Create new section (only when necessary):**

- Topic does not fit existing sections

**Writing style:**

- Use flat hierarchy matching surrounding items
- Write concise, factual statements
- Match existing style (English, table/list format)

### 4. Check Consistency with Existing Rules

- **Duplicate check**: Ensure same rule does not already exist
- **Conflict check**: Ensure no contradiction with existing rules

### 5. Generate and Present Update Proposal

Present in this format:

```markdown
## Proposed Update

### Target Section

[Section name]

### Changes (diff format)

```diff
+ Added content
```

### Rationale

- [Why this section was chosen]
- [Relationship to existing rules]

**Approve? (yes/no)**
```

### 6. Wait for User Approval

- **Approved**: Update AGENTS.md
- **Revision requested**: Incorporate feedback and re-propose
- **Rejected**: Cancel update

## Notes

- Match existing style: AGENTS.md uses English
- No excessive decoration: Avoid emoji or emphasis
- Concise: State facts only, avoid verbose explanations
- Manual commit: Leave commit decision to user
