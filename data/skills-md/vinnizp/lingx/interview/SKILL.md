---
name: interview
description: This skill should be used when the user asks to "interview me about the plan", "validate my implementation plan", "review my design decisions", "question my architecture choices", or when finishing plan mode before implementation. Conducts deep technical interviews to validate plans and produce specifications.
---

# Plan Interview Skill

Conduct in-depth interviews to validate implementation plans before coding begins.

## When to Use

- After user creates or presents an implementation plan
- Before exiting plan mode
- When user wants to validate design decisions

## Interview Process

### Step 1: Locate and Read the Plan

Search for plan files in common locations:

- `.claude/plan.md`
- `docs/plan.md`
- Recent plan discussed in conversation

If no plan file exists, ask the user to specify the plan location.

### Step 2: Conduct the Interview

Use `AskUserQuestion` tool to ask probing questions. Interview areas:

**Technical Implementation**

- Edge cases not addressed
- Error handling strategies
- Performance implications
- Security considerations

**Architecture & Design**

- Alternative approaches considered
- Tradeoffs made and rationale
- Integration points with existing code
- Future extensibility

**UI/UX (if applicable)**

- User flow completeness
- Accessibility considerations
- Error states and feedback

**Concerns & Risks**

- What could go wrong?
- Dependencies on external systems
- Testing strategy

### Step 3: Question Quality Guidelines

Avoid obvious questions. Instead:

- Challenge assumptions
- Explore edge cases
- Ask "what if" scenarios
- Probe for unstated requirements

Continue until all areas are adequately covered.

### Step 4: Write the Specification

After interview completion, produce a spec document containing:

- Finalized requirements
- Technical decisions with rationale
- Open questions resolved
- Implementation checklist
