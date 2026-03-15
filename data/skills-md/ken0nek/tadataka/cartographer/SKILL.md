---
name: cartographer
description: >
  iOS and Android UI element discovery and navigation mapping using agent-device CLI.
  Use this skill whenever the user wants to: find element locators/identifiers on a mobile screen,
  get accessibility info for XCUITest or Espresso automation, snapshot a screen's UI elements,
  navigate to a specific screen and capture its elements, map navigation flows between screens,
  explore an app's screen topology, audit accessibility identifier coverage,
  or anything involving "what elements are on this screen" or "how do I get to that screen."
  Triggers on: locators, identifiers, elements, snapshot, screen map, navigation graph,
  accessibility audit, explore app, UI catalog, XCUITest elements, view hierarchy,
  Appium locators, test automation elements, screen discovery, element catalog, cartographer,
  android elements, espresso locators, package name, android snapshot.
  Even if they don't mention Cartographer by name, use this skill for any mobile UI element discovery task.
---

# Cartographer

> Named after Inō Tadataka, who spent 17 years walking Japan's coastline to produce its first accurate map.
> This skill walks your app's UI so you don't have to.

Uses `agent-device` CLI to snapshot, navigate, and explore iOS/Android app UIs, then formats
results into structured catalogs usable for test automation (XCUITest, Espresso, Appium, etc.).

## Prerequisites

- `agent-device` installed:
  - npm: `npm install -g agent-device`
  - mise: `mise use -g npm:agent-device`
- Simulator/emulator running with the target app installed
- App launched and in the desired state (e.g., logged in)

Check readiness:
```bash
which agent-device && echo "Ready" || echo "Install: npm install -g agent-device  OR  mise use -g npm:agent-device"
```

Discover available devices and apps:
```bash
agent-device devices          # list simulators/emulators
agent-device apps             # list installed apps on running device
```

Note: `open` accepts human-readable app names (e.g., `Settings`, `Hulu`) as well as bundle IDs / package names.

## Three Modes

| Mode | When to use | Time |
|---|---|---|
| **Snapshot** | "What elements are on this screen?" | ~5 sec |
| **Navigate + Snapshot** | "Show me the Search tab locators" | ~15 sec |
| **Explore** | "Map the whole app's screens and navigation" | 2–10 min |

Always start with the simplest mode that answers the user's question.

---

## Mode 1: Snapshot Current Screen

The daily driver. Captures every interactive element on whatever screen is currently visible.

### Steps

1. **Open session** (if not already open):

   **iOS:**
   ```bash
   agent-device open com.hulu.plus --platform ios
   ```
   **Android:**
   ```bash
   agent-device open com.hulu.plus --platform android --serial <device-serial>
   ```
   If the user hasn't specified a bundle/package name, ask — or use `agent-device apps` to list installed apps.
   Both platforms use reverse-domain identifiers (e.g., `com.hulu.plus`). Android uses `--serial` for device targeting.
   `open` also accepts human-readable names: `agent-device open Hulu --platform ios`.
   If the app is already open, use `agent-device open --platform ios` to attach.

2. **Snapshot interactive elements:**
   ```bash
   agent-device snapshot -i --json
   ```
   `-i` = interactive only (buttons, cells, fields, switches). `--json` = structured output.

3. **Scroll to discover off-screen elements** (if element count seems low or the screen is scrollable):
   ```bash
   agent-device scroll                  # scroll down
   agent-device snapshot -i --json      # capture newly visible elements
   ```
   Repeat until two consecutive snapshots return the same elements.

4. **Parse and format** into the element catalog format (see `references/output-formats.md`).

5. **Present results** as a clean table grouped by element type, AND offer JSON export.

### Variants

Full snapshot (all elements, not just interactive):
```bash
agent-device snapshot --json
```

Scoped to a container (e.g., "what's in the tab bar"):
```bash
agent-device snapshot -i -s "Tab Bar" --json
```

---

## Mode 2: Navigate + Snapshot

For when the user knows which screen they want but doesn't want to manually navigate there.

### Steps

1. **Open session:**

   **iOS:**
   ```bash
   agent-device open <bundle_id> --platform ios
   ```
   **Android:**
   ```bash
   agent-device open <package_name> --platform android --serial <device-serial>
   ```

2. **Navigate to the target screen:**

   **Tab navigation** (most common):
   ```bash
   agent-device snapshot -i --json          # See current state + tab bar refs
   agent-device press @<tab_ref>            # Tap the target tab
   agent-device snapshot -i --json          # Confirm arrival
   ```

   **Deep navigation** (screen behind taps):
   ```bash
   agent-device snapshot -i --json          # See what's tappable
   agent-device press @<element_ref>        # Tap to navigate
   agent-device snapshot -i --json          # See new screen
   ```

   **Find and tap by text:**
   ```bash
   agent-device find "Settings" click
   ```

   **Scroll to find off-screen elements:**
   ```bash
   agent-device scrollintoview "Sign In"
   agent-device find "Sign In" click
   ```

   **Combine navigate + snapshot with `batch`** to reduce round-trips:
   ```bash
   agent-device batch --steps '[
     {"command": "press", "positionals": ["@<tab_ref>"]},
     {"command": "snapshot", "flags": {"-i": true, "--json": true}}
   ]'
   ```

3. **Snapshot the target screen** and format results.

### Navigation tips

- Always re-snapshot after any interaction — refs go stale after UI changes
- For tabs, look for elements with role `[button]` inside a `[tab-bar]` container
- `agent-device back` for standard back navigation

---

## Mode 3: Explore (BFS Navigation Map)

Full app mapping. Systematically discovers screens and maps navigation flows.

### Before starting, confirm

- **Which app?** (bundle ID / package name)
- **Starting screen?** (usually Home)
- **Depth limit?** (default: 2)
- **Max screens?** (default: 15)
- **Max elements to tap per screen?** (default: 10)
- **Time limit?** (default: 5 minutes)

### Safety Rules — NEVER tap elements matching these

**Blocked identifiers** (case-insensitive substring):
`log_out`, `logout`, `sign_out`, `delete`, `remove_account`,
`subscribe`, `purchase`, `buy`, `upgrade`, `cancel_subscription`, `deactivate`

**Blocked labels** (case-insensitive substring):
`log out`, `sign out`, `delete account`, `subscribe`,
`purchase`, `upgrade`, `cancel subscription`

If in doubt, skip the element. Log what was skipped.

### Exploration Algorithm

```
VISITED = {}
EDGES = []
QUEUE = [(start_screen, depth=0)]

while QUEUE not empty AND within limits:
    current = QUEUE.pop(0)
    if current.depth >= max_depth: skip

    1. snapshot -i --json → interactive elements
    2. Fingerprint the screen (see below)
    3. Store in VISITED

    4. Select up to N tappable elements:
       - Prioritize WITH identifiers over without
       - Prioritize buttons over cells
       - Deduplicate: cell_item_0..49 → tap one
       - Skip dangerous elements

    5. For each selected element:
       a. Record pre-tap fingerprint
       b. agent-device press @<ref>
       c. Wait, then snapshot again
       d. Fingerprint new state

       Same screen → continue
       Known screen → record edge, go back
       NEW screen → capture, record edge, enqueue, go back

       e. agent-device back
       f. Verify return (compare fingerprint)
       g. If lost: perform tab reset (see below), then break
```

### Fingerprinting

Use `agent-device diff` to compare snapshots — no output means the screen is unchanged:
```bash
agent-device diff   # compare current snapshot to baseline; no output = same screen
```

For richer fingerprinting when `diff` alone is insufficient, compare manually:
1. Navigation bar title
2. Selected tab
3. Structural signature (top-level element types + counts)
4. Anchor identifiers (distinctive IDs that mark specific screens)

Same fingerprint = same screen. Structural, not content-based — dynamic content won't cause false positives.

### Tab Reset

**Tab reset** = navigate to a known safe state using the home screen or app root:

```bash
agent-device home                                        # go to device home screen
agent-device open <bundle_id> --platform ios             # re-enter app at root (iOS)
# or
agent-device open <package_name> --platform android --serial <device-serial>  # (Android)
```

Use tab reset when `agent-device back` fails or leaves the app in an unknown state. If reset also fails, log the stuck state and move on to the next queued element.

### After exploration

Export all three artifacts:
1. `element_catalog.json`
2. `navigation_map.mermaid`
3. `exploration_summary.txt`

For exact schemas, read `references/output-formats.md`.

---

## Element Roles

When classifying elements from snapshots:

| Role | Meaning | Typical element types |
|---|---|---|
| `nav` | Navigation trigger — tapping likely changes screen | button, cell, link (hittable) |
| `tab` | Tab bar item — top-level navigation | button inside tab-bar |
| `back` | Back/close/dismiss button | button with back/close/dismiss/done in id/label |
| `input` | Text input field | text-field, secure-text-field, search-field |
| `toggle` | State toggle | switch, segmented-control, slider |
| `scroll` | Scrollable container | collection-view, table, scroll-view |
| `content` | Static/informational | static-text, image, non-interactive |
| `dangerous` | Must never tap | matches blocked patterns |

---

## Response Guidelines

- **Show identifiers prominently** — the user's #1 need is locator strings
- **Group by element type** — buttons together, cells together, fields together
- **Flag elements without identifiers** — these are gaps the dev team should fix
- **Mode 1 & 2**: formatted table in chat + offer JSON export
- **Mode 3**: always export files (JSON + Mermaid + summary)
- Keep it practical — locators, not lectures

### Example response format

```
## Search Screen — 42 interactive elements

### Buttons (12)
| Identifier | Label | Hittable |
|---|---|---|
| tab_bar_home_button | Home | ✅ |
| tab_bar_search_button | Search | ✅ |

### Text Fields (1)
| Identifier | Label | Placeholder |
|---|---|---|
| search_bar | Search | Search for shows... |

### ⚠️ Elements without identifiers (11)
- [button] label="See All"
- [cell] label="Trending Now"
```

---

## Error Handling

| Problem | Solution |
|---|---|
| `agent-device` not installed | `npm install -g agent-device` or `mise use -g npm:agent-device` |
| No simulator running | `xcrun simctl boot "iPhone 16"` |
| App not installed | Tell user bundle ID not found; run `agent-device apps` to check |
| 0 elements returned | App not in foreground — `agent-device open <bundle_id>` |
| `agent-device back` fails in explore | `agent-device home` then `agent-device open <bundle_id>` |
| Session dies | `agent-device open <bundle_id>` to restart |

When done: `agent-device close`
