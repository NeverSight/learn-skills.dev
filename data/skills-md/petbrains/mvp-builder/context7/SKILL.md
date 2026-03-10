---
name: context7
description: Up-to-date library documentation retrieval using Context7 MCP tools. Process THINK → RESOLVE → FETCH → APPLY. Use when fetching library docs, resolving package names to IDs, getting implementation guides, exploring API references. Provides package resolution strategy, trust score evaluation, token scaling (3K-20K), topic selection patterns.
allowed-tools: Read, Write, Bash (*), mcp__context7__resolve-library-id, mcp__context7__get-library-docs
---

# Context7 Documentation Retrieval

Framework for using `/mcp__context7__resolve-library-id` and `/mcp__context7__get-library-docs` tools effectively.

Process: **THINK → RESOLVE → FETCH → APPLY**

## Command: `/mcp__context7__resolve-library-id`

Resolves a package name to a Context7-compatible library ID.

### Parameters
- `libraryName` (required): Library name to search for

### Returns
List of matching libraries (10-30+ results) with:
- **Context7-compatible library ID**: Format `/org/project`
- **Trust Score**: Authority indicator (1-10, higher is better)
- **Code Snippets**: Number of available examples
- **Description**: Library summary

### Selection Process
Priority order:
1. **Name similarity** (exact matches always win)
2. **Trust score** (minimum 7 preferred, 9-10 ideal)
3. **Documentation coverage** (higher snippet counts)
4. **Description relevance** to query intent

**Decision rules:**
- Exact name + trust ≥7 → Select it
- Multiple high-trust (≥9) → Choose highest snippet count
- Low trust (<7) → Prioritize snippet count
- Ambiguous → Request user clarification

**Skip resolve when:**
- User provides path like `/vercel/next.js`
- Query contains `/org/project` format

**Always resolve when:**
- User mentions name only: "React", "Next.js"
- Generic terms: "React docs"

### Common Patterns
```
"react" → /reactjs/react.dev (trust: 10)
"next.js" → /vercel/next.js (trust: 9.5)
"vue" → /vuejs/core (trust: 10)
"mongodb" → /mongodb/docs (trust: 9.8)
```

## Command: `/mcp__context7__get-library-docs`

Fetches documentation using exact Context7-compatible library ID.

### Parameters
- `context7CompatibleLibraryID` (required): Exact ID from resolve step
- `topic` (optional): Specific focus area
- `tokens` (optional): Max tokens (default: 10000, range: 1000-20000)

### Token Strategy
- **3K-5K:** Quick reference (single function/method)
- **6K-10K:** Feature exploration
- **10K-15K:** Implementation guides
- **15K-20K:** Comprehensive learning

### Topic Selection
Be specific with multi-word topics:
- ❌ "api" → ✅ "REST API endpoints"
- ❌ "hooks" → ✅ "useState useEffect lifecycle"
- ❌ "css" → ✅ "responsive design breakpoints"

## Workflows

### React Implementation
```
THINK: Need React infinite scroll docs
RESOLVE: /mcp__context7__resolve-library-id libraryName="react"
SELECT: /reactjs/react.dev (trust: 10)
FETCH: /mcp__context7__get-library-docs context7CompatibleLibraryID="/reactjs/react.dev" topic="infinite scroll virtualization" tokens=12000
```

### Next.js Debugging
```
THINK: Debug hydration errors
RESOLVE: /mcp__context7__resolve-library-id libraryName="next.js"
SELECT: /vercel/next.js (trust: 9.5)
FETCH: /mcp__context7__get-library-docs context7CompatibleLibraryID="/vercel/next.js" topic="hydration errors debugging SSR" tokens=15000
```

### Direct ID Usage
```
THINK: User provided /mongodb/docs
FETCH: /mcp__context7__get-library-docs context7CompatibleLibraryID="/mongodb/docs" topic="aggregation pipeline" tokens=15000
```

## Error Handling

**No matches:** Try alternative names (vue.js → vue)  
**Multiple matches:** Ask user preference  
**Wrong library:** Re-run with different term  
**Insufficient docs:** Increase tokens or refine topic

## Best Practices

1. **Think before executing** - What does user really need?
2. **Resolve first** - Unless user provides `/org/project`
3. **Be specific with topics** - Multi-word topics work better
4. **Scale tokens appropriately** - Don't always use maximum
5. **Chain related fetches** - Build complete context
6. **Trust score matters** - Prefer libraries with scores ≥7

## Quick Reference

1. **THINK:** What library and documentation needed?
2. **RESOLVE:** `/mcp__context7__resolve-library-id libraryName="[package]"`
3. **SELECT:** Based on trust, snippets, relevance
4. **FETCH:** `/mcp__context7__get-library-docs context7CompatibleLibraryID="[id]" topic="[specific]" tokens="[appropriate]"`
5. **APPLY:** Use documentation to answer question