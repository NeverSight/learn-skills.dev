---
name: fix
description: '[Fix & Debug] ⚡⚡ Analyze and fix issues [INTELLIGENT ROUTING]'
argument-hint: [issues]
---

**Be skeptical. Critical thinking. Everything needs traced proof.** — Never accept code at face value; verify claims against actual behavior, trace data flow end-to-end, and demand evidence (file:line references, grep results, runtime confirmation) for every finding.

**Analyze issues and route to specialized fix command:**
<issues>$ARGUMENTS</issues>

## Decision Tree

**1. Check for existing plan:**

- If markdown plan exists → `/code <path-to-plan>`

**2. Route by issue type:**

**A) Type Errors** (keywords: type, typescript, tsc, type error)
→ `/fix-types`

**B) UI/UX Issues** (keywords: ui, ux, design, layout, style, visual, button, component, css, responsive)
→ `/fix-ui <detailed-description>`

**C) CI/CD Issues** (keywords: github actions, pipeline, ci/cd, workflow, deployment, build failed)
→ `/fix-ci <github-actions-url-or-description>`

**D) Test Failures** (keywords: test, spec, jest, vitest, failing test, test suite)
→ `/fix-test <detailed-description>`

**E) Log Analysis** (keywords: logs, error logs, log file, stack trace)
→ `/fix-logs <detailed-description>`

**F) Multiple Independent Issues** (2+ unrelated issues in different areas)
→ `/fix-parallel <detailed-description>`

**G) Complex Issues** (keywords: complex, architecture, refactor, major, system-wide, multiple components)
→ `/fix-hard <detailed-description>`

**H) Simple/Quick Fixes** (default: small bug, single file, straightforward)
→ `/fix-fast <detailed-description>`

## Notes

- `detailed-description` = enhanced prompt describing issue in detail
- If unclear, ask user for clarification before routing
- Can combine routes: e.g., multiple type errors + UI issue → `/fix-parallel`

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
