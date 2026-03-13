---
name: a2ui
description: Comprehensive guide and utilities for building AI agents that generate Agent-Driven Interfaces (A2UI). Use when implementing declarative UI generation, streaming component-based interfaces, or integrating A2UI with A2A protocol.
argument-hint: "[component-type: server|renderer]"
---

# A2UI Protocol Implementation Guide

This skill provides comprehensive knowledge for building AI agents that generate rich, adaptive user interfaces using the **A2UI Protocol v0.8**.

> **Reference**: https://a2ui.org/specification/v0.8-a2ui/

---

## Protocol Overview

A2UI is a JSONL-based streaming UI protocol enabling AI agents to generate declarative, interactive interfaces that render natively across platforms.

### Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Security** | Declarative JSON, not executable code. Agents use pre-approved component catalogs. |
| **LLM Compatibility** | Flat streaming JSON structure for incremental generation. |
| **Framework Agnostic** | Same response renders across React, Flutter, Angular, native mobile. |
| **Progressive Rendering** | UI streams incrementally for real-time updates. |

### Architecture Flow

```
User Input → Agent → A2UI Messages (JSONL Stream) → Client Renderer → Native UI
                                                              ↓
                                                    User Interaction
                                                              ↓
                                                    userAction → Agent
```

---

## Core Concepts

### 1. Surface

A **Surface** is a distinct, controllable region of the client's UI. Each surface has:
- Unique `surfaceId`
- Component hierarchy (adjacency list)
- Data model (state container)
- Root component reference

```json
{
  "surfaceId": "main",
  "components": { ... },
  "dataModel": { ... },
  "rootId": "root-component"
}
```

### 2. Adjacency List Model

Components are stored as a **flat map** where parent-child relationships use ID references, not nesting:

```json
{
  "components": [
    {
      "id": "card-1",
      "component": {
        "Card": {
          "children": {
            "explicitList": ["card-1-content"]
          }
        }
      }
    },
    {
      "id": "card-1-content",
      "component": {
        "Column": {
          "children": {
            "explicitList": ["card-1-title", "card-1-body"]
          }
        }
      }
    },
    {
      "id": "card-1-title",
      "component": {
        "Text": {
          "text": {"literalString": "Hello World"},
          "usageHint": "h2"
        }
      }
    }
  ]
}
```

### 3. BoundValue System

Properties that can be data-bound accept a `BoundValue` object:

| Property | Type | Description |
|----------|------|-------------|
| `literalString` | string | Static string value |
| `literalNumber` | number | Static number value |
| `literalBoolean` | boolean | Static boolean value |
| `path` | string | JSON Pointer to data model (e.g., `/user/name`) |

**Examples:**

```json
// Literal value only
{"literalString": "Hello"}

// Data binding only
{"path": "/user/name"}

// Combined (initialize and bind)
{
  "literalString": "Default Name",
  "path": "/user/name"
}
```

### 4. Data Model

The data model stores dynamic state accessible via JSON Pointer paths:

```json
{
  "dataModel": {
    "contents": [
      {"key": "user", "valueMap": [
        {"key": "name", "valueString": "John"},
        {"key": "age", "valueNumber": 30}
      ]},
      {"key": "items", "valueList": [
        {"valueString": "Item 1"},
        {"valueString": "Item 2"}
      ]}
    ]
  }
}
```

**Value Types:**
- `valueString`: String values
- `valueNumber`: Numeric values
- `valueBoolean`: Boolean values
- `valueMap`: Nested objects (array of key-value pairs)
- `valueList`: Arrays

---

## Message Types (Server → Client)

### 1. surfaceUpdate

Delivers component definitions to a surface:

```json
{
  "surfaceUpdate": {
    "surfaceId": "main",
    "components": [
      {
        "id": "title",
        "component": {
          "Text": {
            "text": {"literalString": "Welcome"},
            "usageHint": "h1"
          }
        }
      }
    ]
  }
}
```

### 2. dataModelUpdate

Updates the surface's data model:

```json
{
  "dataModelUpdate": {
    "surfaceId": "main",
    "contents": [
      {"key": "username", "valueString": "Alice"},
      {"key": "count", "valueNumber": 42}
    ]
  }
}
```

### 3. beginRendering

Signals the client to render the surface:

```json
{
  "beginRendering": {
    "surfaceId": "main",
    "root": "root-component-id",
    "catalogId": "https://a2ui.org/specification/v0_8/standard_catalog_definition.json"
  }
}
```

### 4. deleteSurface

Removes a surface and its contents:

```json
{
  "deleteSurface": {
    "surfaceId": "secondary-panel"
  }
}
```

### Message Ordering

**Required sequence:**
1. `surfaceUpdate` (components)
2. `dataModelUpdate` (data)
3. `beginRendering` (trigger render)

---

## Standard Component Catalog (v0.8)

Catalog ID: `https://a2ui.org/specification/v0_8/standard_catalog_definition.json`

### Text

Displays text content with semantic hints:

```json
{
  "Text": {
    "text": {"literalString": "Hello World"},
    "usageHint": "h1"
  }
}
```

**usageHint Values:** `h1`, `h2`, `h3`, `body`, `caption`

### Image

Renders images from URLs:

```json
{
  "Image": {
    "url": {"literalString": "https://example.com/image.png"},
    "alt": {"literalString": "Description"}
  }
}
```

### Button

Interactive button with action handling:

```json
{
  "Button": {
    "label": {"literalString": "Submit"},
    "action": {
      "name": "submit_form",
      "context": [
        {"key": "formId", "value": {"literalString": "contact-form"}}
      ]
    }
  }
}
```

**Action Properties:**
- `name`: Action identifier sent to server
- `context`: Key-value pairs resolved against data model

### Card

Container with single child:

```json
{
  "Card": {
    "title": {"literalString": "Card Title"},
    "children": {
      "explicitList": ["card-content-id"]
    }
  }
}
```

### Row

Horizontal layout container:

```json
{
  "Row": {
    "children": {
      "explicitList": ["child-1", "child-2", "child-3"]
    },
    "alignment": "center"
  }
}
```

**Alignment:** `start`, `center`, `end`, `spaceBetween`, `spaceAround`

### Column

Vertical layout container:

```json
{
  "Column": {
    "children": {
      "explicitList": ["child-1", "child-2"]
    },
    "alignment": "start"
  }
}
```

### List

Dynamic list with template rendering:

```json
{
  "List": {
    "children": {
      "template": {
        "dataPath": "/items",
        "componentId": "item-template"
      }
    }
  }
}
```

### ListItem

Template for list items:

```json
{
  "ListItem": {
    "title": {"path": "/title"},
    "subtitle": {"path": "/subtitle"},
    "trailing": {"path": "/price"}
  }
}
```

---

## User Actions (Client → Server)

When users interact with components having `action` definitions:

```json
{
  "userAction": {
    "name": "submit_form",
    "surfaceId": "main",
    "sourceComponentId": "submit-button",
    "timestamp": "2024-01-01T12:00:00Z",
    "context": {
      "formId": "contact-form",
      "userName": "Alice"
    }
  }
}
```

**Fields:**
- `name`: Action identifier from component's `action.name`
- `surfaceId`: Originating surface
- `sourceComponentId`: Component that triggered the action
- `timestamp`: ISO 8601 timestamp
- `context`: Resolved `action.context` with all BoundValues evaluated

---

## A2A Integration

A2UI integrates with A2A protocol via the extension URI:
`https://a2ui.org/a2a-extension/a2ui/v0.8`

### Agent Card Declaration

```json
{
  "capabilities": {
    "extensions": ["https://a2ui.org/a2a-extension/a2ui/v0.8"]
  },
  "a2uiParams": {
    "supportedCatalogIds": [
      "https://a2ui.org/specification/v0_8/standard_catalog_definition.json"
    ],
    "acceptsInlineCatalogs": false
  }
}
```

### A2A DataPart Format

A2UI messages travel as A2A `DataPart` objects:

```json
{
  "type": "data",
  "mimeType": "application/json+a2ui",
  "data": {
    "surfaceUpdate": { ... }
  }
}
```

---

## Implementation Guide

### Python A2UI Builder

```python
from typing import Any, Optional
from dataclasses import dataclass, field
import json

@dataclass
class BoundValue:
    literal_string: Optional[str] = None
    literal_number: Optional[float] = None
    literal_boolean: Optional[bool] = None
    path: Optional[str] = None

    def to_dict(self) -> dict:
        result = {}
        if self.literal_string is not None:
            result["literalString"] = self.literal_string
        if self.literal_number is not None:
            result["literalNumber"] = self.literal_number
        if self.literal_boolean is not None:
            result["literalBoolean"] = self.literal_boolean
        if self.path is not None:
            result["path"] = self.path
        return result

class A2UIBuilder:
    def __init__(self, surface_id: str = "main"):
        self.surface_id = surface_id
        self.components: list[dict] = []
        self.data_model: list[dict] = []

    # --- Component Methods ---

    def text(
        self,
        id: str,
        text: str | BoundValue,
        usage_hint: str = "body"
    ) -> "A2UIBuilder":
        text_val = (
            text.to_dict() if isinstance(text, BoundValue)
            else {"literalString": text}
        )
        self.components.append({
            "id": id,
            "component": {
                "Text": {
                    "text": text_val,
                    "usageHint": usage_hint
                }
            }
        })
        return self

    def image(
        self,
        id: str,
        url: str | BoundValue,
        alt: Optional[str] = None
    ) -> "A2UIBuilder":
        url_val = (
            url.to_dict() if isinstance(url, BoundValue)
            else {"literalString": url}
        )
        img = {"url": url_val}
        if alt:
            img["alt"] = {"literalString": alt}
        self.components.append({
            "id": id,
            "component": {"Image": img}
        })
        return self

    def button(
        self,
        id: str,
        label: str,
        action_name: str,
        context: Optional[dict] = None
    ) -> "A2UIBuilder":
        action = {"name": action_name}
        if context:
            action["context"] = [
                {"key": k, "value": {"literalString": str(v)}}
                for k, v in context.items()
            ]
        self.components.append({
            "id": id,
            "component": {
                "Button": {
                    "label": {"literalString": label},
                    "action": action
                }
            }
        })
        return self

    def card(
        self,
        id: str,
        title: Optional[str] = None,
        children: Optional[list[str]] = None
    ) -> "A2UIBuilder":
        card = {}
        if title:
            card["title"] = {"literalString": title}
        if children:
            card["children"] = {"explicitList": children}
        self.components.append({
            "id": id,
            "component": {"Card": card}
        })
        return self

    def row(
        self,
        id: str,
        children: list[str],
        alignment: str = "start"
    ) -> "A2UIBuilder":
        self.components.append({
            "id": id,
            "component": {
                "Row": {
                    "children": {"explicitList": children},
                    "alignment": alignment
                }
            }
        })
        return self

    def column(
        self,
        id: str,
        children: list[str],
        alignment: str = "start"
    ) -> "A2UIBuilder":
        self.components.append({
            "id": id,
            "component": {
                "Column": {
                    "children": {"explicitList": children},
                    "alignment": alignment
                }
            }
        })
        return self

    def list_item(
        self,
        id: str,
        title: str | BoundValue,
        subtitle: Optional[str | BoundValue] = None,
        trailing: Optional[str | BoundValue] = None
    ) -> "A2UIBuilder":
        def to_bound(val):
            if isinstance(val, BoundValue):
                return val.to_dict()
            return {"literalString": val}

        item = {"title": to_bound(title)}
        if subtitle:
            item["subtitle"] = to_bound(subtitle)
        if trailing:
            item["trailing"] = to_bound(trailing)

        self.components.append({
            "id": id,
            "component": {"ListItem": item}
        })
        return self

    # --- Data Model Methods ---

    def set_data(self, key: str, value: Any) -> "A2UIBuilder":
        if isinstance(value, str):
            self.data_model.append({"key": key, "valueString": value})
        elif isinstance(value, bool):
            self.data_model.append({"key": key, "valueBoolean": value})
        elif isinstance(value, (int, float)):
            self.data_model.append({"key": key, "valueNumber": value})
        elif isinstance(value, list):
            self.data_model.append({
                "key": key,
                "valueList": [self._convert_value(v) for v in value]
            })
        elif isinstance(value, dict):
            self.data_model.append({
                "key": key,
                "valueMap": [
                    {"key": k, **self._convert_value(v)}
                    for k, v in value.items()
                ]
            })
        return self

    def _convert_value(self, value: Any) -> dict:
        if isinstance(value, str):
            return {"valueString": value}
        elif isinstance(value, bool):
            return {"valueBoolean": value}
        elif isinstance(value, (int, float)):
            return {"valueNumber": value}
        return {"valueString": str(value)}

    # --- Build Methods ---

    def build_surface_update(self) -> dict:
        return {
            "surfaceUpdate": {
                "surfaceId": self.surface_id,
                "components": self.components
            }
        }

    def build_data_model_update(self) -> dict:
        return {
            "dataModelUpdate": {
                "surfaceId": self.surface_id,
                "contents": self.data_model
            }
        }

    def build_begin_rendering(self, root_id: str) -> dict:
        return {
            "beginRendering": {
                "surfaceId": self.surface_id,
                "root": root_id,
                "catalogId": "https://a2ui.org/specification/v0_8/standard_catalog_definition.json"
            }
        }

    def build_all(self, root_id: str) -> list[dict]:
        """Returns all messages in correct order."""
        messages = [self.build_surface_update()]
        if self.data_model:
            messages.append(self.build_data_model_update())
        messages.append(self.build_begin_rendering(root_id))
        return messages
```

### Example: Travel Card Generator

```python
def generate_travel_card(destination: dict) -> list[dict]:
    builder = A2UIBuilder(surface_id="main")

    # Build component hierarchy
    builder.card("card-root", title=destination["name"], children=["card-content"])
    builder.column("card-content", children=["card-image", "card-info", "card-actions"])
    builder.image("card-image", url=destination["image_url"], alt=destination["name"])
    builder.column("card-info", children=["card-desc", "card-price"])
    builder.text("card-desc", text=destination["description"], usage_hint="body")
    builder.text("card-price", text=f"${destination['price']}", usage_hint="h3")
    builder.row("card-actions", children=["btn-details", "btn-book"])
    builder.button(
        "btn-details",
        label="View Details",
        action_name="view_details",
        context={"destinationId": destination["id"]}
    )
    builder.button(
        "btn-book",
        label="Book Now",
        action_name="book_destination",
        context={"destinationId": destination["id"]}
    )

    # Set data model
    builder.set_data("destination", destination)

    return builder.build_all(root_id="card-root")
```

### SSE Streaming Example (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import json

app = FastAPI()

async def generate_a2ui_stream(user_message: str):
    builder = A2UIBuilder()

    # Stream surfaceUpdate
    builder.text("loading", "Processing your request...", "body")
    yield {
        "event": "message",
        "data": json.dumps(builder.build_surface_update())
    }

    # Simulate processing...
    result = await process_request(user_message)

    # Stream updated components
    builder = A2UIBuilder()
    builder.text("result-title", "Results", "h2")
    builder.text("result-content", result, "body")
    yield {
        "event": "message",
        "data": json.dumps(builder.build_surface_update())
    }

    # Stream beginRendering
    yield {
        "event": "message",
        "data": json.dumps(builder.build_begin_rendering("result-title"))
    }

    yield {"event": "done", "data": json.dumps({"status": "complete"})}

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return EventSourceResponse(generate_a2ui_stream(request.message))
```

---

## TypeScript Renderer Types

```typescript
// BoundValue resolution
interface BoundValue {
  literalString?: string;
  literalNumber?: number;
  literalBoolean?: boolean;
  path?: string;
}

// Component wrapper
interface A2UIComponent {
  id: string;
  component: {
    Text?: TextComponent;
    Image?: ImageComponent;
    Button?: ButtonComponent;
    Card?: CardComponent;
    Row?: RowComponent;
    Column?: ColumnComponent;
    List?: ListComponent;
    ListItem?: ListItemComponent;
  };
}

// Surface state
interface Surface {
  surfaceId: string;
  components: Map<string, A2UIComponent>;
  dataModel: Map<string, any>;
  rootId: string | null;
  isReady: boolean;
}

// Message types
interface SurfaceUpdate {
  surfaceUpdate: {
    surfaceId: string;
    components: A2UIComponent[];
  };
}

interface DataModelUpdate {
  dataModelUpdate: {
    surfaceId: string;
    contents: DataModelContent[];
  };
}

interface BeginRendering {
  beginRendering: {
    surfaceId: string;
    root: string;
    catalogId?: string;
  };
}

// User action
interface UserAction {
  userAction: {
    name: string;
    surfaceId: string;
    sourceComponentId: string;
    timestamp: string;
    context: Record<string, any>;
  };
}

// Utility: Resolve BoundValue
function resolveBoundValue(
  boundValue: BoundValue,
  dataModel: Map<string, any>
): any {
  if (boundValue.path) {
    return getValueAtPath(dataModel, boundValue.path);
  }
  return boundValue.literalString
    ?? boundValue.literalNumber
    ?? boundValue.literalBoolean;
}
```

---

## Best Practices

### 1. Component ID Strategy
Use consistent, meaningful IDs with prefixes:
```
card-{entityId}
card-{entityId}-title
card-{entityId}-content
btn-{action}-{entityId}
```

### 2. Data Separation
Keep large data in the data model, reference via paths:
```json
// Good: Data in model, bound in component
{"text": {"path": "/article/content"}}

// Avoid: Large data inline
{"text": {"literalString": "Very long text..."}}
```

### 3. Streaming Order
Always send messages in order:
1. `surfaceUpdate` (structure)
2. `dataModelUpdate` (state)
3. `beginRendering` (render trigger)

### 4. Progressive Updates
For long operations, send intermediate updates:
```python
# Initial loading state
yield surface_update(loading_component)
yield begin_rendering("loading")

# Final result
yield surface_update(result_components)
yield data_model_update(result_data)
yield begin_rendering("result-root")
```

### 5. Action Context
Include all necessary data in action context:
```json
{
  "action": {
    "name": "add_to_cart",
    "context": [
      {"key": "productId", "value": {"path": "/product/id"}},
      {"key": "quantity", "value": {"literalNumber": 1}}
    ]
  }
}
```

---

## References

- **Official Site**: https://a2ui.org/
- **v0.8 Specification**: https://a2ui.org/specification/v0.8-a2ui/
- **A2A Extension**: https://a2ui.org/specification/v0.8-a2a-extension/
- **GitHub Repository**: https://github.com/google/A2UI
- **Standard Catalog**: https://a2ui.org/specification/v0_8/standard_catalog_definition.json
