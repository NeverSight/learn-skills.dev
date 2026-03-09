---
name: deepstack
description: "Detects your project's full technology stack, then generates a comprehensive research prompt tailored to a specific topic like security, performance, or testing."
---

# Deep Stack Research Prompt Generator

Deep stack analysis tool.

Arguments: $ARGUMENTS

## Instructions

Generate a comprehensive deep research prompt for the topic **"$ARGUMENTS"** tailored to the current project's technology stack.

**If no topic is provided**, ask the user what topic they want to research (e.g., security, performance, maintainability, scalability, testing, deployment, accessibility).

---

## Phase 1: Detect the Technology Stack

Analyze the current project to identify all technologies and their versions. Check these files:

### Backend Detection

| File | Technology |
|------|------------|
| `composer.json` | PHP ecosystem (Laravel, Symfony, etc.) — check `require` for framework and PHP version |
| `package.json` | Node.js ecosystem (Express, Fastify, NestJS, etc.) — check for server-side frameworks |
| `requirements.txt` / `pyproject.toml` / `Pipfile` | Python (Django, Flask, FastAPI) |
| `Gemfile` | Ruby (Rails, Sinatra) |
| `go.mod` | Go (Gin, Echo, Fiber) |
| `Cargo.toml` | Rust (Actix, Axum, Rocket) |
| `pom.xml` / `build.gradle` | Java (Spring Boot) |
| `*.csproj` / `*.sln` | .NET (ASP.NET Core) |

### Frontend Detection

Check `package.json` dependencies for:
- **Frameworks**: React, Vue, Svelte, Angular, Solid, Preact, Qwik
- **Meta-frameworks**: Next.js, Nuxt, SvelteKit, Remix, Astro
- **Build tools**: Vite, Webpack, Parcel, esbuild, Turbopack
- **CSS**: Tailwind CSS, Bootstrap, styled-components, Sass, PostCSS

### Integration/Middleware Layer

Look for glue technologies:
- **Inertia.js** (`@inertiajs/vue3`, `@inertiajs/react`, etc.)
- **Livewire** (in `composer.json`)
- **HTMX** (in `package.json` or HTML files)
- **Turbo/Hotwire** (in `package.json` or `Gemfile`)
- **Alpine.js** (often paired with Livewire/HTMX)

### Database Detection

Check these locations:
- `.env` file: `DB_CONNECTION`, `DATABASE_URL`
- `docker-compose.yml`: Database service definitions
- `config/database.php` (Laravel), `settings.py` (Django), etc.
- ORM configs: Prisma (`schema.prisma`), Drizzle, TypeORM, Eloquent

Common databases: MySQL, PostgreSQL, SQLite, MongoDB, Redis, Elasticsearch

### Infrastructure/Other Tools

- **Caching**: Redis, Memcached
- **Search**: Elasticsearch, Meilisearch, Algolia
- **Queues**: Redis, RabbitMQ, SQS
- **Storage**: S3, local filesystem
- **Auth**: Sanctum, Passport, NextAuth, Auth0, Clerk

### Version Detection

For each technology found, extract the version:
- `package.json`: Check `dependencies` and `devDependencies` for exact versions
- `composer.json`: Check `require` section
- Lock files (`package-lock.json`, `composer.lock`) have exact versions
- `.env` or Docker configs may specify database versions

---

## Phase 2: Confirm Stack with User

**IMPORTANT: First output the detected stack as a text message to the user.** Do NOT put the stack details inside the AskUserQuestion tool — the tool has limited space for display.

### Step 1: Display the stack as text output

Output a message like this (with actual detected values):

```
I detected the following technology stack for this project:

**Backend:**
- Rust 1.75
- Tauri 2.0

**Frontend:**
- TypeScript 5.3
- React 18.2
- Vite 5.0
- Tailwind CSS 3.4

**Database:**
- SQLite (via Tauri)

**Desktop:**
- Tauri 2.0 (Rust backend, webview frontend)

**Other:**
- pnpm (package manager)
```

### Step 2: Then ask for confirmation

AFTER displaying the stack details above, use the AskUserQuestion tool with a simple confirmation question:

- Question: "Does this detected stack look correct?"
- Options: "Yes, looks correct" / "Need corrections"

**Wait for user confirmation before proceeding.** If the user provides corrections, incorporate them into the stack.

---

## Phase 3: Generate the Deep Research Prompt

Once the stack is confirmed, generate a comprehensive research prompt. The prompt should be structured for a deep research tool (like Claude, Perplexity, or similar).

### Prompt Template

Generate output in this format (replace placeholders with actual stack details):

---

**START OF GENERATED PROMPT**

I'm working on a web application with the following technology stack:

**Backend:**
- [List each backend technology with version]

**Frontend:**
- [List each frontend technology with version]

**Integration:**
- [List integration/middleware if applicable]

**Database:**
- [List databases and data stores with versions]

**Other:**
- [List other notable tools]

I need comprehensive research on **[TOPIC from $ARGUMENTS]** best practices, patterns, and considerations for this specific stack.

## Research Scope

### 1. Individual Technology Analysis

For each technology in my stack, research:
- **[TOPIC]** best practices specific to this version
- Known issues, vulnerabilities, or limitations related to **[TOPIC]**
- Configuration options that affect **[TOPIC]**
- Common mistakes developers make regarding **[TOPIC]**
- Version-specific considerations (what changed in recent versions)

### 2. Integration Points

Research **[TOPIC]** considerations for these technology combinations:
- [Backend framework] + [Frontend framework] (data flow, state management)
- [Backend] + [Database] (query patterns, connection handling)
- [Integration layer] specifics (if applicable)
- [Any other relevant combinations based on the stack]

Focus on issues that arise specifically from these technologies working together, not just individual concerns.

### 3. Stack-Specific Patterns

Identify **[TOPIC]** patterns and architectures that are:
- Recommended for this exact stack combination
- Anti-patterns to avoid with this stack
- Trade-offs specific to these technology choices

### 4. Real-World Considerations

Research:
- Common **[TOPIC]** issues reported by developers using this stack
- Production lessons learned
- Scaling considerations related to **[TOPIC]**
- Monitoring and observability for **[TOPIC]**

## Requested Output Format

Please provide your findings organized as:

1. **Executive Summary**
   - Top 10 most critical **[TOPIC]** considerations for this stack
   - Priority-ranked action items

2. **Per-Technology Guidelines**
   - Organized by each technology in the stack
   - Specific, actionable recommendations
   - Code examples where helpful

3. **Integration Guidelines**
   - **[TOPIC]** at the boundaries between technologies
   - Data flow considerations
   - Common pitfalls when technologies interact

4. **Known Issues & Gotchas**
   - Version-specific bugs or limitations
   - Documented vulnerabilities (for security topics)
   - Edge cases to watch for

5. **Checklist**
   - Actionable audit checklist for **[TOPIC]**
   - Can be used to review existing code

6. **Anti-Patterns**
   - What NOT to do
   - Common mistakes with this stack
   - Why they're problematic

7. **Resources**
   - Official documentation links
   - Recommended articles, tutorials, talks
   - Tools that help with **[TOPIC]** for this stack

**END OF GENERATED PROMPT**

---

## Phase 4: Present the Output

Output the generated prompt as plain text that the user can easily copy.

Before the prompt, add:

> **Here's your deep research prompt for "[TOPIC]" tailored to your stack. Copy this and paste it into your preferred research tool:**

After the prompt, add:

> **Tip:** This prompt works well with Claude, ChatGPT, Perplexity, or similar AI research tools. For best results, use a tool that can search the web for current information.

---

## Topic-Specific Additions

Depending on the topic provided in `$ARGUMENTS`, emphasize different aspects:

### If topic is "security":
- Emphasize CVEs, OWASP Top 10, authentication, authorization, input validation
- Include encryption, secrets management, dependency vulnerabilities
- Request exploit examples and mitigation strategies

### If topic is "performance":
- Emphasize profiling, caching strategies, database optimization, lazy loading
- Include bundle size, Core Web Vitals, memory management
- Request benchmarking approaches and monitoring tools

### If topic is "testing":
- Emphasize unit, integration, e2e testing strategies for the stack
- Include mocking strategies, test data management, CI/CD integration
- Request coverage goals and testing anti-patterns

### If topic is "maintainability":
- Emphasize code organization, naming conventions, documentation
- Include refactoring patterns, technical debt management
- Request code review checklists and architecture patterns

### If topic is "scalability":
- Emphasize horizontal/vertical scaling, load balancing, caching
- Include database sharding, microservices considerations
- Request capacity planning and bottleneck identification

### If topic is "deployment":
- Emphasize CI/CD, containerization, environment management
- Include rollback strategies, zero-downtime deployments
- Request infrastructure as code and monitoring setup

### If topic is "accessibility":
- Emphasize WCAG compliance, screen reader support, keyboard navigation
- Include ARIA patterns, color contrast, focus management
- Request testing tools and audit approaches

---

## Notes

- Always include version numbers — they matter for accurate research
- If you can't detect a version, note it as "[version unknown]" and ask the user
- The generated prompt should be self-contained and not require additional context
- Tailor the integration section to the actual technologies detected (don't include generic examples)
