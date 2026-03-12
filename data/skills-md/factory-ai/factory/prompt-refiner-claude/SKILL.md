---
name: prompt-refiner-claude
description: Refine prompts for Claude models (Opus, Sonnet, Haiku) using Anthropic's best practices. Use when preparing complex tasks for Claude.
---

# Claude Prompt Refiner

Refine prompts to get better results from Claude models by applying Anthropic's recommended patterns.

## When to Use

Invoke this skill when you have a task for Claude that:
- Involves multiple steps or files
- Requires specific output formatting
- Needs careful reasoning or analysis
- Would benefit from structured context

## Refinement Process

### Step 1: Analyze the Draft Prompt

Review the user's prompt for:
- [ ] Clear outcome definition
- [ ] Sufficient context
- [ ] Explicit constraints
- [ ] Success criteria

Ask clarifying questions if any of these are missing.

### Step 2: Apply Claude-Specific Patterns

**Structure with XML tags:**
Claude responds exceptionally well to XML-style tags for organizing complex prompts:

- `<context>` - Background information, codebase state, environment
- `<task>` - The specific action to take
- `<requirements>` - Must-have criteria
- `<constraints>` - Limitations and boundaries
- `<examples>` - Sample inputs/outputs if helpful
- `<output_format>` - How to structure the response

**Ordering matters:**
1. Context first (what exists)
2. Task second (what to do)
3. Requirements third (how to do it)
4. Examples last (clarifying edge cases)

### Step 3: Enhance for Reasoning

For complex tasks, add thinking prompts:
- "Think through the approach before implementing"
- "Consider these edge cases: ..."
- "Explain your reasoning for key decisions"

### Step 4: Output the Refined Prompt

Present the improved prompt with:
- Clear section headers
- XML tags where beneficial
- Specific, measurable criteria
- An explanation of what changed and why

## Example Transformations

### Example 1: Vague Task

**Before:**
```
Add caching to the API
```

**After:**
```
<context>
The /api/products endpoint currently queries the database on every request.
Average response time is 200ms. We use Redis for other caching in the app.
</context>

<task>
Add Redis caching to the /api/products endpoint to reduce database load.
</task>

<requirements>
- Cache TTL of 5 minutes
- Cache invalidation when products are updated
- Graceful fallback to database if Redis is unavailable
- Add cache hit/miss metrics logging
</requirements>

<constraints>
- Don't change the response format
- Must pass existing integration tests
- Use our existing Redis connection from src/lib/redis.ts
</constraints>
```

### Example 2: Code Review Request

**Before:**
```
Review this PR
```

**After:**
```
<context>
This PR adds user authentication to our Next.js application.
Our stack: Next.js 14, TypeScript, Prisma, PostgreSQL.
Security is critical - this handles user sessions and passwords.
</context>

<task>
Review the changes in this PR for security issues, code quality, and adherence to our patterns.
</task>

<requirements>
Focus on:
1. Security vulnerabilities (auth bypass, injection, etc.)
2. Error handling and edge cases
3. TypeScript type safety
4. Test coverage for critical paths
</requirements>

<output_format>
Organize your review as:
## Critical Issues (must fix before merge)
## Recommendations (should consider)
## Minor Suggestions (nice to have)
## What Looks Good (positive feedback)
</output_format>
```

### Example 3: Feature Implementation

**Before:**
```
Add dark mode
```

**After:**
```
<context>
React application using Tailwind CSS for styling.
Currently only has light mode. Design tokens are in tailwind.config.js.
User preference should persist across sessions.
</context>

<task>
Implement dark mode toggle with system preference detection and persistence.
</task>

<requirements>
- Toggle component in the header
- Detect system preference on first visit
- Persist user choice in localStorage
- Smooth transition between modes
- Update all existing components to support both modes
</requirements>

<constraints>
- Use Tailwind's built-in dark mode support
- Don't add new dependencies
- Ensure WCAG AA contrast ratios in both modes
</constraints>

<examples>
Current light mode colors:
- Background: bg-white
- Text: text-gray-900
- Primary: text-blue-600

Expected dark mode equivalents:
- Background: dark:bg-gray-900
- Text: dark:text-gray-100
- Primary: dark:text-blue-400
</examples>
```

## Tips for Best Results

1. **Be specific about scope** - "the auth module" → "src/auth/session.ts"
2. **Include file paths** when relevant
3. **Reference existing patterns** - "follow the pattern in UserService.ts"
4. **State what NOT to do** - constraints prevent unwanted changes
5. **Define done** - what does success look like?
