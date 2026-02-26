---
name: d2
description: >
  Use when writing, generating, reviewing, or improving D2 diagram code.
  Trigger when the user asks to create architecture diagrams, flowcharts,
  sequence diagrams, ER diagrams, class diagrams, or any diagram using D2 syntax.
  Also trigger when working with .d2 files or when the d2_render MCP tool is available.
---

# D2 Diagram Language Reference

D2 is a declarative diagram scripting language that compiles to SVG. Text → diagrams.
Docs: https://d2lang.com | Playground: https://play.d2lang.com

---

## Core Syntax

### Shapes

```d2
# Bare identifier = rectangle by default
server

# With a display label (key vs label)
server: "API Server"

# Set shape type
db: {
  shape: cylinder
}

# Multiple on one line
web; app; db
```

**Available shape types:**
`rectangle` (default), `square`, `circle`, `oval`, `diamond`, `hexagon`, `cloud`,
`cylinder`, `queue`, `package`, `parallelogram`, `document`, `page`, `step`,
`callout`, `stored_data`, `person`, `c4-person`,
`sql_table`, `class`, `sequence_diagram`, `image`

### Connections

```d2
A -> B          # directed arrow
A <- B          # reverse
A -- B          # undirected line
A <-> B         # bidirectional

A -> B: label   # with label

# Chaining
A -> B -> C -> D

# Multiple connections (creates separate arrows, not override)
A -> B
A -> B          # second distinct arrow

# Referencing a specific connection (0-indexed)
(A -> B)[0].style.stroke: red
```

### Containers (nesting)

```d2
cloud: {
  label: "AWS"
  vpc: {
    web: "Web Tier"
    app: "App Tier"
    web -> app
  }
}

# Cross-container connections using _ (parent reference)
cloud: {
  aws: {
    db
    db -> _.gcloud.backup    # _ = parent scope
  }
  gcloud: {
    backup
  }
}
```

### Text and Markdown

```d2
# Standalone markdown block
explanation: |md
  ## Architecture Overview
  This diagram shows the **three-tier** architecture.
  - Web tier
  - App tier
  - Data tier
|

# LaTeX / math
formula: |latex
  \frac{\partial f}{\partial x} = 2x
|
```

---

## Style Reference

All styles live under the `style` key:

```d2
my_shape: {
  style: {
    fill: "#4a90d9"          # background color
    stroke: "#2c5f8a"        # border color
    stroke-width: 2
    stroke-dash: 5           # dashed border
    border-radius: 8         # rounded corners
    font-size: 14
    font-color: white
    opacity: 0.9
    shadow: true
    bold: true
    italic: false
    3d: true                 # rectangles/squares only
    multiple: true           # stacked visual effect
    double-border: true      # rectangles and ovals only
    text-transform: uppercase
  }
}
```

**Connection styles:**
```d2
A -> B: {
  style: {
    stroke: red
    stroke-width: 3
    stroke-dash: 5
    animated: true           # flowing animation in SVG
    bold: true
    font-color: "#666"
  }
}
```

**Arrowheads:**
```d2
A -> B: {
  source-arrowhead: {
    shape: diamond
    style.filled: true
  }
  target-arrowhead: {
    shape: circle
  }
}
```
Arrowhead shapes: `triangle` (default), `arrow`, `diamond`, `circle`, `box`,
`cf-one`, `cf-many`, `cf-one-required`, `cf-many-required`, `cross`

---

## Global Styling with Globs

Apply styles to all shapes or connections at once:

```d2
# Style all shapes
*.style.fill: "#f0f4ff"
*.style.stroke: "#3b5bdb"
*.style.border-radius: 6

# Style all connections
(* -> *)[*].style.stroke: "#888"
(* -> *)[*].style.animated: true

# Scoped globs (only inside a container)
cloud: {
  *.style.fill: "#e8f5e9"
}
```

---

## Variables and Substitutions

```d2
vars: {
  primary: "#3b5bdb"
  secondary: "#74c0fc"
  accent: "#f06595"

  # In-file config (overridden by CLI flags)
  d2-config: {
    layout-engine: elk
    theme-id: 0
  }
}

server: {
  style.fill: ${primary}
  style.stroke: ${secondary}
}
```

---

## Reusable Style Classes

```d2
classes: {
  important: {
    style: {
      stroke: red
      stroke-width: 3
      bold: true
    }
  }
  faded: {
    style: {
      opacity: 0.4
    }
  }
}

# Apply to shapes
critical_db.class: important
legacy_service.class: faded

# Apply multiple (left-to-right, later wins)
service.class: [important; faded]

# Apply to connections
A -> B: {class: important}
```

---

## SQL Tables (ER Diagrams)

```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: varchar {constraint: unique}
  name: varchar
  org_id: int {constraint: foreign_key}
  created_at: timestamp
}

organizations: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar
}

# Foreign key connection
users.org_id -> organizations.id

# Multiple constraints
users: {
  shape: sql_table
  id: int {constraint: [primary_key; not_null]}
}
```

---

## UML Class Diagrams

```d2
UserService: {
  shape: class

  # Fields: visibility prefix + name: type
  -users: User[]
  +db: Database
  #cache: Cache

  # Methods: visibility + name(params): return
  +getUser(id: string): User
  +createUser(data: UserInput): User
  -validateEmail(email: string): bool
}
```

Visibility: `+` public, `-` private, `#` protected

---

## Sequence Diagrams

```d2
auth_flow: {
  shape: sequence_diagram

  # Actors are auto-created on first reference
  # but explicit order controls visual position
  client
  gateway
  auth_service
  db

  client -> gateway: "POST /login"
  gateway -> auth_service: "validate(credentials)"
  auth_service -> db: "SELECT user WHERE email=?"
  db -> auth_service: "user record"
  auth_service -> gateway: "JWT token"
  gateway -> client: "200 OK + token"

  # Notes (standalone shape on actor with no connections)
  auth_service."validates password hash"

  # Groups / fragments
  retry: {
    gateway -> auth_service: "retry"
  }
}
```

---

## Icons

```d2
# Icon from URL (Terrastruct's free icon library)
server: {
  icon: https://icons.terrastruct.com/tech/server.svg
}

# Local file
logo: {
  icon: ./assets/logo.png
}

# Standalone image shape
github: {
  shape: image
  icon: https://icons.terrastruct.com/social/github.svg
}

# Control icon position
server: {
  icon: https://icons.terrastruct.com/tech/server.svg
  icon.near: top-left
}
```

Free icons: https://icons.terrastruct.com

---

## Composition: Layers, Scenarios, Steps

```d2
# Layers: independent views (no inheritance)
layers: {
  overview: {
    web -> app -> db
  }
  detailed: {
    web: "Nginx" { shape: rectangle }
    web -> app: "HTTP/1.1"
    app -> db: "PostgreSQL wire protocol"
  }
}

# Scenarios: variations on base diagram
web -> app -> db

scenarios: {
  with_cache: {
    app -> cache: "read-through"
  }
  with_cdn: {
    cdn -> web
  }
}

# Steps: sequential, each inherits previous
steps: {
  s1: { user }
  s2: { user -> web }
  s3: { user -> web -> app }
  s4: { user -> web -> app -> db }
}
```

---

## Themes

Set via CLI: `d2 --theme=0 input.d2 output.svg`
Or in-file: `vars: { d2-config: { theme-id: 300 } }`

| ID  | Name                    | Character         |
|-----|-------------------------|-------------------|
| 0   | Neutral Default         | Clean, professional |
| 1   | Neutral Grey            | Muted, monochrome |
| 3   | Flagship Terrastruct    | Vibrant, colorful |
| 4   | Cool Classics           | Blues and greens  |
| 8   | Colorblind Clear        | Accessible palette |
| 200 | Dark Mauve              | Dark mode         |
| 300 | Terminal                | Monospace, hacky  |
| 302 | Origami                 | Paper aesthetic   |
| 303 | C4                      | Architecture style|

**Theme overrides** (fine-tune colors):
```d2
vars: {
  d2-config: {
    theme-overrides: {
      B1: "#0057b8"    # primary brand color
      N7: "#1a1a2e"    # darkest neutral
    }
  }
}
```

Color codes: `N1`–`N7` (neutrals), `B1`–`B6` (brand), `AA2`–`AA5` (accent A), `AB4`–`AB5` (accent B)

---

## Layouts

Set via CLI: `d2 --layout=elk input.d2 output.svg`
Or in-file: `vars: { d2-config: { layout-engine: elk } }`

| Engine | Best For                          | Notes                              |
|--------|-----------------------------------|------------------------------------|
| dagre  | **Everything — use this always**  | Fast, handles nested containers and cross-container connections well |
| elk    | Only if user explicitly requests it | Extremely slow in WASM (minutes per render). Do not choose it yourself. |

**Default rule: never set `layout-engine` at all.** Dagre is the default and handles the vast majority of diagrams well, including nested containers and cross-container connections. Only set `layout-engine: elk` if the user specifically asks for it.

**Direction control:**
```d2
direction: right    # top-level: up, down, left, right

# ELK supports per-container direction
container: {
  direction: right
  a -> b -> c
}
```

---

## Imports

```d2
# Spread file contents into current scope
...@shared_styles.d2

# Assign file to a key
network: @network_diagram.d2

# Import specific object from file
db_schema: @schema.users
```

---

## Beautiful Diagram Patterns

### Architecture Diagram

```d2
# Global style
*.style.border-radius: 6
*.style.font-size: 13

direction: right

internet: {
  shape: cloud
  label: "Internet"
}

frontend: {
  label: "Frontend\n(React)"
  icon: https://icons.terrastruct.com/dev/react.svg
  style.fill: "#e8f4fd"
}

api: {
  label: "API Gateway"
  style.fill: "#fff3cd"
}

services: {
  label: "Microservices"
  style.fill: "#f8f9fa"

  auth: "Auth Service"
  orders: "Orders Service"
  payments: "Payments Service"
}

db: {
  shape: cylinder
  label: "PostgreSQL"
  style.fill: "#d4edda"
}

cache: {
  shape: queue
  label: "Redis"
  style.fill: "#fce8e6"
}

internet -> frontend
frontend -> api: "HTTPS"
api -> services.auth: "JWT validate"
api -> services.orders
api -> services.payments
services.orders -> db
services.payments -> db
services.auth -> cache: "session"
```

### Flowchart

```d2
direction: down

start: {shape: circle; style.fill: "#4caf50"; style.font-color: white}
end: {shape: circle; style.fill: "#f44336"; style.font-color: white; label: "End"}
decision: {shape: diamond; label: "Valid?"}
process: "Process Request"
error: "Return Error"

start -> process
process -> decision
decision -> end: "Yes"
decision -> error: "No"
error -> start: "Retry"
```

### ER Diagram

```d2
users: {
  shape: sql_table
  id: uuid {constraint: primary_key}
  email: varchar(255) {constraint: [unique; not_null]}
  name: varchar(100)
  created_at: timestamptz
}

posts: {
  shape: sql_table
  id: uuid {constraint: primary_key}
  author_id: uuid {constraint: foreign_key}
  title: varchar(255)
  body: text
  published_at: timestamptz
}

comments: {
  shape: sql_table
  id: uuid {constraint: primary_key}
  post_id: uuid {constraint: foreign_key}
  author_id: uuid {constraint: foreign_key}
  body: text
}

posts.author_id -> users.id
comments.post_id -> posts.id
comments.author_id -> users.id
```

---

## Saving Rendered SVGs

Always make **two `d2_render` calls** and save three files:

**Step 1 — Render for saving** (full SVG with embedded fonts, for browser viewing):
```
d2_render(d2_code=..., skip_fonts=false)
```
Save this output as `diagrams/<stem>.svg`

**Step 2 — Render for display** (fonts stripped, compact for LLM context):
```
d2_render(d2_code=..., skip_fonts=true)
```
Use this output to show the diagram in the conversation.

**Convention:**
- Directory: `diagrams/` (relative to the current project root; create if it doesn't exist)
- Filename stem: `YYYY-MM-DD_HH-MM_<slug>`
  - Timestamp uses local time in 24-hour format
  - Slug is 2–4 words derived from the diagram's subject, lowercase, hyphenated
  - Example stem: `2025-02-20_14-32_auth-flow-sequence`
  - Example stem: `2025-02-20_09-05_aws-three-tier-architecture`
  - Example stem: `2025-02-20_17-45_users-orders-er-diagram`

**Save two files with the same stem:**
1. `diagrams/<stem>.d2` — the D2 source code (use the Write tool)
2. `diagrams/<stem>.svg` — the full SVG from Step 1 (use the Write tool)

**After saving**, tell the user both paths so they can edit the source or open the SVG in a browser.

SVG files open directly in any browser and are fully interactive (tooltips, links, animations).

---

## Quick Tips

- **Keys vs Labels**: The key is the identifier (`my_shape`); the label is the display text (`my_shape: "Display Text"`). Connections use keys, not labels.
- **Semicolons** separate multiple declarations on one line: `a; b; c` or `a -> b -> c`
- **Repeated connections** each create a *new* arrow — D2 does not merge them
- **`_` (underscore)** refers to the parent container, useful for cross-container connections
- **`near` keyword** positions shapes or icons relative to constants: `top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`
- **SVG class attributes** are written from D2's `class` property, enabling CSS/JS post-processing
- **Animated connections** (`style.animated: true`) create flowing arrows in SVG output
- Use `style.multiple: true` for a "stacked documents" visual effect
- SQL tables: `stroke` styles the body, `fill` styles the header
- Avoid `width`/`height` on containers with dagre — use elk for that feature
