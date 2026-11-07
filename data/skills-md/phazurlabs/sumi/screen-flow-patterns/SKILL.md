---
name: screen-flow-patterns
description: "Taxonomy of 25+ screen types, 15+ user flows, and 25+ UI element deep-dives with layout patterns, component hierarchies, state matrices, and best-in-class references. Use when deciding which screens a product needs and what connects them, before any visual design starts."
---
# Screen and Flow Patterns

## Mental model

Before anything is styled, two questions decide the shape of a product: **which
screens exist**, and **what connects them**. Getting this wrong is expensive in a
way visual decisions never are -- you can restyle a screen in an afternoon; you
cannot re-architect a flow after it ships without breaking people's habits.

- **Name the screen type before designing it.** Nearly every screen is an
  instance of a known type with known states and a known failure mode. "A page
  where users manage their team" is a List/Feed with an invite flow attached, and
  saying so imports thirty solved decisions.
- **A flow is a sequence with an exit at every step.** If a step has no way back
  and no way out, it is a trap, and traps are where support tickets come from.
- **Design the states, not the screen.** The happy path is the easy fifth of the
  work. The other four fifths are empty, loading, error and partial.
- **Density is a decision, not a consequence.** Pick a tier and hold it.

## Constants

Every screen ships all five. A screen specified only in its ideal state is not
specified.


Every screen passes through states. Model them explicitly to ensure all states are designed.

### 6.1 The Five Core States

```
[Initial] -> [Loading] -> [Loaded / Populated]
                |               |
                v               v
            [Error]       [Empty]
                |               |
                v               v
           [Retry -> Loading]  [Action -> Loading]
```

1. **Initial**: Screen is mounted but no data request has fired yet. Often invisible (immediate transition to Loading).
2. **Loading**: Data is being fetched. Show skeleton screens (preferred), spinner, or shimmer. Never show a blank screen.
3. **Loaded / Populated**: Data received and displayed. The "happy" state. Most design time is spent here.
4. **Empty**: Data request succeeded but returned zero items. Show empty state illustration + CTA.
5. **Error**: Data request failed. Show error message + retry button. Distinguish between network error, server error, and permission error.

### 6.2 Extended States

- **Refreshing**: Pulling to refresh or background sync. Show inline indicator without replacing content.
- **Partial Load**: Some data loaded, more available. Infinite scroll loading indicator at bottom.
- **Stale**: Data is old. Show "last updated" timestamp. Background refresh in progress.
- **Offline**: No network connection. Show cached data with offline banner. Queue actions for sync.
- **Permission Required**: User has not granted necessary permission (location, camera, contacts). Show explanation + request button.

### 6.3 State Design Checklist

For every screen, verify you have designed:
- [ ] Loading state (skeleton or spinner)
- [ ] Populated state (with real data, not lorem ipsum)
- [ ] Empty state (zero items, with helpful CTA)
- [ ] Error state (with clear message and retry)
- [ ] Partial/paginated state (loading more indicator)
- [ ] Offline state (if applicable)
- [ ] Permission request state (if applicable)

---

## Section 7: Information Density Levels


### 7.1 Three Density Tiers

| Tier | Description | Target Elements per Viewport | Example Screen Types |
|------|-------------|------|------|
| **Low** | Breathing room. One idea per fold. Marketing-oriented. | 3-5 | Landing, onboarding, login, confirmation, empty state, error pages |
| **Medium** | Balanced. Content-rich but not overwhelming. Scrolling expected. | 6-12 | Profile, detail, settings, blog/article, checkout, contact |
| **High** | Data-dense. Power users. Scanning and filtering essential. | 12-25+ | Dashboard, analytics, file manager, data table, calendar, comparison |

### 7.2 Density Adjustments by Platform

- **Mobile**: Reduce density by 30-40% vs desktop. Stack columns. Collapse secondary info behind taps.
- **Tablet**: Intermediate density. Use split views to maintain context without overwhelming.
- **Desktop**: Highest density acceptable. Multi-column layouts, sidebars, persistent panels.

### 7.3 Density Controls for Users

- **Comfortable / Cozy / Compact**: Gmail-style density toggle. Adjusts row height and spacing.
- **Card / List / Table**: View mode toggle. Cards are lowest density, tables are highest.
- **Show/Hide Columns**: Let users configure which columns appear in data tables.
- **Collapse Panels**: Resizable and collapsible sidebars for user-controlled density.

---

## Section 8: Platform-Specific Screen Conventions

## Index

**Screen types (32)** -- full specification for each in
`references/screen-type-catalog.md`:

Landing · Home/Dashboard · List/Feed · Detail/Show · Profile · Settings ·
Search/Results · Checkout · Onboarding · Login · Sign-up · Forgot Password ·
Empty State · Error 404 · Error 500 · Maintenance · Loading/Splash ·
Notifications Center · Analytics/Reporting · File Manager · Editor/Canvas ·
Wizard/Multi-Step · Chat/Messaging · Calendar · Map View · Comparison ·
About/Team · Contact · Blog/Article · Product Gallery · Booking/Reservation ·
Confirmation/Success

**Flow patterns (22)** -- full specification for each in
`references/user-flow-catalog.md`:

Authentication · Onboarding · Purchase/Checkout · Search-Filter-Select · CRUD ·
Invite/Share · Communication · Notification-to-Action · Upgrade/Upsell ·
Cancellation/Churn · Help/Support · Data Import/Export · Review/Rating ·
Onboarding Checklist · Collaborative Editing · Subscription/Renewal · Referral ·
Multi-Device Handoff · Account Deletion · Error Recovery · Settings Management ·
Content Creation

**UI elements (120+)** across navigation, input, feedback, overlay and layout --
`references/ui-element-deep-dive.md`.


When documenting or communicating user flows, use these standardized conventions.

### 3.1 Node Types
- **Start / End**: Rounded rectangle (pill shape). Green for start, red for end.
- **Screen / Page**: Rectangle. Contains screen name. Color-coded by section.
- **Decision**: Diamond. Contains yes/no or conditional question.
- **Action**: Rectangle with rounded corners. User or system action.
- **Sub-flow**: Rectangle with double border. Links to separate flow diagram.
- **Wait / Delay**: Hourglass or clock icon. Async step (email verification, processing).

### 3.2 Path Types
- **Happy Path**: Solid green arrows. The primary expected journey.
- **Error Path**: Dashed red arrows. What happens when things fail.
- **Alternative Path**: Dotted blue arrows. Valid but less common routes.
- **Escape Hatch**: Gray arrows. Exit points (cancel, back, close).

### 3.3 Entry Points
- **Direct URL**: Globe icon. User arrives via typed URL or link.
- **Deep Link**: Chain icon. From push notification, email, or external app.
- **Navigation**: Menu icon. From in-app navigation.
- **System Trigger**: Gear icon. Automated redirect (session expire, maintenance).

### 3.4 Edge Case Annotations
- **Conditional**: Annotate arrows with conditions (e.g., "if cart > $50").
- **Frequency**: Label paths with expected traffic percentage (e.g., "80% of users").
- **Data Dependencies**: Note when a step requires data from a previous step.
- **Timeout**: Note time limits (e.g., "OTP expires in 10 min").

---

## Section 4: UI Element Pattern Catalog (120+ Elements)

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/screen-type-catalog.md` | 32 screen types, fully specified | 1731 |
| `references/ui-element-deep-dive.md` | 120+ elements, 26 in depth | 1259 |
| `references/user-flow-catalog.md` | 22 flows step by step | 1116 |
| `references/inspiration-reference-guide.md` | where to look for precedent | 228 |
| `references/transitions-and-platform-conventions.md` | push, modal, tab, deep link; iOS/Android/web | 84 |

## What every reference file contains

1. Purpose -- the one job this screen or flow does
2. The component hierarchy, named
3. The state matrix: empty, loading, error, partial, ideal
4. Accessibility requirements specific to the type
5. Best-in-class examples, named
6. The failure mode that type is known for

## Routing

For **deciding which screens a product needs** and the full specification of
each: read `references/screen-type-catalog.md`.

For **the sequence connecting them** -- entry points, steps, decision points,
exits and error branches: read `references/user-flow-catalog.md`.

For **a specific element** -- navigation, input, feedback, overlay or layout:
read `references/ui-element-deep-dive.md`.

For **how screens move between each other** and what each platform expects:
read `references/transitions-and-platform-conventions.md`.

For **precedent** -- where to look and what to look for: read
`references/inspiration-reference-guide.md`.

## Cross-References

- `page-composition-engine` -- once the screen type is chosen, this composes it
- `navigation-pattern-encyclopedia` -- the navigation connecting the screens
- `performance-states-patterns` -- the empty, loading and error states in depth
- `ui-pattern-intelligence` -- whether the pattern chosen is still current
- `mobile-ux-design` -- the mobile form of each screen type
