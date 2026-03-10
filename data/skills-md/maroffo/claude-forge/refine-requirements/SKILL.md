---
name: refine-requirements
description: "Structured requirements gathering before planning. Use when request has ambiguities, multiple valid approaches, or implicit decisions."
---

# ABOUTME: Structured requirements refinement using AskUserQuestion before planning
# ABOUTME: Identifies gray areas, clarifies with concrete options, captures decisions for the plan

# Requirements Refinement

Invoke explicitly or triggered automatically by plan-first-workflow for 🟡/🔴 tasks.

## Process

1. **Identify gray areas** by domain:
   - Visual → layout, density, interactions, empty states
   - API/CLI → response format, error handling, auth flow
   - Infrastructure → scaling, redundancy, monitoring
   - Integration → protocol, auth method, error recovery

2. **For each gray area**, use `AskUserQuestion`:
   - Concrete options ("JWT" not "Option A"), 2-4 choices
   - Include "You decide" when Claude's discretion is fine
   - Follow threads: each answer may reveal the next question

3. **Scope guard**: if user suggests new scope, capture as deferred idea, redirect back

4. **Output**: list of decisions to include as `## Decisions` in the plan file

## Anti-patterns

- Generic questions ("What are your requirements?") → ask about specific decisions
- Checklist walking → follow the thread the user cares about
- Expanding scope → clarify HOW to implement what's requested, not WHETHER to add more
