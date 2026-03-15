---
name: markdown-standards
description: Documentation and content creation standards for Markdown files. Use when creating or editing .md files, writing documentation, README files, or when the user asks about Markdown formatting, content structure, front matter, or documentation best practices.
metadata:
    author: devbyray
    version: '1.0'
    format: 'markdown, yaml'
---

# Markdown Standards

Apply these standards when creating or editing Markdown documentation.

## Content Rules

### 1. Headings

- Use appropriate heading levels (H2, H3, etc.) to structure content
- **Do NOT use H1** - it will be generated from the title/front matter
- Use headings hierarchically (don't skip levels)
- Recommend restructuring if H4+ headings are needed

**Good:**

```markdown
## Main Section

### Subsection

#### Detail (use sparingly)
```

**Bad:**

```markdown
# Title (don't use H1)

### Subsection (skipped H2)
```

### 2. Lists

- Use `-` for bullet points
- Use `1.` for numbered lists
- Indent nested lists with two spaces
- Ensure proper spacing between list items

**Example:**

```markdown
- First item
- Second item
    - Nested item
    - Another nested item
- Third item

1. First step
2. Second step
3. Third step
```

### 3. Code Blocks

- Use fenced code blocks with triple backticks
- Always specify the language for syntax highlighting
- Use inline code with single backticks for short snippets

**Example:**

````markdown
```javascript
const greeting = 'Hello, World!'
console.log(greeting)
```

Use `const` for immutable variables.
````

### 4. Links

- Use descriptive link text
- Ensure URLs are valid and accessible
- Prefer relative links for internal documentation

**Good:**

```markdown
See the [installation guide](./docs/installation.md) for details.
```

**Bad:**

```markdown
Click [here](./docs/installation.md).
```

### 5. Images

- Include descriptive alt text for accessibility
- Use relative paths for local images
- Optimize image sizes

**Example:**

```markdown
![Project architecture diagram showing the main components](./assets/architecture.png)
```

### 6. Tables

- Use proper markdown table syntax
- Ensure proper alignment
- Include headers

**Example:**

```markdown
| Feature | Status | Notes       |
| ------- | ------ | ----------- |
| Auth    | ✅     | Complete    |
| API     | 🚧     | In progress |
```

## Formatting and Structure

### Line Length

- Limit line length to 80-100 characters for readability
- Maximum 400 characters per line
- Use soft line breaks for long paragraphs

### Whitespace

- Use blank lines to separate sections
- Add blank line before and after code blocks
- Add blank line before and after lists
- Avoid excessive whitespace

### Front Matter

Include YAML front matter at the beginning of the file:

```yaml
---
title: Document Title
description: Brief description of the document
author: Author Name
date: 2026-01-29
tags: [tag1, tag2]
---
```

## Content Quality

### Clarity

- Write clear, concise sentences
- Use active voice
- Avoid jargon unless necessary
- Define technical terms

### Structure

- Start with a brief introduction
- Use headings to organize content logically
- Include examples where helpful
- End with next steps or related resources

### Consistency

- Use consistent terminology throughout
- Follow the same formatting patterns
- Maintain consistent heading capitalization

## Examples

### Good README Structure

````markdown
---
title: Project Name
description: Brief description of what the project does
---

## Overview

Brief introduction to the project and its purpose.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
npm install project-name
```

## Usage

```javascript
import { feature } from 'project-name'

feature.doSomething()
```

## Configuration

Available configuration options:

| Option  | Type   | Default | Description |
| ------- | ------ | ------- | ----------- |
| option1 | string | 'value' | Description |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](./LICENSE) for details.
````

### Good Documentation Page

````markdown
---
title: API Reference
description: Complete API documentation for the service
---

## Authentication

All API requests require authentication using an API key.

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/endpoint
```

## Endpoints

### GET /users

Retrieves a list of users.

**Parameters:**

- `limit` (optional): Maximum number of results (default: 10)
- `offset` (optional): Pagination offset (default: 0)

**Response:**

```json
{
	"users": [{ "id": 1, "name": "John Doe" }],
	"total": 100
}
```

**Example:**

```bash
curl https://api.example.com/users?limit=5
```
````

## Validation

### Tools

- Use markdown linters (markdownlint)
- Validate links with link checkers
- Check spelling and grammar

### Checklist

- ✅ No H1 headings in content
- ✅ All code blocks have language specified
- ✅ All images have alt text
- ✅ Links are valid and descriptive
- ✅ Tables are properly formatted
- ✅ Line length under 100 characters (400 max)
- ✅ Proper front matter included
- ✅ Consistent heading hierarchy

## When to Apply

Apply these standards when:

- Creating README files
- Writing documentation
- Creating guides and tutorials
- Editing existing markdown files
- Creating changelog files
- Writing blog posts or articles
- User asks about markdown formatting
