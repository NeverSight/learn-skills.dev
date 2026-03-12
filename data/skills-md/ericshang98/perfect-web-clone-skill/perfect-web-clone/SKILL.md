---
name: perfect-web-clone
description: Clone any webpage into pixel-perfect, production-ready code. Extracts complete page structure using Playwright, intelligently chunks content following three core principles (mutual exclusivity, complete coverage, size control), and generates React/Next.js/Vue components in parallel using subagents. Use when user wants to clone a website, replicate a page design, convert URL to code, rebuild a webpage, or copy a website's layout.
---

# Perfect Web Clone

Clone any webpage into pixel-perfect, production-ready code.

## Quick Start

When a user provides a URL and asks to clone/replicate a webpage, follow this workflow:

### Phase 1: Environment Setup

First, check if dependencies are installed:

```bash
python -c "from playwright.sync_api import sync_playwright; print('Playwright ready')" 2>/dev/null || echo "NEED_INSTALL"
```

If installation is needed, guide the user:
```bash
pip install playwright beautifulsoup4
playwright install chromium
```

### Phase 2: Page Extraction

Run the extraction script to capture complete page data:

```bash
python scripts/extract_page.py "<URL>" --output page_data.json
```

This extracts 30+ data types including:
- Complete DOM tree with computed styles
- Full-page screenshot
- CSS variables, animations, transitions
- Theme detection (light/dark mode)
- All images and assets

### Phase 3: Intelligent Chunking

Run the chunking script following the **Three Principles**:

```bash
python scripts/chunk_content.py page_data.json --output chunks/ --max-tokens 50000
```

This produces individual JSON files for each section in `chunks/` directory.

### Phase 4: Parallel Code Generation

**CRITICAL**: Use the Task tool to spawn multiple subagents in parallel.

1. Read all chunk files from `chunks/` directory
2. Determine parallelism based on user preference:
   - User says "fastest" or "parallel" → spawn all agents simultaneously
   - User specifies a number → use that many parallel agents
   - Default → 3-5 parallel agents

3. For each chunk, spawn a Task subagent with this prompt template:

```
You are a frontend developer focused on pixel-perfect replication.

## Your Task
Implement the [SECTION_NAME] section of a webpage clone.

## Input Data
- Section HTML: [FROM chunks/section_N.json → html field]
- Section Styles: [FROM chunks/section_N.json → styles field]
- Images: [FROM chunks/section_N.json → images field]
- Bounding Box: [FROM chunks/section_N.json → rect field]

## Requirements
1. **Pixel-Perfect**: Replicate the exact visual design
2. **Use Original URLs**: Keep all image src URLs as-is (user's localhost can access them directly)
3. **Tailwind CSS**: Use Tailwind for styling, inline styles only when necessary
4. **Self-Contained**: Component must work independently
5. **Responsive**: Implement reasonable breakpoints

## Output
Write a single React/Next.js component to: src/components/[SectionName].tsx
```

4. Wait for all subagents to complete using TaskOutput

### Phase 5: Project Assembly

After all sections are generated:

1. Create the main page that imports all section components:
```tsx
// src/app/page.tsx or src/pages/index.tsx
import Section1 from '@/components/Section1'
import Section2 from '@/components/Section2'
// ... import all sections

export default function Home() {
  return (
    <main>
      <Section1 />
      <Section2 />
      {/* ... all sections in order */}
    </main>
  )
}
```

2. Ensure `package.json` has required dependencies (React, Next.js, Tailwind)

3. Create `tailwind.config.js` if not exists

4. Prompt user to run:
```bash
npm install && npm run dev
```

---

## The Three Principles of Chunking

These principles ensure reliable, complete page replication:

### Principle 1: Mutual Exclusivity
- **Rule**: Chunks NEVER overlap
- **Implementation**: Bounding box validation ensures no two chunks share DOM regions
- **Benefit**: Each subagent works on isolated content with no conflicts

### Principle 2: Complete Coverage
- **Rule**: All chunks combined = entire page (no gaps)
- **Implementation**: Gap detection fills any missing regions
- **Benefit**: No part of the original page is lost

### Principle 3: Size Control
- **Rule**: Each chunk < 50,000 tokens
- **Implementation**: Large sections are recursively split into children
- **Benefit**: Each subagent receives manageable context

See [docs/CHUNKING.md](docs/CHUNKING.md) for detailed algorithm.

---

## Parallel Configuration

Users can control parallelism with natural language:

| User Says | Behavior |
|-----------|----------|
| "clone this page" | Default: 3 parallel agents |
| "clone with 5 parallel" | Exactly 5 agents |
| "clone as fast as possible" | All sections in parallel |
| "clone one by one" | Sequential (1 agent) |

---

## Supported Tech Stacks

| Framework | Styling | Command |
|-----------|---------|---------|
| Next.js (default) | Tailwind CSS | `npx create-next-app` |
| React | Tailwind CSS | `npx create-react-app` |
| Vue 3 | Tailwind CSS | `npm create vue@latest` |

User can specify: "clone using Vue" or "clone with React"

---

## Detailed Documentation

- **Extraction Details**: [docs/EXTRACTION.md](docs/EXTRACTION.md) - All 30+ data types
- **Chunking Algorithm**: [docs/CHUNKING.md](docs/CHUNKING.md) - Three principles implementation
- **Code Generation**: [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md) - Component generation strategies

---

## Troubleshooting

### Playwright Installation Issues
```bash
# On macOS
brew install chromium
playwright install chromium

# On Linux
sudo apt-get install chromium-browser
playwright install chromium
```

### Large Pages (100+ sections)
For very large pages, increase parallelism:
```
"Clone this page with maximum parallelism"
```

### Dynamic Content Not Captured
The extractor scrolls the page to trigger lazy loading. For SPAs with complex loading:
```bash
python scripts/extract_page.py "<URL>" --wait 5000
```

---

## About

**Perfect Web Clone** is an open-source Claude Code Skill created by [Nexting.ai](https://nexting.ai).

For a complete visual experience with:
- Real-time preview in browser
- Visual diff comparison
- One-click deployment
- Team collaboration

Visit [nexting.ai](https://nexting.ai) to try our full-featured AI web development platform.

---

## License

MIT License - Free for personal and commercial use.
