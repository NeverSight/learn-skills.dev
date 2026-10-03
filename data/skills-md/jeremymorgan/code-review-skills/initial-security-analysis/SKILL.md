---
name: initial-security-analysis
description: Performs a first-pass security audit of project structure and attack surface to map risk and entry points. Use as the starting point for a security review.
license: CC0-1.0
metadata:
  category: security
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

# Initial Project Analysis

**Perform a Project Structure Audit**

Analyze the entire project structure and identify:

1. All entry points (app.js, server.js, etc.)
2. All routes and endpoints
3. Middleware chain and order
4. External service integrations
5. Database connection points
6. Authentication/authorization flow
7. File upload handling locations
8. API rate limiting implementation

Start by detecting the tech stack (language, framework, package manager), then examine the core files appropriate for that stack:

- **Node.js/Express**: `package.json`, `app.js`/`server.js`, `routes/`, `middleware/`
- **Python (Django/Flask/FastAPI)**: `requirements.txt`/`pyproject.toml`, `settings.py`/`app.py`, URL config, middleware config
- **Java/Spring**: `pom.xml`/`build.gradle`, `application.properties`, controller and filter/interceptor classes
- **Ruby/Rails**: `Gemfile`, `config/routes.rb`, `app/controllers/`, `config/initializers/`
- **Go**: `go.mod`, `main.go`, router registration files
- **PHP/Laravel**: `composer.json`, `routes/`, `app/Http/Middleware/`, `bootstrap/app.php`

For other stacks, locate the equivalent dependency manifest, entry point, routing layer, and middleware chain.

---

## Provide:

A structured finding report with the following for each issue:

Title, Severity (Critical/High/Medium/Low), CWE (if applicable), Evidence (file, function, line ranges), and a short Why it matters.

Exploitability notes and, where safe, a minimal PoC or reproduction steps (no real secrets).

Remediation: precise code-level fix or config change (snippets welcome), plus defense-in-depth guidance.

A summary risk score (0–10) and top 3–5 prioritized fixes that reduce risk fastest.

A checklist diff: which items from the “Check for” list are Pass/Fail/Not Applicable.

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
