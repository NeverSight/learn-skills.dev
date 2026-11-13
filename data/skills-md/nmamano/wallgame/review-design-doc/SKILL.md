---
name: review-design-doc
description: Review a design document and provide feedback on implementation challenges, alternative approaches, and underspecified areas. Use when asked to review a design doc or feature spec.
allowed-tools: Read, Glob, Grep
---

# Review Design Doc

Review a design document and provide structured feedback.

## Instructions

When this skill is invoked:

1. Read the design document file provided as an argument using the Read tool
2. Analyze the document thoroughly
3. Provide feedback organized into exactly three sections:

### Feedback Structure

**1. Things that are hard to implement**

- Identify technical challenges, complex dependencies, or areas requiring significant effort
- Consider performance implications, edge cases, and integration complexity
- Note any missing infrastructure or tooling that would be needed

**2. Things that would be easier to do differently**

- Suggest simpler alternatives that achieve similar goals
- Point out over-engineered solutions
- Recommend existing patterns, libraries, or approaches that could reduce complexity

**3. Things that are underspecified**

- Identify missing details needed for implementation
- Note ambiguous requirements or unclear behavior
- Highlight missing error handling, edge cases, or failure modes
- Point out undefined user interactions or flows

## Output Format

Structure your response with clear headers for each section. Be specific and actionable - reference particular parts of the design doc when giving feedback. If a section has no issues, say so briefly rather than inventing problems.
