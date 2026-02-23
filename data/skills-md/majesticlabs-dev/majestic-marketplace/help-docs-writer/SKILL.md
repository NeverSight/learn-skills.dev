---
name: help-docs-writer
description: Create customer-facing help documentation for product features. Analyzes codebase to extract feature details, transforms into user-friendly walkthroughs with troubleshooting sections.
triggers:
  - help docs
  - help article
  - help section
  - customer documentation
  - support article
  - knowledge base
  - how-to guide
allowed-tools: Read Write Edit Grep Glob AskUserQuestion
disable-model-invocation: true
---

# Help Documentation Writer

Create customer-facing help articles for product features. Bridges technical implementation with user-friendly documentation.

## Inputs

Use `AskUserQuestion` to gather:

| Input | Required | Description |
|-------|----------|-------------|
| **Feature name** | Yes | What feature to document |
| **Target audience** | Yes | Technical level (beginner/intermediate/advanced) |
| **Output format** | No | `markdown` (default) or `html` |
| **Help center platform** | No | Zendesk, Intercom, Notion, GitBook, custom |

## Process

### 1. Feature Discovery

Search codebase for feature implementation:

```bash
# Find feature files
rg -l "feature_name" --type-add 'code:*.{rb,js,ts,py,jsx,tsx}'

# Find UI components
rg -l "FeatureName" src/ app/

# Find routes/endpoints
rg "feature" config/routes.rb app/controllers/
```

Extract:
- What the feature does (core functionality)
- User-facing entry points (buttons, menus, URLs)
- Configuration options
- Error states and edge cases

### 2. Structure the Article

Standard help article structure:

```
1. Title (action-oriented)
2. Overview (what + why, 2-3 sentences)
3. Prerequisites (if any)
4. Step-by-step instructions
5. Tips/best practices (optional)
6. Troubleshooting (common issues)
7. Related articles (links)
```

### 3. Write for Customers

- Second person ("you"), present tense, active voice, no jargon
- Numbered steps: one action per step, start with verb, include expected result after each action

## Article Templates

### Feature Walkthrough

```markdown
# How to [Action] with [Feature]

[One sentence: what this helps you do]

## Before you start

- [Prerequisite 1]
- [Prerequisite 2]

## Steps

1. **[Action verb] [object]**

   [Where to find it / what to click]

   ![Screenshot placeholder: description]

2. **[Next action]**

   [Details]

3. **[Final action]**

   You'll see [confirmation message/result].

## Tips

- [Tip 1]
- [Tip 2]

## Troubleshooting

### [Problem statement as question]

[Solution in 1-2 sentences]

### [Another common issue]

[Solution]

## Related articles

- [Link to related feature]
- [Link to related feature]
```

### Quick Reference

For simple features:

```markdown
# [Feature Name]

[What it does in one sentence]

**To use [feature]:**

1. Go to **[Location]**
2. Click **[Button/Link]**
3. [Complete the action]

**Note:** [Important caveat if any]
```

### Settings/Configuration Guide

```markdown
# [Feature] settings

Customize how [feature] works for your account.

## Available settings

| Setting | Description | Default |
|---------|-------------|---------|
| [Name] | [What it controls] | [Value] |
| [Name] | [What it controls] | [Value] |

## How to change settings

1. Go to **Settings > [Section]**
2. Find **[Setting name]**
3. [Instructions to modify]
4. Click **Save**

Changes take effect [immediately/after X].
```

## Writing Guidelines

### Step Instructions

| Do | Don't |
|----|-------|
| Click **Save** | Click on the Save button |
| Select your timezone | Choose the timezone you want |
| Enter your email | Type in your email address |

### UI Element Formatting

- **Bold** for clickable elements: buttons, links, menu items
- `Code` for user input, URLs, or technical values
- *Italics* for emphasis (sparingly)
- "Quotes" for exact text the user should see

### Screenshot Placeholders

Include placeholders for visual guidance:

```markdown
![Screenshot: Settings page with Save button highlighted]
```

Format: `![Screenshot: [description of what to capture and highlight]]`

### Callouts

Use for important information:

```markdown
> **Note:** [Important information]

> **Warning:** [Potential issue or destructive action]

> **Tip:** [Helpful suggestion]
```

## Output Formats

### Markdown (default)

Standard markdown with:
- ATX headings (`#`, `##`, `###`)
- Fenced code blocks
- Tables
- Blockquotes for callouts

### HTML

Semantic HTML with:
- `<article>` wrapper
- `<h1>` through `<h3>` headings
- `<ol>` for numbered steps
- `<table>` for data
- `<aside>` for callouts with `class="note|warning|tip"`
- Inline styles stripped (CSS classes only)

**HTML Template:**

```html
<article class="help-article">
  <h1>[Title]</h1>

  <p class="intro">[Overview]</p>

  <section class="prerequisites">
    <h2>Before you start</h2>
    <ul>
      <li>[Prerequisite]</li>
    </ul>
  </section>

  <section class="steps">
    <h2>Steps</h2>
    <ol>
      <li>
        <strong>[Action]</strong>
        <p>[Details]</p>
      </li>
    </ol>
  </section>

  <section class="troubleshooting">
    <h2>Troubleshooting</h2>
    <details>
      <summary>[Problem as question]</summary>
      <p>[Solution]</p>
    </details>
  </section>

  <aside class="note">
    <p>[Important note]</p>
  </aside>
</article>
```

## Quality Checklist

Before delivery, verify:

- [ ] Title starts with action verb or "How to"
- [ ] Overview explains what AND why (benefit)
- [ ] Prerequisites listed if any
- [ ] Each step = one action
- [ ] Steps start with verbs
- [ ] UI elements in **bold**
- [ ] No jargon or undefined acronyms
- [ ] Troubleshooting covers common issues
- [ ] Screenshot placeholders included
- [ ] Related articles linked

## Platform-Specific Notes

### Zendesk

- Use `{{snippet}}` for reusable content
- Add article labels in metadata
- Include search keywords

### Intercom

- Keep articles under 1000 words
- Use their callout syntax: `> 📌 Note:`
- Add reaction prompts at end

### Notion

- Use toggle blocks for troubleshooting
- Add table of contents
- Use callout blocks with icons

### GitBook

- Use hints syntax: `{% hint style="info" %}`
- Add page descriptions
- Use tabs for multi-platform instructions


## What This Skill Does NOT Do

- Generate screenshots (provides placeholders only)
- Translate to other languages
- Create video tutorials
- Write API documentation (use `docs-architect` for technical docs)
