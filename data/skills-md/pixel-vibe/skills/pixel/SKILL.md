---
name: pixel
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill to implement designs from Figma nodes or natural language to Vue 3 component or Nuxt pages using Mekari Pixel 3 design system. Requires a working Pixel MCP server connection.
metadata:
  author: Ahmad Zakiy
  version: '2026.2.18'
  source: https://pixel-mcp.netlify.app/skills/
---

Mekari Pixel 3 is a comprehensive design system for building consistent, accessible user interfaces in Vue.js applications. It provides a complete set of components, design tokens, and styling utilities following Mekari's design principles.

# Implementation Guide

You are an expert design engineer specializing in implementing complex designs with the Mekari Pixel 3 design system. Follow this step-by-step guide to implement designs accurately and consistently.

**Important:**
Before coding, agents should check

- Pixel already set up in the project
- Theme configuration (Design Token 2.1 vs 2.4)

  If unclear, start by using the Pixel MCP tools (`get-docs`) to gather getting started documentation and design token information.

## Stack

- Nuxt 4 + TypeScript + `@mekari/pixel3`
- Vue 3 Composition API + TypeScript + `@mekari/pixel3`

## Core Topics

| Topic          | Description                                | Reference                                      |
| -------------- | ------------------------------------------ | ---------------------------------------------- |
| Styling        | CSS Props, CSS Function, and stling rules  | [styling](references/styling.md)               |
| Components     | Pixel component catalog and usage patterns | [components](references/components.md)         |
| Design Tokens  | Color, spacing, and typography system      | [design-tokens](references/design-tokens.md)   |
| Code Structure | Vue SFC organization and best practices    | [code-structure](references/code-structure.md) |

---

## Step 1: Analyze Design

### For Figma Designs (if working with Figma designs)

**Use Figma MCP tools to extract design details:**

1. **Extract node ID** from Figma URL

   - Format: `https://figma.com/design/file-key?node-id=1-2` → Node ID: `1:2`
   - Replace hyphens with colons: `1-2` becomes `1:2`

2. **Use Figma MCP tools:**

   - Use `get_design_context(nodeId: "1:2")` to get structured design data
   - Use `get_screenshot(nodeId: "1:2")` to get visual reference

3. **Analyze design details:**
   - Visual hierarchy and layout structure
   - Colors, typography, spacing values
   - Interactive elements and their states
   - Responsive behavior

### For General Designs (if using natural language or other design sources)

1. Analyze the design requested (ex: create a login form)
2. Analyze visual hierarchy, layout, colors, spacing, typography
3. Identify all components needed to implement the design (ex: buttons, inputs, modals, etc.)

## Step 2: Get Pixel 3 Component Documentation

**Use Pixel MCP tools to get components documentantion:**

1. Use `get-docs` to setup Pixel design system if needed (ex: installation, theme setup, etc.)
2. Use `get-component` to identified component (ex: buttons, inputs, modals, etc.)
3. Use `get-docs` to get design tokens and additional context (ex: colors, spacing, typography, etc.)

## Step 3: Implement Pixel 3 Components

See [components reference](references/components.md) for:

1. Component mapping table (Figma elements to Pixel components)
2. Common usage patterns (forms, cards, modals, icons)
3. Prop validation guidelines

## Step 4: Apply Styling

See [styling reference](references/styling.md) for:

1. Use Pixel CSS Props (primary for MpFlex, Pixel.div)
2. Use Pixel CSS Function (secondary for other components)
3. Use Design Token 2.4 (all values must use semantic tokens)

## Step 5: Follow Code Structure

See [code-structure reference](references/code-structure.md) for:

1. Vue 3 SFC implementation
2. Script setup code organization
3. TypeScript best practices

---

# Output Format

Provide complete implementation with:

1. **Vue Component Code** (following code structure rules)
2. **Pixel Components Used** (list all imported components)
3. **Design Tokens Applied** (colors, spacing, typography used)
4. **Implementation Notes** (decisions, assumptions, limitations)

---

# MCP Reference

## Pixel MCP Tools

- `get-docs` - Get Pixel setup, tokens, and general docs
- `get-component` - Get Pixel component documentation

## Pixel MCP Prompts

- `implement-figma-to-pixel` - Implement Figma designs with Pixel components
- `create-deisgn-to-pixel` - Create designs using Pixel components

## Figma MCP Tools (if working with Figma designs)

- `get_design_context` - Extract structured design data from Figma
- `get_screenshot` - Get visual reference from Figma node
- `get_metadata` - Get high-level node map for large designs

## Additional Resources

- [Mekari Pixel 3 Documentation](https://docs.mekari.design/)
- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
