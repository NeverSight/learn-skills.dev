---
name: buildpad-steering-custom
description: Create custom steering documents for specialized project contexts. Use when creating domain-specific steering files.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
metadata:
  shared-rules: "steering-principles.md"
---

# buildpad-steering-custom Skill

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

## Role
You are a specialized skill for creating custom steering documents beyond core files (product, tech, structure).

## Core Mission
**Role**: Create specialized steering documents beyond core files (product, tech, structure).

**Mission**: Help users create domain-specific project memory for specialized areas.

**Success Criteria**:
- Custom steering captures specialized patterns
- Follows same granularity principles as core steering
- Provides clear value for specific domain

## Execution Steps

### Step 1: Gather Context

If steering context is already available from conversation, skip redundant file reads.
Otherwise:
- Check `.kiro/settings/templates/steering-custom/` for available templates (if that directory does not exist, first copy this skill's bundled `settings-templates/steering-custom/` directory to `.kiro/settings/templates/steering-custom/`)
- Read `rules/steering-principles.md` from this skill's directory for steering principles

## Workflow

1. **Ask user** for custom steering needs:
   - Domain/topic (e.g., "API standards", "testing approach")
   - Specific requirements or patterns to document

2. **Check if template exists**:
   - Load from `.kiro/settings/templates/steering-custom/{name}.md` if available
   - Use as starting point, customize based on project

3. **Analyze codebase** (JIT) for relevant patterns, and record the backend:

#### Parallel Research

The following research areas are independent and can be executed in parallel:
1. **Template & principles**: Load matching template and steering-principles.md
2. **Domain patterns**: Analyze codebase for domain-specific patterns using Glob/Grep/Read

After all parallel research completes, synthesize findings for steering document. Where the document touches the backend (data, sign-in, storage, deployment), record the backend that "Establish the backend first" above established: the Buildpad Engine or Supabase. Never infer the backend from dependency or variable names: an Engine project also carries `@supabase/*` packages and `NEXT_PUBLIC_SUPABASE_*` variables, because it keeps the Supabase client for sign-in.

4. **Generate custom steering**:
   - Follow template structure if available
   - Apply principles from `rules/steering-principles.md` from this skill's directory
   - Focus on patterns, not exhaustive lists
   - Keep to 100-200 lines (2-3 minute read)

5. **Create file** in `.kiro/steering/{name}.md`

## Available Templates

Templates available in `.kiro/settings/templates/steering-custom/`:

1. **api-standards.md** - REST/GraphQL conventions, error handling
2. **testing.md** - Test organization, mocking, coverage
3. **security.md** - Auth patterns, input validation, secrets
4. **database.md** - Schema design, migrations, query patterns
5. **error-handling.md** - Error types, logging, retry strategies
6. **authentication.md** - Auth flows, permissions, session management
7. **deployment.md** - CI/CD, environments, rollback procedures

Load template when needed, customize for project.

## Steering Principles

From `rules/steering-principles.md` (in this skill's directory):

- **Patterns over lists**: Document patterns, not every file/component
- **Single domain**: One topic per file
- **Concrete examples**: Show patterns with code
- **Maintainable size**: 100-200 lines typical
- **Security first**: Never include secrets or sensitive data

## Tool Guidance

- **Read**: Load template, analyze existing code
- **Glob**: Find related files for pattern analysis
- **Grep**: Search for specific patterns
- **Bash** with `ls`: Understand relevant structure

**JIT Strategy**: Load template only when creating that type of steering.

## Output Description

Chat summary with file location (file created directly).

```
Custom Steering Created

## Created:
- .kiro/steering/api-standards.md

## Based On:
- Template: api-standards.md
- Analyzed: src/api/ directory patterns
- Extracted: REST conventions, error format

## Content:
- Endpoint naming patterns
- Request/response format
- Error handling conventions
- Authentication approach

Review and customize as needed.
```

## Examples

### Success: API Standards
**Input**: "Create API standards steering"
**Action**: Load template, analyze src/api/, extract patterns
**Output**: api-standards.md with project-specific REST conventions

### Success: Testing Strategy
**Input**: "Document our testing approach"
**Action**: Load template, analyze test files, extract patterns
**Output**: testing.md with test organization and mocking strategies

## Safety & Fallback

- **No template**: Generate from scratch based on domain knowledge
- **Security**: Never include secrets (load principles)
- **Validation**: Ensure doesn't duplicate core steering content

## Notes

- Templates are starting points, customize for project
- Follow same granularity principles as core steering
- All steering files loaded as project memory
- Custom files equally important as core files
- Avoid documenting agent-specific tooling directories (e.g. `.cursor/`, `.gemini/`, `.claude/`)
- Light references to `.kiro/specs/` and `.kiro/steering/` are acceptable; avoid other `.kiro/` directories
