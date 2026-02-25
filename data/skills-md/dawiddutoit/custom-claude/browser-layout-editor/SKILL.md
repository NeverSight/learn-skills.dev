---
name: browser-layout-editor
description: |
  Builds browser-based 2D layout editors with FastAPI backend and vanilla JS + SVG frontend. Use when creating: (1) Visual editors for 2D arrangements (cut lists, floor plans, diagrams), (2) Drag-and-drop interfaces with multiple containers/sheets, (3) Single-file browser UIs served from Python, (4) Real-time position editing with validation. Triggers: "layout editor", "drag between", "visual editor", "browser UI for editing", "SVG editor".

---

# Browser Layout Editor

Build browser-based 2D layout editors with FastAPI + vanilla JS + SVG.

## When to Use This Skill

Use when asked to:
- Create visual editors for 2D layouts (cut lists, floor plans, room arrangements)
- Build drag-and-drop interfaces with multiple containers or sheets
- Develop interactive browser UIs for editing positions and sizes
- Create single-file browser applications served from Python
- Implement real-time position editing with validation and collision detection

Do NOT use when:
- Simple form inputs are sufficient (don't over-engineer)
- 3D visualization is needed (this is 2D only)
- User needs desktop application (this is browser-based)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   JSON File     │◄───►│  FastAPI Server │◄───►│  Browser UI     │
│   (layout.json) │     │  (server.py)    │     │  (editor.html)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Storage              Module globals          Single HTML file
                          for state               CSS + JS embedded
```

## Core Patterns

### 1. Module-Level State (Single-User Server)

For single-user editing, use module globals instead of a database:

```python
# server.py
_layout_path: Path | None = None
_result: LayoutData | None = None
_config: dict | None = None

def run_editor(layout_path: Path, port: int = 8080) -> None:
    global _layout_path, _result, _config
    _layout_path = layout_path
    _result, _config = load_layout(layout_path)

    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=port)
```

### 2. API Endpoint Pattern

Standard CRUD for layout editing:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve HTML |
| `/api/layout` | GET | Get full layout |
| `/api/layout` | PUT | Save to file |
| `/api/piece/{container}/{index}` | PATCH | Update single item |
| `/api/move-piece` | POST | Move between containers |
| `/api/validate` | POST | Check overlaps/bounds |

### 3. Pydantic Schemas

```python
class ItemPosition(BaseModel):
    name: str
    x: int
    y: int
    width: int
    height: int

class ItemUpdate(BaseModel):
    x: int | None = None
    y: int | None = None
    rotated: bool | None = None

class MoveRequest(BaseModel):
    from_container: int
    item_index: int
    to_container: int
    x: int
    y: int
```

### 4. Single-File HTML UI

Embed CSS and JS in one HTML file served by FastAPI:

```python
@app.get("/", response_class=HTMLResponse)
async def serve_editor() -> HTMLResponse:
    html_path = Path(__file__).parent / "static" / "editor.html"
    return HTMLResponse(content=html_path.read_text())
```

### 5. SVG for 2D Layout

Render items as SVG rectangles with labels:

```javascript
const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
svg.setAttribute('viewBox', `0 0 ${width * scale} ${height * scale}`);

items.forEach((item, idx) => {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', item.x * scale);
    rect.setAttribute('y', item.y * scale);
    rect.setAttribute('width', item.width * scale);
    rect.setAttribute('height', item.height * scale);
    rect.setAttribute('data-index', idx);
    svg.appendChild(rect);
});
```

## Cross-Container Drag-and-Drop

See [references/drag-drop-pattern.md](references/drag-drop-pattern.md) for the complete ghost-based drag pattern.

**Key insight**: Items rendered inside different SVGs cannot visually cross boundaries. Use a DOM ghost element that follows the cursor globally.

### Quick Reference

```javascript
// 1. Create ghost on drag start
const ghost = document.createElement('div');
ghost.className = 'drag-ghost';
ghost.style.width = (piece.width * scale) + 'px';
ghost.style.position = 'fixed';
ghost.style.pointerEvents = 'none';
document.body.appendChild(ghost);

// 2. Position ghost at cursor during drag
ghost.style.left = (e.clientX - width/2) + 'px';
ghost.style.top = (e.clientY - height/2) + 'px';

// 3. On drop, calculate position relative to TARGET container
const targetRect = targetSvg.getBoundingClientRect();
let dropX = (e.clientX - targetRect.left) / scale - piece.width / 2;
let dropY = (e.clientY - targetRect.top) / scale - piece.height / 2;

// 4. Clamp to bounds
dropX = Math.max(0, Math.min(dropX, containerWidth - piece.width));
```

## File Structure

```
project/
├── pyproject.toml          # Add fastapi, uvicorn as optional deps
├── src/package/
│   ├── cli.py              # Add 'edit' command
│   ├── layout_io.py        # JSON save/load
│   └── editor/
│       ├── __init__.py     # Export run_editor
│       ├── server.py       # FastAPI app
│       ├── schemas.py      # Pydantic models
│       └── static/
│           └── editor.html # Single-file UI
```

## Dependencies

```toml
[project.optional-dependencies]
editor = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
]
```

## CLI Integration

```python
def edit(args) -> int:
    import webbrowser
    from .editor import run_editor

    layout_path = Path(args.layout)
    port = args.port or 8080

    if not args.no_browser:
        webbrowser.open(f"http://localhost:{port}")

    run_editor(layout_path, port)
    return 0
```

## Validation Pattern

Check bounds and overlaps server-side:

```python
def validate_layout() -> ValidationResult:
    errors = []
    for container_idx, container in enumerate(containers):
        for item in container.items:
            # Bounds check
            if item.x + item.width > container_width:
                errors.append(ValidationError(
                    container=container_idx,
                    item=item.name,
                    error="Exceeds right boundary"
                ))

        # Overlap check
        for i, item1 in enumerate(container.items):
            for item2 in container.items[i+1:]:
                if rectangles_overlap(item1, item2):
                    errors.append(...)

    return ValidationResult(valid=len(errors) == 0, errors=errors)
```
