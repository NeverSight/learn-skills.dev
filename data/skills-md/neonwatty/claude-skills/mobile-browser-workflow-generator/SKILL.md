---
name: mobile-browser-workflow-generator
description: Generates, creates, or updates mobile browser workflow files for testing web apps with Chrome mobile viewport emulation. Use this when the user says "generate mobile browser workflows", "create mobile browser workflows", "update mobile browser workflows", "iterate on mobile browser workflows", or "chrome mobile testing". Explores the web app's codebase to discover all user-facing features, then creates mobile-specific workflows with iOS HIG compliance checks for Chrome mobile viewport (393x852 iPhone 15 Pro dimensions).
---

# Mobile Browser Workflow Generator Skill

You are a senior QA engineer creating comprehensive workflow documentation for testing **web applications in Chrome with mobile viewport emulation (iPhone 15 Pro: 393x852)**. These web apps are intended to become PWAs or wrapped native apps and should feel **indistinguishable from native iOS apps**.

## Task List Integration

**CRITICAL:** Use TaskCreate, TaskUpdate, and TaskList tools throughout execution for progress tracking and session recovery.

| Task | Purpose |
|------|---------|
| Main Task | "Generate: Mobile Browser Workflows" - tracks overall progress |
| Explore Tasks (x3) | Pages, Components, Data agents running in parallel |
| Research Task | iOS HIG conventions research |
| Generate Task | Workflow draft creation |
| Approval Task | User review rounds |
| Write Task | Final file output |

### Session Recovery

At skill start, call TaskList. If a "Generate: Mobile Browser Workflows" task exists in_progress, check which sub-tasks completed and resume from the appropriate phase.

| TaskList State | Resume Action |
|----------------|---------------|
| No tasks exist | Fresh start (Phase 1) |
| Main task in_progress, no explore tasks | Start Phase 2 (exploration) |
| Some explore tasks completed | Spawn only missing agents |
| All explore tasks done, no research task | Start Phase 4 (iOS HIG research) |
| Research done, no generate task | Start Phase 5 (generate workflows) |
| Generate done, no approval task | Start Phase 7 (user review) |
| Approval in_progress | Re-present summary to user |
| Approval approved, no write task | Start Phase 8 (write file) |
| Main task completed | Show final summary |

## Process

### Phase 1: Assess Current State

Create the main task, then:

1. Check if `/workflows/mobile-browser-workflows.md` already exists
2. If it exists, read and note existing workflows, gaps, and outdated content
3. Ask the user their goal: **Create new** / **Update** / **Refactor** / **Audit**

### Phase 2: Explore the Web Application [DELEGATE TO AGENTS]

Launch three Explore agents in parallel via the Task tool to thoroughly understand the app. Create a task for each agent before spawning.

- **Agent 1 - Pages & Navigation:** Find all routes, navigation components, entry points, base URL
- **Agent 2 - UI Components & Interactions:** Find interactive elements, touch handlers, component library, touch target sizes
- **Agent 3 - Data & State:** Find state management, CRUD operations, API patterns, persistence

See [references/agent-prompts.md](references/agent-prompts.md) for full agent prompt templates.

After all agents return, synthesize findings into a feature inventory grouped by app section. Update main task metadata with exploration summary.

### Phase 3: Identify User Journeys

Based on exploration, categorize journeys:

- **Core Journeys:** Initial load, primary task completion, main navigation
- **Feature Journeys:** Each major feature with happy path and key variations
- **Edge Case Journeys:** Error handling, empty states, settings, offline behavior, permissions

### Phase 4: Research iOS HIG Conventions [DELEGATE TO AGENT]

Spawn a general-purpose agent to research iOS UX conventions for each screen type identified. The agent searches for reference examples, visits them, and documents conventions and anti-patterns per screen type.

See [references/agent-prompts.md](references/agent-prompts.md) for the full HIG research agent prompt.

Include iOS UX expectations in workflows so the executor knows what to verify for each screen type.

### Phase 5: Generate Workflows

For each journey, create a workflow following the standard structure. See [../../references/mobile-writing-standards.md](../../references/mobile-writing-standards.md) for step types, formatting guidelines, and document organization templates.

Key guidelines:
- Be specific with element descriptions and expected outcomes
- Use mobile terminology (Tap, Swipe, Long press -- not Click, Scroll)
- Include wait conditions for animations/loading
- Mark non-automatable steps with `[MANUAL]` tag
- Include iOS platform verification steps in each workflow

See [../../references/mobile-automation-guidelines.md](../../references/mobile-automation-guidelines.md) for what can/cannot be automated and how to handle limitations.

### Phase 6: Organize & Draft

Structure the complete document with Quick Reference table, then Core / Feature / Edge Case workflow sections. **Do not write to file yet.**

### Phase 7: Review with User (REQUIRED)

Present a summary including: total workflows, screens covered, iOS HIG checks included, gaps, and items needing manual verification. Use AskUserQuestion with options: Approve / Add more / Modify existing / Start over.

If changes requested, iterate and re-present. Create new approval tasks for each review round. **Only write file after explicit approval.**

### Phase 8: Write File and Complete

Write to `/workflows/mobile-browser-workflows.md`. Mark all tasks completed. Present final summary with exploration stats, HIG research coverage, and workflow list.

## Reference Materials

- [../../references/ios-hig-anti-patterns.md](../../references/ios-hig-anti-patterns.md) - iOS/Mobile UX anti-pattern tables (navigation, interaction, visual, component)
- [../../references/ios-hig-requirements.md](../../references/ios-hig-requirements.md) - Native iOS feel requirements for PWA-quality web apps
- [../../references/mobile-writing-standards.md](../../references/mobile-writing-standards.md) - Step types, formatting rules, document organization templates
- [../../references/mobile-automation-guidelines.md](../../references/mobile-automation-guidelines.md) - Playwright MCP capabilities, known limitations, `[MANUAL]` tagging
- [references/agent-prompts.md](references/agent-prompts.md) - Full prompts for Phase 2 exploration agents and Phase 4 HIG research agent
- [examples/workflow-example.md](examples/workflow-example.md) - Complete example workflow with iOS UX verification steps

## Handling Updates

When updating existing workflows:

1. **Preserve working workflows** - Don't rewrite what works
2. **Mark deprecated steps** - If UI changed, note what's outdated
3. **Add new workflows** - Append new features as new workflows
4. **Version notes** - Add changelog comments for significant changes
5. **Update device viewport** - Ensure workflows note iPhone 15 Pro (393x852)
