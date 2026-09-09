---
name: graphy-editor
description: Make Graphy charts editable and drive edits with @graphysdk/react-renderer/editable and the viz-engine command system. Covers embedding an editable chart, editing charts programmatically or from an agent (commands, per-layer control), undo/redo and command history, saving/persisting edited charts, point-and-click annotation editing, and the optional pre-built editor panel. Building charts from scratch is the graphy-charts skill.
---

# graphy-editor

Edit Graphy charts after they exist: point-and-click on the canvas, programmatically from code or
an agent, or through the optional pre-built settings panel. This skill starts where a chart already
renders — authoring the spec, styling and the annotation builders are the `graphy-charts`
skill.

## Mental model

- **Every edit is a Command.** A canvas drag, a panel control and a line of your code all dispatch
  the same serializable `Command` objects from `@graphysdk/viz-engine` against the provider's live
  spec — so whatever made an edit, it lands on the same undo history and the same save callback.
- **Importing enables; `mode` activates.** `EditableGraphRenderer` (from
  `@graphysdk/react-renderer/editable`) is what makes editing *possible*; `mode="editable"` is what
  makes it *current*. A plain `GraphRenderer` stays read-only whatever `mode` says. Toggle `mode`,
  never swap components.
- **One gesture, one undo entry.** During a drag or a burst of typing, dispatch each change with
  `{ transient: true }` and call `seal()` when the gesture ends — the whole run becomes a single
  undo entry and a single `onChange` call.
- **Saving is a round-trip.** `GraphProvider onChange` hands you a plain-JSON `SpecInput` after
  every finished gesture; store it, and pass it back as `input` to restore. Passing it back does
  not re-trigger the callback. Data is never edited — commands change the spec only.
- **Each surface reaches a different amount of the spec.** Canvas gestures reach the least, the
  pre-built panel a curated subset, commands the most (including per-layer control). Anything
  commands miss is edited by rebuilding the `SpecInput` with the authoring API from
  `graphy-charts`. The panel is one optional UI over the commands, not the whole editor.

## Minimal editable chart

```tsx
import { useRef, useState } from 'react';
import { GraphProvider, useGraphHistoryShortcuts, type GraphHandle } from '@graphysdk/react-renderer';
import { EditableGraphRenderer } from '@graphysdk/react-renderer/editable';
import type { Data, SpecInput } from '@graphysdk/viz-engine';

function ChartEditor({ data, initialSpec }: { data: Data; initialSpec: SpecInput }) {
  const [spec, setSpec] = useState(initialSpec);
  const handleRef = useRef<GraphHandle>(null);
  useGraphHistoryShortcuts(handleRef); // ⌘/Ctrl+Z undo/redo shortcuts

  return (
    <GraphProvider input={spec} data={data} handleRef={handleRef} onChange={setSpec}>
      <EditableGraphRenderer mode="editable" />
    </GraphProvider>
  );
}
```

That alone is a working editor: canvas selection and drags, the `(+)` menu on hovered data points,
in-place title and caption editing, undo/redo — no panel. `setSpec`'s latest value is what you
persist.

## Where to look

| I want to… | Read |
|---|---|
| Get an editable chart on screen; what extra to install; toggle edit mode | `reference/embedding.md` |
| Save/persist edits; restore a saved chart; reset | `reference/embedding.md` |
| Dispatch edits from code or an agent; the full command catalogue | `reference/commands.md` |
| Control one layer: add/remove layers, trend/average lines, per-layer settings | `reference/commands.md` |
| Undo/redo, history UI, keyboard shortcuts | `reference/commands.md` |
| Serialize/replay commands (collaboration, agent-driven editing) | `reference/commands.md` |
| Selection: what's selected, select programmatically | `reference/commands.md` |
| Edit a chart from a toolbar/menu outside the provider tree (`GraphHandle`) | `reference/commands.md` |
| Point-and-click on the canvas: drags, the `(+)` menu, inline text, keyboard | `reference/canvas.md` |
| Add/move/restyle/remove annotations by command; anchors; movability | `reference/canvas.md` |
| Add or remove highlights from an editing UI without creating duplicates | `reference/canvas.md` |
| Mount the pre-built settings panel; what each section edits | `reference/panel.md` |
| Swap panel controls for my design system; write a custom section | `reference/panel.md` |
| Check an exact signature, param type or accepted value | `reference/types.md` |
| Smallest full integration with persistence | `recipes/minimal-embed.md` |
| Drive edits from code/an agent end to end | `recipes/programmatic-editing.md` |
| Canvas-only annotation editing (no panel) | `recipes/annotation-canvas.md` |
| A complete tabbed editor UI with the pre-built panel | `recipes/tabbed-editor.md` |
| Adopt my design system in the panel | `recipes/design-system.md` |
| Author the spec/styles/annotations themselves; install the SDK | the `graphy-charts` skill (`reference/install.md` there for setup) |

## Hard rules

- Commands come from `@graphysdk/viz-engine` (root); hooks and `GraphHandle` from
  `@graphysdk/react-renderer` (root); components from `@graphysdk/react-renderer/editable`. With
  the standard `@graphysdk/react` install, all of it comes from `@graphysdk/react` and
  `@graphysdk/react/editable` instead. A host writing its own editing UI needs nothing from
  `./editable`.
- Read-only embeds must never import from `./editable` — it ships TipTap, the panel and the
  rich-text editors. The 15 `@tiptap/*@^3` peers and React 19 are required (npm 7+/pnpm install
  peers automatically; Yarn users add them).
- Never import `'@graphysdk/react-renderer/editable.css'` — CSS self-injects; the subpath doesn't
  exist. (A stale SDK doc comment still shows it.)
- Toggle `mode` between `'readonly'` and `'editable'`; swapping renderer components remounts the
  chart and loses history and hover state. Remount `GraphProvider` with a React `key` only when you
  *want* a clean history (reset, dataset switch).
- After dispatching with `{ transient: true }`, call `seal()` when the gesture ends (pointer up,
  blur, key up) — without it, `onChange` is delayed until the next edit.
- **The pre-built panel covers a subset of the spec.** Check the section catalog in
  `reference/panel.md` before promising a setting exists; beyond it, dispatch commands, and beyond
  those, rebuild the `SpecInput` (a new `input` from outside replaces the edited state and is not
  an undo step).
- A panel mounted outside the chart's React tree needs both a `handle` (from
  `GraphProvider handleRef`) and the `./editable` entry's own `IntlProvider` — react-intl's is a
  different context and raw phrase keys render without it.
- Section titles are accordion identities — keep them distinct within one `EditorPanel.Root`.
- The old editor API does not exist: no `@graphysdk/editor`, no `EditorProvider`, no `GraphPanel`,
  no `EditorPanel.Section`, no `defaultExpanded` prop. The prop is `defaultExpandedSection`;
  sections are separate named exports; only `AxesPanel` and `ElementsPanel` ship pre-assembled.
- A command whose target is missing or whose value is already set does nothing (returns `null`) —
  dispatching the current value is safe and adds nothing to the history.
