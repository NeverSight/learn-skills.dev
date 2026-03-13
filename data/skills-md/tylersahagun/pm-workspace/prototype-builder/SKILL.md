---
name: prototype-builder
description: Build human-centric AI prototypes with multiple creative directions, required states, and interactive flow stories. Use when creating Storybook components or UI mockups.
---

# Prototype Builder Skill

Specialized knowledge for building Storybook prototypes that meet human-centric AI design standards.

## When to Use

- Creating new UI prototypes
- Building Storybook stories
- Implementing AI feature states
- Designing interactive user flows

## Design Principles

### Trust Before Automation

- New features start as suggestions, not automations
- Show receipts (evidence) for every AI decision
- Make confidence levels explicit
- Graceful failure > silent failure

### Emotional Design

- **Visceral**: Does it look trustworthy at first glance?
- **Behavioral**: Does it work predictably?
- **Reflective**: Does user feel augmented, not replaced?

### Persona Awareness

- **Reps fear**: Surveillance, replacement, embarrassment
- **Managers fear**: Losing touch, surveillance culture
- **RevOps fear**: Ungovernable AI, lack of auditability

## Creative Exploration (Required)

For each major component, create 2-3 directions:

| Direction | User Control | Trust Required | Best Persona        |
| --------- | ------------ | -------------- | ------------------- |
| Option A  | Maximum      | Low            | New users, skeptics |
| Option B  | Balanced     | Medium         | Most users          |
| Option C  | Minimal      | High           | Power users         |

## Required AI States

Every AI feature needs ALL states:

| State           | Visual        | Copy              | Animation        |
| --------------- | ------------- | ----------------- | ---------------- |
| Loading (short) | Spinner       | None              | Pulse            |
| Loading (long)  | Progress      | "Analyzing..."    | Transitions      |
| Success         | Check, muted  | Affirming         | Scale+fade 150ms |
| Error           | Warning       | Honest + solution | Gentle shake     |
| Low Confidence  | Muted, dotted | "I think..."      | None             |
| Empty           | Illustration  | Encouraging       | Fade in          |

## Required: Flow Stories

Every prototype MUST include interactive journey stories:

```typescript
export const Flow_HappyPath: Story = {
  render: () => <ComponentJourney scenario="happy" />,
};

export const Flow_ErrorRecovery: Story = {
  render: () => <ComponentJourney scenario="error" />,
};
```

| Prototype Type   | Required Flows                                  |
| ---------------- | ----------------------------------------------- |
| Simple feature   | 1 (happy path)                                  |
| AI feature       | 2 (happy + error)                               |
| Complex workflow | 3+                                              |
| Any feature      | + Discovery flow (how user finds this)          |
| Any feature      | + Activation flow (first-time setup/onboarding) |
| AI feature       | + Day-2 flow (returning user, ongoing value)    |

### Experience Flow Requirements

Every prototype MUST tell the full user story, not just show the feature:

1. **Discovery flow** - How does the user know this feature exists? Start from the user's natural context (e.g., dashboard, sidebar, notification), not from the feature itself.
2. **Activation flow** - What does first-time setup look like? Can the user enable/configure this without CSM assistance?
3. **Day-2 flow** - What does the returning user see? What value compounds over time?

```typescript
export const Flow_Discovery: Story = {
  render: () => <ComponentJourney scenario="discovery" />,
};

export const Flow_Activation: Story = {
  render: () => <ComponentJourney scenario="first-time-setup" />,
};

export const Flow_Day2: Story = {
  render: () => <ComponentJourney scenario="returning-user" />,
};
```

## Required: Interactive Demo + Walkthrough

Every version MUST include:

- **Interactive demo** story (live click-through of the full experience)
- **Walkthrough** story (step-by-step narration of the flow)

```typescript
export const Demo_Clickthrough: Story = {
  render: () => <Demo />,
};

export const Walkthrough: Story = {
  render: () => <Walkthrough />,
};
```

## Codebase Consistency (Required)

Prototypes must look and feel like they belong in the existing app. Before building any component:

### Use What Already Exists

1. **Check `elephant-ai/web/src/components/primitives/`** for available wrapped shadcn/ui components (the buffer layer). Use `Button`, `Card`, `Badge`, `Sheet`, `Dialog`, `Select`, `Input`, `Tabs`, etc. directly from this layer. Do NOT recreate these or use raw shadcn primitives from `ui/`.
2. **Check existing domain folders** in `elephant-ai/web/src/components/` for patterns. If there's already a `health-score/` folder with `HealthScoreCard.tsx`, reference how it structures props, handles states, and applies styles.
3. **Check existing pages** in `elephant-ai/web/src/pages/` or `elephant-ai/web/src/app/` for layout conventions. Match the same padding, spacing, header patterns, and content area structure.
4. **Top-Level Navigation**: If a new page or view requires top-level visibility, it MUST be added to the map in `apps/web/src/components/navigation/top-nav-main.tsx`.

### Match Visual Patterns

- **Theme V2**: Ensure prototypes use the `.theme-v2` CSS class and `@custom-variant v2` where necessary.
- **Card patterns**: Follow the existing Card → CardHeader → CardContent structure with the same spacing (`p-6`, `pt-0`).
- **Semantic Colors**: Use strict semantic tokens (`success-*`, `destruction-*`, `warning-*`, `primary-*`, `secondary-*`, `muted-*`) from the V2 Design System, not raw Tailwind colors like emerald/amber.
- **Typography**: Use the same text size hierarchy (`text-sm` for body, `text-xs` for secondary, `font-medium` for labels).
- **Borders and shadows**: Follow the existing `border bg-card shadow-sm` pattern for cards.
- **Icons**: Use Lucide icons at the same sizes as existing components (`h-4 w-4` inline, `h-5 w-5` standalone).

### When the Design System File May Be Stale

The `.interface-design/system.md` file is a snapshot. If a prototype looks inconsistent with the live app, check the actual source files — `apps/web/src/index.css` and the Storybook file `color-system-v2-demo.stories.tsx` are authoritative over the visual language, and the actual components in `apps/web/src/components/primitives/` are authoritative over component structure.

## Component Structure

Always use versioned folders. The initiative root should contain only `index.ts` and version folders (no loose components or views). All version-specific components (new or adapted AskElephant components) live inside the version folder:

```
prototypes/[Initiative]/
├── index.ts           # Re-exports latest
├── v1/
│   ├── Component.tsx
│   ├── Component.stories.tsx
│   ├── ComponentJourney.tsx
│   ├── Demo.tsx
│   ├── Demo.stories.tsx
│   ├── Walkthrough.tsx
│   ├── Walkthrough.stories.tsx
│   └── types.ts
```

## Tech Stack

- React 18 + TypeScript (strict)
- Tailwind CSS
- shadcn/ui wrappers from `@/components/primitives/`

## Storybook Title Pattern

```typescript
const meta = {
  title: "Prototypes/[Initiative]/v1/[ComponentName]",
  component: ComponentName,
};
```

For demo and walkthrough, use:

```typescript
title: "Prototypes/[Initiative]/v1/Demo";
title: "Prototypes/[Initiative]/v1/Walkthrough";
```

## Image Generation for Mockups (Cursor 2.4)

When a quick visual is needed before building full components, use image generation:

### When to Generate Images

- **Early concept exploration** - Before committing to code
- **Stakeholder communication** - Quick visuals for feedback
- **Design exploration** - Testing multiple directions rapidly
- **Architecture diagrams** - Visualizing data flows or system design

### How to Use

Describe the mockup in natural language:

```
"Generate an image of a dashboard showing user engagement metrics with a sidebar navigation, using a clean modern design with blue accent colors"
```

### Best Practices

- Reference existing design system colors/patterns in descriptions
- Generated images save to `assets/` by default
- Use for exploration, not final implementation
- Follow up with coded Storybook components for production

### Example Prompts

| Use Case         | Prompt Example                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| Dashboard mockup | "A meeting insights dashboard with cards showing action items, sentiment trends, and speaker breakdown" |
| Mobile view      | "Mobile-first meeting summary view with collapsible sections and swipe actions"                         |
| Error state      | "Error message UI showing a failed CRM sync with retry option and helpful guidance"                     |
| Flow diagram     | "User flow diagram from meeting recording to CRM update showing each step"                              |

---

## Anti-Patterns

🚩 Single option - Always explore 2-3 directions
🚩 Missing states - All AI states required
🚩 States without flows - Always include Flow\_\* stories
🚩 Missing interactive demo or walkthrough
🚩 Loose components/views at initiative root
🚩 Confident wrongness - Show uncertainty
🚩 Surveillance vibes - "Helps YOU" not "reports ON you"
🚩 Prototype starts at the feature, not at the user's natural entry point
🚩 No discovery flow - How does the user know this exists?
🚩 No activation/onboarding flow - First-time experience missing
🚩 No "day 2" story - What does the returning user see?