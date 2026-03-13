---
name: project-analyzer
description: Quickly understand and analyze software project architecture, structure, and organization. Use this skill when users want to understand a new codebase, analyze project structure, identify entry points, understand project layers and architecture, find configuration files, map dependencies, get onboarded to an unfamiliar project, or when they ask questions like "help me understand this project", "what's the architecture", "where do I start reading this code", "explain this codebase", or "analyze this repository". Also triggers when users upload project directories or ask about project organization.
---

# Project Analyzer

Systematically analyze software projects to understand architecture, entry points, layers, and key files. This skill helps quickly onboard to unfamiliar codebases by mapping structure and identifying critical components.

## Analysis Workflow

Follow this workflow to analyze projects efficiently:

### 1. Run Automated Analysis

First, use the provided script to generate a comprehensive project overview:

```bash
python3 scripts/analyze_project.py <project_path>
```

This automatically identifies:
- Project type and primary languages
- File distribution across extensions
- Entry points (main files)
- Configuration files with descriptions
- Dependencies from package managers
- Basic architecture patterns
- Directory structure tree

### 2. Examine Key Configuration Files

Based on the analysis, read critical config files to understand:

**Dependencies and frameworks:**
- `package.json` - Node.js dependencies, scripts, project metadata
- `requirements.txt` / `pyproject.toml` - Python dependencies
- `Cargo.toml` - Rust dependencies
- `go.mod` - Go modules
- `pom.xml` / `build.gradle` - Java dependencies

**Framework configuration:**
- `next.config.js` - Next.js settings
- `vite.config.js` - Vite bundler
- `tsconfig.json` - TypeScript compiler
- `webpack.config.js` - Webpack bundler

**Environment and deployment:**
- `.env.example` - Required environment variables
- `docker-compose.yml` - Service definitions
- `Dockerfile` - Container setup

### 3. Identify Entry Points

Trace execution flow starting from entry points found in analysis:

**Common entry points by project type:**
- **Web apps**: `index.js`, `app.js`, `server.js`, `main.py`
- **Next.js**: `pages/_app.js` or `app/layout.js`
- **APIs**: `server.js`, `app.py`, `main.go`
- **CLIs**: `cli.js`, `__main__.py`, `main.rs`

Read entry point to understand initialization, middleware setup, and routing.

### 4. Map Project Layers

Identify and document the purpose of each layer using common patterns. Consult `references/architecture_patterns.md` for detailed explanations of:

- Frontend layers (components, pages, state, utils)
- Backend layers (routes, services, models, middleware)
- Full-stack structures (monorepo, microservices)
- Common architecture patterns (MVC, Clean Architecture, etc.)

### 5. Understand Data Flow

For web applications, trace a typical request/response:

1. **Route definition** - Where endpoints are defined
2. **Middleware** - Auth, validation, logging
3. **Controller/Handler** - Request processing
4. **Service layer** - Business logic
5. **Data layer** - Database queries
6. **Response formatting** - Serializers, transformers

### 6. Analyze Code Patterns

Use `references/code_reading.md` for strategies on:

- Reading order and priority
- Framework-specific reading paths
- Pattern recognition techniques
- Understanding dependencies
- Identifying code smells and anti-patterns

### 7. Generate Summary

Create a structured summary including:

**Project Overview:**
- Project type and tech stack
- Primary languages and frameworks
- Architecture pattern used

**Entry Points:**
- Main execution files
- How to run/start the project

**Layer Breakdown:**
- Purpose of each major directory
- What code lives where
- Data flow between layers

**Key Configuration:**
- Important config files and their purpose
- Environment variables needed
- External services/APIs integrated

**Development Workflow:**
- How to install dependencies
- How to run locally
- Testing approach
- Build/deployment process

**Notable Patterns:**
- Architecture decisions
- Code organization principles
- Special conventions or structures

## Tips for Effective Analysis

**Start high-level, go deeper as needed:**
- First pass: Project type, structure, entry points
- Second pass: Layer purposes, data flow
- Deep dive: Specific features or complex areas only when requested

**Use search efficiently:**
- `grep -r "TODO\|FIXME"` - Known issues
- `grep -r "class.*Controller"` - Find controllers
- `grep -r "def test_"` - Find tests

**Prioritize understanding over completeness:**
- Focus on answering the user's specific questions
- Don't document every file unless requested
- Highlight important/unusual patterns

**Consider the user's goal:**
- New contributor: Focus on setup, architecture, conventions
- Bug fixing: Find relevant code areas, testing approach
- Feature addition: Understand existing patterns, extension points
- Code review: Architecture decisions, code quality patterns

## Resources

**Scripts:**
- `scripts/analyze_project.py` - Automated project analysis tool that scans directory structure, identifies project type, finds entry points and config files, extracts dependencies, and generates formatted output

**References:**
- `references/architecture_patterns.md` - Common software architecture patterns, project layers, structure indicators, and configuration files reference
- `references/code_reading.md` - Strategies for reading and understanding code, framework-specific paths, pattern recognition, and anti-patterns to watch for

Load reference files when deeper context is needed beyond the automated analysis.
