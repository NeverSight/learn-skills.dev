---
name: wds-docs
description: Wix Design System component reference. Use when building UI with @wix/design-system, choosing components, or checking props and examples. Triggers on "what component", "how do I make", "WDS", "show me props", or component names like Button, Card, Modal, Box, Text.
---

# WDS Documentation Navigator

**Docs path:** `node_modules/@wix/design-system/dist/docs/`

## CRITICAL: Never Read Entire Files

Files are 200-900+ lines. Follow the staged discovery flow below.

---

## Stage 1: Find Component

**Goal:** Search for component by feature/keyword

```bash
Grep: "table" in components.md
Grep: "form\|input\|validation" in components.md
Grep: "modal\|dialog\|popup" in components.md
```

**Output:** Component name + description + do/don'ts

**Next:** Go to Stage 2 with component name

---

## Stage 2: Get Props + Example List

**Goal:** Get props AND discover available examples

```bash
# 2a. Get props (small files OK to read, large files grep)
Read: components/ButtonProps.md              # OK if <100 lines
Grep: "### disabled" in components/BoxProps.md -A 3  # Box is huge

# 2b. List available examples (ALWAYS grep, never read)
Grep: "^### " in components/ButtonExamples.md -n
```

**Output from 2b:**
```
5:### Size
17:### Skin
71:### Affix
123:### Disabled
183:### Loading state
```

**Next:** Pick example(s) from list, go to Stage 3

---

## Stage 3: Fetch Specific Example

**Goal:** Read only the example you need (~30-50 lines)

```bash
# Option A: Read with offset (line number from Stage 2)
Read: components/ButtonExamples.md offset=183 limit=40

# Option B: Grep with context
Grep: "### Loading state" in components/ButtonExamples.md -A 40
```

**Output:** JSX code example for that specific feature

---

## Stage 4: Icons (when needed)

```bash
Grep: "Add\|Edit\|Delete\|Search" in icons.md
```

---

## Flow Summary

```
┌─────────────────────────────────────────────────────────┐
│ Stage 1: Grep components.md for keyword                 │
│          → finds: Button, Card, Table...                │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Stage 2a: Read/Grep {Component}Props.md                 │
│           → gets: props with types & descriptions       │
│                                                         │
│ Stage 2b: Grep "^### " in {Component}Examples.md        │
│           → gets: example names + line numbers          │
│           "5:### Size, 71:### Affix, 183:### Loading"   │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Stage 3: Read offset=183 limit=40                       │
│          → gets: specific example JSX code              │
└────────────────────────────────────────────────────────┘
```

---

## Example Session: Product Page

```bash
# Stage 1: Find components
Grep: "image\|card\|price" in components.md
→ Image, Card, Text found

# Stage 2a: Get Card props
Read: components/CardProps.md

# Stage 2b: List Card examples
Grep: "^### " in components/CardExamples.md -n
→ 5:### Basic, 25:### With media, 60:### Clickable

# Stage 3: Fetch "With media" example
Read: components/CardExamples.md offset=25 limit=35
→ Gets Card with Image example code

# Repeat Stage 2-3 for other components as needed
```

**Result:** ~80 lines read instead of 1500+

---

## Quick Reference

| Stage | Command | Output |
|-------|---------|--------|
| 1. Find | `Grep: "keyword" in components.md` | Component name |
| 2a. Props | `Read: {Name}Props.md` | Props list |
| 2b. Examples | `Grep: "^### " in {Name}Examples.md` | Example names + lines |
| 3. Fetch | `Read: offset=N limit=40` | Example code |
| 4. Icons | `Grep: "IconName" in icons.md` | Icon exists |

---

## File Sizes

| File | Lines | Strategy |
|------|-------|----------|
| components.md | ~970 | Grep, never read fully |
| icons.md | ~400 | Grep for specific icon |
| Most Props.md | 30-100 | Read fully OK |
| BoxProps.md | 8000+ | Grep only! |
| Most Examples.md | 100-600 | Grep → offset read |
| PageExamples.md | 940 | Grep → offset read |

---

## Grep Patterns by Use Case

```bash
# Forms
Grep: "form\|input\|validation" in components.md

# Layout
Grep: "layout\|page\|card\|box" in components.md

# Data display
Grep: "table\|list\|badge" in components.md

# Feedback
Grep: "notification\|toast\|loader" in components.md
```

---

## Quick Component Mapping (Design → WDS)

| Design Element | WDS Component | Notes |
|----------------|---------------|-------|
| Rectangle/container | `<Box>` | Layout wrapper |
| Text button | `<TextButton>` | Secondary actions |
| Input with label | `<FormField>` + `<Input>` | Wrap inputs |
| Toggle | `<ToggleSwitch>` | On/off settings |
| Modal | `<Modal>` + `<CustomModalLayout>` | Use together |
| Grid | `<Layout>` + `<Cell>` | Responsive |

---

## Spacing (px → SP conversion)

When designer specifies pixels, convert to the nearest SP token:

| Token | Classic | Studio |
|-------|---------|--------|
| `SP1` | 6px | 4px |
| `SP2` | 12px | 8px |
| `SP3` | 18px | 12px |
| `SP4` | 24px | 16px |
| `SP5` | 30px | 20px |
| `SP6` | 36px | 24px |

```tsx
<Box gap="SP2" padding="SP3">
```

Only use SP tokens for `gap`, `padding`, `margin` - not for width/height.

---

## Imports

```tsx
import { Button, Card, Image } from '@wix/design-system';
import { Add, Edit, Delete } from '@wix/wix-ui-icons-common';
```
