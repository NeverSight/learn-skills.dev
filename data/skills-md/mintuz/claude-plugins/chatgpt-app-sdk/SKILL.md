---
name: chatgpt-app-sdk
description: WHEN building ChatGPT apps using the OpenAI Apps SDK and MCP; create conversational, composable experiences with proper UX, UI, state management, and server patterns.
---

# ChatGPT Apps SDK Best Practices

Build ChatGPT apps using the OpenAI Apps SDK, Model Context Protocol (MCP), and component-based UI patterns.

## Quick Reference

| Topic                                           | Guide                                                       |
| ----------------------------------------------- | ----------------------------------------------------------- |
| Display modes, visual design, accessibility     | [ui-guidelines.md](./references/ui-guidelines.md)           |
| MCP architecture, tools, and server patterns    | [mcp-server.md](./references/mcp-server.md)                 |
| React patterns and window.openai API            | [ui-components.md](./references/ui-components.md)           |
| React hooks (useOpenAiGlobal, useWidgetState)   | [react-integration.md](./references/react-integration.md)   |
| Three-tier state architecture and best practice | [state-management.md](./references/state-management.md)     |

## Critical Setup Requirements

| Issue               | Prevention                                            |
| ------------------- | ----------------------------------------------------- |
| CORS blocking       | Enable `https://chatgpt.com` origin on endpoints      |
| Widget 404s         | Use `ui://widget/` prefix format for widget resources |
| Plain text display  | Set MIME type to `text/html+skybridge` for widgets    |
| Tool not suggested  | Use action-oriented descriptions in tool definitions  |
| Missing widget data | Pass initial data via `_meta.initialData` field       |
| CSP script blocking | Reference external scripts from allowed CDN origins   |

## Decision Trees

### What display mode should I use?

```
Is this a multi-step workflow or deep exploration?
├── Yes → Fullscreen
└── No → Is this a parallel activity (game, live session)?
    ├── Yes → Picture-in-Picture (PiP)
    └── No → Inline
        ├── Single item with quick action → Inline Card
        └── 3-8 similar items → Inline Carousel
```

### Where should state live?

```
Is this data from your API/database?
├── Yes → MCP Server (Business Data)
│   Return in structuredContent from tool calls
└── No → Is it user preference/cross-session data?
    ├── Yes → Backend Storage (via OAuth)
    └── No → Widget State (UI-scoped)
        Use window.openai.widgetState / useWidgetState
```

### Should this be a separate tool?

```
Is this action:
- Atomic and standalone?
- Invokable by the model via natural language?
- Returning structured data?
├── Yes → Create public tool (model-accessible)
└── No → Is it only for widget interactions?
    ├── Yes → Use private tool ("openai/visibility": "private")
    └── No → Handle within existing tool logic
```

### What should go in structuredContent vs \_meta?

```
Does the model need this data to:
- Understand results?
- Generate follow-ups?
- Reason about next steps?
├── Yes → structuredContent (concise, model-readable)
└── No → _meta (large datasets, widget-only data)
```

### Should I use custom UI or just text?

```
Does this require:
- User input beyond text?
- Structured data visualization?
- Interactive selection/filtering?
├── Yes → Custom UI component
└── No → Return plain text/markdown in content
```

# Official Documentation

- MCP Specification: https://modelcontextprotocol.io
- TypeScript MCP SDK: https://github.com/modelcontextprotocol/typescript-sdk
- OpenAI Apps SDK: https://developers.openai.com/apps-sdk
- MCP Apps Extension: http://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps
- ChatGPT Component Library: https://openai.github.io/apps-sdk-ui
