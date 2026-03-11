---
name: slides-generator
description: Generate interactive presentation slides using React + Tailwind. Triggers on keywords like "slides", "presentation", "PPT", "demo", "benchmark".
---

# Slides Generator

Generate professional presentation slides through parallel subagent execution.

## Workflow Overview

```
Step 1: Collect Requirements
    ↓
Step 2: Confirm Outline
    ↓
Step 3: Create Project Skeleton
    ↓
Step 4: Dispatch Parallel Subagents (one per slide)
    ↓
Step 5: Finalize and Launch
```

## Step 1: Collect Requirements

Ask questions to understand:
- **Scenario type**: Benchmark / Product Demo / Report / General
- **Content**: Title, number of slides, key points per slide
- **Style preference**: Tech / Professional / Vibrant / Minimal

Recommend a theme from [palettes.md](references/palettes.md) based on style keywords.

## Step 2: Confirm Outline

Present the outline for user confirmation:

```markdown
## Presentation Outline

**Title**: Model Engineering Capability Benchmark
**Theme**: dark-sapphire-blue (glass style)
**Output**: ./model-benchmark (reply with path to change)

**Slides**:
1. Hero - Title and overview
2. Framework - Evaluation dimensions
3. Task 1 - Backend development
4. Task 2 - Frontend component
5. Summary - Conclusions

**Confirm to generate?**
```

User responses:
- "OK" / "Confirm" → Use default path `./project-name`
- Custom path (e.g., `~/demos`) → Use `user-path/project-name`

## Step 3: Create Project Skeleton

Copy template and configure:

```bash
# 1. Copy template
cp -r <skill-path>/assets/template <output-dir>
cd <output-dir>

# 2. Update tailwind.config.js with theme colors
# 3. Update index.html title
# 4. Create empty src/slides/ directory
```

## Step 4: Dispatch Parallel Subagents

For each slide, dispatch a subagent with:

**Fixed context (same for all):**
- **Aesthetic philosophy** (from [aesthetics.md](references/aesthetics.md)) - PRIMARY design reference
- Tech stack: React + Tailwind CSS + lucide-react + framer-motion
- Theme color variables (from tailwind.config.js)
- Style keyword (glass / flat)
- Technical principles (from [principles.md](references/principles.md))
- First slide code (for reference, after slide 01 is generated)

**Dynamic context (per subagent):**
- Slide number: 01, 02, 03...
- Filename: `01-hero.jsx`, `02-framework.jsx`...
- Slide type: Hero / Content / Data / Summary
- Content points: Title, key information to display

**Subagent prompt template:**

```
You are generating slide ${number} for a presentation.

## Design Philosophy (IMPORTANT - Read First)
${aestheticsContent}

## Technical Requirements
- Framework: React function component
- Styling: Tailwind CSS
- Icons: lucide-react
- Animations: framer-motion (for entrance animations, hover effects)
- Export: default function component

## Theme Colors (use these variables, not hardcoded colors)
- primary-50 to primary-950
- accent-50 to accent-950
- bg-base, bg-card, bg-elevated
- text-primary, text-secondary, text-muted
- border-default, border-subtle

## Style: ${style}
${style === 'glass' ?
  'Use glassmorphism: glass class or bg-white/10 backdrop-blur-md border-white/20' :
  'Use flat design: bg-bg-card shadow-sm border-border-default'}

## Layout Safety Rules (CRITICAL - Prevents Overflow)

### ⛔ FORBIDDEN - These WILL break the layout:
- ❌ `h-screen` - NEVER use, it ignores parent constraints
- ❌ `h-full` on inner content wrappers - steals padding space
- ❌ Adding `p-*`, `px-*`, `py-*`, `pb-*` to slide-page - conflicts with built-in padding
- ❌ Nesting divs with `h-full flex ... justify-center` inside slide-page
- ❌ `min-h-screen` or any viewport-based heights

### ✅ REQUIRED Structure:
\`\`\`jsx
<div className="slide-page">
  {/* Background decorations - use absolute positioning */}
  <div className="absolute inset-0 pointer-events-none">...</div>

  {/* Header - fixed height, use mb-* for spacing */}
  <header className="relative z-10 mb-6 shrink-0">
    <h1>Title</h1>
  </header>

  {/* Content - use slide-content, it auto-fills remaining space */}
  <div className="slide-content relative z-10">
    {/* Grid/cards here - NO h-full on this div */}
  </div>
</div>
\`\`\`

### Why slide-page works:
- Has `padding: 2.5rem` on all sides (top included!)
- Has `padding-bottom: ~6.5rem` for navigation
- Is `display: flex; flex-direction: column`
- Children auto-size within the padded area

### Content Density Limits (1080p baseline)
- Max 4 cards per slide
- Max 3 info items per card
- Use `line-clamp-2` for long text
- Use `truncate` for single-line overflow

### Grid Layouts
- 2 cards: `grid-auto-fit grid-cols-2`
- 4 cards (2x2): `grid-auto-fit grid-2x2`
- 3 cards: `grid-auto-fit grid-1x3`
- 6 cards (2x3): `grid-auto-fit grid-2x3`

### Card Pattern
\`\`\`jsx
<div className="card-fit glass rounded-xl p-4">
  <header>Title</header>
  <div className="card-body">Content</div>
</div>
\`\`\`

## Animation Patterns (use framer-motion)
- Use motion.div for animated elements
- Stagger children with staggerChildren: 0.1
- Entrance: { opacity: 0, y: 20 } -> { opacity: 1, y: 0 }
- Hover cards: whileHover={{ scale: 1.02 }}
- Import: import { motion } from 'framer-motion'

## Slide Content
Type: ${slideType}
Title: ${title}
Key Points:
${keyPoints}

## Output
Write a complete JSX file to: src/slides/${filename}
Include all necessary imports.
Export default function component.

${firstSlideCode ? `
## Reference (match this style)
\`\`\`jsx
${firstSlideCode}
\`\`\`
` : ''}
```

**Execution:**
```javascript
// Dispatch all subagents in parallel
const subagentPromises = slides.map((slide, index) =>
  dispatchSubagent({
    number: String(index + 1).padStart(2, '0'),
    filename: `${String(index + 1).padStart(2, '0')}-${slide.id}.jsx`,
    slideType: slide.type,
    title: slide.title,
    keyPoints: slide.points,
    style: themeStyle,
    firstSlideCode: index > 0 ? firstSlideCode : null
  })
);

await Promise.all(subagentPromises);
```

## Step 5: Finalize and Launch

After all subagents complete:

```bash
# 1. Update App.jsx with slide imports
# Generate import statements and SLIDES/NAV_ITEMS arrays

# 2. Install and start
npm install && npm run dev
```

**App.jsx update pattern:**

```jsx
// Add imports at top
import Slide01 from './slides/01-hero';
import Slide02 from './slides/02-framework';
// ...

// Update SLIDES array
const SLIDES = [Slide01, Slide02, ...];

// Update NAV_ITEMS array
const NAV_ITEMS = [
  { slideIndex: 0, label: 'Hero' },
  { slideIndex: 1, label: 'Framework' },
  // ...
];
```

## Step 6: Browser Verification (Optional)

If chrome-devtools MCP is available:

```bash
# Check if installed
claude mcp list | grep -q "chrome-devtools"

# If not, install
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

Use chrome-devtools to:
1. Navigate to http://localhost:5173
2. Take screenshots of each slide
3. Verify navigation works
4. Fix any issues found

## Theme System

Themes are defined in [palettes.md](references/palettes.md).

Each theme has:
- **ID**: Unique identifier
- **Tags**: Keywords for matching user preferences
- **Style**: `glass` or `flat` (can be overridden by user)
- **Colors**: 5 base colors that expand to full palette

**Quick recommendations:**

| User says | Recommend |
|-----------|-----------|
| "Tech", "Modern" | dark-sapphire-blue (glass) |
| "Professional", "Business" | banking-website (flat) |
| "Cyberpunk", "Neon" | cyberpunk (glass) |
| "Natural", "Organic" | summer-meadow (flat) |
| "Minimal", "Clean" | black-and-white (flat) |

## Design Principles

See [principles.md](references/principles.md) for:
- Color variable usage
- Typography scale
- Spacing conventions
- Component structure

## Project Structure

Generated project:

```
output-dir/
├── package.json
├── vite.config.js
├── tailwind.config.js      ← Theme colors
├── index.html              ← Title
├── src/
│   ├── main.jsx
│   ├── App.jsx             ← Slide imports & navigation
│   ├── index.css
│   └── slides/
│       ├── 01-hero.jsx     ← Generated by subagent
│       ├── 02-framework.jsx
│       └── ...
└── ...
```

## Example Interaction

```
User: "Create a benchmark presentation for Claude vs GPT"

Claude: "I'll help create benchmark slides. A few questions:

1. How many evaluation tasks? (e.g., 3-5)
2. What capabilities are you testing? (coding / reasoning / agent)
3. Style preference? (Tech/Professional/Vibrant)"

User: "3 tasks, coding ability, tech style"

Claude: "Recommended theme: dark-sapphire-blue (glass style)

## Outline

**Title**: Claude vs GPT Coding Benchmark
**Theme**: dark-sapphire-blue
**Output**: ./claude-benchmark

**Slides**:
1. Hero - Title and model overview
2. Framework - Evaluation methodology
3. Task 1 - API development
4. Task 2 - React components
5. Task 3 - CLI tools
6. Summary - Results and recommendations

Confirm to generate?"

User: "OK"

Claude: [Creates project skeleton]
Claude: [Dispatches 6 parallel subagents]
Claude: [Updates App.jsx with imports]
Claude: [Runs npm install && npm run dev]
Claude: "Presentation ready at http://localhost:5173"
```
