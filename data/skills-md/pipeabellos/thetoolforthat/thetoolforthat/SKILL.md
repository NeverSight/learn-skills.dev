---
name: thetoolforthat
description: Guide for discovering 540+ developer tools, design resources, AI platforms, and agencies using the thetoolforthat MCP server. Use when asked to find tools for a project, recommend tech stack components, discover design agencies, or search for specific tool categories.
---

# The Tool For That - MCP Skill

This skill teaches you how to effectively use the thetoolforthat MCP server to help users discover developer tools, design resources, AI platforms, agencies, and more from a curated collection of 540+ resources.

## Available MCP Tools

| Tool | Description | When to Use |
|------|-------------|-------------|
| `search-tools` | Search by keyword, tool name, or category | User asks for specific tools or searches by name |
| `list-categories` | List all categories and subcategories | User wants to explore what's available |
| `get-tools-by-category` | Get all tools in a category | User wants everything in a specific category |
| `recommend-tools` | Get recommendations for a use case | User describes what they're building |

## Tool Usage Patterns

### 1. Search Tools (`search-tools`)

Best for finding specific tools or searching by keywords.

**Parameters:**
- `query` (required): Search term - can be a keyword, tool name, or category
- `category` (optional): Filter results to a specific category
- `limit` (optional): Maximum results (default: 20)

**Example queries:**
- "animation" - finds animation tools and libraries
- "React" - finds React-related tools
- "Vercel" - finds a specific tool by name

### 2. List Categories (`list-categories`)

Returns the complete taxonomy of categories and subcategories. Use this first when users want to explore or aren't sure what they need.

**No parameters required.**

### 3. Get Tools by Category (`get-tools-by-category`)

Returns all tools in a specific category or subcategory.

**Parameters:**
- `category` (required): Category or subcategory name (case-insensitive, partial match)

**Example categories:**
- "Component Libraries"
- "Design Agencies"
- "AI Agents & Automation"

### 4. Recommend Tools (`recommend-tools`)

Analyzes a use case description and returns relevant tools ranked by relevance.

**Parameters:**
- `useCase` (required): Description of what the user is building or needs

**Example use cases:**
- "building a SaaS dashboard with authentication"
- "need animation libraries for React"
- "setting up monitoring for a Node.js API"

## Workflow Guidelines

### When User Asks for Recommendations

1. Use `recommend-tools` with their description
2. Present results organized by relevance
3. Include tool name, URL, and brief description
4. Suggest related categories if applicable

### When User Searches for Something Specific

1. Use `search-tools` with their query
2. If too many results, suggest filtering by category
3. If no results, suggest alternative search terms

### When User Wants to Explore

1. Use `list-categories` to show available options
2. Once they pick a category, use `get-tools-by-category`
3. Highlight standout tools with context

## Response Formatting

When presenting tools to users:

```
**[Tool Name](url)** - Brief description
Category: Main Category > Subcategory
```

For multiple recommendations, group by category:

```
## Animation Tools

**[Rive](https://rive.app/)** - Design and animation tool for interactive motion-based designs
**[Motion](https://motion.dev/)** - JavaScript animation library for fluid, interactive animations

## Component Libraries

**[shadcn/ui](https://ui.shadcn.com/)** - Customizable React components built on Radix UI
```

## Category Overview

The collection is organized into these main categories:

- **Infrastructure & DevOps** - Deployment, secrets, testing, monitoring
- **Backend & Data** - Databases, search, web scraping
- **AI & Machine Learning** - Model hosting, frameworks, voice, agents
- **Frontend & UI** - Component libraries, design kits, state management
- **Design & Creative** - Animation, 3D, design resources, icons
- **Video & Media** - AI video, screen recording, infrastructure
- **Developer Tools** - IDEs, terminal, API clients, documentation
- **Authentication & Security** - Auth providers, compliance
- **Communication** - Notifications, SMS, email, real-time
- **Business Tools** - Support, CRM, forms, marketing, sales
- **Finance & Payments** - Payments, accounting
- **Mobile & Desktop** - Cross-platform, React Native, app store
- **Hiring & Operations** - Talent, contracts, productivity
- **Boilerplates & Starters** - Starter kits and templates
- **Agencies & Designers** - Design agencies and individual designers
