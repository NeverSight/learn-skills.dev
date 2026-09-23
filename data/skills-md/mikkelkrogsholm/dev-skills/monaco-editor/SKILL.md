---
name: monaco-editor
description: "Monaco Editor — the code editor that powers VS Code, for the browser. Use when integrating Monaco Editor in React, configuring editor instances, adding custom languages/themes, handling editor events, or troubleshooting Monaco in Vite/bundler setups. Fetch live documentation for up-to-date details."
---

# Monaco Editor

> **CRITICAL: Your training data for Monaco Editor is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs based on your task:
>
> - API usage and configuration: **`WebFetch("https://microsoft.github.io/monaco-editor/docs.html")`**
> - TypeScript type signatures: **`WebFetch("https://microsoft.github.io/monaco-editor/typedoc/index.html")`**
> - React wrapper (`@monaco-editor/react`): **`WebFetch("https://raw.githubusercontent.com/suren-atoyan/monaco-react/master/README.md")`**
>
> Do not proceed without fetching the relevant URL first. Never assume an API exists — verify against current docs.

Monaco Editor is the browser-based code editor that powers VS Code. It provides syntax highlighting, IntelliSense, diff view, minimap, and more for 50+ languages.

## Key Capabilities

- **50+ language grammars**: Syntax highlighting out of the box for TypeScript, Python, JSON, Markdown, etc.
- **IntelliSense**: Autocomplete for TypeScript/JavaScript with type inference
- **Diff editor**: Built-in side-by-side and inline diff view
- **Find & replace**: With regex support
- **Minimap**: Code overview panel
- **Multi-cursor**: Alt+Click for multiple cursors
- **Folding**: Code folding by indentation or syntax
- **Custom themes**: Full theme API matching VS Code theme format
- **Web Workers**: Language services run in workers for non-blocking editing

## React Integration (@monaco-editor/react)

The `@monaco-editor/react` wrapper is the standard way to use Monaco in React. Key points:

```tsx
import Editor from '@monaco-editor/react'

<Editor
  height="100%"
  language="markdown"
  theme="vs-dark"
  value={content}
  onChange={(value) => setValue(value ?? '')}
  options={{
    minimap: { enabled: false },
    wordWrap: 'on',
    fontSize: 14,
    lineNumbers: 'on',
  }}
/>
```

**Access the editor instance** via `onMount`:
```tsx
<Editor
  onMount={(editor, monaco) => {
    // editor = IStandaloneCodeEditor
    // monaco = the monaco namespace
    editorRef.current = editor
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      handleSave()
    })
  }}
/>
```

## Best Practices

**Always lazy-load Monaco.** The editor bundle is ~2MB. In Vite/React, use dynamic imports or React.lazy to avoid blocking initial page load:
```tsx
const Editor = lazy(() => import('@monaco-editor/react'))
```

**Vite requires the `monaco-editor` package directly.** The React wrapper (`@monaco-editor/react`) has `monaco-editor` as a peer dependency. Install both: `bun add @monaco-editor/react monaco-editor`.

**Configure Vite worker bundling.** Monaco uses Web Workers for language services. In Vite, use the `vite-plugin-monaco-editor` plugin or configure manually to avoid worker loading failures:
```ts
// vite.config.ts — simplest approach
import monacoEditorPlugin from 'vite-plugin-monaco-editor'
export default defineConfig({
  plugins: [react(), monacoEditorPlugin({})],
})
```

**Custom themes use the VS Code format.** Define themes via `monaco.editor.defineTheme()` — the format matches VS Code's tokenColors JSON. Apply with the `theme` prop.

**Dispose editors on unmount.** The React wrapper handles this automatically, but if using the raw API (`monaco.editor.create()`), always call `editor.dispose()` in cleanup to prevent memory leaks.

**Language detection by extension.** Use `monaco.languages.getLanguages()` to find supported language IDs. Common mappings: `.md` → `markdown`, `.json` → `json`, `.ts` → `typescript`, `.py` → `python`.

**Diff editor is a separate component:**
```tsx
import { DiffEditor } from '@monaco-editor/react'
<DiffEditor original={oldContent} modified={newContent} language="markdown" />
```
