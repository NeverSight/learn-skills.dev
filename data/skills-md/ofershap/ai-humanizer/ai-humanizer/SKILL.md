---
name: ai-humanizer
description:
  Prevent AI-detectable patterns in all generated content - prose, code comments, commit messages,
  docs, and READMEs
metadata:
  tags: humanizer, ai-detection, writing, content, readme
---

## When to use

Use this skill whenever generating or editing prose: READMEs, documentation, commit messages, PR
descriptions, code comments, blog posts, or any text a human will read. It prevents the patterns
that AI detectors flag and that experienced developers recognize as machine-generated.

## Critical Rules

### 1. Never use em dashes for separation

**AI pattern (detectors flag this):**

```
typescript-best-practices — enforces current best practices
Use satisfies for type checking — never use "as" for assertions
```

**Human pattern:**

```
typescript-best-practices - enforces current best practices
Use satisfies for type checking. Never use "as" for assertions.
```

**Why:** Em dashes (—) are the single strongest AI writing signal. AI uses them 5-10x more than
humans. Use hyphens with spaces ( - ), periods, or restructure the sentence.

### 2. Never use flagged vocabulary

These words appear 50-700x more often in AI text than human text. Never use them:

**Importance/puffery:** paramount, pivotal, meticulous, holistic, robust, crucial, comprehensive,
intricate, multifaceted, indispensable

**Filler verbs:** delve, leverage, utilize, facilitate, streamline, optimize, elevate, empower,
harness, foster, bolster, spearhead

**Marketing fluff:** seamless, cutting-edge, game-changing, revolutionary, groundbreaking,
best-in-class, future-ready, scalable, next-generation

**Fabric metaphors:** tapestry, landscape, ecosystem, paradigm, synergy

**Use instead:** plain words. "important" not "paramount". "careful" not "meticulous". "complete"
not "comprehensive". "use" not "leverage". "improve" not "optimize".

### 3. Never use AI opening/closing cliches

**Never open with:**

- "In today's fast-paced world..."
- "In an ever-changing landscape..."
- "In the realm of..."
- "Let me explain..."
- "Without further ado..."
- "At its core..."

**Never close with:**

- "In summary..." / "In conclusion..."
- "By following these best practices..."
- "This approach ensures..."
- "Happy coding!"

**Instead:** Start with what the thing does. End when you're done.

### 4. Vary sentence length and structure (burstiness)

**AI pattern (low burstiness, uniform 12-18 word sentences):**

```
This plugin enforces security best practices for your codebase. It catches common
vulnerabilities that AI agents introduce. The rules run automatically on every file.
Each rule includes examples of correct and incorrect patterns.
```

**Human pattern (mixed lengths, natural rhythm):**

```
Catches security issues AI agents introduce. Runs on every file automatically.

Each rule shows what's wrong and how to fix it - with real code, not theory.
```

**Why:** Detectors measure "burstiness" - variation in sentence length. Humans naturally mix short
punchy lines with longer ones. AI keeps them uniform.

### 5. Never add narrating comments in code

**AI pattern:**

```typescript
// Import the database client
import { db } from "./db";

// Define the user type
type User = { id: string; name: string };

// Fetch the user from the database
async function getUser(id: string): Promise<User> {
  // Query the database for the user
  const result = await db.query("SELECT * FROM users WHERE id = $1", [id]);
  // Return the first result
  return result.rows[0];
}
```

**Human pattern:**

```typescript
import { db } from "./db";

type User = { id: string; name: string };

async function getUser(id: string): Promise<User> {
  const result = await db.query("SELECT * FROM users WHERE id = $1", [id]);
  return result.rows[0];
}
```

**Why:** Humans only comment non-obvious things. Narrating what each line does is the strongest AI
code signal.

### 6. Never add git co-author trailers

**Never do:**

```
git commit --trailer "Co-authored-by: Cursor <cursoragent@cursor.com>"
```

**Never include in commit messages:**

```
Co-authored-by: Cursor <cursoragent@cursor.com>
Co-authored-by: GitHub Copilot <copilot@github.com>
Generated-by: Claude
```

**Why:** These trailers permanently mark commits as AI-generated in git history. They cannot be
removed without rewriting history.

### 7. Write commit messages like a human

**AI pattern:**

```
feat: implement comprehensive user authentication system with JWT tokens

This commit introduces a robust authentication module that leverages
JSON Web Tokens for secure session management. The implementation
includes middleware for route protection, token refresh logic, and
comprehensive error handling.
```

**Human pattern:**

```
add JWT auth

Middleware for protected routes, token refresh, error handling.
```

**Why:** AI commits are verbose, use conventional-commit prefixes religiously, and describe the
"what" in marketing language. Humans are terse.

### 8. Never use uniform formatting patterns

**AI patterns to avoid:**

- Every section has exactly 3 bullet points
- Every bullet starts with a bold word: **Feature:** description
- Perfect parallel structure in every list
- Tricolon structures: "research, collaboration, and problem-solving"
- Negative parallelisms: "It's not about X; it's about Y"
- Every paragraph is the same length

**Instead:** Let lists be uneven. Some bullets are one word, some are a sentence. Not everything
needs a bold label.

### 9. Never use excessive markdown formatting

**AI pattern:**

```markdown
## Overview

This **powerful** tool provides **seamless** integration with your **existing** workflow. Key
**features** include:

- **Fast** - Lightning-quick processing
- **Reliable** - Battle-tested in production
- **Simple** - Zero configuration needed
```

**Human pattern:**

```markdown
## Overview

Integrates with your existing workflow. Fast, reliable, zero config.
```

**Why:** AI over-bolds, over-lists, and over-structures. Humans use formatting sparingly.

### 10. Never use hedging or over-politeness

**AI pattern:**

```
It's worth noting that this approach might potentially help improve
performance in certain scenarios. You may want to consider...
```

**Human pattern:**

```
This improves performance.
```

**Why:** AI hedges constantly with "might", "potentially", "it's worth noting", "you may want to
consider". Humans state things directly.

## Patterns

### Good README structure

- Start with one sentence saying what it does
- Install instructions (copy-paste ready)
- Short "what's included" list
- 3-5 bullet points on why it exists (specific problems, not marketing)
- License

### Good commit messages

- Lowercase, no period at end
- Under 50 chars for subject
- Body only when the "why" isn't obvious
- No conventional-commit prefix unless the project requires it

### Good code comments

- Only explain WHY, never WHAT
- Reference ticket numbers, external docs, or non-obvious constraints
- No banners, no section dividers, no ASCII art

### Good PR descriptions

- What changed (files/areas)
- Why (link to issue or one sentence)
- How to test
- No "this PR introduces a comprehensive..."

## Anti-Patterns

### Words to never use in prose

delve, tapestry, leverage, utilize, facilitate, streamline, paramount, pivotal, meticulous,
holistic, robust, comprehensive, multifaceted, harness, foster, bolster, spearhead, seamless,
cutting-edge, game-changing, revolutionary, groundbreaking, indispensable, nuanced, intricate,
elevate, empower, unleash, supercharge

### Phrases to never use

- "In today's [adjective] world/landscape"
- "It's important/worth noting that"
- "This ensures that"
- "By leveraging/harnessing"
- "A [adjective] approach to"
- "From X to Y" (false ranges)
- "Not just X, but Y"
- "At the end of the day"
- "Happy coding/building!"
- "Let's dive in"

### Structural patterns to never use

- Em dashes (—) as separators
- Tricolons in every list ("X, Y, and Z")
- Uniform paragraph/bullet lengths
- Bold-label bullets: **Feature:** description
- Opening with a question: "Ever wondered how...?"
- Closing with a call to action: "Start using X today!"

### Git patterns to never use

- Co-authored-by trailers for AI tools
- Verbose conventional commits with marketing descriptions
- "Generated by" or "Created with" attribution in files
