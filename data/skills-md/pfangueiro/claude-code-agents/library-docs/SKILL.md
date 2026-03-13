---
name: library-docs
description: Quick access to up-to-date library documentation using MCP. Use this skill when you need to reference official documentation for libraries, frameworks, or APIs. Leverages the context7 MCP server to fetch current docs for React, Next.js, Vue, MongoDB, Supabase, and hundreds of other libraries. Complements the documentation-maintainer agent.
---

# Library Docs

## Overview

This **MCP-powered skill** provides instant access to up-to-date library documentation through the context7 MCP server. Instead of searching documentation manually or relying on potentially outdated information, this skill fetches current, authoritative documentation directly from library maintainers.

## When to Use This Skill

- Looking up API references for libraries
- Understanding how specific features work
- Finding code examples from official docs
- Verifying correct usage patterns
- Checking latest syntax and best practices
- Comparing different library approaches
- Complementing the **documentation-maintainer agent**

## MCP Integration

This skill leverages the **context7 MCP server** which provides access to documentation for hundreds of popular libraries.

### How It Works

1. **MCP Server Connection**: Claude Code connects to context7 MCP server
2. **Library Resolution**: Convert library name to Context7-compatible ID
3. **Documentation Fetch**: Retrieve up-to-date documentation
4. **Context Integration**: Load relevant docs into conversation

### Available Tools

The context7 MCP server provides two tools:

**`mcp__context7__resolve-library-id`**
- Converts a library name to Context7-compatible ID
- Example: "react" → "/facebook/react"
- Handles version-specific requests

**`mcp__context7__get-library-docs`**
- Fetches documentation for a library
- Supports topic-specific queries
- Configurable token limits

## Common Usage Patterns

### Pattern 1: Basic Library Lookup

**User Request:**
```
"Show me React hooks documentation"
```

**Workflow:**
1. Resolve "react" to library ID using MCP
2. Fetch React documentation focused on "hooks"
3. Present relevant hooks documentation

**Example MCP Calls:**
```javascript
// Step 1: Resolve library ID
mcp__context7__resolve-library-id({ libraryName: "react" })
// Returns: "/facebook/react"

// Step 2: Get docs
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks"
})
```

### Pattern 2: Specific Version

**User Request:**
```
"How does routing work in Next.js 14?"
```

**Workflow:**
1. Resolve "Next.js 14" to version-specific ID
2. Fetch Next.js v14 routing documentation
3. Explain routing with v14-specific features

**Example MCP Calls:**
```javascript
// Resolve with version
mcp__context7__resolve-library-id({ libraryName: "Next.js 14" })
// Returns: "/vercel/next.js/v14.x.x"

// Get routing docs
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/vercel/next.js/v14.x.x",
  topic: "routing"
})
```

### Pattern 3: API Comparison

**User Request:**
```
"Compare MongoDB and Supabase query syntax"
```

**Workflow:**
1. Resolve both library IDs
2. Fetch query documentation for each
3. Present side-by-side comparison

**Example MCP Calls:**
```javascript
// Fetch MongoDB docs
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/mongodb/docs",
  topic: "queries"
})

// Fetch Supabase docs
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/supabase/supabase",
  topic: "queries"
})
```

### Pattern 4: Focused Topic Research

**User Request:**
```
"I need comprehensive information on React Server Components"
```

**Workflow:**
1. Resolve React library ID
2. Fetch docs with larger token limit for depth
3. Focus specifically on Server Components topic

**Example MCP Calls:**
```javascript
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "server components",
  tokens: 10000  // More tokens for comprehensive coverage
})
```

## Supported Libraries

The context7 MCP server supports hundreds of libraries. Common ones include:

**Frontend Frameworks:**
- React (`/facebook/react`)
- Vue (`/vuejs/core`)
- Angular (`/angular/angular`)
- Svelte (`/sveltejs/svelte`)
- Next.js (`/vercel/next.js`)
- Nuxt (`/nuxt/nuxt`)

**Backend & Databases:**
- MongoDB (`/mongodb/docs`)
- PostgreSQL
- Supabase (`/supabase/supabase`)
- Prisma (`/prisma/prisma`)

**Tools & Libraries:**
- Tailwind CSS (`/tailwindlabs/tailwindcss`)
- TypeScript (`/microsoft/TypeScript`)
- Vite (`/vitejs/vite`)

*And hundreds more...*

## Integration with Agents

### documentation-maintainer Agent

**Synergy**: This skill provides source documentation, while the documentation-maintainer agent creates project-specific docs.

**Workflow Example:**
```
User: "Document our authentication system"

1. library-docs skill → Fetch auth library documentation
2. documentation-maintainer agent → Create docs using library patterns
3. Result: Consistent documentation following library conventions
```

### api-backend Agent

**Synergy**: This skill provides API reference, while api-backend implements the code.

**Workflow Example:**
```
User: "Implement Stripe payment integration"

1. library-docs skill → Fetch Stripe API documentation
2. api-backend agent → Implement using current Stripe patterns
3. Result: Correct, up-to-date implementation
```

### frontend-specialist Agent

**Synergy**: This skill provides component documentation, while frontend-specialist builds UI.

**Workflow Example:**
```
User: "Create a data table with React"

1. library-docs skill → Fetch React table library docs
2. frontend-specialist agent → Build component following patterns
3. Result: Modern component using best practices
```

## Best Practices

### DO:
- ✅ Specify library versions when relevant
- ✅ Use topic parameter to narrow results
- ✅ Combine with agents for implementation
- ✅ Reference official docs for correctness
- ✅ Check docs when libraries update

### DON'T:
- ❌ Assume docs are current without checking
- ❌ Skip version specifications for major changes
- ❌ Ignore deprecation warnings in docs
- ❌ Mix patterns from different library versions

## Example Workflows

### Workflow 1: Learning New Library

```
User: "I'm new to Supabase, show me how to get started"

Steps:
1. Use library-docs to fetch Supabase getting started guide
2. Review authentication patterns
3. See database query examples
4. Understand real-time subscriptions

Output: Comprehensive introduction with official examples
```

### Workflow 2: Debugging API Usage

```
User: "Why isn't my Next.js API route working?"

Steps:
1. Use library-docs to fetch Next.js API routes documentation
2. Compare user's code with official patterns
3. Identify discrepancies
4. Suggest corrections based on docs

Output: Fix based on current Next.js best practices
```

### Workflow 3: Migration Guide

```
User: "Help me migrate from Vue 2 to Vue 3"

Steps:
1. Fetch Vue 2 documentation for current patterns
2. Fetch Vue 3 documentation for new patterns
3. Identify breaking changes
4. Provide migration steps with examples

Output: Detailed migration guide with official references
```

## MCP Server Setup

### Prerequisites

The context7 MCP server should be configured in Claude Code settings.

**Typical Configuration:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

### Verification

To verify the MCP server is available, Claude Code should show context7 in the MCP servers list.

## Limitations & Considerations

**Token Limits:**
- Default: 5000 tokens
- Max configurable: Higher for comprehensive topics
- Balance depth vs context usage

**Library Coverage:**
- Most popular libraries supported
- Some niche libraries may not be available
- Check context7 documentation for full list

**Update Frequency:**
- Documentation refreshed regularly
- May have slight lag for very recent releases
- Always verify critical production changes

## Quick Reference

**Fetch Library Docs:**
```javascript
// Resolve library name
mcp__context7__resolve-library-id({
  libraryName: "library-name"
})

// Get documentation
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/org/project",
  topic: "optional-topic",
  tokens: 5000
})
```

**Common Queries:**
- "Show me {library} {feature} documentation"
- "How to use {library} for {task}"
- "What's new in {library} version {X}"
- "Compare {library A} vs {library B} for {use case}"

## Resources

### References
- Context7 documentation
- MCP server configuration guide
- Supported libraries list

### Related Skills
- documentation-maintainer: Create project docs
- code-review-checklist: Verify against library patterns

### Related Agents
- documentation-maintainer: Auto-generate documentation
- api-backend: Implement backend using library patterns
- frontend-specialist: Build UI following library conventions

---

**This is an MCP-powered skill** - It demonstrates how Skills can leverage MCP servers for enhanced capabilities. The context7 MCP server provides the data source, while this skill provides the knowledge of how to use it effectively.
