---
name: tiptap
description: 'Builds rich text editors with Tiptap, a headless ProseMirror-based editor framework for React with Tailwind v4 support. Covers SSR-safe setup, image uploads, prose styling, collaborative editing, and markdown support. Use when adding a rich text editor, configuring Tiptap extensions, handling image uploads in editors, or setting up collaborative editing with Y.js. Use for tiptap, rich text, editor, prosemirror, react, tailwind.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://tiptap.dev/docs'
user-invocable: false
---

# Tiptap Rich Text Editor

## Overview

Tiptap is a headless rich text editor built on ProseMirror, providing a modular extension system for React applications. It supports React 19, Tailwind v4, and SSR frameworks like Next.js. Use when building blog editors, comment systems, documentation tools, or Notion-like collaborative apps. Do NOT use with Create React App (CRA is incompatible with Tiptap v3 ESM module structure; use Vite instead).

## Quick Reference

| Pattern              | API / Key Point                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Create editor        | `useEditor({ extensions: [StarterKit], immediatelyRender: false })`                                                       |
| Render editor        | `<EditorContent editor={editor} />`                                                                                       |
| Prose styling        | Add `className="prose dark:prose-invert max-w-none"` to container                                                         |
| Configure StarterKit | `StarterKit.configure({ heading: { levels: [1, 2, 3] } })`                                                                |
| Disable undo/redo    | `StarterKit.configure({ undoRedo: false })` (required for Y.js collab)                                                    |
| Image upload         | Set `allowBase64: false`, use upload handler with URL replacement                                                         |
| Markdown support     | `import { Markdown } from '@tiptap/markdown'` (official, open-source)                                                     |
| shadcn component     | `npx shadcn@latest add https://raw.githubusercontent.com/Aslam97/shadcn-minimal-tiptap/main/registry/block-registry.json` |
| Null guard           | `useEditor()` returns `Editor \| null` — guard before calling methods                                                     |

## Core Dependencies

| Package                   | Purpose                                                    |
| ------------------------- | ---------------------------------------------------------- |
| `@tiptap/react`           | React integration (React 19 supported since v2.10.0)       |
| `@tiptap/starter-kit`     | Bundled extensions: marks, nodes, and functionality        |
| `@tiptap/pm`              | ProseMirror peer dependency (required, not auto-installed) |
| `@tailwindcss/typography` | Prose styling for headings, lists, links                   |

## StarterKit v3 Contents

| Category      | Included                                                                                                                |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Marks         | Bold, Italic, Strike, Code, Link (v3), Underline (v3)                                                                   |
| Nodes         | Document, Paragraph, Text, Heading, BulletList, OrderedList, ListItem, Blockquote, CodeBlock, HorizontalRule, HardBreak |
| Functionality | Undo/Redo, Dropcursor, Gapcursor, ListKeymap (v3), TrailingNode (v3)                                                    |

## Common Additional Extensions

| Extension         | Package                                 | Use Case                             |
| ----------------- | --------------------------------------- | ------------------------------------ |
| Image             | `@tiptap/extension-image`               | Image support with resize            |
| Color             | `@tiptap/extension-color`               | Text color (requires TextStyle)      |
| Typography        | `@tiptap/extension-typography`          | Smart quotes, dashes, ellipsis       |
| Placeholder       | `@tiptap/extension-placeholder`         | Placeholder text (requires CSS)      |
| Table             | `@tiptap/extension-table`               | Table support (+ Row, Cell, Header)  |
| TaskList          | `@tiptap/extension-task-list`           | Checkbox task lists                  |
| CodeBlockLowlight | `@tiptap/extension-code-block-lowlight` | Syntax-highlighted code              |
| Collaboration     | `@tiptap/extension-collaboration`       | Real-time multi-user editing (Y.js)  |
| Markdown          | `@tiptap/markdown`                      | Bidirectional markdown (open-source) |

## Common Mistakes

| Mistake                                   | Fix                                                                |
| ----------------------------------------- | ------------------------------------------------------------------ |
| Missing `immediatelyRender: false`        | Add to `useEditor()` config — required for SSR/Next.js             |
| No `prose` classes on editor container    | Add `className="prose prose-sm dark:prose-invert max-w-none"`      |
| Images stored as base64                   | Set `allowBase64: false`, use upload handler with URL replacement  |
| Using EditorProvider + useEditor together | Choose one — EditorProvider wraps useEditor internally             |
| Undo/Redo enabled with Collaboration      | Set `undoRedo: false` in StarterKit when using Y.js                |
| ProseMirror version conflicts             | Add `resolutions` for prosemirror-model/view/state in package.json |
| Using Create React App                    | Switch to Vite — CRA incompatible with v3 ESM modules              |
| Not checking `editor` for null            | `useEditor()` returns `Editor \| null` — guard before use          |
| Using `history: false` for collab         | Config key renamed to `undoRedo` in v3                             |
| Importing `@tiptap/extension-markdown`    | Correct package is `@tiptap/markdown`                              |

## Delegation

- **Tailwind styling**: see `tailwind` skill
- **Form integration**: see `tanstack-form` skill

## References

- [Setup and Configuration](references/setup.md)
- [Extensions Catalog](references/extensions.md)
- [Image Upload](references/image-upload.md)
- [Patterns](references/patterns.md)
- [Known Issues and Errors](references/known-issues.md)
- [Prose Styling](references/prose-styling.md)
