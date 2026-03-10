---
name: prompt-compression
description:
  Compress documentation, prompts, and context into minimal tokens for AGENTS.md and CLAUDE.md.
  Achieves 80%+ token reduction while preserving agent accuracy.
metadata:
  tags: agents-md, prompt-compression, context-window, token-optimization
---

## When to use

Use this skill when compressing documentation, framework references, API indexes, coding guidelines,
or any structured knowledge into a compact format for inclusion in AGENTS.md, CLAUDE.md, or system
prompts. The goal is maximum information density with minimum token usage.

## Background

Vercel's research (January 2026) showed that an 8KB compressed docs index in AGENTS.md achieved a
100% eval pass rate, compared to 53% baseline and 79% for skills with explicit trigger instructions.
Passive context (always loaded) beats active retrieval (agent must decide to invoke) because it
eliminates the decision point. Compression is the key enabler -- it makes passive context viable
without blowing up the context window.

## Critical Rules

### 1. Use Pipe-Delimited Index Format for File References

**Wrong (agents do this):**

```markdown
## Documentation

- Getting Started: See docs/getting-started.md for installation instructions
- Routing: See docs/routing.md for route definitions
- API Routes: See docs/api-routes.md for API endpoint documentation
```

**Correct:**

```markdown
[Docs Index]|root: ./docs |getting-started:{installation.md,project-structure.md}
|routing:{defining-routes.md,dynamic-routes.md,middleware.md}
|api:{endpoints.md,auth.md,validation.md}
```

**Why:** The pipe-delimited format cuts tokens by 70-80% while remaining parseable by every major
LLM. Agents can still locate and read specific files when needed.

### 2. Compress Rules into Single-Line Directives

**Wrong (agents do this):**

```markdown
## Coding Standards

### Import Organization

When writing imports, always organize them in the following order:

1. Built-in Node.js modules (fs, path, etc.)
2. External dependencies (react, express, etc.)
3. Internal modules (relative imports)
4. Type imports

Make sure to separate each group with a blank line.
```

**Correct:**

```markdown
[Standards] |imports: builtin > external > internal > types (blank line between groups)
```

**Why:** Agents don't need conversational explanation. A compressed directive carries the same
behavioral instruction in 5% of the tokens.

### 3. Strip Explanatory Prose, Keep Only Actionable Content

**Wrong:**

```markdown
## Authentication

Our application uses JWT-based authentication. When a user logs in, the server generates a JWT token
that contains the user's ID and role. This token is sent back to the client and stored in an
httpOnly cookie. On subsequent requests, the middleware extracts the token from the cookie, verifies
it, and attaches the user object to the request.

The token expires after 24 hours, at which point the user must log in again. Refresh tokens are not
currently implemented but are planned for a future release.
```

**Correct:**

```markdown
[Auth]|JWT in httpOnly cookie|24h expiry|no refresh tokens |middleware: extract token > verify >
attach user to req |login flow: validate creds > generate JWT(id,role) > set cookie
```

**Why:** Agents need the behavioral contract (what to do), not the narrative (why it was built this
way). Remove history, motivation, and future plans.

### 4. Use Abbreviated Keys and Symbols

**Wrong:**

```markdown
- Required: true
- Type: string
- Default value: "production"
- Minimum length: 3
- Maximum length: 50
```

**Correct:**

```markdown
|env: required string="production" len:3-50
```

**Why:** Standard abbreviations (req, opt, str, int, bool, len, min, max, def) are universally
understood by LLMs and compress structured metadata by 80%+.

### 5. Flatten Nested Hierarchies

**Wrong:**

```markdown
## Project Structure

### Source Code

#### Components

##### UI Components

- Button.tsx
- Input.tsx
- Modal.tsx

##### Layout Components

- Header.tsx
- Footer.tsx
- Sidebar.tsx
```

**Correct:**

```markdown
[Structure]|src/ |components/ui:{Button,Input,Modal}.tsx
|components/layout:{Header,Footer,Sidebar}.tsx
```

**Why:** Markdown heading hierarchy wastes tokens on whitespace and repetition. Brace expansion and
path prefixes are denser and equally readable to agents.

### 6. Add Retrieval-Led Reasoning Directive

Always include this directive when the compressed context references retrievable files:

```markdown
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for any [DOMAIN] tasks.
```

**Why:** Without this, agents default to training data (which may be stale). This single line shifts
behavior from "guess from memory" to "look it up," which was the key factor in Vercel's 100% pass
rate.

### 7. Preserve Structural Boundaries

**Wrong:**

```markdown
routingdefiningdynamicmiddlewareapiendpointsauthvalidation
```

**Correct:**

```markdown
|routing:{defining,dynamic,middleware} |api:{endpoints,auth,validation}
```

**Why:** Over-compression destroys parseability. Keep logical grouping with delimiters (pipes,
braces, colons). The agent must be able to navigate to a specific file or section.

### 8. Target 8-15KB for Complete Framework Indexes

A full framework docs index (file tree pointing to retrievable docs) should compress to 8-15KB. This
is the sweet spot where:

- It fits comfortably in AGENTS.md alongside project-specific context
- Token cost per request stays under 2-4K tokens
- Agent accuracy reaches near-perfect on framework-specific tasks

If the compressed output exceeds 15KB, split into a primary index (most-used APIs) and a secondary
index that the agent can read on demand.

## Compression Process

1. **Identify the source** - docs directory, API reference, coding guidelines, framework docs
2. **Extract actionable content** - strip prose, motivation, history, examples that duplicate the
   rule
3. **Choose format** - pipe-delimited index for file trees, single-line directives for rules,
   abbreviated keys for config/schema
4. **Compress** - apply abbreviations, brace expansion, path prefixes, symbol shorthand
5. **Add retrieval directive** - if output references readable files
6. **Validate** - check that an agent can still locate any specific piece of information
7. **Measure** - compare token count before/after, target 70-80% reduction

## Output Formats

### File Index (for docs directories)

```markdown
[Topic Index]|root: ./path |IMPORTANT: Prefer retrieval-led reasoning over pre-training-led
reasoning for [TOPIC] |section-a/subsection:{file1.md,file2.md,file3.md}
|section-b:{file1.md,file2.md}
```

### Rules/Standards (for coding guidelines)

```markdown
[Standards] |naming: camelCase vars, PascalCase components, UPPER_SNAKE constants |imports:
builtin > external > internal > types |errors: always use Result<T,E>, never throw in library code
|tests: colocate with source, name: \*.test.ts, min coverage 80%
```

### API Reference (for endpoint documentation)

```markdown
[API]|base: /api/v2 |GET /users?page,limit -> User[]|auth:bearer |POST /users {name,email,role?} ->
User|auth:admin |DELETE /users/:id -> void|auth:admin
```

### Config/Schema (for structured metadata)

```markdown
[Config] |db: host=localhost port=5432 pool:5-20 timeout:30s |cache: redis ttl:5m max:1000
prefix:"app:" |auth: jwt secret=$JWT_SECRET exp:24h algo:HS256
```

## Anti-Patterns

- Compressing content that agents already know well (basic language syntax, standard library)
- Removing code examples that demonstrate non-obvious API usage
- Compressing error messages or edge case documentation (agents need these verbatim)
- Creating compression so aggressive that a human can't review or maintain it
- Putting full documentation content in AGENTS.md instead of an index pointing to files
- Forgetting the retrieval-led reasoning directive
