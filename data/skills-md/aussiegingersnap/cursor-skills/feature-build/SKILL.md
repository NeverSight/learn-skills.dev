---
name: feature-build
description: Orchestrator skill for the complete feature development lifecycle. Coordinates 5 phases - task selection, component design, build loop, analytics setup, and commit/documentation. Use when building any new feature or enhancement that requires multiple steps.
skill_type: orchestrator
---

# Feature Build Skill

Orchestrates the complete feature development lifecycle with clear phases, entry/exit criteria, and conversation loop patterns. This skill transforms feature requests into shipped, tested, and documented code.

## Contract

**Inputs:**
- Feature request or task from TASKS.md
- Project with existing component structure (components/ui/)
- (Optional) Style guide page for component development

**Outputs:**
- Working feature verified in browser
- Components exported from barrel file
- PostHog analytics instrumented
- TASKS.md and CHANGELOG.md updated
- Clean git commit(s) with conventional format

**Success Criteria:**
- [ ] All acceptance criteria pass in browser testing
- [ ] No console errors or build failures
- [ ] Analytics events firing correctly
- [ ] Documentation updated

## Philosophy

### Core Principles

1. **Acceptance Criteria First** — Define what "done" looks like before writing code. Testable criteria prevent scope creep and enable verification.

2. **Components Live in Style Guide** — Every UI component starts in the style-guide page. This ensures reusability, documents all states, and provides a living reference.

3. **Test What You Build** — Use browser tools to verify each step. Don't wait until the end to discover issues.

4. **KISS (Keep It Simple, Stupid)** — Implement the simplest solution that meets the criteria. Avoid over-engineering.

5. **Loop Back, Don't Push Forward** — When something doesn't work, return to the appropriate phase rather than patching around issues.

### Conversation Loop Model

Features are built through phases that can loop back when issues arise:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────┐ │
│  │  Task    │──▶│Component │──▶│  Build   │──▶│Analytics │──▶│   Build     │ │
│  │Selection │   │ Design   │   │  Loop    │   │  Setup   │   │Verification │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └─────────────┘ │
│       ▲              │              │              │               │          │
│       │              ▼              ▼              ▼               ▼          │
│       │         ◀────────────◀─────────────◀──────────────────────────────────│
│       │         (loop back if criteria fail or build errors)                  │
│       │                                                                       │
│       │                                                    ┌──────────────┐   │
│       └────────────────────────────────────────────────────│   Commit &   │◀──│
│                (next feature)                              │  Document    │   │
│                                                            └──────────────┘   │
└───────────────────────────────────────────────────────────────────────────────┘
```

### Relationship to Other Skills

- **design-system** — Reference for UI patterns, component design principles, style-guide template
- **feature-gating** — Use when building pro/freemium features with PostHog flags
- **versioning** — Follow semantic versioning for releases

---

## Phase 1: Task Selection

### Entry Criteria
- Fresh conversation or user requests a feature
- TASKS.md exists in project

### Actions

1. **Read TASKS.md** — Identify the next item from Current Sprint
   ```
   Read TASKS.md and identify the next unchecked item in Current Sprint
   ```

2. **Confirm Scope** — Clarify with user what's included and excluded
   - What exactly should this feature do?
   - What should it NOT do?
   - Are there edge cases to consider?

3. **Break Down if Complex** — Split large features into sub-tasks
   - Each sub-task should be completable in one conversation
   - Sub-tasks should have clear dependencies

4. **Define Acceptance Criteria** — Write testable criteria

### Acceptance Criteria Format

```markdown
### Feature: [Name]

**Acceptance Criteria:**
- [ ] User can [specific action]
- [ ] System [specific behavior] when [condition]
- [ ] Error case: [scenario] displays [message]
- [ ] Mobile: [behavior] works on viewport < 768px
```

### Exit Criteria
- [ ] Feature scope is clearly defined
- [ ] Acceptance criteria are written and agreed
- [ ] Sub-tasks identified if feature is complex

---

## Phase 2: Component Design

### Entry Criteria
- Feature scope is clear
- Acceptance criteria are defined

### Actions

1. **Check Style Guide First** — Look for existing components that can be reused or extended
   ```
   Navigate to /style-guide and snapshot to see existing components
   ```

2. **Design in Style Guide** — Build new components in the style-guide page
   - Components should be isolated and reusable
   - Import from `components/ui/` barrel file
   - Export new components from barrel file

3. **Show All States** — Document every component state:
   - Default/resting
   - Hover/focus
   - Loading/pending
   - Success/complete
   - Error/invalid
   - Disabled
   - Empty (if applicable)

4. **Mobile Considerations** — Test responsive behavior
   - Use PhoneFrame component for mobile mockups if available
   - Consider touch targets (min 44px)

### Style Guide Section Template

```tsx
<section id="my-component">
  <SectionHeader title="My Component" />
  
  <div className="space-y-6">
    <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
      Variants
    </h4>
    <div className="flex flex-wrap gap-3">
      <MyComponent variant="default" />
      <MyComponent variant="secondary" />
    </div>
    
    <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
      States
    </h4>
    <div className="flex flex-wrap gap-3">
      <MyComponent loading />
      <MyComponent disabled />
      <MyComponent error="Error message" />
    </div>
  </div>
</section>
```

### Exit Criteria
- [ ] Components visible in `/style-guide`
- [ ] All states documented and interactive
- [ ] Components exported from `components/ui/index.ts`
- [ ] Responsive behavior verified

---

## Phase 3: Build Loop

### Entry Criteria
- Components designed and in style-guide
- Acceptance criteria ready for testing

### Actions

#### 3.1 Backend First
Build data layer and API before wiring to UI:

1. **Database schema** — Add migrations if needed
2. **Service layer** — Business logic functions
3. **API routes** — REST endpoints with Zod validation
4. **Test API** — Use browser network panel or curl to verify

#### 3.2 Frontend Integration
Wire components to backend:

1. **State management** — Zustand store or React state
2. **API hooks** — Data fetching with proper loading/error states
3. **Component wiring** — Connect UI to state and actions

#### 3.3 Browser Testing
Test at each step using Cursor browser tools:

```
1. Navigate to the page being tested
2. Snapshot to get element references
3. Interact with elements (click, type, etc.)
4. Re-snapshot after state changes
5. Verify expected behavior
6. Screenshot if visual verification needed
```

**See `references/testing-patterns.md` for detailed testing scenarios.**

### Testing Checklist by Component Type

**Forms:**
- [ ] Valid submission works
- [ ] Validation errors display correctly
- [ ] Loading state during submission
- [ ] Success feedback shown
- [ ] Error handling for API failures

**Lists/Tables:**
- [ ] Items render correctly
- [ ] Empty state displays
- [ ] Pagination/infinite scroll works
- [ ] CRUD operations update UI
- [ ] Loading skeleton shows

**Modals/Dialogs:**
- [ ] Opens on trigger
- [ ] Closes on backdrop click
- [ ] Closes on escape key
- [ ] Form inside modal works
- [ ] Focus management correct

**Navigation:**
- [ ] Routes load correctly
- [ ] Active state shows current page
- [ ] Mobile menu works
- [ ] Deep links work

### Loop Back Triggers

Return to **Phase 2** if:
- Component needs additional states not designed
- UI pattern isn't working as expected
- Need to refactor component API

Return to **Phase 1** if:
- Scope is unclear or expanding
- Acceptance criteria need revision
- Feature should be split differently

### Exit Criteria
- [ ] All acceptance criteria pass in browser
- [ ] No console errors
- [ ] Mobile viewport tested (if applicable)
- [ ] Error states handled gracefully

---

## Phase 4: Analytics Setup

### Entry Criteria
- Feature is working in browser
- All acceptance criteria pass

### Actions

1. **Identify Tracking Needs** — What user actions matter?

   | Feature Type | Typical Events |
   |-------------|----------------|
   | Form | `{form}_submitted`, `{form}_error` |
   | Feature | `{feature}_used`, `{feature}_completed` |
   | Navigation | `{page}_viewed` |
   | Pro Feature | `{feature}_attempted`, `{feature}_upgrade_shown` |

2. **Implement Events** — Add PostHog capture calls
   ```typescript
   posthog.capture('{feature}_{action}', {
     feature: 'feature-name',
     // action-specific properties
   })
   ```

3. **Create Dashboard (if appropriate)** — Use PostHog MCP tools
   ```
   Use mcp_posthog-study-bible_dashboard-create for new dashboards
   Use mcp_posthog-study-bible_insight-create-from-query for insights
   ```

4. **Pro Features** — If feature is gated, follow feature-gating skill:
   - Create PostHog feature flag
   - Implement `useProFeature()` hook
   - Track `_attempted`, `_upgrade_shown`, `_upgrade_clicked` events

### Event Naming Convention

```
{feature}_{action}

Examples:
- notes_created
- notes_synced
- chat_message_sent
- upgrade_modal_shown
- model_changed
```

### Exit Criteria
- [ ] Key user actions instrumented
- [ ] Events firing correctly (verify in PostHog)
- [ ] Dashboard created (if feature warrants it)
- [ ] Pro feature flags configured (if applicable)

---

## Phase 5: Build Verification

### Entry Criteria
- Feature is working in browser
- Analytics implemented (or skipped if not applicable)

### Actions

1. **Run Production Build**
   ```bash
   npm run build
   ```
   - Must complete with exit code 0
   - Fix any TypeScript errors
   - Fix any framework-specific build errors (unused exports, client/server boundaries, etc.)

2. **Check Linter**
   ```bash
   npm run lint
   ```
   - Fix any lint errors (warnings acceptable)

3. **Verify No Regressions**
   - If build fails, loop back to Phase 3 to fix issues
   - Do NOT proceed to commit until build passes

### Loop Back Triggers

Return to **Phase 3** if:
- TypeScript errors in new/modified files
- Build errors related to imports or exports
- Client/server component boundary issues

### Exit Criteria
- [ ] `npm run build` succeeds with exit code 0
- [ ] `npm run lint` passes (no errors)
- [ ] No TypeScript errors

---

## Phase 6: Commit & Document

### Entry Criteria
- Feature complete and tested
- Analytics implemented
- Build verification passed

### Actions

1. **Update TASKS.md**
   - Move completed items to Completed section
   - Add completion date
   - Check off sub-tasks
   - Add any new backlog items discovered

2. **Update CHANGELOG.md**
   - Add entry under current version or "Unreleased"
   - Summarize what was added/changed/fixed
   - Reference any breaking changes

3. **Stage and Commit**
   - Use conventional commit format
   - Keep commits atomic (one logical change per commit)

### Conventional Commit Format

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert
```

### Commit Summary Block

Provide at end of feature for easy copy-paste:

```markdown
### Done

**Summary**: [Brief description of what was built]

**Commits** (ohmyzsh):
gaa && gcmsg "feat(scope): add feature description"
gcmsg "fix(scope): fix related issue"
gp
```

### TASKS.md Update Pattern

```markdown
## Completed

- [x] Feature name (YYYY-MM-DD)
  - [x] Sub-task 1 ✓
  - [x] Sub-task 2 ✓
  - [x] Sub-task 3 ✓
```

### Exit Criteria
- [ ] TASKS.md updated with completion status
- [ ] CHANGELOG.md updated with feature summary
- [ ] Clean commit(s) with conventional format
- [ ] Ready for next feature

---

## Quick Reference

### Phase Entry/Exit Summary

| Phase | Entry | Exit |
|-------|-------|------|
| 1. Task Selection | Feature request | Criteria defined |
| 2. Component Design | Criteria clear | Components in style-guide |
| 3. Build Loop | Components ready | All criteria pass in browser |
| 4. Analytics | Feature working | Events instrumented |
| 5. Build Verification | Analytics done | `npm run build` succeeds |
| 6. Commit | Build passes | Docs updated, committed |

### Common Commands

```bash
# Start dev server
npm run dev

# Clear Next.js cache if issues
rm -rf .next

# Rebuild native modules
npm rebuild better-sqlite3

# Git workflow (ohmyzsh)
gaa && gcmsg "feat(scope): description"
gp
```

### Browser Testing Quick Reference

```
1. mcp_cursor-ide-browser_browser_navigate → load page
2. mcp_cursor-ide-browser_browser_snapshot → get elements
3. mcp_cursor-ide-browser_browser_click/type → interact
4. mcp_cursor-ide-browser_browser_snapshot → verify changes
5. mcp_cursor-ide-browser_browser_take_screenshot → visual check
```
