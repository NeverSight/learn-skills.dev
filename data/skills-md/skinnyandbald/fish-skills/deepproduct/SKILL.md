---
name: deepproduct
description: "Builds a profile of your product (users, features, design system) then generates a research prompt for any UX or product design question."
---

# Deep Product Research Prompt Generator

Deep product analysis tool.

Arguments: $ARGUMENTS

## Instructions

Generate a comprehensive deep research prompt for the product question **"$ARGUMENTS"** tailored to the current project's product context — its users, UI/UX patterns, domain, and existing design decisions.

**If no topic is provided**, ask the user what product question they want to research (e.g., onboarding flow, navigation patterns, empty states, pricing page, settings UX, notification design, search experience, mobile responsiveness).

---

## Phase 1: Understand the Product

Analyze the current project to build a product profile. You're looking for what this product IS, who it's for, and what design decisions have already been made.

### App Type & Domain

Determine what kind of product this is:
- **Platform type**: Web app, desktop app (Electron/Tauri), mobile app, CLI, browser extension, SaaS, marketplace, etc.
- **Domain**: E-commerce, developer tools, productivity, social, education, healthcare, finance, content/media, etc.
- **Business model clues**: Free/paid, subscription, freemium, marketplace fees (check for pricing pages, plan tiers, billing code)

Look in:
- `README.md`, `CLAUDE.md`, or any project docs
- Route/page files for feature scope
- Landing page or marketing copy if present
- Package name, descriptions in `package.json` / `composer.json` / `Cargo.toml`

### User-Facing Features

Map the product surface by scanning routes, pages, and navigation:

| Source | What to look for |
|--------|-----------------|
| Route definitions (e.g., `routes/web.php`, `app/routes.ts`, `src/pages/`, `src/app/`) | Feature scope — what screens/pages exist |
| Navigation components (sidebar, header, tabs) | Information architecture — how features are organized |
| Layout files | Page structure patterns — shared chrome, content areas |
| Auth/role code | User types — admin, member, guest, team roles |
| Form components | Data collection patterns — what users input |
| Dashboard/home page | Primary user workflow — what users see first |
| Settings pages | Customization surface — what users can configure |
| Notification/email templates | Communication patterns — how the product talks to users |

### Design System & UI Patterns

Identify the existing design language:
- **Component library**: shadcn/ui, Radix, Material UI, Ant Design, Headless UI, custom components
- **CSS approach**: Tailwind, CSS modules, styled-components, Sass
- **Design tokens**: Colors, spacing, typography (check theme files, CSS variables, tailwind config)
- **Layout patterns**: Sidebar + content, top nav, dashboard grid, wizard/stepper, split pane
- **Interaction patterns**: Modals vs. inline editing, toasts vs. banners, forms vs. command palettes
- **Existing component inventory**: What reusable UI components already exist

Look in:
- `tailwind.config.*` for design tokens
- `components/ui/` or similar for component library
- Theme/design token files
- Storybook config if present

### User Context

Piece together who uses this product:
- **User roles**: Check auth, permissions, middleware for distinct user types
- **Onboarding**: Is there a setup wizard, welcome screen, or tutorial?
- **Collaboration**: Multi-user? Teams? Sharing? Real-time?
- **Data ownership**: Personal data, team data, public data?

---

## Phase 2: Confirm Product Profile with User

**IMPORTANT: First output the detected product profile as a text message to the user.** Do NOT put the profile details inside the AskUserQuestion tool.

### Step 1: Display the profile as text output

Output a message like this (with actual detected values):

```
I detected the following product profile for this project:

**Product:**
- Desktop app (Tauri) — developer productivity tool
- Manages local development environments and processes

**Users:**
- Individual developers
- No collaboration/team features detected

**Key Features:**
- Process management dashboard
- Log viewer with search
- Project configuration
- System tray integration

**Design:**
- React + Tailwind CSS
- shadcn/ui component library
- Sidebar + content layout
- Dark mode support

**Maturity:**
- Active development, core features established
- No onboarding flow detected
```

### Step 2: Then ask for confirmation

AFTER displaying the profile above, use the AskUserQuestion tool with a simple confirmation question:

- Question: "Does this product profile look correct?"
- Options: "Yes, looks correct" / "Need corrections"

**Wait for user confirmation before proceeding.** If the user provides corrections, incorporate them.

---

## Phase 3: Generate the Deep Research Prompt

Once the profile is confirmed, generate a comprehensive research prompt. The prompt should be structured for a deep research tool (like Claude, Perplexity, or similar).

### Prompt Template

Generate output in this format (replace placeholders with actual product details):

---

**START OF GENERATED PROMPT**

I'm building a product with the following profile:

**Product:**
- [App type, platform, domain]
- [Core purpose in one sentence]

**Target Users:**
- [Primary user types and their goals]
- [Technical sophistication level]
- [Usage context: work, personal, team, etc.]

**Current Feature Set:**
- [List key features/screens]

**Design System:**
- [Component library, CSS approach]
- [Layout patterns currently used]
- [Key interaction patterns]

**Product Maturity:**
- [Stage: early prototype, MVP, established product, etc.]
- [Notable gaps or areas under development]

I need comprehensive research on **[TOPIC from $ARGUMENTS]** — specifically product design best practices, UX patterns, and real-world examples for a product like mine.

## Research Scope

### 1. UX Patterns & Best Practices

For **[TOPIC]** in products like mine, research:
- **Established UX patterns** used by successful products in this domain
- **Interaction design** best practices specific to [app type]
- **Information architecture** considerations for [TOPIC]
- **Common UX mistakes** products make with [TOPIC]
- **Accessibility** considerations for [TOPIC]

### 2. Real-World Examples & Inspiration

Find examples of **[TOPIC]** from:
- **Direct competitors** or products in the same domain
- **Best-in-class examples** from any domain that solved [TOPIC] well
- **Before/after case studies** showing how products improved [TOPIC]
- Note what makes each example effective or ineffective

For each example, describe:
- What the product does
- How they handle [TOPIC]
- What makes their approach work (or not)
- Screenshots or detailed descriptions if possible

### 3. User Psychology & Behavior

Research the human side of **[TOPIC]**:
- **User expectations** — what do users expect from [TOPIC] in this type of product?
- **Mental models** — how do users think about [TOPIC]?
- **Decision fatigue and cognitive load** — how does [TOPIC] affect user effort?
- **Error recovery** — what happens when things go wrong with [TOPIC]?
- **Progressive disclosure** — how much complexity to show upfront vs. on demand?

### 4. Product-Specific Considerations

Given my product profile, research:
- How **[TOPIC]** should work for [user type] specifically
- [App type]-specific constraints and opportunities for [TOPIC]
- How [TOPIC] interacts with my existing features
- Scale considerations — how should [TOPIC] work with 10 items vs. 1,000?

### 5. Measuring Success

Research how to know if **[TOPIC]** is working:
- **Key metrics** to track for [TOPIC] (engagement, completion rate, time-on-task, etc.)
- **User signals** that [TOPIC] is working well or poorly
- **A/B testing** opportunities for [TOPIC]
- **Qualitative signals** — what to listen for in user feedback

## Requested Output Format

Please provide your findings organized as:

1. **Executive Summary**
   - Top 10 most important [TOPIC] decisions for a product like mine
   - Priority-ranked recommendations

2. **Pattern Library**
   - Proven UX patterns for [TOPIC] with descriptions
   - When to use each pattern
   - Tradeoffs between approaches

3. **Real-World Examples**
   - 5-10 examples from real products
   - What each does well and what could be improved
   - Applicability to my product

4. **Design Recommendations**
   - Specific recommendations for my product
   - Wireframe-level descriptions where helpful
   - Copy/microcopy suggestions where relevant
   - Component and layout suggestions that fit my design system

5. **Edge Cases & Empty States**
   - First-time user experience for [TOPIC]
   - Empty states, zero-data states
   - Error states and recovery flows
   - Power user vs. new user considerations
   - Extreme data scenarios (none, few, many, too many)

6. **Anti-Patterns**
   - What NOT to do with [TOPIC]
   - Common mistakes products make
   - Why they're problematic for users

7. **Implementation Priorities**
   - What to build first (MVP of [TOPIC])
   - What to add later (nice-to-have enhancements)
   - What to skip entirely

8. **Resources**
   - Relevant articles, case studies, talks
   - Design system references
   - Tools for prototyping or testing [TOPIC]

**END OF GENERATED PROMPT**

---

## Phase 4: Present the Output

Output the generated prompt as plain text that the user can easily copy.

Before the prompt, add:

> **Here's your deep research prompt for "[TOPIC]" tailored to your product. Copy this and paste it into your preferred research tool:**

After the prompt, add:

> **Tip:** This prompt works well with Claude, ChatGPT, Perplexity, or similar AI research tools. For best results, use a tool that can search the web for current information and real product examples.

---

## Topic-Specific Additions

Depending on the topic provided in `$ARGUMENTS`, emphasize different aspects:

### If topic is about "onboarding" / "first-run" / "setup":
- Emphasize time-to-value, activation metrics, progressive profiling
- Include wizard vs. contextual onboarding patterns, empty state design
- Request examples of great onboarding from similar product types

### If topic is about "navigation" / "information architecture":
- Emphasize wayfinding, discoverability, mental models
- Include sidebar vs. top nav vs. command palette patterns, breadcrumbs, search
- Request examples of navigation scaling from simple to complex

### If topic is about "search" / "filtering" / "discovery":
- Emphasize query patterns, faceted search, typeahead, result ranking
- Include empty results, suggested searches, filter UX, saved searches
- Request examples from data-heavy products in similar domains

### If topic is about "settings" / "preferences" / "configuration":
- Emphasize organization, discoverability, defaults, dangerous settings
- Include inline vs. dedicated settings page, search within settings, import/export
- Request examples of settings UX that scales well

### If topic is about "notifications" / "alerts" / "messaging":
- Emphasize notification fatigue, urgency levels, channel selection
- Include in-app vs. push vs. email, notification preferences, batching
- Request examples of notification systems users actually like

### If topic is about "empty states" / "zero data":
- Emphasize first-time experience, calls to action, placeholder content
- Include illustration vs. text, educational empty states, sample data
- Request examples of empty states that drive engagement

### If topic is about "forms" / "data entry" / "input":
- Emphasize validation UX, inline errors, progressive forms, autosave
- Include multi-step forms, conditional fields, smart defaults
- Request examples of complex forms that feel simple

### If topic is about "tables" / "lists" / "data display":
- Emphasize sorting, pagination vs. infinite scroll, bulk actions, column management
- Include responsive table patterns, inline editing, density controls
- Request examples of data-dense UIs that remain usable

### If topic is about "dashboard" / "home" / "overview":
- Emphasize information hierarchy, actionable vs. informational, customization
- Include widget patterns, activity feeds, status summaries, quick actions
- Request examples of dashboards that serve both new and power users

### If topic is about "pricing" / "plans" / "billing":
- Emphasize comparison clarity, plan differentiation, upgrade paths
- Include pricing psychology, trial experiences, plan change UX
- Request examples of pricing pages with high conversion rates

### If topic is about "mobile" / "responsive" / "touch":
- Emphasize touch targets, thumb zones, progressive enhancement
- Include responsive patterns, mobile-specific interactions, offline states
- Request examples of products that transition well between desktop and mobile

### If topic is about "dark mode" / "theming":
- Emphasize readability, color contrast, image handling, user preference
- Include system preference detection, smooth transitions, edge cases
- Request examples of products with excellent dark mode implementations

### If topic is about "error handling" / "error states":
- Emphasize error recovery, clear messaging, suggested actions
- Include form errors, page-level errors, network errors, permission errors
- Request examples of products with graceful error handling

### If topic is about "collaboration" / "sharing" / "teams":
- Emphasize permissions, real-time presence, conflict resolution
- Include sharing models, role management, activity feeds, mentions
- Request examples of collaboration UX from similar product types

---

## Notes

- Always include the product's actual features and user types — they matter for relevant research
- If you can't determine something about the product, note it as "[unknown]" and ask the user
- The generated prompt should be self-contained and not require additional context
- Tailor the examples section to the actual product domain (don't request generic examples)
- Focus on product/UX decisions, not technical implementation — the prompt should help someone make design decisions, not write code
