---
name: fusion-issue-author-user-story
description: Draft and update user-story issues with role-action-value framing, workflow scenarios, repository-valid labels, and explicit publish confirmation.
license: MIT
metadata:
  version: "0.1.1"
  orchestrator: "fusion-issue-authoring"
  role: "subordinate"
  tags:
    - github
    - issue-authoring
    - user-story
  mcp:
    required:
      - github
---

# Author User Story Issue

## Dependency

Requires `fusion-issue-authoring` as the top-level orchestrator for classification, shared gates, and publish flow.

## When to use

Use this skill when the request is primarily about user workflow and behavior from a specific role perspective.

## When not to use

Do not use this skill for pure bug reports, generic feature specs without user narrative, or technical enablement tasks.

## Required inputs

- User role and workflow context
- Story goal (`As a... I want... so that...`)
- Key scenarios and success criteria

## Instructions

1. Confirm routed type is `User Story`.
2. Draft locally in `.tmp/USER-STORY-<context>.md`.
3. Structure draft with:
   - Story statement
   - Context/pain points
   - Functional requirements
   - Scenarios (`Given/When/Then`)
   - Validation approach
4. Ensure scenarios are testable and role-centered.
5. Return draft summary for orchestrator review/publish flow.

Template fallback:
- `skills/fusion-issue-author-user-story/assets/issue-templates/user-story.md`

## Expected output

- Draft file path in `.tmp/`
- Proposed title/body summary
- Story-specific scenario and validation summary

## Safety & constraints

Do not perform mutation directly; mutation stays in `fusion-issue-authoring`.
