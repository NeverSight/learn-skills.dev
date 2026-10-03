---
name: ux-gap-detector
description: SaaS UX gap audit
argument-hint: "[--category dashboard|data-management|form-workflow|navigation-shell|settings-profile] [target-url]"
allowed-tools: "Bash,Read,Write,Edit,Glob,Grep,AskUserQuestion,mcp__sequential-thinking__*,mcp__serena__*"
---

# UX Gap Detector

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.


Detect UI/UX quality gaps in authenticated SaaS web applications through
live browser interaction using the user's logged-in session via **playwright-cli**.

## Quick Start

```
/ux-gap-detector                              <- interactive: asks category + URL
/ux-gap-detector --category dashboard         <- audit dashboard screens
/ux-gap-detector --category data-management   <- audit tables, CRUD, search/filter
```

**Prerequisite**: The user must be logged into their app in Chrome with the
playwright-cli extension connected.

---

## Workflow

### Phase 0: Setup (Authenticated Session)

**Before any browser interaction**: invoke `/dnd` to load the drag-and-drop verification protocol. Required even when DnD is not yet known to be involved — ref-based `drag` returns false success on `dnd-kit` and similar libraries.

1. **Verify playwright-cli connection**: Take a `browser_screenshot` to confirm the extension is active
2. **Navigate to target**: If a URL is provided, `browser_navigate` to it.
   Otherwise ask the user:

```
AskUserQuestion:
  "What is your app's URL? (You must already be logged in via Chrome)"
  Options:
    - "http://localhost:3000"
    - "http://localhost:5173"
    - "http://localhost:8080"
    (User can type custom URL)
```

3. If no category specified, ask the user:

```
AskUserQuestion:
  "Which area of your app should I audit?"
  Options:
    - "Dashboard" (overview, widgets, charts, KPIs)
    - "Data Management" (tables, lists, CRUD, search/filter)
    - "Form Workflow" (multi-step forms, input validation, submission)
    - "Navigation Shell" (sidebar, top-bar, command palette, breadcrumbs)
    - "Settings & Profile" (user settings, preferences, account)
```

4. Create output directory:
```bash
mkdir -p docs/ux-gap-reports/screenshots
```

5. Generate report filename: `docs/ux-gap-reports/YYYY-MM-DD-{category}.md`

### Phase 1: App Discovery

Using the authenticated session, explore the app structure:

1. **Screenshot current state**: `browser_screenshot` to see the logged-in app
2. **Snapshot for navigation**: `browser_snapshot` to get the accessibility tree
3. **Identify navigation elements**: Find sidebar links, top-bar menus, breadcrumbs from the snapshot
4. **Map available routes**: List the major sections/pages discoverable from navigation
5. **Report discovered routes** to the user before proceeding with scenarios

### Phase 2: Scenario Execution

Execute the scenarios defined in `categories.md` for the selected category.

For EACH step in each scenario:

1. **Snapshot the page**: `browser_snapshot` to get element refs
2. **Perform the action** using the ref:
   - Navigation: `browser_click` on nav links or `browser_navigate`
   - Interactions: `browser_click`, `browser_hover`
   - Text input: `browser_type`
   - Dropdowns: `browser_select_option`
   - Keyboard: `browser_press_key`
   - Wait for load: `browser_wait` (1-3 seconds for transitions)
3. **Screenshot**: `browser_screenshot` after the action
4. **Save screenshot** to `docs/ux-gap-reports/screenshots/target-{scenario}-{step}.png`

### Phase 3: Gap Analysis

Use `mcp__sequential-thinking__sequentialthinking` to analyze each dimension:

#### 3a. Screenshot Review (Vision)

For each captured screenshot:
- Analyze visual quality, consistency, polish
- Compare against known best practices from top-tier SaaS apps
- Note specific elements that fall short

#### 3b. Score Each Dimension (0-100)

Apply the scoring rubric from `scoring-rubric.md`:

1. **Typography & Spacing** (25 points max)
2. **Interactive States** (25 points max)
3. **Content Hierarchy** (25 points max)
4. **Loading & Error UX** (25 points max)

**Overall Score** = Sum of all dimensions (0-100)

Reference benchmarks (what top-tier looks like):
- **Linear**: Micro-interactions, skeleton loading, dark theme polish, keyboard shortcuts
- **Notion**: Content blocks, drag-and-drop, inline editing, empty states
- **Vercel**: Dashboard layout, deployment cards, real-time status updates
- **Stripe**: Form validation, data tables, error handling, documentation quality
- **Figma**: Toolbar interactions, canvas controls, collaborative indicators

#### 3c. Generate Fix Recommendations

For each gap scored below 75:
- Describe the specific gap with concrete examples
- Reference what top-tier apps do differently (by known patterns)
- Provide actionable CSS/code fix suggestions
- Classify priority: Critical (< 50) / Moderate (50-75)

### Phase 4: Report Generation

Write the Markdown report to `docs/ux-gap-reports/YYYY-MM-DD-{category}.md`:

```markdown
# UX Gap Report: {project-name} -- {category}

**Date**: YYYY-MM-DD
**Target**: {target-url}
**Category**: {category}
**Session**: Authenticated (user's browser profile via playwright-cli)

## Overall Score: {score}/100

| Dimension | Score | Verdict |
|-----------|-------|---------|
| Typography & Spacing | {n}/25 | {Excellent/Good/Needs Work/Poor/Critical} |
| Interactive States | {n}/25 | {verdict} |
| Content Hierarchy | {n}/25 | {verdict} |
| Loading & Error UX | {n}/25 | {verdict} |

---

## Critical Gaps (Score < 50)

### 1. {Gap Title} ({score}/{max})

**What top-tier apps do**: {description, referencing Linear/Notion/Stripe etc.}

**Your app**:
![target](./screenshots/target-{scenario}-{step}.png)

**Gap**: {Specific description}

**Fix**: {Actionable recommendation with code example}

---

## Moderate Gaps (Score 50-75)
...

## Strengths (Score > 75)
...

## Recommendations Summary

| Priority | Gap | Estimated Effort |
|----------|-----|-----------------|
| Critical | ... | ... |
| Moderate | ... | ... |
```

### Phase 5: Issue Registration

1. Present the gap list to the user:

```
AskUserQuestion (multiSelect: true):
  "Which gaps should be registered as GitHub Issues?"
  Options: [list of Critical and Moderate gaps with scores]
```

2. For each selected gap, create a GitHub Issue:

```bash
gh issue create \
  --title "UX Gap: {gap-title}" \
  --label "ux-gap,priority/{level}" \
  --body "$(cat <<'EOF'
## Gap Detection

**Dimension**: {dimension}
**Score**: {score}/{max}
**Detected**: {date}

## Description

{gap description}

## Screenshots

{screenshot or description}

## Recommended Fix

{actionable fix with code examples}

## Acceptance Criteria

- [ ] Gap score improves to >= 75/{max} on re-audit
EOF
)"
```

---

## Important Notes

### Authenticated Session via playwright-cli

- The skill NEVER logs in itself. The user must already be logged in via Chrome.
- playwright-cli uses the user's real Chrome profile (cookies, sessions, localStorage).
- This means all authenticated SaaS apps are accessible without any credential handling.
- Be careful not to perform destructive actions (delete data, change settings) unless explicitly told to.

### Interaction Pattern

```
browser_snapshot  ->  get element refs
browser_click(ref)  ->  interact with element
browser_wait(1-2s)  ->  wait for transitions
browser_screenshot  ->  capture result
```

Always `browser_snapshot` before interacting to get fresh element refs.

### Screenshot Strategy

- Capture both default and interaction states (hover, focus, active)
- Wait for animations/transitions to complete before capturing
- Name screenshots descriptively for easy identification in the report

### Scope Boundaries

| Will Do | Will NOT Do |
|---------|-------------|
| Use the user's authenticated session | Log into any service |
| Navigate within the app via links/routes | Perform destructive actions (delete, modify data) |
| Take screenshots at each step | Change app settings or preferences |
| Hover/click to test interactive states | Submit real forms with production data |
| Score across 4 dimensions | Access pages the user hasn't navigated to before |
| Generate actionable report | Bypass any security measures |
| Create GitHub Issues | Close the user's browser tabs |

---

## Success Criteria

- [ ] playwright-cli connection verified (screenshot taken)
- [ ] User's authenticated app navigated successfully
- [ ] App navigation structure discovered
- [ ] Category-specific scenarios executed with screenshots
- [ ] All 4 dimensions scored with specific evidence
- [ ] Markdown report generated with screenshot references
- [ ] Report includes actionable fix recommendations referencing top-tier apps
- [ ] User offered GitHub Issue creation for gaps
