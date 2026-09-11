---
name: excalidraw-diagram
description: Generate, refine, and export editable Excalidraw diagrams from prompts or Mermaid. Use for hand-drawn architecture, component anatomy, flows, and annotated technical illustrations.
---

Create real Excalidraw elements with one editable source of truth. Read [REFERENCE.md](REFERENCE.md) for Mermaid conversion, direct elements, and visual language.

## Canvas

All commands use the pinned CLI:

```bash
export EXPRESS_SERVER_URL="http://127.0.0.1:${CONDUCTOR_PORT:-3000}"
bunx mcp-excalidraw-server@1.1.0 <command>
```

Use `bunx` cache; never add it to the consumer repo. Run `start`, open the URL in an isolated browser, keep it open, and require `status` to show a client. If isolation is unavailable, ask the user to open the URL once.

## Workflow

1. Choose destination: disposable `.context/excalidraw/<slug>/` or requested durable path. Never overwrite silently.
2. Before clear/replace, preserve the canvas with `snapshot save <name>` or `export --out <file>`.
3. Choose authority: `.mmd` for Mermaid deliverables; `.excalidraw` after direct editing. Validate Mermaid in its target renderer.
4. Mermaid owns standard flow/sequence/state/relationships; direct elements own exact placement, anatomy, logos, zones, and callouts.
5. Create the first complete slice in one `mermaid`, `add`, or `apply`; give mutable elements stable IDs.
6. After Mermaid, `describe` elements before export/correction. If screenshot renders but scene is empty, keep `.mmd` authoritative or rebuild direct; never claim an empty `.excalidraw` is editable.
7. `describe`, then `screenshot --out <check.png>` -> view -> fix collisions, clipping, contrast, crossed arrows with one `apply`. Repeat until clean.
8. Synchronized canvases export non-empty `.excalidraw` plus PNG or SVG. Otherwise export `.mmd` plus render. Keep editable source beside durable render unless flat-only was requested.
9. Report paths, mode, canonical source, accessible description, and manual browser work.

Core commands: `mermaid diagram.mmd`; `add elements.json`; `apply patch.json`; `describe`; `screenshot --out check.png`; `export --out diagram.excalidraw`; `screenshot --format svg --out diagram.svg`.

## Safety

- `clear --yes`, `import --replace`, and restoration are destructive; preserve first.
- `share` uploads the scene; use only for a requested public link.
- Use SVG/imported brand assets for exact logos; never approximate protected marks.
- Run `stop` after export when editing is done.
