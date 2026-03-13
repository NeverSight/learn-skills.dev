---
name: design
description: Guides UI/UX and design-system work using shadcn, Magic UI, and 21st.dev Magic MCPs and project design docs. Use when building or refining interfaces, components, theming, or layouts.
---

# Design Skill

Use this skill when doing UI/UX work, component authoring, design systems, theming, layouts, or design research in this repo. It directs the agent to use the shadcn and Magic UI MCPs and to align with the project's design system.

## When to Use

- User asks for UI/UX work, new or updated components, design systems, theming, or layouts.
- User wants design research, design-system best practices, or comparative analysis (e.g. "research dashboard patterns," "best practices for X").
- Building or refining interfaces in this repo (Next.js, Tailwind, shadcn, Verse/MNKY LABZ).

## Instructions

### Core MCPs

1. **shadcn MCP** (server `shadcn` in mcp.json)
   - Use for shadcn/ui components: add, customize, and align with the project's `components/ui` and Tailwind setup.
   - Prefer shadcn for forms, buttons, dialogs, data tables, and layout primitives.
   - Keep components consistent with existing shadcn usage in the codebase.

2. **Magic UI Design MCP** (server `@magicuidesign/mcp` when enabled)
   - Use for animated or high-impact UI components and design-system-style work.
   - Combine with shadcn: shadcn for structure and accessibility, Magic UI for motion and visual flair.
   - If the Magic UI MCP server is not in mcp.json, the skill still applies; use it when the user has enabled it (e.g. from mcp.json.example).

3. **21st.dev Magic MCP** (server `@21st-dev/magic` when enabled)
   - Use for natural-language UI generation: create components from descriptions (e.g. "create a modern nav bar"), refine existing components, or search logos/brand assets (`create-ui`, `fetch-ui`, `refine-ui`, `logo-search`).
   - Requires `MAGIC_21ST_API_KEY` in env. Components are 21st.dev-inspired, TypeScript/Tailwind, and added to the project.
   - Prefer for "generate a component from a description" flows; combine with shadcn for layout and Magic UI for animation.

### Project alignment

- Read `docs/DESIGN-SYSTEM.md` when touching tokens, theme, or Verse/MNKY LABZ.
- For Flowise integration (chatflow config, document store, override config), use `components/flowise-mnky/` and `docs/FLOWISE-MNKY-COMPONENTS.md`.
- Follow existing tokens and structure: `globals.css`, `tailwind.config`, `verse-storefront.css`, `verse-glass.css`.
- Do not introduce new design tokens or theme layers without aligning with the documented architecture.

### Other MCPs when helpful

- **21st.dev Magic** (`@21st-dev/magic`): When the user wants to generate UI from a natural-language description or search logos/brand assets; use create-ui, refine-ui, or logo-search as needed.
- **Context7** (if available): Use for up-to-date shadcn, Radix, or Tailwind documentation.
- **Fetch** or **FireCrawl**: Use for design references or design-system docs from URLs when the user provides links or when researching patterns.

### Deep design research

When the user explicitly requests design research, design-system best practices, or comparative analysis (e.g. "research dashboard patterns," "best practices for X"):

1. Follow the **Deep Research Protocol** in `.cursor/rules/deep-thinking.mdc`.
2. Initial engagement: confirm scope with 2–3 clarifying questions; reflect understanding; wait for response.
3. Research planning: present 3–5 themes and a research plan; wait for user approval.
4. For each theme: Brave Search for landscape, Sequential Thinking to analyze; Tavily Search for depth, Sequential Thinking to integrate.
5. Produce a final report (knowledge development, comprehensive analysis, practical implications) in narrative form.

Do **not** run the full deep research protocol for simple component or layout tasks; reserve it for explicit research requests.

### Conventions

- Prefer React Server Components where possible; use `'use client'` only when needed for interactivity or hooks.
- Use kebab-case for component file names (e.g. `my-component.tsx`).
- Keep client components small and isolated.
- Add loading and error states for data-driven UI.
- Use semantic HTML and accessible patterns; align with project coding best practices in `.cursor/rules/coding-best-practices.mdc`.
