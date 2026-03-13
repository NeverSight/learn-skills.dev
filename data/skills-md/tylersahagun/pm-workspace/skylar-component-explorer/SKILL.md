---
name: skylar-component-explorer
description: Navigate and understand the AskElephant component library. Use when the designer says "show me", "what components", "where is", "find the", "list all", "explore", "what do we have", or asks about any component's structure, variants, or usage.
---

# Component Explorer -- Navigating the UI Library

Help the designer understand what components exist, how they look, what variants they have, and where to find them. Describe everything in visual terms, not code terms.

---

## Triggers

Activate when the designer asks:

- "Show me all the buttons"
- "What components do we have?"
- "Where is the sidebar?"
- "Find the engagement card"
- "What does the badge look like?"
- "List all the form inputs"
- "Explore the design system"
- "What can I use for [purpose]?"

---

## Component Map

### UI Primitives (`elephant-ai/apps/web/src/components/ui/`)

These are the building blocks. Every other component is composed from these.

**Layout & Containers:**

- `card.tsx` -- Bordered surface with shadow, has Header/Content/Footer sections
- `dialog.tsx` -- Modal overlay with backdrop
- `drawer.tsx` -- Slide-in panel from screen edge
- `sheet.tsx` -- Side panel overlay
- `separator.tsx` -- Visual divider line
- `scroll-area.tsx` -- Scrollable container with styled scrollbar
- `resizable.tsx` -- Resizable split panels
- `accordion.tsx` -- Collapsible content sections
- `tabs.tsx` -- Tab navigation with content panels

**Actions:**

- `button.tsx` -- 8 variants: default, primary-blue, outline, secondary, ghost, destructive, destructive-ghost, link
- `button-group.tsx` -- Grouped buttons with consistent sizing
- `text-button.tsx` -- Minimal text-style button
- `text-link.tsx` -- Styled hyperlink

**Form Inputs:**

- `input.tsx` -- Standard text input
- `textarea.tsx` -- Multi-line text input
- `select.tsx` -- Dropdown select
- `checkbox.tsx` -- Checkbox with label
- `radio-group.tsx` -- Radio button group
- `switch.tsx` -- Toggle switch
- `slider.tsx` -- Range slider
- `combobox.tsx` -- Searchable dropdown
- `multi-select.tsx` -- Multi-value select with tags
- `search-input.tsx` -- Input with search icon
- `date-picker.tsx` -- Date selection
- `date-range-picker.tsx` -- Date range selection
- `date-time-picker.tsx` -- Date and time selection
- `calendar.tsx` -- Calendar grid for date pickers
- `form.tsx` -- Form wrapper with validation
- `label.tsx` -- Form field label

**Display:**

- `badge.tsx` -- Status/category indicator (multiple color variants)
- `avatar.tsx` -- User/entity avatar (image or initials)
- `tag.tsx` -- Removable tag/chip
- `alert.tsx` -- Informational banner with icon
- `alert-dialog.tsx` -- Confirmation dialog
- `tooltip.tsx` -- Hover information popup
- `hover-card.tsx` -- Rich hover popup with content
- `popover.tsx` -- Anchored popup container
- `progress.tsx` -- Progress bar
- `skeleton.tsx` -- Loading placeholder
- `spinner.tsx` -- Loading spinner
- `table.tsx` -- Data table

**Navigation:**

- `dropdown-menu.tsx` -- Context/action menu
- `command.tsx` -- Command palette (Cmd+K style)
- `sidebar.tsx` -- Application sidebar

**Feedback:**

- `sonner.tsx` -- Toast notifications

**Typography:**

- `tokens/typography.tsx` -- Semantic type variants (h1-h4, p, lead, large, small, extraSmall, tiny)

**Media:**

- `styled-video-player.tsx` -- Video player with controls
- `meeting-clip-slider.tsx` -- Meeting clip scrubber

**Effects:**

- `text-shimmer.tsx` -- Shimmering text effect
- `typewriter.tsx` -- Typewriter text animation

### Feature Components

| Directory      | What it contains     | Key components                               |
| -------------- | -------------------- | -------------------------------------------- |
| `chat/`        | AI chat interface    | Chat messages, input, thread, suggestions    |
| `engagements/` | Meeting/call views   | Engagement cards, timelines, transcripts     |
| `workflows/`   | Workflow builder     | Flow editor, nodes, triggers, actions        |
| `navigation/`  | App navigation       | Sidebar, top nav, breadcrumbs                |
| `person/`      | Contact views        | Person cards, details, activity              |
| `company/`     | Company views        | Company cards, details                       |
| `signals/`     | Signal UI            | Signal cards, lists, details                 |
| `ai-elements/` | AI-specific UI       | AI badges, suggestions, confidence           |
| `onboarding/`  | First-run experience | Setup wizard, welcome screens                |
| `filters/`     | Data filtering       | Filter bars, dropdowns, chips                |
| `projects/`    | Project views        | Project cards, boards                        |
| `tags/`        | Tag management       | Tag pickers, lists                           |
| `prototypes/`  | PM prototypes        | AgentCommandCenter, ClientUsageMetrics, etc. |

---

## How to Explore

### "Show me all [component type]"

1. List the components with a brief visual description
2. Mention how many variants each has
3. Note which have Storybook stories (check for `*.stories.tsx`)
4. Suggest opening Storybook to see them rendered

### "What does [component] look like?"

1. Read the component file
2. Describe it visually: size, colors, spacing, states
3. List all variants/sizes available
4. Mention the Storybook story if one exists

### "Where is [feature]?"

1. Search the component directory for the feature name
2. Read the component to understand its structure
3. Describe what it does and what it looks like
4. Show how it relates to other components (what it contains, what contains it)

### "What should I use for [purpose]?"

1. Consider the purpose and context
2. Recommend the best component(s) from the library
3. Explain why this component is the right fit
4. Note any variants that would work well
5. If no existing component fits, describe what would need to be created

---

## Describing Components

When describing a component, always include:

1. **Visual appearance**: What it looks like (shape, color, size)
2. **Content**: What information it displays
3. **Variants**: Different visual modes (size, color, style)
4. **States**: How it looks when loading, empty, disabled, error
5. **Interactions**: What happens when you click, hover, focus
6. **Responsive behavior**: How it adapts on mobile
7. **Context**: Where it appears in the app (what screens, what parent containers)

Example:

"The Badge component is a small pill-shaped label used for status and categories. It comes in several variants:

- **Default**: Dark background with light text (our primary-dark color)
- **Outline**: Bordered with transparent background
- **Status colors**: Success (emerald), Warning (amber), Error (rose), Info (blue)
- **Category colors**: Rose, orange, yellow, lime, green, teal, blue, indigo, fuchsia, purple, stone

Badges have two sizes: small (about 20px tall) and medium (about 24px tall). They pair well with icons at h-3 w-3 size.

You can see all variants in Storybook under the 'ui / Badge' section."

---

## Storybook Navigation Guide

When the designer is looking at Storybook, help them navigate:

| Storybook location      | What they'll find                      |
| ----------------------- | -------------------------------------- |
| `ui/`                   | All design system primitives           |
| `ui/Button`             | All button variants and sizes          |
| `ui/Card`               | Card layouts and compositions          |
| `ui/Badge`              | Status and category badges             |
| `ui/Dialog`             | Modal dialog patterns                  |
| `ui/Form`               | Form field patterns                    |
| Toolbar > Viewport      | Switch between mobile/tablet/desktop   |
| Toolbar > Theme         | Toggle light/dark mode                 |
| Controls panel (bottom) | Toggle props to change component state |

---

## Comparing Similar Components

When the designer asks "should I use X or Y?", compare them:

1. Visual differences (what they look like)
2. Semantic differences (what they communicate)
3. Interaction differences (how they behave)
4. Context differences (where they're typically used)

Recommend the best fit based on the designer's specific use case.
