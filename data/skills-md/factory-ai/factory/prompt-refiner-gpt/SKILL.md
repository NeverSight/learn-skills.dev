---
name: prompt-refiner-gpt
description: Refine prompts for GPT models (GPT-5, GPT-5.1, Codex) using OpenAI's best practices. Use when preparing complex tasks for GPT.
---

# GPT Prompt Refiner

Refine prompts to get better results from GPT models by applying OpenAI's recommended patterns.

## When to Use

Invoke this skill when you have a task for GPT that:
- Requires a specific persona or expertise
- Involves procedural steps
- Needs structured output
- Benefits from explicit examples

## Refinement Process

### Step 1: Analyze the Draft Prompt

Review the user's prompt for:
- [ ] Clear role/persona definition
- [ ] Step-by-step breakdown (if procedural)
- [ ] Output format specification
- [ ] Concrete examples

Ask clarifying questions if any of these are missing.

### Step 2: Apply GPT-Specific Patterns

**Role framing:**
GPT models respond well to clear role definitions. Start with:
"You are a [specific role] working on [specific context]..."

**Numbered procedures:**
Break complex tasks into numbered steps that build on each other.

**Output specification:**
Be explicit about format: "Return as JSON", "Format as markdown with headers", etc.

**Chain of thought:**
For reasoning tasks, add: "Think through this step by step."

### Step 3: Structure the Prompt

**Effective order for GPT:**
1. Role definition (who/what)
2. Context (background info)
3. Task (what to do)
4. Steps (how to do it, if procedural)
5. Output format (what to return)
6. Examples (optional clarification)

### Step 4: Output the Refined Prompt

Present the improved prompt with:
- Clear role statement
- Numbered steps where applicable
- Explicit output requirements
- An explanation of what changed and why

## Example Transformations

### Example 1: Security Review

**Before:**
```
Review this code for security issues
```

**After:**
```
You are a senior security engineer conducting a security audit of a Node.js payment processing service.

Context: This service handles credit card transactions and communicates with Stripe's API. It runs in AWS ECS with access to a PostgreSQL database.

Task: Review the code in src/payments/ for security vulnerabilities.

Complete these steps:
1. Check for proper input validation on all endpoints
2. Verify secrets are not hardcoded or logged
3. Review authentication and authorization logic
4. Check for SQL injection and XSS vulnerabilities
5. Verify proper error handling that doesn't leak sensitive info
6. Review rate limiting and abuse prevention

Output format:
Return a security report in markdown with these sections:
- **Critical**: Issues that must be fixed before deployment
- **High**: Significant risks that should be addressed soon
- **Medium**: Improvements to consider
- **Recommendations**: General security enhancements

For each issue, include:
- File and line number
- Description of the vulnerability
- OWASP category if applicable
- Recommended fix with code example
```

### Example 2: Refactoring Task

**Before:**
```
Refactor this function to be cleaner
```

**After:**
```
You are a senior TypeScript developer focused on code quality and maintainability.

Context: This function in src/utils/dataProcessor.ts handles data transformation for our analytics pipeline. It currently has high cyclomatic complexity and is difficult to test.

Task: Refactor the processData function to improve readability and testability.

Steps:
1. Analyze the current function and identify code smells
2. Extract logical units into smaller, focused functions
3. Add TypeScript types for all parameters and return values
4. Ensure each extracted function is independently testable
5. Preserve all existing behavior (no functional changes)
6. Add JSDoc comments for public functions

Output format:
1. Brief analysis of issues in the current code (3-5 bullet points)
2. The refactored code
3. List of extracted functions with their responsibilities
4. Example test cases for the new functions
```

### Example 3: API Design

**Before:**
```
Design an API for user management
```

**After:**
```
You are an API architect designing a RESTful API for a B2B SaaS application.

Context: We need user management endpoints for our multi-tenant application. Users belong to organizations, and permissions are role-based (admin, member, viewer).

Task: Design a complete REST API for user management operations.

Requirements:
1. CRUD operations for users
2. Organization membership management
3. Role assignment and permission checking
4. Invitation flow for new users
5. Password reset functionality

Constraints:
- Follow REST best practices
- Use consistent naming conventions
- Support pagination for list endpoints
- Include proper error responses

Output format:
For each endpoint, provide:
- HTTP method and path
- Request body schema (if applicable)
- Response schema
- Possible error codes
- Example request/response

Use OpenAPI 3.0 YAML format for the specification.
```

### Example 4: Debugging

**Before:**
```
Why is this test failing?
```

**After:**
```
You are a senior developer debugging a failing test in a React application.

Context: The test in UserProfile.test.tsx is failing intermittently in CI but passes locally. The component fetches user data and displays it.

Task: Analyze the test and identify the root cause of the flaky failure.

Think through this step by step:
1. What async operations does the test involve?
2. Are there any race conditions?
3. Is the test properly waiting for state updates?
4. Are mocks set up correctly?
5. Could there be timing issues with the test environment?

Output format:
1. Most likely root cause (1-2 sentences)
2. Evidence supporting your diagnosis
3. Recommended fix with code
4. How to verify the fix works
```

## Tips for Best Results

1. **Define the role clearly** - "senior security engineer" > "developer"
2. **Number your steps** - GPT follows ordered lists reliably
3. **Specify output format explicitly** - JSON, markdown, etc.
4. **Use "Think through this step by step"** for reasoning tasks
5. **Provide examples** when the expected format is complex
6. **Include constraints** to prevent scope creep
