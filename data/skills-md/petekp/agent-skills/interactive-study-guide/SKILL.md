---
name: interactive-study-guide
description: "Transform a codebase study guide into a polished interactive web experience. This skill should be used when the user has a completed study guide markdown file (from codebase-study-guide or similar) and wants to turn it into an interactive pedagogical app. Triggers on requests like \"make this study guide interactive\", \"turn this into an interactive experience\", \"visualize this study guide\", \"create an interactive version\", or when a user has a study guide .md file and wants a richer presentation. Produces a Vite-served single-page app with scroll-driven storytelling, interactive architecture diagrams, animated code walkthroughs, and progressive disclosure."
---

# Interactive Study Guide

Transform a static study guide markdown file into an immersive, interactive learning experience served as a local web app. The output should feel like a NYT interactive feature or a Pudding.cool essay — editorial typography, generous whitespace, purposeful animation, and visualizations that reveal structure rather than decorate.

## Guiding Principles

- **Restraint over spectacle.** Every animation must earn its place by revealing something the static text cannot. Avoid gratuitous motion.
- **Content determines form.** Each section gets the layout and interactivity best suited to its content type — never force a visualization where prose works better.
- **Scroll as narrative.** The primary interaction is scrolling. Use scroll-driven reveals, sticky elements, and waypoint transitions to create a reading rhythm.
- **Typographic confidence.** Large serif headings, measured line lengths, and ample vertical rhythm. The text itself should feel beautiful before any interactivity loads.
- **Progressive enhancement.** The page is readable and useful even if JavaScript fails. Interactivity layers on top.

## Workflow

### Step 1: Locate and Parse the Study Guide

Accept a path to the study guide markdown file. Parse it into structured sections using the known template format from `codebase-study-guide`:

| Section | Heading Pattern | Content Type |
|---------|----------------|--------------|
| Purpose | `## 1. Why This Exists` | Prose with problem/approach/users |
| Threshold Concepts | `## 2. The Big Ideas` | Named concepts with code locations |
| System Map | `## 3. System Map` | Mermaid diagram + table |
| Request Walkthrough | `## 4. Walking Through a Request` | Sequence diagram + annotated code steps |
| Deep Dives | `## 5. System Deep Dives` | Multiple `### 5.X` subsections |
| Patterns | `## 6. Patterns & Conventions` | Named patterns + naming table |
| Boundaries | `## 7. Boundaries & External Systems` | Table of external systems |
| Testing | `## 8. Testing Strategy` | Prose with exploration prompts |
| Next Steps | `## 9. Your Next Steps` | Checklists by day |

If the markdown doesn't match this exact structure, adapt gracefully — detect sections by heading content rather than numbering.

### Step 2: Set Up the Project

Run the scaffold script to create the Vite project:

```bash
bash scripts/scaffold.sh <output-directory> "<project-name>"
```

This creates a configured Vite project with D3, Prism.js, and the editorial design system pre-installed. After scaffolding, run `npm install` in the output directory.

### Step 3: Build Section by Section

Transform each parsed section into its interactive counterpart. Consult [references/section-strategies.md](references/section-strategies.md) for detailed visualization patterns and code examples for each section type. Consult [references/design-system.md](references/design-system.md) for all typography, color, spacing, and motion tokens.

The section-to-visualization mapping:

| Section | Interactive Treatment |
|---------|----------------------|
| **Purpose** | Full-bleed hero with large serif typography. Animated text that fades in on load. The problem statement presented as a bold pull-quote. No interactivity needed — let the words breathe. |
| **Threshold Concepts** | Cards that start collapsed showing only the concept name. Click to expand with a smooth height transition. Show "you'll see this in" file paths as clickable pills. Subtle connecting lines between related concepts. |
| **System Map** | Interactive D3 force-directed graph replacing the Mermaid diagram. Nodes are draggable. Hover shows the one-line purpose from the table. Click a node to scroll to its deep dive section. Animated edges show data flow direction. |
| **Request Walkthrough** | Scroll-driven step-through. A sticky diagram panel on the left animates as the reader scrolls through annotated code steps on the right. Each step highlights the active system in the diagram. Code blocks use syntax highlighting with line-by-line reveal. |
| **Deep Dives** | Tabbed interface where each system is a tab. Within each tab: purpose as a bold header, pattern name as a linked badge, abstractions table, interfaces shown as a mini connection diagram, and the exploration task in a distinct callout box. |
| **Patterns** | Searchable/filterable card grid. Each card shows pattern name, where it appears (as code-location pills), and why. Cards flip or expand on click to show the full description. Naming conventions shown as a styled reference table. |
| **Boundaries** | Clean data table with hover-to-expand rows. Each row shows the external system, its role, and integration pattern. Consider a simple boundary diagram showing inside/outside the system. |
| **Testing** | Minimal treatment — styled prose with the exploration prompt in a distinct interactive callout (checkbox that reveals a hint). |
| **Next Steps** | Interactive checklist with local storage persistence. Progress bar at the top. Days presented as horizontal timeline nodes. Completed items get a satisfying check animation. |

### Step 4: Wire Navigation and Transitions

Build a minimal navigation system:

- **Left sidebar** (desktop) or **bottom sheet** (mobile): Section titles as nav links with scroll-spy highlighting
- **Progress indicator**: Thin bar at top of viewport showing read progress
- **Smooth scroll**: Clicking a nav link animates to the section
- **Section transitions**: Each section fades in as it enters the viewport using `IntersectionObserver`

### Step 5: Start the Dev Server

After building all components:

```bash
cd <output-directory> && npx vite --open
```

### Step 6: Polish Pass

Before presenting to the user, verify:

- [ ] Typography hierarchy is clear — headings, body, code, and captions are visually distinct
- [ ] Whitespace is generous — sections breathe, nothing feels cramped
- [ ] Animations are smooth and purposeful — no jank, no gratuitous bouncing
- [ ] System map is interactive — nodes drag, hover shows info, click navigates
- [ ] Code blocks have syntax highlighting appropriate to the codebase's language
- [ ] Mobile layout works — single column, touch-friendly interactions
- [ ] `prefers-reduced-motion` is respected — all animations disable gracefully
- [ ] Color contrast meets WCAG AA — especially code blocks and muted text
- [ ] Navigation scroll-spy accurately tracks the current section
- [ ] Interactive elements (tabs, cards, checklists) respond immediately, no loading states needed

## Resources

### scripts/scaffold.sh

Creates a configured Vite project with dependencies and the editorial design system. Usage documented in Step 2.

### references/section-strategies.md

Detailed visualization strategy and code patterns for each study guide section. The primary reference while building — consult before writing any section component.

### references/design-system.md

Complete editorial design system: typography scale, color palette, spacing, motion tokens, and component-level styles. Every visual decision should reference these tokens.
