---
name: editor-themes
description: Create cohesive color themes for code editors, terminals, and IDEs. Generates semantic token systems from a brand color with reusable palette variables for rapid iteration.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Editor Themes

Generate complete color systems for code editors, terminals, and IDEs from a single brand color. This skill emphasizes **semantic token architecture** - creating a reusable variable layer that makes theme iteration fast and codebase changes minimal.

## When to Use

- "Create a VSCode theme from my brand color"
- "I need a terminal color scheme"
- "Generate editor colors for my design system"
- "Build a theme with semantic tokens"
- "I want to quickly iterate on theme colors"

## Installation

```bash
npx @basiclines/rampa
```

---

## Core Architecture: The Two-Layer System

The key to maintainable themes is separating **palette generation** from **semantic assignment**:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Palette Variables (Rampa output)                  │
│  --accent-0, --accent-1, ... --accent-9                     │
│  --neutral-0, --neutral-1, ... --neutral-9                  │
│  --syntax-0, --syntax-1, ... (triadic colors)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: Semantic Tokens (Your mapping)                    │
│  --editor-bg: var(--neutral-9)                              │
│  --editor-fg: var(--neutral-1)                              │
│  --keyword: var(--accent-4)                                 │
│  --string: var(--syntax-1-5)                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: Theme Consumer (VSCode, terminal, etc.)           │
│  "editor.background": "var(--editor-bg)"                    │
└─────────────────────────────────────────────────────────────┘
```

**Why this matters:** Change `--accent-*` colors once, and all semantic tokens update. Swap palettes without touching theme code.

---

## Recipe: Complete Editor Theme

### Step 1: Generate the Palette Foundation

A complete editor theme needs:
- **Accent ramp** - UI highlights, selections, buttons
- **Neutral ramp** - Backgrounds, text, borders
- **Syntax ramps** - 3-4 distinct hues for syntax highlighting

```bash
# Primary accent (your brand color)
rampa -C "<brand-color>" -L 95:15 --size=10 -O css --name=accent

# Neutrals (slightly tinted from brand)
rampa -C "<brand-color>" -L 98:8 -S 3:8 --size=10 -O css --name=neutral

# Syntax colors via triadic harmony (3 distinct hues)
rampa -C "<brand-color>" --add=triadic -L 85:35 -S 80:60 --size=7 -O css --name=syntax
```

### Step 2: Define Semantic Tokens

Map palette slots to meaningful roles. This is the abstraction layer that makes themes portable:

```css
:root {
  /* ═══════════════════════════════════════════════════════════
     EDITOR CHROME (UI elements)
     ═══════════════════════════════════════════════════════════ */
  --editor-bg:              var(--neutral-9);
  --editor-bg-elevated:     var(--neutral-8);
  --editor-fg:              var(--neutral-1);
  --editor-fg-muted:        var(--neutral-4);
  
  --sidebar-bg:             var(--neutral-9);
  --sidebar-fg:             var(--neutral-2);
  --sidebar-border:         var(--neutral-7);
  
  --panel-bg:               var(--neutral-8);
  --panel-border:           var(--neutral-7);
  
  /* ═══════════════════════════════════════════════════════════
     INTERACTIVE ELEMENTS
     ═══════════════════════════════════════════════════════════ */
  --focus-ring:             var(--accent-5);
  --selection-bg:           var(--accent-7);
  --selection-fg:           var(--neutral-1);
  
  --button-bg:              var(--accent-5);
  --button-fg:              var(--neutral-0);
  --button-hover:           var(--accent-4);
  
  --link:                   var(--accent-4);
  --link-hover:             var(--accent-3);
  
  /* ═══════════════════════════════════════════════════════════
     CODE EDITOR
     ═══════════════════════════════════════════════════════════ */
  --line-number:            var(--neutral-6);
  --line-number-active:     var(--neutral-3);
  --line-highlight:         var(--neutral-8);
  --cursor:                 var(--accent-4);
  
  --indent-guide:           var(--neutral-7);
  --whitespace:             var(--neutral-7);
  
  /* ═══════════════════════════════════════════════════════════
     SYNTAX HIGHLIGHTING
     ═══════════════════════════════════════════════════════════ */
  --syntax-keyword:         var(--accent-4);
  --syntax-function:        var(--syntax-triadic-1-3);
  --syntax-string:          var(--syntax-triadic-2-3);
  --syntax-number:          var(--syntax-triadic-2-4);
  --syntax-comment:         var(--neutral-5);
  --syntax-variable:        var(--neutral-2);
  --syntax-type:            var(--syntax-triadic-1-4);
  --syntax-constant:        var(--accent-3);
  --syntax-operator:        var(--neutral-3);
  --syntax-punctuation:     var(--neutral-4);
  --syntax-tag:             var(--accent-4);
  --syntax-attribute:       var(--syntax-triadic-1-3);
  --syntax-property:        var(--syntax-triadic-2-3);
  
  /* ═══════════════════════════════════════════════════════════
     DIFF & GIT
     ═══════════════════════════════════════════════════════════ */
  --diff-added-bg:          oklch(35% 0.15 145);
  --diff-added-fg:          oklch(80% 0.15 145);
  --diff-removed-bg:        oklch(30% 0.12 25);
  --diff-removed-fg:        oklch(75% 0.15 25);
  --diff-modified-bg:       oklch(32% 0.10 250);
  --diff-modified-fg:       oklch(78% 0.12 250);
  
  /* ═══════════════════════════════════════════════════════════
     DIAGNOSTICS
     ═══════════════════════════════════════════════════════════ */
  --error:                  oklch(65% 0.25 25);
  --warning:                oklch(75% 0.18 85);
  --info:                   var(--accent-4);
  --success:                oklch(70% 0.18 145);
}
```

### Step 3: Light Theme Variant

Same palette, different semantic mapping. This is why the two-layer system shines:

```css
:root[data-theme="light"] {
  /* Invert neutral mapping */
  --editor-bg:              var(--neutral-0);
  --editor-bg-elevated:     var(--neutral-1);
  --editor-fg:              var(--neutral-9);
  --editor-fg-muted:        var(--neutral-6);
  
  --sidebar-bg:             var(--neutral-1);
  --sidebar-fg:             var(--neutral-8);
  --sidebar-border:         var(--neutral-3);
  
  /* Adjust accent usage for light backgrounds */
  --selection-bg:           var(--accent-2);
  --button-bg:              var(--accent-6);
  --link:                   var(--accent-6);
  
  /* Syntax needs more saturation on light */
  --syntax-keyword:         var(--accent-6);
  --syntax-comment:         var(--neutral-5);
}
```

---

## VSCode Theme Example

Transform semantic tokens into VSCode's `package.json` theme format:

```json
{
  "name": "My Rampa Theme",
  "type": "dark",
  "colors": {
    "editor.background": "#1a1a1f",
    "editor.foreground": "#e5e5e5",
    "editor.selectionBackground": "#3b82f640",
    "editor.lineHighlightBackground": "#25252a",
    "editorLineNumber.foreground": "#525260",
    "editorLineNumber.activeForeground": "#a0a0a8",
    "editorCursor.foreground": "#60a5fa",
    
    "sideBar.background": "#1a1a1f",
    "sideBar.foreground": "#c5c5c8",
    "sideBarSectionHeader.background": "#25252a",
    
    "activityBar.background": "#15151a",
    "activityBar.foreground": "#e5e5e5",
    
    "statusBar.background": "#15151a",
    "statusBar.foreground": "#a0a0a8",
    
    "tab.activeBackground": "#25252a",
    "tab.inactiveBackground": "#1a1a1f",
    "tab.activeForeground": "#e5e5e5",
    
    "focusBorder": "#3b82f6",
    "selection.background": "#3b82f680"
  },
  "tokenColors": [
    {
      "name": "Keywords",
      "scope": ["keyword", "storage.type", "storage.modifier"],
      "settings": { "foreground": "#60a5fa" }
    },
    {
      "name": "Functions",
      "scope": ["entity.name.function", "support.function"],
      "settings": { "foreground": "#c084fc" }
    },
    {
      "name": "Strings",
      "scope": ["string", "string.quoted"],
      "settings": { "foreground": "#4ade80" }
    },
    {
      "name": "Numbers",
      "scope": ["constant.numeric"],
      "settings": { "foreground": "#34d399" }
    },
    {
      "name": "Comments",
      "scope": ["comment", "punctuation.definition.comment"],
      "settings": { "foreground": "#6b7280", "fontStyle": "italic" }
    },
    {
      "name": "Variables",
      "scope": ["variable", "variable.other"],
      "settings": { "foreground": "#e5e5e5" }
    },
    {
      "name": "Types",
      "scope": ["entity.name.type", "support.type"],
      "settings": { "foreground": "#a78bfa" }
    },
    {
      "name": "Constants",
      "scope": ["constant", "constant.language"],
      "settings": { "foreground": "#93c5fd" }
    },
    {
      "name": "Operators",
      "scope": ["keyword.operator"],
      "settings": { "foreground": "#c5c5c8" }
    },
    {
      "name": "Punctuation",
      "scope": ["punctuation"],
      "settings": { "foreground": "#a0a0a8" }
    },
    {
      "name": "Tags (HTML/JSX)",
      "scope": ["entity.name.tag"],
      "settings": { "foreground": "#60a5fa" }
    },
    {
      "name": "Attributes",
      "scope": ["entity.other.attribute-name"],
      "settings": { "foreground": "#c084fc" }
    }
  ]
}
```

---

## Terminal Color Scheme

Terminals use a standard 16-color ANSI palette. Map from your Rampa ramps:

```bash
# Generate terminal-optimized colors
rampa -C "<brand-color>" --add=square -L 70:50 -S 85:75 --size=4 -O json
```

### Semantic Mapping for Terminals

```
ANSI Color    │ Semantic Role           │ Rampa Source
──────────────┼─────────────────────────┼─────────────────────────
0  Black      │ Background              │ neutral-9
1  Red        │ Errors, deletions       │ square-3 (warm)
2  Green      │ Success, additions      │ square-1 (green range)
3  Yellow     │ Warnings, modified      │ square-2 (yellow range)
4  Blue       │ Info, links             │ accent-5
5  Magenta    │ Special, numbers        │ triadic-1-5
6  Cyan       │ Constants, paths        │ triadic-2-4
7  White      │ Primary text            │ neutral-1
8  Bright Blk │ Comments, muted         │ neutral-6
9  Bright Red │ Errors (highlighted)    │ square-3 lighter
10 Bright Grn │ Success (highlighted)   │ square-1 lighter
11 Bright Yel │ Warnings (highlighted)  │ square-2 lighter
12 Bright Blu │ Info (highlighted)      │ accent-3
13 Bright Mag │ Special (highlighted)   │ triadic-1-3
14 Bright Cyn │ Constants (highlighted) │ triadic-2-2
15 Bright Wht │ Emphasized text         │ neutral-0
```

### iTerm2 / Alacritty Example

```yaml
# Alacritty colors.yml
colors:
  primary:
    background: '#1a1a1f'  # neutral-9
    foreground: '#e5e5e5'  # neutral-1
  
  normal:
    black:   '#1a1a1f'     # neutral-9
    red:     '#f87171'     # error
    green:   '#4ade80'     # success
    yellow:  '#fbbf24'     # warning
    blue:    '#60a5fa'     # accent-4
    magenta: '#c084fc'     # triadic-1
    cyan:    '#34d399'     # triadic-2
    white:   '#e5e5e5'     # neutral-1
  
  bright:
    black:   '#6b7280'     # neutral-5
    red:     '#fca5a5'
    green:   '#86efac'
    yellow:  '#fcd34d'
    blue:    '#93c5fd'
    magenta: '#d8b4fe'
    cyan:    '#5eead4'
    white:   '#f5f5f5'     # neutral-0
```

---

## Best Practices

### 1. Start with Neutrals

Your neutral ramp does 70% of the visual work. Get it right first:

```bash
# Dark theme neutrals (rich black, not gray)
rampa -C "<brand-color>" -L 98:8 -S 3:8 --size=10 -O css --name=neutral
```

### 2. Use 7-Step Syntax Ramps

10 colors is overkill for syntax. 7 hits the sweet spot:

```bash
rampa -C "<brand-color>" --add=triadic -L 80:40 --size=7 -O css --name=syntax
```

### 3. Fixed Lightness for Syntax

Keep all syntax colors at similar lightness for visual balance:

```bash
# Syntax colors with narrow lightness range
rampa -C "<brand-color>" --add=triadic -L 70:55 -S 80:70 --size=5 -O css
```

### 4. Test with Real Code

Syntax highlighting looks different in practice. Test with:
- Comments next to code (should be clearly muted)
- Strings vs keywords (must be distinct)
- Nested brackets (color variation helps)

### 5. Iterate on Palette, Not Theme

When colors feel off, regenerate the palette layer:

```bash
# Too saturated? Reduce saturation range
rampa -C "#3b82f6" -L 95:15 -S 70:40 --size=10 -O css --name=accent

# Too bright? Narrow lightness ceiling
rampa -C "#3b82f6" -L 85:15 --size=10 -O css --name=accent
```

Then re-export. Semantic tokens stay unchanged.

---

## Complete Example: Blue Theme

```bash
# 1. Generate all palettes
rampa -C "#3b82f6" -L 95:15 --size=10 -O css --name=accent
rampa -C "#3b82f6" -L 98:8 -S 3:8 --size=10 -O css --name=neutral
rampa -C "#3b82f6" --add=triadic -L 80:40 -S 80:65 --size=7 -O css --name=syntax

# 2. Combine into single file
cat > theme-tokens.css << 'EOF'
:root {
  /* Paste accent output here */
  /* Paste neutral output here */
  /* Paste syntax output here */
  
  /* Then add semantic layer */
  --editor-bg: var(--neutral-9);
  --editor-fg: var(--neutral-1);
  /* ... rest of semantic tokens */
}
EOF
```

---

## Quick Reference

| Theme Element | Dark Mode Slot | Light Mode Slot |
|---------------|---------------|-----------------|
| Editor background | neutral-9 | neutral-0 |
| Editor foreground | neutral-1 | neutral-9 |
| Muted text | neutral-5 | neutral-5 |
| Selection | accent-7 @ 40% | accent-2 @ 40% |
| Focus ring | accent-5 | accent-6 |
| Syntax keyword | accent-4 | accent-6 |
| Syntax function | triadic-1-3 | triadic-1-5 |
| Syntax string | triadic-2-3 | triadic-2-5 |
| Comments | neutral-5 | neutral-5 |

---

## Tips

1. **Export to JSON first** (`-O json`) when building theme files programmatically
2. **Use `--add=square`** for status colors (error/warning/success/info) - guaranteed distinct
3. **Keep hue shift minimal** (`-H 0:0`) for professional-looking neutrals
4. **Test at different font sizes** - syntax colors may need adjustment for readability
5. **Version your palette** - store the rampa commands that generated it
