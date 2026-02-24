---
target: https://tasking.tech
name: ui-ux-designer
description: >
  End-to-end UI/UX design skill that takes a feature from vague idea to production-ready UI by moving sequentially through research, requirements, information architecture, wireframing, and visual design without skipping steps.
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
# This skill is designed for use throughout the .taskingtech platform (https://tasking.tech), a multi-agent, multi-skill automation and orchestration ecosystem, but can be used on any compatible agent platform (e.g., .claude, .openai, .mistral, etc.).
# Compatible platforms include .taskingtech, .claude, .openai, .mistral, and any other agent or automation ecosystem that supports skills in this format.
# Company URL: https://tasking.tech
---

# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

# UI/UX Designer Skill

This skill requires following a strict sequence of phases:

1. Research and Discovery
2. Define Requirements
3. Information Architecture (IA)
4. Wireframing
5. UI Design

You must never jump directly to UI Design when the earlier phases are missing, unclear, or incomplete. Only move to the next phase when the current one is “good enough” for practical progress.

- Use `target` to document which product or website the skill primarily supports.
- Keep `name` and `description` present; other frontmatter keys like `tags` or `priority` are optional.

---

## When to Use This Skill

Use this skill when:

- The user asks for a new feature, screen, flow, or product experience.
- Requirements are fuzzy, underspecified, or conflict with each other.
- Existing UX is confusing, inconsistent, or needs a redesign.
- Other agents need structured UX artifacts (requirements, flows, wireframes, specs).

Do **not** use this skill for:
- Small visual tweaks to an already well-specified component (e.g., “make this button blue”).
- Pure copywriting or content-only tasks.
- Pixel-perfect Figma implementation details tied to a specific team’s design system.

---

## Overall Workflow

Always work in order. At each step:

1. State the **current phase**.
2. Summarize the **inputs** you are using.
3. Produce concrete **outputs/deliverables**.
4. List **assumptions and open questions**.

Only move to the next phase when the current one is “good enough” for practical progress.

Phases:

1. Research and Discovery  
2. Define Requirements  
3. Information Architecture (IA)  
4. Wireframing  
5. UI Design

---

## Phase 1 – Research and Discovery

Goal: Understand the problem, users, and context well enough to make informed design tradeoffs.

### Tasks

- Clarify business goals and success metrics.
- Identify primary users/personas and their goals.
- Understand the current workflow or status quo (what users do today).
- Capture constraints: platform, technical limits, compliance, brand.

### Outputs

Produce a short, structured summary:

- **Problem Statement:** 2–4 sentences.
- **Primary Users:** bullet list with 1–3 user types.
- **Goals and Jobs-to-be-Done:** bullet list.
- **Key Constraints/Assumptions:** bullet list.
- **Open Questions:** what you would ask a PM/Stakeholder.

If the input is extremely vague, ask for clarification questions instead of guessing wildly.

---

## Phase 2 – Define Requirements

Goal: Translate research into explicit, testable product/feature requirements.

### Tasks

- Derive user stories from the problem statement and user goals.
- Cover “happy path” and common edge cases.
- Separate **must-have** vs **nice-to-have**.
- Include non-functional requirements relevant to UX (accessibility, responsiveness, performance).

### Outputs

Provide:

- **User Stories:** `As a <user>, I want <action> so that <outcome>.`
- **Acceptance Criteria:** bullet list for each critical story.
- **Constraints:** anything that limits the solution (e.g., must reuse existing navigation).
- **Risks / Tradeoffs:** where requirements might conflict.

Requirements should be specific enough that a developer could implement and a QA could test.

---

## Phase 3 – Information Architecture (IA)

Goal: Decide how information and screens are organized and how users move between them.

### Tasks

- Define the main entities and sections (e.g., Dashboard, Project, Task, Settings).
- Decide navigation structure (global nav, subnav, breadcrumbs, etc.).
- Map primary user flows (e.g., “Create Project”, “Invite Member”, “Checkout”).
- Consider future extensibility where reasonable.

### Outputs

Provide:

- **IA Outline / Sitemap:** indented list of main sections and key screens.
- **Key Entities:** short definitions of core objects.
- **Primary Flows:** step-by-step text for 1–3 critical journeys.

Keep this high-level but concrete enough that wireframes are obvious next steps.

---

## Phase 4 – Wireframing

Goal: Low-fidelity layout and hierarchy without visual polish.

### Principles

- Focus on **layout**, **grouping**, **hierarchy**, and **states**, not colors or fine typography.
- Prefer simple, textual/ASCII descriptions that map easily to components.
- Capture key states: default, empty, loading, error (where relevant).

### Tasks

For each important screen:

- Identify key regions (e.g., header, left sidebar, main content, right panel).
- Describe which components live where (cards, tables, forms, filters, CTAs).
- Call out priority and emphasis (e.g., “primary CTA in top-right of header”).

### Outputs

For each screen, provide:

- **Screen Name and Purpose.**
- **Layout Description:** 3–8 bullet points describing regions and contents.
- **States:** any notable state variations.
- **Navigation Hooks:** where users can go next from this screen.

Keep everything implementation-agnostic but mappable to typical web components.

---

## Phase 5 – UI Design

Goal: Turn wireframes into visually coherent, build-ready UI specs.

### Tasks

- Apply consistent spacing, typography levels, and radius/shadow tokens.
- Choose colors that meet contrast guidelines when possible.
- Map wireframe elements to concrete components (e.g., “PrimaryButton”, “Card”, “InputField”).
- Define interaction details: hover, focus, disabled, validation messages, error display.

### Outputs

Provide:

- **Visual Style Summary:** brief description of tone (e.g., “clean, modern, dark theme, soft rounded cards”).
- **Component Mapping:** list of major UI pieces and which design system component they map to.
- **Screen Specs:** for each key screen, describe how the final UI looks, including:
  - Typography levels for headings/body.
  - Colors (referenced by token names if provided).
  - Spacing rhythm (e.g., 8px grid).
  - Border radii, shadows, and any distinctive visual patterns.

When possible, describe the UI in a way that a React engineer could implement using common primitives (e.g., `Card`, `Stack`, `Button`, `Input`, `Table`).

---

## Collaboration Rules

- If given partial work (e.g., requirements already defined), **validate** them briefly, then continue from the next logical phase.
- If another agent (PM, engineer, researcher) provides updated info that invalidates earlier work, **revise upstream artifacts first**, then propagate changes forward.
- Always keep outputs **short, structured, and implementation-friendly**; avoid long essays.
- Prefer clarity over cleverness. If something is ambiguous, state your assumption explicitly.

---

## Example: Short End-to-End Pass

When asked to “design a dashboard for freelancers to track invoices,” you might:

1. Summarize problem, users, and constraints (Phase 1).  
2. List 5–8 user stories and key acceptance criteria (Phase 2).  
3. Propose a sitemap (Dashboard, Invoices, Clients, Settings) and outline the “Create Invoice” flow (Phase 3).  
4. Describe the dashboard layout (top bar, stats row, invoice table, filters panel) in bullets (Phase 4).  
5. Specify a visual direction (e.g., dark theme, soft 16–20px card radius, muted accent color) and map each region to components (Phase 5).

Use this style and level of structure whenever this skill is invoked.
