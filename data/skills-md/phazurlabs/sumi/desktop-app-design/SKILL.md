---
name: desktop-app-design
description: "Desktop and enterprise application patterns: data-dense interfaces, dashboards, data tables, keyboard-first interaction, multi-window layouts, and data visualization. Use when designing an admin panel, analytics dashboard, or professional tool with complex workflows."
---

# Desktop App Design — Professional & Enterprise Excellence

## Desktop Design Philosophy

Desktop applications serve users who invest hours of focused attention in professional workflows. Unlike mobile's brief, task-focused interactions, desktop design must optimize for sustained productivity, information density, and expert efficiency. The challenge is supporting both first-day learnability and thousandth-day mastery within the same interface.

### Core Principles (Edward Tufte + Jony Ive)

1. **Information density with clarity** — show more data without increasing cognitive load (Tufte: "maximize data-ink ratio")
2. **Invisible design** — the interface should disappear, leaving only the work (Ive: "true simplicity is derived from so much more than just the absence of clutter")
3. **Keyboard-first, mouse-enhanced** — power users live on the keyboard; mouse interaction is the fallback
4. **Progressive complexity** — simple surface, deep capability accessible through exploration
5. **Spatial memory** — consistent layouts allow users to develop muscle memory over months of use

## Dashboard Design

### Dashboard Types

**Operational Dashboards**
- Real-time monitoring with auto-refresh (5-30 second intervals)
- Status-at-a-glance with clear normal/warning/critical states
- Anomaly detection with visual emphasis on outliers
- Minimize decoration — every pixel serves monitoring goals

**Analytical Dashboards**
- Interactive exploration with filter, drill-down, and cross-filtering
- Comparison-oriented: support time-range, segment, and baseline comparisons
- Export and sharing capabilities for collaborative analysis
- Allow users to create and save custom views

**Strategic Dashboards**
- KPI-focused with trend indicators and goal tracking
- Executive summary level — 5-7 key metrics maximum
- Contextual benchmarks (vs. target, vs. last period, vs. industry)
- Minimal interaction needed — the story should be immediately clear

### Dashboard Layout Principles

- **F-pattern reading:** Place the most critical metric top-left, summary row at top
- **Card-based layout:** Each card is one complete thought — metric + context + trend
- **Consistent grid:** 12-column grid with standardized card sizes (1/4, 1/3, 1/2, full)
- **Information hierarchy:** Primary numbers large (24-48px), secondary context small (12-14px)
- **Color as data:** Use color to encode meaning (red=bad, green=good), not decoration
- **White space as separator:** Generous padding between cards reduces cognitive switching cost

### Data Visualization Best Practices (Tufte)

- Choose chart types based on the relationship being shown: comparison → bar, trend → line, composition → stacked bar, distribution → histogram
- Label data directly rather than using legends when possible
- Eliminate chartjunk: unnecessary gridlines, 3D effects, decorative elements
- Use consistent axis scales across comparable charts
- Small multiples (repeated small charts) outperform single complex charts for comparison
- Accessible color palettes: ensure distinguishability for color vision deficiency

## Data Table Design

### Table Architecture

- **Fixed headers** that persist during vertical scroll
- **Fixed key columns** (usually first 1-2) that persist during horizontal scroll
- **Row height:** 40-52px standard, 32px compact mode for data-heavy views
- **Column resizing** by dragging column borders
- **Column reordering** by drag-and-drop headers
- **Row striping** (subtle alternating background) for wide tables — optional for narrow ones

### Table Functionality

- **Sorting:** Click column header to sort; show direction indicator; support multi-column sort
- **Filtering:** Column-level filters with appropriate types (text search, range, multi-select)
- **Search:** Global search across all visible columns with result highlighting
- **Pagination vs. infinite scroll:** Pagination for data manipulation tasks, infinite scroll for browsing
- **Bulk actions:** Checkbox selection with select-all, action toolbar appears on selection
- **Inline editing:** Double-click to edit cells for quick corrections; full edit mode for complex changes
- **Export:** CSV, Excel, PDF with current filter/sort state preserved

### Table Density Modes

- **Comfortable:** 52px rows, generous padding — default for general audiences
- **Standard:** 40px rows — default for data-oriented users
- **Compact:** 32px rows, smaller text — for power users managing large datasets
- Allow users to toggle density preference with persistent setting

## Complex Workflow Design

### Multi-Step Workflows
- **Progress indicator:** Show current step, total steps, and completion state
- **Non-linear navigation:** Allow jumping to completed steps for editing
- **Save draft at every step** — never lose user work on navigation
- **Summary/review step** before final submission
- **Clear step labels** that describe the content, not just "Step 1, Step 2"

### Form-Heavy Interfaces
- **Section grouping** with clear headings and optional collapse
- **Contextual help** near complex fields — info icons with tooltips or inline descriptions
- **Dependent fields:** Show/hide fields based on previous selections
- **Auto-save with visual confirmation** (subtle "Saved" indicator)
- **Validation summary** at top of form linking to each error field

### Master-Detail Pattern
- **List/grid on left, detail panel on right** — the dominant desktop productivity pattern
- Support resizable split panes
- Detail panel updates without full page reload
- Keyboard navigation: arrow keys traverse list, Enter opens detail, Escape returns to list
- Mobile adaptation: replace side-by-side with stack navigation

## Keyboard-First Interaction

### Essential Keyboard Patterns
- **Global shortcuts:** Document common shortcuts in an overlay (? or Ctrl+/)
- **Command palette:** Cmd/Ctrl+K for quick action access — the most important desktop UX innovation of the 2020s
- **Tab order:** Logical focus progression through interactive elements
- **Focus indicators:** Always visible, high-contrast focus rings (never remove outline without replacement)
- **Escape key:** Consistently closes modals, dropdowns, and cancels operations

### Shortcut Design Rules
- Follow platform conventions (Ctrl/Cmd+S = Save, Ctrl/Cmd+Z = Undo)
- Avoid overriding browser shortcuts
- Use modifier combinations logically: Ctrl = action, Shift = modify/extend, Alt = alternate
- Provide visual shortcut hints in menus, tooltips, and command palette

## Multi-Window and Panel Management

### Panel Patterns
- **Sidebar navigation:** Collapsible, persistent across views, icon+label or icon-only modes
- **Inspector panels:** Right-side contextual properties panel (design tool pattern)
- **Bottom panels:** Console, log, terminal outputs — resizable with collapse
- **Floating panels:** Detachable for multi-monitor workflows

### State Management
- Persist panel states (open/closed, sizes) across sessions
- Remember user's last-used view and filters
- Support workspace presets ("Developer layout", "Review layout")
- Handle window resize gracefully — responsive desktop is essential for varied monitor sizes

## Enterprise-Specific Patterns

### Permission-Aware UI
- Hide elements users cannot access (not just disable) for cleaner interfaces
- For disabled elements that provide context, show tooltip explaining why access is restricted
- Role-based views: admin sees all controls, viewer sees read-only, etc.
- Audit trails for sensitive actions with clear attribution

### Notification and Alert Design
- **Severity levels:** Info (blue), Success (green), Warning (amber), Error (red), Critical (red + icon)
- **Position:** Non-blocking toasts for confirmations, blocking modals for critical decisions
- **Persistence:** Success toasts auto-dismiss (3-5s), errors persist until addressed
- **Grouping:** Batch similar notifications to prevent notification fatigue

### Empty States and Onboarding
- First-run experience should guide users to first value moment
- Empty states include illustration, explanation, and clear CTA to populate the view
- Progressive onboarding: introduce features as they become relevant, not all at once
- In-app guidance: highlight new features with subtle callouts, dismissible permanently

## Routing

For **dense data surfaces** — the data table deep dive, inline editing, grid vs
table, master-detail, complex forms, wizards, command palette design, keyboard
shortcut systems, and multi-window layouts: read
`references/data-dense-interfaces.md`.

For **dashboards** — information architecture, the widget and card system, chart
selection, accessible data-viz palettes, real-time patterns, filter and
drill-down, personalization, responsive dashboard layout, and loading states:
read `references/enterprise-dashboard-patterns.md`.

For **an industry's conventions** — healthcare, financial services, e-commerce,
SaaS/B2B, education, and real-time collaboration: read
`references/industry-vertical-patterns.md`.

For **chart-type depth** shared with data visualization: read
`references/data-visualization-patterns.md`.

## Cross-Referencing

- For data visualization accessibility, reference `accessibility-inclusive-design`
- For design token systems, reference `design-systems-architecture`
- For interaction and transition design, reference `interaction-motion-design`
- For UX evaluation, reference `nng-ux-heuristics`

## v3.0 Cross-References

The v3.0 upgrade introduces comprehensive data visualization references, production component patterns, and design tool workflows that extend desktop application design capabilities.

### Data Visualization Patterns — `references/data-visualization-patterns.md`

The new `references/data-visualization-patterns.md` reference expands significantly on the Data Visualization Best Practices section above. It covers: comprehensive chart type selection guides with decision trees (when to use bar vs. column, line vs. area, scatter vs. bubble, treemap vs. sunburst); accessible data visualization patterns including screen reader-compatible chart descriptions, sonification approaches, and tactile-friendly data encoding; and dashboard composition frameworks for arranging multiple visualizations into coherent analytical narratives. Includes real-world examples of dashboard redesigns with before/after performance metrics.

### Production Component Patterns — `component-patterns-code`

The `component-patterns-code` skill provides production-ready React component patterns directly applicable to desktop application design. Includes data table components with full state matrices (loading, empty, error, paginated, filtered, sorted, bulk-selected), command palette implementations, master-detail layout components, resizable panel systems, and keyboard-navigable tree views. Each component cookbook entry includes TypeScript types, accessibility annotations, and Storybook configurations — bridging the gap between the design patterns in this skill and production code.

### Design Tool Workflows — `figma-design-tool-workflows`

The `figma-design-tool-workflows` skill covers the Figma-to-code pipeline applicable to desktop design systems. Relevant capabilities include: Figma variable modes for light/dark/high-contrast theme switching; auto-layout configurations that map to CSS Grid and Flexbox; component property definitions that generate developer handoff specifications; and the MCP-powered design-to-code flywheel that enables continuous synchronization between Figma design system files and production component libraries. Particularly valuable for desktop apps with complex theming requirements and dense component libraries.

## Key Sources

- Tufte, E. (2001). "The Visual Display of Quantitative Information"
- Cooper, A. (2014). "About Face: The Essentials of Interaction Design"
- Microsoft Fluent Design System guidelines
- Apple macOS Human Interface Guidelines
- NNG Group enterprise UX research
