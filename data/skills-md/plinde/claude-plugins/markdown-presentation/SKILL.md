---
name: markdown-presentation
description: This skill should be used when creating markdown-based presentations with expandable sections, timing guides, and speaker-friendly formatting. Use for team onboarding, technical deep-dives, and knowledge transfer sessions.
---

# Markdown Presentation Skill

Create professional, presenter-friendly markdown presentations with timing guidance, expandable details, and clean visual hierarchy.

## When to Use This Skill

- Creating team onboarding presentations
- Technical architecture overviews
- Knowledge transfer sessions
- Sprint demos or retrospectives
- Any presentation that will be viewed in markdown-capable viewers (GitHub, VS Code, Obsidian)

## Presentation Structure

### Standard Template

```markdown
# Presentation Title
## Subtitle or Context

**Duration:** X minutes
**Audience:** Target audience
**Date:** YYYY-MM-DD

---

## Agenda

1. Topic 1 (X min)
2. Topic 2 (X min)
3. Topic 3 (X min)
...

---

## 1. First Section

Content here...

---

## 2. Second Section

Content here...

---

## Questions?

### Contact
- Channel/email
- Resources

---

*Presentation created: YYYY-MM-DD*
*Built with [markdown-presentation@plinde/claude-plugins](https://github.com/plinde/claude-plugins/tree/main/markdown-presentation)*
```

## Key Formatting Patterns

### Horizontal Rules as Slide Breaks

Use `---` to create visual "slide" breaks between sections:

```markdown
## Section 1

Content...

---

## Section 2

Content...
```

### Expandable Details for Dense Content

Use HTML `<details>` tags for content that's too long for a single "slide":

```markdown
<details>
<summary><b>📋 Click to expand detailed info</b></summary>

Long content here...
- Bullet points
- Code blocks
- Tables

</details>
```

**Best Practices for Details:**
- Use emoji + bold for visual distinction: `<b>📋 Title</b>`
- Keep summary text short and descriptive
- Use for: command references, configuration examples, troubleshooting guides
- Don't use for: critical information that everyone must see

### Timing Annotations

Include timing in the agenda to help presenters pace themselves:

```markdown
## Agenda

1. Introduction (2 min)
2. Architecture Overview (5 min)
3. Demo (8 min)
4. Q&A (5 min)

**Total: 20 minutes**
```

### ASCII Diagrams (Markdown Only)

Use ASCII art for architecture diagrams in **pure markdown** contexts (GitHub, VS Code preview):

```markdown
```
┌─────────────┐     ┌─────────────┐
│   Source    │────▶│  Processor  │
└─────────────┘     └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Output    │
                    └─────────────┘
```
```

**ASCII Box Drawing Characters:**
- Corners: `┌ ┐ └ ┘`
- Lines: `─ │`
- Connectors: `├ ┤ ┬ ┴ ┼`
- Arrows: `▶ ▼ ◀ ▲ → ← ↑ ↓`

**Warning:** ASCII diagrams often have alignment issues in HTML output due to font rendering. For HTML presentations, use HTML tables/divs instead (see HTML Presentations section below).

### Tables for Comparisons

```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Speed   | Fast     | Slow     |
| Cost    | High     | Low      |
```

### Quick Reference Cards

End presentations with a quick reference section:

```markdown
## Quick Reference Card

### Key Commands
| Command | Purpose |
|---------|---------|
| `cmd1`  | Does X  |
| `cmd2`  | Does Y  |

### Important Links
- [Doc 1](url)
- [Doc 2](url)
```

## Presentation Length Guidelines

| Duration | Slides/Sections | Content Depth |
|----------|-----------------|---------------|
| 5 min    | 3-5             | Overview only |
| 15 min   | 6-10            | Key concepts + examples |
| 30 min   | 10-15           | Deep dive with demos |
| 60 min   | 15-25           | Comprehensive with exercises |

**Rule of thumb:** ~2 minutes per major section (excluding expandable details)

## Viewing Options

### VS Code
```bash
code presentation.md
# Use Ctrl+Shift+V (or Cmd+Shift+V) for preview
```

### GitHub
- Push to repo, view in browser
- Details sections render as expandable

### Obsidian
- Open in vault
- Use presentation plugins for slideshow mode

### Marp (CLI)
Convert to actual slides:
```bash
marp presentation.md -o presentation.pdf
marp presentation.md -o presentation.html
```

## HTML Presentations

For presentations that will be viewed primarily in browsers, consider using HTML instead of pure markdown. HTML provides better control over styling and diagram alignment.

### When to Use HTML vs Markdown

| Use Case | Format | Reason |
|----------|--------|--------|
| GitHub/GitLab viewing | Markdown | Native rendering |
| Browser presentations | HTML | Full CSS control |
| Complex diagrams | HTML | Precise alignment |
| Print/PDF export | Either | Marp for MD, browser for HTML |
| Slideshow mode | Markdown + Marp | Better tooling |

### Dark Theme CSS Template

Use CSS variables for consistent theming (Tokyo Night-inspired palette):

```css
:root {
    --bg-primary: #1a1b26;
    --bg-secondary: #24283b;
    --bg-tertiary: #1f2335;
    --text-primary: #c0caf5;
    --text-secondary: #a9b1d6;
    --text-muted: #565f89;
    --accent-blue: #7aa2f7;
    --accent-teal: #73daca;
    --accent-purple: #bb9af7;
    --accent-amber: #e0af68;
    --accent-green: #9ece6a;
    --accent-coral: #f7768e;
    --border-color: #3b4261;
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

pre, code {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-color);
}

h1, h2, h3 { color: var(--accent-blue); }
a { color: var(--accent-teal); }
```

### HTML Diagrams (Replace ASCII)

**Problem:** ASCII art alignment breaks in HTML due to font rendering differences.

**Solution:** Use HTML divs with flexbox or tables with defined widths.

#### Architecture Box Pattern

```html
<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
    <div style="border: 2px solid var(--accent-teal); border-radius: 8px;
                padding: 15px; min-width: 200px; background: rgba(115,218,202,0.1);">
        <strong style="color: var(--accent-teal);">Component A</strong>
        <ul><li>Feature 1</li><li>Feature 2</li></ul>
    </div>
    <div style="border: 2px solid var(--accent-purple); border-radius: 8px;
                padding: 15px; min-width: 200px; background: rgba(187,154,247,0.1);">
        <strong style="color: var(--accent-purple);">Component B</strong>
        <ul><li>Feature 1</li><li>Feature 2</li></ul>
    </div>
</div>
```

#### Flow Diagram Pattern (Flexbox)

```html
<div style="display: flex; align-items: center; justify-content: center;
            gap: 10px; flex-wrap: wrap; padding: 20px;">
    <div style="background: var(--accent-blue); color: var(--bg-primary);
                padding: 10px 20px; border-radius: 8px;">
        <strong>Step 1</strong>
    </div>
    <span style="color: var(--accent-teal); font-size: 1.5em;">→</span>
    <div style="background: var(--accent-purple); color: var(--bg-primary);
                padding: 10px 20px; border-radius: 8px;">
        <strong>Step 2</strong>
    </div>
    <span style="color: var(--accent-teal); font-size: 1.5em;">→</span>
    <div style="background: var(--accent-green); color: var(--bg-primary);
                padding: 10px 20px; border-radius: 8px;">
        <strong>Step 3</strong>
    </div>
</div>
```

#### Comparison Table Pattern

```html
<table style="width: 100%; border-collapse: collapse;">
    <thead>
        <tr style="background: var(--bg-secondary);">
            <th style="padding: 12px; border: 1px solid var(--border-color);">Feature</th>
            <th style="padding: 12px; border: 1px solid var(--border-color);">Option A</th>
            <th style="padding: 12px; border: 1px solid var(--border-color);">Option B</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid var(--border-color);">Speed</td>
            <td style="padding: 12px; border: 1px solid var(--border-color);
                       color: var(--accent-green);">Fast</td>
            <td style="padding: 12px; border: 1px solid var(--border-color);
                       color: var(--accent-coral);">Slow</td>
        </tr>
    </tbody>
</table>
```

### Color-Coded Components

Use consistent colors for related components throughout the presentation:

```css
/* Example: Multi-environment architecture */
--env-production: #73daca;    /* teal - production */
--env-staging: #bb9af7;       /* purple - staging */
--env-development: #e0af68;   /* amber - development */
```

Apply with semi-transparent backgrounds for visual grouping:
```html
<div style="border: 2px solid var(--env-production);
            background: rgba(115,218,202,0.1);
            border-radius: 8px; padding: 15px;">
    Production Environment Content
</div>
```

## Example: Technical Onboarding

```markdown
# Service X Onboarding
## For New Team Members

**Duration:** 15 minutes
**Audience:** New engineers

---

## Agenda

1. What is Service X? (2 min)
2. Architecture (5 min)
3. Local Development (5 min)
4. Resources (3 min)

---

## 1. What is Service X?

Service X handles authentication for all internal tools.

**Key Facts:**
- Processes 10M requests/day
- 99.99% uptime SLA
- Deployed in 3 regions

---

## 2. Architecture

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│ Service X│────▶│   IdP    │
└──────────┘     └──────────┘     └──────────┘
```

<details>
<summary><b>📋 Component Details</b></summary>

**Service X Components:**
- API Gateway (Kong)
- Auth Service (Go)
- Token Store (Redis)
- Audit Logger (Kafka → ES)

</details>

---

## 3. Local Development

```bash
# Clone and setup
git clone git@github.com:org/service-x.git
cd service-x
make setup

# Run locally
make run

# Run tests
make test
```

<details>
<summary><b>📋 Troubleshooting</b></summary>

**Port conflicts:**
```bash
lsof -i :8080
kill -9 <PID>
```

**Database issues:**
```bash
make db-reset
```

</details>

---

## 4. Resources

| Resource | Link |
|----------|------|
| Docs | [Wiki](url) |
| Runbooks | [Notion](url) |
| Slack | #service-x |

---

## Questions?

**Contact:** #service-x-support

*Created: 2025-12-22*
*Built with [markdown-presentation@plinde/claude-plugins](https://github.com/plinde/claude-plugins/tree/main/markdown-presentation)*
```

## Self-Test

```bash
# Verify skill exists
ls -la ~/.claude/plugins/marketplaces/plinde-plugins/markdown-presentation/skills/markdown-presentation/SKILL.md

# Or if installed locally
ls -la ~/.claude/skills/markdown-presentation/SKILL.md
```

## Related Tools

- [Marp](https://marp.app/) - Convert markdown to presentation slides
- [Pandoc](https://pandoc.org/) - Universal document converter (md → docx, pdf, html)
