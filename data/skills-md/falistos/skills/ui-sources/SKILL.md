---
name: ui-sources
description: Source real UI components, shadcn registries, AI/agent interface kits, shader and motion tools, design tokens and public design systems instead of inventing them. Use when a UI needs a concrete component (command menu, data table, animated number, gradient background), when picking a library or design system, when asking "where do I get this from", or when building an agent interface (chat, tool calls, approvals, voice). Critique and polish are `impeccable`.
user-invocable: true
argument-hint: "[what you need — e.g. 'chat UI', 'animated counter', 'non-react buttons', 'design system reference']"
---

# UI Sources

A catalogue of places to take real, working UI from.

## Routing

| Need | Load |
|---|---|
| Find a component, any component; browse registries | `reference/discovery.md` |
| Chat UI, tool calls, reasoning, approvals, voice, agent canvas | `reference/ai-interfaces.md` |
| Shaders, gradients, grain, motion, easing, tokens, type, colour | `reference/craft.md` |
| Study how a real design system is built; token architecture | `reference/design-systems.md` |
| Project is not React — Django, Rails, Laravel, Astro, plain HTML, Vue, Svelte | `reference/non-react.md` |

Neighbouring skills own their lanes: **`pick-ui-library`** (canonical React library per task; invoke it explicitly, it never self-triggers), **`baseline-ui`** (spacing/hierarchy/typography cleanup), **`emil-design-eng`** and **`review-animations`** (craft and motion judgement), **`impeccable`** (direction, critique, polish).

## Ground rules

- **Install components, don't rewrite them from memory**: use the CLI or fetch canonical markdown (`reference/discovery.md`). Galleries render code through JS, so fetched HTML is not a reliable source.
- **Check the stack first.** This ecosystem is mostly React + Tailwind + Motion; otherwise go to `reference/non-react.md`.

## The base layer

The base is **shadcn/ui** unless a reason says otherwise: nearly every source distributes through its registry protocol.

```bash
pnpm dlx shadcn@latest init                 # once per project
pnpm dlx shadcn@latest add button           # official registry, no config
pnpm dlx shadcn@latest add @magicui/globe   # third-party, needs a namespace
```

Declare third-party namespaces in `components.json`:

```json
{ "registries": { "@magicui": "https://magicui.design/r/{name}.json" } }
```

Suggest the official MCP server (`npx shadcn@latest mcp init --client claude`, works with any shadcn-compatible registry) when the user will pull components repeatedly in one project.
