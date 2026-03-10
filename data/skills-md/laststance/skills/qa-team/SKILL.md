---
name: qa-team
description: |
  Launch comprehensive QA Agent Team for post-implementation verification.
  Tests 5 perspectives in parallel using AGENT_TEAMS: Visual Integrity,
  Functional Correctness (with Impact Propagation), Apple HIG Compliance,
  Edge Cases, and UX Sensibility. Falls back to Task tool if AGENT_TEAMS unavailable.

  Use when:
  - Implementation is complete and needs QA verification
  - User requests "run QA", "test everything", "quality check"
  - After /workflow completion for end-to-end validation
  - User says "check if the app works", "verify the UI"

  Keywords: "QA team", "quality assurance", "test everything", "visual check",
  "functional test", "edge cases", "UX review", "HIG compliance", "qa-team",
  "run QA", "verify app", "quality gate"
argument-hint: "[--platform web|electron|ios|macos|auto] [--skip visual|functional|hig|edge|ux] [--quick]"
allowed-tools: "Bash,Read,Write,Edit,Glob,Grep,Task,TaskCreate,TaskUpdate,TaskList,TaskGet,TeamCreate,TeamDelete,SendMessage,AskUserQuestion,mcp__claude-in-chrome__*,mcp__plugin_playwright_playwright__*,mcp__electron__*,mcp__ios-simulator__*,mcp__mac-mcp-server__*,mcp__serena__*,mcp__sequential-thinking__*"
---

# QA Agent Team

Comprehensive QA verification team with 5 specialist perspectives + 1 team lead.

## Team Composition

| Role | Model | Agent/Skill Base | Perspective |
|------|-------|-----------------|-------------|
| **qa-lead** | opus | `quality-engineer` | Orchestration, aggregation, final gate |
| **visual-tester** | opus | `gui-phd-*` | Layout, responsive, rendering |
| **functional-tester** | opus | `feature-validator` (enhanced) | User flows + **Impact Propagation** |
| **hig-tester** | opus | `web-design-guidelines` | Apple HIG, WCAG AA+ |
| **edge-case-tester** | opus | `quality-engineer` | Long text, 100+ records, overflow |
| **ux-tester** | opus | `ph-quality-gate` | Dark-on-dark, missing feedback, inconsistency |

## Activation Flow

### Step 1: Prerequisites

1. Ensure dev server / app is running (ask user if unclear)
2. `mkdir -p claudedocs/qa/screenshots`
3. Detect platform from `package.json` (or `--platform` flag):
   - Has `"electron"` → Electron
   - Has `expo` / `app.json` → iOS/Expo
   - Has `.xcodeproj` / `Package.swift` macOS target → macOS
   - Default → Web

### Step 2: Create Agent Team

Use `TeamCreate` tool with team_name `"qa-team"` and description `"QA verification team"`.

**Do NOT do QA work yourself. Only create the team and let teammates work.**

Then spawn 6 teammates using the Task tool with `team_name: "qa-team"`:

**qa-lead** (subagent_type: "general-purpose"):
- Read `~/.claude/agents/quality-engineer.md`
- Create task list with 8 tasks (see dependency graph below)
- Wait for all 5 reports, then aggregate into `claudedocs/qa/qa-summary.md`
- Apply Final Composite Gate from scoring rubric

**visual-tester** (subagent_type: "general-purpose"):
- Read `~/.claude/agents/gui-phd-web-electron.md` (or gui-phd-mobile/gui-phd-macos per platform)
- Execute RALPH protocol screenshot verification at 95% threshold
- Report to `claudedocs/qa/qa-visual-integrity.md`

**functional-tester** (subagent_type: "general-purpose"):
- Read `~/.claude/agents/feature-validator.md`
- Execute 4-Phase Impact Propagation Protocol
- Report to `claudedocs/qa/qa-functional.md`

**hig-tester** (subagent_type: "general-purpose"):
- Read CLAUDE.md Design Policies section
- Check Typography, Tap Areas, Colors, Spacing, Motion, Corner Radius
- Report to `claudedocs/qa/qa-hig-compliance.md`

**edge-case-tester** (subagent_type: "general-purpose"):
- Read `~/.claude/agents/quality-engineer.md`
- Test empty/long text, 100+ records, boundary values, overflow
- Report to `claudedocs/qa/qa-edge-cases.md`
- **blockedBy**: functional-tester task

**ux-tester** (subagent_type: "general-purpose"):
- Apply PH Quality Gate Visual axis (V1-V5, /100)
- Report to `claudedocs/qa/qa-ux-sensibility.md`
- **blockedBy**: visual-tester task

### Step 3: MCP Selection by Platform

| Platform | Primary MCP |
|----------|------------|
| Web | `mcp__claude-in-chrome__*` / `mcp__plugin_playwright_playwright__*` |
| Electron | `mcp__electron__*` |
| iOS/Expo | `mcp__ios-simulator__*` |
| macOS | `mcp__mac-mcp-server__*` |

### Step 4: Enter Delegate Mode

After spawning all teammates, tell the user to press **Shift+Tab** to enter delegate mode.
The lead should coordinate — YOU should not write any QA reports yourself.

### Step 5: Monitor & Aggregate

- qa-lead waits for all 5 reports in `claudedocs/qa/`
- Computes composite score using scoring rubric weights
- Generates `claudedocs/qa/qa-summary.md` with final verdict

### Step 6: Final Quality Gate

| Component | Weight | PASS Threshold |
|-----------|--------|---------------|
| Visual | 25% | 95% Triple-Criteria |
| Functional | 30% | 95% pass rate, P0=0 |
| HIG | 15% | 80/100 composite |
| Edge Cases | 15% | 0 crash |
| UX Sensibility | 15% | PH Visual 75/100, critical=0 |

**>= 85**: PASS / **65-84**: CONDITIONAL PASS / **< 65**: FAIL

## Task Dependency Graph

```
Task 1: [qa-lead] Platform Detection & Test Plan
  ├── Task 2: [visual-tester]     Visual Integrity         (parallel)
  ├── Task 3: [functional-tester] Functional Correctness   (parallel)
  ├── Task 4: [hig-tester]        Apple HIG Compliance     (parallel)
  ├── Task 5: [edge-case-tester]  Edge Cases               (blockedBy: 3)
  ├── Task 6: [ux-tester]         UX Sensibility           (blockedBy: 2)
  ├── Task 7: [qa-lead]           Report Aggregation       (blockedBy: 2,3,4,5,6)
  └── Task 8: [qa-lead]           Final Quality Gate       (blockedBy: 7)
```

## Output Structure

```
claudedocs/qa/
├── qa-test-plan.md              # Platform + test plan
├── qa-visual-integrity.md       # Visual report
├── qa-functional.md             # Functional report (with impact verification)
├── qa-hig-compliance.md         # HIG report
├── qa-edge-cases.md             # Edge case report
├── qa-ux-sensibility.md         # UX sensibility report
├── qa-summary.md                # Aggregated final verdict
└── screenshots/
    ├── visual_*.png
    ├── func_*.png / func_*_impact_*.png
    ├── hig_*.png
    ├── edge_*.png
    └── ux_*.png
```

## Flags

| Flag | Effect |
|------|--------|
| `--platform <type>` | Force platform (skip auto-detection) |
| `--skip <perspective>` | Skip one or more perspectives |
| `--quick` | Only visual + functional (3 teammates instead of 6) |

## References

- `references/qa-scoring-rubric.md` — Detailed scoring criteria per perspective
- `workflows/web-workflow.md` — Web platform test workflow
- `workflows/electron-workflow.md` — Electron test workflow
- `workflows/mobile-workflow.md` — iOS/Expo test workflow
- `workflows/macos-workflow.md` — macOS test workflow

## Completion Criteria

QA session is complete when:
- All 5 individual reports exist with verdicts
- All reports have supporting screenshots
- Composite score calculated in qa-summary.md
- Final verdict rendered (PASS / CONDITIONAL PASS / FAIL)
