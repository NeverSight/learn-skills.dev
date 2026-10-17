---
name: watermelon-ui
description: Discover and install free, source-backed React UI from Watermelon. Use when a user needs a component, block, dashboard, template, design inspiration, or a composed page built from compatible sections.
---

# Watermelon UI Skill

Watermelon UI is a free, open-source catalog of React and Tailwind interfaces. Its MCP server is read-only, needs no API key, and returns preview links, dependencies, installation commands, and source files where available.

## Default workflow

1. Call `search` with the user's visual and functional requirements before writing a component from scratch.
2. If the choice is not obvious, call `get_inspiration` and compare 3-6 suitable options.
3. Call `get_component` for the chosen slug to retrieve its source, dependencies, preview, and shadcn install command.
4. Install or write the returned files, then adapt tokens, copy, props, and imports to the project's existing design system.
5. Verify responsive behavior, keyboard interaction, accessibility, and both supported color modes.

## Full-page workflow

Call `compose_page` for landing pages and other multi-section experiences. Treat its result as a source-backed starting plan, inspect each selected preview, and replace any section that does not fit the project's visual direction.

## Selection guidance

- Use `components` for familiar UI primitives and variants.
- Use `animated-components` for interaction-heavy standalone pieces.
- Use `blocks` for complete page sections.
- Use `dashboards` and `templates` for composition references.
- Preserve the user's existing framework and conventions. Do not force Watermelon styling over an established design system.

## Setup

The hosted server is `https://mcp.watermelon.sh/mcp`. It is public and requires no authentication.
